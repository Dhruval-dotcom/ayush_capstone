from flask import Flask, render_template, request
from main_controller import predict_churn
from chatbot import get_retention_advice

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        try:
            # Get input values from form
            customer = {
                'CustomerId': 15737452,
                'Surname': 'Romeo',
                'CreditScore': int(request.form['CreditScore']),
                'Geography': request.form['Geography'],
                'Gender': request.form['Gender'],
                'Age': int(request.form['Age']),
                'Tenure': int(request.form['Tenure']),
                'Balance': float(request.form['Balance']),
                'NumOfProducts': int(request.form['NumOfProducts']),
                'HasCrCard': 1 if request.form.get('HasCrCard') else 0,
                'IsActiveMember': 1 if request.form.get('IsActiveMember') else 0,
                'EstimatedSalary': float(request.form['EstimatedSalary'])
            }
            print(customer)
            prediction, probability = predict_churn(customer)
            result = 'The customer is likely to churn' if prediction else 'The customer won\'t churn'

            suggestions = None

            if prediction:
               suggestions = get_retention_advice(customer) 
               print(suggestions, 'suggestions')
            return render_template("index.html", result = result, suggestions = suggestions)
        except ValueError as e:
            print(e)
            result = "Some Error occurred!"
            return render_template("index.html", result = None, suggestions = None)
    
    return render_template("index.html", result = None, suggestions = None)


if __name__ == "__main__":
    app.run(debug=True)