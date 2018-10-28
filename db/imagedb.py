import redis

class ImageDB:
    def __init__(self, debug=False):
        self._db = redis.StrictRedis()
        self._debug = debug

    def add(self, key, value):
        if key in self._db.keys():
            if not self._debug:
                # don't want to overwrite keys
                return
        try:
            self._db.set(key, value)
        except redis.exceptions.ResponseError as error:
            import sys
            print 'ERROR:', error
            print 'Try shutting down redis with redis-cli shutdown'
            print 'If that does not work, ps aux | grep redis, and sudo kill it'
            sys.exit(1)

    def get(self, key):
        return self._db.get(key)
