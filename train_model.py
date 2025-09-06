import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# Enhanced training data: [Amount, Time, Location, Device, Frequency]
X = np.array([
    [500, 12, 0, 0, 1], [1200, 14, 0, 1, 2], [800, 10, 0, 0, 1],
    [2000, 15, 0, 1, 1], [1500, 16, 0, 0, 3], [900, 11, 0, 1, 2],
    [50000, 2, 1, 1, 1], [40000, 3, 1, 0, 1], [35000, 1, 1, 1, 1],
    [45000, 4, 1, 0, 1], [60000, 23, 1, 1, 1], [30000, 2, 1, 1, 1],
    [700, 9, 0, 0, 2], [1800, 18, 0, 1, 1], [1100, 13, 0, 0, 3],
    [25000, 22, 1, 0, 1], [55000, 1, 1, 1, 1], [600, 8, 0, 1, 4]
])
y = np.array([0,0,0,0,0,0,1,1,1,1,1,1,0,0,0,1,1,0])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Train optimized model
clf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
clf.fit(X_train_scaled, y_train)

# Evaluate model
y_pred = clf.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Model Accuracy: {accuracy:.2%}")

# Save both model and scaler
pickle.dump({'model': clf, 'scaler': scaler}, open("model.pkl", "wb"))
print("Optimized model & scaler saved as model.pkl")
