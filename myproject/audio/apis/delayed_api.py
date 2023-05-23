from ninja import Router
import os
from ninja import File
from ninja.files import UploadedFile
from myproject.settings import MEDIA_DIR
router = Router(tags=["delayed"])

@router.post("/delayedUpload/",auth=None)
def delayed_upload(request,file:UploadedFile=File(...)):
    '''
    延时测试
    '''
    upload_file = os.path.join(MEDIA_DIR,file.name)
    local_file = open(upload_file,"wb")
    for chunk in file.chunks():
        local_file.write(chunk)
    local_file.close()
    print("测试延时")