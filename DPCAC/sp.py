import os.path as osp
import json
import nni


class SimpleParam:
    def __init__(self,local_dir:str='param',default:dict=None):
        if not default:
            default = dict()
        self.local_dir = local_dir
        self.default = default

    def __call__(self,source:str,preprocess:str='none'):
        if source == 'nni':
            return {**self.default, **nni.get_next_parameter()}
        if source.startswith('local'):
            ts = source.split(':')
            assert len(ts) == 2, 'local parameter file should be specified in a form of `local:FILE_NAME`'
            path = ts[-1]
            path = osp.join(self.local_dir, path)
            if path.endswith('.json'):
                loaded = parse_json(path)
            else:
                raise Exception('Invalid file name. Should end with .yaml or .json.')
            if preprocess == 'nni':
                loaded = preprocess_nni(loaded)
            return {**self.default, **loaded}
        if source == 'default':
            return self.default

        assert False, 'Invalid source!'

def preprocess_nni(params:dict):
    def process_key(key:str):
        xs = key.split('/')
        if len(xs) == 3:
            return xs[1]
        elif len(xs) == 1:
            return key
        else:
            raise Exception('Unexpected param name '+key)

    return {process_key(k): v for k, v in params.items()}

def parse_json(path:str):
    content = open(path).read()
    return json.loads(content)



class SimpleParam1:
    def __init__(self,local_dir:str='../param',default:dict=None):
        if not default:
            default = dict()
        self.local_dir = local_dir
        self.default = default

    def __call__(self,source:str,preprocess:str='none'):
        if source == 'nni':
            return {**self.default, **nni.get_next_parameter()}
        if source.startswith('local'):
            ts = source.split(':')
            assert len(ts) == 2, 'local parameter file should be specified in a form of `local:FILE_NAME`'
            path = ts[-1]
            path = osp.join(self.local_dir, path)
            if path.endswith('.json'):
                loaded = parse_json(path)
            else:
                raise Exception('Invalid file name. Should end with .yaml or .json.')
            if preprocess == 'nni':
                loaded = preprocess_nni(loaded)
            return {**self.default, **loaded}
        if source == 'default':
            return self.default

        assert False, 'Invalid source!'