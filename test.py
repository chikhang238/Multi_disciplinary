import re

b = "Xem tiêu thụ điện từ ngày 2/12/2020"
x = 'tầng'




# mystring =  "hi my name is ryan, and i am new to python and would like to learn more"
# keyword = 'name'
# before_keyword, keyword, after_keyword = mystring.partition(keyword)
# print(before_keyword)
# arr = after_keyword.split(" ", 3)
# print(arr[1])
import re
from datetime import datetime, date
import datetime

def get_input(b, a):
    if a in b:
        b = b.split(a)
        b = b[1].split(' ', 3)
        return b[1]
    else:
        return None

def get_date(b):
    matches = re.findall('(\d{1,2}[-/](\d{1,2})[-/]\d{2,4})', b)
    if len(matches) == 2:
        return matches[0][0] , matches[1][0]
    elif len(matches) == 1:
        return matches[0][0], None
    else:
        return None, None

def get_time(b):
    arr = ["hôm nay", "hôm qua"]
    for x in arr:
        if x in b:
            return x
    matches = re.findall('(\d{1,2}[-/](\d{1,2})[-/]\d{2,4})', b)
    if matches:
        for match in matches:
            return match[0]
    else:
        return None

def extract_info(b):
    building = get_input(b, "tòa")
    print('BBBBBBBB', building)
    floor = get_input(b, "tầng")
    print('BBBBBBBB', floor)
    room = get_input(b, "phòng")
    print('BBBBBBBB', room)
    date = get_time(b)
    print('BBBBBBBB', date)
    if date is None:
        fr_om,t_o=None, None
    else:
        fr_om, t_o = get_date(b)
    print('BBBBBBBB', fr_om)
    print('BBBBBBBB', t_o)
    return building, floor, room, date, fr_om, t_o
# m="thiết bị"
# n="cảm biến "
# test_time=get_time(b)
# if m in b:
#     print(19999)
#     a = get_input(b,"thiết bị")
#     if a in test_time:
#         print("abc")
#     else:
#         print(a)
# elif n in b:
#     print(29999)
#     a = get_input(b, "cảm biến")
#     if a in test_time:
#         print("abc")
#     else:
#         print(a)

#print(get_input(b,"thiết bị"))
building, floor, room, da_te, fr_om, t_o = extract_info(b)
print(building, floor, room, da_te, fr_om, t_o)
# print(type(fr_om))
# f = datetime.datetime.strptime(fr_om, '%d/%m/%Y')
# print(type(f))
# print(f)
# print(date.today())
print(type(room))