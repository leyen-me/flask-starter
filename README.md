### 平台简介
```
Flask-Starter是一套全部开源的快速开发平台，毫无保留给个人及企业免费使用。
感谢Maku，RuoYi等框架提供的灵感来源。
前端采用Vue3, Vite, TypeScript, Pinia全家桶生态。
后端采用 Python 语言 Flask 框架以及强大的 Sqlalchemy
支持加载动态权限菜单，多方式轻松权限控制。
目录结构和编程风格偏向于Java层面，让长期使用Java开发的人员，开箱即用。
```

### 内置功能
```
用户管理：用户是系统操作者，该功能主要完成系统用户配置。
部门管理：配置系统组织机构（公司、部门、小组），树结构展现支持数据权限。
岗位管理：配置系统用户所属担任职务
菜单管理：配置系统菜单，操作权限，按钮权限标识等。
角色管理：角色菜单权限分配、设置角色按机构进行数据范围权限划分。
字典管理：对系统中经常使用的一些较为固定的数据进行维护。
参数管理：对系统动态配置常用参数。
操作日志：系统正常操作日志记录和查询；系统异常信息日志记录和查询。
登录日志：系统登录日志记录查询包含登录异常。
定时任务：定时任务的调度。
代码生成：后端代码的生成（controller层，service层)支持CRUD 
附件管理：对平台上所有文件、图片等进行统一管理。
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

### 系统需求
```
Python >= 3.8
MySQL  >= 5.7
Redis
```

### 安装依赖
```cmd
创建虚拟环境
python -m venv venv

激活虚拟环境
venv\Scripts\activate

安装依赖
pip install -r requirements.txt
```

### 本地运行
```cmd
激活虚拟环境
venv\Scripts\activate

cd src

python main.py
```

### 生成依赖
```
pip freeze > requirements.txt
```

### 服务器部署
```
构建镜像
docker build -t flask-starter .

运行容器
docker run -dit --name flask-starter-demo -p 8080:8080 flask-starter
```