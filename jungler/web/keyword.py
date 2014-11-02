#-*- coding: utf-8 -*-
from flask import Blueprint, request, render_template

from jungler.models.keyword import Keyword
from jungler.decorators import json_response
from jungler.tasks import feeds_of_keyword_crawl

blueprint = Blueprint('keyword', __name__, url_prefix='/keyword')


@blueprint.route('s')
def keywords():
    keywords_ = Keyword.query.all()
    return render_template('keyword_list.html', keywords=keywords_)


@blueprint.route('/create', methods=['GET', 'POST'])
def keyword_create():
    if request.method == 'GET':
        return render_template('keyword_create.html')
    else:
        name = request.form.get('name', None)
        if name:
            keyword = Keyword.get_by(name=name)
            if not keyword:
                keyword = Keyword(name=name)
                keyword.save(True)
                feeds_of_keyword_crawl.delay(keyword.id)
                return render_template('keyword_create.html', message=u'"%s" 키워드가 생성 되었습니다.' % name)
            else:
                return render_template('keyword_create.html', message=u'이미 등록된 키워드입니다.')
        return render_template('keyword_create.html', message=u'키워드 이름을 입력해주세요.')


@blueprint.route('s/<keyword_id>/delete', methods=['DELETE'])
@json_response
def keyword_delete(keyword_id):
    keyword = Keyword.get(keyword_id)
    if not keyword:
        return dict(status=dict(reason=u'존재하지 않는 키워드입니다.', code='FAIL'))
    else:
        keyword.delete()
        return dict(status=dict(reason=u'삭제되었습니다.', code='OK'))