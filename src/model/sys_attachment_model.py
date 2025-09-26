from sqlalchemy import BigInteger, String, Column

from .base_model import BaseModel


class SysAttachmentModel(BaseModel):
    __tablename__ = "sys_attachment"

    name = Column(String(255), nullable=False, comment="附件名称")
    url = Column(String(255), nullable=False, comment="附件地址")
    size = Column(BigInteger, comment="附件大小")
    platform = Column(String(50), comment="存储平台")
