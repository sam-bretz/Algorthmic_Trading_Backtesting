"""
Basic Algorithmic Trading Backtesting Platform
Author: Samuel Bretz
Email: bretzsam@gmail.com

"""

import oandapy as opy
import os
import pandas as pd
import numpy as np

# Get API information from environment variables
oanda_key = os.environ.get('OANDA_API_KEY')
oanda_account_id = os.environ.get('OANDA_ACCOUNT_ID')

oanda = opy.API(environment='practice',
                access_token=oanda_key)

# Get some data and set up dataframe
data = oanda.get_history(instrument='EUR_USD',  # our instrument
                         start='2016-12-08',  # start data
                         end='2016-12-10',  # end date
                         granularity='M1')  # minute bars

df = pd.DataFrame(data['candles']).set_index('time')
df.index = pd.DatetimeIndex(df.index)

# Get returns and start a momentum strategy
df['returns'] = np.log(df['closeAsk'] / df['closeAsk'].shift(1))
cols = []
for momentum in [15, 30, 60, 120]:
    col = 'position_%s' % momentum
    df[col] = np.sign(df['returns'].rolling(momentum).mean())
    cols.append(col)