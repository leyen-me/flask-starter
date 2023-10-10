from sqlalchemy import select
from sqlalchemy.orm import aliased

from db import db
from common import Result, Tree
from model import SysOrgModel, SysUserModel
from service import BaseService



class SysOrgService(BaseService):

    def get_list(self):
        t2 = aliased(SysOrgModel)
        subquery = select(t2.name).where(t2.id == SysOrgModel.pid).label("parent_name")
        # 主查询
        main_query = db.session.query(SysOrgModel, subquery).filter(SysOrgModel.deleted == 0).order_by(SysOrgModel.sort.asc())
        main_query = self.get_query_by_data_scope(main_query, SysOrgModel, 'id')
        results = main_query.all()
        
        org_objects = []
        for res in results:
            result = res[0]
            # 创建 SysOrgModel 模型对象并传入查询结果
            org = SysOrgModel(
                id=result.id, name=result.name, pid=result.pid, deleted=result.deleted, sort=result.sort, parent_name=res[1],
                create_time=result.create_time, update_time=result.update_time, creator=result.creator, updater=result.updater, version = result.version)
            # 将模型对象添加到列表中
            org_objects.append(org)
        return Tree.build_tree(Result.handle(org_objects))

    def info(self, org_id):
        org = db.session.query(SysOrgModel).filter(SysOrgModel.id == org_id, SysOrgModel.deleted == 0).one()
        if(org.pid != 0):
            # 获取上级机构名称
            p_org = db.session.query(SysOrgModel).filter(SysOrgModel.id == org.pid, SysOrgModel.deleted == 0).one()
            org.parent_name = p_org.name
        return org

    def save(self, vo):
        org = SysOrgModel(**vo)
        db.session.add(org)
        db.session.commit()
        return org

    def update(self, vo):
        org = db.session.query(SysOrgModel).filter(SysOrgModel.id==vo['id'], SysOrgModel.deleted==0).one()

        if vo['id'] == vo['pid']:
            raise Exception("上级机构不能为自身")
        
        sub_org_list = self.get_sub_org_id_list(vo['id'])
        if vo['pid'] in sub_org_list:
            raise Exception("上级机构不能为下级")

        for key, value in vo.items():
            setattr(org, key, value)
        db.session.commit()

    def delete(self, org_id):
        # 判断是否有子机构
        count = db.session.query(SysOrgModel).filter(SysOrgModel.pid == org_id, SysOrgModel.deleted == 0).count()
        if count > 0:
            raise Exception("请先删除子机构")
        
        # 判断机构下面是否有用户
        user_count = db.session.query(SysUserModel).filter(SysUserModel.org_id == org_id, SysUserModel.deleted == 0).count()
        if user_count > 0:
            raise Exception("机构下面有用户，不能删除")
        
        org = db.session.query(SysOrgModel).filter(SysOrgModel.id == org_id, SysOrgModel.deleted == 0).one()
        org.deleted = 1
        
        db.session.commit()
        return True

    def get_sub_org_id_list(self, org_id):
        res = db.session.query(SysOrgModel).filter(SysOrgModel.deleted == 0).all()
        org_tree = Tree.build_tree(Result.handle(res))
        # 递归查询所有子机构ID列表
        sub_id_list = Tree.get_child_ids(org_tree, org_id)
        sub_id_list.append(org_id)
        return sub_id_list