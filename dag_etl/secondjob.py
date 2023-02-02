from dagster import job, op, sensor, RunRequest, DefaultSensorStatus
import os

MY_DIRECTORY = "/tmp/incoming"


@op(config_schema={"filename": str})
def log_file(context):
    filename = context.op_config["filename"]
    context.log.info(filename)


@job
def process_file_job():
    log_file()


@sensor(job=process_file_job, minimum_interval_seconds=30)
def my_directory_sensor():
    for filename in os.listdir(MY_DIRECTORY):
        filepath = os.path.join(MY_DIRECTORY, filename)
        if os.path.isfile(filepath):
            yield RunRequest(
                run_key=filename,
                run_config={"ops": {"log_file": {"config": {"filename": filename}}}},
            )
