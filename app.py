from flask import Flask, request, jsonify
from flask import render_template
import openai
import os
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key='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')

# Candidate and Job Description Information
candidate_info = "name - Abhay Gotmare, education - BTech Computer Science, ..."
job_description = "Machine Learning Engineer responsibilities ..."

# Initial System Prompt
system_prompt = [{"role": "system", "content": f"You are interviewer, conducting an interview of a candidate with information: {candidate_info}, and the job description: {job_description}"}]

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
          max_tokens=300,
          top_p=0.9,)
    question = chat_completion.choices[0].message.content
    return question

def generate_feedback(conversation):
    prompt = f"Given the following interview conversation, evaluate the candidate's responses at two parameters  technical knowlwdge and Behaviour also along with feedback rate both out of 100 : {conversation}"

    system = [{"role": "system", "content":prompt}]

    feedback = generate_question(system)  
    return feedback

if __name__ == '__main__':
    app.run(debug=True)
