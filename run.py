from server import app
from db import ImageDB

if __name__ == '__main__':
    idb = ImageDB()

    print 'adding a key to the db for testing'
    idb.add('61713668bb7f0faa161a63f7c8fdfa7c', 'supernova data')

    app.config['IMAGE_DB'] = idb
    app.run(debug=True, host='0.0.0.0')
