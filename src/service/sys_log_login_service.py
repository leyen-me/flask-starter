from flask import request

from db import db
from model import SysLogLoginModel
from service import BaseService


class SysLogLoginService(BaseService):

    def page(self):
        # 检索
        username = request.args.get('username')
        address = request.args.get('address')
        status = request.args.get('status')
        query = db.session.query(SysLogLoginModel).filter(SysLogLoginModel.deleted == 0)
        if username:
            query = query.filter(SysLogLoginModel.username.like(f"%{username}%"))
        if address:
            query = query.filter(SysLogLoginModel.address.like(f"%{address}%"))
        if status:
            query = query.filter(SysLogLoginModel.status == status)

        # 默认排序
        query = query.order_by(SysLogLoginModel.create_time.desc())
        return self.query_page(query)

    def save(self, username, status, operation):
        ip = request.remote_addr
        user_agent = request.headers.get('User-Agent')
        model = SysLogLoginModel(ip=ip, user_agent=user_agent, username=username, status=status, operation=operation,
                                 creator=0, updater=0)
        db.session.add(model)
        db.session.commit()
