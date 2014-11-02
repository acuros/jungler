#-*- coding: utf-8 -*-
from flask import Blueprint, request, render_template

from jungler.models.feed import Feed

blueprint = Blueprint('feed', __name__, url_prefix='/feed')


@blueprint.route('s')
def feeds():
    feed_list = Feed.query.order_by(Feed.write_time.desc()).all()
    return render_template('feed_list.html', feeds=feed_list)


@blueprint.route('s/<feed_id>')
def feed_detail(feed_id):
    feed = Feed.get_or_404(feed_id)
    return render_template('feed_detail.html', feed=feed.serialize())


