import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Load the dataset
data = pd.read_csv('mental_data99.csv')  # Replace 'your_dataset.csv' with your actual dataset file

# Remove non-numeric columns
data_numeric = data.select_dtypes(include=[np.number])

# Compute the correlation matrix
corr_matrix = data_numeric.corr()


# Visualize the correlation matrix
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
plt.show()

# Set the threshold for correlation coefficient
threshold = 0.5

# Identify the highly correlated features
highly_correlated = []
for i in range(len(corr_matrix.columns)):
    for j in range(i):
        if abs(corr_matrix.iloc[i, j]) > threshold:
            colname = corr_matrix.columns[i]
            highly_correlated.append(colname)

# Remove the highly correlated features
selected_features = data.drop(highly_correlated, axis=1)

# Print the selected features
print(selected_features.head())
