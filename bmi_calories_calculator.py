# import packages
import requests
from tkinter import *
import tkinter as tk
from tkinter import ttk


# define all functions

def bmi_calories(age, gender, height, height_units, weight, weight_units, activity):
    # this function returns the bmi and recommended calorie intake per day in a tuple (bmi, calories)
    
    if height_units == 'cm': #this is to convert the height to 'm' if entered in 'cm'
        height = float(height)/100
    if weight_units == 'g':  #this is to convert the weight to 'kg' if entered in 'g'
        weight = float(weight)/1000
        
    bmi = round(float(weight) / float(height) ** 2, 2)

    activity_factor = activity_options[activity]
    BMR = (10 * float(weight)) + (6.25 * float(height) * 100) - (5 * age) + (5 if gender == 'male' else -161)
    correction_factor = 1 if 18.5 <= bmi < 25 else 0.9 if bmi > 25 else 1.1

    calories = int((BMR * activity_factor) * correction_factor)

    return (bmi, calories)


def meal_plan(calories):
    # this function returns a recommended meal plan based on recommended calorie intake per day
    # current assumption: meal plan is for breakfast/lunch/dinner for a day in a dictionary format

    meal = {'breakfast': [('bread', 500), ('banana', 200)], 'lunch': [('baked salmon', 1200)],
            'dinner': [('tuna sandwich', 1000)]}
    # meal = {'breakfast': [], 'lunch': [], 'dinner':[]}

    return meal


def meal_plan_result(plan):
    # this function returns string of meal plan result in a nice format

    if any(plan.values()):
        meal_plan = 'Meal Recommendation:\n'
        total_cal = 0
        for i, j in plan.items():
            if j:
                meal_plan = meal_plan + '\n' + i
                for k in j:
                    meal_plan = meal_plan + '\n' + format(k[1], ',d') + ' calories - ' + k[0]
                    total_cal += k[1]
                meal_plan = meal_plan + '\n'
        meal_plan = meal_plan + '\ntotal\n' + format(total_cal, ',d') + ' calories - per day'
    else:
        meal_plan = 'no recommended meal plan'

    return meal_plan


def result_message():
    # this function returns string of final message to user about bmi and meal plan

    age = age_entry.get()
    gender = gender_entry.get()
    height = height_entry.get()
    units_height = height_units.get()
    weight = weight_entry.get()
    units_weight = weight_units.get()
    activity = activity_entry.get()
    # print(age, gender, height, units_height, weight, units_weight, activity)
    try:

        bmi = bmi_calories(age, gender, height, units_height, weight, units_weight, activity)[0]
        comment = '(underweight)' if bmi < 18.5 else '(normal)' if bmi < 25 else '(overweight)' if bmi < 30 else '(obese)'
        calories = bmi_calories(age, gender, height, units_height, weight, units_weight, activity)[1]
        plan = meal_plan(calories)

        text = 'Your BMI is {} {}.\nYou should consume {} calories per day.\n\n{}'.format(bmi, comment, format(calories, ',d'),
                                                                                       meal_plan_result(plan))


    except ZeroDivisionError:

        text = 'Height and weight must not be 0'

    except:

        text = 'Ensure all fields are input correctly'

    finally:

        result.set(text)


def reset():
    # this function clears/return current input to default values

    age_entry.set(20)
    gender_entry.set("male")
    activity_entry.set("Moderate")
    height_entry.delete(0, END)
    height_units.set('m')
    weight_entry.delete(0, END)
    weight_units.set('kg')
    result.set("")


def close_program():
    # this function closes application

    window.destroy()
    exit()


# main app structure

window = Tk()
window.title('Food and Health Calculator')
window.geometry("400x600")

# age
age_entry = tk.IntVar()
age_entry.set(20)
age_options = [i for i in range(15, 81)]
age_dropdown = ttk.Combobox(window, textvariable=age_entry, values=age_options, state='readonly', justify=tk.CENTER,
                            width=30)
age_dropdown.grid(row=3, column=1, columnspan=2, sticky=W)

# gender
gender_entry = tk.StringVar()
gender_entry.set("male")
male = ttk.Radiobutton(window, text='Male', value='male', variable=gender_entry)
female = ttk.Radiobutton(window, text='Female', value='female', variable=gender_entry)
male.grid(row=4, column=1, sticky=W)
female.grid(row=4, column=2, sticky=W)

# height
height_entry = Entry(window, bg="white", width=16, justify=tk.CENTER)
height_entry.grid(row=5, column=1, columnspan=2, sticky=W)
height_units = tk.StringVar()
height_units.set('m')
height_units_options = ttk.Combobox(window, textvariable=height_units, values=['cm', 'm'], state='readonly',
                                    justify=tk.CENTER, width=13)
height_units_options.grid(row=5, column=2, sticky=W)

# weight
weight_entry = Entry(window, bg="white", width=16, justify=tk.CENTER)
weight_entry.grid(row=6, column=1, columnspan=2, sticky=W)
weight_units = tk.StringVar()
weight_units.set('kg')
weight_units_options = ttk.Combobox(window, textvariable=weight_units, values=['g', 'kg'], state='readonly',
                                    justify=tk.CENTER, width=13)
weight_units_options.grid(row=6, column=2, sticky=W)

# activity
activity_entry = tk.StringVar()
activity_entry.set("Light (exercise 1-3 times/week)")
activity_options = {'Sedentary (little or no exercise)': 1.2, 'Light (exercise 1-3 times/week)': 1.35, \
                    'Moderate (exercise 4-5 times/week)': 1.5, 'Active (daily exercise)': 1.65, \
                    'Very Active (intense daily exercise)': 1.8, 'Extra Active (very intense daily exercise)':1.95}
activity_dropdown = ttk.Combobox(window, textvariable=activity_entry, values=[i for i in activity_options.keys()], state='readonly',
                                 justify=tk.CENTER, width=30)
activity_dropdown.grid(row=7, column=1, columnspan=2, sticky=W)

# initialise final result
result = tk.StringVar()

# field labels
Label(window, text="Enter the following fields:").grid(row=1, columnspan=2, sticky=W)
Label(window).grid(row=2, sticky=W)
Label(window, text="Age:").grid(row=3, column=0, sticky=W)
Label(window, text="Gender:").grid(row=4, column=0, sticky=W)
Label(window, text="Height:").grid(row=5, column=0, sticky=W)
Label(window, text="Weight:").grid(row=6, column=0, sticky=W)
Label(window, text="Activity:").grid(row=7, column=0, sticky=W)
Label(window).grid(row=8, sticky=W)
Label(window).grid(row=10, sticky=W)
Label(window, textvariable=result, justify="left", fg='blue').grid(row=11, column=0, columnspan=4, sticky=W)

# buttons
Button(window, text="reset", width=13, command=reset).grid(row=9, column=1, sticky=W)
Button(window, text="calculate", width=13, command=result_message).grid(row=9, column=2, sticky=W)
Button(window, text="close", width=13, command=close_program).grid(row=9, column=0, sticky=W)

window.mainloop()

