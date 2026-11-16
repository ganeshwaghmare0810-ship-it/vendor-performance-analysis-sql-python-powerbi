"""Load raw CSV files from data/ into the SQLite database data/inventoryy.db."""
import os
import logging
import time
import pandas as pd
from sqlalchemy import create_engine

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/ingestion_db.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
)

engine = create_engine("sqlite:///data/inventoryy.db")


def ingest_db(df, table_name, engine):
    """Write a DataFrame to the database (replaces the table if it exists)."""
    df.to_sql(table_name, con=engine, if_exists="replace", index=False)


def load_raw_data():
    """Read every CSV in data/ and store it as a table named after the file."""
    start = time.time()
    for file in os.listdir("data"):
        if file.endswith(".csv"):
            df = pd.read_csv(os.path.join("data", file))
            logging.info(f"Ingesting {file} into db")
            ingest_db(df, file[:-4], engine)
    logging.info(f"Ingestion complete in {(time.time() - start) / 60:.2f} minutes")


if __name__ == "__main__":
    load_raw_data()
