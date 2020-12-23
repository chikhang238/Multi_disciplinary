
import pandas as pd
from svm  import SVMModel


class TextClassificationPredict(object):
    def __init__(self):
        self.test = None

    def get_train_data(self,a):
        #  train data
        train_data = []
        train_data.append({"feature": u"What's the weather like?", "target": "hoi_thoi_tiet"})
        train_data.append({"feature": u"What's the weather like today?", "target": "hoi_thoi_tiet"})
        train_data.append({"feature": u"Hôm nay mưa không ?", "target": "hoi_thoi_tiet"})
        train_data.append({"feature": u"Hôm nay nắng không ?", "target": "hoi_thoi_tiet"})
        train_data.append({"feature": u"Hôm nay trời có mưa không ?", "target": "hoi_thoi_tiet"})
        train_data.append({"feature": u"Hôm nay trời có nắng không ?", "target": "hoi_thoi_tiet"})
        train_data.append({"feature": u"Thời tiết hôm nay?", "target": "hoi_thoi_tiet"})
        train_data.append({"feature": u"Thời tiết như thế nào?", "target": "hoi_thoi_tiet"})
        train_data.append({"feature": u"Thời tiết", "target": "hoi_thoi_tiet"})
        ################################################################################################################
        train_data.append({"feature": u"mở profile", "target": "profile"})
        train_data.append({"feature": u"coi profile", "target": "profile"})
        train_data.append({"feature": u"vào profile", "target": "profile"})
        train_data.append({"feature": u"tôi muốn mở profile", "target": "profile"})
        train_data.append({"feature": u"profile", "target": "profile"})
        train_data.append({"feature": u"mở thông tin của tôi", "target": "profile"})
        train_data.append({"feature": u"coi thông tin của tôi", "target": "profile"})
        train_data.append({"feature": u"vào thông tin của tôi", "target": "profile"})
        ################################################################################################################
        train_data.append({"feature": u"mở dashboard?", "target": "dashboard"})
        train_data.append({"feature": u"coi dashboard", "target": "dashboard"})
        train_data.append({"feature": u"vào dashboard", "target": "dashboard"})
        train_data.append({"feature": u"tôi muốn mở dashboard", "target": "dashboard"})
        train_data.append({"feature": u"dashboard", "target": "dashboard"})
        train_data.append({"feature": u"mở trang chủ ", "target": "dashboard"})
        train_data.append({"feature": u"về trang chủ", "target": "dashboard"})
        train_data.append({"feature": u"vào trang chủ", "target": "dashboard"})
        ################################################################################################################
        train_data.append({"feature": u"mở settings", "target": "settings"})
        train_data.append({"feature": u"coi settings", "target": "settings"})
        train_data.append({"feature": u"vào settings", "target": "settings"})
        train_data.append({"feature": u"tôi muốn mở settings", "target": "settings"})
        train_data.append({"feature": u"settings", "target": "settings"})
        train_data.append({"feature": u"mở cài đặt", "target": "settings"})
        train_data.append({"feature": u"về cài đặt", "target": "settings"})
        train_data.append({"feature": u"vào cài đặt", "target": "settings"})
        train_data.append({"feature": u"tôi muốn bật settings", "target": "settings"})
        train_data.append({"feature": u"mở setting để thay đổi threshold", "target": "settings"})
        ################################################################################################################
        train_data.append({"feature": u"mở user list", "target": "user_list"})
        train_data.append({"feature": u"mở danh sách người dùng", "target": "user_list"})
        train_data.append({"feature": u"coi danh sách người dùng", "target": "user_list"})
        train_data.append({"feature": u"vào danh sách người dùng", "target": "user_list"})
        train_data.append({"feature": u"tôi muốn xem danh sách người dùng", "target": "user_list"})
        ################################################################################################################
        train_data.append({"feature": u"Chào em gái", "target": "chao_hoi"})
        train_data.append({"feature": u"Chào bạn", "target": "chao_hoi"})
        train_data.append({"feature": u"Hello bạn", "target": "chao_hoi"})
        train_data.append({"feature": u"Hi", "target": "chao_hoi"})
        train_data.append({"feature": u"Xin chào", "target": "chao_hoi"})
        ################################################################################################################
        # train_data.append({"feature": u"report", "target": "report_detail"})
        # train_data.append({"feature": u"báo cáo", "target": "report_detail"})
        # train_data.append({"feature": u"mở báo cáo tòa", "target": "report_detail"})
        # train_data.append({"feature": u"coi báo cáo tầng", "target": "report_detail"})
        # train_data.append({"feature": u"xem báo cáo phòng", "target": "report_detail"})
        # train_data.append({"feature": u"xem báo cáo tòa A5 tầng 4 phòng 193 thiết bị A504 25/07/2020 từ 12:00:00 đến 14:00:00", "target": "report_detail"})
        # train_data.append({"feature": u"xem báo cáo tòa A4 ngày hôm nay", "target": "report_detail"})
        # train_data.append({"feature": u"xem báo cáo tòa A5 ngày hôm nay", "target": "report_detail"})
        # train_data.append({"feature": u"xem báo cáo tòa A5 ngày hôm qua", "target": "report_detail"})
        # train_data.append({"feature": u"xem báo cáo tòa A5 tầng 4 phòng 193 thiết bị A504 25/07/2020", "target": "report_detail"})
        # train_data.append({"feature": u"xem báo cáo tòa A5 tầng 4 phòng 193", "target": "report_detail"})
        # train_data.append({"feature": u"xem báo cáo tòa A5 ", "target": "report_detail"})
        # train_data.append({"feature": u"xem báo cáo phòng A5 ngày hôm nay", "target": "report_detail"})
        train_data.append({"feature": u"hướng dẫn cách dùng", "target": "sd"})
        train_data.append({"feature": u"hướng dẫn tôi được không", "target": "sd"})
        train_data.append({"feature": u"hướng dẫn cách sử dụng", "target": "sd"})
        train_data.append({"feature": u"chưa biết cách dùng như thế nào", "target": "sd"})
        train_data.append({"feature": u"cái này sử dụng sao", "target": "chao_sd"})
        train_data.append({"feature": u"cách sử dụng cái này là gì", "target": "sd"})
        train_data.append({"feature": u"sử dụng như thế nào", "target": "sd"})
        train_data.append({"feature": u"chưa biết cách sử dụng", "target": "sd"})
        train_data.append({"feature": u"cách dùng như thế nào", "target": "sd"})

        ################################################################################################################
        train_data.append({"feature": u"tạm biệt", "target": "bye"})
        train_data.append({"feature": u"goodbye", "target": "bye"})
        train_data.append({"feature": u"bye", "target": "bye"})
        train_data.append({"feature": u"bye bot", "target": "bye"})
        ################################################################################################################
        ################################################################################################################
        train_data.append({"feature": u"xem báo cáo tất cả", "target": "report_all"})
        train_data.append({"feature": u"xem tất cả báo cáo", "target": "report_all"})
        ################################################################################################################
        ################################################################################################################
        ################################################################################################################
        ################################################################################################################
        train_data.append({"feature": u"kW ngày ", "target": "kw"})
        train_data.append({"feature": u"Xem tiêu thụ điện ngày", "target": "kw"})
        train_data.append({"feature": u"Coi tiêu thụ điện ngày", "target": "kw"})
        train_data.append({"feature": u"xem tiêu thụ điện tầng 3 phòng 3 ngày hôm nay", "target": "kw"})
        train_data.append({"feature": u"xem tiêu thụ điện tầng 3 phòng 3 ngày hôm qua", "target": "kw"})
        train_data.append({"feature": u"xem tiêu thụ điện tầng 3 phòng 3 ngày 15/2/2020", "target": "kw"})
        train_data.append({"feature": u"xem tiêu thụ điện tầng 3 phòng 3 từ ngày 2/12/2020 đến 12/20/2020", "target": "kw"})
        train_data.append({"feature": u"điện ngày", "target": "kw"})
        train_data.append({"feature": u"hóa đơn tiền điện ngày", "target": "kw"})
        train_data.append({"feature": u"kW ngày", "target": "kw"})
        train_data.append({"feature": u"mở tiêu thụ điện ngày", "target": "kw"})
        train_data.append({"feature": u"điện đã sử dụng ngày", "target": "kw"})
        ###############################################################
        ###############################################################
        train_data.append({"feature": u"tắt đèn đèn", "target": "control"})
        train_data.append({"feature": u"tắt đèn", "target": "control"})
        train_data.append({"feature": u"mở đèn", "target": "control"})
        train_data.append({"feature": u"điều khiển máy lạnh", "target": "control"})
        train_data.append({"feature": u"bật máy lạnh", "target": "control"})
        train_data.append({"feature": u"tắt máy lạnh", "target": "control"})
        train_data.append({"feature": u"điều khiển thiết bị điện tử ", "target": "control"})
        train_data.append({"feature": u"điều khiển thiết bị", "target": "control"})
        train_data.append({"feature": u"tắt đèn", "target": "control"})
        train_data.append({"feature": u"bật tắt thiết bị", "target": "control"})
        ########################################################################
        df_train = pd.DataFrame(train_data)

        #  test data
        test_data = []
        test_data.append(a)
        df_test = pd.DataFrame(test_data)
        # init model naive bayes
        model = SVMModel()
        clf = model.clf.fit(df_train["feature"], df_train.target)
        predicted = clf.predict(df_test["feature"])
        # Print predicted result
        return predicted[0]





