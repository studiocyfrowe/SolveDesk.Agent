import os
import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine

class LumosLoader:
    def __init__(self):
        connection_string = os.getenv('CONNECTION_STRING')

        if not connection_string:
            raise ValueError("Missing CONNECTION_STRING in environment variables")

        self.engine = create_engine(connection_string)

    def read_data(self, query: str | None = None) -> DataFrame:
        if not query:
            raise ValueError("No SQL query provided")

        return pd.read_sql(query, self.engine)