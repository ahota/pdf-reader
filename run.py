from server import app
from db import ImageDB

import json

# data for various_5_5.pdf
test_data = {
        'd70a8ff17f100c65' : {
            'filename' : '/data/magnetic.raw',
            'dimensions' : [512, 512, 512],
            'isosurfaceValues' : [0.2],
            'colorMap' : 'coolToWarm',
            'cameraPosition' : [128, 256, 512]
        },
        '4090332927509071' : {
            'filename' : '/data/magnetic.raw',
            'dimensions' : [512, 512, 512],
            'isosurfaceValues' : [0.2],
            'colorMap' : 'coolToWarm',
            'cameraPosition' : [32, 64, 128]
        },
        '319c29c3691cdcb7' : {
            'filename' : '/data/E_1350.dat',
            'dimensions' : [432, 432, 432],
            'isosurfaceValues' : [0.0565],
            'colorMap' : 'viridis',
            'cameraPosition' : [0, 0, -324]
        },
        '0b17640461d44454' : {
            'filename' : '/data/E_1350.dat',
            'dimensions' : [432, 432, 432],
            'isosurfaceValues' : [0.0565],
            'colorMap' : 'viridis',
            'cameraPosition' : [-432, 0, 0]
        },
        '949f2252b142104c' : {
            'filename' : '/data/interp8502.nc',
            'dimensions' : [280, 490, 490],
            'dataVariable' : 'wind_velocity_magnitude',
            'colorMap' : 'magma',
            'opacityMap' : 'exponential',
            'isosurfaceValues' : [0.12, 27.59, 55.06, 82.53, 110.0],
            'cameraPosition' : [-280, 200, 175]
        }
}

if __name__ == '__main__':
    idb = ImageDB(debug=True)

    print 'adding keys to the db for testing'
    for dbkey, data in test_data.iteritems():
        idb.add(dbkey, json.dumps(data))

    app.config['IMAGE_DB'] = idb
    app.run(debug=True, host='0.0.0.0')
