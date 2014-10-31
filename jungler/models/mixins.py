#-*- coding:utf-8 -*-
from flask import abort

from datetime import datetime

from jungler.ext import db


class IdMixin(object):
    """
    Provides the :attr:`id` primary key column
    """
    #: Database identity for this model, used for foreign key
    #: references from other models
    id = db.Column(db.Integer, primary_key=True)


class TimestampMixin(object):
    """
    Provides the :attr:`created_at` and :attr:`updated_at` audit timestamps
    """
    #: Timestamp for when this instance was created, in UTC
    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)
    #: Timestamp for when this instance was last updated (via the app), in UTC
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class CRUDMixin(object):
    __table_args__ = {'extend_existing': True}

    @classmethod
    def query(cls):
        return db.session.query(cls)

    @classmethod
    def get(cls, _id):
        if any((isinstance(_id, basestring) and _id.isdigit(),
                isinstance(_id, (int, float))),):
            return cls.query.get(int(_id))
        return None

    @classmethod
    def get_by(cls, **kwargs):
        return cls.query.filter_by(**kwargs).first()

    @classmethod
    def get_or_404(cls, _id):
        rv = cls.get(_id)
        if rv is None:
            abort(404)
        return rv

    @classmethod
    def get_or_create(cls, **kwargs):
        r = cls.get_by(**kwargs)
        if not r:
            r = cls(**kwargs)
            db.session.add(r)
        return r

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        for attr, value in kwargs.iteritems():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
        return self

    def delete(self, commit=True):
        db.session.delete(self)
        return commit and db.session.commit()


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