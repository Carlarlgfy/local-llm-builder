"""LM Studio's native local model inventory and lifecycle API."""
import json
import urllib.error
import urllib.request

BASE = 'http://127.0.0.1:1234/api/v1/models'

def request(action='', payload=None):
    req=urllib.request.Request(BASE+action, data=None if payload is None else json.dumps(payload).encode(), headers={'Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(req,timeout=300 if payload is not None else 5) as response:
            result=json.load(response)
        if not isinstance(result,dict) or result.get('error'):
            raise RuntimeError('LM Studio rejected the model request: '+str(result)[:500])
        return result
    except urllib.error.HTTPError as error:
        detail=error.read(1000).decode(errors='replace');error.close()
        if error.code in (401,403): raise RuntimeError('LM Studio requires authentication. Check its local server settings.') from error
        if error.code==404: raise RuntimeError('Model management requires an LM Studio version with the native v1 API.') from error
        raise RuntimeError('LM Studio could not complete the request: '+detail) from error
    except (TimeoutError,urllib.error.URLError) as error:
        if payload is not None:
            raise RuntimeError('LM Studio did not confirm the operation. Refresh to check its actual state before retrying.') from error
        raise RuntimeError('Cannot reach LM Studio. Start its local server on port 1234.') from error

def catalog():
    result=request()
    if not isinstance(result.get('models'),list): raise RuntimeError('LM Studio returned an unsupported model inventory.')
    return result['models']

def change(action, identifier, context_length=None):
    if action not in ('load','unload') or not isinstance(identifier,str) or not identifier.strip():
        raise ValueError('Choose a model to load or unload')
    models=catalog()
    if action=='load':
        model=next((m for m in models if m['key']==identifier),None)
        if model is None: raise ValueError('This model is no longer installed. Refresh the list.')
        if model.get('loaded_instances'):
            return {'message':'Already loaded', 'instance_id':model['loaded_instances'][0]['id']}
        payload={'model':identifier,'echo_load_config':True}
        if context_length is not None:
            if type(context_length) is not int or not 512<=context_length<=model.get('max_context_length',0):
                raise ValueError('Choose a context size within this model’s supported range')
            payload['context_length']=context_length
        return dict(request('/load',payload),message='Model loaded')
    if not any(i['id']==identifier for m in models for i in m.get('loaded_instances',[])):
        raise ValueError('This model instance is no longer loaded. Refresh the list.')
    return dict(request('/unload',{'instance_id':identifier}),message='Model unloaded')
