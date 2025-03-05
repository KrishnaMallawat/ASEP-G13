import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
import sqlite3

db_path = "users.db"  # Ensure this is the correct path
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in users.db:", tables)

conn.close()


# Step 1: Connect to SQLite Database
db_path = "users.db"  # Adjust path if needed
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Step 2: Load Data from the Table
query = "SELECT avg_speed, accuracy, customers, usr_level FROM cashier_results;"
df = pd.read_sql_query(query, conn)

# Step 3: Preprocess Data
X = df[['avg_speed', 'accuracy', 'customers']]  # Features
y = df['level']  # Target variable

# Handle missing values if needed
df.dropna(inplace=True)

# Step 4: Split Data into Training and Testing Sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train the Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

# Step 6: Make Predictions
y_pred = model.predict(X_test)

# Step 7: Evaluate the Model
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse:.2f}")
print(f"R² Score: {r2:.2f}")

# Step 8: Predict Level for a New Player
new_data = pd.DataFrame({'avg_speed': [50], 'accuracy': [90], 'customers': [30]})
predicted_level = model.predict(new_data)
print(f"Predicted Level: {predicted_level[0]:.2f}")

# Close the database connection
conn.close()
