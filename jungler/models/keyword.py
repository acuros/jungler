#-*- coding: utf-8 -*-
from jungler.ext import db
from jungler.models.mixins import IdMixin, CRUDMixin, SerializerMixin, TimestampMixin


class Keyword(db.Model, IdMixin, CRUDMixin, TimestampMixin, SerializerMixin):
    __tablename__ = 'keywords'

    name = db.Column(db.String(100), nullable=False, index=True, unique=True)
    fields = ('id', 'name', 'created_at', 'updated_at')

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '<Keyword: %s>' % self.name.encode('utf-8')

    def __setattr__(self, key, value):
        return super(Keyword, self).__setattr__(key, value)