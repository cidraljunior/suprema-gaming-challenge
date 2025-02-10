# Airbyte Setup Guide

This directory covers **Airbyte** configuration for ingesting betting data and exchange rate data into Snowflake.

---

## Table of Contents

1. [Overview](#overview)
2. [Local Installation](#local-installation)
3. [Using Airbyte Cloud](#using-airbyte-cloud)
4. [Custom ExchangeRate Connector](#custom-exchangerate-connector)
5. [Creating Connections](#creating-connections)
6. [Testing & Troubleshooting](#testing--troubleshooting)

---

## Overview

We use Airbyte to:
- Ingest **Bet Test Data** (e.g., daily betting summary) from CSV or a custom source.
- Fetch **USD->BRL exchange rates** from a custom ExchangeRate-API connector.
- Load both datasets into **Snowflake** (raw schema in `airbyte_db`).

---

## Local Installation

1. **Install `abctl`** (Airbyte CLI):

```
curl -LsfS https://get.airbyte.com | bash -
```

2. **Install Airbyte**:

```
abctl local install
```

3. **Start Airbyte**:

```
abctl local start
```

4. **Check UI**: Access the Airbyte UI at <http://localhost:8000/>.

### Credentials / Setup
After running:

```
abctl local credentials --email test@test.com
```

You’ll see local admin credentials to log in.

---

## Using Airbyte Cloud

If you’d rather not run Airbyte locally, you can:
1. **Create an Airbyte Cloud account** at <https://airbyte.com/>.
2. **Create a new Workspace**.
3. **Set up your Source** (CSV, ExchangeRate-API) and your Destination (Snowflake) similarly through the UI.

---

## Custom ExchangeRate Connector

Inside [`source-exchange-rate-api/manifest.yaml`](./source-exchange-rate-api/manifest.yaml) is a **declarative connector** for `ExchangeRate-API`.

**Steps** to add it in the Airbyte UI:
1. Go to **Settings -> Custom Connector** (in Airbyte Local or Cloud).
2. **Import from JSON or YAML**: Select `manifest.yaml`.
3. Provide your **API Key**, **base currency** (e.g., `USD`), and the **start date** for fetching historical data.

---

## Creating Connections

In Airbyte, create two main connections:

1. **Betting Data (CSV -> Snowflake)**  
   - **Source**: `File-based` or a custom CSV source.  
   - **Destination**: Snowflake. Provide credentials matching the `airbyte_user` and `loader` role in Snowflake.  
   - **Sync Frequency**: On Demand or scheduled.  
   - **Destination Namespace**: `raw` (or leave it as `_airbyte`).  

2. **Exchange Rate (Custom -> Snowflake)**  
   - **Source**: Our custom ExchangeRate-API connector (manifest).  
   - **Destination**: Snowflake in `raw`.  
   - **Sync Frequency**: On Demand or scheduled.

---

## Testing & Troubleshooting

- **Check Sync Logs** in the Airbyte UI if data fails to land in Snowflake.
- **Snowflake Access**: Make sure the `airbyte_user` has `USAGE` and `CREATE` on the `raw` schema.
- **Connector Logs**: If the custom connector fails, review Airbyte logs or CLI output.

---
