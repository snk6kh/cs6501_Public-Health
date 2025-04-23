import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix


df = pd.read_csv("SnapTimeline.csv", parse_dates=["Date"])
df['Social Interaction Level'] = df['Social Interaction Level'].astype(int)
df["Snap_Social_Score"] = ( #weighted memories count higher bc of statistical analysis and ommited chats sent
    1.0*df["Snaps_Sent_Count"] + #1.5
    #df["Chats_Sent_Count"] + 
    2*df["Memories_Count"]
)
#df.to_csv("Social Results",index=False)

X = df[["Snap_Social_Score"]] 
y = df["Social Interaction Level"]

#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=20)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=20
)

print("Class distribution:")
print(df["Social Interaction Level"].value_counts())
# Build model
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=20)
rf_classifier.fit(X_train, y_train)


y_pred = rf_classifier.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print(classification_report(y_test, y_pred,zero_division=0))

sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()
