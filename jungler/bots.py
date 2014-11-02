#-*- coding: utf-8 -*-
import re
import urllib
import feedparser

from datetime import datetime

from readability.readability import Document

from jungler.ext import db
from jungler.config import DefaultConfig as Config
from jungler.models.feed import Feed


class NaverBot(object):
    url = 'http://openapi.naver.com/search'

    def get_detected_content(self, url):
        html = urllib.urlopen(url).read()
        readable_article = Document(html).summary()
        p = re.compile(r'<img.*?/>')
        return p.sub('', readable_article)

    def crawl(self, keyword, feed_count=10):
        keywords = keyword.name.split(' ')
        keywords = '+'.join(keywords)
        query_dict = dict(
            key=Config.NAVER_SEARCH_API_KEY,
            target='news',
            query=keywords.encode('utf-8'),
            display=feed_count
        )
        query = urllib.urlencode(query_dict)
        parsed_result = feedparser.parse('%s?%s' % (self.url, query))
        feeds = []
        for entry in parsed_result.entries:
            f = Feed.get_by(url=entry.originallink)
            if f is None:
                f = Feed(title=entry.title,
                         summary=entry.summary,
                         content=self.get_detected_content(entry.link),
                         url=entry.originallink,
                         write_time=datetime.strptime(entry.published[:-6], '%a, %d %b %Y %H:%M:%S'))
                f.save(commit=False)
            else:
                if keyword in f.keywords:
                    continue
            f.keywords.append(keyword)
            feeds.append(f)
        db.session.commit()
        return feeds