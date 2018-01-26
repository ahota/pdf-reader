from server import app
from db import ImageDB

if __name__ == '__main__':
    idb = ImageDB()

    print 'adding a key to the db for testing'
    idb.add('272c2e03f868fcff960a30ab8f2c1afa', 'magnetic data')

    app.config['IMAGE_DB'] = idb
    app.run(debug=True, host='0.0.0.0')
