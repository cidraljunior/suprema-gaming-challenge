with dates as (
    
    select distinct bet_date as date_day
    from {{ ref('stg_report__daily_betting_summary') }}
    
    union distinct
    
    select distinct rate_date as date_day
    from {{ ref('stg_exchangerate__history') }}

),

date_spine as (
    
    select
        
        date_trunc('day', date_day) as date,
        extract(year from date_day) as year,
        extract(month from date_day) as month,
        extract(day from date_day) as day,
        extract(quarter from date_day) as quarter,
        extract(week from date_day) as week_of_year,
        extract(dayofweek from date_day) as day_of_week,
        extract(day from date_day) as day_of_month,
    
    from dates

)

select
    {{ dbt_utils.generate_surrogate_key(['date']) }} as date_key,
    *
from date_spine