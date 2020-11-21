## Extract-Transform-Load Framework
Weaknesses:

1. Some tables do not have `updated_at` column
- This will be a problem when we want to upsert new rows in our datalake. Consider the case when a record  created in `01-Jan-2010 10am`, and updated at `01-Jan-2010 11am`. If we will be ingesting records on `01-Jan-2010`, we will not be able to identify which is the most updated version of the record. The solution is to add an additional column containing updated timestamp. 

2. Multiple schema in one database
- If a schema has problems, then other schemas might be affected
- We will be reading everything from the same database. Too many reading processes running concurrently might overwhelm the database.
- Split to multiple databases if necessary.


3. Scalability 
- What happens when there is sudden increase of incoming data? Will resources be automatically scaled up to handle the workload?
- We could use a cloud solution with autoscaling capabilities. 

Stages of data processing:
1. At time `t`, the python script will ingest data that is produced at time `t-1` from the relational database. Example: if it is a daily ingestion, then on `02-Jan-2010`, the python script will ingest data updated at `01-Jan-2010`.

2. Append the newly ingested data to a raw table in the data lake. 

3. Deduplicate the records by primary key, i.e. if two records have the same primary key, take the record with the latest updated date

4. Remove deleted records

The entire process above is coordinated by a scheduler (example Airflow). 

