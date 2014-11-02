#-*- coding: utf-8 -*-
from celery.schedules import crontab
from celery.task import periodic_task

from jungler.ext import celery
from jungler.bots import NaverBot
from jungler.models.keyword import Keyword


@celery.task
def feeds_of_keyword_crawl(keyword):
    bot = NaverBot()
    bot.crawl(keyword=keyword)


@periodic_task(run_every=crontab())
def all_feeds_of_keyword_crawl():
    keywords = Keyword.query().all()
    bot = NaverBot()
    for keyword in keywords:
        bot.crawl(keyword=keyword)