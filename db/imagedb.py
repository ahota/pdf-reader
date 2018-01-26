import redis

class ImageDB:
    def __init__(self):
        self._db = redis.StrictRedis()

    def add(self, key, value):
        if key in self._db.keys():
            # don't want to overwrite keys
            print 'existing key', key
            print 'not doing anything'
        else:
            self._db.set(key, value)

    def get(self, key):
        return self._db.get(key)
