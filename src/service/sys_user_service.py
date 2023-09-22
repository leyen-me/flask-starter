import bcrypt
import pandas as pd
from flask import request, g
from sqlalchemy import func

from db import db
from model import SysUserModel, SysRoleModel, SysUserRoleModel
from service import *
from enums import SysDataScopeEnum, SysLoginStatusEnum, SysLoginOperationEnum, SysUserStatusEnum



class SysUserService(BaseService):

    def get_by_id(self, user_id):
        res = db.session.query(SysUserModel).filter(SysUserModel.id == user_id,SysUserModel.deleted == 0).one()
        return res

    def page(self):
        query = db.session.query(SysUserModel)

        username = request.args.get('username')
        if username:
            query = query.filter(SysUserModel.username == username)

        mobile = request.args.get('mobile')
        if mobile:
            query = query.filter(SysUserModel.mobile == mobile)

        gender = request.args.get('gender')
        if gender:
            query = query.filter(SysUserModel.gender == gender)

        return self.query_page(query)

    def login(self, username, password):
        res = None
        try:
            res: SysUserModel = db.session.query(SysUserModel).filter(
                SysUserModel.username == username).one()
        except:
            SysLogLoginService().save(username=username, status=SysLoginStatusEnum.FAIL.value, operation=SysLoginOperationEnum.ACCOUNT_FAIL.value)        
            # 用户不存在
            raise Exception("用户不存在")
        password = str(password).encode('utf-8')
        _password = str(res.password).encode('utf-8')
        if bcrypt.checkpw(password, _password):
            if res.status == SysUserStatusEnum.DISABLE.value:
                raise Exception("账号已被停用")
            return res
        else:
            SysLogLoginService().save(username=username, status=SysLoginStatusEnum.FAIL.value, operation=SysLoginOperationEnum.ACCOUNT_FAIL.value)        
            raise Exception("用户名或密码错误")
        
    def update_password(self, vo):
        # 旧密码
        old_password = vo['password'].encode('utf-8')
        # 新密码
        new_password = vo['new_password'].encode('utf-8')

        db_model = db.session.query(SysUserModel).filter(SysUserModel.id == g.user['id']).one()
        # 数据库存的密码
        db_passoword = db_model.password.encode('utf-8')
        # 比对以前的密码
        if bcrypt.checkpw(old_password, db_passoword):  
            salt = bcrypt.gensalt()
            new_password = bcrypt.hashpw(password=new_password,salt=salt).decode("utf-8")
            db_model.password = new_password
            db.session.commit()
            return "修改成功"
        else:
            raise Exception("原密码错误")
        
        # 删除在线用户，在线用户需要重新登录

    
    def get_data_scope(self, user):
        data_scope = db.session.query(
            func.min(SysRoleModel.data_scope)).\
            join(SysUserRoleModel, SysRoleModel.id == SysUserRoleModel.role_id).\
            filter(SysUserRoleModel.user_id == user.id, SysRoleModel.deleted == 0,SysUserRoleModel.deleted == 0).\
            scalar()
        if data_scope == None:
            return []
        else:
            # 全部数据权限，则返回null
            if data_scope == SysDataScopeEnum.ALL.value:
                return None
            
            # 本机构及子机构数据
            # 自定义数据权限范围
            elif data_scope == SysDataScopeEnum.ORG_AND_CHILD.value:
                res = []
                res += SysOrgService().get_sub_org_id_list(user.org_id)
                res += SysRoleDataScopeService().get_data_scope_list(user.id)
                return res
                        
            # 本机构数据
            # 自定义数据权限范围
            elif data_scope == SysDataScopeEnum.ORG_ONLY.value:
                res = []
                res += [user.org_id]
                res += SysRoleDataScopeService().get_data_scope_list(user.id)
                return res
            
            # 自定义数据权限范围
            elif data_scope == SysDataScopeEnum.CUSTOM.value:
                res = SysRoleDataScopeService().get_data_scope_list(user.id)
                return res
            else:
                return []

    def get_by_username(self, username):
        return db.session.query(SysUserModel).filter(SysUserModel.username == username, SysUserModel.deleted == 0).one_or_none()
    
    def get_by_mobile(self, mobile):
        return db.session.query(SysUserModel).filter(SysUserModel.mobile == mobile, SysUserModel.deleted == 0).one_or_none()

    def save(self, vo):
        user = SysUserModel(**vo)
        res = self.get_by_username(user.username)
        if res != None:
            raise Exception("用户已存在")
        res = self.get_by_mobile(user.mobile)
        if res != None:
            raise Exception("手机号已存在")
        user.password = bcrypt.hashpw(password=user.password.encode('utf-8'),salt=bcrypt.gensalt()).decode("utf-8")

        # 保存用户
        db.session.add(user)
        db.session.commit()

        # 保存用户角色关系
        SysUserRoleService().save_or_update(user.id, user.role_id_list)
        SysUserPostService().save_or_update(user.id, user.post_id_list)
        
        return True
    


    def update(self, vo):
        user = db.session.query(SysUserModel).filter(SysUserModel.id == vo['id'],SysUserModel.deleted == 0).one()

        res = self.get_by_username(vo['username'])
        if res != None and res.id != user.id:
            raise Exception("用户已存在")
        
        res = self.get_by_mobile(vo['mobile'])
        if res != None and res.id != user.id:
            raise Exception("手机号已存在")

        if user.password != None:
            user.password = bcrypt.hashpw(password=user.password.encode('utf-8'),salt=bcrypt.gensalt()).decode("utf-8")
        
        # 保存用户
        for key, value in vo.items():
            setattr(user, key, value)
        
        db.session.add(user)
        db.session.commit()

        # 保存用户角色关系
        SysUserRoleService().save_or_update(user.id, vo['role_id_list'])
        SysUserPostService().save_or_update(user.id, vo['post_id_list'])

        # 修改用户的缓存信息
        SysUserTokenService().update_cache_auth_by_user_id(user.id)
        return True
    


    def delete(self, curr_user_id, id_list):
        if curr_user_id in id_list:
            raise Exception("不能删除当前用户")
        
        users = db.session.query(SysUserModel).filter(SysUserModel.id.in_(id_list), SysUserModel.deleted == 0).all()
        for user in users:
            user.deleted = 1
        db.session.commit()

        # 批量删除角色关系
        SysUserPostService().delete_by_user_id_list(id_list)
        # 批量删除岗位关系
        SysUserRoleService().delete_by_user_id_list(id_list)
        return True
    
    """
    默认第一行是数据库字段名
    默认第二行是数据库字段名对应的注释
    """
    def import_by_excel(self,file_path):
        df = pd.read_excel(file_path)
        fields = SysUserModel.__table__.columns.keys()
        models = []
        for index, row in df.iterrows():
            if index > 0:
                model_dict = {}
                for key in fields:
                    try:
                        value = row[key]
                        if key == 'password' and value != None:
                            value = bcrypt.hashpw(password=str(value).encode('utf-8'),salt=bcrypt.gensalt()).decode("utf-8")
                    except:
                        value = None
                    model_dict[key] = value
                models.append(SysUserModel(**model_dict))
        db.session.bulk_save_objects(models)
        db.session.commit()
    
    def export(self):
        return super().export()
    
    def role_user_page(self):
        # 非必传参数
        username = request.args.get('username')
        mobile   = request.args.get('mobile')
        gender   = request.args.get('gender')
        role_id   = request.args.get('role_id')

        query = db.session.query(SysUserModel).join(SysUserRoleModel, SysUserModel.id == SysUserRoleModel.user_id, isouter = True).filter(SysUserModel.deleted == 0, SysUserRoleModel.deleted == 0, SysUserRoleModel.role_id == role_id)
        if username:
            query = query.filter(SysUserModel.username.like(f"%{username}%"))
        if mobile:
            query = query.filter(SysUserModel.mobile.like(f"%{mobile}%"))
        if gender:
            query = query.filter(SysUserModel.gender == gender)
        return self.query_page(query)