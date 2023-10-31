from sqlalchemy import Column, BigInteger, Integer, String

from .sys_base_model import SysBaseModel


class SysMenuModel(SysBaseModel):
    __tablename__ = "sys_menu"

    pid = Column(BigInteger, comment="上级ID，一级菜单为0")
    name = Column(String(200), comment="菜单名称")
    url = Column(String(200), comment="菜单URL")
    authority = Column(String(200), comment="授权标识(多个用逗号分隔，如：sys:menu:list,sys:menu:save)")
    type = Column(Integer, comment="类型   0：菜单   1：按钮   2：接口")
    open_style = Column(Integer, comment="打开方式   0：内部   1：外部")
    icon = Column(String(50), comment="菜单图标")
    sort = Column(Integer, default=0, comment="排序")

    parent_name = ''
    children = []
