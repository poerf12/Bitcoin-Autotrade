import ccxt
import pprint
import time
import pandas as pd
from datetime import datetime

# Keys
api_key = "api"
secret  = "secret"

# Log in

binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret
})

# Ohlcv and Preprocessing

btc_ohlcv= binance.fetchOHLCV(symbol='BTC/USDT', timeframe='1d')
df = pd.DataFrame(btc_ohlcv,columns=['datetime','open','high','low','close','volume'])
closedata=df['close']

df = pd.DataFrame(btc_ohlcv,columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')
print(df)


print(df['close'])

closedate=df['close']
delta=closedata.diff()

print(delta)
print(df['close'])

ups, downs = delta.copy(), delta.copy()
ups[ups < 0] = 0
downs[downs > 0] = 0

roll_up= pd.stats.moments.ewma(up, lookback)
roll_down= pd.stats.moments.ewma(down.abs(), lookback)
# Calculate the SMA
roll_up= roll_up[lookback:]
roll_down= roll_down[lookback:]
Data= Data.iloc[lookback + 1:,].values
# Calculate the RSI based on SMA
RS= roll_up /roll_down
RSI= (100.0 -(100.0 /(1.0 + RS)))
RSI= np.array(RSI)
RSI= np.reshape(RSI, (-1, 1))
Data= np.concatenate((Data, RSI), axis= 1)

lower_barrier= 30
upper_barrier= 70
width= 10

# Bullish Divergence
for i in range(len(Data)):
   try:
       if Data[i, 4] < lower_barrier:
           for a in range(i + 1, i + width):
               if Data[a, 4] > lower_barrier:
                    for r in range(a + 1, a + width):
                       if Data[r, 4] < lower_barrier and \
                        Data[r, 4] > Data[i, 4] and Data[r, 3] < Data[i, 3]:
                            for s in range(r + 1, r + width):
                                if Data[s, 4] > lower_barrier:
                                    Data[s + 1, 5]= 1
                                    break
                                else:
                                    continue
                       else:
                            continue
                    else:
                        continue
               else:
                    continue
   except IndexError:
        pass
# Bearish Divergence
for i in range(len(Data)):
   try:
       if Data[i, 4] > upper_barrier:
           for a in range(i + 1, i + width):
               if Data[a, 4] < upper_barrier:
                   for r in range(a + 1, a + width):
                       if Data[r, 4] > upper_barrier and \
                       Data[r, 4] < Data[i, 4] and Data[r, 3] > Data[i, 3]:
                           for s in range(r + 1, r + width):
                               if Data[s, 4] < upper_barrier:
                                   Data[s + 1, 6]= -1
                                   break
                               else:
                                   continue
                       else:
                           continue
                   else:
                       continue
               else:
                   continue
   except IndexError:
       pass