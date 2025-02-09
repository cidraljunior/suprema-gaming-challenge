from dagster import AssetSelection, define_asset_job


all_pipeline_job =define_asset_job(
    name="all_pipeline_job",
    selection=AssetSelection.all()
)