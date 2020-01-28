import seaborn
import matplotlib.pyplot as plt
import pandas as pd
import numpy

df = pd.read_json('dataframe.json')
print("Retrieved posts.")

ax = seaborn.countplot(y='Category', data=df, order=df['Category'].value_counts().index)

flairs = numpy.unique(df['Category'])
flair_freq = [list(df['Category']).count(flair) for flair in flairs]
flair_freq = sorted(flair_freq, reverse=True)

for p, label in zip(ax.patches, flair_freq):
    ax.annotate(label, (p.get_x() + 0.1, p.get_y() + 0.6))

plt.show()
