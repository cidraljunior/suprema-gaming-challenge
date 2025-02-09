------------------------------------------------------------------------------
-- 1) Set up variable placeholders
------------------------------------------------------------------------------
-- Warehouses
set loading_wh       = 'loading';
set transforming_wh  = 'transforming';
set reporting_wh     = 'reporting';

-- Databases
set airbyte_db       = 'airbyte_db';
set data_db          = 'data_analytics';

-- Schemas
-- For Airbyte, we use the raw schema.
set airbyte_schema   = 'raw';

-- Roles
set loader_role      = 'loader';
set transformer_role = 'transformer';
set reporter_role    = 'reporter';

-- Users
set airbyte_user     = 'airbyte_user';
set dbt_user         = 'dbt_user';
set pbi_user         = 'powerbi_user';
set streamlit_user   = 'streamlit_user';

-- Demo passwords; replace with secure strings in production
set airbyte_pwd      = 'replacewithsecurepassword1!';
set dbt_pwd          = 'replacewithsecurepassword2!';
set pbi_pwd          = 'replacewithsecurepassword3!';
set streamlit_pwd    = 'replacewithsecurepassword4!';

------------------------------------------------------------------------------
-- 2) Create Roles
------------------------------------------------------------------------------
use role securityadmin;

begin;

  create role if not exists identifier($loader_role);
  grant role identifier($loader_role) to role sysadmin;
  
  create role if not exists identifier($transformer_role);
  grant role identifier($transformer_role) to role sysadmin;

  create role if not exists identifier($reporter_role);
  grant role identifier($reporter_role) to role sysadmin;

commit;

------------------------------------------------------------------------------
-- 3) Create Warehouses
------------------------------------------------------------------------------
use role sysadmin;

begin;

  create warehouse if not exists identifier($loading_wh)
    warehouse_size = xsmall
    auto_suspend = 60
    initially_suspended = true;

  create warehouse if not exists identifier($transforming_wh)
    warehouse_size = xsmall
    auto_suspend = 60
    initially_suspended = true;

  create warehouse if not exists identifier($reporting_wh)
    warehouse_size = xsmall
    auto_suspend = 60
    initially_suspended = true;

commit;

------------------------------------------------------------------------------
-- 4) Grant Warehouse Permissions to Roles
------------------------------------------------------------------------------
use role securityadmin;

begin;

  -- LOADER can use the LOADING warehouse
  grant usage on warehouse identifier($loading_wh) to role identifier($loader_role);

  -- TRANSFORMER can use the TRANSFORMING warehouse
  grant all on warehouse identifier($transforming_wh) to role identifier($transformer_role);

  -- REPORTER can use the REPORTING warehouse
  grant all on warehouse identifier($reporting_wh) to role identifier($reporter_role);

commit;

------------------------------------------------------------------------------
-- 5) Create Databases and Schemas
------------------------------------------------------------------------------
use role sysadmin;

-- 5.1 Create the Airbyte database with the RAW schema
begin;
  create database if not exists identifier($airbyte_db);
  use database identifier($airbyte_db);
  create schema if not exists identifier($airbyte_schema);
commit;

-- 5.2 Create the Data Analytics database
begin;
  create database if not exists identifier($data_db);
commit;

------------------------------------------------------------------------------
-- 6) Grant Schema-Level Permissions
use role ACCOUNTADMIN;
use database identifier($airbyte_db);

------------------------------------------------------------------------------
-- 6.1 LOADER role (Airbyte) -> RAW schema in Airbyte database
begin;
  grant ownership on database identifier($airbyte_db) to role identifier($loader_role);
  grant ownership on schema identifier($airbyte_schema) to role identifier($loader_role);
commit;

-- 6.2 TRANSFORMER role -> Read from RAW (in Airbyte DB) and full on STAGING and MARTS (in Data Analytics DB)

-- 6.2.a Transformer access on RAW (read-only) in Airbyte database:
begin;
  grant usage on database identifier($airbyte_db) to role identifier($transformer_role);
  grant usage on all schemas in database identifier($airbyte_db) to role identifier($transformer_role);

  grant select on all tables in database identifier($airbyte_db) to role identifier($transformer_role);
  grant select on all views in database identifier($airbyte_db) to role identifier($transformer_role);
  
  grant usage on future schemas in database identifier($airbyte_db) to role identifier($transformer_role);
  grant select on future tables in database identifier($airbyte_db) to role identifier($transformer_role);
  grant select on future views in database identifier($airbyte_db) to role identifier($transformer_role);
commit;

-- 6.2.b Transformer access on Data Analytics database (full access):
begin;
  grant all on database identifier($data_db) to role identifier($transformer_role);
commit;

-- 6.3 REPORTER role -> MARTS (read-only) in Data Analytics database
begin;
  grant usage on database identifier($data_db) to role identifier($reporter_role);
  grant usage on future schemas in database identifier($data_db) to role identifier($reporter_role);
  grant select on future tables in database identifier($data_db) to role identifier($reporter_role);
  grant select on future views in database identifier($data_db) to role identifier($reporter_role);
commit;

------------------------------------------------------------------------------
-- 7) Create Users and Assign Roles
------------------------------------------------------------------------------
use role securityadmin;

-- 7.1 Airbyte User (LOADER)
begin;
  create user if not exists identifier($airbyte_user)
    password = $airbyte_pwd
    default_role = $loader_role
    default_warehouse = $loading_wh;
    
  grant role identifier($loader_role) to user identifier($airbyte_user);
commit;

-- 7.2 dbt User (TRANSFORMER)
begin;
  create user if not exists identifier($dbt_user)
    password = $dbt_pwd
    default_role = $transformer_role
    default_warehouse = $transforming_wh;
    
  grant role identifier($transformer_role) to user identifier($dbt_user);
commit;

-- 7.3 Power BI User (REPORTER)
begin;
  create user if not exists identifier($pbi_user)
    password = $pbi_pwd
    default_role = $reporter_role
    default_warehouse = $reporting_wh;
    
  grant role identifier($reporter_role) to user identifier($pbi_user);
commit;

-- 7.4 Streamlit User (REPORTER)
begin;
  create user if not exists identifier($streamlit_user)
    password = $streamlit_pwd
    default_role = $reporter_role
    default_warehouse = $reporting_wh;
    
  grant role identifier($reporter_role) to user identifier($streamlit_user);
commit;
