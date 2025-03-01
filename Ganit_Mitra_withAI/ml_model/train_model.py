import sqlite3
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import joblib

# Connect to train.db
conn = sqlite3.connect('instances/cashier.db')
cursor = conn.cursor()

# Load data from the database
query = "SELECT avg_speed, accuracy, customers, usr_level FROM cashier_results"
df = pd.read_sql_query(query, conn)

# Close the connection
conn.close()

# Check if data is loaded
print(df.head())

# Prepare features (X) and target (y)
X = df[['avg_speed', 'accuracy', 'customers']].values
y = df['usr_level'].values

# Split the data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the linear regression model
model = LinearRegression()
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: {mae}")
print(f"R² Score: {r2}")

# Save the trained model
joblib.dump(model, "instances/level_predictor.pkl")

print("Model saved as level_predictor.pkl")
