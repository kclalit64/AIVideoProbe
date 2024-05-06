import pyttsx3
import speech_recognition as sr
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask import Flask, request, jsonify
from flask import render_template
import requests
import time
import openai
import os
from openai import OpenAI
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

requests.packages.urllib3.disable_warnings()

engine = pyttsx3.init()
recognizer = sr.Recognizer()
engine.setProperty('volume', 1.0)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 for male voice, 1 for female voice
engine.setProperty('rate', 150) 
app = Flask(__name__)

resume = "Komal Bhole B-Tech IT, VIIT Pune I'm excited to start my career and bring my skills onto the table. I'm a quick learner and eager to take on new challenges. I'm looking forward to connecting with other professionals in the industry and exploring new opportunities. komal.22010509@viit.ac.in 7499203665 Pune, India 02 June, 2003 linkedin.com/in/komal-bhole-4904a2204 github.com/KOMAL616 EDUCATION B-Tech - Information Technology Vishwakarma Institute of Information Technology 01/2021 - Present, 9.19 HSC Board Brijilal Biyani Science College, Amravati SKILLSC C++ Python(Numpy, Pandas, Matplotlib) Java HTML Git/GitHub CSS DBMS(MySql) Operating System Figma Data Structure and Algorithms Oops Php Computer Networking PERSONAL PROJECTS Vegetable Ordering Website (06/2022 - 12/2022) Enable customers to order vegetables online Convenient and hassle-free way to purchase vegies. Technologies used: Html, Css, Javascript, Php, MySql. Health App (Healthify (01/2023 - 04/2023) Booking appointments from any hybrid location.. Unique QR code consisting of all the minute details of patient AI based chatbot for clearing basic doubts. Technologies Used : Java , Xml, Kotlin, Firebase. Built a React CI/CD Pipeline using CircleCI 1. Collaborate with the team to develop and implement machine learning algorithms and models 2. Assist in collecting, cleaning, and analyzing large datasets to derive actionable insights 3. Develop and maintain data preprocessing pipelines for efficient data handling 4. Contribute to the design and development of NLP models for text classification and sentiment analysis 5. Research cutting-edge ML techniques and stay updated with the latest advancements in the field 6. Assist in building and improving ML models for personalized recommendations and content filtering 7. Help with the deployment and monitoring of ML models in production environments Join us and make a significant impact in revolutionizing the way people access knowledge and grow personally through our innovative platform. Apply now and take the first step towards an exciting career in Machine Learning with MentorBoxx! Skill(s) requiredData Analytics Machine Learning Natural Language Processing (NLP)Python"
# Position = "Software Developer"
# job_description = "Design, develop, and test software solutions Collaborate with cross-functional teams to define, design, and ship new features Strong programming skills in languages like Java, Python, or C++"
# Company_Name = "Google"


questions = ""
conversation_log = []
n = 0
conversation_user = ""
timestamps = []
next_question = ""
system_prompt = ""
# system_prompt = [  {"role": "system", "content": f"Hi GPT, you are  acting as an interviewer in this exercise. You are to interview me for {Position} at {Company_Name} with the job description posted as {job_description}. My resume is as follows:{resume}In This exercise you are  conducting my interview and current conversation log is as {conversation_log} if it is empty means it is first question,   Whenever, I would be conversing with you, the ChatGPT model and not as the interviewer,  After the interview, you are to assess me based on the following five aspects:Technical Skills: Assessing the candidate's proficiency in the specific technical skills required for the job. Behavioural Skills: Evaluating communication, teamwork, adaptability, and other interpersonal skills. Problem-Solving and Critical Thinking: Assessing analytical thinking, decision-making, and the ability to handle challenges. Cultural Fit: Examining alignment with the company's values, culture, and the ability to work within a team. Work Experience and Achievements: Reviewing past experiences, achievements, and contributions to understand the candidate's capabilities and potential impact. Hence, please note to ask questions such that all of these aspects can be evaluated and considered in the question set.  currently you have asked {n}  number of questions and the number of questions  should strictly not exceed 3, Once the questions exceed the limit. Simply respond with the following response: EXIT_0 at the start of the responce and greet the candidate and announce that interview is over and instruct him to wait for feedack" }]


client = OpenAI(api_key='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')
@app.route("/")
def home():
    return render_template("index.html")


import datetime
@app.route("/start", methods=['POST'])
def start_interview():
    name = request.form.get('name')
    job_title = request.form.get('job_title')
    job_description = request.form.get('job_description')
    company_name = request.form.get('company_name')
    interviewer = request.form.get('interviewer')

    global questions, n, conversation_log, system_prompt, timestamps, next_question
    initial_prompt = f"Generate an initial interview question."
    
    question = generate_question([*system_prompt, {"role": "user", "content": initial_prompt}])
    print(question)
    conversation_log.append({"role": "assistant", "content": question})
    speak(question)

    system_prompt = [  {"role": "system", "content": f"Hi GPT, you are  acting as an interviewer in this exercise. You are to interview me for {job_description} at {company_name} with the job description posted as {job_description}. My resume is as follows:{resume}In This exercise you are  conducting my interview and current conversation log is as {conversation_log} if it is empty means it is first question,   Whenever, I would be conversing with you, the ChatGPT model and not as the interviewer,  After the interview, you are to assess me based on the following five aspects:Technical Skills: Assessing the candidate's proficiency in the specific technical skills required for the job. Behavioural Skills: Evaluating communication, teamwork, adaptability, and other interpersonal skills. Problem-Solving and Critical Thinking: Assessing analytical thinking, decision-making, and the ability to handle challenges. Cultural Fit: Examining alignment with the company's values, culture, and the ability to work within a team. Work Experience and Achievements: Reviewing past experiences, achievements, and contributions to understand the candidate's capabilities and potential impact. Hence, please note to ask questions such that all of these aspects can be evaluated and considered in the question set.  currently you have asked {n}  number of questions and the number of questions  should strictly not exceed 3, Once the questions exceed the limit. Simply respond with the following response: EXIT_0 at the start of the responce and greet the candidate and announce that interview is over and instruct him to wait for feedack" }]

    continue_interview = True
    while continue_interview:

        if n>3:
            last_question = "Hello there! I must say, your interview went  well. Now, please patiently wait for the feedback. It won't take long, and I'm sure you'll find it insightful. Great job again, and thank you for your time during the interview!"
            print(last_question)
            speak(last_question)
            feedback = generate_feedback(conversation_log)
            error_count = count_grammar_errors(conversation_user)
            conversation_duration = timestamps[-1] - timestamps[0] if timestamps else 1
            fluency_percentage = calculate_fluency(conversation_duration, error_count)
            print(f"Fluency Percentage: {fluency_percentage:.2f}%")
            file_name = "Interview_Report1.pdf"
            conversation = "" 
            generate_pdf()
            print("Interview section PDF generated successfully.")
            continue_interview = False
        else:
            n = n+1
            start_time = time.time()  
            timestamps.append(start_time)
            response = listen()
            print(response)
            end_time = time.time()  # Record the end time
            timestamps.append(end_time)
            conversation_log.append({"role": "user", "content": response})
            follow_up_prompt = " generate a follow-up question."
            next_question = generate_question([*system_prompt, {"role": "user", "content": follow_up_prompt}])
            print(next_question)
            if n<4:
                speak(next_question)

            conversation_log.append({"role": "assistant", "content": next_question})
    return '', 200

def generate_question(prompt):
    chat_completion = client.chat.completions.create(
          messages = prompt,
          model="gpt-3.5-turbo",
          max_tokens=4096,
          top_p=0.9,)
    
    question = chat_completion.choices[0].message.content
    return question

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

def calculate_fluency(conversation_duration, error_count):
    max_errors_per_minute = 10
    conversation_duration_minutes = conversation_duration / 60
    max_allowable_errors = max_errors_per_minute * conversation_duration_minutes
    fluency_percentage = 100 - ((error_count / max_allowable_errors) * 100)
    return max(0, fluency_percentage)

def speak(text):
    engine.say(text)
    engine.startLoop(False)
    engine.iterate()
    engine.endLoop()

def generate_feedback(conversation):
    prompt = f"""
    You are required to evaluate and provide structured feedback based on an interview. The conversation log of the interview is captured as {conversation}.
    Evaluation Criteria: Assess the candidate across the following key aspects:

    Technical Skills: Evaluate the proficiency in the required technical skills for the position.

    Behavioral Skills: Assess communication, teamwork, adaptability, and other interpersonal skills.

    Problem-Solving and Critical Thinking: Analyze the candidate's ability to handle challenges through decision-making and analytical thinking.

    Cultural Fit: Determine the alignment with the company's values and team compatibility.

    Work Experience and Achievements: Review past job experiences, achievements, and contributions to gauge potential impact.

    Feedback Format: Provide the feedback segmented by the aspects above. Each section should contain:

    Section Name: [Name of the section being assessed]
    Score: [Numeric score out of 100, reflecting the candidate’s performance in that section]
    Evaluation Metrics Table:
    Sr. No
    Topic Name: [Specific topics within each section you have evaluated]
    Remarks: [Provide up to 4 bullet points including both strengths and areas for improvement]
    Resources: [Recommendations for resources, such as websites or books, to help the candidate improve]
    Summary:
    Overall analysis of the candidate’s performance in this section.
    Highlight both strengths and areas requiring improvement.
    Justify the score given.
    """
    system = [{"role": "system", "content": prompt}]
    feedback = generate_question(system)
    return feedback

def generate_pdf():
    doc = SimpleDocTemplate("interview_sections.pdf", pagesize=letter, leftMargin=50, rightMargin=50, topMargin=50, bottomMargin=50, \
                            title="Interview Sections", showBoundary=1)
    styles = getSampleStyleSheet()

    # Define content for the PDF
    content = []

    # Insert Section 1 title
    section1_title = Paragraph("<b><i>Section 1</i></b>", styles["Title"])
    section1_title.alignment = 1  # Center alignment
    content.append(section1_title)

    # Add a spacer for gap
    content.append(Spacer(1, 20))

    # Page 1: Technical Section
    content.extend(generate_section("Technical Section", 85, [
        ("1", "Python Programming", "Good understanding", "Official Python Documentation"),
        ("2", "Data Structures", "Needs improvement", "GeeksforGeeks"),
        ("3", "Algorithms", "Excellent", "Introduction to Algorithms."),
        ("4", "Database Management", "Moderate knowledge", "SQL Documentation"),
        ("5", "Web Development", "Basic understanding", "MDN Web Docs")
    ]))

    # Page break
    content.append(PageBreak())

    section1_title = Paragraph("<b><i>Section 2</i></b>", styles["Title"])
    section1_title.alignment = 1  # Center alignment
    content.append(section1_title)

    content.append(Spacer(1, 20))
    # Page 2: Behavioural Skills Section
    content.extend(generate_section("Behavioural Skills", 75, [
        ("1", "Communication", "Proven effective communication", "Example resource"),
        ("2", "Teamwork", "Collaborative team player", "Example resource"),
        ("3", "Problem Solving", "Strong problem-solving abilities", "Example resource"),
        ("4", "Leadership", "Inspiring natural leadership", "Example resource"),
        ("5", "Adaptability", "Quickly adapts to situations", "Example resource")
    ]))

    # Page break
    content.append(PageBreak())

    section1_title = Paragraph("<b><i>Section 3</i></b>", styles["Title"])
    section1_title.alignment = 1  # Center alignment
    content.append(section1_title)
    content.append(Spacer(1, 20))

    # Page 3: Problem-Solving and Critical Thinking
    content.extend(generate_section("Problem-Solving and Critical Thinking", 90, [
        ("1", "Analytical Thinking", "Analytical problem-solving", "Example resource"),
        ("2", "Creativity", "Ability to think outside the box", "Example resource"),
        ("3", "Decision Making", "Decisive under pressure", "Example resource"),
        ("4", "Critical Thinking", "Strong critical thinking skills", "Example resource"),
        ("5", "Logical Reasoning", "Systematic problem-solving", "Example resource")
    ]))

    # Page break
    content.append(PageBreak())
    section1_title = Paragraph("<b><i>Section 4</i></b>", styles["Title"])
    section1_title.alignment = 1  # Center alignment
    content.append(section1_title)
    content.append(Spacer(1, 20))
    # Page 4: Cultural Fit
    content.extend(generate_section("Cultural Fit", 80, [
        ("1", "Team Collaboration", "Works well in diverse teams", "Example resource"),
        ("2", "Company Values Alignment", "Cultural alignment", "Example resource"),
        ("3", "Adaptability", "Adaptable to company culture", "Example resource"),
        ("4", "Respect for Diversity", "Fosters diversity", "Example resource"),
        ("5", "Open Communication", "Fosters open communication", "Example resource")
    ]))

    # Page break
    content.append(PageBreak())
    section1_title = Paragraph("<b><i>Section 5</i></b>", styles["Title"])
    section1_title.alignment = 1  # Center alignment
    content.append(section1_title)
    content.append(Spacer(1, 20))

    # Page 5: Work Experience and Achievements
    content.extend(generate_section("Work Experience and Achievements", 95, [
        ("1", "Project Management", "Complex project management", "Example resource"),
        ("2", "Technical Skills", "Proven technical expertise", "Example resource"),
        ("3", "Leadership Experience", "Team milestone leadership", "Example resource"),
        ("4", "Industry Recognition", "Award-winning contributions", "Example resource"),
        ("5", "Contributions to Community", "Community initiative involvement", "Example resource")
    ]))

    # Build PDF
    doc.build(content)

# Function to generate section content
def generate_section(title, score, topics):
    styles = getSampleStyleSheet()

    content = []

    # Heading with blue color box
    heading_style = styles["Heading1"]
    heading_style.textColor = colors.white
    heading_style.backColor = colors.blue
    heading_style.alignment = 1  # Center alignment
    content.append(Paragraph(title, heading_style))

    # Score section
    score_paragraph = Paragraph(f"Score: {score}/100", styles["Heading2"])
    content.append(score_paragraph)

    # Add 25px top padding between Score section and table
    content.append(Spacer(1, 25))

    # Side heading for Evaluation Metrics
    evaluation_heading_style = styles["Heading2"]
    evaluation_heading_style.alignment = 0  # Left alignment
    content.append(Paragraph("Evaluation Metrics", evaluation_heading_style))

    # Table data
    table_data = [["Sr. No", "Topic", "Remarks", "Resources"]]
    for sr_no, topic, remarks, resources in topics:
        table_data.append([sr_no, topic, remarks, resources])

    # Define table style
    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.blue),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black),
                              ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Border around the entire table
                              ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Border around each cell
                              ('INNERGRID', (0, 0), (-1, -1), 1, colors.black)])  # Inner grid lines

    # Create table
    section_table = Table(table_data)
    section_table.setStyle(table_style)

    # Set width for all columns
    col_widths = [60, 150, 150, 150]
    section_table._argW = col_widths

    # Set row heights
    section_table.setStyle(TableStyle([('SIZE', (0, 0), (-1, -1), 10)]))

    # Enable word wrapping for all columns
    section_table.setStyle(TableStyle([('WORDWRAP', (0, 0), (-1, -1), True)]))

    # Add table to content
    content.append(section_table)

    # Side heading for Summary
    summary_heading_style = styles["Heading2"]
    summary_heading_style.alignment = 0  # Left alignment
    content.append(Paragraph("Summary", summary_heading_style))

    return content
if __name__ == '_main_':
    app.run(debug=True)