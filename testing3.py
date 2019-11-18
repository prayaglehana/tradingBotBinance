import pandas as pd
data=[]
data.append([0,0,0,0,0,0,0,0,0])
df = pd.DataFrame(data, columns = ['Date', 'Open','High','Low','Close','mean','stdev','upperBolBand','LowerBolBand'])
print(df)
