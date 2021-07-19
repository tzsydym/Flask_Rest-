import pymongo
from math import radians, cos, sin, asin, sqrt

class Mongo(object):
    def __init__(self):
        self.CONNECTION_STRING = "mongodb+srv://DUYIMING:duyiming@cluster0.0nryf.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
        self.DB_NAME = "Ryde_Test"
        self.COLLECTION_NAME = "C0"
        self.client = pymongo.MongoClient(self.CONNECTION_STRING)
        self.db = self.client[self.DB_NAME]
        self.collection = self.db[self.COLLECTION_NAME]

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert digits into radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine equation
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # radius of earth, in kilometer
    return c * r * 1000

