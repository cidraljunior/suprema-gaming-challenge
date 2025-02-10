# Streamlit Dashboard

This folder contains a **Streamlit** application (`streamlit_app.py`) that visualizes the final betting data from Snowflake.

---

## Table of Contents

1. [Overview](#overview)  
2. [Local Development](#local-development)  
3. [Snowflake Deployment](#snowflake-deployment)  
4. [Dashboards & Features](#dashboards--features)  

---

## Overview

Streamlit is used to create an interactive **Daily Betting Dashboard** with metrics such as:
- **Daily Profit (BRL & USD)**
- **Total Players**
- **Bet Amount**
- **Exchange Rate** Over Time

---

## Local Development

1. **Set up a virtual environment**:

```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install dependencies**:

```bash
pip install -e .[dev]
```

3. **Set environment variables** (e.g., in a `.env` file or by exporting them):

```bash
export SNOWFLAKE_ACCOUNT='your_account'
export SNOWFLAKE_USER='your_username'
export SNOWFLAKE_PASSWORD='your_password'
export SNOWFLAKE_ROLE='your_role'
export SNOWFLAKE_WAREHOUSE='your_warehouse'
export SNOWFLAKE_DATABASE='your_database'
export SNOWFLAKE_SCHEMA='your_schema'
```

4. **Run Streamlit**:

```bash
streamlit run streamlit_app.py
```

5. **Open** <http://localhost:8501> to view the dashboard.

---

## Snowflake Deployment

If you’d like to host your Streamlit app **within Snowflake** (using Snowflake Streamlit Integration):

1. **Create a Streamlit App** in the Snowflake web UI (Admin > Streamlit > Create App).  
2. Provide:
   - **App Name** (e.g., `daily_betting_dashboard`)
   - **Main File** (upload or reference `streamlit_app.py`)
   - **Dependencies** (`environment.yml` or a custom setup)

3. Run: 

```
snow streamlit deploy
```


---

## Dashboards & Features

The app provides:

1. **KPI Metrics**: Profit, Bet Amount, Exchange Rate, etc.  
2. **Trend Charts**: Using Altair for daily or monthly trends.  
3. **Day of Week Analysis**: Bar chart of average profit by day of week.  
4. **Calendar Heatmap**: Visualizing daily profit across months.  
5. **Dual Axis Chart**: Overlays exchange rate vs. daily profit.

---