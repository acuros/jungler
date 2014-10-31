#-*- coding: utf-8 -*-
import re
import config
import urllib
import feedparser

from models.feed import Feed

from datetime import datetime

from readability.readability import Document


class NaverBot(object):
    url = 'http://openapi.naver.com/search'

    def get_searched_feeds(self, keywords, feed_count=10):
        if not keywords:
            return []
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
                     url=entry.link,
                     created_time=datetime.strptime(entry.published[:-6], '%a, %d %b %Y %H:%M:%S'))
            feeds.append(f)
        return feeds

    def get_detected_content(self, url):
        html = urllib.urlopen(url).read()
        readable_article = Document(html).summary()
        p = re.compile(r'<img.*?/>')
        return p.sub('', readable_article)