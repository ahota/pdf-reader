from server import app
from db import ImageDB

import json
import socket

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
        },
        # the following are for the paper
        'ba30f594754a4b95' : {
            'author' : 'Alok Hota',
            'organization' : 'University of Tennessee',
            'email' : 'ahota@vols.utk.edu',
            'machine' : socket.getfqdn(),
            'filename' : '/data/heptane.raw',
            'dimensions' : [302, 302, 302],
            'dataVariable' : 'csafe_heptane_gas',
            'colorMap' : 'viridis',
            'isosurfaceValues' : [64],
            'cameraPosition' : [75, -200, 200]
        },
        'a4e2e960e51d81dd' : {
            'author' : 'Alok Hota',
            'organization' : 'University of Tennessee',
            'email' : 'ahota@vols.utk.edu',
            'machine' : socket.getfqdn(),
            'filename' : '/data/magnetic.raw',
            'dimensions' : [512, 512, 512],
            'dataVariable' : 'magnetic_reconnection',
            'colorMap' : 'coolToWarm',
            'isosurfaceValues' : [0.2],
            'cameraPosition' : [128, -256, 512]
        },
        '6cf01069b23cda94' : {
            'author' : 'Alok Hota',
            'organization' : 'University of Tennessee',
            'email' : 'ahota@vols.utk.edu',
            'machine' : socket.getfqdn(),
            'filename' : '/data/interp8502.nc',
            'dimensions' : [280, 490, 490],
            'dataVariable' : 'wind_velocity_magnitude',
            'colorMap' : 'magma',
            'isosurfaceValues' : [0.12, 27.59, 55.06, 82.53, 110.0],
            'cameraPosition' : [-280, 200, 175]
        },
        '87683740eaba1ad4' : {
            'author' : 'Alok Hota',
            'organization' : 'University of Tennessee',
            'email' : 'ahota@vols.utk.edu',
            'machine' : socket.getfqdn(),
            'filename' : '/data/E_1354.dat',
            'dimensions' : [432, 432, 432],
            'dataVariable' : 'angular_velocity',
            'colorMap' : 'viridis',
            'isosurfaceValues' : [0.0565],
            'cameraPosition' : [0, 0, -324]
        }
}

if __name__ == '__main__':
    idb = ImageDB(debug=True)

    print 'adding keys to the db for testing'
    for dbkey, data in test_data.iteritems():
        idb.add(dbkey, json.dumps(data))

    app.config['IMAGE_DB'] = idb
    app.run(debug=True, host='0.0.0.0')
