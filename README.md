this small project , gather crypto data based on different time zones + gather related stock tada like nvidia and also gather gold data and save all of them in a csv or excel file in given path 
and after that it clean and labelize data , make ready to go for AI training for price prediction 
how it works ? 
lets say you wanna have BTC price from 01 01 2024 and dayly time frame, you should initiate object and give options for that : 
  d=Get_crypto_data('BTC/USDT')
  S=d.Save_data('2024-01-01T00:00:00Z',timeframe='1d')
