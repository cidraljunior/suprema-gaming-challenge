import os
from datetime import timedelta
import streamlit as st
import pandas as pd
import altair as alt
from snowflake.snowpark.session import Session
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# --- Snowflake Connection Setup ---
try:
    session = get_active_session()
except Exception:
    connection_parameters = {
        "account": os.environ.get("SNOWFLAKE_ACCOUNT"),
        "user": os.environ.get("SNOWFLAKE_USER"),
        "password": os.environ.get("SNOWFLAKE_PASSWORD"),
        "role": os.environ.get("SNOWFLAKE_ROLE"),
        "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE"),
        "database": os.environ.get("SNOWFLAKE_DATABASE"),
        "schema": os.environ.get("SNOWFLAKE_SCHEMA")
    }
    session = Session.builder.configs(connection_parameters).create()

# --- Streamlit App Code ---

st.set_page_config(layout="wide", page_title="Daily Betting Dashboard - BRL Analysis")

@st.cache_data()
def load_data():
    """
    Loads data from star schema tables with date dimension joins
    """
    query = (
        session.table("DATA_ANALYTICS.DBT_MARTS.FACT_DAILY_BETTING")
        .join( session.table("DATA_ANALYTICS.DBT_MARTS.DIM_DATE"), "DATE_KEY")
    )
    return query.to_pandas()

# Load and prepare the data
df = load_data()
df['DATE'] = pd.to_datetime(df['DATE'])
df = df.sort_values("DATE")

# --- Header
st.title("Daily Betting Dashboard - BRL Analysis")
st.markdown("---")

# Date selection using date dimension attributes
min_date = df['DATE'].min().date()
max_date = df['DATE'].max().date()
default_start = max_date - pd.Timedelta(days=365)

start_date, end_date = st.date_input(
    "Select Date Range",
    [default_start, max_date],
    min_value=min_date,
    max_value=max_date
)
start_dt = pd.to_datetime(start_date)
end_dt = pd.to_datetime(end_date)

filtered_df = df[(df['DATE'] >= start_dt) & (df['DATE'] <= end_dt)]

# --- KPIs ---
current_rate = filtered_df['BRL_RATE'].iloc[-1] if not filtered_df.empty else 0
total_profit_brl = filtered_df['PROFIT_BRL'].sum()
total_bets_brl = filtered_df['BET_AMOUNT_BRL'].sum()
total_players = filtered_df['TOTAL_PLAYERS'].sum()
avg_bet_size_brl = total_bets_brl / total_players if total_players > 0 else 0
avg_profit_per_player = total_profit_brl / total_players if total_players > 0 else 0

st.subheader("Key Performance Indicators")
kpi1, kpi2, kpi3 = st.columns(3)
kpi4, kpi5, kpi6 = st.columns(3)
kpi1.metric(
    label="Current Exchange Rate (USD->BRL)",
    value=f"R$ {current_rate:,.2f}",
    help="Latest USD to BRL conversion rate"
)
kpi2.metric(
    label="Total Profit (BRL)",
    value=f"R$ {total_profit_brl:,.2f}",
    help="Total net profit in Brazilian Real"
)
kpi3.metric(
    label="Total Bets (BRL)",
    value=f"R$ {total_bets_brl:,.2f}",
    help="Total betting volume in Brazilian Real"
)
kpi4.metric(
    label="Total Players",
    value=f"{total_players:,.0f}",
    help="Total number of players"
)
kpi5.metric(
    label="Avg Bet Size (BRL)",
    value=f"R$ {avg_bet_size_brl:,.2f}",
    help="Average bet amount per player"
)
kpi6.metric(
    label="Profit/Player (BRL)",
    value=f"R$ {avg_profit_per_player:,.2f}",
    help="Average profit per player"
)

# --- Trend Analysis with Date Attributes ---
st.subheader("Temporal Analysis")

time_granularity = st.selectbox(
    "Select Time Granularity",
    ["Daily", "Weekly", "Monthly", "Quarterly"],
    index=0
)
agg_map = {
    "Daily": ('DATE', 'DATE'),
    "Weekly": ('WEEK_OF_YEAR', 'Week'),
    "Monthly": ('MONTH', 'Month'),
    "Quarterly": ('QUARTER', 'Quarter')
}

time_col, time_label = agg_map[time_granularity]

trend_df = filtered_df.groupby(time_col).agg({
    'PROFIT_BRL': 'sum',
    'BET_AMOUNT_BRL': 'sum',
    'TOTAL_PLAYERS': 'sum'
}).reset_index()

trend_chart = alt.Chart(trend_df).mark_line().encode(
    x=alt.X(f'{time_col}:N', title=time_label),
    y=alt.Y('PROFIT_BRL:Q', title='Profit (BRL)'),
    tooltip=[
        alt.Tooltip(f'{time_col}:N', title=time_label),
        'PROFIT_BRL:Q',
        'BET_AMOUNT_BRL:Q',
        'TOTAL_PLAYERS:Q'
    ]
).properties(
    title=f'Profit Trend by {time_granularity}',
    width=800,
    height=400
)
st.altair_chart(trend_chart.interactive(), use_container_width=True)

# --- Day of Week Analysis ---
st.subheader("Day of Week Patterns")

dow_df = filtered_df.groupby('DAY_OF_WEEK').agg({
    'PROFIT_BRL': 'mean',
    'BET_AMOUNT_BRL': 'mean',
    'TOTAL_PLAYERS': 'mean'
}).reset_index()

dow_chart = alt.Chart(dow_df).mark_bar().encode(
    x=alt.X('DAY_OF_WEEK:O', title='Day of Week (1=Sunday)'),
    y=alt.Y('PROFIT_BRL:Q', title='Average Profit (BRL)'),
    tooltip=['DAY_OF_WEEK', 'PROFIT_BRL', 'BET_AMOUNT_BRL', 'TOTAL_PLAYERS']
).properties(
    title='Average Performance by Day of Week',
    width=800,
    height=400
)
st.altair_chart(dow_chart.interactive(), use_container_width=True)
st.markdown("---")

# --- Players vs. Profit ---
st.subheader("Players vs. Profit")
players_profit_chart = alt.Chart(filtered_df).mark_circle(size=60).encode(
    x=alt.X('TOTAL_PLAYERS:Q', title='Players'),
    y=alt.Y('PROFIT_BRL:Q', title='Profit (BRL)'),
    color=alt.Color('DATE:T', scale=alt.Scale(scheme='viridis')),
    tooltip=['DATE', 'TOTAL_PLAYERS', 'PROFIT_BRL']
).properties(
    title='Players vs. Profit (BRL)',
    width=800,
    height=400
)
st.altair_chart(players_profit_chart.interactive(), use_container_width=True)

st.markdown("---")

# --- Calendar Heatmap ---
st.subheader("Daily Profit Calendar Heatmap")

heatmap_data = filtered_df[['DATE', 'PROFIT_BRL']].copy()
heatmap_data['YEAR'] = heatmap_data['DATE'].dt.year
heatmap_data['MONTH'] = heatmap_data['DATE'].dt.month_name()
heatmap_data['DAY'] = heatmap_data['DATE'].dt.day

heatmap = alt.Chart(heatmap_data).mark_rect().encode(
    x=alt.X('DAY:O', title='Day of Month'),
    y=alt.Y('MONTH:O', title='Month'),
    color=alt.Color('PROFIT_BRL:Q', 
                   scale=alt.Scale(scheme='goldred'),
                   legend=alt.Legend(title="Profit (BRL)")),
    tooltip=['DATE', 'PROFIT_BRL', 'YEAR']
).properties(
    width=800,
    height=400
).facet(
    column='YEAR:O'
)
st.altair_chart(heatmap)

# --- Dual-Axis Chart ---
st.subheader("Exchange Rate vs Profit Trend")

base = alt.Chart(filtered_df).encode(x='DATE:T')

line1 = base.mark_line(color='#4CAF50').encode(
    y=alt.Y('BRL_RATE:Q', axis=alt.Axis(title='Exchange Rate', titleColor='#4CAF50')),
    tooltip=['DATE', 'BRL_RATE']
)

line2 = base.mark_line(color='#FF5722').encode(
    y=alt.Y('PROFIT_BRL:Q', axis=alt.Axis(title='Profit (BRL)', titleColor='#FF5722')),
    tooltip=['DATE', 'PROFIT_BRL']
)

dual_axis = alt.layer(line1, line2).resolve_scale(
    y='independent'
).properties(
    width=1000,
    height=400
)

st.altair_chart(dual_axis)

# --- Detailed Data ---
st.subheader("Detailed Data")
st.dataframe(filtered_df.sort_values("DATE", ascending=False))
