import os
import logging
import eventlet
import json
import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, redirect, url_for
from flask_session import Session
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import jsonify, request
import paho.mqtt.publish as publish
import random
from text_classification_predict import TextClassificationPredict
from datetime import date,timedelta
from datetime import datetime
import datetime
import re
import time

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'  # use the free broker from HIVEMQ
app.config['MQTT_BROKER_PORT'] = 1883  # default port for non-tls connection
app.config['MQTT_USERNAME'] = ''  # set the username here if you need authentication for the broker
app.config['MQTT_PASSWORD'] = ''  # set the password here if the broker demands authentication
app.config['MQTT_KEEPALIVE'] = 5  # set the time interval for sending a ping to the broker to 5 seconds
app.config['MQTT_TLS_ENABLED'] = False  # set TLS to disabled for testing purposes
engine = create_engine("mysql://root:abcdef1234@localhost/SBS", pool_size=20, max_overflow=0)
db = scoped_session(sessionmaker(bind=engine))
GREETING = ["hi", u"chào bạn", u"*gật đầu*", u"Rất vui được nói chuyện với bạn", u"Hello", u'chào']
BYE = ["Goodbye!", "Byeee!"]

# Check for environment variable
# if not os.getenv("DATABASE_URL"):
#     raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
# engine = create_engine(os.getenv("DATABASE_URL"))
# db = scoped_session(sessionmaker(bind=engine))

mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/validate',methods=['POST'])
def validate():
    username = request.form['username']
    password = request.form['password']
    print(username)
    if (username == 'user' and password == '1234'):
        msg = 'Success'
    else:
        msg = 'Falied'
    return msg

@app.route('/home')
def home():
    return render_template('dashboard.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# @app.route('/ui-forms')
# def ui_forms():
#     return render_template('ui-forms.html')

@app.route('/reservation')
def reservation():
    return render_template('book_room.html')

@app.route("/book", methods=['POST'])
def book():
    data = request.form
    db.execute("INSERT INTO reservation VALUES (0,"+data["room_id"]+","+data["period"]+",'truong','"+data["date"]+"')")
    db.commit()
    return render_template('book_room.html')

@app.route("/bookroom", methods=['POST'])
def book_room():
    data = request.form
    date = data["date"]
    period = data["period"]
    rooms = db.execute("SELECT * FROM room")
    json_data=[]
    for room in rooms:
        json_data.append(room["room_id"])

    booked_rooms = db.execute("SELECT * FROM reservation WHERE date='"+date+"' AND period="+period)
    for r in booked_rooms:
        if r["room_id"] in json_data:
            json_data.remove(r["room_id"])
    print(json_data)
    return jsonify(json_data)

@app.route("/set_threshold", methods=['POST'])
def set_threshold():
    data = request.form
    # print(data["light_threshold"])
    # print(data["temp_threshold"])
    # print(data["room_id"])
    # print(type(data["light_threshold"]))
    # print(data["room_id"])
    if data["light_threshold"]:
        db.execute("UPDATE room SET light_threshold="+data["light_threshold"]+" WHERE room_id="+ data["room_id"])
        db.commit()
    if data["temp_threshold"]:
        db.execute("UPDATE room SET temp_threshold="+data["temp_threshold"]+" WHERE room_id="+ data["room_id"])
        db.commit()
    return redirect("/settings")

@app.route("/search-room")
def search_room():
    # global current_user
    # if current_user == 'Guest':
    #     return "Please login"
    return render_template("search_room.html")

@app.route("/chat")
def chat():
    # global current_user
    # if current_user == 'Guest':
    #     return "Please login"
    return render_template("chat.html")

@app.route("/device-control")
def search_room_2():
    # global current_user
    # if current_user == 'Guest':
    #     return "Please login"
    return render_template("device-control.html")

@app.route('/get_result', methods=["POST"])
def get_result():
    # floor = int(request.form.get("floor"))
    room = int(request.form.get("room_id"))
   
    try:
        items = db.execute(f"SELECT * FROM device WHERE room_id = {room}").fetchall()
    finally:
        db.close()
    json_data=[]
    # for result in rv:
    #     json_data.append(dict(zip(row_headers,result)))
    # return jsonìy(json_data)
    # return jsonify(rooms)
    for item in items:
        # json_data.append(dict(zip("room_id",room)))
        device = {'device_id': item["device_id"], 'device_name': item["device_name"], 'status': item['status'], 'floor': item['floor'], 'room_id': item['room_id']}
        json_data.append(device)
    print(json_data)
    return jsonify(json_data)
    # return render_template('control_device.html', items=items)

@app.route('/get_toggled_status') 
def toggled_status():
    device_id = request.args.get('device_id')
    current_status = request.args.get('status')
    name = request.args.get('name')
    print('Name:', name)
    if current_status != "" and current_status in ["On", "Off"]:
        light = 'OFF' if current_status == 'Off' else 'ON'
        value = 0 if current_status == 'Off' else 1
        print(light)
        print(device_id)
        # split_data = topic.split('/')
        p_data = {}
        if 'Light' in name:
            topic = 'Topic/light'
        elif 'Air' in name:
            topic = 'Topic/temp'
        p_data["device_id"] = device_id
        p_data["value"] = light
        data1 = json.dumps([p_data])
        publish.single(topic, data1, hostname="broker.hivemq.com")


        try:
            db.execute(f"UPDATE device SET status = {value} WHERE device_id = {device_id}")
            db.commit()
            print('Update sucessfully')
        finally:
            db.close()
        return jsonify({"success": True,
                        "msg": "Done"})
    else:
        print('Please try')
        return jsonify({"success": False,
                        "msg": "Done"})

@app.route("/lookuprooms")
def lookup_rooms():
    rooms = db.execute("SELECT * FROM room")
    # row_headers=[x[0] for x in rooms.description] #this will extract row headers
    # rv = rooms.fetchall()
    json_data=[]
    # for result in rv:
    #     json_data.append(dict(zip(row_headers,result)))
    # return jsonìy(json_data)
    # return jsonify(rooms)
    for room in rooms:
        # json_data.append(dict(zip("room_id",room)))
        json_data.append(room["room_id"])
    print(json_data)
    return jsonify(json_data)

# @mqtt.on_connect()
# def handle_connect(client, userdata, flags, rc):
#     #Sub 2 chosen topics 
#     print('on connect')
#     mqtt.subscribe('Topic/TempHumi')
#     mqtt.subscribe('Topic/Mois')

# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, message):
#     topic=message.topic    
#     #data = handle_message(message)
#     print('topic')
#     print('topic123')
#     print('topic214')
#     print(message.payload.decode())
#     print(topic)
#     print(client)
#     print(userdata)
#     print(message)
#     mqtt.publish('Topic/TempHumi','Hello World this is payload')


def handle_message(message):
    payload=json.loads(message.payload.decode())
    data = dict()
    if message.topic == "Topic/TempHumi":
        data = dict(
        temp= payload[0]["values"][0],
        humid= payload[0]["values"][1],
    )
    if message.topic == "Topic/Mois":
        data = dict(
            mois = payload[0]["values"][0],
        )        
    return data

@socketio.on('publish')
def handle_publish(json_str):
    data = json.loads(json_str)
    mqtt.publish(data['topic'], data['message'])
    # print('publish')

@socketio.on('subscribe')
def handle_subscribe(json_str):
    data = json.loads(json_str)
    mqtt.subscribe(data['topic'])
    # print('subcribe')

@socketio.on('unsubscribe')
def handle_unsubscribe(json_str):
    data = json.loads(json_str)
    mqtt.unsubscribe(data['topic'])

@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    data = dict(
        topic=message.topic,
        payload=json.loads(str(message.payload.decode()))
    )
    socketio.emit('mqtt_message', data=data)

# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, message):
#     data = dict(
#         topic=message.topic,
#         payload=message.payload.decode()
#     )
#     room = data['topic'].split("-")[1]
#     print(room)

#     socketio.emit('mqtt_message', data=data)
#     # print(data.payload)
#     if int(data['payload']) > 50:
#         db.execute("""UPDATE device SET status=0 WHERE room_id=:room""", {"room":room})
#         db.commit()
#         data1 = json.loads('{"topic": "' + "light-" + room + '", "message": "' + "0" + '"}')
#         mqtt.publish(data1['topic'], data1['message'])

@app.route("/get",methods=['POST'])
def get_bot_response():
    userText = request.form.get("message")  # get data from input,we write js  to index.html
    # return "BOt:" +str(english_bot.get_response(userText))
    print(userText)
    tcp = TextClassificationPredict()
    a = tcp.get_train_data({"feature": userText})
    error=jsonify({"action":"print", "message":"Sorry, I dont understand!"})
    if a == "chao_hoi":
        c=random.choice(GREETING)
        c += ' Tôi giúp gì được cho bạn ?'
        return render_template('chat.html', mess=c)
    elif a == "sd":
        c = ''
        c += 'Bạn có thể yêu cầu tôi chuyển qua phần khác như: device control, dashboard, setting, … hay bạn có thể yêu cầu tôi cho coi tiêu thụ điện đã sử dụng của từng tầng, từng phòng theo ngày, ví dụ: xem tiêu thụ điện tầng 2 ngày 15/12/2020.'
        return render_template('chat.html', mess=c)
    elif a == "bye":
        c=random.choice(BYE)
        return jsonify({"action": "print", "message":c})
    elif a == "hoi_thoi_tiet":
        return jsonify({"action":"weather"})
    elif a== "user_list":
        return jsonify({"action":"redirected","destination":"user_list"})
    elif a== "profile":
        return redirect('/user_profile')
    elif a == "settings":
        return redirect('/settings')
    elif a == "dashboard":
        return redirect('/dashboard')
    elif a=="report_all":
        return jsonify({"action": "redirected", "destination": "report"})
    elif a=="control":
        return redirect('/device-control')
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
        # da_te=get_time(userText)
        # return return_electric_useage(da_te)
        building,floor,room,da_te,fr_om,t_o=extract_info(userText)
        return electrical_consumption(floor, room, da_te, fr_om, t_o)
    else:
        return error
########################################################################################################################
def return_electric_useage(a):
    if a == "hôm nay" or a=="ngày hôm nay":
        dt = date.today()
        midnight = datetime.combine(dt, datetime.min.time()).timestamp()
        end_of_day = datetime.combine(dt, datetime.max.time()).timestamp()
        #return jsonify({"action": "Electric_Consumption","from": str(midnight), "to": str(end_of_day)})
        items = db.execute(f"SELECT * FROM device WHERE room_id = 1").fetchall()
        return render_template('chat.html', items=items)
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

def electrical_consumption(floor, room, da_te, from_date, to_date):
    if room == None:
        room = 'room'
    else:
        room = int(room)
    if floor == None:
        floor = 'floor'
    else:
        floor = int(floor)
        
    print('info::::', floor, room, da_te, from_date, to_date)
    if da_te == 'đến nay' or da_te == 'từ qua đến nay' or da_te == 'từ hôm qua đến hôm nay':
        from_dt = datetime.datetime.strptime(from_date, '%d/%m/%Y')
        to_dt = datetime.date.today()
        items = db.execute(f"SELECT * FROM electric_consumption WHERE date >= '{from_dt}' and date <= '{to_dt}' and floor = {floor} and room = {room}").fetchall()
        print(items)
        return render_template('chat.html', items=items)
    elif da_te == 'đến hôm qua':
        from_dt = datetime.datetime.strptime(from_date, '%d/%m/%Y')
        to_dt = datetime.date.today() - timedelta(days=1)
        items = db.execute(f"SELECT * FROM electric_consumption WHERE date >= '{from_dt}' and date <= '{to_dt}' and floor = {floor} and room = {room}").fetchall()
        print(items)
        return render_template('chat.html', items=items)
    elif da_te == "hôm nay" or da_te =="ngày hôm nay" or da_te == "bây giờ" or da_te =="hiện tại":
        dt = datetime.date.today()
        items = db.execute(f"SELECT * FROM electric_consumption WHERE date = '{dt}' and floor = {floor} and room = {room}").fetchall()
        print(items)
        return render_template('chat.html', items=items)
    elif da_te == "hôm qua" or da_te =="ngày hôm qua":
        dt = datetime.date.today() - timedelta(days=1)
        items = db.execute(f"SELECT * FROM electric_consumption WHERE date = '{dt}' and floor = {floor} and room = {room}").fetchall()
        return render_template('chat.html', items=items)
    elif to_date == None and da_te != None:
        dt = datetime.datetime.strptime(da_te, '%d/%m/%Y')
        items = db.execute(f"SELECT * FROM electric_consumption WHERE date = '{dt}' and floor = {floor} and room = {room}").fetchall()
        return render_template('chat.html', items=items)
    elif to_date != None and da_te != None:
        from_dt = datetime.datetime.strptime(from_date, '%d/%m/%Y')
        to_dt = datetime.datetime.strptime(to_date, '%d/%m/%Y')
        items = db.execute(f"SELECT * FROM electric_consumption WHERE date >= '{from_dt}' and date <= '{to_dt}' and floor = {floor} and room = {room}").fetchall()
        return render_template('chat.html', items=items)
    elif da_te == None:
        items = db.execute(f"SELECT * FROM electric_consumption WHERE floor = {floor} and room = {room}").fetchall()
        return render_template('chat.html', items=items)
    else:
        pass

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

# def get_input(b, a):
#     if a in b:
#         b = b.split(a)
#         b = b[1].split(' ', 3)
#         return b[1]
#     else:
#         return None
# def get_time(b):
#     arr = ["hôm nay", "hôm qua", "bây giờ","hiện tại"]
#     for x in arr:
#         if x in b:
#             return x
#     matches = re.findall('(\d{2}[-/](\d{2})[-/]\d{2,4})', b)
#     if matches:
#         for match in matches:
#             return match[0]
#     else:
#         return None

# def extract_info(b):
#     building = get_input(b, "tòa")
#     floor = get_input(b, "tầng")
#     room = get_input(b, "phòng")
#     m="thiết bị"
#     n="cảm biến"
#     date = get_time(b)
#     if n in b:
#         type="sensor"
#         a = get_input(b, "cảm biến")
#         if a in date:
#             type_id=None
#         else:
#             type_id=a
#     elif m in b:
#         type="device"
#         a = get_input(b, "thiết bị")
#         if a in date:
#             type_id = None
#         else:
#             type_id = a
#     else:
#         type=None
#         type_id = None
#     if date is None:
#         fr_om=None
#         t_o=None
#     else:
#         fr_om = get_input(b, "từ")
#         t_o = get_input(b, "đến")
#     return building, floor, room,type,type_id, date, fr_om, t_o

def get_input(b, a):
    if a in b:
        b = b.split(a)
        b = b[1].split(' ', 3)
        return b[1]
    else:
        return None
def get_time(b):
    arr = ['đến nay','từ qua đến nay' ,'từ hôm qua đến hôm nay','đến hôm qua',"hôm nay", "hôm qua" , "bây giờ", "hiện tại"]
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
    floor = get_input(b, "tầng")
    room = get_input(b, "phòng")
    date = get_time(b)
    if date is None:
        fr_om,t_o=None, None
    else:
        fr_om, t_o = get_date(b)

    return building, floor, room, date, fr_om, t_o

def get_date(b):
    matches = re.findall('(\d{1,2}[-/](\d{1,2})[-/]\d{2,4})', b)
    if len(matches) == 2:
        return matches[0][0] , matches[1][0]
    elif len(matches) == 1:
        return matches[0][0], None
    else:
        return None, None

# @mqtt.on_message()
# def handle_mqtt_message(client, userdata, message):
#     data = dict(
#         topic=message.topic,
#         payload=message.payload.decode()
#     )
#     room = data['topic'].split("-")[1]
#     print(room)

#     socketio.emit('mqtt_message', data=data)
#     # print(data.payload)
#     if int(data['payload']) > 50:
#         db.execute("""UPDATE device SET status=0 WHERE room_id=:room""", {"room":room})
#         db.commit()
#         data1 = json.loads('{"topic": "' + "light-" + room + '", "message": "' + "0" + '"}')
#         mqtt.publish(data1['topic'], data1['message'])

if __name__ == '__main__':
    app.run(debug=True)
