try:
    from . import datagov_api_pipeline, date_spine
except ImportError:
    import datagov_api_pipeline, date_spine

import dagster as dg

from dagster_dbt import dbt_assets, DbtCliResource, DbtProject
from pathlib import Path


# upstream ingestion assets
@dg.asset(compute_kind='python', pool='duckdb')
def generated_date_spine(context: dg.AssetExecutionContext) -> None:
    date_spine.load_date_spine()

@dg.asset(compute_kind='python', pool='duckdb')
def datagov_group(context: dg.AssetExecutionContext) -> None:
    datagov_api_pipeline.run_pipeline('group')

@dg.asset(compute_kind='python', pool='duckdb')
def datagov_license(context: dg.AssetExecutionContext) -> None:
    datagov_api_pipeline.run_pipeline('license')

@dg.asset(compute_kind='python', pool='duckdb')
def datagov_organization(context: dg.AssetExecutionContext) -> None:
    datagov_api_pipeline.run_pipeline('organization')

@dg.asset(compute_kind='python', pool='duckdb')
def datagov_package(context: dg.AssetExecutionContext) -> None:
    datagov_api_pipeline.run_pipeline('package')


# dbt integration
dbt_project_directory = Path(__file__).absolute().parent.parent.parent / "dbt_datagov"
dbt_project = DbtProject(project_dir=dbt_project_directory)
dbt_resource = DbtCliResource(project_dir=dbt_project)
dbt_project.prepare_if_dev()

@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["source", "freshness"], context=context).stream()
    yield from dbt.cli(["build"], context=context).stream()


# Dagster definitions object
defs = dg.Definitions(
    assets=[
        generated_date_spine
        , datagov_group
        , datagov_license
        , datagov_organization
        , datagov_package
        , dbt_models
    ]
    , resources={"dbt": dbt_resource}
)