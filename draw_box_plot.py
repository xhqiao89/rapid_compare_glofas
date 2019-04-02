import matplotlib.pyplot as plt
import pandas as pd

metric_df = pd.read_csv(r"/Users/wade/PycharmProjects/py3k/Historic_Validation/all_comparison_results.csv")
metric_df = metric_df.drop(['Unnamed: 0', 'Location'], axis=1)

print(metric_df)

labels = metric_df.columns
metric_data = metric_df.values
titles = [
    "Kling-Gupta Efficiency (2012)",
    "Normalized Root Mean Square Error (IQR)",
    "Pearson Correlation Coefficient",
    "Symmetric Mean Absolute Percentage Error (1)"
]

fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))

axes = axes.flatten()

i = 0
boxplots = []
for label, title in zip(labels, titles):
    boxplot = axes[i].boxplot(metric_data[:, i], vert=True, patch_artist=True, labels=[label])
    axes[i].set_title(title)
    boxplots.append(boxplot)

    i += 1

colors = ['pink', 'lightblue', 'lightgreen', "Gold"]
for bplot, color in zip(boxplots, colors):
    for patch in bplot['boxes']:
        patch.set_facecolor(color)

plt.tight_layout()

plt.savefig("Box_Plot_Results.png")