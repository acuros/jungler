#-*- coding: utf-8 -*-
from models.mixins import SerializerMixin


class Feed(SerializerMixin):

    title = None
    content = None
    summary = None
    url = None
    created_time = None

    fields = ('title', 'content', 'summary', 'date', 'author')

    def __init__(self, title, content, summary, url, created_time):
        self.title = title
        self.content = content
        self.summary = summary
        self.url = url
        self.created_time = created_time

    def __str__(self):
        return '<News: %s>' % self.title.encode('utf-8')
