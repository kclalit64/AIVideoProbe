import pyttsx3
import speech_recognition as sr
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

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
engine.setProperty('rate', 150)  # Adjust this value as needed (default is 200)

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

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

# Function to analyze resume and frame questions
def analyze_resume(resume):
    # Mock implementation to frame questions based on resume
    # You can replace this with your actual implementation
    questions = [
        "Tell me about your experience as a {job_title}.",
        "What skills do you have related to {skill_1} and {skill_2}?",
        "Can you provide an example of a project where you used {skill_3}?",
        "How do you handle {experience}?",
        "Why are you interested in this position at {company}?",
        "How would you contribute to our team?",
        "Do you have any questions for us?"
    ]
    return questions

# Function to conduct the mock interview
def conduct_interview(questions):
    conversation = []
    for question in questions:
        speak(question)
        response = listen()
        conversation.append(f"Interviewer: {question}\nCandidate: {response}\n")
    return conversation

# Function to generate PDF from conversation
def generate_pdf(conversation, file_name):
    c = canvas.Canvas(file_name, pagesize=letter)
    y = 750  # Starting y position
    for line in conversation:
        c.drawString(50, y, line)
        y -= 15  # Adjust spacing between lines
    c.save()

# Resume analysis and interview flow
resume = {
    "job_title": "Software Engineer",
    "skill_1": "Python",
    "skill_2": "JavaScript",
    "skill_3": "React",
    "experience": "challenging situations",
    "company": "ABC Corp"
}

speak("Welcome to the mock interview. Let's begin by analyzing your resume.")
questions = analyze_resume(resume)
speak("Now, let's start the interview.")
conversation = conduct_interview(questions)
speak("Thank you for participating in the mock interview.")

# Generate PDF from conversation
generate_pdf(conversation, "interview_conversation.pdf")
print("Conversation saved to interview_conversation.pdf")
