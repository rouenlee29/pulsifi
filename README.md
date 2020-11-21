## Extract-Transform-Load Framework
Weaknesses:

1. Some tables do not have `updated_at` column
- This will be a problem when we want to upsert new rows in our data lake. Consider the case when a record  created in 01-Jan-2010 10am, and updated at 01-Jan-2010 11am. If we will be ingesting records on 01-Jan-2010, we will not be able to identify which is the most updated version of the record. The solution is to add an additional column containing updated timestamp. 

2. Multiple schema in one database
- If a schema has problems, then other schemas might be affected.
- We will be reading everything from the same database. Too many reading processes running concurrently might overwhelm the database.
- Split to multiple databases if necessary.


3. Scalability 
- What happens when there is sudden increase of incoming data? Will resources be automatically scaled up to handle the workload?
- We could use a cloud solution with autoscaling capabilities. 

Stages of data processing:
1. At time t, the python script will ingest data that is produced at time t-1 from the relational database. Example: if it is a daily ingestion, then on 02-Jan-2010, the python script will ingest data updated at 01-Jan-2010.
- To access a relational database like PostgreSQL with python, we can use a package like `Psycopg2`

2. Append the newly ingested data to a raw table in the data lake (example, Amazon s3, HDFS, Google Cloud storage). 

3. Deduplicate the records by primary key, i.e. if two records have the same primary key, take the record with the latest updated date.

4. Remove deleted records.

The entire process above is coordinated by a scheduler (example Airflow). 

## SQL
Using `postgresql 9.6`.

```sql
CREATE TABLE IF NOT EXISTS profile (
  profile_id INT NOT NULL,
  name TEXT NOT NULL,
  gender TEXT NOT NULL,
  PRIMARY KEY (profile_id)
) ;
INSERT INTO profile (profile_id, name, gender) VALUES
  ('11', 'Alex', 'Male'),
  ('22', 'Beth', 'Female'),
  ('33', 'Chad', 'Male');
  
CREATE TABLE IF NOT EXISTS action (
  action_id INT NOT NULL,
  action_type TEXT NOT NULL,
  PRIMARY KEY (action_id)
) ;
INSERT INTO action (action_id, action_type) VALUES
  ('1', 'Login'),
  ('2', 'Logout'),
  ('3', 'Start Assessment'),
  ('4', 'Finish Assessment');
  
CREATE TABLE IF NOT EXISTS profile_action (
  profile_action_id INT  NOT NULL,
  profile_id INT  NOT NULL,
  action_id INT  NOT NULL,
  created_at TIMESTAMP NOT NULL
);
INSERT INTO profile_action (profile_action_id, profile_id, action_id, created_at) VALUES
  ('1', '11', '1', '2020-01-01 01:00:00'),
  ('2', '22', '3', '2020-01-01 02:00:00'),
  ('3', '11', '3', '2020-01-01 03:00:00'),
  ('4', '22', '2', '2020-01-01 04:00:00'),
  ('5', '22', '1', '2020-01-01 05:00:00'),
  ('6', '11', '4', '2020-01-01 06:00:00'),
  ('7', '11', '2', '2020-01-01 07:00:00'),
  ('8', '22', '2', '2020-01-01 08:00:00');

WITH temp AS (
SELECT
  *
FROM 
  (
  SELECT
      profile.name AS name,
      profile.gender AS gender,
      action.action_type AS action,
      profile_action.created_at AS action_time,
      ROW_NUMBER() OVER(PARTITION BY profile_action.profile_id ORDER BY profile_action.created_at DESC) AS row_num
  FROM profile_action 
  FULL OUTER JOIN profile 
  ON profile_action.profile_id = profile.profile_id
  LEFT JOIN action 
  ON profile_action.action_id = action.action_id
   ) joined
WHERE row_num <= 2
)

SELECT 
  first.name,
  first.gender,
  first.action AS last_action,
  first.action_time AS last_action_time,
  second.action AS "2nd_last_action",
  second.action_time AS "2nd_last_action_time"
FROM (SELECT * FROM temp WHERE row_num = 1) first
FULL OUTER JOIN (SELECT * FROM temp WHERE row_num = 2) second
ON first.name = second.name
```
## Basic Programming 

Please refer to `src/programming.py`, and `src/tests.py` for the unit tests.

## Data Modeling 
Below are the table and their columns:

Person job (fact table)
- profile_id (string, primary key)
- job_id (string, primary key)
- organization_id (string, primary key)
- started_at (date)
- ended_at (date)
- current_job (boolean)

Index key for the fact table depends on the query pattern. For example, if the fact table is used mostly by headhunters / recruiters, it might be helpful to index the table by year of `started_at` and `current_job`, to identify those who have spent a long time at their current job and more likely to be ready for a new job. 

Person (dimension table) 
- profile_id (string, primary key, links to profile_id in fact table)
- first_name (string)
- last_name (string)
- first letter of last name (string, index key)
- mobile (string)
- email (string)

Job (dimension table)
- job_id (string, primary key, links to job_id in fact table)
- job_title (string)

Organization (dimension table)
- organization_id (string, primary key, links to organization_id in fact table)
- organization_name (string)

Social media (dimension table)
- profile_id (string, primary key, links to profile_id in fact table)
- media (string, primary key and index key)
- account_name (string, primary key)
- active_since (date)

## Data Transformation
Please refer to `src/html_generator.py`

