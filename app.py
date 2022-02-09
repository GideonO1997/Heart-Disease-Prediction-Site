from flask import Flask, request, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap

import pickle

app = Flask(__name__)
Bootstrap(app)
app.secret_key = "theservantking_Kofo90love"
pickle_in = open("HeartDiseaseClassifier.pkl", "rb")
classifier = pickle.load(pickle_in)


@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    # Checking to see if there is a prediction result
    has_prediction = False

    # Checking to see if the route is getting called as a GET
    # I don't want this, so we return an error page with a redirect link
    if request.method == 'GET':
        return render_template("error.html")

    # If the route is called as a POST, then we continue
    if request.method == 'POST':
        age = request.form['age']

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

        # Resting blood pressure comes in the way we expect it to
        resting_bp_s = request.form['resting_bp_s']

        # Setting the fasting blood sugar level as a binary
        fasting_blood_sugar = request.form['fasting_blood_sugar']
        if int(fasting_blood_sugar) > 120:
            resting_bp_s = 1
        else:
            fasting_blood_sugar = 0

        # Resting ECG comes in as a str so, we cast to an int
        resting_ecg = int(request.form['resting_ecg'])

        # Exercise Induced Angina comes in as a str so, we cast to an int
        exercise_angina = int(request.form['exercise_angina'])

        oldpeak = request.form['oldpeak']

        # ST SLope comes in as a str so, we cast to an int
        ST_slope = int(request.form['ST_slope'])

        prediction = classifier.predict([[age, sex, chest_pain_type, resting_bp_s, fasting_blood_sugar, resting_ecg,
                                          exercise_angina, oldpeak, ST_slope]])

        # Now we check the prediction variable to accurately classify things
        if prediction[0] == 0:
            has_prediction = True
            prediction = "No Heart Disease Present"
        else:
            has_prediction = True
            prediction = "Presence of Heart Disease Detected"

    # If the prediction variable is empty, then we return teh error page
    # This is basically a double check to make sure the route gets called correctly
    if not has_prediction:
        return render_template("error.html")
    else:
        flash(prediction)
        return redirect(url_for('index'))


if __name__ == "__main__":
    app.run()
