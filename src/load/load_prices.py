# load prices to SQL database 
from src.database.connection import get_db_connection
from transform.transform_prices import transform_plain_dict_price
import polars as pl
from database.querys import query_to_load


def load_historical_prices(connection_db, price_data:pl.Lazyframe):
    try:

        data_to_load= price_data.collect()
        data_row=data_to_load.rows()


        cur=connection_db.cursor()

        query=query_to_load
        cur.executemany(query,data_row)
        connection_db.commit()

    finally:
        if cur:
            cur.close()
        if connection_db:
            connection_db.close()
