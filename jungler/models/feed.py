#-*- coding: utf-8 -*-
from jungler.ext import db
from jungler.models import Keyword
from jungler.models.mixins import IdMixin, CRUDMixin, TimestampMixin, SerializerMixin


class Feed(db.Model, IdMixin, CRUDMixin, TimestampMixin, SerializerMixin):
    __tablename__ = 'feeds'

    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(255))
    url = db.Column(db.String(255), nullable=False, index=True)
    write_time = db.Column(db.DateTime, nullable=False)

    keywords = db.relationship(Keyword.__name__, secondary='feed_keywords', backref='feeds')

    fields = ('id', 'title', 'content', 'summary', 'url', 'write_time', 'keywords', 'created_at', 'updated_at')

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


class FeedKeywords(db.Model, IdMixin, CRUDMixin, SerializerMixin):
    __tablename__ = 'feed_keywords'

    feed_id = db.Column(db.Integer,
                        db.ForeignKey('%s.id' % Feed.__tablename__, ondelete='CASCADE'),
                        nullable=False)
    feed = db.relationship(Feed, cascade='all')

    keyword_id = db.Column(db.Integer,
                           db.ForeignKey('%s.id' % Keyword.__tablename__, ondelete='CASCADE'),
                           nullable=False)
    keyword = db.relationship(Keyword, cascade='all')