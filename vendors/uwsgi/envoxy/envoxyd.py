import sys
import os
import json
import uwsgi
import inspect

import importlib.util

from flask import Flask

app = Flask(__name__)
app.debug = True

if 'mode' in uwsgi.opt and uwsgi.opt['mode'] == b'test':
    
    @app.route('/')
    def index():
        return "ENVOXY Working!"

elif 'conf' in uwsgi.opt:
    
    _conf_path = uwsgi.opt['conf'].decode('utf-8')
    
    print('>>> Configuration file param found: {}'.format(_conf_path))
    
    if os.path.exists(_conf_path):

        print('>>> Configuration file exists! Trying to parse the file...')

        # try:
        _conf_file = open(_conf_path, encoding='utf-8')
        _conf_content = json.loads(_conf_file.read(), encoding='utf-8')
        print('>>> The configuration file was parsed successfully!')

        _modules_list = _conf_content.get('modules')

        for _module_path in _modules_list:

            print('>>> Module path: {}'.format(_module_path))
    
            #try:
    
            _spec = importlib.util.spec_from_file_location('__init__', _module_path)
            _module = importlib.util.module_from_spec(_spec)
            _spec.loader.exec_module(_module)

            for _name, _obj in inspect.getmembers(_module):
                
                if _name == '__loader__' and isinstance(_obj, list) and len(_obj)>0:
        
                    for _view_class in _obj:
                        _view_class(app)
                        print('>>> Loaded "{}".'.format(str(_view_class)))

                # except Exception as _ex:

                #     print("*** Exception when module class was called: {}".format(_ex))
                #     exit(-1)


        # except Exception as e:
        #     print('*** An error was thrown when ENVOXY tried to parse the file: {}\n\n'.format(e))
        #     exit(-1)

    else:

        print('*** Configuration file not found in this path! Please check if the file exists or the permissions are enough.\n\n')
        exit(-1)



else:
    print('*** Configuration file not found! Please use ./envoxy [params] --set conf=<file> or ./envoxy [params] --set mode=test\n\n')
    exit(-1)

print('\n\n')