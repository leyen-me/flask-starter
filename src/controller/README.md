接口风格
```
RestFul风格
```

记录日志
```
from decorator import has_authority, operate_log
from enums import SysOperateTypeEnum

@operate_log(type = SysOperateTypeEnum.INSERT)
```

校验权限
```
@has_authority("sys:org:list")
```