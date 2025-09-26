from enum import Enum


class SysOperateTypeEnum(Enum):
    # 查询
    GET = 1
    # 新增
    INSERT = 2
    # 修改
    UPDATE = 3
    # 删除
    DELETE = 4
    # 导出
    EXPORT = 5
    # 导入
    IMPORT = 6
    # 导入
    OTHER = 0
