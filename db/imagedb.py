import redis

class ImageDB:
    def __init__(self, debug=False):
        self._db = redis.StrictRedis()
        self._debug = debug

    def add(self, key, value):
        if key in self._db.keys():
            if not self._debug:
                # don't want to overwrite keys
                print 'existing key', key
                print 'not doing anything'
                return
        self._db.set(key, value)

    def get(self, key):
        return self._db.get(key)
