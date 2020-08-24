from flask import request, abort
from flask_injector import FlaskInjector
from injector import Injector
from dependencies import configure
from facekeeper import FaceKeeper, FaceNotFoundError
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
        try:
            result = srv.memorize(person, content)
            response[file.filename] = {
                'length': len(content),
                'digest': result.digest,
            }
        except FaceNotFoundError:
            response[file.filename] = {
                'error': 'FACE_NOT_FOUND',
            }

    return response


def recognize(srv: FaceKeeper):
    content = request.files['file'].read()

    try:
        result = srv.recognize(content)
        if result:
            return {'person': result.person}
    except FaceNotFoundError:
        return {
            'error': 'FACE_NOT_FOUND',
        }

    return {
        'error': 'PERSON_NOT_RECOGNIZED',
    }

def dapr_recognize(srv: FaceKeeper, dapr: Dapr):
    payload = json.loads(request.data)

    try:
        urls = payload['data']['images']
    except TypeError:
        print('Wrong event received: ' + str(request.data), flush=True)
        return {'success': True}
    except KeyError:
        print('Wrong event received: ' + str(request.data), flush=True)
        return {'success': True}

    if len(urls) == 0:
        print('Empty images set received', flush=True)
        return {'success': True}

    result = {}
    for url in urls:
        response = requests.get(url)
        recognition = srv.recognize(response.content)
        if recognition:
            result[url] = {
                'person': recognition.person
            }

    if result:
        payload['data']['recognition'] = result
        print('Payload:' + json.dumps(payload['data']))
        ok = dapr.publish_recognized(json.dumps(payload['data']))
        if ok:
            print('Recognized message pubslihed successfully', flush=True)
        else:
            print('Results not published', flush=True)
    else:
        print('No persons recognized')

    return {'success': True}


def dapr_subscribe(dapr: Dapr):
    return dapr.get_subscriptions()


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
