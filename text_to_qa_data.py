from transformers import BartForConditionalGeneration, BartTokenizer
from transformers import T5Tokenizer, T5ForConditionalGeneration
from transformers import pipeline
from pytube import YouTube
import pandas as pd
import re

# Load pre-trained BART model and tokenizer
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

def get_summary(input_text):
    # Input text to be summarized
    input_text = input_text

    # Split input text into smaller chunks (max token length for BART is 1024)
    max_token_length = 1024
    chunks = [input_text[i:i+max_token_length] for i in range(0, len(input_text), max_token_length)]

    # Generate summaries for each chunk and combine them
    generated_summaries = []
    for chunk in chunks:
        input_ids = tokenizer.encode("summarize: " + chunk, return_tensors="pt", max_length=max_token_length, truncation=True)
        summary_ids = model.generate(input_ids, max_length=150, min_length=50, do_sample=False)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        generated_summaries.append(summary)

    return generated_summaries

def generate_questions(summary):
    tokenizer = T5Tokenizer.from_pretrained('valhalla/t5-base-e2e-qg')
    model = T5ForConditionalGeneration.from_pretrained('valhalla/t5-base-e2e-qg')
    final_questions = []
    for text in summary:
      inputs = tokenizer.encode("generate questions: " + text, return_tensors="pt", max_length=512, truncation=True)
      question_ids = model.generate(inputs, max_length=100, num_return_sequences=3, num_beams=4, early_stopping=True)
      questions = [tokenizer.decode(question_id, skip_special_tokens=True) for question_id in question_ids]
      final_questions.append(questions)
    return final_questions

def get_answers(summary,fquestions):
  tquestions = []
  for question in fquestions:
    que = []
    for quest in question:
      quest = quest.split('? <sep>')
      for i in quest:
        if i != '' and i not in que:
          que.append(i.strip())
    tquestions.append(que)

  # Initialize the question-answering pipeline
  question_answerer = pipeline("question-answering")

  # Input text and question for extracting answer
  answers = []
  for context , questions in zip(summary,tquestions):
    ans = []
    for q1 in questions:
      answer = question_answerer(question=q1, context=context)
      ans.append(answer['answer'])
    answers.append(ans)


  questions1 = []
  answers1  = []
  for i in range(len(tquestions)):
    for j in range(len(tquestions[i])):
      questions1.append(tquestions[i][j])
      answers1.append(answers[i][j])
  return questions1 , answers1

def gererate_question_answers_csv_file(questions1,answers1,outfile_path):
  dt = {}
  for i,j in zip(questions1,answers1):
    if i.lower() not in dt and j.lower() not in dt.values():
      dt[i.lower()] = j.lower()
      
  df2 = {"Question":dt.keys(),"Answer":dt.values()}
  data = pd.DataFrame(df2)

  data.to_csv(f"{outfile_path}/question_answer.csv")

def sanitize_filename(filename):
    # Replace invalid characters with underscores
    sanitized_filename = re.sub(r'[\/:*?"<>|]', '_', filename)
    return sanitized_filename
# Generate questions from the summary using beam search
url = "https://www.youtube.com/watch?v=aywZrzNaKjs"
yt = YouTube(url)
outfile_path = f"YoutubeVideoTranscribeQAData/{sanitize_filename(yt.title)}"
textfile_path = f"YoutubeVideoTranscribeQAData/{sanitize_filename(yt.title)}/transcribe.txt"
with open(textfile_path,'r') as f:
    text = f.read()

summary = get_summary(text)
fquestions = generate_questions(summary)

questions1 , answers1 = get_answers(summary,fquestions)

gererate_question_answers_csv_file(questions1,answers1,outfile_path)