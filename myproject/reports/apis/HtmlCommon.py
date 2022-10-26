import os
from bs4 import BeautifulSoup  #pip install BeautifulSoup4
import bs4.element
from myproject.settings import BASE_DIR

#判断测试报告是否存在失败
def Exist_Fail(Test_Path):
    with open(Test_Path,"r") as f:
        soup = BeautifulSoup(f,'html.parser')
        text_warning = soup.find("span",class_="badge badge-pill bg-soft-warning text-warning me-2")
        text_danger= soup.find("span",class_="badge badge-pill bg-soft-danger text-danger me-2")
        if "失败:0" in text_warning and "错误:0" in text_danger:
            return False
        else:
            return True
