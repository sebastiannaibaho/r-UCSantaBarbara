import seaborn
import matplotlib.pyplot as plt
import numpy
import os
import pandas as pd
import re


def plot(df, name=''):
    ax = seaborn.countplot(y='category', data=df, order=df['category'].value_counts().index)

    flairs = numpy.unique(df['category'])
    flair_freq = [list(df['category']).count(flair) for flair in flairs]
    flair_freq = sorted(flair_freq, reverse=True)

    for p, label in zip(ax.patches, flair_freq):
        ax.annotate(label, (p.get_x() + 0.1, p.get_y() + 0.45))

    if name:
        plt.savefig("FlairPlots/" + str(re.search(r'^[a-zA-Z]+', name).group(0)) + ".png", bbox_inches='tight')
    else:
        plt.show()

    plt.clf()


'''
# go make plots for all the files in Raw
files = os.listdir("Raw")
print(files)
[plot(pd.read_json("Raw/" + f), f) for f in files]
'''
