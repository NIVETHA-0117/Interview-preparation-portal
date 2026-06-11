from flask import Flask, render_template, request, session
import sqlite3
import random
import re

app = Flask(**name**)
app.secret_key = "interview_portal_secret"

# ---------------- HOME ----------------

@app.route('/')
def home():
return render_template('index.html')

# ---------------- LOGIN ----------------

@app.route('/login', methods=['GET','POST'])
def login():

```
if request.method == "POST":

    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email=? AND password=?",
        (email,password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        session['email'] = email
        return render_template('dashboard.html')
    else:
        return "Invalid Email or Password"

return render_template('login.html')
```

# ---------------- REGISTER ----------------

@app.route('/register', methods=['GET','POST'])
def register():

```
if request.method == "POST":

    fullname = request.form['fullname']
    email = request.form['email']
    password = request.form['password']

    conn = sqlite3.connect('database/users.db')
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users(fullname,email,password) VALUES(?,?,?)",
        (fullname,email,password)
    )

    conn.commit()
    conn.close()

    return "Registration Successful"

return render_template('register.html')
```

# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():
return render_template('dashboard.html')

# ---------------- CATEGORY ----------------

@app.route('/category')
def category():
return render_template('interview_category.html')

# ---------------- QUESTIONS ----------------

@app.route('/question/<category>')
def question(category):

```
questions = {

    "python":[
        "What is Python?",
        "What is a List in Python?",
        "What is a Dictionary?",
        "What is a Function?",
        "What are Modules?"
    ],

    "java":[
        "What is Java?",
        "What is JVM?",
        "What is OOP?",
        "What is Inheritance?",
        "What is Polymorphism?"
    ],

    "c":[
        "What is C Programming?",
        "What is a Function in C?",
        "What is a Pointer?",
        "What is an Array?",
        "What is a Structure?"
    ],

    "ds":[
        "What is a Stack?",
        "What is a Queue?",
        "What is a Linked List?",
        "What is a Tree?",
        "What is a Graph?"
    ],

    "hr":[
        "Tell me about yourself.",
        "Why should we hire you?",
        "What are your strengths?",
        "What are your weaknesses?",
        "Where do you see yourself in 5 years?"
    ],

    "aptitude":[
        "What is 10 + 20?",
        "What is 15 + 5?",
        "What is 100 / 4?",
        "What is 12 * 2?",
        "What is 50 - 20?"
    ]
}

if category not in questions:
    return "Invalid category"

q = random.choice(questions[category])
session['question'] = q

return render_template(
    'question.html',
    question=q,
    category=category
)
```

# ---------------- FEEDBACK ----------------

@app.route('/feedback', methods=['POST'])
def feedback():

```
answer = request.form['answer'].lower().strip()

# remove punctuation
answer = re.sub(r'[^\w\s]', '', answer)

category = request.form['category']
question = session.get('question')


# ---------------- ANSWERS DATABASE ----------------
answers = {

    # PYTHON
    "What is Python?": {
        "keywords": ["programming", "language"],
        "feedback": "Mention definition, features and uses."
    },

    "What is a Dictionary?": {
        "keywords": ["key", "value"],
        "feedback": "Explain key-value pairs with example."
    },

    # JAVA
    "What is Java?": {
        "keywords": ["programming", "language"],
        "feedback": "Mention JVM and OOP."
    },

    # C
    "What is a Pointer?": {
        "keywords": ["memory", "address"],
        "feedback": "Explain memory address concept."
    },

    # APTITUDE
    "What is 10 + 20?": {
        "keywords": ["30"],
        "feedback": "Correct answer."
    },

    "What is 15 + 5?": {
        "keywords": ["20"],
        "feedback": "Correct answer."
    },

    "What is 100 / 4?": {
        "keywords": ["25"],
        "feedback": "Correct answer."
    },

    "What is 12 * 2?": {
        "keywords": ["24"],
        "feedback": "Correct answer."
    },

    "What is 50 - 20?": {
        "keywords": ["30"],
        "feedback": "Correct answer."
    }
}


# ---------------- SAFE MATCHING ----------------
question_data = None

for q in answers:
    if q.lower().strip() == question.lower().strip():
        question_data = answers[q]
        break


if not question_data:
    return "Error: Question not found in answer database"


keywords = question_data["keywords"]
custom_feedback = question_data["feedback"]


# ---------------- SCORING ----------------
score = 0

for word in keywords:
    if word in answer:
        score += 1


if score >= 1:
    marks = 10
    feedback_msg = "Excellent answer. " + custom_feedback
else:
    marks = 0
    feedback_msg = "Answer needs improvement. " + custom_feedback


# ---------------- SAVE RESULT ----------------
conn = sqlite3.connect('database/users.db')
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO interview_results(email,interview_type,score) VALUES(?,?,?)",
    (
        session.get('email'),
        category.title() + " Interview",
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
```

# ---------------- PERFORMANCE ----------------

@app.route('/performance')
def performance():

```
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
    avg=round(avg,2),
    level=level
)
```

# ---------------- HISTORY ----------------

@app.route('/history')
def history():

```
conn = sqlite3.connect('database/users.db')
cursor = conn.cursor()

cursor.execute("SELECT interview_type,score FROM interview_results")
data = cursor.fetchall()

conn.close()

return render_template(
    'history.html',
    records=data
)
```

# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():
session.clear()
return render_template('index.html')

# ---------------- CHECK ----------------

@app.route('/check')
def check():
return "Flask is working"

if **name** == "**main**":
app.run(host="0.0.0.0", port=10000)
