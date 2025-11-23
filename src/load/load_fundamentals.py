from src.database.connection import get_db_connection
from transform.transform_fundamentals import transform_fundamentals_plain
from database.querys import query_to_load_fundamentals
import polars as pl

def load_fundamental_indicators (data:pl.LazyFrame):
    try:
        data_to_load =data.collect()
        data_row =data_to_load.row()
        connection=get_db_connection()
        cur =connection.cursor()

        cur.execute(query_to_load_fundamentals,data_row)
        connection.commit()

    except Exception as e:

        connection.rollback()
        raise e
    finally:
        if cur:
            cur.close()
        if connection:
            connection.close()

