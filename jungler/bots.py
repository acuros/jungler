#-*- coding: utf-8 -*-
import re
import urllib
import feedparser

from datetime import datetime

from readability.readability import Document

from jungler.config import DefaultConfig as config
from jungler.models.feed import Feed


class NaverBot(object):
    url = 'http://openapi.naver.com/search'

    def get_searched_feeds(self, keyword, feed_count=10):
        keywords = keyword.name.split(' ')
        keywords = '+'.join(keywords)
        query_dict = dict(
            key=config.NAVER_SEARCH_API_KEY,
            target='news',
            query=keywords.encode('utf-8'),
            display=feed_count
        )
        query = urllib.urlencode(query_dict)
        parsed_result = feedparser.parse('%s?%s' % (self.url, query))
        feeds = []
        for entry in parsed_result.entries:
            f = Feed(title=entry.title,
                     summary=entry.summary,
                     content=self.get_detected_content(entry.link),
                     url=entry.originallink,
                     write_time=datetime.strptime(entry.published[:-6], '%a, %d %b %Y %H:%M:%S'))
            f.keywords.append(keyword)
            feeds.append(f)
        return feeds

    def get_detected_content(self, url):
        html = urllib.urlopen(url).read()
        readable_article = Document(html).summary()
        p = re.compile(r'<img.*?/>')
        return p.sub('', readable_article)