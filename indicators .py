def EMA(Data:pd.DataFrame, Days:int, a:int=1) -> pd.DataFrame:
    Alpha = (1 + a) / (Days + a) # Calculating Alpha
    Data.loc[:, f'EMA({Days})'] = Data.loc[:, 'Close']/Data.loc[:, 'Close'].ewm(alpha=Alpha).mean()-1
    return Data
def MACD(Data,F_days:int=12,s_days:int=24,c:int=9):
    df_fast = Data['Close'].ewm(span=F_days , min_periods = F_days).mean()
    df_slow = Data['Close'].ewm(span=s_days , min_periods = s_days).mean()
    Data['MACD'] = df_fast - df_slow
    Data['Signal'] = Data['MACD'].ewm(span= c , min_periods = c).mean()  
    Data.dropna(inplace=True)
    return Data

def STC(Data:pd.DataFrame, Days:int) -> pd.DataFrame:
    LL = Data.loc[:, 'Low'].rolling(window=Days).min() # Moving Min
    HH = Data.loc[:, 'High'].rolling(window=Days).max() # Moving Max
    Data.loc[:, f'STC({Days})'] = 100 * (Data.loc[:, 'Close'] - LL) / (HH - LL)
    Data.dropna(inplace=True)
    return Data
def RSI(Data,Days:int=14):
    delta=Data['Close'].diff(1)
    delta = delta.dropna()
    up=delta.copy()
    down=delta.copy()
    up[up<0]=0
    down[down>0]=0
    avg_gain=up.rolling(window=Days).mean()
    avg_loss=abs(down.rolling(window=Days).mean())
    RS = avg_gain/avg_loss
    Data[f'RSI {Days}'] = 100.0 - (100.0/(1.0+RS))
    #Data.dropna(inplace=True)
    return Data
