import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Insta Data
insta_df = pd.read_csv("Timeline.csv", parse_dates=["Date"])
insta_df['Social Interaction Level'] = insta_df['Social Interaction Level'].astype(int)

# Snap Data with new .csv including the snap social score
snap_df = pd.read_csv("Social Results.csv", parse_dates=["Date"])
snap_df['Social Interaction Level'] = snap_df['Social Interaction Level'].astype(int)

# Create Snapchat Social Score
# snap_df["Snap_Social_Score"] = (
#     #0.25*snap_df["Snaps_Sent_Count"] + 
#     #0.05*df["Chats_Sent_Count"] + 
#     2*snap_df["Memories_Count"]
# )

# merged_df = pd.merge(
#     insta_df[["Date", "Likes", "Social Interaction Level"]],
#     snap_df[["Date", "Memories_Count","Snaps_Sent_Count", "Snap_Social_Score", "Social Interaction Level"]],
#     on="Date",
#     suffixes=('_insta', '_snap')
# )

merged_df = pd.merge(
    insta_df[["Date", "Likes", "Social Interaction Level"]],
    snap_df[["Date","Snap_Social_Score", "Social Interaction Level"]],
    on="Date",
    suffixes=('_insta', '_snap')
)
print(merged_df[["Likes", "Snap_Social_Score"]].corr())
merged_df["Social Interaction Level"] = merged_df["Social Interaction Level_snap"] #same value if use _insta would not make a difference
# merged_df = merged_df[["Date", "Likes", "Snap_Social_Score", "Social Interaction Level"]]

#merged_df.to_csv("Pre-Classifier.csv")


X = merged_df[["Likes", "Snap_Social_Score"]]
#X = merged_df[["Likes", "Memories_Count", "Snaps_Sent_Count"]]
y = merged_df["Social Interaction Level"]


X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=35
)
rf_classifier = RandomForestClassifier(n_estimators=100, random_state=35) #42
rf_classifier.fit(X_train, y_train)
y_pred = rf_classifier.predict(X_test)


accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy:.2f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

plt.figure(figsize=(6, 5))
sns.heatmap(confusion_matrix(y_test, y_pred), annot=True, cmap="Blues", fmt="d")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()

importances = pd.Series(rf_classifier.feature_importances_, index=X.columns)
print("\nFeature Importances:")
print(importances.sort_values(ascending=False))
