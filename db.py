import pymongo

DATABASE = 'trains'
CONN = ''
mongo_instance: pymongo.MongoClient = None


def init(conn: str):
    global mongo_instance
    if not mongo_instance:
        mongo_instance = get_database(conn)


def get_database(conn: str):
    client = pymongo.MongoClient(conn)
    return client[DATABASE]


def get_collection(name: str) -> pymongo.collection.Collection:
    return mongo_instance[name]


def replace_many(
        collection: pymongo.collection.Collection,
        documents,
        filter_getter=lambda x: {'_id': x['_id']}):
    for d in documents:
        collection.replace_one(filter_getter(d), d, upsert=True)

if __name__ == '__main__':
    dbname = get_database('mongodb://user:password@localhost:27017')
    collection_name = dbname['trains']
    train1 = {
        "number": 2832,
        "from": "1",
        "to": "2"
    }
    collection_name.insert_one(train1)
