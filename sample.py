from flask import Flask, render_template, request, jsonify
import random
from text_classification_predict import TextClassificationPredict
from datetime import date,timedelta
from datetime import datetime
import re


app = Flask(__name__)
GREETING = ["hi", u"chào bạn", u"*gật đầu*", u"Rất vui được nói chuyện với bạn", u"Chào, tôi có thể giúp gì cho bạn không?"]
BYE = ["Goodbye!", "Byeee!"]
import time


@app.route("/")
def index():
    return render_template("index.html")  # to send context to html


##############################


@app.route("/get",methods=['POST'])
def get_bot_response():
    userText = request.form.get("message")  # get data from input,we write js  to index.html
    # return "BOt:" +str(english_bot.get_response(userText))
    tcp = TextClassificationPredict()
    a = tcp.get_train_data({"feature": userText})
    error=jsonify({"action":"print", "message":"Sorry, I dont understand!"})
    if a == "chao_hoi":
        c=random.choice(GREETING)
        return jsonify({"action": "print", "message": c})
    elif a == "bye":
        c=random.choice(BYE)
        return jsonify({"action": "print", "message":c})
    elif a == "hoi_thoi_tiet":
        return jsonify({"action":"weather"})
    elif a== "user_list":
        return jsonify({"action":"redirected","destination":"user_list"})
    elif a== "profile":
        return jsonify({"action": "redirected", "destination": "profile"})
    elif a == "settings":
        return jsonify({"action":"redirected","destination":"settings"})
    elif a == "dashboard":
        return jsonify({"action": "redirected", "destination": "dashboard"})
    elif a=="report_all":
        return jsonify({"action": "redirected", "destination": "report"})
    elif a == "report_detail":
        building,floor,room,type,type_id,da_te,fr_om,t_o=extract_info(userText)
        if building is None and (floor is not None or room is not None or type_id is not None):
            return jsonify({"action":"print", "message":"Không tìm thông tin nào hợp lệ, vui lòng nhập lại(ví dụ: "
                                                        "tòa A4 tầng 3 phòng 10 (thiết bị/cảm biến A504) ngày 25/07/2020 từ 12:00:00 đến "
                                                        "14:00:00 )"})
        elif (building is None or floor is None) and room is not None:
            return jsonify({"action":"print", "message":"Không tìm thấy tòa hoặc tầng hợp lệ, vui lòng nhập thêm(ví dụ: "
                                                        "tòa A4 tầng 3 phòng 10 (thiết bị/cảm biến A504) ngày 25/07/2020 từ 12:00:00 đến "
                                                        "14:00:00 )"})
        elif building is not None and floor is None and room is not None:
            return jsonify({"action":"print", "message":"Không tìm thấy tầng nhà nào hợp lệ, vui lòng nhập thêm(ví dụ: "
                                                        "tòa A4 tầng 3 phòng 10 (thiết bị/cảm biến A504) ngày 25/07/2020 từ 12:00:00 đến "
                                                        "14:00:00 )"})
        elif room is None and type_id is None and building is None and floor is None and da_te is None:
            return jsonify(
                {"action": "print", "message": "Vui lòng nhập thêm thông tin(ví dụ: "
                                               "tòa A4 tầng 3 phòng 10 (thiết bị/cảm biến A504) ngày 25/07/2020 từ 12:00:00 đến "
                                               "14:00:00 )"})
        elif da_te is not None and fr_om is not None and t_o is None:
            return jsonify(
                {"action": "print", "message": "Không tìm được thời điểm, Vui lòng nhập thêm(ví dụ: "
                                               "tòa A4 tầng 3 phòng 10 (thiết bị/cảm biến A504) ngày 25/07/2020 từ 12:00:00 đến "
                                               "14:00:00 )"})
        elif da_te is not None and fr_om is None and t_o is not None:
            return jsonify(
                {"action": "print", "message": "Không tìm được thời điểm, Vui lòng nhập thêm(ví dụ: "
                                               "tòa A4 tầng 3 phòng 10 (thiết bị/cảm biến A504) ngày 25/07/2020 từ 12:00:00 đến "
                                               "14:00:00 )"})
        else:
            return return_report(building, floor, room,type,type_id,da_te, fr_om, t_o)
    elif a == "kw":
        da_te=get_time(userText)
        return return_electric_useage(da_te)
    else:
        return error
########################################################################################################################
def return_electric_useage(a):
    if a == "hôm nay" or a=="ngày hôm nay":
        dt = date.today()
        midnight = datetime.combine(dt, datetime.min.time()).timestamp()
        end_of_day = datetime.combine(dt, datetime.max.time()).timestamp()
        return jsonify({"action": "Electric_Consumption","from": str(midnight), "to": str(end_of_day)})
    elif a == "bây giờ" or a=="hiện tại":
        ts = time.time()
        return jsonify({"action": "Electric_Consumption","from": str(ts), "to": str(ts)})
    elif a == "hôm qua" or a=="ngày hôm qua":
        dt = date.today() - timedelta(days=1)
        midnight = datetime.combine(dt, datetime.min.time()).timestamp()
        end_of_day = datetime.combine(dt, datetime.max.time()).timestamp()
        return jsonify({"action": "Electric_Consumption","from": str(midnight), "to": str(end_of_day)})
    elif a== None:
        return jsonify({"action": "print", "from": "Vui lòng nhập lại(ví dụ: mở tiêu thụ điện ngày 25/07/2020)"})
    else:
        c = datetime.strptime(str(a), '%d/%m/%Y')
        midnight = datetime.combine(c, datetime.min.time()).timestamp()
        end_of_day = datetime.combine(c, datetime.max.time()).timestamp()
        return jsonify({"action": "Electric_Consumption","from": str(midnight), "to": str(end_of_day)})
def return_report(building, floor, room,type,type_id,da_te,fr_om,t_o):
    if da_te == "hôm nay":
        dt = date.today()
        if fr_om is None and t_o is None:
            midnight = datetime.combine(dt, datetime.min.time()).timestamp()
            end_of_day = datetime.combine(dt, datetime.max.time()).timestamp()
        else:
            midnight = datetime.combine(dt, datetime.strptime(str(fr_om), '%H:%M:%S').time()).timestamp()
            end_of_day = datetime.combine(dt, datetime.strptime(str(t_o), '%H:%M:%S').time()).timestamp()
        return jsonify(
            {"action": "report_detail", "building": building, "floor": floor, "room": room,"type":type,"type_id":type_id,"from": str(midnight),
             "to": str(end_of_day)})
    elif da_te == "bây giờ" or da_te == "hiện tại":
        ts = time.time()
        return jsonify(
            {"action": "report_detail", "building": building, "floor": floor, "room": room,"type":type,"type_id":type_id, "from": str(ts),
             "to": str(ts)})
    elif da_te == "hôm qua":
        dt = date.today() - timedelta(days=1)
        if fr_om is None and t_o is None:
            midnight = datetime.combine(dt, datetime.min.time()).timestamp()
            end_of_day = datetime.combine(dt, datetime.max.time()).timestamp()
        else:
            midnight = datetime.combine(dt, datetime.strptime(str(fr_om), '%H:%M:%S').time()).timestamp()
            end_of_day = datetime.combine(dt, datetime.strptime(str(t_o), '%H:%M:%S').time()).timestamp()
        return jsonify(
            {"action": "report_detail", "building": building, "floor": floor, "room": room,"type":type,"type_id":type_id, "from": str(midnight),
             "to": str(end_of_day)})
    elif da_te == None:
        return jsonify(
            {"action": "report_detail", "building": building, "floor": floor, "room": room,"type":type,"type_id":type_id, "from": None,
             "to": None})
    elif da_te is not None and fr_om is None and t_o is None:
        c = datetime.strptime(str(da_te), '%d/%m/%Y')
        midnight = datetime.combine(c, datetime.min.time()).timestamp()
        end_of_day = datetime.combine(c, datetime.max.time()).timestamp()
        return jsonify(
            {"action": "report_detail", "building": building, "floor": floor, "room": room, "type":type,"type_id": type_id,
             "from": str(midnight), "to": str(end_of_day)})
    else:
        c = datetime.strptime(str(da_te), '%d/%m/%Y')
        midnight = datetime.combine(c, datetime.strptime(str(fr_om), '%H:%M:%S').time()).timestamp()
        end_of_day = datetime.combine(c, datetime.strptime(str(t_o), '%H:%M:%S').time()).timestamp()
        return jsonify(
            {"action": "report_detail", "building": building, "floor": floor, "room": room,"type":type,"type_id":type_id,
             "from": str(midnight), "to": str(end_of_day)})

def get_input(b, a):
    if a in b:
        b = b.split(a)
        b = b[1].split(' ', 3)
        return b[1]
    else:
        return None
def get_time(b):
    arr = ["hôm nay", "hôm qua", "bây giờ","hiện tại"]
    for x in arr:
        if x in b:
            return x
    matches = re.findall('(\d{2}[-/](\d{2})[-/]\d{2,4})', b)
    if matches:
        for match in matches:
            return match[0]
    else:
        return None

def extract_info(b):
    building = get_input(b, "tòa")
    floor = get_input(b, "tầng")
    room = get_input(b, "phòng")
    m="thiết bị"
    n="cảm biến"
    date = get_time(b)
    if n in b:
        type="sensor"
        a = get_input(b, "cảm biến")
        if a in date:
            type_id=None
        else:
            type_id=a
    elif m in b:
        type="device"
        a = get_input(b, "thiết bị")
        if a in date:
            type_id = None
        else:
            type_id = a
    else:
        type=None
        type_id = None
    if date is None:
        fr_om=None
        t_o=None
    else:
        fr_om = get_input(b, "từ")
        t_o = get_input(b, "đến")
    return building, floor, room,type,type_id, date, fr_om, t_o


if __name__ == "__main__":
    app.run(debug=True)
