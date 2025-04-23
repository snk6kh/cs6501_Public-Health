import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import matplotlib.pyplot as plt
import seaborn as sns
from joblib import dump


df = pd.read_csv("Pre-Classifier.csv")
y = df["Social Interaction Level"]

df["Binary_Social_Level"] = y.apply(lambda val: 0 if val < 2 else 1) #changing 0-1 value to 0 and 2-3 value to 1 to make binary
y_binary = df["Binary_Social_Level"]

X = df[["Likes", "Snap_Social_Score"]]
X_train, X_test, y_train, y_test = train_test_split(X, y_binary, test_size=0.2, random_state=55) #55 and 65


clf = RandomForestClassifier(random_state=55)
clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))


cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=["Low", "High"], yticklabels=["Low", "High"])
plt.xlabel("Predicted")
plt.ylabel("True")
plt.title("Confusion Matrix: Binary Social Level Prediction")
plt.show()


importances = clf.feature_importances_
feature_names = X.columns
for name, importance in zip(feature_names, importances):
    print(f"{name}: {importance:.4f}")


filename = 'binary_socialmodel.joblib' #save model for later/prediction use
dump(clf, filename)
print(f"Model saved to {filename}")
