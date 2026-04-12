#!/usr/bin/env python3
"""Generate service_consumer.csv — SVC data for Global Career Development Index."""
import csv, sys, random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from tools.score_calculator import load_weights, calculate_composite

# === OCCUPATIONS (141) from categories.yaml SVC ===
O = []
def _a(mid, mid_zh, mid_en, items):
    for id_, zh, en, isco, onet, loc in items:
        O.append({"id": id_, "mid": mid, "mid_zh": mid_zh, "mid_en": mid_en,
                   "zh": zh, "en": en, "isco": isco, "onet": onet, "locality": loc})

_a("food_beverage", "餐饮", "Food & Beverage", [
    ("0101","中餐厨师","Chinese Cuisine Chef","5120","35-1011.00","global"),
    ("0102","西餐厨师","Western Cuisine Chef","5120","35-1011.00","global"),
    ("0103","西点烘焙师","Pastry Chef / Baker","7512","51-3011.00","global"),
    ("0104","调酒师","Bartender / Mixologist","5132","35-3011.00","global"),
    ("0105","侍酒师","Sommelier","5132","35-3031.00","global"),
    ("0106","餐厅经理","Restaurant Manager","1412","11-9051.00","global"),
    ("0107","食品安全检查员","Food Safety Inspector","3257","45-2011.00","global"),
    ("0108","食品研发工程师","Food Product Developer","2145","19-1012.00","global"),
    ("0109","日料寿司师傅","Sushi Chef / Itamae","5120","35-1011.00","global"),
    ("0110","咖啡师","Barista","5132","35-3023.01","global"),
    ("0111","服务员","Waiter / Waitress","5131","35-3031.00","global"),
    ("0112","行政总厨","Executive Chef","3434","35-1011.00","global"),
    ("0113","屠宰师/肉类切割师","Butcher / Meat Cutter","7511","51-3021.00","global"),
    ("0114","巧克力师","Chocolatier","7512","51-3092.00","global"),
    ("0115","茶艺师","Tea Ceremony Master / Tea Specialist","5132","","regional"),
    ("0116","食品卫生管理员","Food Hygiene Manager","3257","29-9011.00","global"),
    ("0117","面包师","Bread Baker / Boulanger","7512","51-3011.00","global"),
    ("0118","甜品师","Dessert Chef / Patissier","7512","51-3011.00","global"),
    ("0119","餐饮连锁运营经理","Restaurant Chain Operations Manager","1412","11-9051.00","global"),
    ("0120","美食评论家/美食博主","Food Critic / Food Blogger","2641","27-3043.00","global"),
    ("0121","中央厨房经理","Central Kitchen / Commissary Manager","1412","11-9051.00","global"),
])
_a("hospitality_tourism", "酒店旅游", "Hospitality & Tourism", [
    ("0201","酒店总经理","Hotel General Manager","1411","11-9081.00","global"),
    ("0202","前台接待员","Hotel Front Desk Receptionist","4224","43-4081.00","global"),
    ("0203","导游","Tour Guide","5113","39-7012.00","global"),
    ("0204","旅行社计调","Travel Agency Operations Planner","4221","41-3041.00","global"),
    ("0205","OTA运营经理","Online Travel Agency (OTA) Operations Manager","1439","11-9081.00","global"),
    ("0206","礼宾部经理","Concierge Manager","1411","39-6012.00","global"),
    ("0207","客房管理主管","Housekeeping Manager","1411","37-1011.00","global"),
    ("0208","度假村经理","Resort Manager","1411","11-9081.00","global"),
    ("0209","邮轮经理","Cruise Director","1411","11-9081.00","global"),
    ("0210","旅游规划师","Tourism Planner / Destination Manager","2164","19-3051.00","global"),
    ("0211","民宿经营者","B&B / Guesthouse Operator","1411","11-9081.00","global"),
    ("0212","旅游顾问","Travel Consultant","4221","41-3041.00","global"),
    ("0213","赌场酒店经理","Casino/Resort Hotel Manager","1411","11-9081.00","regional"),
    ("0214","主题公园运营经理","Theme Park Operations Manager","1431","11-9071.00","global"),
    ("0215","生态旅游导游","Ecotourism Guide","5113","39-7012.00","global"),
    ("0216","酒店收益管理师","Hotel Revenue Manager","1411","11-9081.00","global"),
])
_a("retail", "零售", "Retail", [
    ("0301","零售店员/销售助理","Retail Sales Associate","5223","41-2031.00","global"),
    ("0302","店长","Store Manager","1420","41-1011.00","global"),
    ("0303","买手","Retail Buyer / Merchandiser","3323","13-1022.00","global"),
    ("0304","电商运营专员","E-commerce Operations Specialist","2431","11-2021.00","global"),
    ("0305","视觉陈列设计师","Visual Merchandiser","3432","27-1026.00","global"),
    ("0306","收银员","Cashier","5230","41-2011.00","global"),
    ("0307","奢侈品销售顾问","Luxury Retail Sales Advisor","5223","41-2031.00","global"),
    ("0308","加油站员工","Gas Station Attendant","5245","53-6031.00","global"),
    ("0309","仓储会员店运营","Warehouse Club Operations Staff","1420","41-1011.00","global"),
    ("0310","直播电商运营","Livestream E-commerce Operator","2431","","regional"),
    ("0311","超市部门经理","Supermarket Department Manager","1420","41-1011.00","global"),
    ("0312","药房零售店员","Pharmacy Retail Assistant","5223","29-2052.00","global"),
    ("0313","二手店/古着店经营者","Secondhand / Vintage Shop Owner","1420","41-1011.00","global"),
    ("0314","花店经营者","Florist / Flower Shop Owner","5243","27-1023.00","global"),
])
_a("beauty_wellness", "美容养生", "Beauty & Wellness", [
    ("0401","美容顾问","Beauty Consultant / Advisor","5142","39-5094.00","global"),
    ("0402","SPA技师/水疗师","Spa Therapist","5142","39-9032.00","global"),
    ("0403","注册营养师","Registered Dietitian","2265","29-1031.00","global"),
    ("0404","健身教练","Fitness Trainer / Personal Trainer","3423","39-9031.00","global"),
    ("0405","瑜伽教练","Yoga Instructor","3423","39-9031.00","global"),
    ("0406","普拉提教练","Pilates Instructor","3423","39-9031.00","global"),
    ("0407","按摩治疗师","Massage Therapist","5142","31-9011.00","global"),
    ("0408","皮肤管理师","Skin Care Specialist","5142","39-5094.00","global"),
    ("0409","体重管理顾问","Weight Management Consultant","2265","29-1031.00","global"),
    ("0410","游泳教练","Swimming Coach / Instructor","3423","39-9031.00","global"),
    ("0411","芳香治疗师","Aromatherapist","5142","39-9032.00","global"),
    ("0412","足疗师/反射疗法师","Reflexologist / Foot Massage Therapist","5142","31-9011.00","global"),
    ("0413","康体私教(功能训练)","Functional Training Coach","3423","39-9031.00","global"),
])
_a("domestic_care", "家政照护", "Domestic & Care Services", [
    ("0501","保姆/家政服务员","Domestic Helper / Housekeeper","5152","39-9011.00","global"),
    ("0502","月嫂/产后护理师","Maternity Nurse / Postpartum Doula","5321","31-1131.00","regional"),
    ("0503","育儿嫂","Childcare Nanny","5311","39-9011.00","global"),
    ("0504","家庭教师","Home Tutor","2353","25-3098.00","global"),
    ("0505","老年护理员","Elderly Care Worker","5322","31-1122.00","global"),
    ("0506","残障护理员","Disability Support Worker","5322","31-1122.00","global"),
    ("0507","陪诊员","Medical Appointment Companion","5322","","regional"),
    ("0508","宠物护理员/宠物美容师","Pet Groomer / Pet Care Worker","5164","39-2021.00","global"),
    ("0509","宠物训练师","Pet/Dog Trainer","5164","39-2011.00","global"),
    ("0510","家庭收纳师","Professional Home Organizer","5152","","global"),
    ("0511","管家(私人/豪宅)","Butler / Estate Manager","5152","39-9011.00","global"),
    ("0512","临终关怀护理员","Hospice Care Worker","5322","31-1122.00","global"),
    ("0513","私人厨师","Private Chef","5120","35-1011.00","global"),
    ("0514","家庭护理协调员","Home Care Coordinator","5322","31-1121.00","global"),
])
_a("platform_gig", "平台零工", "Platform & Gig Economy", [
    ("0601","网约车司机","Ride-hailing Driver (Uber/Didi/etc.)","8322","53-3054.00","global"),
    ("0602","跑腿代办","Errand Runner / Task-based Worker","9621","53-7065.00","global"),
    ("0603","自由职业者平台接单","Freelancer (Fiverr/Upwork/etc.)","2514","15-1252.00","global"),
    ("0604","任务众包工人","Task-based Gig Worker (TaskRabbit/etc.)","9629","53-7065.00","global"),
    ("0605","M-Pesa代理人","M-Pesa Agent","4211","","regional"),
    ("0606","共享单车运维员","Bike-sharing Maintenance Worker","9629","49-3091.00","global"),
    ("0607","代购/个人购物者","Personal Shopper / Daigou Agent","5243","41-2031.00","global"),
    ("0608","在线虚拟助理","Virtual Assistant (Online)","4120","43-6014.00","global"),
    ("0609","民宿清洁服务者","Airbnb / Vacation Rental Cleaner","9112","37-2012.00","global"),
])
_a("funeral", "殡葬", "Funeral Services", [
    ("0701","殡葬师/殡仪馆主任","Funeral Director / Mortician","5163","39-4031.00","global"),
    ("0702","遗体化妆师","Embalmer / Mortuary Cosmetician","5163","39-4011.00","global"),
    ("0703","公墓管理员","Cemetery Manager","5163","39-4031.00","global"),
    ("0704","哀伤辅导师","Grief Counselor","2634","21-1013.00","global"),
])
_a("special_legal", "特殊合法职业", "Special Legal Occupations", [
    ("0801","性工作者(合法地区)","Licensed Sex Worker (Legal Jurisdictions)","5169","","regional"),
    ("0802","博彩从业者/荷官","Casino Dealer / Gaming Worker","4212","39-3011.00","regional"),
    ("0803","大麻产业工人(合法地区)","Cannabis Industry Worker (Legal Jurisdictions)","6113","","regional"),
    ("0804","彩票销售员","Lottery Sales Agent","5230","41-2031.00","global"),
    ("0805","烟草专卖员(合法地区)","Tobacco Retail Specialist","5223","41-2031.00","regional"),
])
_a("cleaning_maintenance", "清洁与维护", "Cleaning & Maintenance", [
    ("0901","保洁员","Janitor / Cleaner","9112","37-2011.00","global"),
    ("0902","物业维修工","Building Maintenance Worker","7131","49-9071.00","global"),
    ("0903","园艺师/园丁","Gardener / Landscaper","6113","37-3011.00","global"),
    ("0904","害虫防治员","Pest Control Technician","7544","37-2021.00","global"),
    ("0905","高空清洁工(蜘蛛人)","High-rise Window Cleaner","9112","37-2011.00","global"),
    ("0906","泳池维护技师","Pool Maintenance Technician","7544","37-2011.00","global"),
    ("0907","洗衣/干洗师","Laundry / Dry Cleaning Worker","8157","51-6011.00","global"),
    ("0908","电梯操作员","Elevator Operator","9629","53-6011.00","global"),
    ("0909","停车管理员","Parking Lot Attendant","5419","53-6021.00","global"),
    ("0910","地毯清洁工","Carpet Cleaner","9112","37-2012.00","global"),
    ("0911","工业清洁工(高压清洗等)","Industrial Cleaner / Pressure Washer","9112","37-2011.00","global"),
])
_a("security", "安保", "Security", [
    ("1001","保安","Security Guard","5414","33-9032.00","global"),
    ("1002","私人保镖","Personal Bodyguard","5414","33-9032.00","global"),
    ("1003","安检员","Security Screener","5414","33-9093.00","global"),
    ("1004","私家侦探","Private Investigator","3411","33-9021.00","global"),
    ("1005","安防系统技术员","Security System Technician","7412","49-2098.00","global"),
])
_a("customer_service", "客户服务", "Customer Service", [
    ("1101","客服专员/呼叫中心坐席","Customer Service Representative / Call Center Agent","4222","43-4051.00","global"),
    ("1102","客服经理","Customer Service Manager","1439","11-9199.00","global"),
    ("1103","投诉处理专员","Complaints Handler","4222","43-4051.00","global"),
    ("1104","技术支持专员","Technical Support Specialist","3512","15-1232.00","global"),
    ("1105","在线客服(聊天)","Online Chat Support Agent","4222","43-4051.00","global"),
])
_a("office_admin", "行政办公", "Office & Administration", [
    ("1201","行政助理/秘书","Administrative Assistant / Secretary","4120","43-6014.00","global"),
    ("1202","前台接待员(企业)","Corporate Receptionist","4226","43-4171.00","global"),
    ("1203","办公室经理","Office Manager","1346","11-3012.00","global"),
    ("1204","会议/日程协调员","Meeting / Schedule Coordinator","4120","43-6014.00","global"),
    ("1205","速记员/文字录入员","Stenographer / Data Entry Clerk","4131","43-9021.00","global"),
])
_a("wedding_events", "婚庆活动", "Wedding & Events", [
    ("1301","婚礼策划师","Wedding Planner","3332","13-1121.00","global"),
    ("1302","司仪/婚礼主持人","Wedding Officiant / MC","2656","27-2011.00","global"),
    ("1303","婚纱礼服顾问","Bridal Gown Consultant","5223","41-2031.00","global"),
    ("1304","婚礼花艺师","Wedding Florist","3432","27-1023.00","global"),
    ("1305","活动安保经理","Event Security Manager","5414","33-9032.00","global"),
])
_a("recreation", "休闲娱乐", "Recreation & Entertainment", [
    ("1401","密室逃脱设计师","Escape Room Designer","2163","27-1027.00","global"),
    ("1402","游乐园操作员","Amusement Park Ride Operator","9629","39-3091.00","global"),
    ("1403","保龄球馆/台球厅经理","Bowling Alley / Billiards Hall Manager","1431","11-9071.00","global"),
    ("1404","高尔夫球场管理员","Golf Course Superintendent","1431","11-9071.00","global"),
    ("1405","KTV/歌厅经理","Karaoke Venue Manager","1431","11-9071.00","regional"),
    ("1406","潜水教练","Scuba Diving Instructor","3423","39-9031.00","global"),
    ("1407","滑雪教练","Ski Instructor","3423","39-9031.00","global"),
    ("1408","马术教练","Equestrian Coach / Riding Instructor","3423","39-9031.00","global"),
    ("1409","攀岩教练","Rock Climbing Instructor","3423","39-9031.00","global"),
    ("1410","射击教练","Shooting / Firearms Instructor","3423","39-9031.00","global"),
    ("1411","蹦极/跳伞教练","Bungee Jumping / Skydiving Instructor","3423","39-9031.00","global"),
    ("1412","电子竞技赛事运营","Esports Event Organizer","3332","13-1121.00","global"),
    ("1413","赛车机械师","Motorsport Mechanic","7231","49-3023.00","global"),
    ("1414","宠物酒店经理","Pet Hotel / Boarding Manager","1431","11-9071.00","global"),
])

OCCUPATIONS = O

# === COUNTRIES (same 45 as all categories) ===
COUNTRIES = [
    {"iso":"CN","name_zh":"中国","name_en":"China","region":"东亚","type":"country","dev":"emerging"},
    {"iso":"JP","name_zh":"日本","name_en":"Japan","region":"东亚","type":"country","dev":"developed"},
    {"iso":"KR","name_zh":"韩国","name_en":"South Korea","region":"东亚","type":"country","dev":"developed"},
    {"iso":"TW","name_zh":"中国台湾地区","name_en":"Taiwan (China)","region":"东亚","type":"region","dev":"developed"},
    {"iso":"HK","name_zh":"中国香港地区","name_en":"Hong Kong (China)","region":"东亚","type":"region","dev":"developed"},
    {"iso":"SG","name_zh":"新加坡","name_en":"Singapore","region":"东南亚","type":"country","dev":"developed"},
    {"iso":"TH","name_zh":"泰国","name_en":"Thailand","region":"东南亚","type":"country","dev":"emerging"},
    {"iso":"VN","name_zh":"越南","name_en":"Vietnam","region":"东南亚","type":"country","dev":"emerging"},
    {"iso":"ID","name_zh":"印度尼西亚","name_en":"Indonesia","region":"东南亚","type":"country","dev":"emerging"},
    {"iso":"MY","name_zh":"马来西亚","name_en":"Malaysia","region":"东南亚","type":"country","dev":"emerging"},
    {"iso":"PH","name_zh":"菲律宾","name_en":"Philippines","region":"东南亚","type":"country","dev":"emerging"},
    {"iso":"IN","name_zh":"印度","name_en":"India","region":"南亚","type":"country","dev":"emerging"},
    {"iso":"PK","name_zh":"巴基斯坦","name_en":"Pakistan","region":"南亚","type":"country","dev":"developing"},
    {"iso":"BD","name_zh":"孟加拉国","name_en":"Bangladesh","region":"南亚","type":"country","dev":"developing"},
    {"iso":"AE","name_zh":"阿联酋","name_en":"United Arab Emirates","region":"中亚/西亚","type":"country","dev":"developed"},
    {"iso":"IL","name_zh":"以色列","name_en":"Israel","region":"中亚/西亚","type":"country","dev":"developed"},
    {"iso":"SA","name_zh":"沙特阿拉伯","name_en":"Saudi Arabia","region":"中亚/西亚","type":"country","dev":"emerging"},
    {"iso":"TR","name_zh":"土耳其","name_en":"Turkey","region":"中亚/西亚","type":"country","dev":"emerging"},
    {"iso":"GB","name_zh":"英国","name_en":"United Kingdom","region":"西欧","type":"country","dev":"developed"},
    {"iso":"FR","name_zh":"法国","name_en":"France","region":"西欧","type":"country","dev":"developed"},
    {"iso":"DE","name_zh":"德国","name_en":"Germany","region":"西欧","type":"country","dev":"developed"},
    {"iso":"NL","name_zh":"荷兰","name_en":"Netherlands","region":"西欧","type":"country","dev":"developed"},
    {"iso":"CH","name_zh":"瑞士","name_en":"Switzerland","region":"西欧","type":"country","dev":"developed"},
    {"iso":"SE","name_zh":"瑞典","name_en":"Sweden","region":"北欧","type":"country","dev":"developed"},
    {"iso":"DK","name_zh":"丹麦","name_en":"Denmark","region":"北欧","type":"country","dev":"developed"},
    {"iso":"FI","name_zh":"芬兰","name_en":"Finland","region":"北欧","type":"country","dev":"developed"},
    {"iso":"IT","name_zh":"意大利","name_en":"Italy","region":"南欧","type":"country","dev":"developed"},
    {"iso":"ES","name_zh":"西班牙","name_en":"Spain","region":"南欧","type":"country","dev":"developed"},
    {"iso":"PT","name_zh":"葡萄牙","name_en":"Portugal","region":"南欧","type":"country","dev":"developed"},
    {"iso":"PL","name_zh":"波兰","name_en":"Poland","region":"东欧","type":"country","dev":"emerging"},
    {"iso":"CZ","name_zh":"捷克","name_en":"Czech Republic","region":"东欧","type":"country","dev":"developed"},
    {"iso":"RU","name_zh":"俄罗斯","name_en":"Russia","region":"东欧","type":"country","dev":"emerging"},
    {"iso":"US","name_zh":"美国","name_en":"United States","region":"北美","type":"country","dev":"developed"},
    {"iso":"CA","name_zh":"加拿大","name_en":"Canada","region":"北美","type":"country","dev":"developed"},
    {"iso":"MX","name_zh":"墨西哥","name_en":"Mexico","region":"北美","type":"country","dev":"emerging"},
    {"iso":"BR","name_zh":"巴西","name_en":"Brazil","region":"南美","type":"country","dev":"emerging"},
    {"iso":"AR","name_zh":"阿根廷","name_en":"Argentina","region":"南美","type":"country","dev":"emerging"},
    {"iso":"CL","name_zh":"智利","name_en":"Chile","region":"南美","type":"country","dev":"emerging"},
    {"iso":"CO","name_zh":"哥伦比亚","name_en":"Colombia","region":"南美","type":"country","dev":"emerging"},
    {"iso":"AU","name_zh":"澳大利亚","name_en":"Australia","region":"大洋洲","type":"country","dev":"developed"},
    {"iso":"NZ","name_zh":"新西兰","name_en":"New Zealand","region":"大洋洲","type":"country","dev":"developed"},
    {"iso":"ZA","name_zh":"南非","name_en":"South Africa","region":"非洲","type":"country","dev":"emerging"},
    {"iso":"NG","name_zh":"尼日利亚","name_en":"Nigeria","region":"非洲","type":"country","dev":"developing"},
    {"iso":"KE","name_zh":"肯尼亚","name_en":"Kenya","region":"非洲","type":"country","dev":"developing"},
    {"iso":"EG","name_zh":"埃及","name_en":"Egypt","region":"非洲","type":"country","dev":"developing"},
]

# === COUNTRY PROFILES for SVC ===
# Keys: svc(service economy), tour(tourism sector), ret(retail market), gig(gig economy),
#   care(care demand), hosp(hospitality pay), tip(tipping culture),
#   comp(compensation), wlb(work-life balance), stab(stability),
#   edu(edu quality), intl(international openness), gender(gender equality),
#   reg(regulatory), ot(overtime culture, higher=less OT)
CP = {
    "US": {"svc":9.0,"tour":8.5,"ret":9.5,"gig":9.0,"care":7.5,"hosp":6.5,"tip":9.5,"comp":8.5,"wlb":6.0,"stab":6.0,"edu":9.0,"intl":8.5,"gender":7.5,"reg":6.0,"ot":5.0},
    "GB": {"svc":8.5,"tour":8.0,"ret":8.5,"gig":8.0,"care":7.5,"hosp":6.0,"tip":6.0,"comp":7.0,"wlb":7.0,"stab":7.0,"edu":8.5,"intl":9.0,"gender":7.5,"reg":7.5,"ot":6.5},
    "FR": {"svc":8.0,"tour":9.5,"ret":7.5,"gig":6.5,"care":7.0,"hosp":6.5,"tip":4.5,"comp":6.5,"wlb":8.0,"stab":7.0,"edu":8.0,"intl":7.5,"gender":7.0,"reg":8.0,"ot":7.0},
    "DE": {"svc":7.5,"tour":7.5,"ret":8.0,"gig":6.0,"care":8.0,"hosp":7.0,"tip":5.0,"comp":7.5,"wlb":8.0,"stab":8.0,"edu":8.5,"intl":8.0,"gender":7.0,"reg":8.0,"ot":7.5},
    "JP": {"svc":9.0,"tour":8.5,"ret":9.0,"gig":5.5,"care":9.0,"hosp":7.0,"tip":2.0,"comp":6.5,"wlb":4.5,"stab":7.5,"edu":8.0,"intl":5.0,"gender":5.0,"reg":7.0,"ot":3.5},
    "KR": {"svc":8.5,"tour":7.5,"ret":8.5,"gig":6.0,"care":8.0,"hosp":6.5,"tip":2.5,"comp":6.5,"wlb":4.0,"stab":6.5,"edu":8.0,"intl":6.0,"gender":4.5,"reg":6.5,"ot":3.0},
    "CN": {"svc":8.5,"tour":8.0,"ret":9.5,"gig":9.5,"care":8.5,"hosp":5.5,"tip":3.0,"comp":5.5,"wlb":3.5,"stab":5.5,"edu":7.5,"intl":5.0,"gender":5.5,"reg":5.5,"ot":2.5},
    "TW": {"svc":7.5,"tour":7.0,"ret":7.5,"gig":6.5,"care":7.0,"hosp":5.5,"tip":3.0,"comp":5.0,"wlb":5.0,"stab":6.0,"edu":7.5,"intl":6.5,"gender":6.0,"reg":6.0,"ot":4.0},
    "HK": {"svc":8.5,"tour":8.0,"ret":8.0,"gig":6.0,"care":7.5,"hosp":6.5,"tip":5.5,"comp":7.0,"wlb":4.5,"stab":6.5,"edu":7.5,"intl":9.0,"gender":6.5,"reg":6.5,"ot":3.5},
    "SG": {"svc":8.0,"tour":8.0,"ret":7.5,"gig":6.5,"care":7.5,"hosp":7.0,"tip":3.5,"comp":7.5,"wlb":5.5,"stab":8.0,"edu":8.5,"intl":9.5,"gender":7.0,"reg":8.5,"ot":4.5},
    "IN": {"svc":7.5,"tour":7.5,"ret":8.0,"gig":8.5,"care":6.0,"hosp":4.0,"tip":6.5,"comp":3.5,"wlb":4.5,"stab":5.0,"edu":7.0,"intl":7.0,"gender":4.0,"reg":5.0,"ot":4.0},
    "TH": {"svc":8.0,"tour":9.0,"ret":7.0,"gig":6.5,"care":5.5,"hosp":4.5,"tip":5.5,"comp":3.5,"wlb":5.5,"stab":5.5,"edu":5.5,"intl":6.0,"gender":6.5,"reg":5.0,"ot":5.5},
    "VN": {"svc":7.0,"tour":7.5,"ret":7.0,"gig":7.0,"care":5.0,"hosp":3.5,"tip":4.0,"comp":3.0,"wlb":5.0,"stab":5.0,"edu":5.5,"intl":5.5,"gender":5.5,"reg":5.0,"ot":4.5},
    "ID": {"svc":7.0,"tour":7.5,"ret":7.5,"gig":8.0,"care":5.0,"hosp":3.5,"tip":4.5,"comp":3.0,"wlb":5.5,"stab":5.0,"edu":5.0,"intl":4.5,"gender":5.0,"reg":5.0,"ot":5.0},
    "MY": {"svc":7.0,"tour":7.5,"ret":7.0,"gig":6.5,"care":5.5,"hosp":4.5,"tip":4.5,"comp":4.5,"wlb":5.5,"stab":6.0,"edu":6.0,"intl":6.5,"gender":5.5,"reg":5.5,"ot":5.0},
    "PH": {"svc":7.5,"tour":7.0,"ret":6.5,"gig":7.5,"care":6.5,"hosp":4.0,"tip":6.0,"comp":3.0,"wlb":5.0,"stab":4.5,"edu":5.5,"intl":7.0,"gender":6.5,"reg":4.5,"ot":4.5},
    "PK": {"svc":5.5,"tour":5.5,"ret":6.0,"gig":5.5,"care":4.5,"hosp":3.0,"tip":5.0,"comp":2.5,"wlb":4.5,"stab":3.5,"edu":4.5,"intl":4.5,"gender":3.0,"reg":4.0,"ot":4.5},
    "BD": {"svc":5.5,"tour":4.5,"ret":5.5,"gig":5.5,"care":4.0,"hosp":2.5,"tip":4.0,"comp":2.0,"wlb":4.5,"stab":3.5,"edu":4.0,"intl":4.5,"gender":3.5,"reg":3.5,"ot":4.5},
    "AE": {"svc":8.5,"tour":9.0,"ret":8.5,"gig":6.0,"care":7.0,"hosp":7.5,"tip":5.0,"comp":7.5,"wlb":5.5,"stab":7.0,"edu":7.0,"intl":8.5,"gender":5.5,"reg":7.0,"ot":5.0},
    "IL": {"svc":7.0,"tour":7.0,"ret":7.0,"gig":7.0,"care":6.5,"hosp":6.0,"tip":7.0,"comp":7.0,"wlb":6.0,"stab":5.5,"edu":8.5,"intl":8.0,"gender":7.0,"reg":6.0,"ot":5.0},
    "SA": {"svc":6.5,"tour":7.0,"ret":7.0,"gig":5.0,"care":5.5,"hosp":5.5,"tip":4.0,"comp":6.0,"wlb":5.5,"stab":6.0,"edu":6.0,"intl":5.5,"gender":3.5,"reg":6.0,"ot":5.0},
    "TR": {"svc":7.5,"tour":8.5,"ret":7.0,"gig":6.0,"care":5.5,"hosp":4.5,"tip":5.5,"comp":4.0,"wlb":5.0,"stab":4.0,"edu":6.5,"intl":5.5,"gender":4.5,"reg":5.0,"ot":4.5},
    "NL": {"svc":7.5,"tour":7.5,"ret":7.5,"gig":7.0,"care":8.0,"hosp":7.0,"tip":3.5,"comp":7.5,"wlb":9.0,"stab":7.5,"edu":8.0,"intl":9.0,"gender":8.5,"reg":7.5,"ot":8.0},
    "CH": {"svc":7.5,"tour":8.0,"ret":7.0,"gig":5.5,"care":7.5,"hosp":8.5,"tip":4.0,"comp":9.5,"wlb":8.5,"stab":9.0,"edu":9.0,"intl":8.5,"gender":7.0,"reg":7.5,"ot":7.5},
    "SE": {"svc":7.0,"tour":6.5,"ret":7.0,"gig":6.0,"care":8.5,"hosp":7.0,"tip":2.5,"comp":7.0,"wlb":9.0,"stab":8.0,"edu":8.5,"intl":8.5,"gender":9.0,"reg":7.5,"ot":8.5},
    "DK": {"svc":7.0,"tour":6.5,"ret":7.0,"gig":5.5,"care":8.5,"hosp":7.5,"tip":2.5,"comp":7.5,"wlb":9.0,"stab":8.0,"edu":8.5,"intl":8.5,"gender":9.0,"reg":7.5,"ot":8.5},
    "FI": {"svc":6.5,"tour":6.0,"ret":6.5,"gig":5.5,"care":8.5,"hosp":6.5,"tip":2.0,"comp":6.5,"wlb":9.0,"stab":7.5,"edu":9.0,"intl":8.0,"gender":9.0,"reg":7.5,"ot":8.5},
    "IT": {"svc":7.5,"tour":9.0,"ret":7.5,"gig":5.5,"care":6.5,"hosp":5.5,"tip":4.5,"comp":5.5,"wlb":6.5,"stab":5.5,"edu":7.0,"intl":6.5,"gender":5.5,"reg":6.5,"ot":5.5},
    "ES": {"svc":8.0,"tour":9.5,"ret":7.0,"gig":6.0,"care":6.0,"hosp":5.0,"tip":4.0,"comp":5.0,"wlb":7.0,"stab":5.5,"edu":7.0,"intl":7.0,"gender":6.5,"reg":6.5,"ot":5.5},
    "PT": {"svc":7.0,"tour":8.5,"ret":6.5,"gig":5.5,"care":5.5,"hosp":4.5,"tip":4.0,"comp":4.5,"wlb":7.0,"stab":5.5,"edu":6.5,"intl":7.5,"gender":7.0,"reg":6.0,"ot":6.0},
    "PL": {"svc":6.5,"tour":6.5,"ret":7.0,"gig":5.5,"care":6.0,"hosp":5.0,"tip":5.5,"comp":5.5,"wlb":7.0,"stab":6.5,"edu":7.0,"intl":7.5,"gender":6.5,"reg":6.5,"ot":6.0},
    "CZ": {"svc":6.5,"tour":7.0,"ret":6.5,"gig":5.5,"care":6.0,"hosp":5.5,"tip":5.0,"comp":5.5,"wlb":7.5,"stab":7.0,"edu":7.0,"intl":7.5,"gender":6.5,"reg":6.5,"ot":6.5},
    "RU": {"svc":7.0,"tour":6.5,"ret":7.0,"gig":6.5,"care":5.5,"hosp":4.0,"tip":5.0,"comp":4.5,"wlb":5.5,"stab":4.0,"edu":7.5,"intl":3.5,"gender":6.0,"reg":4.5,"ot":5.5},
    "CA": {"svc":8.0,"tour":7.5,"ret":8.0,"gig":7.5,"care":7.5,"hosp":6.5,"tip":8.5,"comp":7.5,"wlb":7.5,"stab":7.0,"edu":8.0,"intl":9.0,"gender":8.0,"reg":7.0,"ot":6.5},
    "MX": {"svc":7.5,"tour":8.5,"ret":7.0,"gig":7.0,"care":5.0,"hosp":4.0,"tip":7.0,"comp":3.5,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.5,"gender":5.0,"reg":5.0,"ot":4.5},
    "BR": {"svc":7.5,"tour":7.5,"ret":7.5,"gig":7.5,"care":5.5,"hosp":4.5,"tip":5.5,"comp":4.0,"wlb":6.0,"stab":4.5,"edu":6.0,"intl":5.0,"gender":5.5,"reg":5.5,"ot":5.0},
    "AR": {"svc":7.0,"tour":7.0,"ret":6.5,"gig":6.0,"care":5.0,"hosp":4.0,"tip":5.5,"comp":3.5,"wlb":5.5,"stab":3.5,"edu":6.5,"intl":5.0,"gender":5.5,"reg":4.5,"ot":5.0},
    "CL": {"svc":6.5,"tour":6.5,"ret":6.5,"gig":5.5,"care":5.5,"hosp":4.5,"tip":5.0,"comp":4.5,"wlb":6.0,"stab":5.5,"edu":6.0,"intl":6.0,"gender":5.5,"reg":5.5,"ot":5.5},
    "CO": {"svc":6.5,"tour":7.0,"ret":6.5,"gig":6.0,"care":5.0,"hosp":4.0,"tip":5.5,"comp":3.5,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.0,"gender":5.0,"reg":5.0,"ot":5.0},
    "AU": {"svc":8.5,"tour":8.5,"ret":8.5,"gig":7.5,"care":7.5,"hosp":7.5,"tip":5.0,"comp":8.0,"wlb":8.0,"stab":7.5,"edu":8.0,"intl":8.5,"gender":8.0,"reg":7.5,"ot":7.0},
    "NZ": {"svc":7.5,"tour":8.5,"ret":7.0,"gig":6.5,"care":7.0,"hosp":6.5,"tip":4.0,"comp":6.5,"wlb":8.5,"stab":7.5,"edu":7.5,"intl":8.0,"gender":8.5,"reg":7.0,"ot":7.5},
    "ZA": {"svc":6.5,"tour":7.5,"ret":6.5,"gig":5.5,"care":5.0,"hosp":4.5,"tip":6.5,"comp":4.0,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.5,"gender":5.5,"reg":5.0,"ot":5.5},
    "NG": {"svc":6.0,"tour":5.0,"ret":6.0,"gig":7.0,"care":4.0,"hosp":3.0,"tip":5.5,"comp":2.5,"wlb":4.5,"stab":3.5,"edu":4.0,"intl":4.5,"gender":4.0,"reg":3.5,"ot":4.5},
    "KE": {"svc":6.0,"tour":7.5,"ret":5.5,"gig":7.5,"care":4.5,"hosp":3.5,"tip":5.5,"comp":2.5,"wlb":5.0,"stab":4.0,"edu":4.5,"intl":5.0,"gender":4.5,"reg":4.0,"ot":5.0},
    "EG": {"svc":7.0,"tour":8.0,"ret":6.5,"gig":5.5,"care":5.0,"hosp":4.0,"tip":6.0,"comp":3.0,"wlb":5.0,"stab":4.0,"edu":5.0,"intl":5.0,"gender":3.5,"reg":4.5,"ot":4.5},
}

# === MID-CATEGORY DEFAULT SCORES ===
K = ["learning_cost","education_req","growth_coeff","career_lifespan",
     "opportunity","market_size","supply_demand","developed_scarcity",
     "value_added","cost_performance","stability","safety","occupational_disease",
     "overtime","burnout","skill_versatility","career_switch","reputation_variance",
     "ai_resistance","social_status","remote_friendly","autonomy","family_friendly",
     "fulfillment","entrepreneurship","gender_equality","age_flexibility",
     "social_interaction","physical_demand","license_barrier","cycle_sensitivity",
     "side_job_compat","intl_mobility","industry_monopoly",
     "trend_long","trend_short","edu","age"]

def _d(*v):
    return dict(zip(K, v))

MID_DEFAULTS = {
    # food_beverage: skilled manual, moderate learning, high physical, high burnout, tipping-dependent, low remote
    "food_beverage": _d(5.5,3.5,5.0,6.5, 5.5,6.0,5.5,5.5, 4.5,4.5, 4.5,6.0,5.5,3.5,6.0, 6.0,5.5,2.5, 7.0,5.0,1.5,5.5,3.5,7.0,7.0,5.0,5.5, 7.5,7.0,3.0,6.0,5.5,5.0,4.5, 2,1,"专科/职校","18-28"),
    # hospitality_tourism: customer-facing, seasonal, high cycle sensitivity, tipping matters, moderate pay
    "hospitality_tourism": _d(4.5,4.0,5.0,7.0, 5.5,6.0,5.0,5.0, 5.0,4.5, 4.5,7.0,6.5,4.0,5.5, 6.0,5.5,2.0, 7.0,5.5,2.5,5.0,4.0,6.0,6.5,5.5,5.5, 8.0,5.0,2.5,7.5,4.5,6.0,4.5, 2,1,"专科/本科","20-30"),
    # retail: low barrier, AI-disrupted (cashiers), high customer-facing, low pay
    "retail": _d(3.0,3.0,4.0,6.5, 5.5,7.0,4.5,4.0, 3.5,4.0, 4.5,8.0,7.0,4.5,5.5, 5.5,5.5,1.5, 5.0,4.0,2.0,4.0,4.0,4.5,5.5,5.5,5.5, 7.5,4.5,1.5,6.0,5.0,3.5,4.0, 0,-1,"高中/专科","18-30"),
    # beauty_wellness: skilled service, growing demand, physical, moderate entrepreneurship
    "beauty_wellness": _d(4.5,3.5,6.0,7.0, 6.0,6.0,5.5,5.0, 4.5,5.0, 5.0,7.5,6.0,4.5,5.5, 5.5,5.0,2.0, 7.5,5.0,2.0,6.0,4.5,7.0,7.5,6.5,6.0, 7.5,6.5,3.0,5.0,6.5,4.0,3.5, 3,2,"专科/证书","20-30"),
    # domestic_care: growing demand everywhere, low barrier, aging society driver, low pay, high physical
    "domestic_care": _d(3.5,2.5,6.0,6.5, 6.5,6.5,6.5,6.0, 3.5,4.0, 4.0,7.0,5.5,4.5,6.5, 4.5,4.5,1.5, 8.5,3.5,1.5,4.5,4.0,6.5,4.5,6.5,5.5, 7.5,6.5,2.0,3.5,4.5,4.5,3.5, 3,3,"高中/证书","20-40"),
    # platform_gig: zero barrier, zero stability, high flexibility, zero benefits
    "platform_gig": _d(2.0,1.5,6.5,5.0, 7.0,7.5,5.0,3.5, 3.0,3.5, 2.0,6.0,5.5,3.5,6.0, 4.5,5.0,1.5, 5.5,3.0,3.5,7.5,4.5,4.0,6.5,5.0,5.0, 5.0,5.5,1.0,5.5,8.0,3.0,3.0, 4,3,"无要求","18-40"),
    # funeral: stable demand, low competition, moderate pay, emotionally demanding
    "funeral": _d(4.0,4.0,4.5,8.0, 5.0,4.0,5.5,5.5, 5.0,5.5, 6.5,6.5,5.0,5.5,5.5, 4.5,4.0,1.0, 8.5,4.5,1.5,5.5,5.0,6.0,4.5,5.0,6.5, 6.5,5.0,4.0,2.0,3.0,3.5,5.0, 1,0,"专科/证书","22-35"),
    # special_legal: highly regulated, region-specific, social stigma in some areas, variable
    "special_legal": _d(2.5,2.0,4.0,5.5, 5.0,5.0,4.5,4.0, 4.0,4.5, 3.5,5.0,5.0,4.0,5.5, 4.0,4.0,2.5, 7.0,3.0,1.5,5.0,3.0,4.0,4.5,4.5,4.5, 6.5,5.0,5.0,4.5,4.5,3.0,5.5, 1,1,"无要求/证书","18-35"),
    # cleaning_maintenance: lowest barrier, low pay, high physical, stable demand, low AI risk
    "cleaning_maintenance": _d(2.0,1.5,3.5,7.0, 5.5,6.0,5.0,5.5, 2.5,3.5, 5.0,6.0,5.0,5.0,5.0, 3.5,4.5,1.0, 7.5,2.5,1.0,3.5,4.0,3.5,4.0,5.0,6.5, 4.5,7.5,1.0,4.0,5.5,3.0,3.5, 0,0,"无要求","18-45"),
    # security: physical, shift-based, moderate stability, low AI for physical roles
    "security": _d(3.0,2.5,4.5,6.5, 5.5,5.5,5.0,5.0, 3.5,4.0, 5.5,5.0,6.0,4.0,5.0, 4.0,4.5,1.5, 7.0,4.0,1.0,4.0,3.5,4.5,4.0,3.5,5.0, 5.0,7.0,3.0,4.0,4.5,3.5,4.5, 1,0,"高中/证书","20-35"),
    # customer_service: high AI disruption, remote possible, high burnout, low pay
    "customer_service": _d(3.0,3.5,4.0,6.5, 5.5,7.0,5.0,4.0, 3.5,4.0, 5.0,8.5,7.0,4.5,6.5, 5.0,5.5,1.5, 3.5,3.5,6.5,3.5,5.0,3.5,3.5,6.0,5.5, 8.0,2.0,1.5,5.0,4.5,4.0,4.5, -1,-2,"高中/专科","18-30"),
    # office_admin: moderate, AI-threatened, shrinking roles, remote growing
    "office_admin": _d(3.0,3.5,3.5,7.0, 5.0,6.5,4.5,4.0, 3.5,4.0, 5.5,8.5,7.5,5.0,5.0, 5.5,5.5,1.0, 3.5,4.0,6.0,4.0,5.5,4.0,3.5,6.0,6.0, 6.0,2.0,1.5,4.0,4.0,4.0,4.0, -1,-2,"专科/本科","20-30"),
    # wedding_events: seasonal, creative-service hybrid, customer-facing, entrepreneurial
    "wedding_events": _d(3.5,3.5,5.0,7.0, 5.5,5.5,5.0,4.5, 4.5,4.5, 4.0,7.5,7.0,4.0,5.5, 5.5,5.5,2.0, 7.5,5.0,2.0,6.5,4.0,7.0,7.5,6.0,5.5, 8.0,4.5,2.0,7.0,5.5,4.0,3.5, 2,1,"专科","20-32"),
    # recreation: seasonal, physical, growing wellness/experience economy, moderate
    "recreation": _d(4.0,3.5,5.5,7.0, 5.5,5.5,5.0,4.5, 4.0,4.5, 4.5,6.0,6.0,4.5,5.0, 5.0,5.0,1.5, 7.5,4.5,1.5,6.0,4.0,7.0,6.5,5.5,5.5, 7.5,6.0,3.0,6.5,5.5,4.5,4.0, 2,2,"专科/证书","20-32"),
}

# === PER-OCCUPATION OVERRIDES ===
OVR = {
    # food_beverage
    "0101": {"intl_mobility":4.5,"value_added":5.0,"social_status":5.5,"ai_resistance":8.0,"fulfillment":7.5},
    "0102": {"intl_mobility":6.0,"value_added":5.0,"social_status":5.5,"ai_resistance":8.0},
    "0103": {"fulfillment":7.5,"ai_resistance":8.0,"entrepreneurship":8.0,"gender_equality":6.0},
    "0104": {"social_interaction":8.5,"fulfillment":7.0,"entrepreneurship":7.0,"social_status":5.5,"intl_mobility":6.0},
    "0105": {"learning_cost":6.0,"value_added":6.0,"social_status":6.5,"education_req":4.5,"ai_resistance":8.5,"intl_mobility":7.0,"market_size":4.0},
    "0106": {"education_req":4.5,"value_added":6.0,"social_status":6.0,"autonomy":7.0,"entrepreneurship":7.5,"stability":5.5,"age":"25-35"},
    "0107": {"education_req":5.0,"stability":7.0,"value_added":5.0,"social_status":5.0,"ai_resistance":6.5,"license_barrier":5.0,"physical_demand":3.5,"remote_friendly":3.5},
    "0108": {"education_req":6.0,"learning_cost":6.5,"value_added":6.5,"social_status":5.5,"ai_resistance":6.0,"remote_friendly":4.0,"physical_demand":3.0,"edu":"本科","age":"24-32"},
    "0109": {"learning_cost":7.0,"ai_resistance":9.0,"value_added":5.5,"fulfillment":8.0,"intl_mobility":6.5,"career_lifespan":7.0},
    "0110": {"learning_cost":3.5,"value_added":3.0,"social_status":4.0,"ai_resistance":7.0,"entrepreneurship":6.0,"side_job_compat":6.5},
    "0111": {"learning_cost":2.0,"education_req":1.5,"value_added":2.5,"stability":3.5,"social_status":3.0,"ai_resistance":6.5,"burnout":6.5,"age":"16-25","edu":"无要求"},
    "0112": {"learning_cost":7.0,"value_added":7.0,"social_status":7.5,"autonomy":8.0,"entrepreneurship":8.0,"career_lifespan":7.5,"stability":5.5,"age":"30-40"},
    "0113": {"physical_demand":8.0,"ai_resistance":8.0,"value_added":4.0,"safety":5.5,"learning_cost":4.0,"market_size":5.0},
    "0114": {"learning_cost":6.0,"fulfillment":8.0,"ai_resistance":8.5,"entrepreneurship":8.5,"value_added":5.0,"market_size":4.0,"intl_mobility":6.5},
    "0115": {"ai_resistance":9.0,"market_size":3.5,"intl_mobility":3.5,"fulfillment":7.0,"social_status":5.0},
    "0116": {"stability":6.5,"value_added":4.5,"social_status":4.5,"ai_resistance":6.0,"license_barrier":4.5,"physical_demand":3.0},
    "0117": {"physical_demand":7.5,"ai_resistance":8.0,"fulfillment":7.0,"entrepreneurship":7.5,"learning_cost":4.5},
    "0118": {"fulfillment":7.5,"ai_resistance":8.5,"entrepreneurship":8.0,"value_added":4.5,"intl_mobility":6.0},
    "0119": {"education_req":5.0,"value_added":6.5,"social_status":6.0,"autonomy":6.5,"stability":5.5,"entrepreneurship":7.0,"age":"28-38","edu":"本科"},
    "0120": {"remote_friendly":7.5,"ai_resistance":6.0,"education_req":4.0,"entrepreneurship":9.0,"value_added":5.0,"social_status":5.5,"physical_demand":2.0,"side_job_compat":8.0},
    "0121": {"education_req":4.5,"value_added":5.5,"stability":5.5,"autonomy":6.5,"social_interaction":5.0,"physical_demand":4.0,"age":"28-38"},
    # hospitality_tourism
    "0201": {"education_req":6.0,"value_added":7.5,"social_status":7.5,"autonomy":8.0,"career_lifespan":8.0,"stability":6.5,"intl_mobility":7.5,"entrepreneurship":7.5,"age":"30-40","edu":"本科"},
    "0202": {"learning_cost":2.5,"education_req":2.5,"value_added":3.0,"stability":4.5,"social_status":3.5,"ai_resistance":6.0,"burnout":5.0,"age":"18-25","edu":"高中"},
    "0203": {"physical_demand":6.0,"social_interaction":9.0,"ai_resistance":7.5,"value_added":3.5,"stability":3.5,"fulfillment":7.0,"intl_mobility":5.5,"cycle_sensitivity":8.0},
    "0204": {"ai_resistance":5.0,"value_added":3.5,"stability":4.5,"social_interaction":7.0,"remote_friendly":5.0},
    "0205": {"education_req":5.0,"ai_resistance":5.0,"value_added":6.0,"growth_coeff":6.5,"remote_friendly":7.0,"trend_short":2,"age":"25-35","edu":"本科"},
    "0206": {"social_interaction":9.0,"value_added":5.5,"social_status":6.5,"ai_resistance":7.5,"intl_mobility":7.0},
    "0207": {"physical_demand":5.5,"value_added":4.5,"stability":5.5,"gender_equality":4.5,"ai_resistance":7.5},
    "0208": {"value_added":6.5,"social_status":7.0,"autonomy":7.5,"fulfillment":7.0,"intl_mobility":6.5,"entrepreneurship":7.0,"age":"28-38"},
    "0209": {"intl_mobility":8.0,"value_added":6.0,"social_status":6.5,"physical_demand":4.0,"family_friendly":3.0,"ai_resistance":7.0},
    "0210": {"education_req":6.0,"value_added":5.5,"social_status":6.0,"ai_resistance":6.5,"remote_friendly":5.0,"entrepreneurship":6.0,"learning_cost":5.5,"edu":"本科"},
    "0211": {"entrepreneurship":9.0,"autonomy":8.5,"value_added":5.0,"stability":3.5,"growth_coeff":6.5,"trend_short":2,"cycle_sensitivity":7.5},
    "0212": {"ai_resistance":5.0,"value_added":3.5,"remote_friendly":5.5,"social_interaction":7.5},
    "0213": {"value_added":7.0,"social_status":7.0,"stability":6.0,"license_barrier":5.0,"market_size":4.0},
    "0214": {"value_added":6.0,"social_status":6.0,"market_size":5.0,"stability":5.5,"entrepreneurship":6.0,"age":"25-35"},
    "0215": {"fulfillment":7.5,"ai_resistance":8.0,"growth_coeff":6.5,"trend_short":2,"physical_demand":6.5,"value_added":4.0,"market_size":4.5},
    "0216": {"education_req":5.5,"value_added":6.0,"ai_resistance":5.5,"remote_friendly":6.0,"learning_cost":5.0,"growth_coeff":6.0,"trend_short":2,"edu":"本科"},
    # retail
    "0301": {"value_added":2.5,"stability":4.0,"ai_resistance":5.5,"social_interaction":8.0,"burnout":5.5},
    "0302": {"value_added":5.0,"social_status":5.0,"autonomy":6.5,"stability":5.5,"entrepreneurship":6.5,"age":"25-35"},
    "0303": {"education_req":4.5,"value_added":5.5,"social_status":5.5,"ai_resistance":6.0,"intl_mobility":6.0,"fulfillment":6.0,"learning_cost":4.5},
    "0304": {"remote_friendly":7.0,"ai_resistance":4.5,"growth_coeff":7.0,"trend_short":3,"value_added":5.0,"education_req":4.0,"physical_demand":1.5},
    "0305": {"fulfillment":6.5,"ai_resistance":6.5,"value_added":4.5,"learning_cost":4.0,"education_req":4.0,"physical_demand":4.0},
    "0306": {"value_added":2.0,"ai_resistance":3.0,"learning_cost":1.5,"education_req":1.5,"stability":4.0,"social_status":2.5,"trend_short":-2,"trend_long":-2,"age":"16-25","edu":"无要求"},
    "0307": {"value_added":5.5,"social_status":5.5,"social_interaction":8.5,"ai_resistance":6.5,"intl_mobility":5.5,"learning_cost":4.0,"market_size":4.5},
    "0308": {"value_added":2.0,"ai_resistance":5.5,"learning_cost":1.5,"education_req":1.5,"social_status":2.5,"trend_long":-1,"trend_short":-2,"safety":5.5,"age":"18-30","edu":"无要求"},
    "0309": {"value_added":3.5,"stability":5.0,"social_status":4.0,"ai_resistance":5.0},
    "0310": {"growth_coeff":8.0,"trend_short":4,"value_added":5.5,"ai_resistance":5.5,"remote_friendly":5.0,"entrepreneurship":8.0,"social_interaction":8.0,"market_size":6.5},
    "0311": {"value_added":4.5,"stability":5.5,"social_status":4.5,"autonomy":5.5,"age":"25-35"},
    "0312": {"license_barrier":3.0,"value_added":3.5,"ai_resistance":5.5,"stability":5.5,"learning_cost":3.5},
    "0313": {"entrepreneurship":9.0,"autonomy":8.5,"fulfillment":6.5,"value_added":4.5,"growth_coeff":5.5,"trend_short":1},
    "0314": {"entrepreneurship":8.5,"autonomy":8.0,"fulfillment":7.0,"ai_resistance":7.5,"value_added":4.0,"physical_demand":4.5},
    # beauty_wellness
    "0401": {"social_interaction":8.0,"value_added":4.0,"ai_resistance":7.0,"entrepreneurship":7.0},
    "0402": {"physical_demand":7.0,"ai_resistance":8.5,"fulfillment":7.5,"value_added":5.0,"intl_mobility":5.0},
    "0403": {"education_req":6.5,"learning_cost":6.0,"license_barrier":5.0,"value_added":6.0,"social_status":6.0,"stability":6.5,"ai_resistance":6.5,"remote_friendly":5.0,"edu":"本科","age":"24-32"},
    "0404": {"physical_demand":7.0,"social_interaction":8.5,"growth_coeff":7.0,"trend_short":3,"value_added":5.0,"entrepreneurship":8.0,"stability":4.5},
    "0405": {"fulfillment":8.0,"growth_coeff":7.0,"trend_short":3,"entrepreneurship":8.5,"intl_mobility":5.5,"physical_demand":5.5,"value_added":4.5},
    "0406": {"growth_coeff":6.5,"trend_short":2,"value_added":4.5,"entrepreneurship":8.0,"market_size":4.5,"physical_demand":5.5},
    "0407": {"physical_demand":7.5,"ai_resistance":9.0,"value_added":4.5,"fulfillment":7.0,"license_barrier":3.5,"intl_mobility":5.0},
    "0408": {"growth_coeff":7.0,"trend_short":3,"ai_resistance":7.0,"value_added":5.0,"entrepreneurship":7.5,"social_interaction":8.0},
    "0409": {"remote_friendly":5.0,"value_added":5.0,"growth_coeff":6.5,"ai_resistance":6.0,"social_interaction":7.5},
    "0410": {"physical_demand":5.5,"safety":6.5,"ai_resistance":8.0,"value_added":4.0,"license_barrier":3.5,"cycle_sensitivity":5.5},
    "0411": {"ai_resistance":8.0,"market_size":4.0,"value_added":4.5,"fulfillment":7.0},
    "0412": {"ai_resistance":9.0,"physical_demand":7.0,"value_added":4.0,"market_size":5.0},
    "0413": {"growth_coeff":7.0,"trend_short":3,"value_added":5.0,"physical_demand":5.5,"social_interaction":8.0,"entrepreneurship":8.0},
    # domestic_care
    "0501": {"value_added":2.5,"social_status":2.5,"stability":4.5,"ai_resistance":8.5,"gender_equality":3.5,"intl_mobility":5.0},
    "0502": {"value_added":5.0,"growth_coeff":7.0,"trend_short":3,"social_status":4.5,"ai_resistance":9.0,"market_size":5.0,"gender_equality":3.0},
    "0503": {"value_added":3.5,"social_status":3.5,"ai_resistance":9.0,"gender_equality":3.5,"stability":4.5},
    "0504": {"education_req":5.0,"learning_cost":5.0,"value_added":5.0,"social_status":5.0,"ai_resistance":6.5,"remote_friendly":5.0,"physical_demand":2.0,"edu":"本科"},
    "0505": {"growth_coeff":7.5,"trend_short":4,"supply_demand":7.5,"value_added":3.5,"social_status":3.5,"ai_resistance":9.0,"burnout":7.0,"fulfillment":6.5},
    "0506": {"growth_coeff":7.0,"trend_short":3,"supply_demand":7.0,"value_added":3.5,"social_status":3.5,"ai_resistance":8.5,"burnout":6.5,"fulfillment":6.5},
    "0507": {"growth_coeff":7.0,"trend_short":3,"value_added":3.0,"ai_resistance":8.0,"social_interaction":8.0,"market_size":4.5},
    "0508": {"growth_coeff":7.0,"trend_short":3,"value_added":3.5,"fulfillment":6.5,"entrepreneurship":7.0,"ai_resistance":8.5,"physical_demand":5.5},
    "0509": {"value_added":4.5,"fulfillment":7.0,"entrepreneurship":7.5,"ai_resistance":8.5,"physical_demand":5.0,"learning_cost":4.5,"market_size":4.5},
    "0510": {"growth_coeff":6.5,"trend_short":2,"entrepreneurship":8.5,"value_added":4.0,"ai_resistance":7.5,"physical_demand":4.5,"market_size":3.5},
    "0511": {"value_added":6.5,"social_status":5.5,"ai_resistance":8.5,"learning_cost":5.0,"intl_mobility":6.5,"market_size":3.5,"social_interaction":7.5},
    "0512": {"fulfillment":7.5,"burnout":7.5,"ai_resistance":9.0,"value_added":3.5,"social_status":4.0,"safety":6.5},
    "0513": {"learning_cost":6.0,"value_added":6.0,"ai_resistance":8.5,"social_status":5.5,"entrepreneurship":8.0,"fulfillment":7.5,"intl_mobility":6.0},
    "0514": {"value_added":4.0,"social_status":4.5,"growth_coeff":7.0,"trend_short":3,"ai_resistance":7.5,"remote_friendly":4.5,"social_interaction":7.5},
    # platform_gig
    "0601": {"physical_demand":4.5,"safety":5.0,"value_added":3.0,"ai_resistance":5.0,"market_size":8.0,"trend_short":2,"social_interaction":4.5},
    "0602": {"physical_demand":6.0,"value_added":2.5,"ai_resistance":6.0,"social_interaction":5.0},
    "0603": {"remote_friendly":9.0,"value_added":5.0,"ai_resistance":5.0,"learning_cost":4.0,"education_req":4.0,"skill_versatility":7.0,"intl_mobility":6.0,"physical_demand":2.0},
    "0604": {"physical_demand":6.0,"value_added":2.5,"ai_resistance":5.5},
    "0605": {"market_size":3.5,"value_added":3.0,"social_interaction":7.0,"ai_resistance":6.5,"growth_coeff":5.5},
    "0606": {"physical_demand":6.5,"value_added":2.5,"ai_resistance":6.5,"safety":5.5,"market_size":5.0,"trend_short":1},
    "0607": {"social_interaction":7.0,"value_added":3.5,"ai_resistance":6.0,"intl_mobility":5.0,"entrepreneurship":7.0},
    "0608": {"remote_friendly":9.5,"ai_resistance":4.0,"value_added":3.5,"physical_demand":1.5,"growth_coeff":7.0,"trend_short":3,"social_interaction":6.5,"intl_mobility":6.0},
    "0609": {"physical_demand":7.0,"value_added":2.5,"ai_resistance":7.5,"stability":3.0,"cycle_sensitivity":6.0},
    # funeral
    "0701": {"social_status":5.0,"license_barrier":5.0,"stability":7.0,"value_added":5.5,"ai_resistance":8.5,"social_interaction":7.0,"entrepreneurship":6.0},
    "0702": {"ai_resistance":9.0,"physical_demand":5.5,"social_status":4.0,"value_added":4.5,"learning_cost":5.0,"fulfillment":5.5},
    "0703": {"stability":7.0,"value_added":4.0,"ai_resistance":7.5,"physical_demand":4.5,"social_interaction":5.0},
    "0704": {"education_req":6.0,"learning_cost":6.0,"value_added":5.5,"social_status":5.5,"ai_resistance":8.5,"remote_friendly":5.0,"fulfillment":7.0,"physical_demand":2.0,"license_barrier":4.5,"edu":"本科/硕士"},
    # special_legal
    "0801": {"physical_demand":6.0,"safety":3.5,"social_status":2.0,"stability":3.0,"ai_resistance":8.5,"burnout":7.0,"gender_equality":3.0,"fulfillment":3.0,"value_added":4.5,"cycle_sensitivity":3.5},
    "0802": {"learning_cost":3.5,"value_added":4.5,"social_status":4.0,"stability":5.0,"social_interaction":7.5,"ai_resistance":7.0,"license_barrier":5.5,"market_size":5.5},
    "0803": {"growth_coeff":7.0,"trend_short":4,"value_added":4.5,"stability":4.0,"license_barrier":6.0,"ai_resistance":7.0,"physical_demand":6.0,"market_size":4.5},
    "0804": {"value_added":2.5,"ai_resistance":5.5,"social_interaction":7.0,"stability":5.5,"learning_cost":1.5,"market_size":5.0},
    "0805": {"value_added":3.0,"social_status":3.0,"market_size":4.0,"trend_long":-1,"trend_short":-2,"ai_resistance":5.5,"stability":5.0},
    # cleaning_maintenance
    "0901": {"value_added":2.0,"social_status":2.0,"ai_resistance":7.0,"supply_demand":5.5,"physical_demand":7.0,"gender_equality":4.5},
    "0902": {"learning_cost":3.5,"value_added":3.5,"ai_resistance":7.5,"physical_demand":7.0,"skill_versatility":5.0,"supply_demand":5.5,"safety":5.5},
    "0903": {"fulfillment":5.5,"ai_resistance":7.5,"value_added":3.0,"entrepreneurship":6.5,"physical_demand":7.0,"cycle_sensitivity":5.0,"side_job_compat":6.0},
    "0904": {"license_barrier":3.0,"value_added":3.5,"ai_resistance":7.0,"safety":5.5,"physical_demand":6.0,"entrepreneurship":6.0},
    "0905": {"physical_demand":9.0,"safety":3.5,"value_added":4.0,"ai_resistance":8.0,"supply_demand":6.5,"age_flexibility":3.5,"career_lifespan":5.5},
    "0906": {"value_added":3.5,"entrepreneurship":6.5,"ai_resistance":7.0,"physical_demand":5.5,"cycle_sensitivity":5.0},
    "0907": {"ai_resistance":6.0,"value_added":2.5,"physical_demand":5.5,"market_size":5.0},
    "0908": {"ai_resistance":4.0,"trend_long":-2,"trend_short":-3,"value_added":2.0,"market_size":3.0,"social_status":2.0},
    "0909": {"ai_resistance":5.0,"trend_long":-1,"trend_short":-2,"value_added":2.0,"social_status":2.0},
    "0910": {"value_added":2.5,"ai_resistance":7.0,"entrepreneurship":5.5,"physical_demand":6.5},
    "0911": {"physical_demand":8.0,"safety":4.5,"value_added":3.0,"ai_resistance":7.5,"supply_demand":5.5},
    # security
    "1001": {"value_added":2.5,"social_status":3.5,"stability":5.5,"ai_resistance":6.5,"physical_demand":6.0,"burnout":5.5},
    "1002": {"value_added":6.0,"social_status":5.0,"ai_resistance":8.0,"physical_demand":7.5,"safety":4.5,"learning_cost":5.0,"market_size":4.0,"intl_mobility":5.5,"career_lifespan":5.5},
    "1003": {"value_added":2.5,"ai_resistance":5.0,"trend_short":-1,"stability":5.5,"social_interaction":6.0,"safety":6.5},
    "1004": {"learning_cost":5.0,"education_req":4.5,"value_added":5.5,"social_status":5.0,"ai_resistance":6.5,"autonomy":7.5,"entrepreneurship":8.0,"remote_friendly":4.0,"social_interaction":6.5,"license_barrier":4.5},
    "1005": {"learning_cost":4.5,"value_added":4.5,"ai_resistance":6.0,"growth_coeff":6.0,"trend_short":2,"supply_demand":6.0,"skill_versatility":5.5,"physical_demand":4.5},
    # customer_service
    "1101": {"ai_resistance":3.0,"value_added":3.0,"burnout":7.0,"social_interaction":8.5,"social_status":3.0},
    "1102": {"value_added":5.5,"social_status":5.0,"autonomy":6.0,"stability":6.0,"ai_resistance":5.0,"age":"28-38","edu":"本科"},
    "1103": {"burnout":7.5,"social_interaction":8.5,"ai_resistance":4.0,"value_added":3.0,"fulfillment":3.0},
    "1104": {"learning_cost":4.5,"education_req":4.5,"value_added":4.5,"ai_resistance":4.5,"growth_coeff":5.0,"remote_friendly":7.5,"skill_versatility":6.0},
    "1105": {"remote_friendly":8.5,"ai_resistance":2.5,"value_added":2.5,"trend_short":-3,"social_interaction":6.5,"physical_demand":1.0},
    # office_admin
    "1201": {"social_interaction":6.5,"value_added":3.5,"ai_resistance":3.5,"gender_equality":4.5,"stability":5.5},
    "1202": {"social_interaction":7.5,"value_added":3.0,"ai_resistance":5.0,"trend_short":-1,"social_status":3.5,"physical_demand":2.5},
    "1203": {"value_added":5.0,"social_status":5.0,"autonomy":6.5,"stability":6.0,"ai_resistance":5.0,"age":"28-38"},
    "1204": {"ai_resistance":3.5,"value_added":3.5,"social_interaction":7.0,"remote_friendly":7.0},
    "1205": {"ai_resistance":2.5,"trend_long":-3,"trend_short":-4,"value_added":2.5,"social_status":3.0,"market_size":4.5},
    # wedding_events
    "1301": {"entrepreneurship":8.5,"social_interaction":9.0,"fulfillment":7.5,"value_added":5.0,"autonomy":7.5,"social_status":5.5,"intl_mobility":5.0},
    "1302": {"social_interaction":9.5,"fulfillment":7.5,"value_added":5.0,"social_status":5.5,"ai_resistance":8.0,"side_job_compat":7.0},
    "1303": {"social_interaction":8.5,"value_added":3.5,"ai_resistance":6.5,"cycle_sensitivity":7.5},
    "1304": {"fulfillment":7.5,"ai_resistance":8.0,"entrepreneurship":8.0,"value_added":4.5,"physical_demand":5.0,"cycle_sensitivity":7.5},
    "1305": {"physical_demand":6.0,"social_status":4.5,"value_added":4.5,"safety":6.0,"gender_equality":4.0,"ai_resistance":7.0},
    # recreation
    "1401": {"fulfillment":8.0,"ai_resistance":7.0,"entrepreneurship":8.5,"growth_coeff":7.0,"trend_short":3,"value_added":5.0,"remote_friendly":4.0,"learning_cost":5.0},
    "1402": {"learning_cost":2.0,"value_added":2.5,"safety":5.0,"ai_resistance":6.5,"social_status":3.0,"social_interaction":7.5,"age":"18-28","edu":"无要求"},
    "1403": {"value_added":4.5,"stability":5.0,"entrepreneurship":7.0,"social_interaction":7.0,"ai_resistance":7.0},
    "1404": {"value_added":5.0,"social_status":5.5,"stability":5.5,"physical_demand":5.0,"ai_resistance":7.0,"market_size":4.5},
    "1405": {"value_added":4.5,"social_interaction":7.5,"ai_resistance":7.0,"market_size":4.5},
    "1406": {"physical_demand":7.5,"safety":5.0,"fulfillment":8.5,"intl_mobility":6.5,"ai_resistance":9.0,"value_added":5.0,"license_barrier":4.5,"learning_cost":5.5},
    "1407": {"physical_demand":7.0,"safety":5.5,"fulfillment":8.0,"intl_mobility":6.0,"ai_resistance":9.0,"value_added":5.0,"cycle_sensitivity":8.0,"license_barrier":4.0,"learning_cost":5.0},
    "1408": {"physical_demand":6.5,"fulfillment":8.0,"ai_resistance":9.0,"value_added":5.5,"social_status":5.5,"market_size":4.0,"learning_cost":5.5,"license_barrier":4.0},
    "1409": {"physical_demand":7.5,"safety":5.5,"fulfillment":8.0,"growth_coeff":6.5,"trend_short":2,"ai_resistance":9.0,"value_added":4.5,"license_barrier":4.0},
    "1410": {"safety":5.0,"license_barrier":5.5,"ai_resistance":8.5,"value_added":4.5,"market_size":3.5,"physical_demand":4.5},
    "1411": {"physical_demand":6.5,"safety":4.0,"fulfillment":8.5,"ai_resistance":9.0,"value_added":5.0,"market_size":3.5,"license_barrier":5.0,"career_lifespan":5.5},
    "1412": {"growth_coeff":7.5,"trend_short":3,"value_added":5.0,"remote_friendly":5.0,"social_interaction":8.0,"ai_resistance":6.5,"physical_demand":3.0},
    "1413": {"learning_cost":5.5,"value_added":4.5,"ai_resistance":7.5,"physical_demand":6.5,"skill_versatility":5.5,"market_size":3.5,"safety":5.5},
    "1414": {"growth_coeff":7.0,"trend_short":3,"value_added":4.5,"fulfillment":7.0,"entrepreneurship":8.0,"ai_resistance":7.5,"social_interaction":7.0,"market_size":4.0},
}

# === Build occupation base scores ===
def occ_base(occ_id, mid):
    d = dict(MID_DEFAULTS[mid])
    ovr = OVR.get(occ_id, {})
    d.update(ovr)
    return d

# === SCORING ===
def clamp(val, lo=0.0, hi=10.0):
    return max(lo, min(hi, round(val, 1)))

def clamp5(val):
    return max(0.0, min(5.0, round(val, 1)))

def apply_country_modifiers(base, cp, occ):
    s = dict(base)
    svc_f = (cp["svc"] - 7.0) / 3.0
    tour_f = (cp["tour"] - 7.0) / 3.0
    ret_f = (cp["ret"] - 7.0) / 3.0
    gig_f = (cp["gig"] - 6.0) / 4.0
    care_f = (cp["care"] - 6.0) / 4.0
    hosp_f = (cp["hosp"] - 5.0) / 5.0
    tip_f = (cp["tip"] - 5.0) / 5.0
    comp_f = (cp["comp"] - 5.0) / 5.0
    stab_f = (cp["stab"] - 5.5) / 4.5
    wlb_f = (cp["wlb"] - 6.0) / 4.0
    gender_f = (cp["gender"] - 5.5) / 4.5
    edu_f = (cp["edu"] - 6.0) / 4.0
    intl_f = (cp["intl"] - 6.0) / 4.0
    reg_f = (cp["reg"] - 5.5) / 4.5

    mid = occ["mid"]
    # Sector-specific factors
    if mid in ("food_beverage",):
        sector_f = (svc_f + hosp_f) / 2
    elif mid in ("hospitality_tourism",):
        sector_f = (tour_f + hosp_f) / 2
    elif mid in ("retail",):
        sector_f = ret_f
    elif mid in ("beauty_wellness",):
        sector_f = (svc_f + care_f) / 2
    elif mid in ("domestic_care",):
        sector_f = care_f
    elif mid in ("platform_gig",):
        sector_f = gig_f
    elif mid in ("funeral",):
        sector_f = svc_f * 0.3  # funeral is less market-dependent
    elif mid in ("special_legal",):
        sector_f = (svc_f + reg_f) / 2
    elif mid in ("cleaning_maintenance",):
        sector_f = svc_f * 0.5
    elif mid in ("security",):
        sector_f = svc_f * 0.5
    elif mid in ("customer_service",):
        sector_f = (svc_f + ret_f) / 2
    elif mid in ("office_admin",):
        sector_f = svc_f * 0.4
    elif mid in ("wedding_events",):
        sector_f = (svc_f + tour_f) / 2
    elif mid in ("recreation",):
        sector_f = (tour_f + svc_f) / 2
    else:
        sector_f = svc_f

    s["value_added"] = clamp(s["value_added"] + comp_f * 2.0 + hosp_f * 0.5)
    s["cost_performance"] = clamp(s["cost_performance"] + comp_f * 0.8 + svc_f * 0.3)
    s["growth_coeff"] = clamp(s["growth_coeff"] + sector_f * 0.8 + svc_f * 0.2)
    s["career_lifespan"] = clamp(s["career_lifespan"] + stab_f * 0.6)
    s["opportunity"] = clamp(s["opportunity"] + sector_f * 1.2 + svc_f * 0.3)
    s["market_size"] = clamp(s["market_size"] + sector_f * 1.5 + svc_f * 0.3)
    s["supply_demand"] = clamp(s["supply_demand"] + sector_f * 0.6 + care_f * 0.3)
    dev_bonus = 0.8 if cp["hosp"] >= 7.0 else (0.0 if cp["hosp"] >= 4.5 else -0.8)
    s["developed_scarcity"] = clamp(s["developed_scarcity"] + dev_bonus)
    s["stability"] = clamp(s["stability"] + stab_f * 1.5 + reg_f * 0.3)
    s["safety"] = clamp(s["safety"] + wlb_f * 0.3 + reg_f * 0.3)
    s["occupational_disease"] = clamp(s["occupational_disease"] + wlb_f * 0.5)
    s["overtime"] = clamp(s["overtime"] + (cp["ot"] - 5.0) / 5.0 * 2.5)
    s["burnout"] = clamp(s["burnout"] + (cp["ot"] - 5.0) / 5.0 * 1.5)
    s["remote_friendly"] = clamp(s["remote_friendly"] + wlb_f * 0.3)
    s["autonomy"] = clamp(s["autonomy"] + wlb_f * 0.4 + svc_f * 0.15)
    s["family_friendly"] = clamp(s["family_friendly"] + wlb_f * 1.5)
    s["social_status"] = clamp(s["social_status"] + comp_f * 0.5 + hosp_f * 0.3)
    s["fulfillment"] = clamp(s["fulfillment"] + svc_f * 0.2)
    s["gender_equality"] = clamp(s["gender_equality"] + gender_f * 2.0)
    s["age_flexibility"] = clamp(s["age_flexibility"] + wlb_f * 0.3 + svc_f * 0.15)
    s["entrepreneurship"] = clamp(s["entrepreneurship"] + svc_f * 0.4 + reg_f * 0.3)
    s["intl_mobility"] = clamp(s["intl_mobility"] + intl_f * 1.5)
    s["ai_resistance"] = clamp(s["ai_resistance"] + svc_f * 0.1)
    s["learning_cost"] = clamp(s["learning_cost"] + edu_f * 0.2)
    s["education_req"] = clamp(s["education_req"] + edu_f * 0.2)
    s["license_barrier"] = clamp(s["license_barrier"] + reg_f * 0.4)
    s["cycle_sensitivity"] = clamp(s["cycle_sensitivity"] - stab_f * 0.5)
    s["side_job_compat"] = clamp(s["side_job_compat"] + wlb_f * 0.3)
    s["industry_monopoly"] = clamp(s["industry_monopoly"] - svc_f * 0.2 + (1 - cp["reg"] / 10.0) * 0.3)
    s["skill_versatility"] = clamp(s["skill_versatility"] + svc_f * 0.3)
    s["career_switch"] = clamp(s["career_switch"] + svc_f * 0.2)
    rep_adj = -0.3 if cp["hosp"] >= 7.0 else (0.3 if cp["hosp"] < 4.0 else 0.0)
    s["reputation_variance"] = clamp5(s["reputation_variance"] + rep_adj)

    # Tipping culture bonus for food/hospitality
    if mid in ("food_beverage", "hospitality_tourism"):
        s["value_added"] = clamp(s["value_added"] + tip_f * 0.8)
        s["cost_performance"] = clamp(s["cost_performance"] + tip_f * 0.4)
    # Care demand boost for domestic_care
    if mid == "domestic_care":
        s["supply_demand"] = clamp(s["supply_demand"] + care_f * 0.8)
        s["growth_coeff"] = clamp(s["growth_coeff"] + care_f * 0.5)
        s["opportunity"] = clamp(s["opportunity"] + care_f * 0.5)
    # Gig economy boost for platform_gig
    if mid == "platform_gig":
        s["opportunity"] = clamp(s["opportunity"] + gig_f * 1.0)
        s["market_size"] = clamp(s["market_size"] + gig_f * 1.0)
        s["stability"] = clamp(s["stability"] - abs(gig_f) * 0.3)
    # Tourism cycle sensitivity for hospitality/recreation
    if mid in ("hospitality_tourism", "recreation", "wedding_events"):
        s["cycle_sensitivity"] = clamp(s["cycle_sensitivity"] + tour_f * 0.5)
    return s

def get_trends(base, cp):
    t_long = base["trend_long"]
    t_short = base["trend_short"]
    if cp.get("svc", 7) >= 8.5:
        t_short = min(5, t_short + 1)
    elif cp.get("svc", 7) < 5.5:
        t_short = max(-5, t_short - 1)
    if cp["tour"] >= 8.5:
        t_long = min(5, t_long + 1)
    elif cp["tour"] < 5.0:
        t_long = max(-5, t_long - 1)
    return t_long, t_short

def get_demand_direction(t):
    if t >= 4: return "up_strong"
    elif t >= 2: return "up"
    elif t >= -1: return "stable"
    elif t >= -3: return "down"
    else: return "down_strong"

def get_ai_timeline(ai_r):
    if ai_r >= 7.5: return "2035+"
    elif ai_r >= 6.0: return "2032-2038"
    elif ai_r >= 4.5: return "2028-2033"
    elif ai_r >= 3.0: return "2026-2030"
    else: return "2025-2028"

def generate_summary(occ, country, scores, trend_5yr):
    hz, he = [], []
    if scores["value_added"] >= 8.0: hz.append("薪资回报高"); he.append("high compensation")
    elif scores["value_added"] <= 4.5: hz.append("薪资水平偏低"); he.append("relatively low pay")
    if scores["supply_demand"] >= 7.5: hz.append("人才需求旺盛"); he.append("strong talent demand")
    elif scores["supply_demand"] <= 4.0: hz.append("供过于求"); he.append("oversupply of talent")
    if scores["ai_resistance"] <= 4.0: hz.append("AI替代风险较高"); he.append("high AI displacement risk")
    elif scores["ai_resistance"] >= 7.5: hz.append("AI替代抗性强"); he.append("strong AI resistance")
    if scores["reputation_variance"] >= 3.5: hz.append("收入/口碑分化大"); he.append("high income/reputation variance")
    if scores["stability"] <= 3.5: hz.append("就业波动大"); he.append("volatile employment")
    elif scores["stability"] >= 7.5: hz.append("就业稳定"); he.append("stable employment")
    if scores["fulfillment"] >= 8.0: hz.append("职业成就感高"); he.append("high career fulfillment")
    if trend_5yr >= 4: hz.append("近年增长迅猛"); he.append("rapid recent growth")
    elif trend_5yr <= -2: hz.append("近年需求下降"); he.append("declining demand")
    hz, he = hz[:3], he[:3]
    if not hz: hz, he = ["发展平稳"], ["steady development"]
    return (f"{country['name_zh']}{occ['zh']}：{'，'.join(hz)}",
            f"{country['name_en']} {occ['en']}: {', '.join(he)}")

# === HEADERS & DIMS ===
HEADERS = [
    "id","major_category","major_code","mid_category","sub_category",
    "sub_category_en","isco_code","onet_code","region","country_or_region",
    "iso_code","type","employer_type","typical_education","typical_entry_age",
    "locality","learning_cost","education_req","growth_coeff","career_lifespan",
    "opportunity","market_size","supply_demand","developed_scarcity",
    "value_added","cost_performance","stability","safety","occupational_disease",
    "overtime","burnout","skill_versatility","career_switch","reputation_variance",
    "ai_resistance","social_status","remote_friendly","autonomy","family_friendly",
    "fulfillment","entrepreneurship","gender_equality","age_flexibility",
    "social_interaction","physical_demand","license_barrier","cycle_sensitivity",
    "side_job_compat","intl_mobility","industry_monopoly","trend_2000_2026",
    "trend_5yr","demand_direction","ai_timeline","composite_index",
    "summary_zh","summary_en","data_source"
]
SCORE_DIMS = [
    "learning_cost","education_req","growth_coeff","career_lifespan",
    "opportunity","market_size","supply_demand","developed_scarcity",
    "value_added","cost_performance","stability","safety","occupational_disease",
    "overtime","burnout","skill_versatility","career_switch","reputation_variance",
    "ai_resistance","social_status","remote_friendly","autonomy","family_friendly",
    "fulfillment","entrepreneurship","gender_equality","age_flexibility",
    "social_interaction","physical_demand","license_barrier","cycle_sensitivity",
    "side_job_compat","intl_mobility","industry_monopoly"
]

def main():
    random.seed(42)
    weights = load_weights()
    csv_path = PROJECT_ROOT / "data" / "csv" / "service_consumer.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for occ in OCCUPATIONS:
        base = occ_base(occ["id"], occ["mid"])
        for country in COUNTRIES:
            iso = country["iso"]
            cp = CP[iso]
            scores = apply_country_modifiers(base, cp, occ)
            rng = random.Random(hash(f"SVC-{occ['id']}-{iso}") % 10000)
            for dim in SCORE_DIMS:
                if dim == "reputation_variance":
                    scores[dim] = clamp5(scores[dim] + rng.uniform(-0.2, 0.2))
                elif dim == "safety":
                    scores[dim] = clamp(scores[dim] + rng.uniform(-0.1, 0.1))
                else:
                    scores[dim] = clamp(scores[dim] + rng.uniform(-0.3, 0.3))
            trend_long, trend_short = get_trends(base, cp)
            demand_dir = get_demand_direction(trend_short)
            ai_tl = get_ai_timeline(scores["ai_resistance"])
            score_dict = {dim: scores[dim] for dim in weights}
            composite = calculate_composite(score_dict, weights)
            summary_zh, summary_en = generate_summary(occ, country, scores, trend_short)
            row_id = f"SVC-{occ['id']}-{iso}-general"
            row = {
                "id": row_id,
                "major_category": "服务业与消费",
                "major_code": "SVC",
                "mid_category": occ["mid_zh"],
                "sub_category": occ["zh"],
                "sub_category_en": occ["en"],
                "isco_code": occ["isco"],
                "onet_code": occ["onet"],
                "region": country["region"],
                "country_or_region": country["name_zh"],
                "iso_code": iso,
                "type": country["type"],
                "employer_type": "general",
                "typical_education": base.get("edu", "专科"),
                "typical_entry_age": base.get("age", "20-30"),
                "locality": occ["locality"],
            }
            for dim in SCORE_DIMS:
                row[dim] = scores[dim]
            row["trend_2000_2026"] = trend_long
            row["trend_5yr"] = trend_short
            row["demand_direction"] = demand_dir
            row["ai_timeline"] = ai_tl
            row["composite_index"] = composite
            row["summary_zh"] = summary_zh
            row["summary_en"] = summary_en
            row["data_source"] = "AI综合评估 + O*NET/ILO/OECD锚点校准"
            rows.append(row)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated {len(rows)} rows to {csv_path}")
    print(f"Occupations: {len(OCCUPATIONS)}, Countries: {len(COUNTRIES)}")

    # JSON
    from tools.csv_to_json import convert_csv_to_json
    json_path = PROJECT_ROOT / "data" / "json" / "service_consumer.json"
    convert_csv_to_json(str(csv_path), str(json_path))
    print(f"JSON written to {json_path}")

    # Notebook
    from tools.generate_notebook import create_data_notebook
    nb_path = PROJECT_ROOT / "notebooks" / "11_service_consumer.ipynb"
    create_data_notebook(
        str(csv_path), str(nb_path),
        title="服务业与消费 (SVC) — 完整数据",
        description="141 occupations x 45 countries/regions = 6,345 rows",
    )
    print(f"Notebook written to {nb_path}")


if __name__ == "__main__":
    main()
