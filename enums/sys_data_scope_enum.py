from enum import Enum


class SysDataScopeEnum(Enum):
    # 全部数据
    ALL = 0

    # 本机构及子机构数据
    # org_id in [a,b,c]
    ORG_AND_CHILD = 1

    # 本机构数据
    # org_id == a
    ORG_ONLY = 2

    # 本人数据
    # creator == mid
    SELF = 3

    # 自定义数据
    # org_id in [c,d]
    CUSTOM = 4
