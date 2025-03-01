import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib

# Connect to train.db and fetch past user data
conn = sqlite3.connect('../instance/cashier_results.db')
query = "SELECT average_speed, accuracy, customers_served, level FROM players"  # Adjust table name if needed
df = pd.read_sql_query(query, conn)
conn.close()

# Ensure there is data to train
if df.empty:
    raise ValueError("No data found in train.db to train the model.")

# Define features and target
X = df[['average_speed', 'accuracy', 'customers_served']]
y = df['level']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"Mean Squared Error: {mse}")

# Save the trained model
joblib.dump(model, 'ganit_mitra/instances/level_predictor.pkl')
print("Model saved as level_predictor.pkl")
