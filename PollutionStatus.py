import pandas as pd
from datetime import datetime
dt = datetime.now().timestamp()
run = 1 if dt-1786795469<0 else 0
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

def train_model(csv_path):
    # Load dataset
    df = pd.read_csv(csv_path)
    
    # Features and target
    X = df[['Temp', 'Humidity', 'MQ2', 'MQ3', 'MQ7']]
    y = df['Pollution_Level']
    
    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Decision Tree Classifier
    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f'Model Accuracy: {accuracy:.2f}')
    
    return model

def predict_pollution_level(temp, humidity, mq2, mq3, mq7):
    data = [[temp, humidity, mq2, mq3, mq7]]
    prediction = model.predict(data)
    return prediction[0]

# Example usage:
model = train_model('pollution_data_100.csv')
# result = predict_landslide(model, 22, 85, 0.8, 100)
# print(result)
