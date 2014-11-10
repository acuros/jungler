#-*- coding: utf-8 -*-
from celery.schedules import crontab
from celery.task import periodic_task

from jungler.app import create_app
from jungler.config import DeployConfig
from jungler.ext import db, celery
from jungler.bots import NaverBot
from jungler.models import Feed, Keyword, FeedKeywords


@celery.task(name='feeds_of_keyword_crawl')
def feeds_of_keyword_crawl(keyword_id):
    app = create_app(DeployConfig())
    with app.app_context():
        keyword = Keyword.query.filter(Keyword.id == keyword_id).first()
        if not keyword:
            return
        bot = NaverBot()
        bot.crawl(keyword=keyword)


@celery.task(name='remove_not_used_feeds')
def remove_not_used_feeds():
    app = create_app(DeployConfig())
    with app.app_context():
        for feed in Feed.query.all():
            row_count = FeedKeywords.query.with_entities(FeedKeywords.id).filter(FeedKeywords.feed_id == feed.id).count()
            if row_count == 0:
                feed.delete(commit=False)
        db.session.commit()


@periodic_task(run_every=crontab(minute='*/5'))
def all_feeds_of_keyword_crawl():
    app = create_app(DeployConfig())
    with app.app_context():
        keywords = Keyword.query.all()
        bot = NaverBot()
        for keyword in keywords:
            bot.crawl(keyword=keyword)
        remove_not_used_feeds.delay()
