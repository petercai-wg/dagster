python -m venv dagit
Scripts\activate.bat

pip install dagster dagit

dagster project scaffold --name dag_etl

cd C:\ws\py\dagit\dag_etl
pip install -e ".[dev]"

set windows DAGSTER_HOME environment variable
Dagster tries to load your instance, looking for an instance config file at $DAGSTER_HOME/dagster.yaml.


https://dagster.io/blog/dagster-crash-course-oct-2022
https://github.com/petehunt/dagster-github-stars-example/tree/quickstart/my-dagster-project/my_dagster_project
https://github.com/dagster-io/dagster/tree/master/examples


C:\app\sqlite\sqlite3 etl_db.sqlite3
.tables,  .schema table_name

dagster dev  --Launches Dagit and the Dagster daemon, start a full local deployment, read pyproject.toml
#Note that several Dagster features, like schedules and sensors, require the Dagster daemon to be running in order to function.

dagit  (works if .workspace.yaml exists)
dagster-daemon run 
