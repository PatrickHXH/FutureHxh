a = "测试报告2022-10-10 092633"
b = a.split()[-1]
str_list =list(b)
str_list.insert(2,":")
str_list.insert(5,":")
str = ''.join(str_list)
str = "2022-10-10"+" "+str
print(str)