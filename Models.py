from pydantic import BaseModel


# 2. Class which describes Patient measurements
class Patients(BaseModel):
    age: int
    sex: int
    chest_pain_type: int
    resting_bp_s: int
    fasting_blood_sugar: int
    resting_ecg: int
    exercise_angina: int
    oldpeak: float
    ST_slope: int
