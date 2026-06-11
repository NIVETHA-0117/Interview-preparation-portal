from flask import Flask, render_template, request, session
import sqlite3
import random
import re

app = Flask(__name__)
app.secret_key = "interview_portal_secret"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            session['email'] = email
            return render_template('dashboard.html')
        else:
            return "Invalid Email or Password"

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        fullname = request.form['fullname']
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect('database/users.db')
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users(fullname,email,password) VALUES(?,?,?)",
            (fullname, email, password)
        )

        conn.commit()
        conn.close()

        return "Registration Successful!"

    return render_template('register.html')


@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')


@app.route('/category')
def category():
    return render_template('interview_category.html')


@app.route('/question/<category>')
def question(category):

    questions = {
        "python": [
            "What is Python?",
            "What is a List in Python?",
            "What is a Dictionary?",
            "What is a Function?",
            "What are Modules?"
        ],
        "java": [
            "What is Java?",
            "What is JVM?",
            "What is OOP?",
            "What is Inheritance?",
            "What is Polymorphism?"
        ],
        "c": [
            "What is C Programming?",
            "What is a Function in C?",
            "What is a Pointer?",
            "What is an Array?",
            "What is a Structure?"
        ],
        "ds": [
            "What is a Stack?",
            "What is a Queue?",
            "What is a Linked List?",
            "What is a Tree?",
            "What is a Graph?"
        ],
        "hr": [
            "Tell me about yourself.",
            "Why should we hire you?",
            "What are your strengths?",
            "What are your weaknesses?",
            "Where do you see yourself in 5 years?"
        ],
        "aptitude": [
            "What is 10 + 20?",
            "What is 15 + 5?",
            "What is 100 / 4?",
            "What is 12 * 2?",
            "What is 50 - 20?"
        ]
    }

    question_text = random.choice(
        questions.get(category, ["Tell me about yourself."])
    )

    session['question'] = question_text

    return render_template(
        'question.html',
        question=question_text,
        category=category
    )


@app.route('/feedback', methods=['POST'])
def feedback():

    answer = request.form['answer'].lower()
    category = request.form['category']
    question = session.get('question')

    score = 0

    correct_answers = {

        "What is Python?": [
            "programming language",
            "high level",
            "interpreted"
        ],

        "What is a List in Python?": [
            "ordered",
            "mutable",
            "collection"
        ],

        "What is a Dictionary?": [
            "key",
            "value",
            "key-value"
        ],

        "What is a Function?": [
            "reusable",
            "code",
            "block"
        ],

        "What are Modules?": [
            "python file",
            "import",
            "code"
        ],

        "What is Java?": [
            "programming language",
            "object oriented",
            "jvm"
        ],

        "What is JVM?": [
            "java virtual machine",
            "bytecode"
        ],

        "What is a Pointer?": [
            "memory",
            "address"
        ],

        "What is a Stack?": [
            "lifo",
            "push",
            "pop"
        ],

        "What is a Queue?": [
            "fifo",
            "enqueue",
            "dequeue"
        ]

    }


    keywords = correct_answers.get(question, [])


    for word in keywords:
        if word in answer:
            score += 1


    if score >= 1:
        marks = 10
        feedback_msg = "Good answer. Your concept is correct. Try adding more explanation."
    else:
        marks = 0
        feedback_msg = "Answer needs improvement. Focus on the main concept and important points."


    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()


    cursor.execute(
        "INSERT INTO interview_results(email, interview_type, score) VALUES (?, ?, ?)",
        (
            session.get('email'),
            category.title()+" Interview",
            marks
        )
    )


    conn.commit()
    conn.close()


    return render_template(
        'feedback.html',
        score=marks,
        feedback_msg=feedback_msg
    )


@app.route('/history')
def history():

    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT interview_type, score FROM interview_results"
    )

    records = cursor.fetchall()
    conn.close()

    return render_template(
        'history.html',
        records=records
    )


@app.route('/logout')
def logout():
    session.clear()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)