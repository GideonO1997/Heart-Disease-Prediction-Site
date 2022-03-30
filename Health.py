import math

# AGE
__max_age_data = 54
__max_age_online = 65
__max_bps_online = 120

# CHEST PAIN
__has_one_cp = 38
__has_two_cp = 14
__has_three_cp = 32
__has_four_cp = 77


def assessment(age, ch_tp, prediction):
    # Calculating the Percentages
    age_percentage_data = round((age / __max_age_data) * 100)

    if ch_tp == 1:
        ch_tp_percentage = __has_one_cp
    elif ch_tp == 2:
        ch_tp_percentage = __has_two_cp
    elif ch_tp == 3:
        ch_tp_percentage = __has_three_cp
    else:
        ch_tp_percentage = __has_four_cp

    total_risk = round(( (age_percentage_data + ch_tp_percentage) / 2 ))
    # Setting the Result Variable
    if prediction == 0:
        result = {
            "Result": 0,
            "Age": age_percentage_data,
            "Chest": ch_tp_percentage,
            "Total": total_risk
        }
    else:
        result = {
            "Result": 1,
            "Age": age_percentage_data,
            "Chest": ch_tp_percentage,
            "Total": total_risk
        }

    return result
