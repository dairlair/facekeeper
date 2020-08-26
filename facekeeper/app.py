from flask import request, abort
from flask_injector import FlaskInjector
from injector import Injector
from dependencies import configure
from facekeeper import FaceKeeper
from http import HTTPStatus
from waitress import serve
from config import Config
from dapr import Dapr
import requests
import json
import connexion
import threading


def healthz():
    return HTTPStatus.OK.phrase


def readyz(srv: FaceKeeper):
    if not srv.is_initialized():
        abort(HTTPStatus.SERVICE_UNAVAILABLE)

    return HTTPStatus.OK.phrase


def memorize(srv: FaceKeeper):
    person = request.form['person']
    response = {}
    for file in request.files.getlist('files'):
        content = file.read()
        if result := srv.memorize(person, content):
            response[file.filename] = {
                'length': len(content),
                'digest': result.digest,
            }
        else:
            response[file.filename] = {
                'error': 'FACE_NOT_FOUND',
            }

    return response


def recognize(srv: FaceKeeper):
    content = request.files['file'].read()
    if result := srv.recognize(content):
        return {'person': result.person}

    return {
        'error': 'FACE_NOT_FOUND',
    }

def dapr_memorize(srv: FaceKeeper, dapr: Dapr):
    data = dapr.get_data(request)
    try:
        result = {}
        person = data['person']
        urls = data['images']
        for url in urls:
            response = requests.get(url)
            memorization = srv.memorize(person, response.content)

            if memorization:
                result['url'] = {'digest': memorization.digest, 'length': len(response.content)}

    except TypeError:
        print('Wrong event received: ' + str(type(data)) + ': ' + str(data), flush=True)
        return {'success': True}
    except KeyError:
        print('Wrong event received: ' + str(type(data)) + ': ' + str(data), flush=True)
        return {'success': True}

    if result:
        data['memorizing'] = result
        dapr.publish('Memorized', json.dumps(data))    

    return {'success': True}

def dapr_recognize(srv: FaceKeeper, dapr: Dapr):
    data = dapr.get_data(request)
    try:
        urls = data['images']
    except TypeError:
        print('Wrong event received: ' + str(request.data), flush=True)
        return {'success': True}
    except KeyError:
        print('Wrong event received: ' + str(request.data), flush=True)
        return {'success': True}

    result = {}
    for url in urls:
        response = requests.get(url)
        if recognition := srv.recognize(response.content):
            result[url] = {
                'person': recognition.person
            }
        

    if result:
        data['recognition'] = result
        dapr.publish('Recognized', json.dumps(data))
    else:
        print('No faces found')

    return {'success': True}


def dapr_subscribe(dapr: Dapr):
    return [
        {'pubsubName': dapr.pubsub, 'topic': 'Memorize', 'route': 'dapr/memorize'},
        {'pubsubName': dapr.pubsub, 'topic': 'Recognize', 'route': 'dapr/recognize'},
    ]


injector = Injector()


def initialize(srv: FaceKeeper) -> None:
    srv.initialize()


if __name__ == "__main__":
    app = connexion.FlaskApp(
        __name__, port=Config.port(), specification_dir='../api/')
    app.add_api('facekeeper.yaml', validate_responses=True)

    FlaskInjector(app=app.app, modules=[configure], injector=injector)

    # Need this tricky call to eager initialization
    # https://github.com/alecthomas/injector/issues/44
    service = injector.get(FaceKeeper)
    thread = threading.Thread(target=initialize, args=[service])
    thread.start()

    # Use this for local app run
    # app.run(host=Config.host(), port=Config.port())

    serve(app, host=Config.host(), port=Config.port())
