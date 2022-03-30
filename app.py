from flask import Flask, request, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap
from Health import assessment

import json
import re
import pickle
import warnings

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "theservantking_Kofo90love"
# Getting rid of the unpickle warnings
warnings.filterwarnings("ignore", category=UserWarning);
pickle_in = open("HeartDiseaseClassifier.pkl", "rb")
classifier = pickle.load(pickle_in)

@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # Checking to see if there is a prediction result
    has_prediction = False

    # Checking to see if the route is getting called as a GET
    # I don't want this, so we just redirect back to home
    if request.method == 'GET':
        return redirect(url_for("index"))

    # If the route is called as a POST, then we continue
    if request.method == 'POST':
        age = int(request.form['age'])

        # Checking to see if the sex is a string or a number
        sex = request.form['sex']
        if type(sex) is str:
            if sex.lower() == "female":
                sex = 0
            elif sex.lower() == "male":
                sex = 1
            else:
                sex = {"Error": "Gender"}

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
        response = assessment(age, chest_pain_type, model_prediction)
        return redirect(url_for("result", param_pred=response))
    except:
        # If the prediction variable is empty, then we return teh error page
        # This is basically a double check to make sure the route gets called correctly
        flash("Something went wrong, please try again.")
        return render_template("error.html")


@app.route('/prediction')
@app.route('/prediction/<param_pred>')
def result(param_pred=None):
    if param_pred is not None:
        p = re.compile('(?<!\\\\)\'')
        param_pred = p.sub('\"', param_pred)

    return render_template('prediction.html', prediction=json.loads(param_pred))


if __name__ == "__main__":
    app.run()
