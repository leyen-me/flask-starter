from sqlalchemy import Column, BigInteger, Integer, String

from .base_model import BaseModel


class SysRoleModel(BaseModel):
    __tablename__ = "sys_role"

    name = Column(String(50), comment="角色名称")
    remark = Column(String(100), comment="备注")
    data_scope = Column(Integer,
                        comment="数据范围  0：全部数据  1：本机构及子机构数据  2：本机构数据  3：本人数据  4：自定义数据")
    org_id = Column(BigInteger, comment="机构ID")

    menu_id_list = []
    org_id_list = []
