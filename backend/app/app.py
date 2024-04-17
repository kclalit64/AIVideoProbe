from flask import Flask, request, jsonify
from flask import render_template
import openai
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key='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')

# Candidate and Job Description Information
resume = "name - Abhay Gotmare, education - BTech Computer Science, ..."
job_description = "Machine Learning Engineer responsibilities ..."
Position = "Machine Learning Engineer"
Company_Name = ""
prompt = ""
conversation = ""
n = ""
# Initial System Prompt
system_prompt = [{"role": "system", "content": f"Hi GPT, you are  acting as an interviewer in this exercise. You are to interview me for {Position} at {Company_Name} with the job description posted as {job_description}. My resume is as follows:{resume}In This exercise you are  conducting my interview and current conversation log is as {conversation} if it is empty means it is first question,  currently you have asked {n}  number of questions and questions  should strictly not exceed the range of 30 - 50..  Whenever, I would be conversing with you, the ChatGPT model and not as the interviewer,  After the interview, you are to assess me based on the following five aspects:Technical Skills: Assessing the candidate's proficiency in the specific technical skills required for the job. Behavioural Skills: Evaluating communication, teamwork, adaptability, and other interpersonal skills. Problem-Solving and Critical Thinking: Assessing analytical thinking, decision-making, and the ability to handle challenges. Cultural Fit: Examining alignment with the company's values, culture, and the ability to work within a team. Work Experience and Achievements: Reviewing past experiences, achievements, and contributions to understand the candidate's capabilities and potential impact. Hence, please note to ask questions such that all of these aspects can be evaluated and considered in the question set. Once you are done with the interview questions. Simply respond with the following response: EXIT_0 and greet the candidate and announce that interview is over and instruct him to wait for feedack  "}]

conversation_log = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['GET'])
def start_interview():
    initial_prompt = f"Generate an initial interview question."
    question = generate_question([*system_prompt, {"role": "user", "content": initial_prompt}])
    conversation_log.append({"role": "assistant", "content": question})
    return jsonify({"question": question})

@app.route('/submit', methods=['POST'])
def submit_response():
    data = request.json
    candidate_response = data['response']
    conversation_log.append({"role": "user", "content": candidate_response})

    if len(conversation_log) < 5:  # Limiting to 3 questions (question + response pairs)
        follow_up_prompt = "Considering the last question and response, generate a follow-up question."
        question = generate_question([*system_prompt, {"role": "user", "content": follow_up_prompt}, *conversation_log])
        conversation_log.append({"role": "assistant", "content": question})
        return jsonify({"question": question})
    else:
        feedback = generate_feedback("\n".join([item["content"] for item in conversation_log]))
        logs = "\n".join([item["content"] for item in conversation_log])
        return jsonify({"feedback": feedback, "conversation_log" :logs})
    print(conversation_log)

def generate_question(prompt):
    chat_completion = client.chat.completions.create(
          messages = prompt,
          model="gpt-3.5-turbo",
          max_tokens=4096,
          top_p=0.9,)
    question = chat_completion.choices[0].message.content
    return question

def generate_feedback(conversation):
    prompt = f"you have to evaluate and provide feedback for interview of a candidate which has the conversation log as {conversation} you are to assess candidate based on the following five aspects: Technical Skills: Assessing the candidate's proficiency in the specific technical skills required for the job. Behavioural Skills: Evaluating communication, teamwork, adaptability, and other interpersonal skills. Problem-Solving and Critical Thinking: Assessing analytical thinking, decision-making, and the ability to handle challenges. Cultural Fit: Examining alignment with the company's values, culture, and the ability to work within a team. Work Experience and Achievements: Reviewing past experiences, achievements, and contributions to understand the candidate's capabilities and potential impact. The feedback  should be strictly in the following format for all the mentioned aspects: Section X:  Score: The score would be calculated based on the candidate’s performance for that particular section out  f 100. This should be accurate and should be calculated considering all the aspects relevant to the section.  Evaluation Metrics Table: This would be a table consisting of the following columns: Sr. No Topic Name: This refers to the topic you evaluated in the section Remarks: Your remarks in bullet points for the topic; try to include both positive and negative remarks here (at max 4). Keep this as descriptive as possible but short. You are free to use phrases to mind the word limit.  Resources: A list of websites, books or any helpful resource that can be used by the candidate to improve on his weak aspects and points for the topic evaluated Summary: This section should be a summary of a candidate's performance for the section mentioning the shortcomings, positive aspects, wrong responses and overall justification for the grading. The scope of improvement for the candidate and the other"
    system = [{"role": "system", "content":prompt}]

    feedback = generate_question(system)  
    return feedback

if __name__ == '__main__':
    app.run(debug=True)
