import matplotlib.pyplot as plt
import pandas as pd
import datetime

import sunpy_meta


data = pd.read_csv('sunpy_history.csv', parse_dates=True, index_col=0)

x = data.index
y1 = data['code'].values / 10000.
y2 = data['comment'].values / 10000.

plt.plot(x, y1, label='code', color='black', linestyle='-')
plt.plot(x, y2, label='comment', color='black', linestyle='--')

plt.ylabel('Lines (thousands)')
plt.ylim(0, 4)

for this_release in sunpy_meta.sunpy_releases:
    plt.axvline(pd.to_datetime(sunpy_meta.sunpy_releases[this_release]), color='black', alpha=0.2, linestyle='-')
    plt.text(pd.to_datetime(sunpy_meta.sunpy_releases[this_release]) + datetime.timedelta(days=15), 0.2, this_release, size='smaller', rotation=90)


plt.legend(loc=2)
plt.savefig('sunpy_history.pdf')

