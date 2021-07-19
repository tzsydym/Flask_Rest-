import abc
from util import Mongo, haversine
from datetime import datetime
class UserDAO(object):
    '''
    Abstract object for data access object
    '''

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        return

    @abc.abstractmethod
    def get(self, name):
        return

    @abc.abstractmethod
    def create(self, data):
        return

    @abc.abstractmethod
    def update(self, name, data):
        return

    @abc.abstractmethod
    def delete(self, name):
        return

    @abc.abstractmethod
    def get_all(self):
        return

    @abc.abstractmethod
    def get_nearby(self,range):
        return


class UserDAOMongo(UserDAO):
    '''
    Data access object
    Class that manages the users in MongoDBue
    Exclude _id which can't be jsonified directly
    '''

    def __init__(self):
        self.mongo = Mongo()

    def get(self, name):
        user = self.mongo.collection.find_one({'name': name},{'_id': False})
        return user

    def create(self, data):
        if self.get(data["name"]) is None:
            data["createdAt"] = datetime.now(). strftime("%Y-%m-%d %H:%M:%S.%f")
            result = self.mongo.collection.insert_one(data)
            return str(result.inserted_id)

    def update(self, name, data):
        result = self.mongo.collection.update_one({'name': name}, {"$set": data})
        return result.matched_count

    def delete(self, name):
        result = self.mongo.collection.delete_one({'name': name})
        return result.deleted_count

    def get_all(self):
        user_list = list(self.mongo.collection.find({}, {'_id': False}))
        return user_list

    def get_nearby(self,user_name,range):
        self_user = self.get(user_name)
        res = []
        if self_user is not None:
            user_list = list(self.mongo.collection.find({}, {'_id': False}))
            for user in user_list:
                if(user['name'] != user_name and haversine(user['address']['longitude'],user['address']['latitude'],
                                                       self_user['address']['longitude'],self_user['address']['latitude']) <= range):
                    res.appen(user)
            return res