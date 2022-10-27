import datetime
import poplib
from email.parser import Parser
# 解码头部
from email.header import decode_header
# 解析地址
from email.utils import parseaddr
import os
import time

class email:
    #连接邮箱
    def email_login(email_user,password,pop3_server):
        #连接服务器
        server = poplib.POP3(pop3_server)
        # server.utf8()
        #打开调试信息，这里设置为打开，会在控制台输出与pop3服务器交互信息
        server.set_debuglevel(1)
        #输出pop3服务器的欢迎文字，验证是否正确连接到邮件服务器
        print(server.getwelcome().decode('utf-8'))
        #开始身份验证
        server.user(email_user)
        server.pass_(password)
        # num,size = server.stat()
        # print("邮件id数：",num)
        return server

    #根据id获取邮件原始文本
    def get_origin_text(id:int,email_user,password,pop3_server): #
        server = email.email_login(email_user,password,pop3_server)
        resp, lines, octets= server.retr(id)
        msg_content = b'\r\n'.join(lines).decode('utf-8')
        msg = Parser().parsestr(msg_content)
        return  msg

    #解码字符串
    def decode_str(s):
        value,charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    # 设置字符集
    def set_charset(msg):
        charset = msg.get_charset() # 获取字符集
        if charset is None:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    #解析邮件
    def parse_msg(msg):
        parse_msg_dict = {}
        #解析时间
        Received = msg.get("Received",'')
        date = Received.split(',')[-1]
        a = time.strptime(date, ' %d %b %Y %H:%M:%S %z')
        date = str(a.tm_year)+"-"+str(a.tm_mon)+"-"+str(a.tm_mday)
        parse_msg_dict["Date"] = date
        #解析邮件头
        for header in ['From','To','Subject']:  # 遍历获取发件人，收件人，主题的相关信息
            value = msg.get(header,'')  #获取遍历的相应内容
            if value:
                if header == 'Subject':
                    value = email.decode_str(value)   #解码字符串
                    parse_msg_dict["Subject"] = value
                if header == 'From':
                    hdr,addr = parseaddr(value)   #解析邮件地址
                    name = email.decode_str(hdr)  #解码字符串
                    value = '%s <%s>'%(name,addr)
                    parse_msg_dict["From"] = value
                if header =='To':
                    hdr,addr = parseaddr(value)   #解析邮件地址
                    name = email.decode_str(hdr)  #解码字符串
                    value = '%s <%s>' % (name, addr)
                    parse_msg_dict["To"] = value
            # print('%s: %s'%(header,value))
        # 解析邮件正文
        if (msg.is_multipart()): # 如果消息由多个部分组成，则返回True
            parts = msg.get_payload() #返回一个包含邮件所有子对象的列表
            for n,part in enumerate(parts):
                # print('part %s'%(n))
                content_type = part.get_content_type()  #获取邮件信息内容
                if "text/plain" in content_type or 'text/html' in content_type:  # 如果是纯文本或者html类型
                    content = part.get_payload(decode=True)  # 返回一个包含邮件所有的子对象(已解码)的列表
                    charset = email.set_charset(part)  # 设置字符集
                    if charset:  # 字符集不为空
                        content = content.decode(charset)  # 解码
                    parse_msg_dict["Text"] = content
                    # print('Text: %s' % (content))
                else:
                    # print('Attachment: %s' % (content_type))  # 附件
                    parse_msg_dict["Attachment"] = content_type

        return parse_msg_dict

    #下载附件
    def save_att_file(msg,save_path):
        for part in msg.walk():
            file_name = part.get_filename()
            print("filename:",file_name)
            attachment_files = []
            if file_name:
                file_name = email.decode_str(file_name )
                data = part.get_payload(decode=True)
                att_file = open(os.path.join(save_path,file_name), 'wb')
                attachment_files.append(file_name)
                att_file.write(data)
                att_file.close()
                print(f"附件 {file_name} 下载完成")
                return  file_name
        if file_name is None:
            return None

    #查询邮箱报告
    def get_reportlist(source,time,email_user,password,pop3_server):
        #获取每个id，拿每个id得到邮件内容，再判断时间和关键在不在邮箱内容里，如果在就返回id 和整个邮箱内容
        # now = datetime.datetime.now().strftime("%Y-%m-%d")
        server = email.email_login(email_user,password,pop3_server)
        email_num,email_size =server.stat()
        reportlist = []
        j = 0
        for i in range(email_num,69,-1):
            j = j + 1
            list = []
            if j==21:
                return reportlist
            msg = email.get_origin_text(i,email_user,password,pop3_server)
            analysis_msg = email.parse_msg(msg)
            if "Text" not  in analysis_msg.keys() or "Subject"not  in analysis_msg.keys() or "测试报告" not in analysis_msg["Subject"] :
                continue
            if  source in analysis_msg["Text"] and time in analysis_msg["Date"]:
                analysis_msg["email_code"] = i
                list = [i,analysis_msg]
                reportlist.append(list)
                break
        return reportlist[-1][-1]

    #获取邮箱id数，大小
    def get_email_info(email_user,password,pop3_server):
        server = email.email_login(email_user,password,pop3_server)
        email_num,email_size =server.stat()
        return email_num,email_size