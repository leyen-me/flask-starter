### 平台简介
```
flask-starter是一套全部开源的快速开发平台，毫无保留给个人及企业免费使用。
灵感来源，感谢Maku，RuoYi等框架提供的解决方案。
前端采用Vue3, Vite, TypeScript, Pinia
后端采用 Python 语言 Flask 框架以及强大的 sqlalchemy
支持加载动态权限菜单，多方式轻松权限控制。
目录结构和编程风格偏向于Java层面，让长期使用Java开发的人员，开箱即用。
```

### 内置功能
```
用户管理：用户是系统操作者，该功能主要完成系统用户配置。
机构管理：配置系统组织机构（公司、部门、角色）
角色管理：角色菜单权限分配、数据权限分配、设置角色按部门进行数据范围权限划分。
权限权限：授权角色的权限范围。

菜单管理：配置系统菜单，操作权限，按钮权限标识、后端接口权限等。
定时任务：配置系统常用的定时任务。
数据字典：对系统中经常使用的一些较为固定的数据进行维护。
参数管理：对系统中经常使用的一些较为固定的参数进行维护。
附件管理：对平台上所有文件、图片等进行统一管理。

操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。
代码生成：根据模型对象，快速建表和建立对应的CRUD。（一分钟就能写一个CRUD）
```

### 项目框架
```
Flask             -> 基础框架
flask-sqlalchemy  -> ORM
redis             -> 缓存数据库
Flask-Cors        -> 跨域
Flask-APScheduler -> 定时任务
Pillow            -> 验证码生成器
pandas            -> Excel导入导出
PyYAML            -> 配置文件
bcrypt            -> 数据库密码加解密方案
```

### 首次使用
```
创建虚拟环境
python -m venv venv

激活虚拟环境
venv\Scripts\activate

安装依赖
pip install -r requirements.txt
```

### 运行
```cmd
run
```

### 生成依赖
```
pip freeze > requirements.txt
```