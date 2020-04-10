import core.aip_ocr as env


# client = client(**cfg.config)
client = env.getAipOcr()

type_index = {
    "Type_basicGeneral" : 0,
    "Type_webImage" : 1,
    "Type_idcard_front" : 2,
    "Type_idcard_back" : 3,
    "Type_bankcard" : 4,
    "Type_drivingLicense" : 5,
    "Type_vehicleLicense" : 6,
    "Type_licensePlate" : 7,
    "Type_businessLicense" : 8
}

type_map = {
    0: 'basicGeneral',
    1: 'webImage',
    2: 'idcard_front',
    3: 'idcard_back',
    4: 'bankcard',
    5: 'drivingLicense',
    6: 'vehicleLicense',
    7: 'licensePlate',
    8: 'businessLicense'
}


class BaiduOCR():

    def __init__(self, img_path):
        self.img_path = img_path

    def set_img_path(self, img_path):
        self.img_path = img_path

    def get_img_path(self):
        return self.img_path

    def get_file_content(self, filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()

    def img_ocr(self):
        image = self.get_file_content(self.img_path)
        #""" 调用通用文字识别, 图片参数为本地图片 """
        # 高精度识别
        options = {}
        options["language_type"] = "CHN_ENG"
        options["detect_direction"] = "true"
        options["detect_language"] = "true"
        options["probability"] = "true"
        bendi = client.basicAccurate(image, options)
        # print(bendi)
        return bendi  # 返回字典数据

    def img2txt_by_type(self, img_type_index):

        img_type = type_map[img_type_index]
        image = self.get_file_content(self,self.img_path)

        if img_type == 'basicGeneral':

            try:
                  result = client.basicGeneral(image)
            except Exception as e:
                print("err={}".format(str(e)))
                return "错误：无法连接到网络！"

          
            if 'words_result' in result:
                return '\n'.join([w['words'] for w in result['words_result']])

        # 待添加图片识别加精度
        elif img_type == 'webImage':
            options = {}
            result = client.webImage(image, options)
            if 'words_result' in result:
                return '\n'.join([w['words'] for w in result['words_result']])

        elif img_type == 'idcard_front':
            options = {}
            options["detect_direction"] = "true"  # 检测朝向
            # 是否开启身份证风险类型(身份证复印件、临时身份证、身份证翻拍、修改过的身份证)功能，默认不开启
            options["detect_risk"] = "true"

            result = client.idcard(image, 'front', options)
            for key in result['words_result'].keys():
                print(key + ':' + result['words_result'][key]['words'])

        elif img_type == 'idcard_back':
            options = {}
            options["detect_direction"] = "true"  # 检测朝向
            # 是否开启身份证风险类型(身份证复印件、临时身份证、身份证翻拍、修改过的身份证)功能，默认不开启
            options["detect_risk"] = "true"

            result = client.idcard(image, 'back', options)
            for key in result['words_result'].keys():
                print(key + ':' + result['words_result'][key]['words'])

        elif img_type == 'bankcard':

            result = client.bankcard(image)
            # bank_card_type 银行卡类型，0:不能识别 1: 借记卡 2: 信用卡
            for key in result['result']:
                print(key + ':' + str(result['result'][key]))

        elif img_type == 'drivingLicense':
            options = {}
            result = client.drivingLicense(image, options)
            for key in result['words_result']:
                print(key + ':' + str(result['words_result'][key]['words']))

        elif img_type == 'vehicleLicense':
            options = {}
            result = client.vehicleLicense(image, options)
            for key in result['words_result']:
                print(key + ':' + str(result['words_result'][key]['words']))

        elif img_type == 'licensePlate':
            options = {}
            options["multi_detect"] = "true"
            # 是否检测多张车牌，默认为false，当置为true的时候可以对一张图片内的多张车牌进行识别
            result = client.licensePlate(image, options)
            print(result)

            if ("error_code" in result) :
                error_code = result["error_code"]
                if error_code != 0 :
                    return result

            for i in range(len(result['words_result'])):
                print(result['words_result'][i]['color'] +
                      ' ' + result['words_result'][i]['number'])

        elif img_type == 'businessLicense':
            options = {}
            result = client.businessLicense(image, options)
            # print(result)
            for key in result['words_result']:
                print(key + ':' + str(result['words_result'][key]['words']))

        else:
            print("no support")
