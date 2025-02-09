with source as (

    select * from {{ source("airbyte_raw", "report_daily_betting_summary") }}

),

renamed as (
     
    select
        -- dates
        try_to_date(date, 'MM/DD/YYYY') as bet_date,

        -- numerics
        profit as profit_usd,
        players as total_players,
        "BET AMOUNT" as bet_amount_usd
    
    from source
)

select * from renamed
