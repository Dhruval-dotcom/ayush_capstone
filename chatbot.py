import requests
import json
import markdown
from IPython.display import Markdown

def get_retention_advice(customer_dict):
    # Generate dynamic prompt from dictionary
    gender = "he" if customer_dict["Gender"].lower() == "male" else "she"
    pronoun = "his" if customer_dict["Gender"].lower() == "male" else "her"
    
    prompt = (
        f"Here is the data of a customer in the bank:\n"
        f"- Credit score: {customer_dict['CreditScore']}\n"
        f"- Gender: {customer_dict['Gender']}\n"
        f"- Age: {customer_dict['Age']}\n"
        f"- Tenure: {customer_dict['Tenure']}\n"
        f"- Balance: {customer_dict['Balance']}\n"
        f"- Number of products: {customer_dict['NumOfProducts']}\n"
        f"- Active Member: {'Yes' if customer_dict['IsActiveMember'] else 'No'}\n"
        f"- Has Credit Card: {'Yes' if customer_dict['HasCrCard'] else 'No'}\n"
        f"- Estimated Salary: {customer_dict['EstimatedSalary']}\n\n"
        f"I have built a machine learning model that predicts {gender} is likely to churn or not.\n"
        f"What advice would you give to retain this customer?\n"
        f"Suggest brief, specific points based on the above features.\n"
        f"Start with mentioning {pronoun} factors and then say 'Here is advice to retain:'"
    )

    url = "https://dhruval-ai.vercel.app/chatbot/stream"
    payload = json.dumps({"prompt": prompt})
    headers = {'Content-Type': 'application/json'}
    
    try:
        response = requests.post(url, headers=headers, data=payload)
        response.raise_for_status()
        advice = response.json().get("response", "No response from model.")
        return markdown.markdown(advice.replace('\n', '<br />'))
    except Exception as e:
        return f"Error: {e}"
