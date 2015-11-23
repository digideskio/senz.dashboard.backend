# coding: utf-8
import leancloud
from random import randrange
from leancloud import Object, Query

query_limit = 100


def get_userid_list():
    query = Query(Object.extend('User'))
    query.not_equal_to('type', 'developer')
    total_count = query.count()
    query_times = (total_count + query_limit - 1) / query_limit
    user_list = []
    for index in range(query_times):
        query.limit(query_limit)
        query.skip(index * query_limit)
        user_list.extend(query.find())

    tracker_id_set = set()
    for user in user_list:
        if user.id not in tracker_id_set:
            tracker_id_set.add(user.id)
    return list(tracker_id_set)


def set_fake_data_to_db(app_id, user_id):
    # gender_list = ['male', 'female', '']
    # age_list = ['16down', '16to35', '35to55', '55up', '']
    event_list = ["contextAtHome", "contextCommutingWork", "contextAtWork", "contextCommutingHome",
                  "contextWorkingInCBD", "contextStudyingInSchool", "contextWorkingInSchool",
                  "contextOutdoorExercise", "contextIndoorExercise", "contextDinningOut", "contextTravelling",
                  "contextShortTrip", "contextInParty", "contextWindowShopping", "contextAtCinema",
                  "contextAtExhibition", "contextAtPopsConcert", "contextAtTheatre", "contextAtClassicsConcert"]
    # consumption_list = ['5000down', '5000to10000', '10000to20000', '20000up']
    # occupation_list = ['official', 'freelancer', 'teacher', 'student', 'supervisor', 'salesman',
    #                  'engineer', 'others', 'soldier', '']
    # field_list = ['infotech', 'law', 'commerce', 'athlete', 'medical', 'human_resource',
    #              'financial', 'architecture', 'humanities', 'natural', 'manufacture',
    #              'agriculture', 'service']
    # sport_list = ['jogging', 'bicycling', 'fitness', 'basketball', 'football', 'table_tennis'
    #              'badminton']
    # hascar_list = ['yes', 'no', '']
    # haspet_list = ['yes', 'no', '']
    marriage_list = ['yes', 'no', '']
    pregnant_list = ['yes', 'no', '']
    # home_offic_status_list = ['contextAtWork', 'contextAtHome', 'contextCommutingWork', 'contextCommutingHome', '']
    # interest_list = ["jogging", "fitness", "basketball", "football", "badminton", "bicycling", "table_tennis",
    #                  'social', 'online_shopping', 'offline_shopping', 'tech_news', 'entertainment_news',
    #                  'current_news', 'business_news', 'sports_news', 'game_news', 'study', 'gamer', 'health',
    #                  'sports_show', 'game_show', 'variety_show', 'tvseries_show', 'acg', 'indoorsman', '']
    province_list = ['北京', '天津', '上海', '重庆', '河北', '河南', '云南', '辽宁', '黑龙江', '湖南', '安徽', '山东',
                     '新疆', '江苏', '浙江', '江西', '湖北', '广西', '甘肃', '山西', '内蒙古', '陕西', '吉林', '福建',
                     '贵州', '广东', '青海', '西藏', '四川', '宁夏', '海南', '台湾', '香港', '澳门', '兰州']
    city_list = ["北京市", "天津市", "上海市", "重庆市", "崇明县", "湖北省直辖县市", "铜仁市", "毕节市", "石家庄市",
                 "唐山市",  "秦皇岛市",  "邯郸市",  "邢台市",  "保定市",  "张家口市",  "承德市",  "沧州市",  "廊坊市",
                 "衡水市",  "太原市", "大同市",  "阳泉市",  "长治市",  "晋城市",  "朔州市",  "晋中市",  "运城市",
                 "忻州市",  "临汾市",  "吕梁市",  "呼和浩特市",  "包头市",  "乌海市",  "赤峰市",  "通辽市",  "鄂尔多斯市",
                 "呼伦贝尔市",  "巴彦淖尔市",  "乌兰察>    布市",  "兴安盟",  "锡林郭勒盟",  "阿拉善盟",  "沈阳市",  "大连市",
                 "鞍山市",  "抚顺市",  "本溪市",  "丹东市",  "锦州市",  "营口市",  "阜新市",  "辽阳市",  "盘锦市",  "铁岭市",
                 "朝阳市",  "葫芦岛市",  "长春市",  "吉林市",      "四平市",  "辽源市",  "通化市",  "白山市",  "松原市",
                 "白城市",  "延边朝鲜族自治州",  "哈尔滨市",  "齐齐哈尔市",  "鸡西市",  "鹤岗市",  "双鸭山市",  "大庆市",
                 "伊春市",  "佳木斯市",  "七台河市",  "牡丹江市",  "黑河市",  "    绥化市",  "大兴安岭地区",  "南京市",
                 "无锡市",  "徐州市",  "常州市",  "苏州市",  "南通市",  "连云港市",  "淮安市",  "盐城市",  "扬州市",
                 "镇江市",  "泰州市",  "宿迁市",  "杭州市",  "宁波市",  "温州市",  "嘉兴市",  "湖州市",  "绍兴市",
                 "金华市",  "衢州市", "舟山市", "台州市",  "丽水市",  "合肥市",  "芜湖市",  "蚌埠市",  "淮南市",
                 "马鞍山市","淮北市", "铜陵市",  "安庆市",  "黄山市",  "滁州市",  "阜阳市",  "宿州市",  "六安市",
                 "亳州市",  "池州市",  "宣城市",  "福州市",  "厦门市",  "莆田市",  "三明市",  "泉州市",  "漳州市",
                 "南平市",  "龙岩市",  "宁德市",  "南昌市",  "景德镇市",  "萍乡市",  "九江市",  "新余市",  "鹰潭市",  "赣州市",
                 "吉安市",  "宜春市",  "抚州市",  "上饶市",  "济南市",  "青岛市",  "淄博市",  "枣庄市",  "东营市",  "烟台市",
                 "潍坊市",  "济宁市",  "泰安市",  "威海市",  "日照市",  "莱芜市",  "临沂市",  "德州市",  "聊城市",  "滨州市",
                 "菏泽市",  "郑州市",  "开封市",  "洛阳市",  "平顶山市",  "安阳市",  "鹤壁市",  "新乡市",  "焦作市",
                 "濮阳市",  "许昌市",  "漯河市",  "三门峡市",  "南阳市",  "商丘市",  "信阳市",  "周口市",  "驻马店市",
                 "省直辖县级行政区划",  "武汉市",  "黄石市",  "十堰市",  "宜昌市",  "襄阳市",  "鄂州市",  "荆门市",
                 "孝感市",  "荆州市",  "黄冈市",  "咸宁市",  "随州市",  "恩施土家族苗族自治州",  "长沙市",  "株洲市",  "湘潭市",
                 "衡阳市",  "邵阳市",  "岳阳市",  "常德市",  "张家界市", "益阳市",  "郴州市",  "永州市",  "怀化市",
                 "娄底市",  "湘西土家族苗族自治州",  "广州市",  "韶关市",  "深圳市",  "珠海市",  "汕头市",  "佛山市",  "江门市",
                 "湛江市",  "茂名市",  "肇庆市",  "惠州市",  "梅州市",  "汕尾市",  "河源市",  "阳江市",  "清远市",
                 "东莞市",  "中山市",  "潮州市",  "揭阳市",  "云浮市",  "南宁市",  "柳州市",  "桂林市",  "梧州市",  "北海市",
                 "防城港市",  "钦州市",  "贵港市",  "玉林市",  "百色市",  "贺州市",  "河池市",  "来宾市",  "崇左市",
                 "海口市",  "三亚市",  "三沙市",  "成都市",  "自贡市",  "攀枝花市",  "泸州市",  "德阳市",  "绵阳市",  "广元市",
                 "遂宁市",  "内江市",  "乐山市",  "南充市",  "眉山市",  "宜宾市",  "广安市",  "达州市",  "雅安市",
                 "巴中市",  "资阳市",  "阿坝藏族羌族自治州",  "甘孜藏族自治州",  "凉山彝族自治州",  "贵阳市",  "六盘水市",
                 "遵义市",  "安顺市",  "黔西南布依族苗族自治州",  "黔东南苗族侗族自治州",  "黔南布依族苗族自治州",  "昆明市",
                 "曲靖市",  "玉溪市",  "保山市",  "昭通市",  "丽江市",  "普洱市",  "临沧市",  "楚雄彝族自治州",
                 "红河哈尼族彝族自治州",  "文山壮族苗族自治州",  "西双版纳傣族自治州",  "大理白族自治州",  "德宏傣族景颇族自治州",
                 "怒江傈僳族自治州",  "迪庆藏族自治州",  "拉萨市",  "昌都地区",  "山南地区",  "日喀则地区",  "那曲地区",
                 "阿里地区",  "林芝地区",  "西安市",  "铜川市",  "宝鸡市",  "咸阳市",  "渭南市",  "延安市",  "汉中市",
                 "榆林市",  "安康市",  "商洛市    ",  "兰州市",  "嘉峪关市",  "金昌市",  "白银市",  "天水市",  "武威市",
                 "张掖市",  "平凉市",  "酒泉市",  "庆阳市",  "定西市",  "陇南市",  "临夏回族自治州",  "甘南藏族自治州",
                 "西宁市",  "海东地区",  "海北藏族自治州",  "黄南    藏族自治州",  "海南藏族自治州",  "果洛藏族自治州",
                 "玉树藏族自治州",  "海西蒙古族藏族自治州",  "银川市",  "石嘴山市",  "吴忠市",  "固原市",  "中卫市",
                 "乌鲁木齐市",  "克拉玛依市",  "吐鲁番地区",  "哈密地区",  "昌吉回族自治州",  "博尔塔拉蒙古自治州",
                 "巴音郭楞蒙古自治州",  "阿克苏地区",  "克孜勒苏柯尔克孜自治州",  "喀什地区",  "和田地区",  "伊犁哈萨克自治州",
                 "塔城地区",  "阿勒泰地区",  "自治区直辖县级行政区划",  "台湾省",  "香港特别行政区", "澳门特别行政区"]
    dashdatasource = Object.extend('DashDataSource')
    query = Query(dashdatasource)
    query.equal_to('app_id', app_id)
    query.equal_to('user_id', user_id)
    dst_record = query.find()
    if not dst_record:
        dst_record = dashdatasource()
    else:
        dst_record = dst_record[0]

    # content = {}
    # for t in range(24):
    #     status = 'status' + str(t)
    #     content[status] = home_offic_status_list[randrange(0, len(home_offic_status_list))]
    # dst_record.set('home_office_status', content)
    # dst_record.set('pregnant', pregnant_list[randrange(0, len(pregnant_list))])
    # dst_record.set('marriage', marriage_list[randrange(0, len(marriage_list))])
    # dst_record.set('interest', interest_list[randrange(0, len(interest_list))])
    # dst_record.set('consumption', consumption_list[randrange(0, len(consumption_list))])
    # dst_record.set('field', field_list[randrange(0, len(field_list))])
    # dst_record.set('sport', sport_list[randrange(0, len(sport_list))])
    # dst_record.set('occupation', occupation_list[randrange(0, len(occupation_list))])
    # dst_record.set('has_car', hascar_list[randrange(0, len(hascar_list))])
    # dst_record.set('has_pet', haspet_list[randrange(0, len(haspet_list))])
    # dst_record.set('app_id', app_id)
    # dst_record.set('user_id', user_id)
    # dst_record.set('gender', gender_list[randrange(0, len(gender_list))])
    # dst_record.set('age', age_list[randrange(0, len(age_list))])
    dst_record.set('event', event_list[randrange(0, len(event_list))])
    # dst_record.set('province', province_list[randrange(0, len(province_list))])
    # dst_record.set('city', city_list[randrange(0, len(city_list))])
    dst_record.save()
    return True


def get_tracker_of_app(app_id):
    query = Query(Object.extend('Application'))
    query.equal_to('app_id', app_id)
    app_list = query.find()
    if not app_list:
        return []
    the_app = app_list[0]

    query = Query(Object.extend('BindingInstallation'))
    query.equal_to('application', the_app)
    query.select('user')
    installation_list = query.find()
    user_set = set()
    for installation in installation_list:
        user_set.add(installation.attributes['user'].id)
    return list(user_set)

if __name__ == '__main__':
    leancloud.init('z6fhqxvpal43l238q7xzogfdls74my214o5bapm5vkwfn4xh',
                   'rb7jufb22o15nzc9ub5b6b0lx3xt845o2ofz494oc1s9esg8')
    user_list = get_userid_list()
    for item in user_list:
        print(item)
        set_fake_data_to_db('5621fb0f60b27457e863fabb', item)

    # app_id = 'demo55603e35e4b07ae45cd1e581'
    # tracker_list = get_tracker_of_app(app_id)
    # print(tracker_list, len(tracker_list))
