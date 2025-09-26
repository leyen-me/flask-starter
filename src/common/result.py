import json
import logging
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Union, Optional
from sqlalchemy.engine.row import Row
from dataclasses import is_dataclass, asdict
import uuid

logger = logging.getLogger(__name__)

class SerializationError(Exception):
    """序列化异常"""
    pass

class Result:
    code = 0
    msg = 'success'
    data = None

    def __init__(self):
        self.code = 0
        self.msg = 'success'
        self.data = None

    @classmethod
    def serialize(cls, data: Any, max_depth: int = 10, visited_objects: Optional[set] = None) -> Any:
        """
        处理返回时的序列化问题
        """
        if visited_objects is None:
            visited_objects = set()
        
        if max_depth <= 0:
            logger.warning("达到最大序列化深度")
            return str(data)
        
        # 处理 None
        if data is None:
            return data
        
        # 处理基本类型
        if isinstance(data, (int, str, bool, float)):
            return data
        
        # 处理日期时间类型
        elif isinstance(data, (datetime, date, time)):
            return data.isoformat()
        
        # 处理 Decimal
        elif isinstance(data, Decimal):
            return float(data)
        
        # 处理 UUID
        elif isinstance(data, uuid.UUID):
            return str(data)
        
        # 处理字节类型
        elif isinstance(data, bytes):
            return data.decode('utf-8')
        
        # 处理字典
        elif isinstance(data, dict):
            result = {}
            for key, value in data.items():
                result[str(key)] = cls.serialize(value, max_depth - 1, visited_objects)
            return result
        
        # 处理列表
        elif isinstance(data, list):
            return [cls.serialize(item, max_depth - 1, visited_objects) for item in data]
        
        # 处理元组
        elif isinstance(data, tuple):
            return [cls.serialize(item, max_depth - 1, visited_objects) for item in data]
        
        # 处理集合
        elif isinstance(data, (set, frozenset)):
            return list(cls.serialize(list(data), max_depth - 1, visited_objects))
        
        # 处理枚举
        elif isinstance(data, Enum):
            return data.value if hasattr(data, 'value') else str(data)
        
        # 处理异常对象
        elif isinstance(data, BaseException):
            return {
                'type': type(data).__name__,
                'message': str(data),
                'args': cls.serialize(data.args, max_depth - 1, visited_objects) if data.args else []
            }
        
        # 序列化数据库模型
        elif hasattr(data, '__table__'):  # SQLAlchemy Model
            return cls._serialize_sqlalchemy_model(data, max_depth - 1, visited_objects)
        
        # 处理 Row 对象
        elif isinstance(data, Row):
            return cls.serialize(dict(data._mapping), max_depth - 1, visited_objects)
        
        # 处理数据类
        elif is_dataclass(data):
            try:
                return cls.serialize(asdict(data), max_depth - 1, visited_objects)
            except Exception:
                # 如果 asdict 失败，回退到属性序列化
                return cls._serialize_object_attributes(data, max_depth - 1, visited_objects)
        
        # 处理可调用对象（函数、方法等）
        elif callable(data):
            return f"<callable: {type(data).__name__}>"
        
        # 处理生成器
        elif hasattr(data, '__next__') or hasattr(data, '__iter__'):
            try:
                # 尝试转换为列表，但要小心无限生成器
                if hasattr(data, '__len__'):
                    return cls.serialize(list(data), max_depth - 1, visited_objects)
                else:
                    # 对于迭代器，只取前10个元素作为示例
                    items = []
                    for i, item in enumerate(data):
                        if i >= 10:  # 限制数量防止无限迭代
                            items.append("... (truncated)")
                            break
                        items.append(cls.serialize(item, max_depth - 1, visited_objects))
                    return items
            except:
                return f"<iterator: {type(data).__name__}>"
        
        # 处理自定义对象
        elif isinstance(data, object):
            obj_id = id(data)
            if obj_id in visited_objects:
                logger.warning(f"检测到循环引用: {type(data).__name__}")
                return f"<Circular reference: {type(data).__name__}>"
            
            visited_objects.add(obj_id)
            try:
                result = cls._serialize_object_attributes(data, max_depth - 1, visited_objects)
                return result
            finally:
                visited_objects.discard(obj_id)
        
        # 最后尝试转换为字符串
        else:
            try:
                return str(data)
            except Exception as e:
                logger.error(f"序列化异常: {type(data)}, 错误: {e}")
                raise SerializationError(f"序列化异常: {e}")

    @classmethod
    def _serialize_sqlalchemy_model(cls, data: Any, max_depth: int, visited_objects: set) -> Dict[str, Any]:
        """序列化 SQLAlchemy 模型"""
        result = {}
        
        # 获取模型的所有列名（数据库字段）
        if hasattr(data, '__table__'):
            columns = data.__table__.columns.keys()
        else:
            # 备用方案
            columns = [attr for attr in dir(data) 
                      if not attr.startswith('_') and not callable(getattr(data, attr))]
        
        # 序列化数据库字段
        for column in columns:
            try:
                value = getattr(data, column)
                # 跳过 SQLAlchemy 内部属性和可调用对象
                if column in ['metadata', 'query', 'registry'] or callable(value) or column.startswith('_'):
                    continue
                result[column] = cls.serialize(value, max_depth, visited_objects)
            except AttributeError:
                continue
            except Exception as e:
                logger.warning(f"序列化模型属性 {column} 失败: {e}")
                continue
        
        # 序列化动态属性（扩展属性）
        dynamic_attrs = cls._get_dynamic_attributes(data)
        for attr_name in dynamic_attrs:
            try:
                attr_value = getattr(data, attr_name)
                if not callable(attr_value):  # 跳过方法
                    result[attr_name] = cls.serialize(attr_value, max_depth, visited_objects)
            except (AttributeError, TypeError):
                continue
            except Exception as e:
                logger.warning(f"序列化动态属性 {attr_name} 失败: {e}")
                continue
        
        return result

    @classmethod
    def _get_dynamic_attributes(cls, data: Any) -> List[str]:
        """获取 SQLAlchemy 模型的动态属性"""
        # 获取所有属性名
        all_attrs = dir(data)
        
        # 获取数据库列名
        db_columns = set()
        if hasattr(data, '__table__'):
            db_columns = set(data.__table__.columns.keys())
        
        # 获取 SQLAlchemy 内部属性
        sqlalchemy_internal = {
            '_sa_instance_state', '_sa_class_manager', '_sa_registry', 
            '__mapper__', '__table__', 'metadata', 'query', 'registry'
        }
        
        # 筛选出动态属性（不在数据库列中的属性）
        dynamic_attrs = []
        for attr in all_attrs:
            if (not attr.startswith('_') and 
                attr not in db_columns and 
                attr not in sqlalchemy_internal and
                attr not in ['metadata', 'query', 'registry']):  # 额外排除这些
                try:
                    value = getattr(data, attr)
                    if not callable(value):  # 不包括方法
                        dynamic_attrs.append(attr)
                except:
                    continue
        
        return dynamic_attrs

    @classmethod
    def _serialize_object_attributes(cls, data: Any, max_depth: int, visited_objects: set) -> Dict[str, Any]:
        """序列化普通对象的属性"""
        result = {}
        
        # 安全地获取对象属性
        for attr_name in dir(data):
            if attr_name.startswith('_') or attr_name.endswith('_'):
                continue
            
            try:
                attr_value = getattr(data, attr_name)
                if callable(attr_value):
                    continue
                
                # 跳过 SQLAlchemy 相关属性
                if attr_name in ['metadata', 'query', 'registry']:
                    continue
                
                result[attr_name] = cls.serialize(attr_value, max_depth, visited_objects)
            except (AttributeError, TypeError):
                continue
            except Exception as e:
                logger.warning(f"序列化属性 {attr_name} 失败: {e}")
                continue
        
        return result

    @classmethod
    def handle(cls, data: Any) -> Dict[str, Any]:
        """处理序列化"""
        try:
            # 序列化数据
            return cls.serialize(data)
        except Exception as e:
            error_msg = "序列化异常, 请手动添加规则" + ' ' + str(e)
            logger.error(f'{error_msg}')
            raise Exception("序列化异常, 请手动添加规则")

    @classmethod
    def ok(cls, data=None):
        """成功响应"""
        res = Result()
        res.data = data
        # 直接返回格式化的字典，而不是序列化整个 Result 对象
        return {
            'code': 0,
            'msg': 'success',
            'data': cls.serialize(data)
        }

    @classmethod
    def error(cls, msg: str):
        """错误响应"""
        res = Result()
        res.code = 500
        res.msg = msg
        # 直接返回格式化的字典
        return {
            'code': 500,
            'msg': msg,
            'data': None
        }