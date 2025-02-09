with
    source as (

        select
            -- dates
            try_to_date(date, 'YYYY-MM-DD') as rate_date,

            -- strings
            base_code as base_currency,

            -- numerics
            conversion_rates:BRL::float as brl_rate

        from {{ source("airbyte_raw", "exchangerate_history") }}
    )

select *
from source
