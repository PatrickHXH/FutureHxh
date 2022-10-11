import time
from django.core import signing
import hashlib
from django.core.cache import cache


HEADER = {'typ': 'JWP', 'alg': 'default'}
KEY = 'HUANG_XIA_HAN'
SALT = 'seldomplatform'
TIME_OUT = 1440 * 60  # 300min

class Error:
    '''
    定义错误码与错误信息
    '''
    USER_OR_PAWD_NULL = {"10010":"用户名或密码为空"}
    USER_OR_PAWD_EROOR={"10011":"用户名或密码错误"}
    PAWD_ERROR = {"10012":"两次密码不一致"}
    USER_EXIST = {"10013":"用户已被注册"}

    USER_OR_PAWD_OR_SERVER_ERROR = {"10014":"请填写正确的邮箱、授权码、服务器"}
    DATE_FORMAT_ERROR = {"10015":"日期格式错误,正确例子：xxxx-xx-xx"}
    REPORT_LIST_NONE ={"10016":"没有查询到报告"}
    SEARCH_REPORT_TIME_BEYOND ={"10017":"超出查询范围，只允许查询≤90天"}
    SOURCE_OR_DATE_ERROR = {"10018":"来源或日期格式错误"}

def response(success:bool = True, error = None, result=[]):
    if error is None:
        error_code = ""
        error_msg = ""
    else:
        success = False
        error_code = list(error.keys())[0]
        error_msg = list(error.values())[0]
    '''
    定义统一返回格式
    '''
    resp_dict = {
        "success":success,
        "error":{
            "code":error_code,
            "msg":error_msg
        },
        "result" : result
    }
    return resp_dict


class TokenMethod:
    #加密
    def encrypt(obj):
        """加密"""
        value = signing.dumps(obj, key=KEY, salt=SALT)
        value = signing.b64_encode(value.encode()).decode()
        return value

    #解密
    def decrypt(src):
        """解密"""
        src = signing.b64_decode(src.encode()).decode()
        raw = signing.loads(src, key=KEY, salt=SALT)
        print(type(raw))
        return raw

    #生成token
    def create_token(username):
        """生成token信息"""
        # 1. 加密头信息
        header = TokenMethod.encrypt(HEADER)
        # 2. 构造Payload
        payload = {"username": username, "iat": time.time()}
        payload = TokenMethod.encrypt(payload)
        # 3. 生成签名
        md5 = hashlib.md5()
        md5.update(("%s.%s" % (header, payload)).encode())
        signature = md5.hexdigest()
        token = "%s.%s.%s" % (header, payload, signature)
        # 存储到缓存中
        cache.set(username, token, TIME_OUT)
        return token

    #获取参数
    def get_payload(token):
        payload = str(token).split('.')[1]
        payload = TokenMethod.decrypt(payload)
        return payload


    # 通过token获取用户名
    def get_username(token):
        payload = TokenMethod.get_payload(token)
        return payload['username']
        pass

    #检查token是否有效
    def check_token(token):
        username = TokenMethod.get_username(token)
        last_token = cache.get(username)
        if last_token:
            return last_token == token
        return False