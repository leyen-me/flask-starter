import json
from flask import request

from db import db
from model import SysLogOperateModel
from service import BaseService

class SysLogOperateService(BaseService):

    def page(self):
        query = db.session.query(SysLogOperateModel).filter(SysLogOperateModel.deleted == 0)
        status = request.args.get('status')
        if status:
            query = query.filter(SysLogOperateModel.status == status)
        real_name = request.args.get('real_name')
        if real_name:
            query = query.filter(SysLogOperateModel.real_name.like(f"%{real_name}%"))
        req_uri = request.args.get('req_uri')
        if req_uri:
            query = query.filter(SysLogOperateModel.req_uri.like(f"%{req_uri}%"))
        # module = request.args.get('module')
        # if module:
        #     query = query.filter(SysLogOperateModel.module.like(f"%{module}%"))
        return self.query_page(query)
    
    def save(self, vo):
        ip = request.remote_addr
        req_method = request.method
        req_uri = request.path
        req_params = json.dumps(dict(request.args))
        user_agent = request.headers.get('User-Agent')
        model = SysLogOperateModel(
                            req_uri=req_uri, req_method=req_method, req_params= req_params, 
                            ip=ip, user_agent=user_agent, operate_type=vo['operate_type'], 
                            duration=vo['duration'], user_id=vo['user_id'], real_name=vo['real_name'], 
                            result_msg=vo['result_msg'], status=vo['status'])
        db.session.add(model)
        db.session.commit()