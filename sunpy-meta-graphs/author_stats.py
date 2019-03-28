from git import Repo
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
sns.set()

import sunpy_meta

repo_path = sunpy_meta.repo_path
repo = Repo(repo_path)


commits = list(repo.iter_commits('master'))
commit_datetime = [pd.to_datetime(str(c.committed_datetime)) for c in commits]
author_names = [c.author.name.lower() for c in commits]
author_emails = [c.author.email for c in commits]
data = pd.DataFrame(data={'author_name': author_names, 'author_email': author_emails}, index=commit_datetime)

# the following fixes duplicate author entries in the log
replace_fix = {'albert y. shih':['albert shih', 'ayshih'], 'alex hamilton':['alex', 'alex-ian-hamilton'], 'ankit kumar': ['ankitkmr'],
               'andrew hill': ['andrew hill (astroengisci)'],
               'ankit kumar':['ankitmr'], 'andrew inglis':['aringlis'], 'dan ryan':['danryanirish'],
               'david pérez-suárez':['david ps', 'davidps', 'david perez-suarez', 'dpshelio'], 'jack ireland':['wafels'],
               'drew leonard':['drew'], 'jongyeob park':['jongyeob'], 'nabil freij':['nabobalis', 'nabil'], 'naman':['naman9639'],
               'pritish chakraborty': ['pritishc'], 'punyaslok pattnaik':['punyaslokpattnaik@yahoo.co.in', 'punyaslok'],
               'rajul srivastava': ['rajul'], 'vishnunarayan k i': ['vn ki', 'vn-ki'], 'steven d. christe':['steven christe'], 'michael kirk':['mskirk'],
               'Monica Bobra': ['mbobra'], 'russell hewett': ['rhewett'],
               'stuart mumford': ['u cadair core\\stuart', 'codetriage-readme-bot', '', 'system administrator', 'unknown'],
               'yash jain': ['yash_jain'], 'sanskar modi':['sanskar-modi'], 'sallyda':['sally']
              }

for key in replace_fix:
    for alias in replace_fix[key]:
        data['author_name'][data['author_name'] == alias] = key


temp = data['author_name'].resample('M').apply(set)
x = pd.DataFrame(data={'set': temp.values}, index=temp.index)
x['count'] = [len(v) for v in x['set'].values]


# author commits
x['count'].plot(ls='steps')
plt.ylabel('Committers per month')
for this_release in sunpy_meta.sunpy_releases:
    plt.axvline(pd.to_datetime(sunpy_meta.sunpy_releases[this_release]), color='black', alpha=0.5, linestyle='--')
    plt.text(pd.to_datetime(sunpy_meta.sunpy_releases[this_release]), 16, this_release, size='smaller')
plt.savefig('committers_per_month_vs_time.pdf')


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
    plt.axvline(pd.to_datetime(sunpy_meta.sunpy_releases[this_release]), color='black', alpha=0.5, linestyle='--')
    plt.text(pd.to_datetime(sunpy_meta.sunpy_releases[this_release]), 140, this_release, size='smaller')
plt.savefig('cumulative_authors.pdf')


# now create a plot of the number of commits versus the number of committers
author_count = data.groupby('author_name').count()
author_count.sort_values('author_email', inplace=True)
bins=np.logspace(np.log10(1),np.log10(10000), 20)
author_count.hist(bins=bins)
vals, bins = np.histogram(author_count.values, bins=bins)

bin_centers = np.log10(bins) + (np.log10(bins[1]) - np.log10(bins[0]))/2.
x = bin_centers[:-1]
y = np.log10(vals)
result = np.polyfit(x[:-4], y[:-4], deg=1)
print(result)
plt.plot(10**x[:-4], 10**(result[0] * x[:-4] + result[1]), label='N$^{' + '{0:0.2f}'.format(result[0]) + '}$')
plt.legend()

plt.yscale('log')
plt.xscale('log')
plt.ylabel('number of committers')
plt.xlabel('number of commits')

plt.title('')
plt.savefig("busfactor_plot.pdf")

