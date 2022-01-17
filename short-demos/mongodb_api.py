import pymongo
import os

CONNECTION_STRING = os.environ['MONGO_COSMOS_CONNECTION_STRING']
client = pymongo.MongoClient(CONNECTION_STRING)
db = client['test-database']
collection = db.test_collection
document_id = collection.insert_one({
    'productName': 'Widget',
    'productModel': 'Model Test'
    }).inserted_id