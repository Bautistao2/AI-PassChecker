import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle
import string

# Function to extract features from passwords
# This function analyzes a given password and extracts specific attributes to represent it as a feature vector.
# These features include:
# - 'length': Total number of characters in the password.
# - 'num_uppercase': Number of uppercase letters in the password, indicating complexity.
# - 'num_lowercase': Number of lowercase letters in the password, ensuring variety.
# - 'num_digits': Number of numeric characters, contributing to strength.
# - 'num_special': Number of special characters (e.g., @, #, $), which enhance security.
# These features are relevant because they are commonly used indicators of password strength.
def extract_features(password):
    return {
        'length': len(password),  # Length of the password
        'num_uppercase': sum(1 for c in password if c.isupper()),  # Count of uppercase letters
        'num_lowercase': sum(1 for c in password if c.islower()),  # Count of lowercase letters
        'num_digits': sum(1 for c in password if c.isdigit()),  # Count of digits
        'num_special': sum(1 for c in password if c in string.punctuation),  # Count of special characters
    }

# Load the dataset
# The CSV file should contain the following columns:
# - 'password': A string representing the password.
# - 'strength': A string label ('weak', 'moderate', 'strong') indicating the strength of the password.
df = pd.read_csv("Data/password_dataset.csv")

# Extract features from each password
df_features = pd.DataFrame([extract_features(pw) for pw in df['password']])

# Add the strength label to the processed dataset
df_features['strength'] = df['strength'].map({'weak': 0, 'moderate': 1, 'strong': 2})

# Separate features and labels
X = df_features.drop(columns=['strength'])
y = df_features['strength']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest model
# Random Forest was chosen for its robustness and ability to handle complex, non-linear relationships in the data.
# It is an ensemble method that reduces overfitting and provides high accuracy by combining multiple decision trees.
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
predictions = model.predict(X_test)
# This classification report provides a detailed analysis of the model's performance.
# It includes metrics such as precision, recall, and F1-score for each class (Weak, Moderate, Strong).
# Users can use these insights to understand how well the model predicts each category and identify potential areas for improvement.
print("Classification Report:")
print(classification_report(y_test, predictions, target_names=['Weak', 'Moderate', 'Strong']))

# Save the trained model to a file
# Saving the model ensures that it can be reused later without the need to retrain it.
# This is particularly useful for deployment, where the model can be loaded and used for real-time predictions.
with open("password_strength_model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

print("Model trained and saved as 'password_strength_model.pkl'")
