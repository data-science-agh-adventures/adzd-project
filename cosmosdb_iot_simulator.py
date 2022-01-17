import time

from azure.cosmos import CosmosClient
import datetime
import argparse
from faker import Faker


fake = Faker()
WAIT_INTERVAL = 1  # seconds


def prepare_iot_data_item(device_id):
    result = {
        'deviceId': device_id,
        'dateTime': str(datetime.datetime.utcnow()),
        'coordinates': {
            'latitude': str(fake.latitude()),
            'longitude': str(fake.longitude())
        }
    }
    return result


def main(args):
    database_name = args.db_name
    container_name = args.container_name
    url = args.account_uri
    key = args.account_key
    simulation_minutes = args.duration
    simulator_id = args.program_id
    results_basedir = args.results_base_dir
    results_filename = f'{results_basedir}/iot-simulation-{simulator_id}-results.csv'
    results_file = open(results_filename, 'w')
    results_file.write('Iteration,DB Write Duration (s)\n')

    client = CosmosClient(url, credential=key)
    database = client.get_database_client(database_name)
    container = database.get_container_client(container_name)
    device_id = fake.isbn13()

    n_iter = simulation_minutes * 60 // WAIT_INTERVAL
    for i in range(n_iter):
        new_data_item = prepare_iot_data_item(device_id=device_id)
        start = time.time()
        container.upsert_item(new_data_item)
        end = time.time()
        results_file.write(f'{i},{end - start}\n')
        i += 1
        time.sleep(WAIT_INTERVAL)
    
    results_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', dest='program_id', required=True, help='ID of the IoT simulator program')
    parser.add_argument('--uri', dest='account_uri', required=True, help='URI of the Cosmos DB account')
    parser.add_argument('--key', dest='account_key', required=True, help='Cosmos DB account access key')
    parser.add_argument('--db', dest='db_name', required=True, help='Name of the database')
    parser.add_argument('--cont', dest='container_name', required=True, help='Name of the container in the DB')
    parser.add_argument('--basedir', dest='results_base_dir', required=True, help='Base directory path for results file')
    parser.add_argument('--duration', dest='duration', required=True, help='Simulation duration in minutes', type=int)
    args = parser.parse_args()

    main(args)
