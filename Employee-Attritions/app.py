# importing required libraries

from flask import Flask, request, render_template
import numpy as np
import pickle


app = Flask(__name__)
# load the model
model = pickle.load(open('model1.pkl','rb'))

# for taking the input from the user
@app.route('/', methods = ['GET'])
def home():
    return render_template('index.html')

# for processing the user input and predict the result
@app.route("/predict", methods = ['POST'])
def predict():
    if request.method == 'POST':
        satisfaction = float(float(request.form['satisfaction_level'])/5)
        last_evaluation = float(float(request.form['last_evaluation'])/5)
        no_project = int(request.form['number_project'])
        monthly_hrs = float(request.form['average_montly_hours'])
        years = float(request.form['time_spend_company'])
        accident = int(request.form['Work_accident'])
        promotion = int(request.form.get('promotion', False))
        salary = request.form['salary']
        if salary == 'low':
            low = 1
            medium = 0
        elif salary == 'medium':
            low =0
            medium = 1
        else:
            low = 0
            medium = 0
        prediction = model.predict(np.array([[satisfaction,last_evaluation,no_project,monthly_hrs,years,accident,promotion]]))
        
        if prediction == 1:
            output = 'LEAVE'
        elif prediction == 0:
            output = 'NOT LEAVE'

        return render_template('result.html',prediction_text="EMPLOYEE WILL {}".format(output))

    else:
        return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)
