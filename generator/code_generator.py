import os
import re


class CodeGenerator:
    MODEL_DIR = "model"
    CONTROLLER_DIR = "controller"
    SERVICE_DIR = "service"

    # 并不是所有的服务都需要controller，比如中间表，所以要忽略生成的controller
    CONTROLLER_IGNORE = [
        "sys_role_data_scope_controller",
        "sys_role_menu_controller",
        "sys_user_post_controller",
        "sys_user_role_controller",
        "sys_user_token_controller"
    ]

    def get_service_template(self, upper_name):
        return f"""from flask import request

from db import db
from model import {upper_name}Model
from service import BaseService



class {upper_name}Service(BaseService):

    def page(self):
        query = db.session.query({upper_name}Model)
        return self.query_page(query)
    
    def list(self):
        return db.session.query({upper_name}Model).filter({upper_name}Model.deleted == 0).all()
    
    def info(self, id):
        return db.session.query({upper_name}Model).filter({upper_name}Model.id == id, {upper_name}Model.deleted == 0).one()

    def save(self, vo):
        model = {upper_name}Model(**vo)
        db.session.add(model)
        db.session.commit()
        return model

    def update(self, vo):
        model = db.session.query({upper_name}Model).filter({upper_name}Model.id == vo['id'], {upper_name}Model.deleted == 0).one()
        for key, value in vo.items():
            setattr(model, key, value)
        db.session.commit()
        return True

    def delete(self, id_list):
        self.remove_by_ids(id_list)
"""

    def get_controller_template(self, upper_name, underline_name, url_name, auth_name):
        return f"""from flask import Blueprint as Controller, request

from service import {upper_name}Service
from common import Result
from decorator import has_authority, operate_log

{underline_name}_controller = Controller("{underline_name}", __name__, url_prefix='{url_name}')

@{underline_name}_controller.route("/list", methods=['GET'])
@has_authority("{auth_name}:list")
def list():
    return Result.ok({upper_name}Service().list())

@{underline_name}_controller.route("/page", methods=["GET"])
@has_authority("{auth_name}:page")
def page():
    return Result.ok({upper_name}Service().page())

@{underline_name}_controller.route("/<int:id>", methods=['GET'])
@has_authority("{auth_name}:info")
def info(id):
    return Result.ok({upper_name}Service().info(id))

@{underline_name}_controller.route("/", methods=['POST'])
@has_authority("{auth_name}:save")
def save():
    data = request.json
    return Result.ok({upper_name}Service().save(data))

@{underline_name}_controller.route("/", methods=['PUT'])
@has_authority("{auth_name}:update")
def update():
    data = request.json
    return Result.ok({upper_name}Service().update(data))

@{underline_name}_controller.route("/", methods=['DELETE'])
@has_authority("{auth_name}:delete")
def delete():
    data = request.json
    return Result.ok({upper_name}Service().delete(data))
"""

    def run(self):
        model_path = os.path.join(os.getcwd(), f"{self.MODEL_DIR}")
        file_names = self.get_filename_list(model_path)
        for file_name in file_names:
            file_name_split_list = file_name.split("_")
            if file_name_split_list[-1] == f"{self.MODEL_DIR}.py":
                # 判断__init__.py中是否添加了
                # 没有添加，给他追加一下
                underline_name = "_".join(file_name_split_list[:-1])
                upper_name = "".join([item.capitalize() for item in file_name_split_list[:-1]])
                url_name = "/" + "/".join(file_name_split_list[:-1])
                auth_name = ":".join(file_name_split_list[:-1])
                service_file_name = underline_name + f"_{self.SERVICE_DIR}.py"
                controller_file_name = underline_name + f"_{self.CONTROLLER_DIR}.py"

                self.insert_import_model(underline_name, upper_name)
                self.generate_service(upper_name, service_file_name)
                self.insert_import_service(underline_name, upper_name)
                if not (underline_name + "_" + self.CONTROLLER_DIR) in self.CONTROLLER_IGNORE:
                    self.generate_controller(controller_file_name, upper_name, underline_name, url_name, auth_name)
                    self.insert_import_controller(underline_name, upper_name)

    def get_filename_list(self, folder_path):
        file_names = []
        for root, dirs, files in os.walk(folder_path):
            # 跳过__pycache__文件夹下的内容
            if "__pycache__" in root:
                continue
            for file in files:
                # 排除文件名为 "__init__.py" 的文件
                if file != '__init__.py' and file != 'sys_base_model.py':
                    file_names.append(file)
        return file_names

    def insert_import_model(self, underline_name, upper_name):
        model_init_path = os.path.join(os.getcwd(), f"{self.MODEL_DIR}/__init__.py")
        import_statement = f"\nfrom .{underline_name}_model import {upper_name}Model as {upper_name}Model\n"
        with open(model_init_path, "r", encoding="utf-8") as file:
            content = file.read()
        # 使用正则表达式检查是否已经导入
        pattern = re.compile(
            f"from\\s+\\.{underline_name}_model\\s+import\\s+{upper_name}Model\\s+as\\s+{upper_name}Model")
        if not pattern.search(content):
            with open(model_init_path, "a") as file:
                file.write(import_statement)

    def insert_import_service(self, underline_name, upper_name):
        model_init_path = os.path.join(os.getcwd(), f"{self.SERVICE_DIR}/__init__.py")
        import_statement = f"\nfrom .{underline_name}_service import {upper_name}Service as {upper_name}Service\n"
        with open(model_init_path, "r", encoding="utf-8") as file:
            content = file.read()
        # 使用正则表达式检查是否已经导入
        pattern = re.compile(
            f"from\\s+\\.{underline_name}_service\\s+import\\s+{upper_name}Service\\s+as\\s+{upper_name}Service")
        if not pattern.search(content):
            with open(model_init_path, "a") as file:
                file.write(import_statement)

    def insert_import_controller(self, underline_name, upper_name):
        model_init_path = os.path.join(os.getcwd(), f"{self.CONTROLLER_DIR}/__init__.py")
        import_statement = f"\nfrom .{underline_name}_{self.CONTROLLER_DIR} import {underline_name}_{self.CONTROLLER_DIR} as {underline_name}_{self.CONTROLLER_DIR}\n"
        with open(model_init_path, "r", encoding="utf-8") as file:
            content = file.read()
        # 使用正则表达式检查是否已经导入
        pattern = re.compile(
            f"from\\s+\\.{underline_name}_{self.CONTROLLER_DIR}\\s+import\\s+{underline_name}_{self.CONTROLLER_DIR}\\s+as\\s+{underline_name}_{self.CONTROLLER_DIR}")
        if not pattern.search(content):
            with open(model_init_path, "a") as file:
                file.write(import_statement)

    def generate_service(self, upper_name, file_name):
        file_path = os.path.join(os.getcwd(), f"{self.SERVICE_DIR}/{file_name}")
        # 判断文件是否存在，不存在则创建
        if not os.path.exists(file_path):
            # 文件不存在，创建文件并填充内容
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.get_service_template(upper_name))

    def generate_controller(self, file_name, upper_name, underline_name, url_name, auth_name):
        file_path = os.path.join(os.getcwd(), f"{self.CONTROLLER_DIR}/{file_name}")
        # 判断文件是否存在，不存在则创建
        if not os.path.exists(file_path):
            # 文件不存在，创建文件并填充内容
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(self.get_controller_template(upper_name, underline_name, url_name, auth_name))


if __name__ == '__main__':
    CodeGenerator().run()
