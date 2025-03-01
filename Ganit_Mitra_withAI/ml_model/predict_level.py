import sqlite3
import pandas as pd
import joblib

# Load the trained model
model = joblib.load('ganit_mitra/instances/level_predictor.pkl')

# Connect to cashier.db and get user's past performance
conn = sqlite3.connect('ganit_mitra/instances/cashier.db')
query = "SELECT player_id, AVG(average_speed) AS avg_speed, AVG(accuracy) AS avg_accuracy, SUM(customers_served) AS total_customers FROM players GROUP BY player_id"
df = pd.read_sql_query(query, conn)
conn.close()

# Ensure there is data to predict
if df.empty:
    raise ValueError("No player data found in cashier.db.")

# Predict the level for all users
df['predicted_level'] = model.predict(df[['avg_speed', 'avg_accuracy', 'total_customers']])

# Print predictions
print(df[['player_id', 'predicted_level']])
