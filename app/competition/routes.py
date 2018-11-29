from flask import Blueprint, jsonify, request, g
from app import db, auth
from app.competition.forms import Competition, Comtype
from app.interest.forms import Interest
from app.user.forms import User
import datetime
from sqlalchemy import or_


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
    except Exception:
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

# 推荐


@competitions.route('/api/competitions/recommend', methods=['POST'])
@auth.login_required
def get_recommends():
    try:
        p_page = int(request.json.get("page"))
        p_pageSize = int(request.json.get("pageSize"))
        all_types = Interest.query.filter(Interest.int_usernum == g.user.user_num).all()
        if all_types:
            all_types = [types.int_typename for types in all_types]
            rule = or_(*[Comtype.comtype_typename == t for t in all_types])
            all_comids = Comtype.query.filter(rule).group_by(Comtype.comtype_comid).all()
            all_comids = [com.comtype_comid for com in all_comids]
            rule = or_(*[Competition.com_id == c for c in all_comids])
            all_coms = Competition.query.filter(rule).order_by(Competition.com_id.desc()).limit(p_pageSize).offset((p_page - 1) * p_pageSize).all()
            return return_json(data=[com.to_dict() for com in all_coms])
        else:
            rand = datetime.datetime.now().second % 8 + 2
            all_coms = Competition.query.filter(Competition.com_id % rand == 0).order_by(Competition.com_id.desc()).limit(p_pageSize).offset((p_page - 1) * p_pageSize).all()
            return return_json(data=[com.to_dict() for com in all_coms])
    except Exception as e:
        raise e
        return return_json(code=0, msg='请求参数错误')
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
        all_compe = Competition.query.filter(Comtype.comtype_typename == p_type).join(Comtype, Comtype.comtype_comid == Competition.com_id).order_by(Competition.com_id.desc()).limit(p_pageSize).offset((p_page - 1) * p_pageSize).all()
        return return_json(data=[comp.to_dict() for comp in all_compe])
    except Exception:
        return return_json(code=0, msg='请求参数有误')


@competitions.route('/api/competitions/search', methods=['POST'])
def search():
    try:
        p_page = int(request.json.get("page"))
        p_pageSize = int(request.json.get("pageSize"))
        p_words = request.json.get("words")
        p_words = p_words.split(' ')
        p_words = ['%' + word + '%' for word in p_words]
        title_rule = or_(*[Competition.com_title.like(w) for w in p_words])
        type_rule = or_(*[Competition.com_type.like(w) for w in p_words])
        user_rule = or_(*[User.user_name.like(w) for w in p_words])
        all_compe = Competition.query.filter(or_(title_rule, type_rule)).order_by(Competition.com_id.desc()).limit(p_pageSize).offset((p_page - 1) * p_pageSize).all()
        all_users = User.query.filter(user_rule).limit(p_pageSize).offset((p_page - 1) * p_pageSize).all()
        return return_json(data={'competitions': [comp.to_dict() for comp in all_compe], 'users': [user.to_dict() for user in all_users]})
    except Exception:
        return return_json(code=0, msg='请求参数有误')
