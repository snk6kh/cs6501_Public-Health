from joblib import load
import pandas as pd

clf_model = load("binary_socialmodel.joblib")

df = pd.read_csv("FullYear.csv")

df["Snap_Social_Score"] = (
    1.0*df["Snaps_Sent_Count"] + #1.5
    2*df["Memories_Count"]
)


X_year = df[["Likes", "Snap_Social_Score"]]

predicted_binary_labels = clf_model.predict(X_year)

df["Predicted_Social_Interaction_Level"] = predicted_binary_labels

df["Probability_High_Interaction"] = clf_model.predict_proba(X_year)[:, 1]
df.to_csv("predicted_social_interaction_by_day.csv", index=False)
