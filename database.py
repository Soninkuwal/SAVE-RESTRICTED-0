    import pymongo
    from bot.config import MONGODB_URL
    from bson.objectid import ObjectId

    class Database:
        def __init__(self):
            self._client = pymongo.MongoClient(MONGODB_URL)
            self.db = self._client.bot_db
            self.links_collection = self.db.links
            self.users_collection = self.db.users

        def add_link(self, link_type, link):
            return self.links_collection.insert_one({"type": link_type, "link": link}).inserted_id

        def get_links_by_type(self, link_type):
            return list(self.links_collection.find({"type": link_type}))

        def delete_link(self, id):
            self.links_collection.delete_one({'_id': ObjectId(id)})
            return True

        def link_exists(self, link):
            return bool(self.links_collection.find_one({"link": link}))

        def save_user(self, user_id, user_name, first_name, last_name):
            return self.users_collection.update_one(
                {"user_id": user_id},
                {"$set": {"user_id": user_id, "user_name": user_name, "first_name": first_name, "last_name": last_name}},
                upsert=True,
            )

        def get_all_users(self):
            return list(self.users_collection.find())

        def get_user(self, user_id):
            return self.users_collection.find_one({"user_id": user_id})

        def is_user_exist(self, user_id):
            return self.users_collection.find_one({"user_id": user_id}) is not None

        def update_user_status(self, user_id, status):
            return self.users_collection.update_one({"user_id": user_id}, {"$set": {"status": status}})

        def get_user_status(self, user_id):
            user = self.users_collection.find_one({"user_id": user_id})
            if user:
                return user.get('status', None)
            return None

        def update_user_settings(self,user_id,settings):
             return self.users_collection.update_one({"user_id": user_id}, {"$set": {"settings": settings}},upsert=True)

        def get_user_settings(self,user_id):
           user =  self.users_collection.find_one({"user_id": user_id})
           if user:
               return user.get('settings',None)
           return None
        def close(self):
            self._client.close()
