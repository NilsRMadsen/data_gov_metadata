from dagster import ScheduleDefinition
from ..jobs import run_all_assets

run_all_assets_schedule = ScheduleDefinition(
    job=run_all_assets
    , cron_schedule="0 5 * * *" # every morning at 5am
    , execution_timezone='US/Central'
)