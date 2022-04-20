# Flask related imports
from flask import Flask, request, render_template, flash, redirect, url_for, session
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect

# Internal function created
from Health import assessment

# Model prediction related imports
import pickle
import warnings

app = Flask(__name__)

# Adding Bootstrap to the Flask APP
Bootstrap(app)

# Adding Secret Key to Flask APP
app.secret_key = "theservantking_Kofo90love"

# Adding Security for CSRF protection
# csrf = CSRFProtect(app)

# Removing the unpickle user warnings
warnings.filterwarnings("ignore", category=UserWarning)

# Opening and storing the pickle file as a variable
pickle_in = open("HeartDiseaseClassifier.pkl", "rb")
classifier = pickle.load(pickle_in)

# Cookie Handling
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/home')
def home():
    session.clear()
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    session.clear()
    # Checking to see if the route is getting called as a GET
    # I don't want this, so we just redirect back to home
    if request.method == 'GET':
        return redirect(url_for("index"))

    # If the route is called as a POST, then we continue
    if request.method == 'POST':
        age = int(request.form['age'])

        # Sex comes in as a str so, we cast to an int
        sex = int(request.form['sex'])

        # Chest pain comes in as a str so, we cast to an int
        chest_pain_type = int(request.form['chest_pain_type'])

        # Exercise Induced Angina comes in as a str so, we cast to an int
        exercise_angina = int(request.form['exercise_angina'])

        oldpeak = int(request.form['oldpeak'])

        # ST SLope comes in as a str so, we cast to an int
        ST_slope = int(request.form['ST_slope'])

        # Adding a try except to catch any and all problems before returning
        try:
            model_prediction = classifier.predict([[age, sex, chest_pain_type, exercise_angina, oldpeak, ST_slope]])
            # Calculating How far each controllable variable is from getting Heart Disease
            # And getting the assessment
            finalResult = assessment(age, chest_pain_type, model_prediction)
            session['result'] = finalResult
            return redirect(url_for("result"))
        except Exception as case:
            # If the prediction variable is empty, then we return teh error page
            # This is basically a double check to make sure the route gets called correctly
            flash(str(case.args))
            return render_template("error.html")


@app.route('/prediction/')
def result():
    try:
        paramPred = session['result']
        session.clear()
        return render_template('prediction.html', prediction=paramPred)
    except KeyError:
        return redirect(url_for("home"))
    # # Adding Content Security Policy (CSP) to protect from XSS and Clickjacking
    # response = make_response(render_template('prediction.html', prediction=json.loads(param_pred)))
    # response.headers['Content-Security-Policy'] = "default-src 'self'"
    # return response


if __name__ == "__main__":
    app.run()
