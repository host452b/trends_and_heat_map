#!/usr/bin/env python3
"""Generate engineering_manufacturing.csv — ENG data for Global Career Development Index."""
import csv, sys, random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from tools.score_calculator import load_weights, calculate_composite

# === OCCUPATIONS (134) from categories.yaml ENG ===
O = []
def _a(mid, mid_zh, mid_en, items):
    for id_, zh, en, isco, onet, loc in items:
        O.append({"id": id_, "mid": mid, "mid_zh": mid_zh, "mid_en": mid_en,
                   "zh": zh, "en": en, "isco": isco, "onet": onet, "locality": loc})

_a("mechanical_eng", "机械工程", "Mechanical Engineering", [
    ("0101","机械设计工程师","Mechanical Design Engineer","2144","17-2141.00","global"),
    ("0102","热能工程师","Thermal Engineer","2144","17-2141.00","global"),
    ("0103","流体力学工程师","Fluid Mechanics Engineer","2144","17-2141.00","global"),
    ("0104","机器人工程师","Robotics Engineer","2144","17-2199.08","global"),
    ("0105","CAD/CAM工程师","CAD/CAM Engineer","2144","17-3013.00","global"),
    ("0106","设备工程师","Equipment Engineer","2144","17-2141.00","global"),
    ("0107","机电一体化工程师","Mechatronics Engineer","2144","17-2199.08","global"),
    ("0108","振动与噪声工程师","Vibration & Acoustics Engineer","2144","17-2141.00","global"),
    ("0109","液压工程师","Hydraulic Systems Engineer","2144","17-2141.00","global"),
    ("0110","有限元分析工程师(FEA)","Finite Element Analysis (FEA) Engineer","2144","17-2141.00","global"),
    ("0111","3D打印/增材制造工程师","Additive Manufacturing Engineer","2144","17-2141.00","global"),
    ("0112","包装工程师","Packaging Engineer","2144","17-2141.00","global"),
])
_a("electrical_eng", "电气工程", "Electrical Engineering", [
    ("0201","电力工程师","Power Engineer","2151","17-2071.00","global"),
    ("0202","电子工程师","Electronics Engineer","2152","17-2072.00","global"),
    ("0203","控制工程师","Control Systems Engineer","2151","17-2072.01","global"),
    ("0204","自动化工程师","Automation Engineer","2151","17-2072.01","global"),
    ("0205","PLC编程工程师","PLC Programmer","2151","17-2072.01","global"),
    ("0206","电气设计工程师","Electrical Design Engineer","2151","17-2071.00","global"),
    ("0207","仪器仪表工程师","Instrumentation Engineer","2151","17-2072.01","global"),
    ("0208","电磁兼容工程师","EMC Engineer","2152","17-2072.00","global"),
    ("0209","电力系统规划工程师","Power System Planning Engineer","2151","17-2071.00","global"),
    ("0210","变电站工程师","Substation Engineer","2151","17-2071.00","global"),
    ("0211","信号与通信工程师","Signal & Communications Engineer","2153","17-2061.00","global"),
    ("0212","射频工程师(RF)","RF Engineer","2153","17-2061.00","global"),
    ("0213","光电工程师","Optoelectronics Engineer","2152","17-2072.00","global"),
])
_a("chemical_eng", "化学工程", "Chemical Engineering", [
    ("0301","化工工艺工程师","Chemical Process Engineer","2145","17-2041.00","global"),
    ("0302","材料工程师","Materials Engineer","2146","17-2131.00","global"),
    ("0303","高分子材料工程师","Polymer Engineer","2146","17-2131.00","global"),
    ("0304","涂料工程师","Coatings Engineer","2145","17-2041.00","global"),
    ("0305","生物化学工程师","Biochemical Engineer","2145","17-2041.00","global"),
    ("0306","催化剂工程师","Catalyst Engineer","2145","17-2041.00","global"),
    ("0307","陶瓷工程师","Ceramic Engineer","2146","17-2131.00","global"),
    ("0308","纳米材料研究员","Nanomaterials Researcher","2146","17-2131.00","global"),
    ("0309","食品工程师","Food Engineer","2145","17-2041.00","global"),
    ("0310","环境化学工程师","Environmental Chemical Engineer","2145","17-2041.00","global"),
    ("0311","复合材料工程师","Composite Materials Engineer","2146","17-2131.00","global"),
    ("0312","腐蚀工程师","Corrosion Engineer","2145","17-2041.00","global"),
])
_a("civil_construction", "土木与建筑", "Civil Engineering & Architecture", [
    ("0401","结构工程师","Structural Engineer","2142","17-2051.00","global"),
    ("0402","桥梁工程师","Bridge Engineer","2142","17-2051.00","global"),
    ("0403","建筑师","Architect","2161","17-1011.00","global"),
    ("0404","测量工程师","Surveyor","2165","17-1022.00","global"),
    ("0405","岩土工程师","Geotechnical Engineer","2142","17-2051.00","global"),
    ("0406","道路工程师","Highway Engineer","2142","17-2051.00","global"),
    ("0407","水利工程师","Hydraulic Engineer","2142","17-2051.01","global"),
    ("0408","景观设计师","Landscape Architect","2162","17-1012.00","global"),
    ("0409","城市规划师","Urban Planner","2164","19-3051.00","global"),
    ("0410","工程造价师","Quantity Surveyor / Cost Estimator","2149","13-1051.00","global"),
    ("0411","BIM工程师","BIM Engineer","2142","17-2051.00","global"),
    ("0412","隧道工程师","Tunnel Engineer","2142","17-2051.00","global"),
    ("0413","消防工程师","Fire Protection Engineer","2149","17-2111.02","global"),
    ("0414","地下管网工程师","Underground Utilities Engineer","2142","17-2051.00","global"),
    ("0415","海洋工程师","Ocean/Marine Engineer","2142","17-2121.00","global"),
    ("0416","暖通空调设计工程师","HVAC Design Engineer","2144","17-2141.00","global"),
    ("0417","给排水工程师","Water Supply & Drainage Engineer","2142","17-2051.01","global"),
])
_a("aerospace", "航空航天", "Aerospace Engineering", [
    ("0501","飞机设计工程师","Aircraft Design Engineer","2144","17-2011.00","global"),
    ("0502","航天工程师","Aerospace Engineer","2144","17-2011.00","global"),
    ("0503","卫星工程师","Satellite Engineer","2144","17-2011.00","global"),
    ("0504","推进系统工程师","Propulsion Engineer","2144","17-2011.00","global"),
    ("0505","航空电子工程师","Avionics Engineer","2152","17-2011.00","global"),
    ("0506","航空结构工程师","Aerospace Structural Engineer","2144","17-2011.00","global"),
    ("0507","无人机工程师","Drone Engineer / UAV Engineer","2144","17-2011.00","global"),
    ("0508","航空材料工程师","Aerospace Materials Engineer","2146","17-2131.00","global"),
    ("0509","飞行测试工程师","Flight Test Engineer","2144","17-2011.00","global"),
    ("0510","空气动力学工程师","Aerodynamics Engineer","2144","17-2011.00","global"),
])
_a("automotive", "汽车", "Automotive Engineering", [
    ("0601","汽车设计工程师","Automotive Design Engineer","2144","17-2141.02","global"),
    ("0602","新能源汽车工程师","New Energy Vehicle Engineer","2144","17-2141.02","global"),
    ("0603","自动驾驶工程师","Autonomous Driving Engineer","2144","17-2141.02","global"),
    ("0604","车辆动力系统工程师","Powertrain Engineer","2144","17-2141.02","global"),
    ("0605","汽车电子工程师","Automotive Electronics Engineer","2152","17-2072.00","global"),
    ("0606","汽车安全工程师","Automotive Safety Engineer","2144","17-2141.02","global"),
    ("0607","汽车NVH工程师","Automotive NVH Engineer","2144","17-2141.02","global"),
    ("0608","电池系统工程师","Battery Systems Engineer","2144","17-2141.02","global"),
    ("0609","车身工程师","Vehicle Body Engineer","2144","17-2141.02","global"),
    ("0610","底盘工程师","Chassis Engineer","2144","17-2141.02","global"),
    ("0611","汽车标定工程师","Automotive Calibration Engineer","2144","17-2141.02","global"),
    ("0612","车联网(V2X)工程师","V2X / Connected Vehicle Engineer","2153","17-2061.00","global"),
])
_a("semiconductor", "半导体", "Semiconductor", [
    ("0701","芯片设计工程师(IC Designer)","IC Design Engineer","2152","17-2072.00","global"),
    ("0702","半导体制造工程师","Semiconductor Fabrication Engineer","2152","17-2072.00","global"),
    ("0703","封装测试工程师","Packaging & Testing Engineer","2152","17-2072.00","global"),
    ("0704","FPGA工程师","FPGA Engineer","2152","17-2072.00","global"),
    ("0705","半导体工艺工程师","Semiconductor Process Engineer","2152","17-2072.00","global"),
    ("0706","光刻工程师","Lithography Engineer","2152","17-2072.00","global"),
    ("0707","EDA工具工程师","EDA Tools Engineer","2152","17-2072.00","global"),
    ("0708","芯片验证工程师","Chip Verification Engineer","2152","17-2072.00","global"),
    ("0709","模拟IC设计工程师","Analog IC Design Engineer","2152","17-2072.00","global"),
    ("0710","晶圆代工工程师","Foundry / Wafer Fab Engineer","2152","17-2072.00","global"),
])
_a("nuclear_eng", "核工程", "Nuclear Engineering", [
    ("0801","核电工程师","Nuclear Power Engineer","2149","17-2161.00","global"),
    ("0802","核医学物理师","Medical Physicist (Nuclear)","2111","29-1299.01","global"),
    ("0803","辐射防护工程师","Radiation Protection Engineer","2149","17-2161.00","global"),
    ("0804","核反应堆操作员","Nuclear Reactor Operator","3131","51-8011.00","global"),
    ("0805","核废料管理工程师","Nuclear Waste Management Engineer","2149","17-2161.00","global"),
    ("0806","核燃料工程师","Nuclear Fuel Engineer","2149","17-2161.00","global"),
])
_a("manufacturing_mgmt", "制造管理", "Manufacturing Management", [
    ("0901","工厂厂长","Plant Manager","1321","11-3051.00","global"),
    ("0902","精益生产工程师","Lean Manufacturing Engineer","2141","17-2112.00","global"),
    ("0903","工业工程师","Industrial Engineer","2141","17-2112.00","global"),
    ("0904","生产计划员","Production Planner","3122","11-3051.04","global"),
    ("0905","制造工程师","Manufacturing Engineer","2141","17-2112.00","global"),
    ("0906","供应商质量工程师","Supplier Quality Engineer","2141","17-2112.00","global"),
    ("0907","设备维护经理","Maintenance Manager","1321","11-3051.00","global"),
    ("0908","安全工程师(工厂)","Factory Safety Engineer","2149","17-2111.02","global"),
    ("0909","自动化产线工程师","Automated Production Line Engineer","2141","17-2112.00","global"),
    ("0910","智能制造工程师","Smart Manufacturing / Industry 4.0 Engineer","2141","17-2112.00","global"),
])
_a("quality_control", "质量控制", "Quality Control", [
    ("1001","质量保证工程师(QA)","Quality Assurance Engineer","2141","17-2112.01","global"),
    ("1002","质量控制工程师(QC)","Quality Control Engineer","2141","17-2112.01","global"),
    ("1003","计量工程师","Metrology Engineer","2149","17-2112.01","global"),
    ("1004","标准化工程师","Standards Engineer","2141","17-2112.01","global"),
    ("1005","无损检测工程师","Non-Destructive Testing (NDT) Engineer","2149","17-3029.09","global"),
    ("1006","可靠性工程师","Reliability Engineer","2141","17-2112.01","global"),
    ("1007","六西格玛黑带","Six Sigma Black Belt","2141","17-2112.00","global"),
    ("1008","认证工程师(CE/UL)","Certification Engineer (CE/UL)","2141","17-2112.01","global"),
])
_a("telecom_eng", "通信工程", "Telecommunications Engineering", [
    ("1101","通信网络工程师","Telecommunications Network Engineer","2153","17-2061.00","global"),
    ("1102","5G系统工程师","5G Systems Engineer","2153","17-2061.00","global"),
    ("1103","光纤工程师","Fiber Optics Engineer","2153","17-2061.00","global"),
    ("1104","卫星通信工程师","Satellite Communications Engineer","2153","17-2061.00","global"),
    ("1105","天线工程师","Antenna Engineer","2153","17-2061.00","global"),
])
_a("biomedical_eng", "生物医学工程", "Biomedical Engineering", [
    ("1201","生物医学工程师","Biomedical Engineer","2149","17-2031.00","global"),
    ("1202","医疗器械设计工程师","Medical Device Design Engineer","2149","17-2031.00","global"),
    ("1203","康复工程师","Rehabilitation Engineer","2149","17-2031.00","global"),
    ("1204","组织工程研究员","Tissue Engineering Researcher","2149","17-2031.00","global"),
    ("1205","生物力学工程师","Biomechanical Engineer","2149","17-2031.00","global"),
])
_a("environmental_eng", "环境工程", "Environmental Engineering", [
    ("1301","环境工程师(制造)","Environmental Engineer (Manufacturing)","2143","17-2081.00","global"),
    ("1302","噪声控制工程师","Noise Control / Acoustic Engineer","2149","17-2199.01","global"),
    ("1303","能源审计师","Energy Auditor","2149","13-1199.01","global"),
    ("1304","绿色建筑工程师","Green Building / LEED Engineer","2142","17-2051.00","global"),
    ("1305","水处理工程师(工业)","Industrial Water Treatment Engineer","2143","17-2081.00","global"),
    ("1306","可靠性/可用性工程师(RAMS)","RAMS Engineer (Reliability, Availability)","2141","17-2112.01","global"),
    ("1307","安全评价工程师","Safety Assessment Engineer (HAZOP)","2149","17-2111.02","global"),
    ("1308","防腐蚀工程师","Corrosion Protection Engineer","2145","17-2041.00","global"),
    ("1309","管道完整性工程师","Pipeline Integrity Engineer","2145","17-2171.00","global"),
    ("1310","激光工程师","Laser Engineer","2152","17-2072.00","global"),
    ("1311","焊接工程师","Welding Engineer","2144","17-2141.00","global"),
    ("1312","电镀工程师","Electroplating / Surface Treatment Engineer","2145","17-2041.00","global"),
    ("1313","真空技术工程师","Vacuum Technology Engineer","2152","17-2072.00","global"),
    ("1314","爆炸力学工程师","Explosion Mechanics / Blast Engineer","2149","17-2199.00","global"),
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

# === COUNTRY PROFILES for ENG ===
# Keys: eng(eng ecosystem maturity), comp(compensation), wlb(work-life balance),
#   mfg(manufacturing strength), stab(stability), auto(auto industry),
#   semi(semiconductor), aero(aerospace), constr(construction boom),
#   safety(safety standards), edu(edu quality), intl(international openness),
#   gender(gender equality), reg(regulatory), ot(overtime culture, higher=less OT)
CP = {
    "US": {"eng":9.0,"comp":9.0,"wlb":6.0,"mfg":8.0,"stab":6.0,"auto":8.5,"semi":9.0,"aero":9.5,"constr":7.0,"safety":8.5,"edu":9.0,"intl":8.5,"gender":7.5,"reg":6.5,"ot":5.0},
    "DE": {"eng":9.5,"comp":8.0,"wlb":8.0,"mfg":9.5,"stab":8.0,"auto":9.5,"semi":6.5,"aero":8.0,"constr":6.5,"safety":9.0,"edu":8.5,"intl":8.0,"gender":7.0,"reg":7.5,"ot":7.5},
    "JP": {"eng":9.0,"comp":7.0,"wlb":4.5,"mfg":9.0,"stab":7.5,"auto":9.5,"semi":8.0,"aero":7.0,"constr":7.5,"safety":9.0,"edu":8.0,"intl":5.0,"gender":5.0,"reg":7.0,"ot":3.5},
    "KR": {"eng":8.5,"comp":7.0,"wlb":4.0,"mfg":8.5,"stab":6.5,"auto":8.5,"semi":9.5,"aero":6.0,"constr":7.5,"safety":7.5,"edu":8.0,"intl":6.0,"gender":4.5,"reg":6.5,"ot":3.0},
    "CN": {"eng":8.5,"comp":6.5,"wlb":3.5,"mfg":9.5,"stab":5.5,"auto":9.0,"semi":7.5,"aero":7.5,"constr":9.0,"safety":5.5,"edu":7.5,"intl":5.0,"gender":5.5,"reg":5.0,"ot":2.5},
    "TW": {"eng":8.0,"comp":5.5,"wlb":5.0,"mfg":8.0,"stab":6.0,"auto":5.0,"semi":9.5,"aero":4.0,"constr":6.0,"safety":7.0,"edu":7.5,"intl":6.5,"gender":6.0,"reg":6.0,"ot":4.0},
    "GB": {"eng":8.0,"comp":7.5,"wlb":7.0,"mfg":6.5,"stab":7.0,"auto":7.0,"semi":5.0,"aero":8.5,"constr":7.0,"safety":8.5,"edu":8.5,"intl":9.0,"gender":7.5,"reg":7.0,"ot":6.5},
    "FR": {"eng":8.0,"comp":7.0,"wlb":8.0,"mfg":7.0,"stab":7.0,"auto":7.5,"semi":5.5,"aero":9.0,"constr":6.5,"safety":8.0,"edu":8.0,"intl":7.5,"gender":7.0,"reg":7.5,"ot":7.0},
    "CH": {"eng":9.0,"comp":9.5,"wlb":8.5,"mfg":8.5,"stab":9.0,"auto":4.0,"semi":5.0,"aero":5.0,"constr":6.0,"safety":9.0,"edu":9.0,"intl":8.5,"gender":7.0,"reg":7.0,"ot":7.5},
    "SE": {"eng":8.0,"comp":7.0,"wlb":9.0,"mfg":7.5,"stab":8.0,"auto":7.5,"semi":4.0,"aero":7.0,"constr":6.0,"safety":9.0,"edu":8.5,"intl":8.5,"gender":9.0,"reg":7.0,"ot":8.5},
    "NL": {"eng":7.5,"comp":7.5,"wlb":9.0,"mfg":7.0,"stab":7.5,"auto":4.0,"semi":8.0,"aero":5.0,"constr":6.5,"safety":8.5,"edu":8.0,"intl":9.0,"gender":8.5,"reg":7.0,"ot":8.0},
    "FI": {"eng":7.5,"comp":6.5,"wlb":9.0,"mfg":7.0,"stab":7.5,"auto":3.5,"semi":4.0,"aero":5.0,"constr":5.5,"safety":9.0,"edu":9.0,"intl":8.0,"gender":9.0,"reg":7.0,"ot":8.5},
    "DK": {"eng":7.5,"comp":7.0,"wlb":9.0,"mfg":6.5,"stab":8.0,"auto":3.5,"semi":3.5,"aero":4.5,"constr":6.0,"safety":9.0,"edu":8.5,"intl":8.5,"gender":9.0,"reg":7.0,"ot":8.5},
    "IT": {"eng":7.0,"comp":5.5,"wlb":6.5,"mfg":7.5,"stab":5.5,"auto":7.5,"semi":4.0,"aero":7.0,"constr":6.0,"safety":7.0,"edu":7.0,"intl":6.5,"gender":5.5,"reg":6.5,"ot":5.5},
    "ES": {"eng":6.5,"comp":5.0,"wlb":7.0,"mfg":6.0,"stab":5.5,"auto":6.5,"semi":3.0,"aero":6.0,"constr":6.5,"safety":7.0,"edu":7.0,"intl":7.0,"gender":6.5,"reg":6.0,"ot":5.5},
    "PT": {"eng":6.0,"comp":4.5,"wlb":7.0,"mfg":5.5,"stab":5.5,"auto":4.5,"semi":3.0,"aero":4.0,"constr":5.5,"safety":7.0,"edu":6.5,"intl":7.5,"gender":7.0,"reg":6.0,"ot":6.0},
    "PL": {"eng":6.5,"comp":5.5,"wlb":7.0,"mfg":7.0,"stab":6.5,"auto":6.5,"semi":3.5,"aero":5.0,"constr":7.0,"safety":6.5,"edu":7.0,"intl":7.5,"gender":6.5,"reg":6.5,"ot":6.0},
    "CZ": {"eng":7.0,"comp":5.5,"wlb":7.5,"mfg":7.5,"stab":7.0,"auto":8.0,"semi":4.0,"aero":5.0,"constr":6.5,"safety":7.5,"edu":7.0,"intl":7.5,"gender":6.5,"reg":6.5,"ot":6.5},
    "RU": {"eng":7.0,"comp":4.5,"wlb":5.5,"mfg":7.0,"stab":4.0,"auto":5.0,"semi":4.0,"aero":7.5,"constr":6.5,"safety":5.5,"edu":7.5,"intl":3.5,"gender":6.0,"reg":4.5,"ot":5.5},
    "SG": {"eng":7.5,"comp":8.0,"wlb":5.5,"mfg":7.0,"stab":8.0,"auto":3.0,"semi":8.0,"aero":5.0,"constr":7.5,"safety":8.5,"edu":8.5,"intl":9.5,"gender":7.0,"reg":8.0,"ot":4.5},
    "IN": {"eng":7.0,"comp":4.5,"wlb":4.5,"mfg":7.0,"stab":5.0,"auto":7.0,"semi":5.0,"aero":6.5,"constr":8.5,"safety":4.5,"edu":7.0,"intl":7.0,"gender":4.0,"reg":5.0,"ot":4.0},
    "AU": {"eng":7.5,"comp":8.0,"wlb":8.0,"mfg":5.5,"stab":7.5,"auto":4.0,"semi":3.0,"aero":5.0,"constr":8.0,"safety":8.5,"edu":8.0,"intl":8.5,"gender":8.0,"reg":7.0,"ot":7.0},
    "CA": {"eng":7.5,"comp":7.5,"wlb":7.5,"mfg":6.0,"stab":7.0,"auto":6.5,"semi":4.0,"aero":7.5,"constr":7.5,"safety":8.5,"edu":8.0,"intl":9.0,"gender":8.0,"reg":7.0,"ot":6.5},
    "NZ": {"eng":6.5,"comp":6.5,"wlb":8.5,"mfg":4.5,"stab":7.5,"auto":2.0,"semi":2.0,"aero":3.0,"constr":7.0,"safety":8.5,"edu":7.5,"intl":8.0,"gender":8.5,"reg":7.0,"ot":7.5},
    "BR": {"eng":6.0,"comp":4.5,"wlb":6.0,"mfg":6.5,"stab":4.5,"auto":7.0,"semi":3.0,"aero":7.0,"constr":7.0,"safety":5.0,"edu":6.0,"intl":5.0,"gender":5.5,"reg":5.5,"ot":5.0},
    "MX": {"eng":5.5,"comp":4.0,"wlb":5.5,"mfg":7.0,"stab":4.5,"auto":8.0,"semi":3.5,"aero":5.0,"constr":7.0,"safety":5.0,"edu":5.5,"intl":5.5,"gender":5.0,"reg":5.0,"ot":4.5},
    "AR": {"eng":5.5,"comp":3.5,"wlb":5.5,"mfg":5.0,"stab":3.5,"auto":5.5,"semi":2.5,"aero":4.0,"constr":5.0,"safety":5.0,"edu":6.5,"intl":5.0,"gender":5.5,"reg":4.5,"ot":5.0},
    "CL": {"eng":5.5,"comp":4.5,"wlb":6.0,"mfg":4.5,"stab":5.5,"auto":2.5,"semi":2.0,"aero":3.0,"constr":6.0,"safety":6.0,"edu":6.0,"intl":6.0,"gender":5.5,"reg":5.5,"ot":5.5},
    "CO": {"eng":5.0,"comp":3.5,"wlb":5.5,"mfg":4.5,"stab":4.5,"auto":3.0,"semi":2.0,"aero":3.0,"constr":6.0,"safety":5.0,"edu":5.5,"intl":5.0,"gender":5.0,"reg":5.0,"ot":5.0},
    "AE": {"eng":7.0,"comp":8.0,"wlb":5.5,"mfg":5.5,"stab":7.0,"auto":3.0,"semi":3.0,"aero":6.0,"constr":9.0,"safety":7.5,"edu":7.0,"intl":8.5,"gender":5.5,"reg":6.5,"ot":5.0},
    "SA": {"eng":6.0,"comp":6.5,"wlb":5.5,"mfg":5.0,"stab":6.0,"auto":3.0,"semi":2.5,"aero":5.5,"constr":8.5,"safety":6.0,"edu":6.0,"intl":5.5,"gender":3.5,"reg":5.5,"ot":5.0},
    "IL": {"eng":8.0,"comp":7.5,"wlb":6.0,"mfg":6.5,"stab":5.5,"auto":3.0,"semi":7.5,"aero":8.5,"constr":6.5,"safety":8.0,"edu":8.5,"intl":8.0,"gender":7.0,"reg":6.0,"ot":5.0},
    "TR": {"eng":6.0,"comp":4.0,"wlb":5.0,"mfg":6.5,"stab":4.0,"auto":7.0,"semi":3.0,"aero":6.0,"constr":7.5,"safety":5.5,"edu":6.5,"intl":5.5,"gender":4.5,"reg":5.0,"ot":4.5},
    "TH": {"eng":5.5,"comp":3.5,"wlb":5.5,"mfg":6.5,"stab":5.5,"auto":7.5,"semi":4.0,"aero":3.5,"constr":6.5,"safety":5.5,"edu":5.5,"intl":5.5,"gender":6.0,"reg":5.0,"ot":5.5},
    "VN": {"eng":5.0,"comp":3.0,"wlb":5.0,"mfg":6.5,"stab":5.0,"auto":4.5,"semi":4.0,"aero":3.0,"constr":7.5,"safety":4.5,"edu":5.5,"intl":5.5,"gender":5.5,"reg":5.0,"ot":4.5},
    "ID": {"eng":5.0,"comp":3.5,"wlb":5.5,"mfg":6.0,"stab":5.0,"auto":5.0,"semi":3.0,"aero":4.0,"constr":7.5,"safety":4.5,"edu":5.0,"intl":4.5,"gender":5.0,"reg":5.0,"ot":5.0},
    "MY": {"eng":6.0,"comp":4.5,"wlb":5.5,"mfg":7.0,"stab":6.0,"auto":5.0,"semi":7.0,"aero":4.0,"constr":7.0,"safety":6.0,"edu":6.0,"intl":6.5,"gender":5.5,"reg":5.5,"ot":5.0},
    "PH": {"eng":5.0,"comp":3.0,"wlb":5.0,"mfg":5.0,"stab":4.5,"auto":3.5,"semi":5.5,"aero":3.0,"constr":6.5,"safety":4.5,"edu":5.5,"intl":6.5,"gender":6.5,"reg":4.5,"ot":4.5},
    "HK": {"eng":6.5,"comp":7.0,"wlb":4.5,"mfg":3.5,"stab":6.5,"auto":2.0,"semi":3.0,"aero":3.0,"constr":7.5,"safety":8.0,"edu":7.5,"intl":9.0,"gender":6.5,"reg":6.5,"ot":3.5},
    "PK": {"eng":4.5,"comp":2.5,"wlb":4.5,"mfg":4.5,"stab":3.5,"auto":3.0,"semi":2.0,"aero":3.5,"constr":6.0,"safety":3.5,"edu":4.5,"intl":4.5,"gender":3.0,"reg":4.0,"ot":4.5},
    "BD": {"eng":4.0,"comp":2.0,"wlb":4.5,"mfg":5.0,"stab":3.5,"auto":2.0,"semi":1.5,"aero":2.0,"constr":6.5,"safety":3.0,"edu":4.0,"intl":4.5,"gender":3.5,"reg":3.5,"ot":4.5},
    "ZA": {"eng":5.5,"comp":4.0,"wlb":5.5,"mfg":5.5,"stab":4.5,"auto":5.5,"semi":2.5,"aero":4.0,"constr":6.0,"safety":5.5,"edu":5.5,"intl":5.5,"gender":5.5,"reg":5.0,"ot":5.5},
    "NG": {"eng":4.0,"comp":2.5,"wlb":4.5,"mfg":3.5,"stab":3.5,"auto":2.0,"semi":1.5,"aero":2.5,"constr":6.0,"safety":3.5,"edu":4.0,"intl":4.5,"gender":4.0,"reg":3.5,"ot":4.5},
    "KE": {"eng":4.5,"comp":2.5,"wlb":5.0,"mfg":3.5,"stab":4.0,"auto":2.0,"semi":1.5,"aero":2.5,"constr":6.0,"safety":4.0,"edu":4.5,"intl":5.0,"gender":4.5,"reg":4.0,"ot":5.0},
    "EG": {"eng":5.0,"comp":3.0,"wlb":5.0,"mfg":5.0,"stab":4.0,"auto":3.0,"semi":2.0,"aero":4.0,"constr":7.5,"safety":4.5,"edu":5.0,"intl":5.0,"gender":3.5,"reg":4.0,"ot":4.5},
}

# === MID-CATEGORY DEFAULT SCORES ===
# Each mid-category has a default score dict; per-occupation overrides only differ fields.
# Keys: lc=learning_cost, er=education_req, gc=growth_coeff, cl=career_lifespan,
#   op=opportunity, ms=market_size, sd=supply_demand, ds=developed_scarcity,
#   va=value_added, cp_=cost_performance, st=stability, sa=safety,
#   od=occupational_disease, ot=overtime, bu=burnout, sv=skill_versatility,
#   cs=career_switch, rv=reputation_variance, ar=ai_resistance, ss=social_status,
#   rf=remote_friendly, au=autonomy, ff=family_friendly, fu=fulfillment,
#   en=entrepreneurship, ge=gender_equality, af=age_flexibility,
#   si=social_interaction, pd=physical_demand, lb=license_barrier,
#   cy=cycle_sensitivity, sj=side_job_compat, im=intl_mobility, mo=industry_monopoly,
#   tl=trend_long, ts=trend_short, edu=typical_education, age=typical_entry_age

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
    "mechanical_eng": _d(6.0,6.0,5.5,7.5, 6.0,6.5,5.5,5.5, 6.5,6.0, 7.0,7.5,5.5,5.5,5.0, 6.5,5.5,1.5, 6.5,6.5,4.0,6.0,6.0,6.5,4.5,4.5,6.5, 5.0,3.5,3.0,5.5,4.0,6.5,3.0, 2,1,"本科/硕士","22-28"),
    "electrical_eng": _d(6.0,6.0,6.0,7.5, 6.5,6.5,6.0,6.0, 6.5,6.5, 7.0,7.0,5.5,5.5,5.0, 6.5,5.5,1.5, 6.0,6.5,4.5,6.0,5.5,6.5,4.5,4.5,6.5, 5.0,3.0,3.5,5.0,4.0,6.0,3.5, 2,1,"本科/硕士","22-28"),
    "chemical_eng": _d(6.5,6.5,5.0,7.5, 5.5,5.5,5.5,5.5, 6.5,6.0, 7.0,6.0,4.5,5.5,5.0, 6.0,5.0,1.5, 6.5,6.5,3.5,5.5,5.5,6.5,4.0,4.5,6.5, 5.0,3.5,3.5,5.0,3.5,6.0,3.5, 2,0,"本科/硕士","22-28"),
    "civil_construction": _d(6.0,6.0,5.0,8.0, 6.5,7.0,5.5,5.0, 6.0,5.5, 7.0,5.5,5.0,5.5,5.0, 6.0,5.0,1.5, 7.0,6.5,3.0,5.5,5.5,6.0,4.5,4.0,7.0, 6.5,5.0,5.0,6.5,3.5,5.0,3.5, 2,1,"本科/硕士","22-28"),
    "aerospace": _d(7.5,7.5,6.5,8.0, 5.5,4.0,7.0,7.5, 8.0,6.5, 7.5,6.5,5.5,5.0,5.0, 6.0,5.0,1.0, 7.5,8.0,4.0,6.0,5.5,8.0,3.0,4.0,6.0, 5.5,3.5,4.0,4.5,3.0,6.5,5.5, 3,2,"硕士","24-30"),
    "automotive": _d(6.5,6.0,6.5,7.0, 6.5,6.5,6.0,6.0, 7.0,6.5, 6.5,7.0,5.5,5.0,5.0, 6.5,5.5,1.5, 6.0,6.5,3.5,5.5,5.5,6.5,4.0,4.5,6.5, 5.5,3.0,3.0,6.0,3.5,6.5,4.5, 3,2,"本科/硕士","22-28"),
    "semiconductor": _d(7.5,7.0,7.0,7.0, 7.0,5.0,7.5,8.0, 8.0,7.0, 6.5,7.0,5.0,4.5,5.0, 6.0,5.0,1.0, 6.5,7.5,4.0,6.0,5.0,7.0,3.5,4.0,5.5, 4.5,2.5,2.5,5.5,3.5,7.0,6.0, 4,3,"硕士","23-28"),
    "nuclear_eng": _d(8.0,8.0,5.0,8.5, 4.5,3.0,6.5,7.0, 7.5,6.0, 8.5,5.0,4.0,6.0,4.5, 5.0,4.0,1.0, 8.5,8.0,2.0,5.5,5.0,7.5,2.0,4.0,7.0, 5.5,4.0,7.0,3.5,2.5,5.5,7.0, 2,1,"硕士/博士","25-32"),
    "manufacturing_mgmt": _d(5.5,5.5,5.5,8.0, 6.5,7.0,5.5,5.0, 6.5,6.5, 7.0,7.0,5.5,5.0,5.0, 7.0,6.0,1.5, 5.5,6.5,3.0,6.5,5.5,6.0,5.0,4.5,7.0, 7.0,3.0,3.0,5.5,3.5,5.5,3.5, 2,1,"本科","22-30"),
    "quality_control": _d(5.5,5.5,5.0,8.0, 6.0,6.5,5.0,5.0, 5.5,5.5, 7.5,7.5,6.0,6.0,5.5, 6.5,5.5,1.0, 5.5,5.5,3.5,5.5,6.0,5.5,4.0,5.0,7.0, 6.0,3.0,4.0,4.5,3.5,6.0,3.0, 2,1,"本科","22-28"),
    "telecom_eng": _d(6.5,6.0,6.0,7.5, 6.5,6.0,6.0,6.0, 6.5,6.5, 7.0,7.5,5.5,5.0,5.0, 6.0,5.5,1.5, 5.5,6.5,4.5,6.0,5.5,6.0,4.5,4.5,6.5, 5.5,3.5,3.5,5.0,4.0,6.5,4.0, 3,2,"本科/硕士","22-28"),
    "biomedical_eng": _d(7.0,7.0,7.0,8.0, 6.5,5.0,7.0,7.0, 7.5,6.5, 7.0,8.0,6.5,6.0,5.0, 7.0,6.0,1.0, 7.5,7.5,4.5,6.5,6.0,8.0,5.0,5.5,6.0, 5.5,2.5,4.5,4.0,4.0,7.5,4.5, 4,3,"硕士","24-30"),
    "environmental_eng": _d(6.0,6.0,5.5,7.5, 5.5,5.5,5.5,5.5, 6.0,5.5, 7.0,6.0,5.0,6.0,5.0, 6.5,5.5,1.5, 6.5,6.0,3.5,5.5,6.0,6.5,4.0,5.0,7.0, 5.5,4.0,4.0,4.5,3.5,5.5,3.5, 3,2,"本科/硕士","22-28"),
}

# === PER-OCCUPATION OVERRIDES (only fields that differ from mid-category default) ===
# Format: {occ_id: {field: value, ...}}
OVR = {
    # mechanical_eng
    "0101": {},  # default
    "0102": {"learning_cost":6.5,"education_req":6.5,"market_size":5.5,"supply_demand":5.0,"opportunity":5.0},
    "0103": {"learning_cost":7.0,"education_req":7.0,"market_size":4.5,"supply_demand":5.0,"ai_resistance":7.0,"opportunity":5.0,"social_status":7.0},
    "0104": {"growth_coeff":7.5,"opportunity":7.5,"supply_demand":7.5,"developed_scarcity":7.5,"ai_resistance":7.0,"trend_long":4,"trend_short":4,"remote_friendly":5.0,"value_added":7.5,"social_status":7.5},
    "0105": {"learning_cost":5.0,"education_req":5.0,"ai_resistance":5.0,"remote_friendly":5.5,"career_lifespan":6.5,"social_status":5.5,"trend_short":0},
    "0106": {"learning_cost":5.5,"education_req":5.5,"stability":7.5,"remote_friendly":2.5,"physical_demand":4.0,"career_lifespan":8.0,"ai_resistance":7.0},
    "0107": {"growth_coeff":7.0,"opportunity":7.0,"supply_demand":7.0,"developed_scarcity":7.0,"ai_resistance":6.5,"trend_long":3,"trend_short":3,"value_added":7.0,"social_status":7.0},
    "0108": {"learning_cost":7.0,"education_req":7.0,"market_size":4.0,"supply_demand":5.0,"ai_resistance":7.0,"opportunity":5.0},
    "0109": {"market_size":5.0,"supply_demand":5.0,"remote_friendly":2.5,"physical_demand":4.0,"opportunity":5.5},
    "0110": {"learning_cost":7.0,"education_req":7.0,"market_size":4.0,"supply_demand":5.5,"ai_resistance":7.0,"remote_friendly":5.0,"opportunity":5.0,"social_status":7.0},
    "0111": {"growth_coeff":7.5,"opportunity":7.0,"supply_demand":7.0,"developed_scarcity":7.0,"trend_long":4,"trend_short":4,"ai_resistance":6.0,"value_added":7.0},
    "0112": {"learning_cost":5.0,"education_req":5.0,"market_size":6.0,"ai_resistance":5.5,"social_status":5.5,"career_lifespan":7.0,"trend_short":0},
    # electrical_eng
    "0201": {"stability":7.5,"market_size":7.0,"license_barrier":4.5,"safety":6.5,"physical_demand":3.5,"remote_friendly":3.0},
    "0202": {"supply_demand":6.5,"growth_coeff":6.5,"remote_friendly":5.0},
    "0203": {"growth_coeff":6.5,"supply_demand":6.5,"ai_resistance":6.5,"remote_friendly":5.0},
    "0204": {"growth_coeff":7.0,"opportunity":7.0,"supply_demand":7.0,"developed_scarcity":7.0,"trend_long":3,"trend_short":3,"ai_resistance":5.5,"value_added":7.0,"remote_friendly":3.5},
    "0205": {"learning_cost":5.5,"education_req":5.0,"ai_resistance":5.0,"remote_friendly":3.0,"physical_demand":3.5,"social_status":5.5,"market_size":5.5},
    "0206": {"remote_friendly":5.0},
    "0207": {"market_size":5.5,"supply_demand":5.5,"remote_friendly":3.0,"physical_demand":3.5},
    "0208": {"learning_cost":7.0,"education_req":7.0,"market_size":4.0,"supply_demand":6.5,"ai_resistance":7.0,"social_status":7.0},
    "0209": {"stability":7.5,"market_size":5.5,"license_barrier":5.0,"remote_friendly":4.5,"growth_coeff":5.5},
    "0210": {"stability":8.0,"market_size":5.0,"license_barrier":5.0,"remote_friendly":2.5,"physical_demand":4.5,"safety":5.5},
    "0211": {"growth_coeff":6.5,"supply_demand":6.5,"remote_friendly":4.5,"market_size":5.5},
    "0212": {"learning_cost":7.0,"education_req":7.0,"supply_demand":7.0,"developed_scarcity":7.5,"market_size":4.5,"ai_resistance":7.0,"value_added":7.5,"social_status":7.5},
    "0213": {"learning_cost":7.0,"education_req":7.0,"market_size":4.5,"supply_demand":6.0,"growth_coeff":6.5,"ai_resistance":7.0},
    # chemical_eng
    "0301": {"market_size":6.0,"remote_friendly":3.0,"physical_demand":3.5,"safety":5.5},
    "0302": {"growth_coeff":6.0,"supply_demand":6.0,"developed_scarcity":6.0,"opportunity":6.0,"market_size":6.0,"trend_short":1},
    "0303": {"market_size":5.0,"supply_demand":5.0},
    "0304": {"learning_cost":5.5,"education_req":5.5,"market_size":5.0,"social_status":5.5,"ai_resistance":5.5},
    "0305": {"growth_coeff":6.5,"opportunity":6.0,"supply_demand":6.5,"developed_scarcity":6.5,"trend_long":3,"trend_short":2,"value_added":7.0},
    "0306": {"market_size":3.5,"supply_demand":6.0,"ai_resistance":7.0,"social_status":7.0,"learning_cost":7.5,"education_req":7.5},
    "0307": {"market_size":4.0,"supply_demand":5.0,"social_status":6.0},
    "0308": {"learning_cost":8.0,"education_req":8.5,"growth_coeff":7.0,"opportunity":6.0,"supply_demand":7.0,"developed_scarcity":7.5,"value_added":7.5,"trend_long":4,"trend_short":3,"edu":"硕士/博士","age":"25-32","social_status":7.5,"ai_resistance":7.0,"remote_friendly":4.5},
    "0309": {"learning_cost":5.5,"education_req":5.5,"market_size":6.5,"ai_resistance":5.5,"safety":6.5,"social_status":5.5},
    "0310": {"growth_coeff":6.0,"opportunity":6.0,"trend_long":3,"trend_short":2,"ai_resistance":6.0},
    "0311": {"growth_coeff":6.5,"opportunity":6.0,"supply_demand":6.5,"developed_scarcity":6.5,"trend_long":3,"trend_short":2,"value_added":7.0},
    "0312": {"market_size":5.0,"supply_demand":5.5,"physical_demand":3.5,"remote_friendly":2.5},
    # civil_construction
    "0401": {"supply_demand":6.0,"developed_scarcity":5.5,"license_barrier":6.0,"ai_resistance":7.5,"social_status":7.0,"value_added":6.5},
    "0402": {"supply_demand":5.5,"market_size":5.5,"license_barrier":6.0,"ai_resistance":7.5,"social_status":7.0},
    "0403": {"learning_cost":7.0,"education_req":7.0,"supply_demand":5.5,"license_barrier":7.0,"ai_resistance":7.0,"social_status":8.0,"fulfillment":7.5,"remote_friendly":4.5,"value_added":6.5,"entrepreneurship":6.0,"career_lifespan":9.0},
    "0404": {"learning_cost":5.5,"education_req":5.5,"remote_friendly":2.0,"physical_demand":6.0,"license_barrier":5.0,"ai_resistance":6.0,"social_status":5.5,"market_size":6.5},
    "0405": {"supply_demand":5.5,"market_size":5.0,"license_barrier":5.5,"ai_resistance":7.5,"physical_demand":5.5},
    "0406": {"market_size":6.5,"remote_friendly":2.0,"physical_demand":5.5,"license_barrier":5.0},
    "0407": {"market_size":5.5,"supply_demand":5.5,"license_barrier":5.5,"ai_resistance":7.0},
    "0408": {"learning_cost":6.5,"education_req":6.5,"license_barrier":5.0,"fulfillment":7.5,"ai_resistance":7.5,"social_status":6.5,"remote_friendly":4.0,"entrepreneurship":5.5},
    "0409": {"growth_coeff":5.5,"license_barrier":5.5,"ai_resistance":7.0,"social_status":7.0,"remote_friendly":4.5,"fulfillment":7.0,"market_size":5.5},
    "0410": {"learning_cost":5.5,"education_req":5.5,"license_barrier":5.5,"market_size":6.5,"remote_friendly":5.0,"ai_resistance":5.5,"social_status":6.0},
    "0411": {"growth_coeff":7.0,"opportunity":7.0,"supply_demand":7.0,"developed_scarcity":6.5,"trend_long":4,"trend_short":4,"ai_resistance":5.5,"remote_friendly":6.0,"value_added":6.5},
    "0412": {"market_size":4.5,"supply_demand":5.5,"physical_demand":5.5,"ai_resistance":7.5,"safety":4.5,"license_barrier":5.5},
    "0413": {"supply_demand":5.5,"license_barrier":6.5,"safety":6.0,"market_size":5.0,"ai_resistance":7.0},
    "0414": {"remote_friendly":2.0,"physical_demand":5.5,"market_size":5.5,"ai_resistance":7.0,"social_status":5.5},
    "0415": {"learning_cost":7.0,"education_req":7.0,"market_size":4.0,"supply_demand":5.5,"ai_resistance":7.5,"social_status":7.0,"safety":5.0},
    "0416": {"market_size":6.0,"remote_friendly":4.0,"supply_demand":5.5,"license_barrier":4.5,"ai_resistance":6.0},
    "0417": {"market_size":6.0,"license_barrier":5.0,"remote_friendly":3.0,"ai_resistance":6.5},
    # aerospace
    "0501": {"ai_resistance":8.0,"social_status":8.5,"fulfillment":8.5,"value_added":8.5,"opportunity":6.0},
    "0502": {"value_added":8.5,"social_status":8.5,"fulfillment":8.5},
    "0503": {"growth_coeff":7.0,"opportunity":6.0,"supply_demand":7.5,"trend_short":3},
    "0504": {"market_size":3.5,"supply_demand":7.5,"ai_resistance":8.0,"social_status":8.5},
    "0505": {"market_size":4.5,"supply_demand":7.5,"growth_coeff":7.0,"remote_friendly":4.5},
    "0506": {"ai_resistance":8.0,"value_added":8.0},
    "0507": {"growth_coeff":8.0,"opportunity":7.5,"supply_demand":8.0,"developed_scarcity":7.0,"trend_long":4,"trend_short":4,"market_size":5.0,"ai_resistance":6.5,"value_added":7.0},
    "0508": {"ai_resistance":7.0,"supply_demand":6.5,"market_size":3.5},
    "0509": {"physical_demand":4.0,"safety":5.0,"remote_friendly":2.0,"ai_resistance":8.0,"market_size":3.5},
    "0510": {"learning_cost":8.0,"education_req":8.0,"market_size":3.0,"supply_demand":7.0,"ai_resistance":7.5,"social_status":8.0,"edu":"硕士/博士"},
    # automotive
    "0601": {"remote_friendly":4.0,"value_added":7.0,"ai_resistance":6.5},
    "0602": {"growth_coeff":8.0,"opportunity":8.0,"supply_demand":8.0,"developed_scarcity":7.5,"trend_long":4,"trend_short":5,"value_added":8.0,"ai_resistance":6.5},
    "0603": {"learning_cost":7.5,"education_req":7.5,"growth_coeff":8.5,"opportunity":8.0,"supply_demand":8.5,"developed_scarcity":8.5,"value_added":8.5,"trend_long":5,"trend_short":5,"remote_friendly":5.5,"ai_resistance":5.5,"social_status":8.0,"edu":"硕士"},
    "0604": {"remote_friendly":3.0,"physical_demand":3.5},
    "0605": {"growth_coeff":7.0,"supply_demand":7.0,"developed_scarcity":7.0,"value_added":7.5,"trend_short":3},
    "0606": {"license_barrier":4.0,"ai_resistance":7.0,"safety":6.0,"social_status":7.0},
    "0607": {"market_size":5.0,"supply_demand":5.5,"ai_resistance":7.0,"social_status":6.5},
    "0608": {"growth_coeff":8.0,"opportunity":8.0,"supply_demand":8.0,"developed_scarcity":8.0,"trend_long":5,"trend_short":5,"value_added":8.0,"ai_resistance":6.5,"social_status":7.5},
    "0609": {"ai_resistance":6.5,"market_size":6.0,"social_status":6.0,"trend_short":1},
    "0610": {"ai_resistance":6.5,"market_size":5.5,"trend_short":1},
    "0611": {"market_size":5.0,"supply_demand":5.5,"remote_friendly":3.0,"ai_resistance":6.0,"social_status":6.0},
    "0612": {"growth_coeff":8.0,"opportunity":7.5,"supply_demand":7.5,"developed_scarcity":7.5,"trend_long":4,"trend_short":4,"remote_friendly":5.5,"value_added":7.5,"ai_resistance":5.5},
    # semiconductor
    "0701": {"learning_cost":8.0,"education_req":8.0,"supply_demand":8.5,"developed_scarcity":9.0,"value_added":9.0,"social_status":8.5,"ai_resistance":7.0,"trend_short":4,"edu":"硕士/博士"},
    "0702": {"remote_friendly":2.0,"physical_demand":3.5,"safety":6.0,"learning_cost":7.0,"supply_demand":7.0},
    "0703": {"learning_cost":6.5,"education_req":6.0,"supply_demand":7.0,"market_size":5.5,"social_status":6.5,"remote_friendly":2.5,"physical_demand":3.0},
    "0704": {"supply_demand":7.0,"developed_scarcity":7.5,"remote_friendly":5.5,"ai_resistance":6.0,"social_status":7.0},
    "0705": {"remote_friendly":2.0,"physical_demand":3.5,"safety":6.0,"market_size":5.5},
    "0706": {"learning_cost":8.0,"education_req":8.0,"supply_demand":8.0,"developed_scarcity":8.5,"market_size":4.0,"ai_resistance":7.0,"social_status":8.0},
    "0707": {"supply_demand":7.0,"developed_scarcity":7.5,"remote_friendly":6.5,"value_added":8.5,"ai_resistance":5.5,"market_size":4.0},
    "0708": {"supply_demand":7.0,"developed_scarcity":7.5,"remote_friendly":5.5,"ai_resistance":5.5},
    "0709": {"learning_cost":8.0,"education_req":8.0,"supply_demand":8.5,"developed_scarcity":9.0,"value_added":9.0,"social_status":8.5,"ai_resistance":7.5,"market_size":4.0,"edu":"硕士/博士"},
    "0710": {"remote_friendly":2.0,"physical_demand":3.5,"safety":6.0,"market_size":5.0},
    # nuclear_eng
    "0801": {"license_barrier":8.0,"safety":4.5,"social_status":8.5,"value_added":8.0},
    "0802": {"learning_cost":8.5,"education_req":9.0,"social_status":8.5,"value_added":8.0,"license_barrier":8.0,"market_size":3.5,"safety":4.5,"ai_resistance":8.0},
    "0803": {"license_barrier":7.5,"safety":4.5,"market_size":3.5,"physical_demand":4.5},
    "0804": {"learning_cost":6.5,"education_req":6.0,"license_barrier":8.0,"safety":3.5,"physical_demand":4.0,"remote_friendly":1.0,"social_status":7.0,"value_added":6.5,"edu":"大专/本科","age":"22-28"},
    "0805": {"market_size":2.5,"safety":4.0,"license_barrier":7.5,"physical_demand":4.5,"trend_short":1},
    "0806": {"market_size":2.5,"safety":4.5,"license_barrier":7.5},
    # manufacturing_mgmt
    "0901": {"learning_cost":6.5,"education_req":6.0,"value_added":7.5,"social_status":7.5,"autonomy":8.0,"fulfillment":7.0,"remote_friendly":2.5,"career_lifespan":8.5,"ai_resistance":7.0,"age":"30-40"},
    "0902": {"ai_resistance":5.5,"growth_coeff":6.0,"supply_demand":6.0,"trend_short":2},
    "0903": {"opportunity":7.0,"market_size":7.5,"supply_demand":6.0,"ai_resistance":5.0,"remote_friendly":4.0},
    "0904": {"learning_cost":4.5,"education_req":4.5,"value_added":5.0,"social_status":5.0,"remote_friendly":3.5,"ai_resistance":4.5,"career_lifespan":7.0},
    "0905": {"remote_friendly":3.0,"physical_demand":3.5,"ai_resistance":6.0},
    "0906": {"remote_friendly":3.5,"supply_demand":6.0,"ai_resistance":6.5,"physical_demand":3.0},
    "0907": {"remote_friendly":2.0,"physical_demand":4.0,"safety":6.0,"stability":7.5,"ai_resistance":7.0,"social_status":6.5,"value_added":6.5,"age":"28-38"},
    "0908": {"license_barrier":5.0,"safety":5.5,"ai_resistance":7.0,"physical_demand":3.5,"remote_friendly":2.5,"fulfillment":6.5},
    "0909": {"growth_coeff":7.0,"opportunity":7.0,"supply_demand":7.0,"developed_scarcity":6.5,"trend_long":3,"trend_short":3,"remote_friendly":3.0,"value_added":7.0,"ai_resistance":5.0},
    "0910": {"growth_coeff":8.0,"opportunity":8.0,"supply_demand":8.0,"developed_scarcity":7.5,"trend_long":4,"trend_short":4,"remote_friendly":4.5,"value_added":7.5,"ai_resistance":5.5,"social_status":7.5},
    # quality_control
    "1001": {"remote_friendly":4.0,"ai_resistance":5.0},
    "1002": {"remote_friendly":3.0,"physical_demand":3.5,"ai_resistance":5.5},
    "1003": {"learning_cost":6.0,"education_req":6.0,"market_size":5.0,"remote_friendly":3.0,"physical_demand":3.0,"ai_resistance":6.5,"license_barrier":4.5},
    "1004": {"remote_friendly":5.0,"ai_resistance":5.0,"market_size":5.5,"social_status":6.0},
    "1005": {"license_barrier":5.5,"physical_demand":4.5,"safety":6.0,"remote_friendly":2.0,"ai_resistance":7.0,"social_status":6.0,"market_size":5.0},
    "1006": {"growth_coeff":6.0,"supply_demand":6.0,"ai_resistance":6.5,"remote_friendly":4.5},
    "1007": {"learning_cost":6.0,"supply_demand":5.5,"social_status":6.5,"value_added":6.5,"remote_friendly":4.5,"ai_resistance":5.0,"career_switch":6.0},
    "1008": {"license_barrier":5.5,"intl_mobility":7.0,"remote_friendly":4.0,"ai_resistance":6.0,"social_status":6.0},
    # telecom_eng
    "1101": {"remote_friendly":4.0,"physical_demand":4.0},
    "1102": {"growth_coeff":7.5,"opportunity":7.5,"supply_demand":7.5,"developed_scarcity":7.5,"trend_long":4,"trend_short":4,"value_added":7.5,"ai_resistance":6.0,"social_status":7.5},
    "1103": {"remote_friendly":3.0,"physical_demand":4.5,"market_size":5.0,"ai_resistance":6.5},
    "1104": {"learning_cost":7.5,"education_req":7.5,"market_size":4.0,"supply_demand":7.0,"ai_resistance":7.0,"social_status":7.5,"trend_short":3},
    "1105": {"learning_cost":7.0,"education_req":7.0,"market_size":4.5,"supply_demand":6.0,"ai_resistance":6.5},
    # biomedical_eng
    "1201": {"opportunity":7.0,"market_size":5.5,"value_added":7.5},
    "1202": {"opportunity":7.0,"supply_demand":7.5,"license_barrier":5.5,"value_added":7.5,"market_size":5.5,"trend_short":3},
    "1203": {"market_size":4.0,"supply_demand":6.0,"ai_resistance":8.0,"physical_demand":3.5,"social_status":7.0},
    "1204": {"learning_cost":8.0,"education_req":8.5,"market_size":3.0,"supply_demand":7.5,"ai_resistance":8.0,"social_status":8.0,"fulfillment":8.5,"edu":"博士","age":"26-33","remote_friendly":5.0},
    "1205": {"market_size":4.0,"supply_demand":6.5,"ai_resistance":7.0,"physical_demand":3.0},
    # environmental_eng
    "1301": {"market_size":6.0,"growth_coeff":6.0,"trend_long":3,"trend_short":2,"license_barrier":4.5},
    "1302": {"market_size":4.5,"supply_demand":5.0,"ai_resistance":7.0,"physical_demand":3.5},
    "1303": {"learning_cost":5.0,"education_req":5.0,"market_size":5.5,"license_barrier":4.5,"remote_friendly":5.0,"ai_resistance":5.5,"social_status":5.5,"trend_long":3,"trend_short":2},
    "1304": {"growth_coeff":7.0,"opportunity":6.5,"supply_demand":6.5,"trend_long":4,"trend_short":3,"license_barrier":5.0,"ai_resistance":6.0,"social_status":6.5,"remote_friendly":4.5},
    "1305": {"remote_friendly":2.5,"physical_demand":4.0,"safety":5.5,"market_size":5.5},
    "1306": {"growth_coeff":6.0,"supply_demand":6.0,"ai_resistance":6.5,"remote_friendly":4.5},
    "1307": {"license_barrier":5.5,"ai_resistance":7.0,"safety":5.5,"social_status":6.5,"remote_friendly":4.0},
    "1308": {"market_size":5.0,"remote_friendly":2.5,"physical_demand":4.0},
    "1309": {"market_size":5.0,"remote_friendly":2.5,"physical_demand":4.5,"safety":5.0,"license_barrier":4.5},
    "1310": {"learning_cost":7.0,"education_req":7.0,"market_size":4.0,"supply_demand":6.0,"ai_resistance":7.0,"social_status":7.0,"growth_coeff":6.0},
    "1311": {"learning_cost":5.5,"education_req":5.0,"remote_friendly":2.0,"physical_demand":5.5,"safety":5.0,"ai_resistance":7.0,"license_barrier":4.5,"social_status":5.5,"edu":"大专/本科","market_size":6.0},
    "1312": {"learning_cost":5.0,"education_req":5.0,"remote_friendly":2.0,"physical_demand":4.5,"safety":4.5,"ai_resistance":6.5,"social_status":5.0,"market_size":5.0},
    "1313": {"learning_cost":7.0,"education_req":7.0,"market_size":3.5,"supply_demand":5.5,"ai_resistance":7.0,"social_status":6.5},
    "1314": {"learning_cost":7.5,"education_req":7.5,"market_size":3.0,"supply_demand":5.5,"safety":3.5,"ai_resistance":8.0,"social_status":7.0,"license_barrier":6.0,"physical_demand":4.5},
}

# === Build occupation base scores ===
def occ_base(occ_id, mid):
    d = dict(MID_DEFAULTS[mid])
    ovr = OVR.get(occ_id, {})
    d.update(ovr)
    return d

# === SCORING (same as gen_tech_data.py adapted for ENG) ===
def clamp(val, lo=0.0, hi=10.0):
    return max(lo, min(hi, round(val, 1)))

def clamp5(val):
    return max(0.0, min(5.0, round(val, 1)))

def apply_country_modifiers(base, cp, occ):
    s = dict(base)
    eng_f = (cp["eng"] - 6.0) / 4.0
    comp_f = (cp["comp"] - 5.0) / 5.0
    mfg_f = (cp["mfg"] - 6.0) / 4.0
    stab_f = (cp["stab"] - 5.5) / 4.5
    wlb_f = (cp["wlb"] - 6.0) / 4.0
    remote_f = (cp.get("wlb", 6.0) - 6.0) / 4.0  # eng jobs generally less remote-sensitive
    gender_f = (cp["gender"] - 5.5) / 4.5
    edu_f = (cp["edu"] - 6.0) / 4.0
    intl_f = (cp["intl"] - 6.0) / 4.0
    reg_f = (cp["reg"] - 5.5) / 4.5
    safety_f = (cp["safety"] - 6.0) / 4.0

    mid = occ["mid"]
    # Sector-specific boosts
    auto_f = (cp["auto"] - 5.0) / 5.0 if mid == "automotive" else 0.0
    semi_f = (cp["semi"] - 5.0) / 5.0 if mid == "semiconductor" else 0.0
    aero_f = (cp["aero"] - 5.0) / 5.0 if mid == "aerospace" else 0.0
    constr_f = (cp["constr"] - 6.0) / 4.0 if mid == "civil_construction" else 0.0
    sector_f = auto_f + semi_f + aero_f + constr_f

    s["value_added"] = clamp(s["value_added"] + comp_f * 2.0 + eng_f * 0.3)
    s["cost_performance"] = clamp(s["cost_performance"] + comp_f * 0.8 + eng_f * 0.5)
    s["growth_coeff"] = clamp(s["growth_coeff"] + eng_f * 0.5 + mfg_f * 0.3 + sector_f * 0.8)
    s["career_lifespan"] = clamp(s["career_lifespan"] + stab_f * 0.8)
    s["opportunity"] = clamp(s["opportunity"] + mfg_f * 0.8 + sector_f * 1.0 + eng_f * 0.3)
    s["market_size"] = clamp(s["market_size"] + mfg_f * 1.2 + sector_f * 0.8)
    s["supply_demand"] = clamp(s["supply_demand"] + eng_f * 0.8 + sector_f * 0.5)
    dev_bonus = 0.8 if cp["eng"] >= 7.5 else (0.0 if cp["eng"] >= 5.0 else -0.8)
    s["developed_scarcity"] = clamp(s["developed_scarcity"] + dev_bonus)
    s["stability"] = clamp(s["stability"] + stab_f * 1.5 + safety_f * 0.3)
    s["safety"] = clamp(s["safety"] + safety_f * 1.0)
    s["occupational_disease"] = clamp(s["occupational_disease"] + wlb_f * 0.5 + safety_f * 0.5)
    s["overtime"] = clamp(s["overtime"] + (cp["ot"] - 5.0) / 5.0 * 2.5)
    s["burnout"] = clamp(s["burnout"] + (cp["ot"] - 5.0) / 5.0 * 1.5)
    s["remote_friendly"] = clamp(s["remote_friendly"] + wlb_f * 0.5)
    s["autonomy"] = clamp(s["autonomy"] + wlb_f * 0.5 + eng_f * 0.2)
    s["family_friendly"] = clamp(s["family_friendly"] + wlb_f * 1.5)
    s["social_status"] = clamp(s["social_status"] + eng_f * 0.6 + comp_f * 0.4)
    s["fulfillment"] = clamp(s["fulfillment"] + eng_f * 0.4)
    s["gender_equality"] = clamp(s["gender_equality"] + gender_f * 2.0)
    s["age_flexibility"] = clamp(s["age_flexibility"] + wlb_f * 0.4 + eng_f * 0.2)
    s["entrepreneurship"] = clamp(s["entrepreneurship"] + mfg_f * 0.4 + reg_f * 0.3)
    s["intl_mobility"] = clamp(s["intl_mobility"] + intl_f * 1.5)
    s["ai_resistance"] = clamp(s["ai_resistance"] + eng_f * 0.2)
    s["learning_cost"] = clamp(s["learning_cost"] + edu_f * 0.3)
    s["education_req"] = clamp(s["education_req"] + edu_f * 0.3)
    s["license_barrier"] = clamp(s["license_barrier"] + reg_f * 0.5 + safety_f * 0.3)
    s["cycle_sensitivity"] = clamp(s["cycle_sensitivity"] - stab_f * 0.5)
    s["side_job_compat"] = clamp(s["side_job_compat"] + wlb_f * 0.3)
    s["industry_monopoly"] = clamp(s["industry_monopoly"] - mfg_f * 0.3 + (1 - cp["reg"] / 10.0) * 0.3)
    s["skill_versatility"] = clamp(s["skill_versatility"] + eng_f * 0.4)
    s["career_switch"] = clamp(s["career_switch"] + mfg_f * 0.3 + eng_f * 0.2)
    rep_adj = -0.3 if cp["eng"] >= 7.5 else (0.3 if cp["eng"] < 5.0 else 0.0)
    s["reputation_variance"] = clamp5(s["reputation_variance"] + rep_adj)
    return s

def get_trends(base, cp):
    t_long = base["trend_long"]
    t_short = base["trend_short"]
    mid_key = None
    # sector boosts
    if cp.get("mfg", 6) >= 8.0:
        t_short = min(5, t_short + 1)
    elif cp.get("mfg", 6) < 4.0:
        t_short = max(-5, t_short - 1)
    if cp["eng"] >= 8.0:
        t_long = min(5, t_long)
    elif cp["eng"] < 5.0:
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
    if scores["safety"] <= 5.5: hz.append("工作安全风险较高"); he.append("higher workplace safety risks")
    if scores["overtime"] <= 3.5: hz.append("加班文化严重"); he.append("heavy overtime culture")
    elif scores["overtime"] >= 7.5: hz.append("工作时间规律"); he.append("regular working hours")
    if scores["stability"] >= 7.5: hz.append("就业稳定"); he.append("stable employment")
    elif scores["stability"] <= 4.0: hz.append("就业波动大"); he.append("volatile employment")
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
    out = PROJECT_ROOT / "data" / "csv" / "engineering_manufacturing.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for occ in OCCUPATIONS:
        base = occ_base(occ["id"], occ["mid"])
        for country in COUNTRIES:
            iso = country["iso"]
            cp = CP[iso]
            scores = apply_country_modifiers(base, cp, occ)
            rng = random.Random(hash(f"ENG-{occ['id']}-{iso}") % 10000)
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
            row_id = f"ENG-{occ['id']}-{iso}-general"
            row = {
                "id": row_id,
                "major_category": "工程与制造",
                "major_code": "ENG",
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
                "typical_education": base.get("edu", "本科"),
                "typical_entry_age": base.get("age", "22-28"),
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
    with open(out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated {len(rows)} rows to {out}")
    print(f"Occupations: {len(OCCUPATIONS)}, Countries: {len(COUNTRIES)}")

if __name__ == "__main__":
    main()
