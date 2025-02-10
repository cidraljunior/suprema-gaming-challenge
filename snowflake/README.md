# Snowflake Setup Guide

This folder contains SQL scripts and environment information to configure Snowflake for the Betting Data Pipeline project.

---

## Table of Contents

1. [Overview](#overview)  
2. [Snowflake Objects](#snowflake-objects)  
3. [Setup Steps](#setup-steps)  
4. [Running SQL Scripts](#running-sql-scripts)  
5. [Connecting from dbt & Tools](#connecting-from-dbt--tools)  
6. [Best Practices & Tips](#best-practices--tips)  

---

## Overview

We use Snowflake as the centralized data warehouse:

- **Airbyte** loads raw data into `airbyte_db.raw`.  
- **dbt** transforms data from `airbyte_db.raw` into `data_analytics.staging` and `data_analytics.marts`.  
- **Streamlit** and **Power BI** query the final marts for reporting.

---

## Snowflake Objects

We organize Snowflake objects using the following structure:

- **Warehouses**: `loading`, `transforming`, `reporting`  
- **Databases**:  
  - `airbyte_db` (for raw ingest)  
  - `data_analytics` (for staging + marts)  
- **Schemas**:  
  - `raw` (within `airbyte_db`)  
  - `staging` and `marts` (within `data_analytics`)  
- **Roles**:  
  - `loader` (for Airbyte user)  
  - `transformer` (for dbt user)  
  - `reporter` (for analysts, Power BI, Streamlit)

---

## Setup Steps

1. **Create a Snowflake account** (or use an existing one).  
2. **Clone this repo** and navigate to the `snowflake/` folder.  
3. **Open** the Snowflake web UI or use SnowSQL CLI.

---

## Running SQL Scripts

We have two main scripts:

1. **`setup_snowflake_infrastructure.sql`**  
   - Creates roles (`loader`, `transformer`, `reporter`).  
   - Creates warehouses (`loading`, `transforming`, `reporting`).  
   - Creates databases (`airbyte_db`, `data_analytics`).  
   - Creates schemas (e.g. `raw`, `staging`, `marts`).  
   - Grants privileges to roles.  
   - Creates users (e.g. `airbyte_user`, `dbt_user`, `streamlit_user`, etc.).

2. **`create_analyst_user.sql`**  
   - Example script for creating an additional user with the `transformer` or `reporter` role.

**Usage** (in Snowflake Worksheet or CLI):

```
-- Switch to the SECURITYADMIN role
USE ROLE SECURITYADMIN;
-- Paste or import the contents of setup_snowflake_infrastructure.sql
-- Then run.

-- Similarly, to create an analyst user:
USE ROLE SECURITYADMIN;
-- Paste or import create_analyst_user.sql script
-- Then run.
```

---

## Connecting from dbt & Tools

- **dbt** uses the connection details from `analytics/profiles.yml`. Make sure your environment variables match the user/password set in the Snowflake script.  
- **Airbyte**: If using a dedicated Airbyte user, confirm:
  - Snowflake account host
  - Warehouse
  - Database
  - Schema
  - Role
  - Username / Password  
- **Streamlit**: The app relies on environment variables (see [Streamlit README](../streamlit/README.md)) to connect to Snowflake.

---

## Best Practices & Tips

1. **Use Strong Passwords**: Replace placeholder passwords in the scripts with secure ones.  
2. **Role-based Access**: The loader/transformer/reporter roles ensure separation of duties.  
3. **Warehouse Sizing**: `XSMALL` might suffice for demos. Scale up for production.  
4. **Data Governance**: Evaluate if you need more schemas for dev/test/prod, or if you have multiple subject areas.  

---
