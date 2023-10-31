import os
import uuid

from model import SysAttachmentModel
from config import CONFIG


class SysFileUploadService():

    def upload(self, files):
        if 'file' in files:
            file = files['file']
            file_name = str(uuid.uuid4()) + os.path.splitext(file.filename)[-1]
            file_folder = os.path.join(CONFIG['APP']['STATIC_FOLDER'])
            file_path = os.path.join(os.getcwd(), file_folder, file_name)
            file.save(file_path)
            return SysAttachmentModel(name=file.filename, url=f"/static/{file_name}", size=os.path.getsize(file_path),
                                      platform='LOCAL')
