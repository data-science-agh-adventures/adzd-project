from cassandra.cluster import Cluster, Session, PlainTextAuthProvider
from ssl import PROTOCOL_TLSv1_2, SSLContext, CERT_NONE
import os


KEYSPACE_NAME = 'CassandraDemo'
TABLE_NAME = 'CosmosCassandraDemoTable'
ENDPOINT = os.environ['COSMOS_CASSANDRA_ENDPOINT']
PORT = os.environ['COSMOS_CASSANDRA_PORT']
USERNAME = os.environ['COSMOS_CASSANDRA_USERNAME']
PASSWORD = os.environ['COSMOS_CASSANDRA_PASSWORD']

auth_provider = PlainTextAuthProvider(username=USERNAME, password=PASSWORD)
ssl_context = SSLContext(PROTOCOL_TLSv1_2)
ssl_context.verify_mode = CERT_NONE
session: Session = Cluster([ENDPOINT], port=PORT, auth_provider=auth_provider, ssl_context=ssl_context).connect()
session.execute(f'INSERT INTO {KEYSPACE_NAME}.{TABLE_NAME} (user_id, user_name , user_bcity) VALUES ({1},{"Lybkov"},{"Seattle"})')