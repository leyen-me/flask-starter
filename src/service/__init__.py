from .base_service import BaseService as BaseService

# =========================================中间表START=========================================#
from .sys_file_upload_service import SysFileUploadService as SysFileUploadService
from .sys_user_role_service import SysUserRoleService as SysUserRoleService
from .sys_user_post_service import SysUserPostService as SysUserPostService
from .sys_role_menu_service import SysRoleMenuService as SysRoleMenuService
from .sys_role_data_scope_service import SysRoleDataScopeService as SysRoleDataScopeService
from .sys_log_login_service import SysLogLoginService as SysLogLoginService
from .sys_log_operate_service import SysLogOperateService as SysLogOperateService
# =========================================中间表E N D=========================================#



# =========================================主 表START=========================================#
from .sys_params_service import SysParamsService as SysParamsService
from .sys_captcha_service import SysCaptchaService as SysCaptchaService
from .sys_dict_type_service import SysDictTypeService as SysDictTypeService
from .sys_dict_data_service import SysDictDataService as SysDictDataService

from .sys_org_service import SysOrgService as SysOrgService
from .sys_post_service import SysPostService as SysPostService
from .sys_user_service import SysUserService as SysUserService
from .sys_role_service import SysRoleService as SysRoleService
from .sys_menu_service import SysMenuService as SysMenuService
from .sys_attachment_service import SysAttachmentService as SysAttachmentService

from .sys_auth_service import SysAuthService as SysAuthService
# =========================================主 表E N D=========================================#