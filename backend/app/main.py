from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

import pyttsx3
import speech_recognition as sr
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import request, jsonify
from flask import render_template
import requests
import time
import openai
import os
from openai import OpenAI
requests.packages.urllib3.disable_warnings()

# Initialize the speech engine for text-to-speech conversion
engine = pyttsx3.init()

# Initialize the recognizer for speech recognition
recognizer = sr.Recognizer()

# Set the volume (0.0 to 1.0)
engine.setProperty('volume', 1.0)

# Change the voice to female
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 for male voice, 1 for female voice

# Reduce the speaking rate
engine.setProperty('rate', 150) 

app = Flask(__name__)
global questions, n, conversation_log

resume = "name - Abhay Gotmare, education - BTech Computer Science, ..."
job_description = "Machine Learning Engineer responsibilities ..."
Position = "Machine Learning Engineer"
Company_Name = "infogen global"
questions = ""
conversation_log = []
n = 0

# System prompt to be used in API module
system_prompt = [  {"role": "system", "content": f"Hi GPT, you are  acting as an interviewer in this exercise. You are to interview me for {Position} at {Company_Name} with the job description posted as {job_description}. My resume is as follows:{resume}In This exercise you are  conducting my interview and current conversation log is as {conversation_log} if it is empty means it is first question,  currently you have asked {n}  number of questions and questions  should strictly not exceed the range of 3 to 5..  Whenever, I would be conversing with you, the ChatGPT model and not as the interviewer,  After the interview, you are to assess me based on the following five aspects:Technical Skills: Assessing the candidate's proficiency in the specific technical skills required for the job. Behavioural Skills: Evaluating communication, teamwork, adaptability, and other interpersonal skills. Problem-Solving and Critical Thinking: Assessing analytical thinking, decision-making, and the ability to handle challenges. Cultural Fit: Examining alignment with the company's values, culture, and the ability to work within a team. Work Experience and Achievements: Reviewing past experiences, achievements, and contributions to understand the candidate's capabilities and potential impact. Hence, please note to ask questions such that all of these aspects can be evaluated and considered in the question set. Once you are done with the interview questions. Simply respond with the following response: EXIT_0 and greet the candidate and announce that interview is over and instruct him to wait for feedack" }]


client = OpenAI(api_key='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')
@app.route("/")
def home():
    return render_template("index.html")



@app.route("/start", methods=['GET'])
def start_interview():
    initial_prompt = f"Generate an initial interview question."
    question = generate_question([*system_prompt, {"role": "user", "content": initial_prompt}])
    conversation_log.append({"role": "assistant", "content": question})
    speak(question)
    interview_loop()  # Start the interactive interview loop
    return '', 200

def interview_loop():
    global conversation_log
    continue_interview = True
    while continue_interview:
        user_input = listen()
        conversation_log.append({"role": "user", "content": user_input})
        
        if "EXIT_0" in user_input:
            feedback = generate_feedback(conversation_log)
            speak("Interview is over. Please wait for your feedback.")
            speak(feedback)  # Optionally speak the feedback
            continue_interview = False
        else:
            follow_up_prompt = " generate a follow-up question."
            next_question = generate_question([*system_prompt, {"role": "user", "content": follow_up_prompt}, *conversation_log])
            speak(next_question)
            conversation_log.append({"role": "assistant", "content": next_question})
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to generate questions
def generate_question(prompt):
    chat_completion = client.chat.completions.create(
          messages = prompt,
          model="gpt-3.5-turbo",
          max_tokens=4096,
          top_p=0.9,)
    question = chat_completion.choices[0].message.content
    return question

# Function to convert speech to text
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I did not understand that."
        except sr.RequestError as e:
            return f"Sorry, an error occurred. {e}"

# Function to count grammar errors
def count_grammar_errors(conversation):
    total_errors = 0
    language_tool_url = "https://languagetool.org/api/v2/check"
    data = {
        "text": conversation,
        "language": "en-US"
    }
    response = requests.post(language_tool_url, data=data, verify=False)
    if response.ok:
        matches = response.json()["matches"]
        total_errors = len(matches)
    return total_errors

# Function to calculate fluency percentage


# Function to generate feedback
def generate_feedback(conversation):
    prompt = f"you have to evaluate and provide feedback for interview of a candidate which has the conversation log as {conversation} you are to assess candidate based on the following five aspects: Technical Skills: Assessing the candidate's proficiency in the specific technical skills required for the job. Behavioural Skills: Evaluating communication, teamwork, adaptability, and other interpersonal skills. Problem-Solving and Critical Thinking: Assessing analytical thinking, decision-making, and the ability to handle challenges. Cultural Fit: Examining alignment with the company's values, culture, and the ability to work within a team. Work Experience and Achievements: Reviewing past experiences, achievements, and contributions to understand the candidate's capabilities and potential impact. The feedback  should be strictly in the following format for all the mentioned aspects: Section X:  Score: The score would be calculated based on the candidates performance for that particular section out  f 100. This should be accurate and should be calculated considering all the aspects relevant to the section.  Evaluation Metrics Table: This would be a table consisting of the following columns: Sr. No Topic Name: This refers to the topic you evaluated in the section Remarks: Your remarks in bullet points for the topic; try to include both positive and negative remarks here (at max 4). Keep this as descriptive as possible but short. You are free to use phrases to mind the word limit.  Resources: A list of websites, books or any helpful resource that can be used by the candidate to improve on his weak aspects and points for the topic evaluated Summary: This section should be a summary of a candidate's performance for the section mentioning the shortcomings, positive aspects, wrong responses and overall justification for the grading. The scope of improvement for the candidate and the other"
    system = [{"role": "system", "content": prompt}]
    feedback = generate_question(system)
    return feedback

# Function to generate PDF
def generate_pdf(conversation, file_name):
    c = canvas.Canvas(file_name, pagesize=letter)
    y = 750  # Starting y position
    for line in conversation:
        c.drawString(50, y, line)
        y -= 15  # Adjust spacing between lines
    c.save()

if __name__ == '__main__':
    app.run(debug=True)