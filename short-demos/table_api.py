import os
from azure.cosmosdb.table.tableservice import TableService

CONNECTION_STRING = os.environ['COSMOS_TABLE_API_CONNECTION_STRING']
table_service = TableService(endpoint_suffix="table.cosmos.azure.com", \
    connection_string=CONNECTION_STRING)
table_service.create_table('tasktable')
task = {
    'PartitionKey': 'tasksSeattle',  # required to set
    'RowKey': '001',  # required to set
    'description': 'Take out the trash',
    'priority': 200
    }
table_service.insert_entity('tasktable', task)