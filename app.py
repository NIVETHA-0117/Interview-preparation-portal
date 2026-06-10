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

    answer = request.form['answer']
    category = request.form['category']
    question = session.get('question')

    score = 2  
    answer = answer.lower().strip()
    answer = re.sub(r'[^\w\s]', '', answer)

    if category == "aptitude":
        correct_values = {
            "What is 10 + 20?": "30",
            "What is 15 + 5?": "20",
            "What is 100 / 4?": "25",
            "What is 12 * 2?": "24",
            "What is 50 - 20?": "30"
        }

        correct_answer = correct_values.get(question, "")

        try:
            if float(answer) == float(correct_answer):
                score = 10
                feedback_msg = "Correct answer."
            else:
                score = 2
                feedback_msg = "Wrong answer."
        except:
            score = 2
            feedback_msg = "Enter a valid number."

    else:
        correct_answers = {
            "What is Python?": ["programming", "language"],
            "What is a List in Python?": ["ordered", "mutable"],
            "What is a Dictionary?": ["key", "value"],
            "What is a Function?": ["reusable", "code"],
            "What are Modules?": ["file", "import"],
            "What is Java?": ["programming", "language"],
            "What is JVM?": ["java", "virtual", "machine"],
            "What is OOP?": ["object", "class"],
            "What is Inheritance?": ["parent", "child"],
            "What is Polymorphism?": ["many", "forms"],
            "What is C Programming?": ["programming", "language"],
            "What is a Function in C?": ["reusable", "code"],
            "What is a Pointer?": ["memory", "address"],
            "What is an Array?": ["collection"],
            "What is a Structure?": ["user", "defined"],
            "What is a Stack?": ["lifo"],
            "What is a Queue?": ["fifo"],
            "What is a Linked List?": ["node"],
            "What is a Tree?": ["root"],
            "What is a Graph?": ["vertex"]
        }

        keywords = correct_answers.get(question, [])

        match_count = 0
        for keyword in keywords:
            if keyword in answer:
                match_count += 1

        
        if match_count == len(keywords) and len(keywords) > 0:
            score = 10
        elif match_count > 0:
            score = 6   
        else:
            score = 2

        
        if score == 10:
            feedback_msg = "Excellent answer."
        elif score >= 5:
            feedback_msg = "Good answer."
        else:
            feedback_msg = "Try to explain more clearly."

    
    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()

    cursor.execute(
     "INSERT INTO interview_results(email, interview_type, score) VALUES (?, ?, ?)",
     (session['email'], category.title() + " Interview", score)
    )

    conn.commit()
    conn.close()

    return render_template(
        'feedback.html',
        score=score,
        feedback_msg=feedback_msg
    )


@app.route('/performance')
def performance():

    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM interview_results")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(score) FROM interview_results")
    avg = cursor.fetchone()[0]

    conn.close()

    if avg is None:
        avg = 0

    if avg >= 8:
        level = "Excellent"
    elif avg >= 5:
        level = "Good"
    else:
        level = "Needs Improvement"

    return render_template(
        'performance.html',
        total=total,
        avg=round(avg, 2),
        level=level
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