from dagster import Definitions, ScheduleDefinition
from dagster_dbt import DbtCliResource

from .assets import dbt_project_assets, all_airbyte_assets, airbyte_workspace
from .project import dbt_project
from .jobs import all_pipeline_job


defs = Definitions(
    assets=all_airbyte_assets + [dbt_project_assets],
    resources = {
        "dbt": DbtCliResource(project_dir=dbt_project),
        "airbyte": airbyte_workspace
    },
    schedules=[
        ScheduleDefinition(job=all_pipeline_job, cron_schedule="0 3 * * *")
    ]
)
