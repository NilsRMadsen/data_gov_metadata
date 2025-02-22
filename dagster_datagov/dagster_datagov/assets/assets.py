try:
    from . import config, datagov_api_pipeline, date_spine
except ImportError:
    import config, datagov_api_pipeline, date_spine

import dagster as dg

from dagster_dbt import dbt_assets, DbtCliResource, DbtProject


# upstream ingestion assets
@dg.asset(compute_kind='python', pool='duckdb')
def generated_date_spine(context: dg.AssetExecutionContext) -> None:
    date_spine.load_date_spine()

@dg.asset(compute_kind='python', pool='duckdb')
def datagov_group(context: dg.AssetExecutionContext) -> None:
    pipeline = datagov_api_pipeline.DatagovCkanApiPipeline('group')
    pipeline.run()

@dg.asset(compute_kind='python', pool='duckdb')
def datagov_license(context: dg.AssetExecutionContext) -> None:
    pipeline = datagov_api_pipeline.DatagovCkanApiPipeline('license')
    pipeline.run()

@dg.asset(compute_kind='python', pool='duckdb')
def datagov_organization(context: dg.AssetExecutionContext) -> None:
    pipeline = datagov_api_pipeline.DatagovCkanApiPipeline('organization')
    pipeline.run()

@dg.asset(compute_kind='python', pool='duckdb')
def datagov_package(context: dg.AssetExecutionContext) -> None:
    pipeline = datagov_api_pipeline.DatagovCkanApiPipeline('package')
    pipeline.run()


# dbt integration
dbt_project = DbtProject(project_dir=config.DBT_PATH)
dbt_resource = DbtCliResource(project_dir=dbt_project)
dbt_project.prepare_if_dev()

@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
