from gremlin_python.driver import client, serializer

GREMLIN_ENDPOINT = 'wss://<YOUR_ENDPOINT>.gremlin.cosmosdb.azure.com:443/'
gremlin_client = client.Client(GREMLIN_ENDPOINT, 'g',
    username="/dbs/<YOUR_DATABASE>/colls/<YOUR_COLLECTION_OR_GRAPH>",
    password="<YOUR_PASSWORD>",
    message_serializer=serializer.GraphSONSerializersV2d0()
)

gremlin_insert_vertices = [
    "g.addV('person').property('id', 'thomas').property('firstName', 'Thomas').property('age', 44).property('pk', 'pk')",
    "g.addV('person').property('id', 'mary').property('firstName', 'Mary').property('lastName', 'Andersen').property('age', 39).property('pk', 'pk')"
]
for query in gremlin_insert_vertices:
    callback = gremlin_client.submitAsync(query)
    if callback.result() is not None:
        print("\tInserted this vertex:\n\t{0}".format(callback.result().all().result()))