#!/usr/bin/env python3
"""Generate skilled_trades.csv — SKL data for Global Career Development Index.
104 occupations x 45 countries = 4,680 rows.
"""
import csv, sys, random, json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from tools.score_calculator import load_weights, calculate_composite

# === OCCUPATIONS (104) from categories.yaml SKL ===
O = []
def _a(mid, mid_zh, mid_en, items):
    for id_, zh, en, isco, onet, loc in items:
        O.append({"id": id_, "mid": mid, "mid_zh": mid_zh, "mid_en": mid_en,
                   "zh": zh, "en": en, "isco": isco, "onet": onet, "locality": loc})

_a("electrical_trades", "电气技术", "Electrical Trades", [
    ("0101","电工","Electrician","7411","47-2111.00","global"),
    ("0102","电梯维修技师","Elevator Repair Technician","7412","47-4021.00","global"),
    ("0103","电力线路工人","Power Line Worker / Lineman","7413","49-9051.00","global"),
    ("0104","工业电气技师","Industrial Electrician","7411","47-2111.00","global"),
    ("0105","太阳能电池板安装工","Solar Panel Installer","7411","47-2231.00","global"),
    ("0106","防雷工程师","Lightning Protection Technician","7411","47-2111.00","global"),
    ("0107","弱电工程师","Low-Voltage Systems Technician","7411","49-2022.00","global"),
    ("0108","电动车充电桩安装技师","EV Charging Station Installer","7411","47-2111.00","global"),
    ("0109","通信线路技师","Telecommunications Line Technician","7422","49-9052.00","global"),
    ("0110","家电维修技师","Appliance Repair Technician","7412","49-9031.00","global"),
    ("0111","安防监控安装技师","Security & CCTV Installation Technician","7412","49-2098.00","global"),
])
_a("plumbing_hvac", "管道暖通", "Plumbing & HVAC", [
    ("0201","水管工","Plumber","7126","47-2152.00","global"),
    ("0202","暖通空调技师","HVAC Technician","7127","49-9021.00","global"),
    ("0203","制冷技师","Refrigeration Technician","7127","49-9021.00","global"),
    ("0204","管道安装工","Pipefitter","7126","47-2152.02","global"),
    ("0205","锅炉技师","Boiler Technician","7127","51-8021.00","global"),
    ("0206","燃气安装维修工","Gas Fitter","7126","47-2152.00","global"),
    ("0207","洒水/消防系统安装工","Sprinkler Fitter / Fire Suppression Installer","7126","47-2152.03","global"),
    ("0208","管道清洗工","Drain Technician / Sewer Cleaner","7126","47-2152.00","global"),
])
_a("welding", "焊接", "Welding", [
    ("0301","电弧焊工","Arc Welder","7212","51-4121.00","global"),
    ("0302","TIG焊工","TIG Welder","7212","51-4121.00","global"),
    ("0303","水下焊工","Underwater Welder","7212","51-4121.00","global"),
    ("0304","焊接检验员","Welding Inspector","7212","51-4121.00","global"),
    ("0305","管道焊工","Pipe Welder","7212","51-4121.00","global"),
    ("0306","机器人焊接技师","Robotic Welding Technician","7212","51-4121.00","global"),
    ("0307","MIG焊工","MIG Welder","7212","51-4121.00","global"),
    ("0308","铝焊工","Aluminum Welder","7212","51-4121.00","global"),
])
_a("machining", "机械加工", "Machining", [
    ("0401","CNC操作员","CNC Machine Operator","7223","51-4011.00","global"),
    ("0402","车工","Lathe Operator / Turner","7223","51-4034.00","global"),
    ("0403","铣工","Milling Machine Operator","7223","51-4035.00","global"),
    ("0404","模具制造技师","Tool & Die Maker","7222","51-4111.00","global"),
    ("0405","磨床操作员","Grinder Operator","7224","51-4033.00","global"),
    ("0406","钣金工","Sheet Metal Worker","7213","47-2211.00","global"),
    ("0407","CNC编程员","CNC Programmer","7223","51-4012.00","global"),
    ("0408","精密加工技师","Precision Machinist","7223","51-4041.00","global"),
    ("0409","3D打印技术员","3D Printing Technician / Additive Manufacturing","7223","51-4041.00","global"),
    ("0410","电火花加工技师","EDM (Electrical Discharge Machining) Technician","7223","51-4041.00","global"),
    ("0411","数控磨床操作员","CNC Grinding Operator","7224","51-4033.00","global"),
])
_a("auto_repair", "汽车维修", "Automotive Repair", [
    ("0501","汽车维修技师","Automotive Mechanic / Technician","7231","49-3023.00","global"),
    ("0502","汽车钣金工","Auto Body Repairer","7213","49-3021.00","global"),
    ("0503","汽车喷漆工","Automotive Painter","7132","51-9124.00","global"),
    ("0504","新能源汽车维修技师","EV Repair Technician","7231","49-3023.00","global"),
    ("0505","汽车诊断技师","Automotive Diagnostic Technician","7231","49-3023.00","global"),
    ("0506","摩托车维修技师","Motorcycle Mechanic","7231","49-3052.00","global"),
    ("0507","轮胎技师","Tire Technician","7231","49-3093.00","global"),
    ("0508","汽车空调维修技师","Automotive AC Technician","7231","49-3023.00","global"),
    ("0509","柴油机技师","Diesel Mechanic","7231","49-3031.00","global"),
    ("0510","汽车改装技师","Automotive Customization Technician","7231","49-3023.00","global"),
    ("0511","汽车贴膜/改色技师","Vehicle Wrap / Tinting Technician","7231","49-3023.00","global"),
])
_a("construction_trades", "建筑工", "Construction Trades", [
    ("0601","砌筑工","Bricklayer / Mason","7112","47-2021.00","global"),
    ("0602","抹灰工","Plasterer","7123","47-2161.00","global"),
    ("0603","防水工","Waterproofing Worker","7124","47-2141.00","global"),
    ("0604","钢筋工","Rebar Worker / Ironworker","7214","47-2171.00","global"),
    ("0605","混凝土工","Concrete Finisher","7114","47-2051.00","global"),
    ("0606","脚手架工","Scaffolder","7119","47-2225.00","global"),
    ("0607","吊车操作员","Crane Operator","8343","53-7021.00","global"),
    ("0608","挖掘机操作员","Excavator Operator","8342","47-2073.00","global"),
    ("0609","瓦工/贴砖工","Tile Setter","7122","47-2044.00","global"),
    ("0610","油漆工","Painter (Construction)","7131","47-2141.00","global"),
    ("0611","屋顶工","Roofer","7121","47-2181.00","global"),
    ("0612","玻璃安装工","Glazier","7125","47-2121.00","global"),
    ("0613","地板安装工","Floor Layer / Installer","7122","47-2042.00","global"),
    ("0614","石材工","Stone Mason","7113","47-2022.00","global"),
    ("0615","桩基工","Pile Driver Operator","8342","47-2072.00","global"),
    ("0616","绝缘工","Insulation Worker","7124","47-2131.00","global"),
    ("0617","木模工","Formwork Carpenter / Shuttering Joiner","7115","47-2031.00","global"),
])
_a("traditional_crafts", "传统手工艺", "Traditional Crafts", [
    ("0701","木工/细木工","Carpenter / Joiner","7115","47-2031.00","global"),
    ("0702","裁缝","Tailor / Dressmaker","7531","51-6052.00","global"),
    ("0703","陶艺师","Potter / Ceramicist","7314","51-9195.04","global"),
    ("0704","制表师/钟表匠","Watchmaker / Horologist","7311","49-9064.00","global"),
    ("0705","珠宝工匠","Jewelry Craftsman / Goldsmith","7313","51-9071.00","global"),
    ("0706","铁匠/锻工","Blacksmith","7221","51-4022.00","global"),
    ("0707","玻璃工匠","Glassblower / Glass Artisan","7315","51-9195.00","global"),
    ("0708","皮革工匠","Leather Worker / Saddler","7536","51-6041.00","global"),
    ("0709","编织工艺师","Weaver / Textile Artisan","7318","51-6063.00","global"),
    ("0710","猎鹰训练师","Falconer","6129","","country_specific"),
    ("0711","烟斗工匠","Pipe Maker","7319","51-9199.00","global"),
    ("0712","乐器制作师","Musical Instrument Maker / Luthier","7312","51-9071.06","global"),
    ("0713","书籍装帧师","Bookbinder","7323","51-5113.00","global"),
    ("0714","雕刻师","Engraver / Carver","7316","51-9194.00","global"),
    ("0715","鞋匠/制鞋师","Cobbler / Shoemaker","7536","51-6041.00","global"),
    ("0716","酿酒师(手工啤酒)","Craft Brewer","7514","51-3092.00","global"),
])
_a("beauty_grooming", "美发美容技术", "Hairdressing & Beauty", [
    ("0801","美发师","Hairdresser / Barber","5141","39-5012.00","global"),
    ("0802","美容师","Beautician / Esthetician","5142","39-5094.00","global"),
    ("0803","纹身师","Tattoo Artist","5142","39-5091.00","global"),
    ("0804","化妆师","Makeup Artist","5142","39-5091.00","global"),
    ("0805","美甲师","Nail Technician / Manicurist","5142","39-5092.00","global"),
    ("0806","美睫师","Eyelash Extension Technician","5142","39-5094.00","global"),
    ("0807","假发制作师","Wig Maker","5141","39-5012.00","global"),
])
_a("heavy_equipment", "重型设备操作", "Heavy Equipment Operation", [
    ("0901","推土机操作员","Bulldozer Operator","8342","47-2073.00","global"),
    ("0902","混凝土搅拌车司机","Concrete Mixer Truck Driver","8332","53-3032.00","global"),
    ("0903","装载机操作员","Loader Operator","8342","53-7032.00","global"),
    ("0904","压路机操作员","Road Roller Operator","8342","47-2073.00","global"),
    ("0905","打桩机操作员","Pile Driver / Piling Rig Operator","8342","47-2072.00","global"),
    ("0906","高空作业车操作员","Aerial Work Platform Operator","8343","53-7021.00","global"),
    ("0907","矿用卡车司机","Mining Haul Truck Driver","8342","53-7032.00","global"),
    ("0908","隧道掘进机操作员","Tunnel Boring Machine (TBM) Operator","8342","47-5041.00","global"),
])
_a("industrial_maintenance", "工业维护", "Industrial Maintenance", [
    ("1001","工业机械维修工","Industrial Machinery Mechanic","7233","49-9041.00","global"),
    ("1002","液压系统维修工","Hydraulic Systems Technician","7233","49-9041.00","global"),
    ("1003","仪表维修技师","Instrument Maintenance Technician","7412","49-9062.00","global"),
    ("1004","印刷机操作员","Printing Press Operator","7322","51-5112.00","global"),
    ("1005","锁匠","Locksmith","7222","49-9094.00","global"),
    ("1006","自动售货机维修工","Vending Machine Technician","7233","49-9091.00","global"),
    ("1007","电池回收技术员","Battery Recycling Technician","7233","51-9199.00","global"),
])
OCCUPATIONS = O

# === 45 COUNTRIES ===
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

# === COUNTRY PROFILES for SKL ===
# Keys: trade_pay, apprentice(apprenticeship system quality), constr_boom,
#   mfg_base(manufacturing base), craft_trad(craft tradition), safe(safety standards),
#   shortage(trade shortage level), comp(compensation), wlb, stab, edu, intl,
#   gender, reg(regulatory), ot(overtime culture, higher=less OT)
CP = {
    # STRONG APPRENTICESHIP / HIGH TRADE PAY — Germany, Switzerland, Austria-like
    "DE": {"trade_pay":8.5,"apprentice":9.5,"constr_boom":6.5,"mfg_base":9.5,"craft_trad":9.5,"safe":9.0,"shortage":8.5,"comp":8.0,"wlb":8.0,"stab":8.0,"edu":8.5,"intl":7.5,"gender":6.5,"reg":8.0,"ot":7.5},
    "CH": {"trade_pay":9.5,"apprentice":9.5,"constr_boom":6.0,"mfg_base":8.5,"craft_trad":9.5,"safe":9.5,"shortage":7.5,"comp":9.5,"wlb":8.5,"stab":9.0,"edu":9.0,"intl":8.0,"gender":6.5,"reg":8.0,"ot":7.5},
    "AT": {"trade_pay":8.0,"apprentice":9.0,"constr_boom":5.5,"mfg_base":8.5,"craft_trad":9.0,"safe":9.0,"shortage":8.0,"comp":7.5,"wlb":8.0,"stab":8.0,"edu":8.5,"intl":7.5,"gender":6.5,"reg":8.0,"ot":7.5},
    # HIGH TRADE PAY / MAJOR SHORTAGE — US, AU, CA
    "US": {"trade_pay":8.5,"apprentice":5.5,"constr_boom":7.5,"mfg_base":8.0,"craft_trad":6.0,"safe":7.5,"shortage":8.5,"comp":8.5,"wlb":5.5,"stab":5.5,"edu":8.0,"intl":7.5,"gender":6.5,"reg":6.5,"ot":5.0},
    "AU": {"trade_pay":8.5,"apprentice":7.5,"constr_boom":8.0,"mfg_base":6.0,"craft_trad":6.5,"safe":8.5,"shortage":9.0,"comp":8.0,"wlb":8.0,"stab":7.5,"edu":7.5,"intl":8.5,"gender":7.5,"reg":7.5,"ot":7.0},
    "CA": {"trade_pay":8.0,"apprentice":7.0,"constr_boom":7.0,"mfg_base":6.5,"craft_trad":6.0,"safe":8.5,"shortage":8.5,"comp":7.5,"wlb":7.5,"stab":7.0,"edu":7.5,"intl":8.5,"gender":7.5,"reg":7.0,"ot":6.5},
    "NZ": {"trade_pay":7.5,"apprentice":7.0,"constr_boom":7.5,"mfg_base":4.5,"craft_trad":5.5,"safe":8.5,"shortage":8.5,"comp":6.5,"wlb":8.5,"stab":7.5,"edu":7.5,"intl":7.5,"gender":8.0,"reg":7.0,"ot":7.5},
    # UK / IRELAND — decent trades, shortage, mixed apprentice
    "GB": {"trade_pay":7.5,"apprentice":7.0,"constr_boom":6.5,"mfg_base":6.5,"craft_trad":7.5,"safe":8.5,"shortage":8.0,"comp":7.5,"wlb":7.0,"stab":6.5,"edu":8.0,"intl":8.5,"gender":7.0,"reg":7.5,"ot":6.5},
    # NORDICS — good pay, strong safety, moderate crafts
    "SE": {"trade_pay":7.5,"apprentice":7.0,"constr_boom":6.0,"mfg_base":7.5,"craft_trad":7.0,"safe":9.0,"shortage":7.0,"comp":7.0,"wlb":9.0,"stab":8.0,"edu":8.5,"intl":8.0,"gender":9.0,"reg":7.5,"ot":8.5},
    "DK": {"trade_pay":7.5,"apprentice":7.5,"constr_boom":5.5,"mfg_base":6.5,"craft_trad":7.0,"safe":9.0,"shortage":7.0,"comp":7.0,"wlb":9.0,"stab":8.0,"edu":8.5,"intl":8.0,"gender":9.0,"reg":7.5,"ot":8.5},
    "FI": {"trade_pay":7.0,"apprentice":7.0,"constr_boom":5.0,"mfg_base":7.0,"craft_trad":7.5,"safe":9.0,"shortage":6.5,"comp":6.5,"wlb":9.0,"stab":7.5,"edu":9.0,"intl":7.5,"gender":9.0,"reg":7.5,"ot":8.5},
    "NL": {"trade_pay":7.5,"apprentice":7.0,"constr_boom":7.0,"mfg_base":6.5,"craft_trad":7.0,"safe":9.0,"shortage":7.5,"comp":7.5,"wlb":9.0,"stab":7.5,"edu":8.0,"intl":9.0,"gender":8.5,"reg":7.5,"ot":8.0},
    # WESTERN / SOUTHERN EUROPE
    "FR": {"trade_pay":6.5,"apprentice":7.5,"constr_boom":5.5,"mfg_base":7.0,"craft_trad":8.5,"safe":8.0,"shortage":7.0,"comp":7.0,"wlb":8.0,"stab":7.0,"edu":7.5,"intl":7.0,"gender":6.5,"reg":7.5,"ot":7.0},
    "IT": {"trade_pay":5.5,"apprentice":5.5,"constr_boom":4.5,"mfg_base":7.5,"craft_trad":9.0,"safe":7.0,"shortage":6.0,"comp":5.5,"wlb":6.5,"stab":5.5,"edu":7.0,"intl":6.5,"gender":5.0,"reg":6.5,"ot":5.5},
    "ES": {"trade_pay":5.0,"apprentice":5.0,"constr_boom":4.5,"mfg_base":6.0,"craft_trad":7.5,"safe":7.5,"shortage":5.5,"comp":5.0,"wlb":7.0,"stab":5.0,"edu":7.0,"intl":7.0,"gender":6.5,"reg":6.5,"ot":5.5},
    "PT": {"trade_pay":4.5,"apprentice":4.5,"constr_boom":5.0,"mfg_base":5.0,"craft_trad":7.0,"safe":7.0,"shortage":5.5,"comp":4.5,"wlb":7.0,"stab":5.5,"edu":6.5,"intl":7.0,"gender":6.5,"reg":6.0,"ot":6.0},
    # EASTERN EUROPE — strong manufacturing, moderate pay
    "PL": {"trade_pay":5.5,"apprentice":5.0,"constr_boom":6.5,"mfg_base":7.5,"craft_trad":6.5,"safe":7.0,"shortage":7.0,"comp":5.5,"wlb":7.0,"stab":6.5,"edu":7.0,"intl":7.5,"gender":6.0,"reg":6.5,"ot":6.0},
    "CZ": {"trade_pay":5.5,"apprentice":6.0,"constr_boom":5.5,"mfg_base":8.0,"craft_trad":7.0,"safe":7.5,"shortage":7.5,"comp":5.5,"wlb":7.5,"stab":7.0,"edu":7.0,"intl":7.5,"gender":6.0,"reg":7.0,"ot":6.5},
    "RU": {"trade_pay":4.5,"apprentice":5.0,"constr_boom":6.0,"mfg_base":7.0,"craft_trad":5.5,"safe":5.0,"shortage":5.5,"comp":4.5,"wlb":5.5,"stab":4.0,"edu":7.0,"intl":3.5,"gender":5.5,"reg":5.0,"ot":5.5},
    # EAST ASIA
    "JP": {"trade_pay":6.5,"apprentice":7.5,"constr_boom":5.5,"mfg_base":9.0,"craft_trad":9.5,"safe":9.0,"shortage":8.0,"comp":6.5,"wlb":4.5,"stab":7.5,"edu":7.5,"intl":4.5,"gender":4.0,"reg":7.5,"ot":3.5},
    "KR": {"trade_pay":5.5,"apprentice":5.5,"constr_boom":6.0,"mfg_base":8.5,"craft_trad":7.0,"safe":7.5,"shortage":6.5,"comp":6.0,"wlb":4.0,"stab":6.0,"edu":7.5,"intl":5.5,"gender":4.0,"reg":6.5,"ot":3.0},
    "CN": {"trade_pay":5.0,"apprentice":4.0,"constr_boom":8.5,"mfg_base":9.5,"craft_trad":8.0,"safe":5.5,"shortage":5.0,"comp":5.5,"wlb":3.5,"stab":5.0,"edu":7.0,"intl":4.5,"gender":5.0,"reg":5.5,"ot":2.5},
    "TW": {"trade_pay":5.0,"apprentice":5.0,"constr_boom":5.5,"mfg_base":8.5,"craft_trad":6.5,"safe":7.5,"shortage":6.0,"comp":5.5,"wlb":5.0,"stab":6.0,"edu":7.0,"intl":6.0,"gender":5.5,"reg":6.5,"ot":4.0},
    "HK": {"trade_pay":6.5,"apprentice":4.5,"constr_boom":6.5,"mfg_base":3.0,"craft_trad":5.5,"safe":8.0,"shortage":7.5,"comp":7.0,"wlb":4.5,"stab":6.5,"edu":7.0,"intl":8.5,"gender":6.0,"reg":7.0,"ot":3.5},
    # SOUTHEAST ASIA
    "SG": {"trade_pay":7.0,"apprentice":5.5,"constr_boom":7.0,"mfg_base":6.5,"craft_trad":4.5,"safe":8.5,"shortage":7.5,"comp":7.5,"wlb":5.5,"stab":8.0,"edu":8.0,"intl":9.0,"gender":6.5,"reg":8.0,"ot":4.5},
    "TH": {"trade_pay":3.5,"apprentice":3.5,"constr_boom":5.5,"mfg_base":6.5,"craft_trad":7.0,"safe":5.0,"shortage":4.5,"comp":3.5,"wlb":5.5,"stab":5.5,"edu":5.5,"intl":5.0,"gender":5.5,"reg":5.0,"ot":5.5},
    "VN": {"trade_pay":3.0,"apprentice":3.0,"constr_boom":7.0,"mfg_base":6.5,"craft_trad":7.5,"safe":4.5,"shortage":4.0,"comp":3.0,"wlb":5.0,"stab":5.0,"edu":5.5,"intl":5.0,"gender":5.5,"reg":5.0,"ot":4.5},
    "ID": {"trade_pay":3.0,"apprentice":3.0,"constr_boom":7.0,"mfg_base":5.5,"craft_trad":7.5,"safe":4.0,"shortage":4.0,"comp":3.0,"wlb":5.5,"stab":5.0,"edu":5.0,"intl":4.5,"gender":5.0,"reg":5.0,"ot":5.0},
    "MY": {"trade_pay":4.0,"apprentice":4.0,"constr_boom":6.5,"mfg_base":6.5,"craft_trad":5.5,"safe":6.0,"shortage":5.5,"comp":4.5,"wlb":5.5,"stab":6.0,"edu":6.0,"intl":6.5,"gender":5.0,"reg":5.5,"ot":5.0},
    "PH": {"trade_pay":3.0,"apprentice":3.0,"constr_boom":6.0,"mfg_base":4.5,"craft_trad":5.5,"safe":4.0,"shortage":4.5,"comp":3.0,"wlb":5.0,"stab":4.5,"edu":5.5,"intl":6.5,"gender":6.0,"reg":4.5,"ot":4.5},
    # SOUTH ASIA
    "IN": {"trade_pay":2.5,"apprentice":3.5,"constr_boom":8.0,"mfg_base":6.5,"craft_trad":8.5,"safe":3.5,"shortage":3.5,"comp":3.5,"wlb":4.5,"stab":5.0,"edu":6.5,"intl":6.5,"gender":3.5,"reg":5.0,"ot":4.0},
    "PK": {"trade_pay":2.0,"apprentice":2.5,"constr_boom":6.0,"mfg_base":4.5,"craft_trad":6.5,"safe":3.0,"shortage":3.5,"comp":2.5,"wlb":4.5,"stab":3.5,"edu":4.5,"intl":4.5,"gender":2.5,"reg":4.0,"ot":4.5},
    "BD": {"trade_pay":1.5,"apprentice":2.0,"constr_boom":6.5,"mfg_base":4.5,"craft_trad":6.5,"safe":2.5,"shortage":3.0,"comp":2.0,"wlb":4.5,"stab":3.5,"edu":4.0,"intl":4.5,"gender":3.0,"reg":3.5,"ot":4.5},
    # MIDDLE EAST
    "AE": {"trade_pay":6.0,"apprentice":3.5,"constr_boom":9.0,"mfg_base":4.5,"craft_trad":5.0,"safe":7.5,"shortage":6.5,"comp":7.0,"wlb":5.5,"stab":7.0,"edu":6.5,"intl":8.5,"gender":4.5,"reg":6.5,"ot":5.0},
    "IL": {"trade_pay":6.5,"apprentice":5.0,"constr_boom":7.0,"mfg_base":6.0,"craft_trad":5.5,"safe":7.5,"shortage":7.0,"comp":7.0,"wlb":6.0,"stab":5.5,"edu":8.0,"intl":7.5,"gender":6.5,"reg":6.5,"ot":5.0},
    "SA": {"trade_pay":5.5,"apprentice":3.0,"constr_boom":8.5,"mfg_base":4.5,"craft_trad":5.0,"safe":6.0,"shortage":7.0,"comp":6.0,"wlb":5.5,"stab":6.0,"edu":5.5,"intl":5.0,"gender":3.0,"reg":5.5,"ot":5.0},
    "TR": {"trade_pay":4.0,"apprentice":4.5,"constr_boom":7.0,"mfg_base":6.5,"craft_trad":7.5,"safe":5.5,"shortage":5.0,"comp":4.0,"wlb":5.0,"stab":4.0,"edu":6.5,"intl":5.5,"gender":4.0,"reg":5.5,"ot":4.5},
    # AMERICAS
    "MX": {"trade_pay":3.5,"apprentice":3.5,"constr_boom":6.5,"mfg_base":7.0,"craft_trad":7.5,"safe":4.5,"shortage":4.5,"comp":4.0,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.5,"gender":4.5,"reg":5.0,"ot":4.5},
    "BR": {"trade_pay":3.5,"apprentice":4.0,"constr_boom":5.5,"mfg_base":6.0,"craft_trad":6.0,"safe":5.0,"shortage":5.0,"comp":4.0,"wlb":6.0,"stab":4.5,"edu":5.5,"intl":5.0,"gender":5.0,"reg":5.5,"ot":5.0},
    "AR": {"trade_pay":3.0,"apprentice":3.5,"constr_boom":4.5,"mfg_base":5.0,"craft_trad":6.0,"safe":5.0,"shortage":4.5,"comp":3.5,"wlb":5.5,"stab":3.5,"edu":6.0,"intl":5.0,"gender":5.0,"reg":4.5,"ot":5.0},
    "CL": {"trade_pay":4.0,"apprentice":4.0,"constr_boom":5.5,"mfg_base":5.0,"craft_trad":5.0,"safe":6.0,"shortage":5.5,"comp":4.5,"wlb":6.0,"stab":5.5,"edu":6.0,"intl":5.5,"gender":5.0,"reg":5.5,"ot":5.5},
    "CO": {"trade_pay":3.0,"apprentice":3.5,"constr_boom":5.5,"mfg_base":4.5,"craft_trad":5.5,"safe":4.5,"shortage":4.5,"comp":3.5,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.0,"gender":4.5,"reg":5.0,"ot":5.0},
    # AFRICA
    "ZA": {"trade_pay":4.0,"apprentice":4.5,"constr_boom":5.0,"mfg_base":5.5,"craft_trad":5.0,"safe":5.0,"shortage":6.0,"comp":4.0,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.5,"gender":5.0,"reg":5.0,"ot":5.5},
    "NG": {"trade_pay":2.0,"apprentice":3.0,"constr_boom":6.0,"mfg_base":3.5,"craft_trad":6.0,"safe":3.0,"shortage":4.0,"comp":2.5,"wlb":4.5,"stab":3.5,"edu":4.0,"intl":5.0,"gender":3.5,"reg":3.5,"ot":4.5},
    "KE": {"trade_pay":2.5,"apprentice":3.0,"constr_boom":6.5,"mfg_base":3.5,"craft_trad":6.0,"safe":3.5,"shortage":5.0,"comp":2.5,"wlb":5.0,"stab":4.0,"edu":4.5,"intl":5.5,"gender":4.0,"reg":4.0,"ot":5.0},
    "EG": {"trade_pay":2.5,"apprentice":3.0,"constr_boom":7.0,"mfg_base":4.5,"craft_trad":7.0,"safe":3.5,"shortage":4.5,"comp":2.5,"wlb":5.0,"stab":4.0,"edu":5.0,"intl":4.5,"gender":3.0,"reg":4.5,"ot":4.5},
}
# AT is not in the 45-country list; remove it (used for reference only)
del CP["AT"]

# === MID-CATEGORY DEFAULTS ===
MID_DEFAULTS = {
    "electrical_trades": {
        "learning_cost":4.5,"education_req":3.5,"growth_coeff":6.5,"career_lifespan":8.0,
        "opportunity":7.0,"market_size":7.5,"supply_demand":7.0,"developed_scarcity":7.5,
        "value_added":6.5,"cost_performance":7.0,"stability":7.0,"safety":5.5,
        "occupational_disease":5.5,"overtime":5.0,"burnout":5.5,
        "skill_versatility":6.5,"career_switch":5.5,"reputation_variance":1.5,
        "ai_resistance":8.0,"social_status":5.5,"remote_friendly":0.5,"autonomy":6.5,
        "family_friendly":5.0,"fulfillment":6.5,"entrepreneurship":7.0,"gender_equality":3.0,
        "age_flexibility":6.5,"social_interaction":5.5,"physical_demand":6.5,"license_barrier":5.5,
        "cycle_sensitivity":5.0,"side_job_compat":7.0,"intl_mobility":6.0,"industry_monopoly":3.0,
        "trend_long":3,"trend_short":2,"edu":"职校/学徒","age":"18-25",
    },
    "plumbing_hvac": {
        "learning_cost":4.0,"education_req":3.0,"growth_coeff":6.0,"career_lifespan":8.0,
        "opportunity":7.0,"market_size":7.0,"supply_demand":7.5,"developed_scarcity":8.0,
        "value_added":6.5,"cost_performance":7.5,"stability":7.5,"safety":5.5,
        "occupational_disease":5.0,"overtime":5.0,"burnout":5.5,
        "skill_versatility":6.0,"career_switch":5.0,"reputation_variance":1.5,
        "ai_resistance":8.5,"social_status":5.0,"remote_friendly":0.5,"autonomy":7.0,
        "family_friendly":5.0,"fulfillment":6.5,"entrepreneurship":7.5,"gender_equality":2.5,
        "age_flexibility":6.5,"social_interaction":6.0,"physical_demand":7.0,"license_barrier":6.0,
        "cycle_sensitivity":4.5,"side_job_compat":7.5,"intl_mobility":6.5,"industry_monopoly":2.5,
        "trend_long":3,"trend_short":2,"edu":"职校/学徒","age":"18-25",
    },
    "welding": {
        "learning_cost":4.0,"education_req":3.0,"growth_coeff":5.5,"career_lifespan":7.0,
        "opportunity":6.0,"market_size":6.0,"supply_demand":6.5,"developed_scarcity":7.0,
        "value_added":6.0,"cost_performance":6.5,"stability":6.0,"safety":4.0,
        "occupational_disease":4.0,"overtime":5.0,"burnout":5.5,
        "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":1.5,
        "ai_resistance":6.5,"social_status":5.0,"remote_friendly":0.5,"autonomy":5.5,
        "family_friendly":4.5,"fulfillment":6.0,"entrepreneurship":5.5,"gender_equality":2.0,
        "age_flexibility":5.5,"social_interaction":5.0,"physical_demand":8.0,"license_barrier":5.0,
        "cycle_sensitivity":6.5,"side_job_compat":5.5,"intl_mobility":6.5,"industry_monopoly":3.0,
        "trend_long":2,"trend_short":1,"edu":"职校/短期培训","age":"18-25",
    },
    "machining": {
        "learning_cost":4.5,"education_req":3.5,"growth_coeff":5.0,"career_lifespan":7.5,
        "opportunity":5.5,"market_size":6.0,"supply_demand":6.0,"developed_scarcity":6.5,
        "value_added":5.5,"cost_performance":6.0,"stability":6.0,"safety":5.5,
        "occupational_disease":5.0,"overtime":5.0,"burnout":5.5,
        "skill_versatility":5.0,"career_switch":4.5,"reputation_variance":1.5,
        "ai_resistance":5.0,"social_status":5.0,"remote_friendly":0.5,"autonomy":5.5,
        "family_friendly":5.0,"fulfillment":6.0,"entrepreneurship":5.0,"gender_equality":2.5,
        "age_flexibility":6.0,"social_interaction":4.5,"physical_demand":6.5,"license_barrier":3.5,
        "cycle_sensitivity":6.0,"side_job_compat":4.5,"intl_mobility":5.5,"industry_monopoly":3.5,
        "trend_long":1,"trend_short":0,"edu":"职校/技校","age":"18-25",
    },
    "auto_repair": {
        "learning_cost":4.0,"education_req":3.0,"growth_coeff":5.5,"career_lifespan":7.5,
        "opportunity":6.5,"market_size":7.5,"supply_demand":6.0,"developed_scarcity":6.5,
        "value_added":5.5,"cost_performance":6.5,"stability":6.5,"safety":5.5,
        "occupational_disease":5.0,"overtime":5.0,"burnout":5.5,
        "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":1.5,
        "ai_resistance":7.0,"social_status":5.0,"remote_friendly":0.5,"autonomy":6.5,
        "family_friendly":5.0,"fulfillment":6.5,"entrepreneurship":7.5,"gender_equality":2.5,
        "age_flexibility":6.5,"social_interaction":6.5,"physical_demand":6.5,"license_barrier":4.0,
        "cycle_sensitivity":5.5,"side_job_compat":7.0,"intl_mobility":5.0,"industry_monopoly":2.5,
        "trend_long":2,"trend_short":1,"edu":"职校/学徒","age":"18-25",
    },
    "construction_trades": {
        "learning_cost":3.0,"education_req":2.0,"growth_coeff":5.0,"career_lifespan":6.5,
        "opportunity":6.5,"market_size":8.0,"supply_demand":6.0,"developed_scarcity":7.0,
        "value_added":5.0,"cost_performance":6.0,"stability":5.5,"safety":4.0,
        "occupational_disease":4.0,"overtime":4.5,"burnout":4.5,
        "skill_versatility":4.5,"career_switch":4.0,"reputation_variance":2.0,
        "ai_resistance":7.5,"social_status":4.0,"remote_friendly":0.5,"autonomy":5.0,
        "family_friendly":4.0,"fulfillment":5.5,"entrepreneurship":5.5,"gender_equality":2.0,
        "age_flexibility":5.0,"social_interaction":5.5,"physical_demand":8.5,"license_barrier":3.0,
        "cycle_sensitivity":7.5,"side_job_compat":5.5,"intl_mobility":5.5,"industry_monopoly":2.5,
        "trend_long":2,"trend_short":1,"edu":"短期培训/学徒","age":"18-25",
    },
    "traditional_crafts": {
        "learning_cost":5.5,"education_req":3.0,"growth_coeff":3.5,"career_lifespan":8.5,
        "opportunity":4.0,"market_size":3.5,"supply_demand":5.0,"developed_scarcity":5.5,
        "value_added":5.0,"cost_performance":5.0,"stability":5.5,"safety":6.5,
        "occupational_disease":5.5,"overtime":6.0,"burnout":6.5,
        "skill_versatility":4.5,"career_switch":3.5,"reputation_variance":2.0,
        "ai_resistance":9.0,"social_status":5.5,"remote_friendly":2.0,"autonomy":8.0,
        "family_friendly":6.0,"fulfillment":8.0,"entrepreneurship":7.5,"gender_equality":4.5,
        "age_flexibility":7.5,"social_interaction":5.0,"physical_demand":5.5,"license_barrier":2.0,
        "cycle_sensitivity":4.5,"side_job_compat":7.0,"intl_mobility":4.5,"industry_monopoly":2.0,
        "trend_long":0,"trend_short":-1,"edu":"师徒制/自学","age":"16-30",
    },
    "beauty_grooming": {
        "learning_cost":3.0,"education_req":2.0,"growth_coeff":5.0,"career_lifespan":7.0,
        "opportunity":6.5,"market_size":7.0,"supply_demand":5.0,"developed_scarcity":5.0,
        "value_added":4.5,"cost_performance":6.0,"stability":5.5,"safety":7.0,
        "occupational_disease":5.5,"overtime":5.5,"burnout":5.5,
        "skill_versatility":4.0,"career_switch":4.0,"reputation_variance":2.0,
        "ai_resistance":9.0,"social_status":4.5,"remote_friendly":0.5,"autonomy":7.0,
        "family_friendly":5.5,"fulfillment":6.5,"entrepreneurship":8.0,"gender_equality":7.0,
        "age_flexibility":6.5,"social_interaction":8.5,"physical_demand":5.0,"license_barrier":3.5,
        "cycle_sensitivity":4.0,"side_job_compat":7.5,"intl_mobility":5.0,"industry_monopoly":1.5,
        "trend_long":2,"trend_short":1,"edu":"职校/短期培训","age":"18-25",
    },
    "heavy_equipment": {
        "learning_cost":3.5,"education_req":2.5,"growth_coeff":5.0,"career_lifespan":7.0,
        "opportunity":6.0,"market_size":6.0,"supply_demand":5.5,"developed_scarcity":6.5,
        "value_added":5.5,"cost_performance":6.0,"stability":5.5,"safety":4.0,
        "occupational_disease":4.5,"overtime":4.5,"burnout":5.0,
        "skill_versatility":4.0,"career_switch":3.5,"reputation_variance":1.5,
        "ai_resistance":5.5,"social_status":4.0,"remote_friendly":0.5,"autonomy":5.5,
        "family_friendly":4.0,"fulfillment":5.5,"entrepreneurship":4.5,"gender_equality":2.0,
        "age_flexibility":5.5,"social_interaction":4.0,"physical_demand":7.5,"license_barrier":5.0,
        "cycle_sensitivity":7.0,"side_job_compat":3.5,"intl_mobility":5.0,"industry_monopoly":3.5,
        "trend_long":2,"trend_short":1,"edu":"驾照/培训","age":"20-30",
    },
    "industrial_maintenance": {
        "learning_cost":4.5,"education_req":3.5,"growth_coeff":5.5,"career_lifespan":7.5,
        "opportunity":6.0,"market_size":6.5,"supply_demand":6.5,"developed_scarcity":7.0,
        "value_added":5.5,"cost_performance":6.5,"stability":7.0,"safety":5.5,
        "occupational_disease":5.0,"overtime":5.0,"burnout":5.5,
        "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":1.5,
        "ai_resistance":7.0,"social_status":5.0,"remote_friendly":0.5,"autonomy":6.0,
        "family_friendly":5.0,"fulfillment":6.0,"entrepreneurship":5.5,"gender_equality":3.0,
        "age_flexibility":6.5,"social_interaction":5.0,"physical_demand":6.0,"license_barrier":4.0,
        "cycle_sensitivity":5.0,"side_job_compat":5.0,"intl_mobility":5.5,"industry_monopoly":3.5,
        "trend_long":2,"trend_short":1,"edu":"职校/技校","age":"20-28",
    },
}

# === PER-OCCUPATION OVERRIDES ===
OVR = {
    # electrical_trades
    "0101": {"supply_demand":7.5,"developed_scarcity":8.0,"entrepreneurship":7.5,"license_barrier":6.5,"side_job_compat":7.5},
    "0102": {"value_added":7.0,"safety":5.0,"license_barrier":6.5,"supply_demand":7.5,"developed_scarcity":8.0,"physical_demand":6.0},
    "0103": {"value_added":7.0,"safety":3.5,"physical_demand":8.5,"license_barrier":5.0,"developed_scarcity":8.5,"ai_resistance":8.5,"family_friendly":3.5,"overtime":4.0},
    "0104": {"value_added":7.0,"learning_cost":5.0,"education_req":4.0,"supply_demand":7.5,"developed_scarcity":8.0,"license_barrier":6.0,"mfg_link":True},
    "0105": {"growth_coeff":8.0,"trend_short":4,"trend_long":4,"supply_demand":7.0,"developed_scarcity":6.5,"ai_resistance":7.5,"physical_demand":7.0,"safety":5.0},
    "0106": {"market_size":3.5,"opportunity":4.5,"supply_demand":5.5,"developed_scarcity":5.5,"license_barrier":6.0},
    "0107": {"growth_coeff":7.0,"learning_cost":5.0,"education_req":4.5,"ai_resistance":7.0,"trend_short":2,"physical_demand":5.0},
    "0108": {"growth_coeff":8.5,"trend_short":5,"trend_long":4,"supply_demand":7.5,"market_size":5.5,"ai_resistance":7.5,"physical_demand":6.0},
    "0109": {"value_added":6.0,"physical_demand":7.0,"safety":5.0,"ai_resistance":7.0,"supply_demand":6.0,"developed_scarcity":6.5},
    "0110": {"value_added":5.0,"market_size":6.5,"supply_demand":5.5,"developed_scarcity":5.0,"entrepreneurship":8.0,"side_job_compat":8.0,"ai_resistance":8.0,"social_interaction":7.0},
    "0111": {"growth_coeff":7.0,"learning_cost":4.0,"value_added":6.0,"trend_short":2,"supply_demand":6.5,"ai_resistance":7.5,"physical_demand":5.5},
    # plumbing_hvac
    "0201": {"supply_demand":8.0,"developed_scarcity":8.5,"entrepreneurship":8.0,"side_job_compat":8.0,"license_barrier":6.5,"social_interaction":6.5,"ai_resistance":9.0},
    "0202": {"growth_coeff":7.0,"supply_demand":8.0,"developed_scarcity":8.5,"trend_short":3,"value_added":7.0,"ai_resistance":8.5},
    "0203": {"value_added":6.5,"supply_demand":7.0,"developed_scarcity":7.5},
    "0204": {"value_added":6.5,"physical_demand":7.5,"safety":5.0,"supply_demand":7.0,"developed_scarcity":7.5},
    "0205": {"value_added":6.0,"safety":4.5,"license_barrier":6.5,"supply_demand":6.5,"physical_demand":6.5,"trend_short":0},
    "0206": {"safety":4.0,"license_barrier":7.0,"supply_demand":7.0,"developed_scarcity":7.5,"ai_resistance":9.0},
    "0207": {"safety":4.5,"license_barrier":6.5,"growth_coeff":6.0,"supply_demand":7.0,"physical_demand":7.0},
    "0208": {"value_added":5.0,"learning_cost":2.5,"education_req":2.0,"physical_demand":7.5,"social_status":3.5,"supply_demand":6.0,"developed_scarcity":6.0,"ai_resistance":9.0,"fulfillment":4.5},
    # welding
    "0301": {"supply_demand":6.5,"value_added":5.5,"physical_demand":8.0,"safety":3.5},
    "0302": {"learning_cost":5.0,"value_added":6.5,"supply_demand":7.0,"developed_scarcity":7.5,"ai_resistance":7.0},
    "0303": {"learning_cost":7.0,"value_added":8.5,"safety":2.5,"physical_demand":9.0,"supply_demand":8.5,"developed_scarcity":9.0,"license_barrier":7.5,"ai_resistance":9.0,"intl_mobility":8.0,"social_status":6.0,"market_size":2.5,"opportunity":5.0},
    "0304": {"learning_cost":5.5,"education_req":4.5,"value_added":7.0,"safety":7.0,"physical_demand":4.0,"ai_resistance":7.5,"license_barrier":6.0,"social_status":6.0,"remote_friendly":2.5},
    "0305": {"value_added":7.0,"supply_demand":7.5,"developed_scarcity":8.0,"safety":3.5,"physical_demand":8.0,"license_barrier":6.0,"ai_resistance":7.5},
    "0306": {"learning_cost":5.5,"education_req":4.5,"value_added":6.5,"ai_resistance":4.0,"growth_coeff":6.5,"trend_short":2,"physical_demand":5.0,"safety":6.0},
    "0307": {"value_added":5.5,"supply_demand":6.0,"physical_demand":8.0,"safety":3.5},
    "0308": {"learning_cost":5.0,"value_added":6.5,"supply_demand":7.0,"developed_scarcity":7.0,"ai_resistance":7.0,"market_size":4.5},
    # machining
    "0401": {"ai_resistance":3.5,"growth_coeff":4.0,"trend_short":-1,"supply_demand":5.5,"physical_demand":6.0,"safety":5.5},
    "0402": {"ai_resistance":4.0,"growth_coeff":3.5,"trend_short":-2,"trend_long":0,"supply_demand":5.0,"developed_scarcity":5.5,"physical_demand":6.5},
    "0403": {"ai_resistance":4.0,"growth_coeff":3.5,"trend_short":-2,"supply_demand":5.0,"physical_demand":6.5},
    "0404": {"learning_cost":6.0,"education_req":4.5,"value_added":7.0,"ai_resistance":7.0,"supply_demand":7.0,"developed_scarcity":7.5,"career_lifespan":8.0,"social_status":6.0,"fulfillment":7.0},
    "0405": {"ai_resistance":3.5,"growth_coeff":3.0,"trend_short":-2,"physical_demand":6.5,"safety":5.0},
    "0406": {"value_added":5.5,"physical_demand":7.5,"safety":5.0,"supply_demand":6.0,"developed_scarcity":6.5,"ai_resistance":6.5},
    "0407": {"learning_cost":5.5,"education_req":4.5,"value_added":6.5,"ai_resistance":4.5,"growth_coeff":5.5,"trend_short":1,"remote_friendly":2.0},
    "0408": {"learning_cost":6.0,"education_req":4.5,"value_added":7.0,"ai_resistance":7.0,"supply_demand":7.0,"developed_scarcity":7.5,"social_status":6.0},
    "0409": {"learning_cost":4.5,"growth_coeff":7.5,"trend_short":4,"trend_long":4,"ai_resistance":5.0,"value_added":6.0,"market_size":4.0,"supply_demand":6.5,"physical_demand":4.0,"safety":6.5},
    "0410": {"learning_cost":5.5,"value_added":6.5,"ai_resistance":6.0,"supply_demand":6.0,"market_size":3.5,"physical_demand":5.0},
    "0411": {"ai_resistance":3.5,"growth_coeff":3.5,"trend_short":-1,"supply_demand":5.5,"physical_demand":6.0},
    # auto_repair
    "0501": {"supply_demand":6.5,"developed_scarcity":7.0,"entrepreneurship":8.0,"side_job_compat":7.5},
    "0502": {"value_added":5.5,"physical_demand":7.0,"safety":5.0,"ai_resistance":7.5},
    "0503": {"value_added":5.0,"physical_demand":6.0,"safety":4.5,"ai_resistance":7.5,"occupational_disease":4.0},
    "0504": {"growth_coeff":7.5,"trend_short":4,"trend_long":4,"value_added":6.5,"supply_demand":7.5,"developed_scarcity":7.5,"learning_cost":5.0,"education_req":4.0,"ai_resistance":6.5},
    "0505": {"learning_cost":5.0,"education_req":4.0,"value_added":6.5,"ai_resistance":6.5,"supply_demand":7.0,"developed_scarcity":7.0,"growth_coeff":6.5,"trend_short":2},
    "0506": {"value_added":5.0,"market_size":5.5,"supply_demand":5.5,"entrepreneurship":7.5},
    "0507": {"learning_cost":2.0,"education_req":1.5,"value_added":4.0,"social_status":3.5,"ai_resistance":7.5,"physical_demand":7.0,"career_lifespan":6.5},
    "0508": {"value_added":5.5,"supply_demand":6.0,"license_barrier":4.5},
    "0509": {"value_added":6.0,"physical_demand":7.0,"supply_demand":7.0,"developed_scarcity":7.5,"safety":5.0,"trend_short":0},
    "0510": {"value_added":6.0,"entrepreneurship":8.0,"fulfillment":7.5,"market_size":5.0,"ai_resistance":8.0,"social_interaction":7.0},
    "0511": {"learning_cost":3.0,"value_added":5.0,"entrepreneurship":8.0,"market_size":5.5,"physical_demand":4.5,"ai_resistance":8.5,"growth_coeff":6.0,"trend_short":2},
    # construction_trades
    "0601": {"value_added":5.0,"physical_demand":9.0,"safety":4.0,"ai_resistance":8.0,"skill_versatility":4.5},
    "0602": {"value_added":4.5,"physical_demand":8.5,"safety":4.5,"ai_resistance":8.5},
    "0603": {"value_added":5.5,"physical_demand":7.5,"safety":4.5,"license_barrier":4.0,"supply_demand":6.5},
    "0604": {"value_added":5.0,"physical_demand":9.0,"safety":3.0,"ai_resistance":7.5},
    "0605": {"value_added":4.5,"physical_demand":9.0,"safety":4.0,"ai_resistance":8.0},
    "0606": {"value_added":5.5,"physical_demand":8.5,"safety":2.5,"ai_resistance":8.0,"license_barrier":4.5},
    "0607": {"learning_cost":4.5,"education_req":3.5,"value_added":6.5,"license_barrier":6.5,"safety":3.5,"physical_demand":6.0,"supply_demand":7.0,"developed_scarcity":7.5,"ai_resistance":5.5},
    "0608": {"learning_cost":3.5,"value_added":5.5,"license_barrier":4.5,"safety":4.0,"physical_demand":5.0,"supply_demand":6.0,"ai_resistance":4.5,"trend_short":0},
    "0609": {"value_added":5.0,"physical_demand":8.0,"safety":5.5,"ai_resistance":8.5,"fulfillment":6.5,"social_interaction":5.0},
    "0610": {"value_added":4.5,"physical_demand":7.5,"safety":5.5,"ai_resistance":8.0,"occupational_disease":4.5},
    "0611": {"value_added":5.5,"physical_demand":9.0,"safety":2.5,"ai_resistance":8.0,"developed_scarcity":7.5},
    "0612": {"value_added":5.5,"physical_demand":7.5,"safety":4.0,"ai_resistance":8.0,"supply_demand":6.5},
    "0613": {"value_added":5.0,"physical_demand":7.5,"safety":6.0,"ai_resistance":8.0},
    "0614": {"learning_cost":5.0,"value_added":5.5,"physical_demand":8.5,"safety":5.0,"ai_resistance":9.0,"fulfillment":7.0,"craft_trad_link":True},
    "0615": {"value_added":5.5,"physical_demand":7.0,"safety":3.5,"license_barrier":5.5,"supply_demand":6.0,"ai_resistance":5.0},
    "0616": {"value_added":5.0,"physical_demand":7.0,"safety":5.0,"supply_demand":6.0,"ai_resistance":8.0},
    "0617": {"learning_cost":4.0,"value_added":5.5,"physical_demand":8.0,"safety":3.5,"ai_resistance":7.5,"supply_demand":6.5},
    # traditional_crafts
    "0701": {"learning_cost":4.5,"value_added":5.5,"supply_demand":6.0,"developed_scarcity":6.5,"physical_demand":7.0,"safety":5.5,"entrepreneurship":7.5,"ai_resistance":8.5,"market_size":5.5,"opportunity":5.5,"trend_short":0,"edu":"学徒/职校","age":"18-25"},
    "0702": {"value_added":4.5,"market_size":5.0,"supply_demand":4.5,"entrepreneurship":7.5,"social_interaction":6.5,"gender_equality":7.0,"physical_demand":3.5,"ai_resistance":8.0,"trend_short":0},
    "0703": {"value_added":4.5,"market_size":3.0,"fulfillment":8.5,"entrepreneurship":8.0,"ai_resistance":9.5,"physical_demand":4.5},
    "0704": {"learning_cost":7.5,"education_req":4.5,"value_added":7.5,"supply_demand":6.5,"developed_scarcity":7.0,"social_status":7.0,"ai_resistance":9.5,"market_size":2.5,"physical_demand":3.0,"fulfillment":8.5,"intl_mobility":7.0,"edu":"师徒制(3-5年)","age":"18-25"},
    "0705": {"learning_cost":6.5,"value_added":6.5,"supply_demand":5.5,"social_status":6.5,"ai_resistance":9.5,"fulfillment":8.5,"entrepreneurship":8.0,"market_size":3.0,"physical_demand":4.0,"intl_mobility":5.5},
    "0706": {"value_added":5.0,"physical_demand":8.5,"safety":4.5,"supply_demand":5.0,"ai_resistance":9.5,"market_size":2.5,"fulfillment":8.0},
    "0707": {"learning_cost":6.5,"value_added":5.5,"physical_demand":5.0,"safety":4.0,"ai_resistance":9.5,"market_size":2.0,"fulfillment":8.5},
    "0708": {"value_added":5.5,"supply_demand":4.5,"ai_resistance":9.5,"entrepreneurship":8.0,"market_size":3.0,"physical_demand":4.5,"fulfillment":8.0},
    "0709": {"value_added":4.0,"supply_demand":4.0,"ai_resistance":9.5,"market_size":2.5,"fulfillment":7.5,"gender_equality":6.5,"physical_demand":4.0},
    "0710": {"learning_cost":6.0,"value_added":5.0,"market_size":1.0,"opportunity":2.0,"supply_demand":4.0,"ai_resistance":10.0,"social_status":6.0,"fulfillment":9.0,"intl_mobility":2.0,"physical_demand":5.0,"gender_equality":3.0,"license_barrier":5.0},
    "0711": {"value_added":5.0,"market_size":1.5,"supply_demand":4.5,"ai_resistance":9.5,"fulfillment":8.0,"physical_demand":4.0},
    "0712": {"learning_cost":7.0,"value_added":6.5,"supply_demand":5.5,"social_status":7.0,"ai_resistance":9.5,"fulfillment":9.0,"market_size":2.0,"intl_mobility":6.0,"physical_demand":4.0,"edu":"师徒制/专业学校"},
    "0713": {"value_added":4.5,"market_size":2.0,"supply_demand":4.0,"ai_resistance":9.0,"fulfillment":7.5,"trend_short":-2},
    "0714": {"value_added":5.5,"supply_demand":5.0,"ai_resistance":9.5,"fulfillment":8.5,"physical_demand":5.0,"social_status":6.0},
    "0715": {"value_added":4.0,"market_size":3.0,"supply_demand":4.0,"ai_resistance":9.5,"entrepreneurship":7.5,"physical_demand":4.5,"trend_short":-1},
    "0716": {"learning_cost":5.0,"value_added":6.0,"growth_coeff":6.0,"trend_short":2,"trend_long":3,"entrepreneurship":9.0,"market_size":4.0,"supply_demand":5.5,"fulfillment":8.5,"social_interaction":6.5,"social_status":6.0,"ai_resistance":9.0,"license_barrier":4.5},
    # beauty_grooming
    "0801": {"supply_demand":5.5,"entrepreneurship":8.5,"side_job_compat":8.0,"social_interaction":9.0,"fulfillment":7.0,"social_status":5.0},
    "0802": {"growth_coeff":5.5,"entrepreneurship":8.5,"social_interaction":8.5,"fulfillment":7.0},
    "0803": {"learning_cost":4.5,"value_added":5.5,"entrepreneurship":8.5,"fulfillment":8.0,"social_status":4.5,"license_barrier":4.5,"social_interaction":8.0,"market_size":4.5},
    "0804": {"value_added":5.5,"side_job_compat":8.0,"social_interaction":8.5,"fulfillment":7.5,"gender_equality":7.5,"intl_mobility":6.0},
    "0805": {"learning_cost":2.0,"value_added":4.0,"entrepreneurship":8.5,"social_interaction":8.0,"physical_demand":4.0,"occupational_disease":5.0},
    "0806": {"learning_cost":2.5,"value_added":4.5,"market_size":5.0,"growth_coeff":6.0,"trend_short":2,"social_interaction":7.5,"physical_demand":3.5},
    "0807": {"learning_cost":4.5,"value_added":5.0,"market_size":3.5,"supply_demand":5.5,"physical_demand":4.0,"social_interaction":5.5,"ai_resistance":9.5},
    # heavy_equipment
    "0901": {"physical_demand":7.0,"safety":3.5,"ai_resistance":4.5,"license_barrier":5.5},
    "0902": {"physical_demand":6.0,"safety":4.0,"license_barrier":4.5,"ai_resistance":4.5,"social_interaction":3.5},
    "0903": {"physical_demand":6.5,"safety":3.5,"ai_resistance":4.5,"license_barrier":5.0},
    "0904": {"physical_demand":5.5,"safety":4.5,"ai_resistance":4.0,"market_size":5.0},
    "0905": {"physical_demand":7.0,"safety":3.0,"license_barrier":5.5,"supply_demand":6.0,"ai_resistance":5.0},
    "0906": {"physical_demand":5.5,"safety":3.0,"license_barrier":5.5,"supply_demand":6.0,"developed_scarcity":7.0,"ai_resistance":6.0},
    "0907": {"value_added":6.5,"physical_demand":6.0,"safety":3.5,"ai_resistance":3.5,"market_size":4.5,"family_friendly":3.0,"intl_mobility":5.5},
    "0908": {"learning_cost":5.5,"education_req":4.0,"value_added":7.0,"physical_demand":5.5,"safety":4.5,"ai_resistance":6.0,"supply_demand":6.5,"developed_scarcity":7.0,"market_size":3.5,"license_barrier":6.0},
    # industrial_maintenance
    "1001": {"supply_demand":7.0,"developed_scarcity":7.5,"value_added":6.0,"physical_demand":6.5,"safety":5.0},
    "1002": {"value_added":6.0,"physical_demand":6.5,"safety":5.0,"supply_demand":6.5,"market_size":5.5},
    "1003": {"learning_cost":5.0,"education_req":4.5,"value_added":6.0,"ai_resistance":6.5,"supply_demand":6.5,"physical_demand":4.5},
    "1004": {"ai_resistance":3.5,"growth_coeff":2.5,"trend_short":-3,"trend_long":-2,"value_added":4.5,"physical_demand":5.0,"supply_demand":4.5,"developed_scarcity":4.5},
    "1005": {"value_added":5.0,"entrepreneurship":8.0,"side_job_compat":7.5,"ai_resistance":8.5,"social_interaction":6.5,"physical_demand":4.5,"market_size":5.0,"safety":7.0},
    "1006": {"value_added":5.0,"ai_resistance":6.0,"physical_demand":5.5,"market_size":5.0,"supply_demand":5.5},
    "1007": {"growth_coeff":7.0,"trend_short":3,"trend_long":3,"value_added":5.5,"safety":4.0,"physical_demand":6.5,"supply_demand":6.0,"ai_resistance":6.5,"market_size":4.0},
}

# === Build occupation base scores ===
def occ_base(occ_id, mid):
    d = dict(MID_DEFAULTS[mid])
    ovr = OVR.get(occ_id, {})
    # Remove non-score keys from overrides
    for k in ("mfg_link", "craft_trad_link"):
        ovr.pop(k, None)
    d.update(ovr)
    return d

# === SCORING ===
def clamp(val, lo=0.0, hi=10.0):
    return max(lo, min(hi, round(val, 1)))

def clamp5(val):
    return max(0.0, min(5.0, round(val, 1)))

def apply_country_modifiers(base, cp, occ):
    s = dict(base)
    trade_f = (cp["trade_pay"] - 5.0) / 5.0
    appr_f = (cp["apprentice"] - 5.0) / 5.0
    constr_f = (cp["constr_boom"] - 6.0) / 4.0
    mfg_f = (cp["mfg_base"] - 6.0) / 4.0
    craft_f = (cp["craft_trad"] - 6.0) / 4.0
    safe_f = (cp["safe"] - 6.0) / 4.0
    short_f = (cp["shortage"] - 5.0) / 5.0
    comp_f = (cp["comp"] - 5.0) / 5.0
    stab_f = (cp["stab"] - 5.5) / 4.5
    wlb_f = (cp["wlb"] - 6.0) / 4.0
    gender_f = (cp["gender"] - 5.5) / 4.5
    edu_f = (cp["edu"] - 6.0) / 4.0
    intl_f = (cp["intl"] - 6.0) / 4.0
    reg_f = (cp["reg"] - 5.5) / 4.5

    mid = occ["mid"]

    # Sector-specific factor
    if mid in ("construction_trades", "heavy_equipment"):
        sector_f = constr_f
    elif mid in ("machining", "industrial_maintenance"):
        sector_f = mfg_f
    elif mid == "traditional_crafts":
        sector_f = craft_f
    elif mid in ("electrical_trades", "plumbing_hvac"):
        sector_f = (constr_f + short_f) / 2
    elif mid == "welding":
        sector_f = (mfg_f + constr_f) / 2
    elif mid == "auto_repair":
        sector_f = trade_f
    elif mid == "beauty_grooming":
        sector_f = comp_f
    else:
        sector_f = trade_f

    # Value-added: strongly driven by trade pay + compensation
    s["value_added"] = clamp(s["value_added"] + trade_f * 1.5 + comp_f * 0.8)
    s["cost_performance"] = clamp(s["cost_performance"] + trade_f * 0.8 + comp_f * 0.4)

    # Growth: construction boom / mfg base + shortage
    s["growth_coeff"] = clamp(s["growth_coeff"] + sector_f * 0.8 + short_f * 0.3)
    s["career_lifespan"] = clamp(s["career_lifespan"] + stab_f * 0.6)

    # Opportunity & market: boom-driven
    s["opportunity"] = clamp(s["opportunity"] + sector_f * 1.0 + short_f * 0.5)
    s["market_size"] = clamp(s["market_size"] + sector_f * 1.2 + constr_f * 0.3)

    # Supply-demand: shortage is the primary driver
    s["supply_demand"] = clamp(s["supply_demand"] + short_f * 1.5 + sector_f * 0.3)

    # Developed scarcity: massive in developed countries with trade shortages
    dev_bonus = 1.0 if cp["shortage"] >= 7.5 else (0.0 if cp["shortage"] >= 5.0 else -0.8)
    s["developed_scarcity"] = clamp(s["developed_scarcity"] + dev_bonus + appr_f * 0.3)

    # Stability: regulation + stability
    s["stability"] = clamp(s["stability"] + stab_f * 1.2 + reg_f * 0.4)

    # Safety: strongly affected by country safety standards
    s["safety"] = clamp(s["safety"] + safe_f * 1.5 + reg_f * 0.3)

    # Occupational disease: safety standards + WLB
    s["occupational_disease"] = clamp(s["occupational_disease"] + safe_f * 0.5 + wlb_f * 0.3)

    # Overtime / burnout
    s["overtime"] = clamp(s["overtime"] + (cp["ot"] - 5.0) / 5.0 * 2.5)
    s["burnout"] = clamp(s["burnout"] + (cp["ot"] - 5.0) / 5.0 * 1.5)

    # Remote: trades are inherently non-remote, minor adjustment only
    s["remote_friendly"] = clamp(s["remote_friendly"] + wlb_f * 0.1)

    # Autonomy
    s["autonomy"] = clamp(s["autonomy"] + wlb_f * 0.3 + appr_f * 0.2)

    # Family friendly: WLB culture
    s["family_friendly"] = clamp(s["family_friendly"] + wlb_f * 1.5)

    # Social status: trades pay well in some countries, poorly in others
    s["social_status"] = clamp(s["social_status"] + trade_f * 0.8 + appr_f * 0.5)

    # Fulfillment: craft tradition, apprenticeship quality
    s["fulfillment"] = clamp(s["fulfillment"] + craft_f * 0.3 + appr_f * 0.2)

    # Gender equality
    s["gender_equality"] = clamp(s["gender_equality"] + gender_f * 2.0)

    # Age flexibility
    s["age_flexibility"] = clamp(s["age_flexibility"] + wlb_f * 0.3 + safe_f * 0.2)

    # Entrepreneurship: strong in developed trade-shortage markets
    s["entrepreneurship"] = clamp(s["entrepreneurship"] + trade_f * 0.4 + reg_f * 0.3)

    # International mobility
    s["intl_mobility"] = clamp(s["intl_mobility"] + intl_f * 1.2 + short_f * 0.3)

    # AI resistance: slightly lower in high-tech manufacturing countries
    ai_adj = -0.2 if cp["mfg_base"] >= 8.5 else (0.1 if cp["mfg_base"] < 5.0 else 0.0)
    s["ai_resistance"] = clamp(s["ai_resistance"] + ai_adj)

    # Learning cost / education req: apprenticeship countries may have higher formal requirements
    s["learning_cost"] = clamp(s["learning_cost"] + appr_f * 0.4)
    s["education_req"] = clamp(s["education_req"] + appr_f * 0.3)

    # License barrier: higher in more regulated environments
    s["license_barrier"] = clamp(s["license_barrier"] + reg_f * 0.6 + safe_f * 0.2)

    # Cycle sensitivity: construction is cyclical, less so in boom countries
    s["cycle_sensitivity"] = clamp(s["cycle_sensitivity"] - stab_f * 0.5 - constr_f * 0.2)

    # Side job compatibility
    s["side_job_compat"] = clamp(s["side_job_compat"] + trade_f * 0.3 + wlb_f * 0.2)

    # Industry monopoly
    s["industry_monopoly"] = clamp(s["industry_monopoly"] - sector_f * 0.2 + (1 - cp["reg"] / 10.0) * 0.3)

    # Skill versatility: apprenticeship quality helps
    s["skill_versatility"] = clamp(s["skill_versatility"] + appr_f * 0.4 + sector_f * 0.2)

    # Career switch
    s["career_switch"] = clamp(s["career_switch"] + appr_f * 0.3 + sector_f * 0.2)

    # Reputation variance: lower in strong apprenticeship countries (trades respected)
    rep_adj = -0.3 if cp["apprentice"] >= 7.5 else (0.3 if cp["apprentice"] < 3.5 else 0.0)
    s["reputation_variance"] = clamp5(s["reputation_variance"] + rep_adj)

    # === Sector-specific adjustments ===
    # Construction: boom countries boost market size and opportunity
    if mid in ("construction_trades", "heavy_equipment"):
        s["market_size"] = clamp(s["market_size"] + constr_f * 0.8)
        s["opportunity"] = clamp(s["opportunity"] + constr_f * 0.5)
    # Machining: manufacturing powerhouses boost
    if mid in ("machining", "industrial_maintenance"):
        s["supply_demand"] = clamp(s["supply_demand"] + mfg_f * 0.5)
        s["stability"] = clamp(s["stability"] + mfg_f * 0.3)
    # Traditional crafts: craft tradition countries boost market & fulfillment
    if mid == "traditional_crafts":
        s["market_size"] = clamp(s["market_size"] + craft_f * 1.0)
        s["fulfillment"] = clamp(s["fulfillment"] + craft_f * 0.3)
        s["social_status"] = clamp(s["social_status"] + craft_f * 0.5)
    # Plumbing/HVAC: massive shortage in developed countries
    if mid == "plumbing_hvac":
        if cp["shortage"] >= 7.5:
            s["supply_demand"] = clamp(s["supply_demand"] + 0.5)
            s["developed_scarcity"] = clamp(s["developed_scarcity"] + 0.5)
    # Auto repair: EV transition affects different countries differently
    if mid == "auto_repair":
        if cp["mfg_base"] >= 8.0:
            s["growth_coeff"] = clamp(s["growth_coeff"] + 0.3)
    # Welding: high-mfg countries boost demand
    if mid == "welding":
        s["supply_demand"] = clamp(s["supply_demand"] + mfg_f * 0.4)
        s["value_added"] = clamp(s["value_added"] + mfg_f * 0.3)

    return s

def get_trends(base, cp):
    t_long = base["trend_long"]
    t_short = base["trend_short"]
    # Construction boom boosts short-term for construction/heavy equip
    if cp["constr_boom"] >= 8.0:
        t_short = min(5, t_short + 1)
    elif cp["constr_boom"] < 4.5:
        t_short = max(-5, t_short - 1)
    # Severe shortage boosts demand across the board
    if cp["shortage"] >= 8.0:
        t_long = min(5, t_long + 1)
    elif cp["shortage"] < 4.0:
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
    if scores["developed_scarcity"] >= 8.0: hz.append("发达国家严重短缺"); he.append("severe shortage in developed countries")
    if scores["safety"] <= 4.0: hz.append("安全风险较高"); he.append("high safety risk")
    if scores["physical_demand"] >= 8.0: hz.append("体力要求高"); he.append("high physical demand")
    if scores["license_barrier"] >= 7.0: hz.append("准入门槛较高"); he.append("significant entry barriers")
    if scores["stability"] >= 7.5: hz.append("就业稳定"); he.append("stable employment")
    elif scores["stability"] <= 4.0: hz.append("就业波动大"); he.append("volatile employment")
    if scores["entrepreneurship"] >= 8.0: hz.append("创业前景好"); he.append("good entrepreneurship prospects")
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
    csv_path = PROJECT_ROOT / "data" / "csv" / "skilled_trades.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for occ in OCCUPATIONS:
        base = occ_base(occ["id"], occ["mid"])
        for country in COUNTRIES:
            iso = country["iso"]
            cp = CP[iso]
            scores = apply_country_modifiers(base, cp, occ)
            rng = random.Random(hash(f"SKL-{occ['id']}-{iso}") % 10000)
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
            row_id = f"SKL-{occ['id']}-{iso}-general"
            row = {
                "id": row_id,
                "major_category": "技术工种与手工业",
                "major_code": "SKL",
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
                "typical_education": base.get("edu", "职校/学徒"),
                "typical_entry_age": base.get("age", "18-25"),
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
    json_path = PROJECT_ROOT / "data" / "json" / "skilled_trades.json"
    convert_csv_to_json(str(csv_path), str(json_path))
    print(f"JSON written to {json_path}")

    # Notebook
    from tools.generate_notebook import create_data_notebook
    nb_path = PROJECT_ROOT / "notebooks" / "10_skilled_trades.ipynb"
    create_data_notebook(
        str(csv_path), str(nb_path),
        title="技术工种与手工业 (SKL) — 完整数据",
        description="104 occupations × 45 countries/regions = 4,680 rows",
    )
    print(f"Notebook written to {nb_path}")


if __name__ == "__main__":
    main()
