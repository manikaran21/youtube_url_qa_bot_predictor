<h1>Youtube URL QA Bot Predictor</h1>

1. In this project we have three files
 * video_to_text.py file : Is is used to convert youtube url video to text file and taht file is stored in YoutubeVideoTranscribeData folder
 * text_to_qa_data.py : It is used to generate question and answers csv file from the transcribed text .
 * app.py : It is used to run the application .

2. So , to run this application , follow the below steps:
  1. Clone this project repository into your local system 
  2. Go to the project directory
  3. Install the packages :<br>
        *  pip install -r requirements.txt
  4. Run the application :<br>
        *  streamlit run app.py

3.If you want to change the youtube video then follow below steps:
  1. Change the "url" variable in all .py files .
  2. First run the video_to_text.py file .
  3. Next , run the text_to_qa_data.py file .
  4. Finally , run the app.py file : <br>
        *  streamlit run app.py

