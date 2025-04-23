import pandas as pd
from scipy.stats import spearmanr
import matplotlib.pyplot as plt

df = pd.read_csv("Timeline.csv", parse_dates=["Date"])
df['Social Interaction Level'] = df['Social Interaction Level'].astype(int)

color_map = {
    0: 'red',
    1: 'orange',  
    2: 'green',
    3: 'blue'   
}

plt.figure(figsize=(12, 6))
for level in sorted(df['Social Interaction Level'].unique()):
    subset = df[df['Social Interaction Level'] == level]
    plt.plot(subset['Date'], subset['Likes'], 
             marker='o', linestyle='-', 
             label=f'Level {level}', color=color_map[level])
plt.title("Instagram Likes Over Time by Social Interaction Level")
plt.xlabel("Date")
plt.ylabel("Number of Likes")
plt.legend(title="Interaction Level")
plt.grid(True)
plt.tight_layout()
plt.show()

avg_likes_by_level = df.groupby("Social Interaction Level")["Likes"].mean()
print("Average Likes by Social Interaction Level:")
print(avg_likes_by_level)

r, p = spearmanr(df["Likes"], df["Social Interaction Level"])
print(f"Spearman correlation: r = {r:.3f}, p = {p:.4f}")
