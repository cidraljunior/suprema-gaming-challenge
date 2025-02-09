with

    betting as (select * from {{ ref("stg_report__daily_betting_summary") }}),
    rates as (select * from {{ ref("stg_exchangerate__history") }})

select

    betting.bet_date as date,
    betting.profit as profit_usd,
    betting.bet_amount as bet_amount_usd,
    betting.players,
    -- Convert values to BRL using the exchange rate.
    betting.profit * rates.brl_rate as profit_brl,
    betting.bet_amount * rates.brl_rate as bet_amount_brl

from betting

left join rates on betting.bet_date = rates.rate_date
