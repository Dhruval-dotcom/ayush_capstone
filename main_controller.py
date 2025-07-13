# loading necessary libraries
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# to display all columns and rows:
pd.set_option('display.max_columns', None); pd.set_option('display.max_rows', None);

df = pd.read_csv('data/churn.csv', index_col = 0)

categorical_variables = [col for col in df.columns if col in "O"
                        or df[col].nunique() <=11
                        and col not in "Exited"]

numeric_variables = [col for col in df.columns if df[col].dtype != "object"
                        and df[col].nunique() >11
                        and col not in "CustomerId"]

# Variables to apply one hot encoding
list = ["Gender", "Geography"]
df = pd.get_dummies(df, columns =list, drop_first = True)

# Removing variables that will not affect the dependent variable
df = df.drop(["CustomerId","Surname"], axis = 1)

scaler = StandardScaler()
df[numeric_variables] = scaler.fit_transform(df[numeric_variables])

X = df.drop("Exited",axis=1)
y = df["Exited"]
# Train-Test Separation
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=12345)

# 2. Create and train the Gradient Boosting model
gb_model = GradientBoostingClassifier(random_state=12345)
gb_model.fit(X_train, y_train)  # Train the model

test_predictions = gb_model.predict(X_test)

# 4. Calculate accuracies
test_accuracy = accuracy_score(y_test, test_predictions)

print(f"Test Accuracy: {test_accuracy:.2%}")


def predict_churn(input_data, model = gb_model):
    """
    Predict customer churn given raw customer input data.

    Parameters:
    - input_data: dict with keys as column names (CustomerId, Surname, CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary)
    - model: trained sklearn model (e.g., GradientBoostingClassifier)
    - scaler: fitted StandardScaler used during training

    Returns:
    - prediction: 0 or 1 (no churn or churn)
    - probability: churn probability
    """
    # Create DataFrame from input
    input_df = pd.DataFrame([input_data])
    
    # One-hot encoding (same as training)
    input_df = pd.get_dummies(input_df, columns=["Gender", "Geography"], drop_first=True)
    
    # # Ensure all required dummy columns exist (add missing with 0)
    for col in ['Geography_Germany', 'Geography_Spain', 'Gender_Male']:
        if col not in input_df.columns:
            input_df[col] = 0

    # Drop unnecessary columns
    input_df = input_df.drop(['CustomerId', 'Surname'], axis=1)
    
    # Reorder columns to match training data
    input_df = input_df[X.columns]
    
    # Scale numeric variables
    input_df[numeric_variables] = scaler.transform(input_df[numeric_variables])
    
    # Predict
    pred = model.predict(input_df)[0]
    pred_prob = model.predict_proba(input_df)[0][1]
    
    return pred, pred_prob