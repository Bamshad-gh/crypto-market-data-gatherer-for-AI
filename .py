class Get_crypto_data():
    def __init__(self,crypto_exchange:(str),num_of_last_data=12,main_crypto:(str)='BTC/USDT'
                 ,exchange_platform:(str)='bitso',path:(str)='C:/Users/User/Desktop/Smart Market/Data/Crypto',
                 Labelized:(bool)=True) -> pd.DataFrame:
        
        self.crypto_exchange=crypto_exchange
        self.main_crypto=main_crypto
        self.exchange_platform=exchange_platform
        self.path=path
        self.Labelized=Labelized
        self.num_of_last_data=num_of_last_data

    
    def labelized(self,data,auto_labeled:(bool)=True,number_of_Label=5
                  ,Thmin=-5,THmean1=-1.5,THmean2=1.5,ThMax=5):

        if number_of_Label == 5:
            if auto_labeled==True:
                Thmin=data.quantile(0.2)
                THmean1=data.quantile(0.4)
                THmean2=data.quantile(0.6)
                ThMax=data.quantile(0.8)
            data_new = np.where(data< Thmin, 0, np.nan)
            data_new = np.where((data> Thmin) & (data < THmean1), 1, data_new)
            data_new = np.where((data> THmean1) & (data < THmean2), 2, data_new)
            data_new = np.where((data> THmean2) & (data < ThMax), 3, data_new)
            data_new = np.where(data > ThMax, 4, data_new)
            TO=[Thmin,THmean1,THmean2,ThMax]
        elif number_of_Label == 3:
            if auto_labeled==True:
                Thmin=data.quantile(0.33)
                THmean1=data.quantile(0.66)
            data_new = np.where(data< Thmin, 0, np.nan)
            data_new = np.where((data> Thmin) & (data < THmean1), 1, data_new)
            data_new = np.where(data > THmean1, 2, data_new)
            TO=[THmean1,THmean2]
        elif number_of_Label == 2:
            
            data_new = np.where(data< 0, 0, np.nan)
            data_new = np.where(data> 0 , 1, data_new)
            TO=[-0,0]


        else:
            print('wrong Number it must 2 OR 3 OR 5')
            
        return pd.Series (data_new) , TO
    
    def get_crypto_data(self,timeframe:(str)='1h',since:(str)='2023-01-01T00:00:00Z',TH=1):
        print(f'geting {self.crypto_exchange}...')
        
        # download data for each Brooker
        ph=getattr(ccxt,self.exchange_platform)()
        #set coin name
        symol=self.crypto_exchange

        if symol != 'BTC/USDT' and timeframe=='1d':
            self.exchange_platform='kucoin'
        # download data for each Brooker
        ph=getattr(ccxt,self.exchange_platform)()
        start=ph.parse8601 (since)
        try:
            bars=ph.fetch_ohlcv(symbol=symol ,timeframe=timeframe,since=start, limit=None)
        except:
            time.sleep(1)
            bars=ph.fetch_ohlcv(symbol=symol ,timeframe=timeframe,since=start, limit=None)

        

        
        data=pd.DataFrame(bars,columns=['Datetime','Open','High','Low','Close','Volume'])
        data['Datetime']=pd.to_datetime(data['Datetime'],unit='ms')
        data=data.rename(columns={'Datetime':'Date'})
        # remove time from Date

        data['Date'] = pd.to_datetime(data['Date'])
        if timeframe == '1d':
            data['Date'] = pd.to_datetime(data['Date']).dt.date
            data['Date'] = pd.to_datetime(data['Date'])
        data.set_index('Date')
        #'nowC_LastC% means change by percentage from now to last close'
        ########## ADD Main Stock Feuturs ##########
        # main Stock Close Change
        data['nowC_LastC%']=((data['Close']/data['Close'].shift(periods=+1))-1)*100
        for i in range (1,self.num_of_last_data):
            N=i
            L=i+1
            data[f'Last{N}C_{L}LastC%']=((data['Close'].shift(periods=N)/data['Close'].shift(periods=L))-1)*100





        data['nowC_2LastC%']=((data['Close']/data['Close'].shift(periods=+2))-1)*100
        data['nowC_3LastC%']=((data['Close']/data['Close'].shift(periods=+3))-1)*100

        # main Stock Volume Change
        data['nowV_LastV%']=((data['Volume']/data['Volume'].shift(periods=+1))-1)*100
        data['LastV_2LastV%']=((data['Volume'].shift(periods=+1)/data['Volume'].shift(periods=+2))-1)*100
        data['nowV_2LastV%']=((data['Volume']/data['Volume'].shift(periods=+2))-1)*100
        data['nowV_3LastV%']=((data['Volume']/data['Volume'].shift(periods=+3))-1)*100
        
        data=data.replace([np.inf, -np.inf], np.nan)
        #data.dropna(inplace=True,axis=0)
    

        data=data.replace(0, np.nan).ffill()
        data=data.replace([np.inf, -np.inf], np.nan)
        #data.dropna(inplace=True,axis=0)
        print('Done!')
        
        return data
    
    def get_BTC_data(self,timeframe:(str)='1h',since:(str)='2023-01-01T00:00:00Z'):
       
        print(f'geting BTC/USDT...')
        # download data for each Brooker
   
        #set coin name and clean data
        symol=self.crypto_exchange
        if symol != 'BTC/USDT' and timeframe=='1d':
            self.exchange_platform='kucoin'
            
        ph=getattr(ccxt,self.exchange_platform)()
        start=ph.parse8601 (since)
        
        try:
            bars=ph.fetch_ohlcv(symbol=symol ,timeframe=timeframe,since=start, limit=None)
        except:
            time.sleep(1)
            bars=ph.fetch_ohlcv(symbol=symol ,timeframe=timeframe,since=start, limit=None)
        ########## ADD BTC features ##########
        data=pd.DataFrame(bars,columns=['Datetime','Open','High','Low','Close','Volume'])
        data['Datetime']=pd.to_datetime(data['Datetime'],unit='ms')
        
        data[f'BTC_nowC_LastC%']=((data['Close']/data['Open'])-1)*100
        data[f'BTC_LastC_2LastC%']=((data['Close'].shift(1)/data['Close'].shift(2))-1)*100
        #data[f'BTC_nowC_2LastC%']=((data['Close']/data['Close'].shift(2))-1)*100
        data[f'BTC_nowV_LastV%']=((data['Volume']/data['Volume'].shift(+1))-1)*100

        # refine and remove UNwanted data  
        data=data.drop(['Open','High','Low','Volume'],axis=1)
        data=data.rename(columns={'Close':'BTC_Close'})  
        data=data.rename(columns={'Datetime':'Date'})  
        #data.reset_index(inplace=True)
        data['Date'] = pd.to_datetime(data['Date'])
        if timeframe == '1d':
            data['Date'] = pd.to_datetime(data['Date']).dt.date
            data['Date'] = pd.to_datetime(data['Date'])
        data=data.replace(0, np.nan).ffill()
    
        
        data.set_index('Date')

        print('Done!')
        
        return data


    def get_Stock_Data(self,symbol:(str),since:(str)='2023-01-01',timeframe:(str)='1h',Add_time_delta:(int)=0):
        
        #set names
        if len(since) > 10:
            since=since[0:10]
        data = yf.Ticker(symbol)
        if symbol == 'ES=F':
            name='mini_S_and_P_500'
        elif symbol == 'CL=F':
            name='Oil'
        elif symbol == 'GC=F':
            name='Gold'
        elif symbol == 'NVDA':
            name='Nvidia'
        print(f'geting {name}...')
        
        
        if timeframe == '1h':
            # get data
            MFD = data.history(start = since , interval = timeframe)
            MFD.index = MFD.index.tz_convert('UTC')
            MFD.index = MFD.index.tz_localize(None)
            MFD.reset_index(inplace=True)
            MFD=MFD.rename(columns={'Datetime':'Date'})
            MFD['Date'] = pd.to_datetime(MFD['Date'])
            MFD['Date']=MFD['Date']+datetime.timedelta(minutes=Add_time_delta)
            MFD.set_index('Date')
            
            #shif 3 hours
            # MFD=MFD.shift(periods=-1)
            # MFD.dropna(inplace=True,axis=0)
            
        elif timeframe=='1d':
            MFD = data.history(start = since , interval = timeframe)
            MFD.index = MFD.index.tz_convert('UTC')
            MFD.index = MFD.index.tz_localize(None)
            MFD.reset_index(inplace=True)
            MFD['Date'] = pd.to_datetime(MFD['Date'])
            MFD['Date'] = pd.to_datetime(MFD['Date']).dt.date
            MFD['Date'] = pd.to_datetime(MFD['Date'])
            MFD.set_index('Date')

        else:
            print('timeframe must 1d or 1h')
        MFD=MFD.replace(0, np.nan).ffill()
        MFD[f'{name}_nowC_LastC%']=((MFD['Close']/MFD['Open'])-1)*100
        MFD[f'{name}_LastC_2LastC%']=((MFD['Close'].shift(1)/MFD['Close'].shift(2))-1)*100
        #MFD[f'{name}_nowtC_2LastC%']=((MFD['Close']/MFD['Open'])-1)*100
        MFD[f'{name}_Volume change %']=((MFD['Volume']/MFD['Volume'].shift(+1))-1)*100
        # remove usless columns
        MFD=MFD.drop(['Open','High','Low','Dividends','Stock Splits'],axis=1)
        # rename close and volume
        MFD=MFD.rename(columns={'Close':f'{name}_Close'})
        MFD=MFD.rename(columns={'Volume':f'{name}_Volume'})
        # remove time from Date)
   
        # Turn time to Data Frame
        #MFD['Date']=pd.to_datetime(MFD['Date'])
        MFD=MFD.replace(0, np.nan).ffill()
        print('Done!')
        return pd.DataFrame(MFD)
    
    def Labelized_Data(self,data,timeframe,Labelize_just_Target:(bool)=False,Labelze_Volume:(bool)=True,
                       auto_labeled:(bool)=True,number_of_Label=5
                  ,Thmin=-5,THmean1=-1.5,THmean2=1.5,ThMax=5):
        
        if timeframe=='1h' and auto_labeled==False:
            Thmin,THmean,ThMax = -2.6,0.6,2.6
        if Labelize_just_Target == False:
            data =data
            #### Main Stock Close Change ####
            data['nowC_LastC%']=self.labelized(data['nowC_LastC%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]
            for i in range (1,self.num_of_last_data):
                N=i
                L=i+1
                data[f'Last{N}C_{L}LastC%']=self.labelized(data[f'Last{N}C_{L}LastC%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]



            
            data['nowC_2LastC%']=self.labelized(data['nowC_2LastC%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]
            data['nowC_3LastC%']=self.labelized(data['nowC_3LastC%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]

            #### main Coin Volume Change ####
            if Labelze_Volume == True:

                data['nowV_LastV%']=self.labelized(data['nowV_LastV%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]
                data['LastV_2LastV%']=self.labelized(data['LastV_2LastV%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]
                data['nowV_2LastV%']=self.labelized(data['nowV_2LastV%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]
                data['nowV_3LastV%']=self.labelized(data['nowV_3LastV%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]
            if self.crypto_exchange != 'BTC/USDT':
                #### BTC close ####
                data[f'BTC_nowC_LastC%']=self.labelized(data['BTC_nowC_LastC%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]
                data[f'BTC_LastC_2LastC%']=self.labelized(data[f'BTC_LastC_2LastC%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]
                if Labelze_Volume == True:
                    #### BTC Volume ####
                    data[f'BTC_nowV_LastV%']=self.labelized(data[f'BTC_nowV_LastV%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]

            ##### STOCK ####
            data[f'mini_S_and_P_500_nowC_LastC%']=self.labelized(data['mini_S_and_P_500_nowC_LastC%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]
            data[f'mini_S_and_P_500_LastC_2LastC%']=self.labelized(data[f'mini_S_and_P_500_LastC_2LastC%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]


            data[f'Oil_nowC_LastC%']=self.labelized(data['Oil_nowC_LastC%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]
            data[f'Oil_LastC_2LastC%']=self.labelized(data[f'Oil_LastC_2LastC%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]


            data[f'Gold_nowC_LastC%']=self.labelized(data['Gold_nowC_LastC%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]
            data[f'Gold_LastC_2LastC%']=self.labelized(data[f'Gold_LastC_2LastC%'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]
            if Labelze_Volume == True:
                    #### Stock Volume ####
                    data['mini_S_and_P_500_Volume change %']=self.labelized(data['mini_S_and_P_500_Volume change %'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]

                    data['Oil_Volume change %']=self.labelized(data['Oil_Volume change %'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]

                    data['Gold_Volume change %']=self.labelized(data['Gold_Volume change %'],auto_labeled=auto_labeled,
                                            number_of_Label=number_of_Label
                    ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]
                    




        data['Target']=self.labelized(data['Next'],auto_labeled=auto_labeled,
                                           number_of_Label=number_of_Label
                  ,Thmin=Thmin,THmean1=THmean1,THmean2=THmean2,ThMax=ThMax)[0]
        

        data=data.drop(['Next'],axis=1)

        return data
    def __get_all_Data(self,since:(str)='2023-01-01T00:00:00Z',timeframe:(str)='1h'):
        print('combinig data...')
        if self.crypto_exchange=='BTC/USDT':
            MeRge1=pd.merge_asof(self.get_crypto_data(timeframe=timeframe,since=since), self.get_Stock_Data(symbol='ES=F'
                                                                                                             ,timeframe=timeframe,since=since)
                             , on ='Date', direction = 'nearest')
            print('combination Done!')
               
        else:
            # COMBINE 2 DataFrames of pure stuck and total market
            MeRge=pd.merge_asof(self.get_crypto_data(timeframe=timeframe,since=since), right=self.get_BTC_data(timeframe=timeframe,since=since)
                                , on ='Date', direction = 'backward')
            # COMBINE 2 DataFrames with Manufacture
            MeRge1=pd.merge_asof(MeRge, self.get_Stock_Data(symbol='ES=F',
                                                            timeframe=timeframe,since=since)
                                , on ='Date', direction = 'nearest')

        # Merge More Data
        meRge2=pd.merge_asof(MeRge1, self.get_Stock_Data(symbol='CL=F',
                                                            timeframe=timeframe,since=since)
                                , on ='Date', direction = 'nearest')  
        meRge3=pd.merge_asof(meRge2, self.get_Stock_Data(symbol='GC=F',
                                                            timeframe=timeframe,since=since)
                                , on ='Date', direction = 'nearest') 
        # add nvidia just for dayly time frame
        if timeframe == '1d':
            meRge4=pd.merge_asof(meRge3, self.get_Stock_Data(symbol='NVDA',
                                                            timeframe=timeframe,since=since)
                                , on ='Date', direction = 'nearest') 
            meRge3=meRge4

        # Clean Data
        meRge3=meRge3.replace([np.inf, -np.inf], np.nan)
        meRge3.dropna(inplace=True,axis=0)
        meRge3=meRge3.replace(0, np.nan).ffill()
        #### future price change ####
        meRge3['Next']=((meRge3['Close'].shift(periods=-1)/meRge3['Close'])-1)*100
        print('Done!')

        return meRge3
        
    def show_saved_path(self,timeframe):
        crypto_exchange=self.crypto_exchange.replace('/','-')
        path=f'{self.path}/{crypto_exchange}'
        SavePath = f'''{path}/{crypto_exchange}_in_{timeframe}.csv'''

        return (path , SavePath)
    
    def Save_data(self,since:(str)='2023-01-01T00:00:00Z',timeframe:(str)='1h'): 

        crypto_exchange=self.crypto_exchange.replace('/','-')
        path=f'{self.path}/{crypto_exchange}'
        # Make Folder
        if not os.path.exists(path):
            os.makedirs(path)
        # Make file save path directory
        SavePath = f'''{path}/{crypto_exchange}_in_{timeframe}.csv'''
        # Make File
        if not os.path.exists(SavePath):
            # set Date data to date and time
            try:
                S=self.__get_all_Data(since=since,timeframe=timeframe)   
            except:
                print('something happend cant get and Merg Data Try one more time...')
                time.sleep(2.5)
                S=self.__get_all_Data()

            S['Date']=pd.to_datetime(S['Date'])
            S=S.drop_duplicates().set_index('Date')

            print('saving Data...')

            S.to_csv(path_or_buf=SavePath)
            print(f'Data Saved to {SavePath}')

        
        DataFrame=pd.read_csv(SavePath)
        DataFrame['Date']=pd.to_datetime(DataFrame['Date'])
        
        return DataFrame

    def Last_Updated_Time(self,timeframe):
        L=self.Save_data(timeframe=timeframe)
        
        
        if timeframe == '1h':
            S=str(L['Date'][-1:])[7:18]
            T=str(L['Date'][-1:])[18:27]
        else:
            S=str(L['Date'][-1:])[6:18]
            T=None
        M=((S).replace('-',',').replace('\nN','')).split(',')

        Last1=[]
        for i in M :
            Last1.append(int(i))  
        Last=datetime.date(Last1[0],Last1[1],Last1[2])
        #print(f'Last Updated dat is {Last} or {M}')
        return Last ,T
    
    def Update(self,since:(str)='2023-01-01T00:00:00Z',timeframe:(str)='1h'):

        crypto_exchange=self.crypto_exchange.replace('/','-')
        path=f'{self.path}/{crypto_exchange}'
        SavePath = f'''{path}/{crypto_exchange}_in_{timeframe}.csv'''

        DataFrame=self.Save_data(since=since,timeframe=timeframe)
        # set Now
        Now_Day=datetime.date.today()
        Now_Day_hour=dt.now(pytz.timezone('UTC'))
        
        
        Last2=self.Last_Updated_Time(timeframe=timeframe)[0]
        Last22=self.Last_Updated_Time(timeframe=timeframe)[1]

        #DataFrame=self.Save_data(timeframe=timeframe)
        Last_Data_Date=str(Last2-datetime.timedelta(0))[0:10]
        Last_Data_Date_and_Hour=str(f'{str(Last2)} {Last22}') 
        if timeframe == '1d':
            if Now_Day > Last2 + datetime.timedelta(0) :
                print('Updating Daily...')
                Since=f'{Last_Data_Date}T{'00:00:00'}Z'
                H=self.__get_all_Data(since=Since,timeframe=timeframe)

                if str(DataFrame['Date'].tail(1)) == str(H['Date'].head(1)):
                    DataFrame=DataFrame.drop(DataFrame.tail(1).index)
                    
                H['Date']=pd.to_datetime(H['Date'])
                H=H.set_index('Date').drop_duplicates()

            else:
                H=None

        if timeframe == '1h':   
            print('Updating Hourly ...')
            # turn last data an hour to date time
            print(f'Last data is {Last_Data_Date_and_Hour}')
            LDDaH=[int(i) for i in ((Last_Data_Date_and_Hour).replace('-',',').replace(':',',').replace(' ',',')).split(',') if i]
            LDDaH=dt(LDDaH[0],LDDaH[1],LDDaH[2],LDDaH[3])
            if Now_Day_hour.timestamp() > (LDDaH+datetime.timedelta(minutes=60)).timestamp():

                
                # find out when is first time of Yfinance 
                
                try:
                    Last_Data_Date=str(Last2-datetime.timedelta(2))[0:10]
                    R=self.get_Stock_Data(symbol='ES=F',since=Last_Data_Date,timeframe=timeframe)
                    
                except:
                    print('its Holliday!')
                    Last_Data_Date=str(Last2-datetime.timedelta(3))[0:10]
                    R=self.get_Stock_Data(symbol='ES=F',since=Last_Data_Date,timeframe=timeframe)
                    
                T=str(R['Date'].head(1))[15:24]
                T1=str(R['Date'].head(1))[4:24]
                print(f' new data downloaded from {R['Date'].head(1)} till {R['Date'].tail(1)}')
                
                
                First_Date_Update_Data=[int(i) for i in ((T1).replace('-',',').replace(':',',').replace(' ',',')).split(',')]
                First_Date_Update_Data=dt(First_Date_Update_Data[0],First_Date_Update_Data[1],
                                          First_Date_Update_Data[2],First_Date_Update_Data[3])
                # find diffrence between Last date Old data abd first date of new data
                NR=LDDaH-First_Date_Update_Data
                print(Last_Data_Date)
                print('...........')
                print(NR)
                print(LDDaH)
                print(First_Date_Update_Data)
                S=int((NR.days)*23)
                NR=int(NR.seconds/3600)
                H=self.__get_all_Data(since=f'{T1[:10]}T{T}Z',timeframe=timeframe)
                # remove over writed data
                print('==============')
                print(NR)
                print(len(H))
                print('==============')
                H=H.drop(H.head(NR+S).index)
                print(f'{len(H)} data aded to Old data')
                # clean new data
                H['Date']=pd.to_datetime(H['Date'])
                H=H.set_index('Date')
                
            else:
                H=None

        if not timeframe=='1h' and timeframe == '1d':
            print('timeframe must 1h or 1d')

        if type(H)== pd.DataFrame:

            DataFrame['Date']=pd.to_datetime(DataFrame['Date'])
            DataFrame=DataFrame.set_index('Date')  
            DataFrame=pd.concat([DataFrame,H],join='inner')
            DataFrame.to_csv( SavePath,)        
        DataFrame=pd.read_csv(SavePath)
