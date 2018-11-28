from flask import Blueprint, jsonify, request
from app import db
from app.collection.forms import Collection
from app.competition.forms import Competition

collections = Blueprint('collections', __name__)


def return_json(code=200, msg='成功', data=None):
    return jsonify({'code': code, 'msg': msg, 'data': data})

# 查询单条有没有被收藏


@collections.route('/api/collections/byid', methods=['POST'])
def get_byid():
    try:
        p_usernum = int(request.json.get("usernum"))
        p_comid = int(request.json.get("comid"))
        p_album = request.json.get("album")
        old_col = Collection.query.filter(Collection.col_usernum == p_usernum, Collection.col_comid == p_comid, Collection.col_album == p_album).all()
        if old_col:
            return return_json(data=old_col[0].to_dict())
        else:
            return return_json(code=1, msg='此信息未被收藏')
    except Exception:
        return return_json(code=0, msg='请求参数有误')

# 查


@collections.route('/api/collections/bypage', methods=['POST'])
def get_collections_page():
    try:
        p_page = int(request.json.get("page"))
        p_pageSize = int(request.json.get("pageSize"))
        p_usernum = int(request.json.get("usernum"))
        all_compe = Competition.query.filter(Collection.col_usernum == p_usernum).join(Collection, Competition.com_id == Collection.col_comid).order_by(Collection.col_id.desc()).limit(p_pageSize).offset((p_page - 1) * p_pageSize).all()
        return return_json(data=[comp.to_dict() for comp in all_compe])
    except Exception:
        return return_json(code=0, msg='请求参数有误')

# 增


@collections.route('/api/collections/add', methods=['POST'])
def add_collections():
    try:
        p_usernum = int(request.json.get("usernum"))
        p_comid = int(request.json.get("comid"))
        p_album = request.json.get("album")
        old_col = Collection.query.filter(Collection.col_usernum == p_usernum, Collection.col_comid == p_comid, Collection.col_album == p_album).all()
        if old_col:
            return return_json(code=1, msg='你已经添加过')
        new_col = Collection(col_comid=p_comid, col_usernum=p_usernum, col_album=p_album)
        db.session.add(new_col)
        db.session.commit()
        return return_json()
    except Exception:
        return return_json(code=0, msg='请求参数有误')
# 删


@collections.route('/api/collections/delete', methods=['POST'])
def delete_collections():
    try:
        p_usernum = int(request.json.get("usernum"))
        p_comid = int(request.json.get("comid"))
        p_album = request.json.get("album")
        old_col = Collection.query.filter(Collection.col_usernum == p_usernum, Collection.col_comid == p_comid, Collection.col_album == p_album).first()
        if old_col:
            db.session.delete(old_col)
            db.session.commit()
            return return_json()
        else:
            return return_json(code=1, msg='查无此条记录')
    except Exception:
        return return_json(code=0, msg='请求参数有误')
