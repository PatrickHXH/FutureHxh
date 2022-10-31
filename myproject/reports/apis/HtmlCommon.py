import os
from bs4 import BeautifulSoup  #pip install BeautifulSoup4
import bs4.element
from myproject.settings import BASE_DIR

#判断测试报告是否存在失败
def Exist_Fail(Test_Path):
    with open(Test_Path,"r") as f:
        soup = BeautifulSoup(f,'html.parser')
        text = soup.find_all(text=True)
        if  "失败:0" not in text or "错误:0" not in text:
            return True
        else:
            return False
