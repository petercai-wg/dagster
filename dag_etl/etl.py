from dagster import (
    Out,
    Output,
    job,
    op,
    sensor,
    RunRequest,
    graph,
    In,
    Nothing,
    resource,
)
import pandas as pd
import logging
import os


from .db import get_db_conn, get_db_engine


@op
def setup_logger():
    logging.basicConfig(
        filename="/Temp/logs/my_dagster.log",
        format="%(asctime)s - %(message)s",
        level=logging.INFO,
    )

    logging.info("set up logging config ....")


@op(
    ins={"start": In(Nothing)},
    out={"df": Out(is_required=True), "tbl": Out(is_required=True)},
)
def extract_employee_data(context):
    try:

        with get_db_conn() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "select name from sqlite_master where type = 'table' and name = 'Employee' "
            )
            tables = cursor.fetchall()

            for tbl in tables:
                df = pd.read_sql_query(f"select * from {tbl[0]} ", conn)
                context.log.info(f"read from  {tbl[0]}")
                logging.info("logger read * from " + str(tbl[0]))

                yield Output(df, "df")
                yield Output(tbl[0], "tbl")

    except Exception as e:
        logging.exception("Data Extract Exception", e)


@op
def load_employee_backup(context, df, tbl):
    try:

        stg_table = f"stg_{tbl}"
        logging.info(df.head())
        context.log.info(f"importing rows  {len(df)} for {stg_table}")
        engine = get_db_engine()
        df.to_sql(stg_table, engine, if_exists="replace", index=False)
        context.log.info("load completed...")
    except Exception as e:
        logging.exception("Data Extract Exception", e)
        context.log.error("load error ")


@job
def run_employee_etl_job():
    # setup_logger()
    # show_db_version()
    df, tbl = extract_employee_data(start=setup_logger())
    load_employee_backup(df, tbl)
