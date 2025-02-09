with
    source as (
        select
            try_to_date(date, 'MM/DD/YYYY') as bet_date,
            profit,
            players,
            "BET AMOUNT" as bet_amount
        from {{ source("airbyte_raw", "report_daily_betting_summary") }}
    )

select *
from source
