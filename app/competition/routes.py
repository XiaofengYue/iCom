from flask import Blueprint, jsonify, request
from app import db
from app.competition.forms import Competition, Comtype
import json
import datetime


competitions = Blueprint('competitions', __name__)


def return_json(code=200, msg='成功', data=None):
    return jsonify({'code': code, 'msg': msg, 'data': data})


@competitions.route('/api/competitions/bypage', methods=['POST'])
def get_by_page():
    try:
        p_page = int(request.json.get("page"))
        p_pageSize = int(request.json.get("pageSize"))
        all_compe = Competition.query.order_by(Competition.com_id.desc()).limit(p_pageSize).offset((p_page - 1) * p_pageSize).all()
        return return_json(data=[comp.to_dict() for comp in all_compe])
    except Exception as e:
        return return_json(code=0, msg='请求参数有误')


@competitions.route('/api/competitions/byid', methods=['POST'])
def get_by_id():
    try:
        p_id = int(request.json.get("com_id"))
        p_com = Competition.query.filter(Competition.com_id == p_id).all()
        if p_com:
            return return_json(data=p_com[0].to_dict())
        else:
            return return_json(code=0, msg='无此ID内容')
    except Exception:
        return return_json(code=0, msg='参数错误')


@competitions.route('/api/competitions/hot', methods=['POST'])
def get_hot_page():
    try:
        p_page = int(request.json.get("page"))
        p_pageSize = int(request.json.get("pageSize"))
        all_compe = Competition.query.filter(datetime.datetime.strftime(datetime.datetime.now(), '%Y.%m.%d %H:%M') < Competition.com_endtime).order_by(Competition.com_browse.desc()).limit(p_pageSize).offset((p_page - 1) * p_pageSize).all()
        return return_json(data=[comp.to_dict() for comp in all_compe])
    except Exception:

        return return_json(code=0, msg='请求参数有误')

# 获取全部类型


@competitions.route('/api/types', methods=['POST'])
def get_types():
    try:
        all_types = Comtype.query.group_by(Comtype.comtype_typename).all()
        print(all_types)
        return return_json(data=[types.comtype_typename for types in all_types])
    except Exception as e:
        raise e
        return return_json(code=0, msg='出错')


'''
select  competitions.com_id from competitions,comtypes
where
competitions.com_id = comtypes.comtype_comid
and comtypes.comtype_typename='服装设计'
'''


@competitions.route('/api/competitions/type', methods=['POST'])
def get_type_page():
    try:
        p_page = int(request.json.get("page"))
        p_pageSize = int(request.json.get("pageSize"))
        p_type = request.json.get("type")
        all_compe = Competition.query.filter(Comtype.comtype_typename == p_type).join(Comtype, Comtype.comtype_comid == Competition.com_id).limit(p_pageSize).offset((p_page - 1) * p_pageSize).all()
        return return_json(data=[comp.to_dict() for comp in all_compe])
    except Exception:
        return return_json(code=0, msg='请求参数有误')
