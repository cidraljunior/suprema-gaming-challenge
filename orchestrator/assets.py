import dagster
from dagster import AssetExecutionContext, AssetKey
from dagster_airbyte import AirbyteCloudWorkspace, build_airbyte_assets_definitions
from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator

from .project import dbt_project


airbyte_workspace = AirbyteCloudWorkspace(
    workspace_id=dagster.EnvVar("AIRBYTE_CLOUD_WORKSPACE_ID"),
    client_id=dagster.EnvVar("AIRBYTE_CLOUD_CLIENT_ID"),
    client_secret=dagster.EnvVar("AIRBYTE_CLOUD_CLIENT_SECRET"),
)

all_airbyte_assets = build_airbyte_assets_definitions(workspace=airbyte_workspace)


class CustomizedDagsterDbtTranslator(DagsterDbtTranslator):
    def get_asset_key(self, dbt_resource_props):
        resource_type = dbt_resource_props["resource_type"]
        name = dbt_resource_props["name"]
        if resource_type == "source":
            return AssetKey(name)
        else:
            return super().get_asset_key(dbt_resource_props)

@dbt_assets(
    manifest=dbt_project.manifest_path,
    dagster_dbt_translator=CustomizedDagsterDbtTranslator()

)
def dbt_project_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
