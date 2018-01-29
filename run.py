from server import app
from db import ImageDB

import json

if __name__ == '__main__':
    idb = ImageDB(debug=True)

    print 'adding a couple keys to the db for testing'
    supernova_test_data = {
            'filename' : '/data/E_1354.dat'
    }
    idb.add('61713668bb7f0faa161a63f7c8fdfa7c', json.dumps(supernova_test_data))
    magnetic_test_data = {
            'filename' : '/data/magnetic.raw',
            'dimensions' : [512, 512, 512],
            'isosurfaceValue' : 4,
            'cameraPosition' : [128, 256, 512]
    }
    idb.add('23a528b58eb82effde23e2ab7f4b305a', json.dumps(magnetic_test_data))

    app.config['IMAGE_DB'] = idb
    app.run(debug=True, host='0.0.0.0')
