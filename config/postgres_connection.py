import psycopg2
import configparser
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sys

config = configparser.ConfigParser()
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'ConfigFile.properties')
print(CONFIG_PATH)
config.read(CONFIG_PATH)

for each_section in config.sections():
    for (each_key, each_val) in config.items(each_section):
        print(each_key)
        print(each_val)

postgresProps = config['postgres']
username = postgresProps["postgres_username"]
password = postgresProps["postgres_password"]
hostname = postgresProps["postgres_host_name"]
port = postgresProps["postgres_port"]
database = postgresProps["postgres_database"]

connection = psycopg2.connect(user = username,
                                  password = password,
                                  host = hostname,
                                  port = port,
                                  database = database,
                                  )
cursor = connection.cursor()

print(connection.get_dsn_parameters(),"\n")

cursor = connection.cursor()

db_string = "postgres://" + username + ":" + password + "@" + hostname + ":" + port + "/" + database
db = create_engine(db_string)
base = declarative_base()

Session = sessionmaker(db)
session = Session()
