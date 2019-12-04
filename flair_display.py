import Post_Scraper
import seaborn
import matplotlib.pyplot as plt
import pandas as pd
import numpy

posts, last_date = Post_Scraper.get_posts(1000)

title, content, category = [], [], []
for p in posts:
    title.append(p['title'])
    content.append(p['selftext'])
    # this accounts for new flairs being added as I don't hard code the existing ones anywhere
    category.append(p['link_flair_richtext'][0]['t'] if p['link_flair_richtext'] != [] else 'None')

df = pd.DataFrame({'Title': title, 'Category': category})
ax = seaborn.countplot(y='Category', data=df, order=df['Category'].value_counts().index)

flairs = numpy.unique(category)
flair_freq = [category.count(flair) for flair in flairs]
flair_freq = sorted(flair_freq, reverse=True)

for p, label in zip(ax.patches, flair_freq):
    ax.annotate(label, (p.get_x() + 0.1, p.get_y() + 0.6))

plt.show()
