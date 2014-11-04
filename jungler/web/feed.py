#-*- coding: utf-8 -*-
from flask import Blueprint, request, render_template

from jungler.decorators import json_response
from jungler.models.feed import Feed

blueprint = Blueprint('feed', __name__)


@blueprint.route('/feeds')
def feeds():
    feed_list = Feed.query.order_by(Feed.write_time.desc()).limit(30).all()
    return render_template('feed_list.html', feeds=feed_list)


@blueprint.route('/additional-feeds')
@json_response
def additional_feeds():
    last_feed_id = request.args.get('last_feed_id')
    last_feed = Feed.get(last_feed_id)
    if last_feed is None:
        return dict(status=dict(code='FAIL', reason=u'올바르지 않은 요청입니다.'))
    feeds_ = Feed.query.filter(Feed.id != last_feed_id, Feed.write_time >= last_feed.write_time).order_by(Feed.write_time.desc()).limit(30).all()
    serialized_feeds = []
    for f in feeds_:
        serialized_feeds.append(f.serialize())
    return dict(status=dict(code='OK', reason='OK'), feeds=serialized_feeds)


@blueprint.route('/feeds/<feed_id>')
def feed_detail(feed_id):
    feed = Feed.get_or_404(feed_id)
    return render_template('feed_detail.html', feed=feed.serialize())


