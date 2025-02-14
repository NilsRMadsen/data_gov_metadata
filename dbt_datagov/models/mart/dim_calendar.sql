with date_spine as (

    select *
    from {{ ref('stg_generated__date_spine') }}

)

, dim_calendar as (

    select
        calendar_date
        , calendar_year
        , calendar_quarter
        , calendar_month
        , day_of_year
        , day_of_month
        , day_of_week
        , iso_week_of_year
        , quarter_name
        , month_name
        , month_abbr
        , day_of_week_name
        , day_of_week_abbr
        , start_of_year
        , start_of_quarter
        , start_of_month
        , end_of_month
        , start_of_week
    from date_spine

)

select *
from dim_calendar