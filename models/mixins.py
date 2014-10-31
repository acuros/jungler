# -*- coding:utf-8 -*-
import datetime


class SerializerMixin(object):
    """
    Mixin class for models.

    Model define::

        class User(SerializerMixin):
            id = None
            name = None

            fields = ('id', 'name')

            def __init__(self, _id, name):
                self.id = _id
                self.name = name

    Model serialize::

        u = User(1, 'Loup')
        u.serialize()
    """

    fields = tuple()

    def serialize(self, fields=[]):
        result = dict()
        if not fields:
            try:
                fields = self.fields
            except AttributeError:
                return result
        for field in fields:
            if isinstance(field, dict):
                if 'key' in field and 'fields' in field:
                    value = getattr(self, field['key'])
                    result[field['key']] = dict()
                    for sub_field in field['fields']:
                        result[field['key']][sub_field] = getattr(value, sub_field)
            else:
                try:
                    value = getattr(self, field)
                except AttributeError:
                    continue
                result[field] = self.get_cleaned_value(field, value)
        try:
            f = getattr(self, 'get_external_data')
        except AttributeError:
            pass
        else:
            result.update(f())
        return result

    def get_cleaned_value(self, key, value):
        if isinstance(value, self.__class__):
            result = dict()
            try:
                fields = self.self_fields
            except AttributeError:
                return result
            return value.serialize(fields)
        elif isinstance(value, list):
            result = []
            for v in value:
                if isinstance(v, self.__class__):
                    try:
                        fields = self.self_fields
                    except AttributeError:
                        continue
                    result.append(v.serialize(fields))
                else:
                    result.append(v.serialize())
            return result
        elif SerializerMixin in value.__class__.__bases__:
            return value.serialize()
        elif isinstance(value, datetime.date):
            return value.strftime('%Y-%m-%d')
        elif isinstance(value, datetime.datetime):
            return value.strftime('%Y-%m-%d %H:%M')
        else:
            return value