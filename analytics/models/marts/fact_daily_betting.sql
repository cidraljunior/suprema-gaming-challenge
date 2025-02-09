with

    betting as (select * from {{ ref("stg_report__daily_betting_summary") }}),
    rates as (select * from {{ ref("stg_exchangerate__history") }})

select

    {{ dbt_utils.generate_surrogate_key(['betting.bet_date']) }} as date_key,

    betting.bet_date,
    betting.total_players,
    betting.profit_usd,
    betting.bet_amount_usd,
    rates.brl_rate,
    (betting.profit_usd * rates.brl_rate) as profit_brl,
    (betting.bet_amount_usd * rates.brl_rate) as bet_amount_brl

from betting

left join rates on betting.bet_date = rates.rate_date

