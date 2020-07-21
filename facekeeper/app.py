from flask import request, abort
from flask_injector import FlaskInjector
from injector import Injector
from dependencies import configure
from facekeeper import FaceKeeper, FaceNotFoundError
from http import HTTPStatus
from waitress import serve
from config import Config
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


injector = Injector()


def initialize(srv: FaceKeeper) -> None:
    srv.initialize()


if __name__ == "__main__":
    app = connexion.FlaskApp(__name__, port=Config.port(), specification_dir='../api/')
    app.add_api('facekeeper.yaml', validate_responses=True)

    FlaskInjector(app=app.app, modules=[configure], injector=injector)

    # Need this tricky call to eager initialization
    # https://github.com/alecthomas/injector/issues/44
    service = injector.get(FaceKeeper)
    thread = threading.Thread(target=initialize, args=[service])
    thread.start()

    serve(app, host=Config.host(), port=Config.port())
