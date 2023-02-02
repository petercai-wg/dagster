import pandas as pd
from dagster import asset, Output, OpExecutionContext, AssetOut, multi_asset
from dag_etl import db as db
from typing import Tuple


# @multi_asset(
#     group_name="firstjob",
#     outs={
#         "df": AssetOut(),
#         "db_table": AssetOut(),
#     },
# )
# def download_csv_pd() -> Tuple[pd.DataFrame, str]:
@asset(group_name="firstjob")
def download_csv_pd() -> pd.DataFrame:
    url = "https://docs.dagster.io/assets/cereal.csv"
    df = pd.read_csv(url)
    # metadata = {"num_records": len(df), "table_name": "Cereal"}

    # return df, "Cereal"
    return df


@asset(group_name="firstjob")
def load_dataframe(context: OpExecutionContext, download_csv_pd) -> str:
    stg_table = "Cereal"
    df = download_csv_pd

    try:
        context.log.info(f"importing rows  {len(df)} for {stg_table}")
        engine = db.get_db_engine()
        df.to_sql(stg_table, engine, if_exists="replace", index=False)
        context.log.info("load completed...")
    except Exception as e:
        context.log.error("load error ")

    return stg_table
