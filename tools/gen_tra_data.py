#!/usr/bin/env python3
"""Generate transport_logistics.csv — TRA data for Global Career Development Index."""
import csv, sys, random, json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from tools.score_calculator import load_weights, calculate_composite

# === OCCUPATIONS (72) from categories.yaml TRA ===
O = []
def _a(mid, mid_zh, mid_en, items):
    for id_, zh, en, isco, onet, loc in items:
        O.append({"id": id_, "mid": mid, "mid_zh": mid_zh, "mid_en": mid_en,
                   "zh": zh, "en": en, "isco": isco, "onet": onet, "locality": loc})

_a("aviation", "航空", "Aviation", [
    ("0101","民航飞行员","Commercial Airline Pilot","3153","53-2011.00","global"),
    ("0102","空中乘务员","Flight Attendant","5111","53-2031.00","global"),
    ("0103","航空管制员","Air Traffic Controller","3154","53-2021.00","global"),
    ("0104","机场运营经理","Airport Operations Manager","1324","11-3071.01","global"),
    ("0105","飞机维修工程师","Aircraft Maintenance Engineer","7232","49-3011.00","global"),
    ("0106","飞行签派员","Flight Dispatcher","3154","53-2022.00","global"),
    ("0107","货机飞行员","Cargo Pilot","3153","53-2011.00","global"),
    ("0108","直升机飞行员","Helicopter Pilot","3153","53-2012.00","global"),
    ("0109","航空地勤","Airport Ground Crew","5111","53-2031.00","global"),
    ("0110","机务人员","Aircraft Mechanic","7232","49-3011.00","global"),
    ("0111","航空货运代理","Air Cargo Agent","3331","43-5011.01","global"),
    ("0112","航空安全检查员","Aviation Safety Inspector","3154","53-6051.07","global"),
    ("0113","飞行教官(民航)","Certified Flight Instructor","3153","25-3021.00","global"),
])
_a("maritime", "航海", "Maritime", [
    ("0201","船长","Ship Captain / Master Mariner","3151","53-5021.00","global"),
    ("0202","大副/二副","Chief/Second Officer (Mate)","3151","53-5021.00","global"),
    ("0203","轮机长","Chief Engineer (Marine)","3151","53-5031.00","global"),
    ("0204","普通海员","Able Seaman","8350","53-5011.00","global"),
    ("0205","港口管理人员","Port Manager","1324","11-3071.01","global"),
    ("0206","引航员","Marine Pilot / Harbor Pilot","3151","53-5021.02","global"),
    ("0207","船舶检验师","Marine Surveyor","3151","53-5021.00","global"),
    ("0208","邮轮乘务员","Cruise Ship Crew","5111","53-2031.00","global"),
    ("0209","船舶调度员","Vessel Traffic Controller","3151","53-5021.02","global"),
    ("0210","海洋救助员","Maritime Search & Rescue Worker","5419","33-2011.00","global"),
    ("0211","船舶代理人","Ship Broker / Shipping Agent","3331","43-5011.01","global"),
])
_a("railway", "铁路", "Railway", [
    ("0301","列车司机","Train Driver / Locomotive Engineer","8311","53-4011.00","global"),
    ("0302","铁路调度员","Railway Dispatcher","4323","43-5032.00","global"),
    ("0303","铁路维护工程师","Railway Maintenance Engineer","7233","49-9097.00","global"),
    ("0304","高铁技术工程师","High-Speed Rail Engineer","2144","17-2141.00","global"),
    ("0305","列车长/车务员","Train Conductor","8311","53-4031.00","global"),
    ("0306","地铁运营员","Metro Operations Staff","8311","53-4011.00","global"),
    ("0307","信号工程师(铁路)","Railway Signal Engineer","2151","17-2071.00","global"),
    ("0308","铁路客运服务员","Railway Passenger Service Agent","5111","43-4181.00","global"),
    ("0309","轨道车辆工程师","Rolling Stock Engineer","2144","17-2141.00","global"),
])
_a("road_transport", "公路", "Road Transport", [
    ("0401","长途卡车司机","Long-haul Truck Driver","8332","53-3032.00","global"),
    ("0402","公交车司机","Bus Driver","8331","53-3052.00","global"),
    ("0403","出租车司机","Taxi Driver","8322","53-3054.00","global"),
    ("0404","驾校教练","Driving Instructor","5165","25-3021.00","global"),
    ("0405","特种车辆驾驶员","Specialized Vehicle Driver","8332","53-3032.00","global"),
    ("0406","道路救援员","Roadside Assistance Technician","8332","49-3023.00","global"),
    ("0407","摩托车信使","Motorcycle Courier","8322","53-3054.00","global"),
    ("0408","校车司机","School Bus Driver","8331","53-3051.00","global"),
    ("0409","拖车司机/重型运输司机","Tow Truck / Heavy Hauler Driver","8332","53-3032.00","global"),
    ("0410","搬家工人","Moving Company Worker / Mover","9333","53-7062.00","global"),
])
_a("logistics_mgmt", "物流管理", "Logistics Management", [
    ("0501","仓储经理","Warehouse Manager","1324","11-3071.02","global"),
    ("0502","物流经理","Logistics Manager","1324","11-3071.01","global"),
    ("0503","报关员","Customs Broker","3331","13-1041.06","global"),
    ("0504","货运代理人","Freight Forwarder","3331","43-5011.01","global"),
    ("0505","仓库管理员","Warehouse Operative / Stocker","9321","53-7065.00","global"),
    ("0506","物流分析师","Logistics Analyst","2413","13-1081.01","global"),
    ("0507","跨境电商物流专员","Cross-border E-commerce Logistics Specialist","3331","43-5011.01","global"),
    ("0508","叉车操作员","Forklift Operator","8344","53-7051.00","global"),
    ("0509","冷链物流专员","Cold Chain Logistics Specialist","1324","11-3071.02","global"),
    ("0510","物流自动化工程师","Logistics Automation Engineer","2141","17-2112.00","global"),
    ("0511","危险品运输管理员","Hazardous Materials Transport Manager","1324","53-1044.00","global"),
])
_a("last_mile", "快递最后一公里", "Last-Mile Delivery", [
    ("0601","快递员","Courier / Delivery Driver","9321","53-7065.00","global"),
    ("0602","外卖骑手","Food Delivery Rider","9321","53-7065.00","global"),
    ("0603","同城配送员","Same-City Express Courier","9321","53-7065.00","global"),
    ("0604","快递站长","Delivery Station Manager","1324","11-3071.02","global"),
    ("0605","达巴瓦拉(印度送餐人)","Dabbawala (Mumbai Lunchbox Deliverer)","9321","","country_specific"),
    ("0606","包裹柜运维员","Parcel Locker Technician","9321","49-9071.00","global"),
])
_a("urban_transport", "城市交通", "Urban Transportation", [
    ("0701","交通规划师","Transportation Planner","2164","19-3051.00","global"),
    ("0702","交通工程师","Traffic Engineer","2142","17-2051.00","global"),
    ("0703","停车场管理员","Parking Manager / Attendant","5419","53-6021.00","global"),
    ("0704","共享出行运营经理","Shared Mobility Operations Manager","1324","11-3071.01","global"),
    ("0705","自动驾驶安全员","Autonomous Vehicle Safety Operator","8322","53-3054.00","global"),
    ("0706","交通信号技术员","Traffic Signal Technician","7412","49-2098.00","global"),
])
_a("pipeline_transport", "管道运输", "Pipeline Transport", [
    ("0801","管道运行工","Pipeline Operator","3132","53-7072.00","global"),
    ("0802","管道检测技师","Pipeline Inspection Technician","3132","53-7072.00","global"),
    ("0803","管道调度员","Pipeline Dispatcher","3132","43-5032.00","global"),
])
_a("space_transport", "太空运输", "Space Transport", [
    ("0901","商业航天飞行员","Commercial Space Pilot","3153","53-2011.00","global"),
    ("0902","航天任务控制员","Mission Control Specialist","3154","53-2021.00","global"),
    ("0903","太空旅游顾问","Space Tourism Consultant","4221","41-3041.00","global"),
])

OCCUPATIONS = O

# === COUNTRIES (same 45) ===
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

# === COUNTRY PROFILES for TRA ===
# Keys: avi(aviation hub), ship(shipping hub), rail(rail network), road(road infra),
#   logi(logistics index), drv_pay(driver pay), safe(safety standards),
#   comp(compensation), wlb(work-life balance), stab(stability),
#   edu(edu quality), intl(international openness), gender(gender equality),
#   reg(regulatory), ot(overtime culture, higher=less OT)
CP = {
    "US": {"avi":9.5,"ship":7.0,"rail":5.0,"road":9.0,"logi":9.0,"drv_pay":7.5,"safe":8.0,"comp":8.5,"wlb":6.0,"stab":6.0,"edu":9.0,"intl":8.5,"gender":7.5,"reg":7.0,"ot":5.0},
    "GB": {"avi":8.5,"ship":8.0,"rail":7.0,"road":7.5,"logi":8.5,"drv_pay":7.0,"safe":8.5,"comp":7.5,"wlb":7.0,"stab":7.0,"edu":8.5,"intl":9.0,"gender":7.5,"reg":7.5,"ot":6.5},
    "FR": {"avi":7.5,"ship":6.5,"rail":8.5,"road":8.0,"logi":7.5,"drv_pay":6.5,"safe":8.0,"comp":7.0,"wlb":8.0,"stab":7.0,"edu":8.0,"intl":7.5,"gender":7.0,"reg":7.5,"ot":7.0},
    "DE": {"avi":8.0,"ship":7.5,"rail":8.5,"road":9.0,"logi":9.5,"drv_pay":7.5,"safe":9.0,"comp":8.0,"wlb":8.0,"stab":8.0,"edu":8.5,"intl":8.0,"gender":7.0,"reg":8.0,"ot":7.5},
    "JP": {"avi":8.0,"ship":8.5,"rail":9.5,"road":8.0,"logi":9.0,"drv_pay":6.0,"safe":9.5,"comp":7.0,"wlb":4.5,"stab":7.5,"edu":8.0,"intl":5.0,"gender":5.0,"reg":8.0,"ot":3.5},
    "KR": {"avi":7.5,"ship":9.0,"rail":8.0,"road":8.0,"logi":8.5,"drv_pay":5.5,"safe":8.0,"comp":6.5,"wlb":4.0,"stab":6.5,"edu":8.0,"intl":6.0,"gender":4.5,"reg":7.0,"ot":3.0},
    "CN": {"avi":8.5,"ship":9.5,"rail":9.5,"road":8.5,"logi":8.0,"drv_pay":4.5,"safe":6.5,"comp":6.0,"wlb":3.5,"stab":5.5,"edu":7.5,"intl":5.0,"gender":5.5,"reg":6.0,"ot":2.5},
    "TW": {"avi":6.0,"ship":7.5,"rail":7.0,"road":7.5,"logi":7.0,"drv_pay":5.0,"safe":7.5,"comp":5.5,"wlb":5.0,"stab":6.0,"edu":7.5,"intl":6.5,"gender":6.0,"reg":6.5,"ot":4.0},
    "HK": {"avi":8.5,"ship":9.0,"rail":7.5,"road":7.0,"logi":8.5,"drv_pay":6.0,"safe":8.5,"comp":7.0,"wlb":4.5,"stab":6.5,"edu":7.5,"intl":9.0,"gender":6.5,"reg":7.0,"ot":3.5},
    "SG": {"avi":9.5,"ship":9.5,"rail":7.0,"road":8.0,"logi":9.5,"drv_pay":6.5,"safe":9.5,"comp":8.0,"wlb":5.5,"stab":8.0,"edu":8.5,"intl":9.5,"gender":7.0,"reg":8.5,"ot":4.5},
    "IN": {"avi":6.5,"ship":7.0,"rail":8.0,"road":5.5,"logi":5.5,"drv_pay":2.5,"safe":4.0,"comp":4.0,"wlb":4.5,"stab":5.0,"edu":7.0,"intl":7.0,"gender":4.0,"reg":5.0,"ot":4.0},
    "TH": {"avi":6.0,"ship":6.5,"rail":4.5,"road":6.5,"logi":6.0,"drv_pay":3.0,"safe":5.0,"comp":3.5,"wlb":5.5,"stab":5.5,"edu":5.5,"intl":5.5,"gender":6.0,"reg":5.0,"ot":5.5},
    "VN": {"avi":5.0,"ship":7.0,"rail":4.0,"road":5.5,"logi":5.5,"drv_pay":2.5,"safe":4.5,"comp":3.0,"wlb":5.0,"stab":5.0,"edu":5.5,"intl":5.5,"gender":5.5,"reg":5.0,"ot":4.5},
    "ID": {"avi":5.5,"ship":7.5,"rail":4.0,"road":5.5,"logi":5.0,"drv_pay":2.5,"safe":4.0,"comp":3.5,"wlb":5.5,"stab":5.0,"edu":5.0,"intl":4.5,"gender":5.0,"reg":5.0,"ot":5.0},
    "MY": {"avi":6.0,"ship":8.0,"rail":5.0,"road":7.0,"logi":6.5,"drv_pay":3.5,"safe":6.0,"comp":4.5,"wlb":5.5,"stab":6.0,"edu":6.0,"intl":6.5,"gender":5.5,"reg":5.5,"ot":5.0},
    "PH": {"avi":5.0,"ship":6.5,"rail":3.0,"road":4.5,"logi":5.0,"drv_pay":2.5,"safe":4.0,"comp":3.0,"wlb":5.0,"stab":4.5,"edu":5.5,"intl":6.5,"gender":6.5,"reg":4.5,"ot":4.5},
    "PK": {"avi":4.0,"ship":5.0,"rail":4.5,"road":4.0,"logi":4.0,"drv_pay":2.0,"safe":3.0,"comp":2.5,"wlb":4.5,"stab":3.5,"edu":4.5,"intl":4.5,"gender":3.0,"reg":4.0,"ot":4.5},
    "BD": {"avi":3.5,"ship":6.0,"rail":3.5,"road":3.5,"logi":3.5,"drv_pay":1.5,"safe":2.5,"comp":2.0,"wlb":4.5,"stab":3.5,"edu":4.0,"intl":4.5,"gender":3.5,"reg":3.5,"ot":4.5},
    "AE": {"avi":9.5,"ship":9.0,"rail":5.5,"road":8.5,"logi":9.0,"drv_pay":6.0,"safe":8.5,"comp":8.0,"wlb":5.5,"stab":7.0,"edu":7.0,"intl":8.5,"gender":5.5,"reg":7.0,"ot":5.0},
    "IL": {"avi":6.5,"ship":6.0,"rail":5.0,"road":7.0,"logi":6.5,"drv_pay":6.0,"safe":7.5,"comp":7.5,"wlb":6.0,"stab":5.5,"edu":8.5,"intl":8.0,"gender":7.0,"reg":6.5,"ot":5.0},
    "SA": {"avi":7.0,"ship":7.5,"rail":6.0,"road":7.5,"logi":6.5,"drv_pay":5.0,"safe":6.0,"comp":6.5,"wlb":5.5,"stab":6.0,"edu":6.0,"intl":5.5,"gender":3.5,"reg":6.0,"ot":5.0},
    "TR": {"avi":7.0,"ship":7.5,"rail":6.5,"road":7.0,"logi":6.5,"drv_pay":3.5,"safe":5.5,"comp":4.0,"wlb":5.0,"stab":4.0,"edu":6.5,"intl":5.5,"gender":4.5,"reg":5.5,"ot":4.5},
    "NL": {"avi":8.0,"ship":9.5,"rail":7.5,"road":8.5,"logi":9.5,"drv_pay":7.0,"safe":9.0,"comp":7.5,"wlb":9.0,"stab":7.5,"edu":8.0,"intl":9.0,"gender":8.5,"reg":7.5,"ot":8.0},
    "CH": {"avi":7.0,"ship":4.0,"rail":9.0,"road":8.5,"logi":8.0,"drv_pay":9.0,"safe":9.5,"comp":9.5,"wlb":8.5,"stab":9.0,"edu":9.0,"intl":8.5,"gender":7.0,"reg":7.5,"ot":7.5},
    "SE": {"avi":6.5,"ship":7.0,"rail":7.5,"road":8.0,"logi":8.0,"drv_pay":7.5,"safe":9.0,"comp":7.0,"wlb":9.0,"stab":8.0,"edu":8.5,"intl":8.5,"gender":9.0,"reg":7.5,"ot":8.5},
    "DK": {"avi":6.0,"ship":8.5,"rail":7.0,"road":8.0,"logi":8.0,"drv_pay":7.5,"safe":9.0,"comp":7.0,"wlb":9.0,"stab":8.0,"edu":8.5,"intl":8.5,"gender":9.0,"reg":7.5,"ot":8.5},
    "FI": {"avi":5.5,"ship":7.0,"rail":6.5,"road":7.5,"logi":7.5,"drv_pay":6.5,"safe":9.0,"comp":6.5,"wlb":9.0,"stab":7.5,"edu":9.0,"intl":8.0,"gender":9.0,"reg":7.5,"ot":8.5},
    "IT": {"avi":6.5,"ship":7.5,"rail":7.0,"road":7.5,"logi":7.0,"drv_pay":5.5,"safe":7.0,"comp":5.5,"wlb":6.5,"stab":5.5,"edu":7.0,"intl":6.5,"gender":5.5,"reg":6.5,"ot":5.5},
    "ES": {"avi":7.0,"ship":7.0,"rail":8.0,"road":8.0,"logi":7.0,"drv_pay":5.0,"safe":7.5,"comp":5.0,"wlb":7.0,"stab":5.0,"edu":7.0,"intl":7.0,"gender":6.5,"reg":6.5,"ot":5.5},
    "PT": {"avi":5.5,"ship":6.5,"rail":5.5,"road":7.0,"logi":6.0,"drv_pay":4.5,"safe":7.0,"comp":4.5,"wlb":7.0,"stab":5.5,"edu":6.5,"intl":7.5,"gender":7.0,"reg":6.0,"ot":6.0},
    "PL": {"avi":5.0,"ship":5.5,"rail":6.5,"road":7.5,"logi":7.0,"drv_pay":5.0,"safe":7.0,"comp":5.5,"wlb":7.0,"stab":6.5,"edu":7.0,"intl":7.5,"gender":6.5,"reg":6.5,"ot":6.0},
    "CZ": {"avi":5.0,"ship":3.5,"rail":7.0,"road":7.5,"logi":7.0,"drv_pay":5.0,"safe":7.5,"comp":5.5,"wlb":7.5,"stab":7.0,"edu":7.0,"intl":7.5,"gender":6.5,"reg":7.0,"ot":6.5},
    "RU": {"avi":7.0,"ship":6.5,"rail":8.0,"road":6.0,"logi":5.5,"drv_pay":3.5,"safe":5.0,"comp":4.5,"wlb":5.5,"stab":4.0,"edu":7.5,"intl":3.5,"gender":6.0,"reg":5.0,"ot":5.5},
    "CA": {"avi":8.0,"ship":6.5,"rail":7.0,"road":8.5,"logi":8.5,"drv_pay":7.5,"safe":8.5,"comp":7.5,"wlb":7.5,"stab":7.0,"edu":8.0,"intl":9.0,"gender":8.0,"reg":7.0,"ot":6.5},
    "MX": {"avi":5.5,"ship":5.5,"rail":4.0,"road":6.5,"logi":5.5,"drv_pay":3.0,"safe":4.5,"comp":4.0,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.5,"gender":5.0,"reg":5.0,"ot":4.5},
    "BR": {"avi":6.5,"ship":6.5,"rail":4.0,"road":6.5,"logi":5.5,"drv_pay":3.0,"safe":5.0,"comp":4.0,"wlb":6.0,"stab":4.5,"edu":6.0,"intl":5.0,"gender":5.5,"reg":5.5,"ot":5.0},
    "AR": {"avi":5.0,"ship":5.0,"rail":4.0,"road":6.0,"logi":5.0,"drv_pay":2.5,"safe":5.0,"comp":3.5,"wlb":5.5,"stab":3.5,"edu":6.5,"intl":5.5,"gender":5.5,"reg":5.0,"ot":5.0},
    "CL": {"avi":5.0,"ship":6.0,"rail":4.5,"road":6.5,"logi":5.5,"drv_pay":3.5,"safe":6.0,"comp":4.5,"wlb":6.0,"stab":5.5,"edu":6.0,"intl":6.0,"gender":5.5,"reg":5.5,"ot":5.5},
    "CO": {"avi":5.0,"ship":5.0,"rail":3.0,"road":5.5,"logi":5.0,"drv_pay":2.5,"safe":4.5,"comp":3.5,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.0,"gender":5.0,"reg":5.0,"ot":5.0},
    "AU": {"avi":8.0,"ship":7.5,"rail":6.5,"road":8.5,"logi":8.5,"drv_pay":8.0,"safe":8.5,"comp":7.5,"wlb":8.0,"stab":7.5,"edu":8.0,"intl":8.5,"gender":8.0,"reg":7.5,"ot":7.0},
    "NZ": {"avi":6.0,"ship":6.5,"rail":4.5,"road":7.5,"logi":7.0,"drv_pay":6.5,"safe":8.5,"comp":6.5,"wlb":8.5,"stab":7.5,"edu":7.5,"intl":8.0,"gender":8.5,"reg":7.0,"ot":7.5},
    "ZA": {"avi":5.5,"ship":6.0,"rail":5.0,"road":5.5,"logi":5.5,"drv_pay":3.0,"safe":4.5,"comp":4.0,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.5,"gender":5.5,"reg":5.0,"ot":5.5},
    "NG": {"avi":4.0,"ship":5.5,"rail":3.0,"road":3.5,"logi":4.0,"drv_pay":2.0,"safe":3.0,"comp":2.5,"wlb":4.5,"stab":3.5,"edu":4.0,"intl":5.0,"gender":4.0,"reg":3.5,"ot":4.5},
    "KE": {"avi":5.0,"ship":6.0,"rail":4.5,"road":4.5,"logi":4.5,"drv_pay":2.0,"safe":3.5,"comp":2.5,"wlb":5.0,"stab":4.0,"edu":4.5,"intl":5.5,"gender":4.5,"reg":4.0,"ot":5.0},
    "EG": {"avi":5.5,"ship":8.0,"rail":5.5,"road":5.5,"logi":5.0,"drv_pay":2.5,"safe":4.0,"comp":2.5,"wlb":5.0,"stab":4.0,"edu":5.0,"intl":5.0,"gender":3.5,"reg":4.5,"ot":4.5},
}

# === MID-CATEGORY DEFAULTS ===
# Base profiles shared by all occupations in each mid-category.
MID_DEFAULTS = {
    "aviation": {
        "learning_cost":7.5,"education_req":6.5,"growth_coeff":5.5,"career_lifespan":7.0,
        "opportunity":6.0,"market_size":5.0,"supply_demand":6.5,"developed_scarcity":6.5,
        "value_added":7.0,"cost_performance":6.5,"stability":6.5,"safety":5.0,
        "occupational_disease":5.5,"overtime":5.0,"burnout":5.5,
        "skill_versatility":5.0,"career_switch":4.5,"reputation_variance":1.5,
        "ai_resistance":6.5,"social_status":7.5,"remote_friendly":1.0,"autonomy":5.5,
        "family_friendly":4.0,"fulfillment":7.5,"entrepreneurship":3.0,"gender_equality":4.0,
        "age_flexibility":4.5,"social_interaction":6.0,"physical_demand":5.0,"license_barrier":8.5,
        "cycle_sensitivity":7.0,"side_job_compat":2.0,"intl_mobility":8.0,"industry_monopoly":5.0,
        "trend_long":2,"trend_short":1,"edu":"本科/专业培训","age":"22-30",
    },
    "maritime": {
        "learning_cost":6.5,"education_req":5.5,"growth_coeff":4.0,"career_lifespan":7.5,
        "opportunity":5.0,"market_size":4.5,"supply_demand":6.0,"developed_scarcity":6.5,
        "value_added":6.0,"cost_performance":6.0,"stability":6.0,"safety":4.5,
        "occupational_disease":4.5,"overtime":4.5,"burnout":5.0,
        "skill_versatility":4.0,"career_switch":3.5,"reputation_variance":1.5,
        "ai_resistance":6.5,"social_status":6.0,"remote_friendly":0.5,"autonomy":5.0,
        "family_friendly":2.5,"fulfillment":6.5,"entrepreneurship":3.5,"gender_equality":3.0,
        "age_flexibility":5.0,"social_interaction":5.5,"physical_demand":7.0,"license_barrier":8.0,
        "cycle_sensitivity":7.5,"side_job_compat":1.5,"intl_mobility":9.0,"industry_monopoly":4.5,
        "trend_long":1,"trend_short":0,"edu":"航海院校/大专","age":"20-28",
    },
    "railway": {
        "learning_cost":5.5,"education_req":5.0,"growth_coeff":5.0,"career_lifespan":8.0,
        "opportunity":5.5,"market_size":5.0,"supply_demand":5.5,"developed_scarcity":5.5,
        "value_added":5.5,"cost_performance":6.0,"stability":7.5,"safety":6.0,
        "occupational_disease":5.5,"overtime":5.0,"burnout":5.0,
        "skill_versatility":4.5,"career_switch":4.0,"reputation_variance":1.0,
        "ai_resistance":6.0,"social_status":5.5,"remote_friendly":1.0,"autonomy":4.0,
        "family_friendly":4.5,"fulfillment":5.5,"entrepreneurship":2.5,"gender_equality":4.5,
        "age_flexibility":5.5,"social_interaction":5.0,"physical_demand":5.5,"license_barrier":6.5,
        "cycle_sensitivity":4.5,"side_job_compat":2.5,"intl_mobility":4.5,"industry_monopoly":7.0,
        "trend_long":2,"trend_short":1,"edu":"大专/本科","age":"20-28",
    },
    "road_transport": {
        "learning_cost":2.5,"education_req":2.0,"growth_coeff":3.0,"career_lifespan":6.5,
        "opportunity":6.0,"market_size":8.0,"supply_demand":4.5,"developed_scarcity":5.5,
        "value_added":3.5,"cost_performance":5.0,"stability":5.0,"safety":5.5,
        "occupational_disease":4.0,"overtime":3.5,"burnout":4.5,
        "skill_versatility":3.0,"career_switch":3.0,"reputation_variance":1.5,
        "ai_resistance":3.0,"social_status":3.5,"remote_friendly":0.5,"autonomy":5.5,
        "family_friendly":3.5,"fulfillment":4.0,"entrepreneurship":5.0,"gender_equality":3.0,
        "age_flexibility":6.5,"social_interaction":4.0,"physical_demand":7.0,"license_barrier":4.0,
        "cycle_sensitivity":6.0,"side_job_compat":5.5,"intl_mobility":3.5,"industry_monopoly":3.0,
        "trend_long":0,"trend_short":-2,"edu":"驾照/高中","age":"20-35",
    },
    "logistics_mgmt": {
        "learning_cost":4.5,"education_req":4.0,"growth_coeff":6.0,"career_lifespan":7.0,
        "opportunity":6.5,"market_size":7.0,"supply_demand":5.5,"developed_scarcity":5.0,
        "value_added":5.5,"cost_performance":6.0,"stability":6.0,"safety":7.5,
        "occupational_disease":6.0,"overtime":5.0,"burnout":5.5,
        "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":1.5,
        "ai_resistance":5.0,"social_status":5.0,"remote_friendly":4.0,"autonomy":5.5,
        "family_friendly":5.0,"fulfillment":5.0,"entrepreneurship":5.5,"gender_equality":5.0,
        "age_flexibility":6.0,"social_interaction":6.0,"physical_demand":4.5,"license_barrier":3.0,
        "cycle_sensitivity":6.5,"side_job_compat":3.5,"intl_mobility":5.5,"industry_monopoly":3.5,
        "trend_long":3,"trend_short":2,"edu":"大专/本科","age":"22-30",
    },
    "last_mile": {
        "learning_cost":1.5,"education_req":1.5,"growth_coeff":6.0,"career_lifespan":4.5,
        "opportunity":7.5,"market_size":8.5,"supply_demand":4.0,"developed_scarcity":4.0,
        "value_added":2.5,"cost_performance":4.5,"stability":4.0,"safety":6.0,
        "occupational_disease":4.0,"overtime":3.0,"burnout":4.0,
        "skill_versatility":2.5,"career_switch":3.0,"reputation_variance":2.0,
        "ai_resistance":3.5,"social_status":3.0,"remote_friendly":0.5,"autonomy":5.5,
        "family_friendly":3.5,"fulfillment":3.5,"entrepreneurship":4.5,"gender_equality":3.5,
        "age_flexibility":7.0,"social_interaction":5.0,"physical_demand":8.0,"license_barrier":1.5,
        "cycle_sensitivity":5.5,"side_job_compat":7.0,"intl_mobility":2.5,"industry_monopoly":4.0,
        "trend_long":4,"trend_short":3,"edu":"无要求","age":"18-35",
    },
    "urban_transport": {
        "learning_cost":6.0,"education_req":5.5,"growth_coeff":6.5,"career_lifespan":7.5,
        "opportunity":6.0,"market_size":5.0,"supply_demand":5.5,"developed_scarcity":5.5,
        "value_added":6.0,"cost_performance":6.0,"stability":6.5,"safety":7.5,
        "occupational_disease":6.5,"overtime":5.5,"burnout":5.5,
        "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":1.5,
        "ai_resistance":5.5,"social_status":5.5,"remote_friendly":3.5,"autonomy":5.5,
        "family_friendly":5.5,"fulfillment":6.0,"entrepreneurship":4.5,"gender_equality":5.5,
        "age_flexibility":6.0,"social_interaction":5.5,"physical_demand":3.0,"license_barrier":4.0,
        "cycle_sensitivity":4.0,"side_job_compat":3.5,"intl_mobility":5.0,"industry_monopoly":5.5,
        "trend_long":3,"trend_short":2,"edu":"本科","age":"24-32",
    },
    "pipeline_transport": {
        "learning_cost":5.0,"education_req":4.5,"growth_coeff":3.5,"career_lifespan":8.0,
        "opportunity":4.0,"market_size":3.0,"supply_demand":5.5,"developed_scarcity":6.0,
        "value_added":5.5,"cost_performance":6.0,"stability":7.5,"safety":5.0,
        "occupational_disease":5.0,"overtime":6.0,"burnout":5.5,
        "skill_versatility":3.5,"career_switch":3.5,"reputation_variance":1.0,
        "ai_resistance":6.0,"social_status":4.5,"remote_friendly":2.0,"autonomy":5.0,
        "family_friendly":5.0,"fulfillment":4.5,"entrepreneurship":2.5,"gender_equality":3.5,
        "age_flexibility":6.0,"social_interaction":4.0,"physical_demand":6.5,"license_barrier":5.5,
        "cycle_sensitivity":5.0,"side_job_compat":2.5,"intl_mobility":4.0,"industry_monopoly":7.0,
        "trend_long":1,"trend_short":0,"edu":"大专/技校","age":"20-30",
    },
    "space_transport": {
        "learning_cost":9.0,"education_req":8.5,"growth_coeff":8.0,"career_lifespan":6.0,
        "opportunity":3.5,"market_size":1.5,"supply_demand":8.5,"developed_scarcity":9.0,
        "value_added":8.5,"cost_performance":6.0,"stability":5.0,"safety":3.5,
        "occupational_disease":5.0,"overtime":4.5,"burnout":5.0,
        "skill_versatility":5.0,"career_switch":4.5,"reputation_variance":2.0,
        "ai_resistance":7.5,"social_status":9.0,"remote_friendly":1.0,"autonomy":5.5,
        "family_friendly":3.5,"fulfillment":9.0,"entrepreneurship":5.0,"gender_equality":4.5,
        "age_flexibility":3.5,"social_interaction":6.0,"physical_demand":7.0,"license_barrier":9.5,
        "cycle_sensitivity":6.0,"side_job_compat":1.5,"intl_mobility":7.0,"industry_monopoly":8.0,
        "trend_long":4,"trend_short":4,"edu":"硕士/博士+飞行资质","age":"28-38",
    },
}

# === PER-OCCUPATION OVERRIDES (only non-default fields) ===
OVR = {
    # aviation
    "0101": {"learning_cost":9.0,"education_req":7.5,"value_added":8.5,"social_status":8.5,"license_barrier":9.5,"safety":4.5,"intl_mobility":9.0,"career_lifespan":6.5,"ai_resistance":7.0,"physical_demand":4.0,"gender_equality":3.0,"family_friendly":3.0,"age":"23-32","edu":"航校/本科+ATPL"},
    "0102": {"learning_cost":3.5,"education_req":3.5,"value_added":4.5,"social_status":6.0,"license_barrier":4.5,"safety":5.5,"physical_demand":5.5,"gender_equality":5.5,"family_friendly":3.0,"intl_mobility":8.5,"social_interaction":8.5,"ai_resistance":7.5,"age":"20-28","edu":"大专/高中"},
    "0103": {"learning_cost":7.0,"education_req":6.5,"value_added":7.5,"social_status":7.5,"license_barrier":9.0,"safety":8.5,"stability":8.0,"ai_resistance":7.0,"remote_friendly":2.0,"burnout":4.0,"physical_demand":2.0,"age":"22-30","edu":"本科+专业资格"},
    "0104": {"learning_cost":6.0,"education_req":6.0,"value_added":7.0,"social_status":7.0,"license_barrier":5.0,"remote_friendly":2.5,"autonomy":6.5,"social_interaction":7.5,"career_switch":5.5,"age":"28-38","edu":"本科"},
    "0105": {"value_added":6.5,"physical_demand":6.5,"safety":5.5,"license_barrier":7.5,"ai_resistance":7.0,"stability":7.0,"remote_friendly":0.5,"age":"20-28","edu":"大专/本科+执照"},
    "0106": {"learning_cost":5.5,"value_added":5.5,"license_barrier":7.0,"remote_friendly":3.0,"social_interaction":6.5,"physical_demand":2.0,"ai_resistance":5.5},
    "0107": {"learning_cost":9.0,"education_req":7.5,"value_added":8.0,"license_barrier":9.5,"intl_mobility":9.5,"family_friendly":2.0,"safety":4.0,"gender_equality":2.5,"social_interaction":3.5,"ai_resistance":6.0,"trend_short":2},
    "0108": {"value_added":7.5,"license_barrier":9.0,"market_size":3.5,"safety":4.0,"physical_demand":5.0,"intl_mobility":7.5,"ai_resistance":7.5,"gender_equality":3.0,"age":"24-35"},
    "0109": {"learning_cost":2.0,"education_req":2.0,"value_added":3.0,"social_status":3.5,"license_barrier":2.0,"physical_demand":7.5,"safety":5.5,"ai_resistance":4.5,"career_lifespan":5.5,"age":"18-30","edu":"高中"},
    "0110": {"learning_cost":5.5,"education_req":4.5,"value_added":5.5,"license_barrier":6.5,"physical_demand":7.0,"safety":5.5,"ai_resistance":7.0,"remote_friendly":0.5,"age":"20-28","edu":"技校/大专"},
    "0111": {"learning_cost":4.0,"education_req":4.0,"value_added":5.0,"license_barrier":3.5,"social_interaction":7.0,"intl_mobility":7.5,"physical_demand":3.0,"remote_friendly":3.5,"ai_resistance":4.5,"career_switch":5.0,"age":"22-30","edu":"大专/本科"},
    "0112": {"learning_cost":6.0,"education_req":6.0,"value_added":6.5,"license_barrier":7.5,"stability":7.5,"safety":8.0,"social_status":7.0,"remote_friendly":2.0,"ai_resistance":7.0,"physical_demand":3.0,"age":"28-38","edu":"本科+工程经验"},
    "0113": {"value_added":6.5,"license_barrier":9.0,"social_interaction":7.5,"social_status":7.0,"physical_demand":3.5,"market_size":3.0,"fulfillment":8.0,"entrepreneurship":5.5,"ai_resistance":8.0,"age":"28-40","edu":"ATPL+教官资格"},
    # maritime
    "0201": {"learning_cost":8.0,"education_req":7.0,"value_added":8.0,"social_status":7.5,"license_barrier":9.0,"safety":4.0,"career_lifespan":8.0,"intl_mobility":9.5,"family_friendly":1.5,"ai_resistance":7.5,"physical_demand":5.5,"autonomy":7.0,"age":"30-40","edu":"航海院校+甲类适任证书"},
    "0202": {"value_added":6.5,"license_barrier":8.0,"safety":4.0,"family_friendly":1.5,"intl_mobility":9.0,"physical_demand":6.0,"ai_resistance":6.5,"age":"24-32"},
    "0203": {"learning_cost":7.5,"education_req":6.5,"value_added":7.0,"license_barrier":8.5,"safety":4.5,"physical_demand":6.5,"ai_resistance":7.0,"family_friendly":1.5,"intl_mobility":9.0,"age":"26-35","edu":"轮机工程+证书"},
    "0204": {"learning_cost":3.0,"education_req":2.5,"value_added":3.5,"social_status":3.5,"license_barrier":4.5,"safety":3.5,"physical_demand":8.5,"family_friendly":1.5,"intl_mobility":8.5,"ai_resistance":5.0,"career_lifespan":6.0,"age":"18-28","edu":"海员证"},
    "0205": {"learning_cost":6.0,"education_req":6.0,"value_added":7.0,"social_status":7.0,"license_barrier":5.0,"safety":7.5,"remote_friendly":3.0,"physical_demand":3.0,"family_friendly":5.0,"autonomy":6.5,"social_interaction":7.5,"age":"30-40","edu":"本科+航运经验"},
    "0206": {"learning_cost":7.5,"education_req":6.5,"value_added":8.0,"social_status":7.0,"license_barrier":9.5,"safety":4.5,"physical_demand":4.0,"ai_resistance":7.5,"intl_mobility":7.5,"supply_demand":7.0,"developed_scarcity":7.5,"age":"30-45","edu":"甲类船长+引航资格"},
    "0207": {"learning_cost":6.5,"education_req":6.0,"value_added":6.5,"license_barrier":7.0,"safety":6.0,"physical_demand":4.5,"remote_friendly":2.0,"ai_resistance":6.5,"family_friendly":3.5,"age":"28-38","edu":"航海+检验资格"},
    "0208": {"learning_cost":2.5,"education_req":2.5,"value_added":3.5,"social_status":4.0,"license_barrier":3.0,"safety":5.5,"physical_demand":5.5,"social_interaction":8.5,"intl_mobility":8.5,"family_friendly":2.0,"gender_equality":5.0,"ai_resistance":7.5,"age":"20-30","edu":"高中/大专"},
    "0209": {"learning_cost":5.5,"education_req":5.0,"value_added":5.5,"license_barrier":6.5,"safety":7.5,"remote_friendly":2.5,"physical_demand":2.5,"ai_resistance":6.0,"age":"24-32"},
    "0210": {"learning_cost":5.0,"education_req":4.0,"value_added":5.0,"social_status":6.5,"license_barrier":5.5,"safety":2.5,"physical_demand":8.5,"fulfillment":8.0,"family_friendly":2.5,"ai_resistance":8.0,"gender_equality":3.5,"age":"22-32","edu":"救援培训+证书"},
    "0211": {"learning_cost":5.0,"education_req":5.0,"value_added":6.5,"social_interaction":8.0,"remote_friendly":4.0,"physical_demand":2.0,"license_barrier":4.5,"intl_mobility":8.5,"entrepreneurship":6.5,"ai_resistance":5.0,"family_friendly":5.0,"age":"25-35","edu":"本科"},
    # railway
    "0301": {"learning_cost":4.5,"value_added":5.0,"license_barrier":7.5,"safety":5.5,"physical_demand":4.5,"ai_resistance":4.5,"stability":8.0,"remote_friendly":0.5,"autonomy":4.5,"family_friendly":4.0,"social_interaction":3.0,"age":"22-30","edu":"技校/大专"},
    "0302": {"value_added":5.0,"license_barrier":6.0,"safety":7.5,"remote_friendly":1.5,"ai_resistance":5.5,"stability":8.0,"physical_demand":2.0,"social_interaction":5.5},
    "0303": {"value_added":5.5,"physical_demand":7.0,"safety":5.0,"license_barrier":5.5,"ai_resistance":6.5,"remote_friendly":0.5,"career_switch":4.0},
    "0304": {"learning_cost":7.0,"education_req":7.0,"value_added":7.0,"social_status":7.0,"growth_coeff":6.5,"license_barrier":5.0,"ai_resistance":6.5,"remote_friendly":2.0,"physical_demand":3.0,"supply_demand":6.5,"trend_short":3,"edu":"本科/硕士","age":"24-32"},
    "0305": {"learning_cost":3.5,"education_req":3.0,"value_added":4.0,"license_barrier":4.5,"social_interaction":7.0,"physical_demand":4.0,"safety":6.0,"ai_resistance":5.0,"remote_friendly":0.5,"age":"20-28","edu":"高中/大专"},
    "0306": {"learning_cost":4.0,"education_req":3.5,"value_added":4.5,"license_barrier":5.5,"physical_demand":4.0,"safety":6.5,"stability":7.5,"ai_resistance":5.0,"remote_friendly":0.5,"age":"20-28","edu":"高中/技校"},
    "0307": {"learning_cost":6.5,"education_req":6.0,"value_added":6.5,"license_barrier":6.0,"safety":7.5,"ai_resistance":6.0,"physical_demand":3.5,"remote_friendly":1.5,"supply_demand":6.0,"trend_short":2,"edu":"本科"},
    "0308": {"learning_cost":2.5,"education_req":2.5,"value_added":3.5,"social_interaction":8.0,"physical_demand":3.5,"safety":7.0,"license_barrier":2.5,"gender_equality":6.0,"ai_resistance":5.5,"remote_friendly":0.5,"age":"18-28","edu":"高中/大专"},
    "0309": {"learning_cost":7.0,"education_req":7.0,"value_added":7.0,"social_status":6.5,"license_barrier":5.0,"ai_resistance":6.5,"physical_demand":3.0,"supply_demand":6.0,"remote_friendly":2.0,"trend_short":2,"edu":"本科/硕士","age":"24-32"},
    # road_transport
    "0401": {"value_added":4.0,"physical_demand":7.5,"safety":4.5,"ai_resistance":2.0,"family_friendly":2.0,"burnout":3.5,"overtime":2.5,"intl_mobility":4.0,"cycle_sensitivity":7.0,"supply_demand":5.5,"developed_scarcity":6.5,"trend_short":-3},
    "0402": {"value_added":3.0,"stability":6.0,"safety":5.5,"ai_resistance":3.0,"social_interaction":6.5,"license_barrier":4.5,"cycle_sensitivity":3.5,"gender_equality":3.5,"industry_monopoly":5.0},
    "0403": {"value_added":3.0,"ai_resistance":2.0,"entrepreneurship":6.5,"license_barrier":3.5,"safety":5.0,"cycle_sensitivity":6.0,"side_job_compat":7.0,"social_interaction":6.0,"trend_short":-3},
    "0404": {"value_added":4.0,"ai_resistance":5.0,"social_interaction":8.0,"entrepreneurship":7.0,"license_barrier":5.0,"safety":6.0,"gender_equality":3.5,"fulfillment":5.5,"age":"25-40","edu":"驾照+教练资格"},
    "0405": {"value_added":4.5,"license_barrier":5.5,"safety":4.0,"physical_demand":7.5,"ai_resistance":4.0,"supply_demand":5.0,"developed_scarcity":5.5},
    "0406": {"value_added":3.5,"safety":5.0,"physical_demand":7.0,"license_barrier":3.0,"ai_resistance":6.0,"social_interaction":6.5,"fulfillment":5.5,"age":"20-35","edu":"驾照+技术培训"},
    "0407": {"value_added":2.5,"safety":3.5,"physical_demand":8.0,"ai_resistance":3.5,"license_barrier":2.5,"side_job_compat":7.5,"entrepreneurship":6.0,"cycle_sensitivity":5.0,"trend_short":0},
    "0408": {"value_added":3.0,"stability":6.5,"safety":5.5,"ai_resistance":4.0,"social_interaction":6.0,"license_barrier":4.5,"family_friendly":5.0,"gender_equality":4.0,"cycle_sensitivity":3.0},
    "0409": {"value_added":4.0,"physical_demand":7.5,"safety":4.5,"license_barrier":4.5,"ai_resistance":4.5,"supply_demand":5.0},
    "0410": {"learning_cost":1.5,"education_req":1.0,"value_added":2.5,"physical_demand":9.0,"safety":4.5,"ai_resistance":5.5,"social_status":2.5,"career_lifespan":5.5,"license_barrier":1.0,"age":"18-35","edu":"无要求"},
    # logistics_mgmt
    "0501": {"value_added":6.0,"social_status":5.5,"autonomy":6.5,"social_interaction":7.0,"physical_demand":4.0,"remote_friendly":3.5,"license_barrier":2.5,"ai_resistance":5.5,"age":"26-35","edu":"大专/本科"},
    "0502": {"value_added":7.0,"social_status":6.5,"growth_coeff":6.5,"autonomy":7.0,"social_interaction":7.5,"remote_friendly":4.5,"career_switch":6.0,"ai_resistance":5.5,"age":"28-38","edu":"本科"},
    "0503": {"value_added":5.5,"license_barrier":6.5,"intl_mobility":7.0,"social_interaction":6.5,"remote_friendly":3.5,"ai_resistance":5.0,"physical_demand":2.0,"age":"22-30","edu":"大专/本科+报关资格"},
    "0504": {"value_added":5.5,"intl_mobility":7.5,"social_interaction":7.0,"remote_friendly":4.0,"entrepreneurship":6.5,"ai_resistance":5.0,"physical_demand":2.5,"age":"22-32","edu":"大专/本科"},
    "0505": {"learning_cost":2.0,"education_req":1.5,"value_added":3.0,"physical_demand":7.5,"social_status":3.0,"ai_resistance":3.5,"safety":6.5,"license_barrier":1.5,"career_lifespan":5.5,"age":"18-30","edu":"高中/无要求"},
    "0506": {"learning_cost":5.5,"education_req":5.5,"value_added":6.0,"remote_friendly":6.5,"ai_resistance":4.5,"growth_coeff":7.0,"physical_demand":1.5,"social_interaction":5.5,"trend_short":3,"edu":"本科","age":"24-32"},
    "0507": {"value_added":5.5,"growth_coeff":7.0,"intl_mobility":7.0,"social_interaction":6.5,"remote_friendly":5.0,"ai_resistance":5.0,"trend_short":3,"edu":"本科","age":"22-30"},
    "0508": {"learning_cost":2.0,"education_req":1.5,"value_added":3.5,"physical_demand":7.0,"safety":5.5,"license_barrier":3.5,"ai_resistance":4.0,"career_lifespan":5.5,"social_status":3.0,"age":"18-30","edu":"培训证书"},
    "0509": {"value_added":5.5,"growth_coeff":6.5,"license_barrier":4.0,"physical_demand":4.0,"ai_resistance":5.5,"safety":6.5,"trend_short":2,"age":"24-32"},
    "0510": {"learning_cost":7.0,"education_req":6.5,"value_added":7.5,"growth_coeff":8.0,"ai_resistance":6.5,"remote_friendly":4.0,"physical_demand":2.5,"supply_demand":7.0,"developed_scarcity":7.0,"social_status":6.5,"trend_short":4,"edu":"本科/硕士","age":"24-32"},
    "0511": {"value_added":6.0,"license_barrier":7.0,"safety":5.0,"physical_demand":3.5,"ai_resistance":6.0,"stability":6.5,"social_status":5.5,"age":"25-35","edu":"本科+危险品资格"},
    # last_mile
    "0601": {"value_added":2.5,"physical_demand":8.0,"safety":5.5,"ai_resistance":3.0,"side_job_compat":6.0,"burnout":3.5,"overtime":2.5,"social_interaction":5.5,"trend_short":2},
    "0602": {"value_added":2.0,"physical_demand":8.5,"safety":4.5,"ai_resistance":3.0,"burnout":3.0,"overtime":2.0,"side_job_compat":7.5,"social_interaction":4.5,"career_lifespan":4.0,"trend_short":3},
    "0603": {"value_added":2.5,"physical_demand":8.0,"safety":5.0,"ai_resistance":3.5,"side_job_compat":6.5,"social_interaction":5.0},
    "0604": {"learning_cost":3.5,"education_req":3.0,"value_added":4.5,"social_status":4.5,"autonomy":6.5,"social_interaction":7.5,"physical_demand":5.0,"ai_resistance":5.0,"license_barrier":2.5,"age":"25-35","edu":"高中/大专"},
    "0605": {"market_size":2.0,"intl_mobility":1.0,"ai_resistance":8.5,"physical_demand":8.5,"fulfillment":7.0,"social_interaction":7.5,"safety":5.5,"social_status":5.0,"value_added":2.0,"career_lifespan":6.0},
    "0606": {"learning_cost":3.0,"education_req":3.0,"value_added":3.5,"physical_demand":5.0,"ai_resistance":5.0,"safety":7.5,"social_interaction":4.0,"side_job_compat":4.0,"growth_coeff":5.5,"age":"20-30","edu":"技校/培训"},
    # urban_transport
    "0701": {"learning_cost":7.0,"education_req":7.0,"value_added":7.0,"social_status":6.5,"growth_coeff":7.0,"remote_friendly":5.0,"ai_resistance":6.5,"autonomy":6.5,"physical_demand":1.5,"supply_demand":6.0,"trend_short":3,"edu":"本科/硕士","age":"26-35"},
    "0702": {"learning_cost":7.0,"education_req":7.0,"value_added":7.0,"social_status":6.5,"growth_coeff":6.5,"remote_friendly":4.0,"ai_resistance":6.0,"license_barrier":5.5,"physical_demand":2.0,"supply_demand":6.0,"trend_short":2,"edu":"本科/硕士","age":"24-32"},
    "0703": {"learning_cost":1.5,"education_req":1.5,"value_added":2.5,"social_status":3.0,"ai_resistance":3.0,"physical_demand":4.5,"safety":7.0,"license_barrier":1.5,"career_lifespan":6.5,"age":"18-40","edu":"无要求"},
    "0704": {"value_added":6.5,"growth_coeff":7.5,"social_interaction":7.5,"remote_friendly":4.5,"ai_resistance":5.5,"entrepreneurship":6.5,"trend_short":3,"age":"26-35","edu":"本科"},
    "0705": {"learning_cost":5.0,"education_req":4.5,"value_added":5.5,"growth_coeff":8.0,"ai_resistance":4.0,"safety":6.5,"physical_demand":3.0,"license_barrier":4.5,"remote_friendly":0.5,"supply_demand":7.0,"trend_short":4,"age":"22-35","edu":"技术培训+驾照"},
    "0706": {"learning_cost":4.5,"education_req":4.0,"value_added":5.0,"safety":6.5,"physical_demand":5.5,"license_barrier":4.0,"ai_resistance":5.5,"remote_friendly":1.0,"stability":7.0,"age":"20-30","edu":"技校/大专"},
    # pipeline_transport
    "0801": {"physical_demand":7.0,"safety":4.5,"remote_friendly":1.0,"ai_resistance":5.5,"stability":7.5,"family_friendly":4.5,"age":"22-32"},
    "0802": {"learning_cost":5.5,"value_added":6.0,"physical_demand":6.0,"safety":5.0,"license_barrier":6.0,"ai_resistance":6.5,"supply_demand":6.0,"developed_scarcity":6.5,"age":"24-35"},
    "0803": {"physical_demand":2.5,"remote_friendly":3.0,"safety":7.0,"ai_resistance":5.5,"social_interaction":5.0},
    # space_transport
    "0901": {"learning_cost":9.5,"education_req":9.0,"value_added":9.5,"social_status":9.5,"license_barrier":9.5,"safety":3.0,"physical_demand":8.0,"intl_mobility":8.0,"gender_equality":3.5,"family_friendly":2.5,"ai_resistance":8.0,"market_size":1.0,"age":"30-42","edu":"硕士/博士+飞行员资格"},
    "0902": {"learning_cost":7.5,"education_req":7.5,"value_added":7.5,"social_status":8.0,"license_barrier":7.5,"safety":8.0,"physical_demand":2.0,"remote_friendly":2.5,"ai_resistance":7.0,"age":"26-38","edu":"硕士+航天培训"},
    "0903": {"learning_cost":5.0,"education_req":5.0,"value_added":5.5,"social_status":6.0,"license_barrier":3.5,"safety":8.5,"physical_demand":1.5,"remote_friendly":5.0,"social_interaction":8.0,"ai_resistance":5.5,"entrepreneurship":7.0,"growth_coeff":7.0,"trend_short":3,"age":"25-35","edu":"本科+旅游/航天知识"},
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
    avi_f = (cp["avi"] - 6.0) / 4.0
    ship_f = (cp["ship"] - 6.0) / 4.0
    rail_f = (cp["rail"] - 6.0) / 4.0
    road_f = (cp["road"] - 6.0) / 4.0
    logi_f = (cp["logi"] - 6.0) / 4.0
    drv_f = (cp["drv_pay"] - 4.0) / 6.0
    safe_f = (cp["safe"] - 6.0) / 4.0
    comp_f = (cp["comp"] - 5.0) / 5.0
    stab_f = (cp["stab"] - 5.5) / 4.5
    wlb_f = (cp["wlb"] - 6.0) / 4.0
    gender_f = (cp["gender"] - 5.5) / 4.5
    edu_f = (cp["edu"] - 6.0) / 4.0
    intl_f = (cp["intl"] - 6.0) / 4.0
    reg_f = (cp["reg"] - 5.5) / 4.5

    mid = occ["mid"]
    # Sector-specific factor
    if mid == "aviation":
        sector_f = avi_f
    elif mid == "maritime":
        sector_f = ship_f
    elif mid == "railway":
        sector_f = rail_f
    elif mid in ("road_transport", "last_mile"):
        sector_f = road_f
    elif mid == "logistics_mgmt":
        sector_f = logi_f
    elif mid == "urban_transport":
        sector_f = (road_f + logi_f) / 2
    elif mid == "pipeline_transport":
        sector_f = logi_f * 0.5
    elif mid == "space_transport":
        sector_f = avi_f
    else:
        sector_f = logi_f

    s["value_added"] = clamp(s["value_added"] + comp_f * 1.8 + drv_f * 0.8)
    s["cost_performance"] = clamp(s["cost_performance"] + comp_f * 0.6 + drv_f * 0.5)
    s["growth_coeff"] = clamp(s["growth_coeff"] + sector_f * 0.8 + logi_f * 0.3)
    s["career_lifespan"] = clamp(s["career_lifespan"] + stab_f * 0.6)
    s["opportunity"] = clamp(s["opportunity"] + sector_f * 1.2 + logi_f * 0.3)
    s["market_size"] = clamp(s["market_size"] + sector_f * 1.5 + logi_f * 0.3)
    s["supply_demand"] = clamp(s["supply_demand"] + sector_f * 0.6 + logi_f * 0.5)
    dev_bonus = 0.8 if cp["logi"] >= 7.5 else (0.0 if cp["logi"] >= 5.0 else -0.8)
    s["developed_scarcity"] = clamp(s["developed_scarcity"] + dev_bonus)
    s["stability"] = clamp(s["stability"] + stab_f * 1.5 + reg_f * 0.3)
    s["safety"] = clamp(s["safety"] + safe_f * 1.2 + reg_f * 0.3)
    s["occupational_disease"] = clamp(s["occupational_disease"] + wlb_f * 0.5 + safe_f * 0.3)
    s["overtime"] = clamp(s["overtime"] + (cp["ot"] - 5.0) / 5.0 * 2.5)
    s["burnout"] = clamp(s["burnout"] + (cp["ot"] - 5.0) / 5.0 * 1.5)
    s["remote_friendly"] = clamp(s["remote_friendly"] + wlb_f * 0.3)
    s["autonomy"] = clamp(s["autonomy"] + wlb_f * 0.3 + sector_f * 0.2)
    s["family_friendly"] = clamp(s["family_friendly"] + wlb_f * 1.5)
    s["social_status"] = clamp(s["social_status"] + sector_f * 0.5 + comp_f * 0.4)
    s["fulfillment"] = clamp(s["fulfillment"] + sector_f * 0.3)
    s["gender_equality"] = clamp(s["gender_equality"] + gender_f * 2.0)
    s["age_flexibility"] = clamp(s["age_flexibility"] + wlb_f * 0.3 + sector_f * 0.2)
    s["entrepreneurship"] = clamp(s["entrepreneurship"] + sector_f * 0.3 + reg_f * 0.3)
    s["intl_mobility"] = clamp(s["intl_mobility"] + intl_f * 1.5)
    s["ai_resistance"] = clamp(s["ai_resistance"] + sector_f * 0.15)
    s["learning_cost"] = clamp(s["learning_cost"] + edu_f * 0.3)
    s["education_req"] = clamp(s["education_req"] + edu_f * 0.3)
    s["license_barrier"] = clamp(s["license_barrier"] + reg_f * 0.5)
    s["cycle_sensitivity"] = clamp(s["cycle_sensitivity"] - stab_f * 0.5)
    s["side_job_compat"] = clamp(s["side_job_compat"] + wlb_f * 0.3)
    s["industry_monopoly"] = clamp(s["industry_monopoly"] - sector_f * 0.2 + (1 - cp["reg"] / 10.0) * 0.3)
    s["skill_versatility"] = clamp(s["skill_versatility"] + sector_f * 0.4)
    s["career_switch"] = clamp(s["career_switch"] + sector_f * 0.3 + logi_f * 0.2)
    rep_adj = -0.3 if cp["safe"] >= 7.5 else (0.3 if cp["safe"] < 4.5 else 0.0)
    s["reputation_variance"] = clamp5(s["reputation_variance"] + rep_adj)
    # Maritime special: shipping hubs boost
    if mid == "maritime":
        s["market_size"] = clamp(s["market_size"] + ship_f * 1.0)
        s["value_added"] = clamp(s["value_added"] + ship_f * 0.4)
    # Aviation special: hub boost
    if mid == "aviation":
        s["market_size"] = clamp(s["market_size"] + avi_f * 0.8)
        s["intl_mobility"] = clamp(s["intl_mobility"] + avi_f * 0.3)
    # Road transport: autonomous vehicle disruption in high-tech countries
    if mid in ("road_transport", "last_mile"):
        if cp["logi"] >= 8.0:
            s["ai_resistance"] = clamp(s["ai_resistance"] - 0.5)
        s["value_added"] = clamp(s["value_added"] + drv_f * 0.5)
    # Railway: rail-network countries boost stability
    if mid == "railway":
        s["stability"] = clamp(s["stability"] + rail_f * 0.5)
        s["market_size"] = clamp(s["market_size"] + rail_f * 0.8)
    return s

def get_trends(base, cp):
    t_long = base["trend_long"]
    t_short = base["trend_short"]
    if cp["logi"] >= 8.0:
        t_short = min(5, t_short + 1)
    elif cp["logi"] < 4.0:
        t_short = max(-5, t_short - 1)
    if cp.get("avi", 6) >= 8.0 or cp.get("ship", 6) >= 8.0:
        t_long = min(5, t_long)
    elif cp["logi"] < 4.5:
        t_long = max(-5, t_long - 1)
    return t_long, t_short

def get_demand_direction(t):
    if t >= 4: return "↑↑"
    elif t >= 2: return "↑"
    elif t >= -1: return "→"
    elif t >= -3: return "↓"
    else: return "↓↓"

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
    if scores["safety"] <= 4.5: hz.append("安全风险较高"); he.append("high safety risk")
    if scores["physical_demand"] >= 7.5: hz.append("体力要求高"); he.append("high physical demand")
    if scores["license_barrier"] >= 8.0: hz.append("准入门槛高"); he.append("high entry barrier")
    if scores["stability"] >= 7.5: hz.append("就业稳定"); he.append("stable employment")
    elif scores["stability"] <= 4.0: hz.append("就业波动大"); he.append("volatile employment")
    if scores["intl_mobility"] >= 8.0: hz.append("国际流动性强"); he.append("high international mobility")
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
    csv_path = PROJECT_ROOT / "data" / "csv" / "transport_logistics.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for occ in OCCUPATIONS:
        base = occ_base(occ["id"], occ["mid"])
        for country in COUNTRIES:
            iso = country["iso"]
            cp = CP[iso]
            scores = apply_country_modifiers(base, cp, occ)
            rng = random.Random(hash(f"TRA-{occ['id']}-{iso}") % 10000)
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
            row_id = f"TRA-{occ['id']}-{iso}-general"
            row = {
                "id": row_id,
                "major_category": "交通运输与物流",
                "major_code": "TRA",
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
                "typical_education": base.get("edu", "大专/本科"),
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
    json_path = PROJECT_ROOT / "data" / "json" / "transport_logistics.json"
    convert_csv_to_json(str(csv_path), str(json_path))
    print(f"JSON written to {json_path}")

    # Notebook
    from tools.generate_notebook import create_data_notebook
    nb_path = PROJECT_ROOT / "notebooks" / "09_transport_logistics.ipynb"
    create_data_notebook(
        str(csv_path), str(nb_path),
        title="交通运输与物流 (TRA) — 完整数据",
        description="72 occupations × 45 countries/regions = 3,240 rows",
    )
    print(f"Notebook written to {nb_path}")


if __name__ == "__main__":
    main()
