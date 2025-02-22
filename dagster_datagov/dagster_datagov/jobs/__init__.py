from dagster import AssetSelection, define_asset_job

run_all_assets = define_asset_job(
    name='run_all_assets'
    , selection=AssetSelection.all()
)
