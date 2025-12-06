#Module of transform initial data from extract prices.py
from datetime import date,timedelta,datetime
import polars as pl 
schema_i={"ticker_id":pl.Int64,"date_key":pl.Date,"open_price":pl.Float64,"high_price":pl.Float64,"low_price":pl.Float64,"close_price":pl.Float64,"volume":pl.Int64}
def transform_plain_dict_price (ticker_id:int,data:dict):
    clean_data_list=list()
    for x,price in data.items():
        clean_data=dict()
        date= x
        open_p= price["1. open"]
        high = price["2. high"]
        low = price["3. low"]
        close =price["4. close"]
        volume =price["6. volume"]
        
        date_x =datetime.strptime(x,'%Y-%m-%d').date()
        open_f=float(open_p)
        high_f=float(high)
        low_f=float(low)
        close_f=float(close)
        volume_f=int(volume)

        clean_data["ticker_id"]=ticker_id
        clean_data["date_key"]= date_x
        clean_data["open_price"]=open_f
        clean_data["high_price"]=high_f
        clean_data["low_price"]=low_f
        clean_data["close_price"]=close_f
        clean_data["volume"]=volume_f

        clean_data_list.append(clean_data)


    data_f= pl.DataFrame(clean_data_list, schema=schema_i).lazy()
    data_sort= data_f.sort("date_key")
    df_with_retunrs=data_sort.with_columns([pl.col("close_price").pct_change().alias("weekly_return")])
    df_final=df_with_retunrs.with_columns([pl.col("weekly_return").rolling_std(window_size=20).alias("Volatility").fill_null(value=0.0)])
    bad_data=(pl.col("open_price")<= 0) | (pl.col("high_price")<= 0) | (pl.col("low_price")<= 0) | (pl.col("close_price")<= 0) | (pl.col("volume")<= 0) 
    is_violation= df_final.select(bad_data.any()).collect().item()
    if is_violation:
        raise ValueError (" Data is already infect with values incorrect to our database")
    else:
        return df_final





