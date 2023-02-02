from dagster import (
    Definitions,
    ScheduleDefinition,
    define_asset_job,
    load_assets_from_package_module,
)

from . import assets
from .secondjob import my_directory_sensor

from .etl import run_employee_etl_job


# from .etl import my_graph

daily_refresh_schedule = ScheduleDefinition(
    job=define_asset_job(name="etl_job"), cron_schedule="0 0 * * *"
)

defs = Definitions(
    assets=load_assets_from_package_module(assets),
    schedules=[daily_refresh_schedule],
    sensors=[my_directory_sensor],
    jobs=[run_employee_etl_job],
)
