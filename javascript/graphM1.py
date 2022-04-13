#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pandas as pd
from matplotlib import pyplot as plt

# Set the figure size
plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

# Create a dataframe
df = pd.DataFrame(
   dict(
      time=[3632, 11284, 10702, 11868, 14648, 21283, 21106],
      bytes=[137369684, 67980943,65905329,59829856,68870124,54183032,53941157],
      points=['raw.trk', '1.trk.gz', '6.trk.gz', '11.trk.gz', '1.trx', '4.trx', '6.trx']
   )
)

# Scatter plot
ax = df.plot.scatter(title='M1 (fflate)', x='time', y='bytes', alpha=0.5)
ax.set_ylim(ymin=0)
# Annotate each data point
for i, txt in enumerate(df.points):
   ax.annotate(txt, (df.time.iat[i], df.bytes.iat[i]))

#plt.show()
plt.savefig('M1.png', dpi=300)