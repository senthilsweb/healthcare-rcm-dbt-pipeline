# healthcare-rcm-dbt-pipeline
End-to-end healthcare revenue cycle management analytics pipeline showcasing ETL, data modeling, lineage, governance, and business intelligence using dbt

## Getting Started

### Development Environment Setup

```
python3 -m venv env 
source env/bin/activate      
```

### Running the project locally

```  
docker compose -f docker-compose-pg.yml up -d

pip install -r reqirements.txt
dbt debug
dbt deps
dbt seed

# Run Default 
dbt run
dbt test
dbt docs genereate
dbt docs serve

# Run with elementary-date and send the results to elementary catalog (Preferred method)
dbt run --select elementary
dbt test  --select elementary 
edr report  --profiles-dir .
```

## Developer guide

### Generate Model Schema : run below command and copy the results in clipboard

```
dbt run-operation generate_source --args '{
   "schema_name": "raw",
    "generate_columns": true,
    "include_descriptions": true,
    "include_data_types": true,
    "case_sensitive_cols" : true
}'

# create  /models/staging/_sources.yml and paste the copied content

# Generate staging models for each table : run below command and copy the results in clipboard

dbt run-operation generate_base_model --args '{"source_name": "raw", "table_name": "activities", "case_sensitive_cols": true}' > models/staging/stg_activities.sql

dbt run-operation generate_base_model --args '{"source_name": "raw", "table_name": "claims", "case_sensitive_cols": true}' > models/staging/stg_claims.sql

dbt run-operation generate_base_model --args '{"source_name": "raw", "table_name": "collections", "case_sensitive_cols": true}' > models/staging/stg_collections.sql

dbt run-operation generate_base_model --args '{"source_name": "raw", "table_name": "encounters", "case_sensitive_cols": true}' > models/staging/stg_encounters.sql

dbt run-operation generate_base_model --args '{"source_name": "raw", "table_name": "facilities", "case_sensitive_cols": true}' > models/staging/stg_facilities.sql

dbt run-operation generate_base_model --args '{"source_name": "raw", "table_name": "users", "case_sensitive_cols": true}' > models/staging/stg_users.sql

dbt run-operation generate_base_model --args '{"source_name": "raw", "table_name": "health_plans", "case_sensitive_cols": true}' > models/staging/stg_health_plans.sql


# dbt run --select staging or dbt run --select stg_users

# Generate Model Schema for `intermediate` using manual manner as we need to denormalize and add additional attributes

# Run all intermediate models
dbt run --select intermediate
dbt run --select mart.core 
dbt run --select mart.admin   
dbt run --select mart.billing 
dbt run --select mart.clinical
```