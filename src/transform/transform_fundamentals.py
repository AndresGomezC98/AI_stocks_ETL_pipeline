import polars as pl 
from datetime import date, timedelta,datetime

def transform_fundamentals_plain(ticker_id:int,data_fundamentals:dict):
    if data_fundamentals is None:
        pass
    else:
        schema_i={"ticker_id":pl.Int64,"reporting_date":pl.Date,"market_capitalization":pl.Int64,"pe_ratio":pl.Float64,"peg_ratio":pl.Float64,"EPS":pl.Float64,"forwardPE":pl.Float64}
        clean_data_list =list()
        data_to_process=dict()
        reporting_date_b=data_fundamentals["LatestQuarter"]
        market_capitalization_b=data_fundamentals["MarketCapitalization"]
        pe_ratio_b=data_fundamentals["PERatio"]
        peg_ratio_b=data_fundamentals["PEGRatio"]
        EPS_b=data_fundamentals["EPS"]
        forwardPE_b=data_fundamentals["ForwardPE"]


        reporting_date_a=datetime.strptime(reporting_date_b,'%Y-%m-%d').date()
        market_capitalization_a=int(market_capitalization_b)
        pe_ratio_a=float(pe_ratio_b)
        peg_ratio_a=float(peg_ratio_b)
        EPS_a=float(EPS_b)
        forwardPE_a=float(forwardPE_b)

        data_to_process["ticker_id"]=ticker_id
        data_to_process["reporting_date"]=reporting_date_a
        data_to_process["market_capitalization"]=market_capitalization_a
        data_to_process["pe_ratio"]=pe_ratio_a
        data_to_process["peg_ratio"]=peg_ratio_a
        data_to_process["EPS"]=EPS_a
        data_to_process["forwardPE"]=forwardPE_a

        clean_data_list.append(data_to_process)

        data_f =pl.DataFrame(clean_data_list,schema=schema_i).lazy()

        bad_data= (pl.col("market_capitalization")<0) | (pl.col("pe_ratio")<0) |(pl.col("peg_ratio")<0) | (pl.col("EPS")<0) | (pl.col("forwardPE")<0)
        is_violation= data_f.select(bad_data.any()).collect().item()
        if is_violation:
            raise ValueError(" some value is incorrect please verify before to continue")
        else:
            return data_f


