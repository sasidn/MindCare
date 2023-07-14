import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Load the dataset
dataset = pd.read_csv('mental_data99.csv')

# Perform necessary operations to generate the 'result' variable
X = dataset.iloc[:, 0:21].values
y = dataset.iloc[:, 22].values

bridge_df = pd.DataFrame(y, columns=['Bridge_Types'])
dum_df = pd.get_dummies(bridge_df, columns=["Bridge_Types"], prefix=["Type_is"])

result = pd.concat([dataset, dum_df], axis=1, sort=False)

X = result.iloc[:, 0:21].values
y = result.iloc[:, 23:29].values

# Split the dataset into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Scale the features using StandardScaler
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Build the model
classifier = Sequential()
classifier.add(Dense(units=10, kernel_initializer='uniform', activation='relu', input_dim=21))
classifier.add(Dense(units=6, kernel_initializer='uniform', activation='relu'))
classifier.add(Dense(units=6, kernel_initializer='uniform', activation='sigmoid'))

# Compile the model
classifier.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
classifier.fit(X_train, y_train, batch_size=10, epochs=500)

# Make predictions on the test set
y_pred = classifier.predict(X_test)
