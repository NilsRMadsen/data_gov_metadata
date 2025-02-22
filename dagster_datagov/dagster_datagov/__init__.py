from dagster import Definitions, load_assets_from_modules
from .assets import assets
from .jobs import run_all_assets
from .schedules import run_all_assets_schedule


all_assets = load_assets_from_modules([assets])
all_jobs = [run_all_assets]
all_schedules = [run_all_assets_schedule]

# Dagster definitions object
defs = Definitions(
    assets=[*all_assets]
    , resources={"dbt": assets.dbt_resource}
    , jobs=all_jobs
    , schedules=all_schedules
)