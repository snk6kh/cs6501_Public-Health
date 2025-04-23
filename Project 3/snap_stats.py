import pandas as pd
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

df = pd.read_csv("SnapTimeline.csv", parse_dates=["Date"])
df['Social Interaction Level'] = df['Social Interaction Level'].astype(int)

# df["Snap_Social_Score"] = (
#     0.5*df["Snaps_Sent_Count"] + 
#     #0.05*df["Chats_Sent_Count"] + 
#     2*df["Memories_Count"]
# )

color_map = {
    0: 'red',
    1: 'orange', 
    2: 'green',
    3: 'blue'   
}


plt.figure(figsize=(12, 6))
for level in sorted(df['Social Interaction Level'].unique()):
    subset = df[df['Social Interaction Level'] == level]
    plt.plot(subset['Date'], subset['Chats_Sent_Count'], 
             marker='o', linestyle='-', 
             label=f'Level {level}', color=color_map[level])

plt.title("Instagram Likes Over Time by Social Interaction Level")
plt.xlabel("Date")
plt.ylabel("Number of Snaps Sent")
plt.legend(title="Interaction Level")
plt.grid(True)
plt.tight_layout()
plt.show()

avg_feature_by_level = df.groupby("Social Interaction Level")["Chats_Sent_Count"].mean() # change to Snaps_Sent_Count or Memories_Count to test the other features
print("Average Feature Value by Social Interaction Level:")
print(avg_feature_by_level)

r, p = spearmanr(df["Chats_Sent_Count"], df["Social Interaction Level"])
print(f"Spearman correlation: r = {r:.3f}, p = {p:.4f}")
