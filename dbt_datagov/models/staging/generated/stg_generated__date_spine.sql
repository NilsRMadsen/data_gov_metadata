with date_spine as (

    select *
    from {{ source('generated', 'date_spine') }}

)

, date_calcs as (

    select
        calendar_date
        , extract(year from calendar_date) as calendar_year
        , extract(quarter from calendar_date) as calendar_quarter
        , extract(month from calendar_date) as calendar_month
        , extract(dayofyear from calendar_date) as day_of_year
        , extract(day from calendar_date) as day_of_month
        , extract(isodow from calendar_date) as day_of_week
        , extract(week from calendar_date) as iso_week_of_year
        , 'Q' || extract(quarter from calendar_date) as quarter_name
        , monthname(calendar_date) as month_name
        , strftime(calendar_date, '%b') as month_abbr
        , dayname(calendar_date) as day_of_week_name
        , strftime(calendar_date, '%a') as day_of_week_abbr
        , datetrunc('year', calendar_date) as start_of_year
        , datetrunc('quarter', calendar_date) as start_of_quarter
        , datetrunc('month', calendar_date) as start_of_month
        , last_day(calendar_date) as end_of_month
        , datetrunc('week', calendar_date) as start_of_week
    from date_spine

)

select *
from date_calcs