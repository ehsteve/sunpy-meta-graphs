import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytz
import seaborn as sns
from git import Repo

import sunpy_meta
from parse_mailmap import get_author_transform_mapping

sns.set()

repo_path = '/home/stuart/Git/sunpy'
repo = Repo(repo_path)

commits = list(repo.iter_commits('master'))
commit_datetime = [pd.to_datetime(c.committed_datetime.astimezone(pytz.utc)) for c in commits]
authors = [f"{c.author.name} <{c.author.email}>" for c in commits]
mailmap = get_author_transform_mapping(repo)
mapped_authors = [mailmap.get(a.strip().lower(), a.strip().lower()) for a in authors]
author_names = [c.author.name.lower() for c in commits]
author_emails = [c.author.email for c in commits]
data = pd.DataFrame(
    data={
        'author': mapped_authors
    },
    index=commit_datetime)

temp = data['author'].resample('M').apply(set)
x = pd.DataFrame(data={'set': temp.values}, index=temp.index)
x['count'] = [len(v) for v in x['set'].values]

# author commits
x['count'].plot(ls='steps')
plt.ylabel('Committers per month')
for this_release in sunpy_meta.sunpy_releases:
    plt.axvline(
        pd.to_datetime(sunpy_meta.sunpy_releases[this_release]),
        color='black',
        alpha=0.5,
        linestyle='--')
    plt.text(
        pd.to_datetime(sunpy_meta.sunpy_releases[this_release]),
        16,
        this_release,
        size='smaller')
plt.savefig('committers_per_month_vs_time.pdf')

plt.figure()
# now plot cumulative authors as a function of time
a = set()
result = []
for i in range(len(x['set'].values)):
    these_authors = x['set'].values[0:i]
    a = []
    for this_set in these_authors:
        a += (list(this_set))
    result.append(len(set(a)))
cum_authors = pd.Series(data=result, index=temp.index)
cum_authors.plot()
plt.ylabel('Cumulative Authors')

for this_release in sunpy_meta.sunpy_releases:
    plt.axvline(
        pd.to_datetime(sunpy_meta.sunpy_releases[this_release]),
        color='black',
        alpha=0.5,
        linestyle='--')
    plt.text(
        pd.to_datetime(sunpy_meta.sunpy_releases[this_release]),
        140,
        this_release,
        size='smaller')
plt.savefig('cumulative_authors.pdf')

plt.figure()
# now create a plot of the number of commits versus the number of committers
author_count = data.groupby('author').apply(lambda x: len(x))
# author_count.sort_values('author', inplace=True)
bins = np.logspace(np.log10(1), np.log10(10000), 20)
author_count.hist(bins=bins)
vals, bins = np.histogram(author_count.values, bins=bins)

bin_centers = np.log10(bins) + (np.log10(bins[1]) - np.log10(bins[0])) / 2.
x = bin_centers[:-1]
y = np.log10(vals)
result = np.polyfit(x[:-4], y[:-4], deg=1)
print(result)
plt.plot(10**x[:-4], 10**(result[0] * x[:-4] + result[1]),
         label='N$^{' + '{0:0.2f}'.format(result[0]) + '}$')
plt.legend()

# plt.yscale('log')
plt.xscale('log')
plt.ylabel('number of committers')
plt.xlabel('number of commits')

plt.title('')
plt.savefig("busfactor_plot.pdf")

plt.show()
