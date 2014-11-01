# -*- coding: utf-8 -*-
import json

from flask import Response

from functools import wraps

from jungler.ext import db


def json_response(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        data = f(*args, **kwargs)
        status = 0

        if data is None:
            data = {}

        elif isinstance(data, tuple):
            status = data[1]
            data = data[0]

        if isinstance(data, Response):
            return data

        elif isinstance(data, list):
            if len(data) and isinstance(data[0], db.Model):
                data = {'data': [elem.serialize() for elem in data]}
            else:
                data = {'data': data}

        elif isinstance(data, db.Model):
            data = data.serialize()
        return Response(json.dumps(data), mimetype='application/json',
                        status=status or 200)
    return decorator