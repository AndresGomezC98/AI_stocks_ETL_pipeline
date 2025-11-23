import polars as pl
from src.transform.transform_prices import transform_plain_dict_price
from datetime import date
from polars.testing import assert_frame_equal

data_test = {
        "2025-11-21": {
            "1. open": "305.5900",
            "2. high": "306.0000",
            "3. low": "288.0700",
            "4. close": "297.4400",
            "5. adjusted close": "297.4400",
            "6. volume": "23675512",
            "7. dividend amount": "0.0000"
        },
        "2025-11-14": {
            "1. open": "306.8200",
            "2. high": "324.9000",
            "3. low": "297.5900",
            "4. close": "305.6900",
            "5. adjusted close": "305.6900",
            "6. volume": "22302392",
            "7. dividend amount": "1.6800"
        },
        "2025-11-07": {
            "1. open": "308.0000",
            "2. high": "315.4400",
            "3. low": "296.0000",
            "4. close": "306.3800",
            "5. adjusted close": "304.7239",
            "6. volume": "27157777",
            "7. dividend amount": "0.0000"
        },
        "2025-10-31": {
            "1. open": "307.8000",
            "2. high": "319.3500",
            "3. low": "301.6300",
            "4. close": "307.4100",
            "5. adjusted close": "305.7484",
            "6. volume": "32440643",
            "7. dividend amount": "0.0000"
        },
        "2025-10-24": {
            "1. open": "281.2500",
            "2. high": "310.7500",
            "3. low": "263.5623",
            "4. close": "307.4600",
            "5. adjusted close": "305.7981",
            "6. volume": "51704434",
            "7. dividend amount": "0.0000"
        },
        "2025-10-17": {
            "1. open": "279.7900",
            "2. high": "285.4500",
            "3. low": "272.5469",
            "4. close": "281.2800",
            "5. adjusted close": "279.7596",
            "6. volume": "19005226",
            "7. dividend amount": "0.0000"
        }}

TICKER = 'MSFT'

expected_df = pl.DataFrame(
    {
        "ticker_id": [TICKER,TICKER,TICKER,TICKER,TICKER,TICKER],
        "date_key": [date(2025, 11, 21),date(2025,11,14),date(2025,11,7),date(2025,10,31),date(2025,10,24),date(2025,10,17)], # Tipo Date
        "open_price": [305.59,306.82,308.00,307.80,281.25,279.79],           # Tipo Float64
        "high_price": [306.00,324.90,315.44,319.35,310.75,285.45],           # Tipo Float64
        "low_price": [288.07,297.59,296.00,301.63,263.56,272.5469],            # Tipo Float64
        "close_price": [297.44,305.69,306.38,307.41,307.46,281.28],          # Tipo Float64
        "volume": [23675512,22302392,27157777,32440643,51704434,19005226],             # Tipo Int64
    },
    schema={
        "ticker_id": pl.String,
        "date_key": pl.Date,
        "open_price": pl.Float64,
        "high_price": pl.Float64,
        "low_price": pl.Float64,
        "close_price": pl.Float64,
        "volume": pl.Int64,
    }
)

expected_df_sort=expected_df.sort("date_key")

def test_initial ():
    result=transform_plain_dict_price(TICKER,data_test)
    result_sort=result.sort("date_key")
    assert_frame_equal(result_sort.collect(), expected_df_sort, check_dtype=True, atol=1e-4)


