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
      time=[3298, 3507, 17416, 21652, 14849, 3781],
      bytes=[137615686,137369684,65905329,68870016,137369222,400545731],
      points=['tck', 'trk', 'trk.gz', 'trx', 'trx32', 'vtk']
   )
)

# Scatter plot
ax = df.plot.scatter(title='M1', x='time', y='bytes', alpha=0.5)
ax.set_ylim(ymin=0)
# Annotate each data point
for i, txt in enumerate(df.points):
   ax.annotate(txt, (df.time.iat[i], df.bytes.iat[i]))

#plt.show()
plt.savefig('M1.png', dpi=300)