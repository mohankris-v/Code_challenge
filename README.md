## Setup instructions

This module is developed in Python version 3.9.1.
Install Python and the below required libraries:

```commandline
pyodbc
urllib
sqlalchemy
psycopg2
logging
```

## Database 
The module uses PostgreSql which an Open-source Relation Database Management System.


```commandline
Use the below link for download. 
https://www.postgresql.org/download/

Installation instructions
https://www.postgresql.org/docs/12/tutorial-install.html
```

## Environment variables
Create the environment variables with the following names:

```commandline
## The variables prefixed with db_ are database environment variables which is used for the connection.
## These variables has to initialized according to your database setup.
db_database
db_username
db_pwd
db_host
db_port

## Logfilename holds the path & name of the log file is stored. This variable has to be set.
Logfilename
```

## Program execution
Copy the Python file BTC_Price_Vol.py to the python environment and run the file. The table ```BTC_Price_variation holding``` BTC price variation data and the table ```BTC_Price_variation_agg``` holding the daily price volatility metric will be created in the database.




