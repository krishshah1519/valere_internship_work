import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix)

df = pd.read_csv("personality_dataset.csv")  
print(df.head())


print(df.info())
print(df.describe())
print(df.isnull().sum())


print(len(df) - df.dropna().shape[0])


df.fillna(method='bfill', inplace=True)
le = LabelEncoder()
df['Stage_fear'] = le.fit_transform(df['Stage_fear'])
df['Drained_after_socializing'] = le.fit_transform(
    df['Drained_after_socializing'])

df['Personality'] = le.fit_transform(df['Personality'])


sns.countplot(data=df, x='Personality')
plt.title("Extrovert VS Introvert Count")
plt.show()

x = df.drop('Personality', axis=1)
y = df['Personality']


scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

print(x_scaled.shape)
print(len(y))

x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2,
                                                    random_state=42)


model = LogisticRegression()
model.fit(x_train, y_train)


y_pred = model.predict(x_test)


print("Accuracy:", accuracy_score(y_test, y_pred))
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
