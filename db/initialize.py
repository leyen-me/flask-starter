from db import db
from model import SysUserModel, SysMenuModel, SysDictTypeModel, SysDictDataModel, SysParamsModel

class Initialize:

    @classmethod
    def init(cls):
        # 视情况创建表和初始化数据
        cls.create_table()
        cls.init_data()
        pass

    @classmethod
    def create_table(cls):
        db.create_all()

    @classmethod
    def create_data_with_none(cls, model):
        res = db.session.query(model.__class__).filter(getattr(model.__class__,'id') == model.id).one_or_none()
        if not res:
            db.session.add(model)
            db.session.commit()

    @classmethod
    def init_data(cls):
        # =========================================创建超级管理员START=========================================#
        super_admin =  SysUserModel(
                         id=10000, 
                         username="admin", 
                         password="$2a$10$mW/yJPHjyueQ1g26WNBz0uxVPa0GQdJO1fFZmqdkqgMTGnyszlXxu",
                         real_name="admin",
                         avatar="https://cdn.maku.net/images/avatar.png",
                         gender=0,
                         email="admin@qq.com",
                         mobile="13612345678",
                         status=1,
                         org_id=None,
                         super_admin=1,
                         creator=10000,
                         updater=10000,
                         )
        cls.create_data_with_none(super_admin)
        # =========================================创建超级管理员E N D=========================================#



        # =========================================创建菜单START=========================================#
        menu_list = [
            SysMenuModel(
                id=1, pid=0, name="系统设置", url=None, authority=None, type=0, open_style=0, icon="icon-setting", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=2, pid=1, name="菜单管理", url="sys/menu", authority=None, type=0, open_style=0, icon="icon-menu", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=3, pid=2, name="查看", url="", authority="sys:menu:list", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=4, pid=2, name="新增", url="", authority="sys:menu:save", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=5, pid=2, name="修改", url="", authority="sys:menu:update,sys:menu:info", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=6, pid=2, name="删除", url="", authority="sys:menu:delete", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=7, pid=1, name="数据字典", url="sys/dict", authority=None, type=0, open_style=0, icon="icon-insertrowabove", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=8, pid=7, name="查询", url="", authority="sys:dict:page", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=9, pid=7, name="新增", url="", authority="sys:dict:save", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=10, pid=7, name="修改", url="", authority="sys:dict:update,sys:dict:info", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=11, pid=7, name="删除", url="", authority="sys:dict:delete", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=12, pid=0, name="权限管理", url="", authority=None, type=0, open_style=0, icon="icon-safetycertificate", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=13, pid=12, name="岗位管理", url="sys/post", authority=None, type=0, open_style=0, icon="icon-solution", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=14, pid=13, name="查询", url="", authority="sys:post:page", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=15, pid=13, name="新增", url="", authority="sys:post:save", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=16, pid=13, name="修改", url="", authority="sys:post:update,sys:post:info", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=17, pid=13, name="删除", url="", authority="sys:post:delete", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=18, pid=12, name="机构管理", url="sys/org", authority=None, type=0, open_style=0, icon="icon-cluster", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=19, pid=18, name="查询", url="", authority="sys:org:list", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=20, pid=18, name="新增", url="", authority="sys:org:save", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=21, pid=18, name="修改", url="", authority="sys:org:update,sys:org:info", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=22, pid=18, name="删除", url="", authority="sys:org:delete", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=23, pid=12, name="角色管理", url="sys/role", authority=None, type=0, open_style=0, icon="icon-team", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=24, pid=23, name="查询", url="", authority="sys:role:page", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=25, pid=23, name="新增", url="", authority="sys:role:save,sys:role:menu,sys:org:list", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=26, pid=23, name="修改", url="", authority="sys:role:update,sys:role:info,sys:role:menu,sys:org:list,sys:user:page", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=27, pid=23, name="删除", url="", authority="sys:role:delete", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=28, pid=12, name="用户管理", url="sys/user", authority=None, type=0, open_style=0, icon="icon-user", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=29, pid=28, name="查询", url="", authority="sys:user:page", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=30, pid=28, name="新增", url="", authority="sys:user:save,sys:role:list", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=31, pid=28, name="修改", url="", authority="sys:user:update,sys:user:info,sys:role:list", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=32, pid=28, name="删除", url="", authority="sys:user:delete", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            # SysMenuModel(
            #     id=33, pid=0, name="应用管理", url="", authority=None, type=0, open_style=0, icon="icon-appstore", creator=10000, updater=10000
            # ),
            SysMenuModel(
                id=34, pid=1, name="附件管理", url="sys/attachment", authority=None, type=0, open_style=0, icon="icon-folder-fill", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=35, pid=34, name="查看", url="", authority="sys:attachment:page", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=36, pid=34, name="上传", url="", authority="sys:attachment:save", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=37, pid=34, name="删除", url="", authority="sys:attachment:delete", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=38, pid=0, name="日志管理", url="", authority=None, type=0, open_style=0, icon="icon-filedone", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=39, pid=38, name="登录日志", url="sys/log/login", authority="sys:log:login", type=0, open_style=0, icon="icon-solution", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=40, pid=28, name="导入", url="", authority="sys:user:import", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=41, pid=28, name="导出", url="", authority="sys:user:export", type=1, open_style=0, icon="", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=42, pid=1, name="参数管理", url="sys/params", authority="sys:params:all", type=0, open_style=0, icon="icon-filedone", creator=10000, updater=10000
            ),
            SysMenuModel(
                id=43, pid=38, name="操作日志", url="sys/log/operate", authority="sys:operate:all", type=0, open_style=0, icon="icon-file-text", creator=10000, updater=10000
            ),
        ]

        for menu in menu_list:
            cls.create_data_with_none(menu)
        # =========================================创建菜单E N D=========================================#



        # =========================================创建字典类型START=========================================#
        dict_type_list = [
            SysDictTypeModel(id=1, dict_type="post_status", dict_name="状态", remark="岗位管理", creator=super_admin.id, updater=super_admin.id),
            SysDictTypeModel(id=2, dict_type="user_gender", dict_name="性别", remark="用户管理", creator=super_admin.id, updater=super_admin.id),
            SysDictTypeModel(id=3, dict_type="user_status", dict_name="状态", remark="用户管理", creator=super_admin.id, updater=super_admin.id),
            SysDictTypeModel(id=4, dict_type="role_data_scope", dict_name="数据范围", remark="角色管理", creator=super_admin.id, updater=super_admin.id),
            SysDictTypeModel(id=5, dict_type="enable_disable", dict_name="状态", remark="功能状态：启用 | 禁用", creator=super_admin.id, updater=super_admin.id),
            SysDictTypeModel(id=6, dict_type="success_fail", dict_name="状态", remark="操作状态：成功 | 失败", creator=super_admin.id, updater=super_admin.id),
            SysDictTypeModel(id=7, dict_type="login_operation", dict_name="操作信息", remark="登录管理", creator=super_admin.id, updater=super_admin.id),
            SysDictTypeModel(id=8, dict_type="params_type", dict_name="系统参数", remark="参数管理", creator=super_admin.id, updater=super_admin.id),
            SysDictTypeModel(id=9, dict_type="user_super_admin", dict_name="用户是否是超管", remark="用户是否是超管", creator=super_admin.id, updater=super_admin.id),
            SysDictTypeModel(id=10, dict_type="log_operate_type", dict_name="操作类型", remark="操作日志", creator=super_admin.id, updater=super_admin.id),
        ]
        for dict_type in dict_type_list:
            cls.create_data_with_none(dict_type)
        # =========================================创建字典类型E N D=========================================#



        # =========================================创建字典数据START=========================================#
        dict_data_list = [
            SysDictDataModel(id=1, dict_type_id=1, dict_label="停用", dict_value="0", label_class="danger", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=2, dict_type_id=1, dict_label="正常", dict_value="1", label_class="primary", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=3, dict_type_id=2, dict_label="男", dict_value="0", label_class="primary", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=4, dict_type_id=2, dict_label="女", dict_value="1", label_class="success", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=5, dict_type_id=2, dict_label="未知", dict_value="2", label_class="warning", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=6, dict_type_id=3, dict_label="正常", dict_value="1", label_class="primary", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=7, dict_type_id=3, dict_label="停用", dict_value="0", label_class="danger", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=8, dict_type_id=4, dict_label="全部数据", dict_value="0", label_class="", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=9, dict_type_id=4, dict_label="本机构及子机构数据", dict_value="1", label_class="", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=10, dict_type_id=4, dict_label="本机构数据", dict_value="2", label_class="", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=11, dict_type_id=4, dict_label="本人数据", dict_value="3", label_class="", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=12, dict_type_id=4, dict_label="自定义数据", dict_value="4", label_class="", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=13, dict_type_id=5, dict_label="禁用", dict_value="0", label_class="danger", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=14, dict_type_id=5, dict_label="启用", dict_value="1", label_class="primary", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=15, dict_type_id=6, dict_label="失败", dict_value="0", label_class="danger", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=16, dict_type_id=6, dict_label="成功", dict_value="1", label_class="primary", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=17, dict_type_id=7, dict_label="登录成功", dict_value="0", label_class="primary", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=18, dict_type_id=7, dict_label="退出成功", dict_value="1", label_class="warning", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=19, dict_type_id=7, dict_label="验证码错误", dict_value="2", label_class="danger", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=20, dict_type_id=7, dict_label="账号密码错误", dict_value="3", label_class="danger", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=21, dict_type_id=8, dict_label="否", dict_value="0", label_class="primary", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=22, dict_type_id=8, dict_label="是", dict_value="1", label_class="danger", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=23, dict_type_id=9, dict_label="是", dict_value="1", label_class="danger", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=24, dict_type_id=9, dict_label="否", dict_value="0", label_class="primary", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=25, dict_type_id=10, dict_label="其它", dict_value="0", label_class="info", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=26, dict_type_id=10, dict_label="查询", dict_value="1", label_class="primary", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=27, dict_type_id=10, dict_label="新增", dict_value="2", label_class="success", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=28, dict_type_id=10, dict_label="修改", dict_value="3", label_class="warning", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=29, dict_type_id=10, dict_label="删除", dict_value="4", label_class="danger", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=30, dict_type_id=10, dict_label="导出", dict_value="5", label_class="info", remark="", creator=super_admin.id, updater=super_admin.id),
            SysDictDataModel(id=31, dict_type_id=10, dict_label="导入", dict_value="6", label_class="info", remark="", creator=super_admin.id, updater=super_admin.id),
        ]
        for dict_data in dict_data_list:
            cls.create_data_with_none(dict_data)
        # =========================================创建字典数据E N D=========================================#



        # =========================================创建参数START=========================================#
        param_list = [
            SysParamsModel(id=1, param_name="用户登录-验证码开关", param_type=1, param_key="LOGIN_CAPTCHA", param_value="false", remark="是否开启验证码（true：开启，false：关闭）", creator=super_admin.id, updater=super_admin.id)
        ]
        for param in param_list:
            cls.create_data_with_none(param)
        # =========================================创建参数E N D=========================================#