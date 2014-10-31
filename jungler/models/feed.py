#-*- coding: utf-8 -*-
from jungler.ext import db
from jungler.models.mixins import IdMixin, CRUDMixin, SerializerMixin


class Feed(db.Model, IdMixin, CRUDMixin, SerializerMixin):
    __tablename__ = 'feeds'

    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(255))
    url = db.Column(db.String(255), nullable=False)
    write_time = db.Column(db.DateTime, nullable=False)

    fields = ('title', 'content', 'summary', 'url', 'write_time')

    def __init__(self, title, content, summary, url, write_time):
        self.title = title
        self.content = content
        self.summary = summary
        self.url = url
        self.write_time = write_time

    def __str__(self):
        return '<News: %s>' % self.title.encode('utf-8')

    def __setattr__(self, key, value):
        return super(Feed, self).__setattr__(key, value)