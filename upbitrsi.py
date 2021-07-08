import time
import pyupbit
import datetime
import pandas

# acces key

access = "nMdEtad6mi5tU8vqkfhfE9FXR8TjvqsX6SIPiB1E"
secret = "DoDe7Bz5AsH8X6ifdpy6F0CImLMzTDsYTonZaY6i"


upbit = pyupbit.Upbit(access, secret)
print(upbit.get_balances())


# close price listing

data = pyupbit.get_ohlcv(ticker="KRW-XRP", interval="minute5")
closedata = data["close"]
delta = closedata.diff()

def rsi(ohlc: pandas.DataFrame, period: int = 14):
    delta = ohlc["close"].diff()
    ups, downs = delta.copy(), delta.copy()
    ups[ups < 0] = 0
    downs[downs > 0] = 0

    AU = ups.ewm(com = period-1, min_periods = period).mean()
    AD = downs.abs().ewm(com = period-1, min_periods = period).mean()
    RS = AU/AD

    return pandas.Series(100 - (100/(1 + RS)), name = "RSI")

coinlist = ["KRW-BTC", "KRW-XRP", "KRW-ETC", "KRW-ETH", "KRW-BCH", "KRW-EOS"]
lower28 = []
higher70 = []

for i in range(len(coinlist)):
    lower28.append(False)
    higher70.append(False)


while(True): 
    for i in range(len(coinlist)):
        data = pyupbit.get_ohlcv(ticker=coinlist[i], interval="minute3")
        now_rsi = rsi(data, 14).iloc[-1]
        # print("코인명: ", coinlist[i])
        # print("현재시간: ", datetime.datetime.now())
        # print("RSI :", now_rsi)
        # print()
        if now_rsi <= 28 : 
            lower28[i] = True
        elif now_rsi >= 33 and lower28[i] == True:
            buy(coinlist[i])
            lower28[i] = False
        elif now_rsi >= 70 and higher70[i] == False:
            sell(coinlist[i])
            higher70[i] = True
        elif now_rsi <= 60 :
            higher70[i] = False
    time.sleep(0.5)


# buy market price
    def buy(coin):
        money = upbit.get_balance("KRW")
        if money < 20000 :
            res = upbit.buy_market_order(coin, money)
        elif money < 50000:
            res = upbit.buy_market_order(coin, money*0.4)
        elif money < 100000 :
            res = upbit.buy_market_order(coin, money*0.3)
        else :
            res = upbit.buy_market_order(coin, money*0.2)
        return
    # sell market price
    def sell(coin):
        amount = upbit.get_balance(coin)
        cur_price = pyupbit.get_current_price(coin)
        total = amount * cur_price
        if total < 20000 :
            res = upbit.sell_market_order(coin, amount)
        elif total < 50000:
            res = upbit.sell_market_order(coin, amount*0.4)
        elif total < 100000:
            res = upbit.sell_market_order(coin, amount*0.3)
        else :
            res = upbit.sell_market_order(coin, amount*0.2)
        return

print('1')