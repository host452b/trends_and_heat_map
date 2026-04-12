#!/usr/bin/env python3
"""Generate agriculture_resources.csv — AGR data for Global Career Development Index."""
import csv, sys, random, json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from tools.score_calculator import load_weights, calculate_composite

# === OCCUPATIONS (86) from categories.yaml AGR ===
O = []
def _a(mid, mid_zh, mid_en, items):
    for id_, zh, en, isco, onet, loc in items:
        O.append({"id": id_, "mid": mid, "mid_zh": mid_zh, "mid_en": mid_en,
                   "zh": zh, "en": en, "isco": isco, "onet": onet, "locality": loc})

_a("crop_farming", "种植", "Crop Farming", [
    ("0101","粮食作物种植者","Grain Farmer","6111","45-2091.00","global"),
    ("0102","果蔬种植者","Fruit & Vegetable Grower","6112","45-2092.02","global"),
    ("0103","茶叶种植与加工师","Tea Farmer / Tea Processing Specialist","6112","45-2092.02","regional"),
    ("0104","花卉种植师","Floriculturist / Flower Grower","6113","45-2092.01","global"),
    ("0105","有机农业技术员","Organic Farming Technician","6111","45-2091.00","global"),
    ("0106","精准农业技术员","Precision Agriculture Technician","6111","45-2091.00","global"),
    ("0107","农学家/农艺师","Agronomist","2132","19-1011.00","global"),
    ("0108","葡萄酒酿造师","Winemaker / Viticulturist","7514","45-2092.02","global"),
    ("0109","种子研究员","Seed Researcher / Plant Breeder","2132","19-1013.00","global"),
    ("0110","灌溉专员","Irrigation Specialist","6111","45-2091.00","global"),
    ("0111","烟草种植者","Tobacco Farmer","6111","45-2091.00","regional"),
    ("0112","咖啡种植者","Coffee Farmer","6112","45-2092.02","regional"),
    ("0113","蘑菇种植者","Mushroom Farmer","6112","45-2092.02","global"),
    ("0114","农业无人机操作员","Agricultural Drone Operator","6111","45-2091.00","global"),
])
_a("livestock", "畜牧", "Livestock", [
    ("0201","畜牧养殖者","Livestock Farmer / Rancher","6121","45-2093.00","global"),
    ("0202","兽医","Veterinarian","2250","29-1131.00","global"),
    ("0203","乳业技术员","Dairy Technician","6121","45-2093.00","global"),
    ("0204","家禽养殖者","Poultry Farmer","6122","45-2093.00","global"),
    ("0205","畜牧育种师","Animal Breeder","6121","45-2021.00","global"),
    ("0206","兽医助理/兽医技师","Veterinary Technician","3240","29-2056.00","global"),
    ("0207","动物营养师","Animal Nutritionist","2132","19-1011.00","global"),
    ("0208","养蜂人","Beekeeper / Apiarist","6123","45-2093.00","global"),
    ("0209","牧场经理","Ranch Manager","6121","11-9013.00","global"),
    ("0210","蚕丝养殖者","Sericulturist / Silkworm Farmer","6123","45-2093.00","regional"),
])
_a("fishery", "渔业", "Fishery", [
    ("0301","远洋渔民","Deep-sea Fisherman","6222","45-3011.00","global"),
    ("0302","淡水渔业养殖者","Freshwater Fish Farmer","6221","45-3031.00","global"),
    ("0303","水产养殖技术员","Aquaculture Technician","6221","45-3031.00","global"),
    ("0304","水产品加工技师","Seafood Processing Technician","8160","51-3022.00","global"),
    ("0305","海洋生物学家","Marine Biologist","2131","19-1023.00","global"),
    ("0306","珍珠养殖者","Pearl Farmer / Oyster Culturist","6221","45-3031.00","regional"),
    ("0307","渔业检查员","Fisheries Inspector","3257","45-3011.00","global"),
])
_a("mining", "采矿", "Mining", [
    ("0401","露天矿工","Open-pit Miner","8111","47-5041.00","global"),
    ("0402","井下矿工","Underground Miner","8111","47-5041.00","global"),
    ("0403","矿业工程师","Mining Engineer","2146","17-2151.00","global"),
    ("0404","地质学家/探矿师","Geologist / Exploration Geologist","2114","19-2042.00","global"),
    ("0405","爆破技师","Blaster / Explosives Technician","8111","47-5031.00","global"),
    ("0406","矿山安全工程师","Mine Safety Engineer","2149","17-2111.02","global"),
    ("0407","FIFO矿工(飞进飞出矿工)","FIFO Miner (Fly-In Fly-Out)","8111","47-5041.00","regional"),
    ("0408","手工采矿工人","Artisanal / Small-scale Miner","8111","47-5041.00","regional"),
])
_a("oil_gas", "石油天然气", "Oil & Gas", [
    ("0501","石油工程师","Petroleum Engineer","2145","17-2171.00","global"),
    ("0502","钻井工程师","Drilling Engineer","2145","17-2171.00","global"),
    ("0503","管道工程师(油气)","Pipeline Engineer","2145","17-2171.00","global"),
    ("0504","炼化工程师","Refinery Process Engineer","2145","17-2041.00","global"),
    ("0505","油田技术员","Oilfield Technician","3117","47-5013.00","global"),
    ("0506","油气勘探地球物理师","Geophysicist (Oil & Gas Exploration)","2114","19-2042.00","global"),
    ("0507","天然气处理技师","Natural Gas Processing Technician","3117","51-8093.00","global"),
    ("0508","LNG工程师","LNG (Liquefied Natural Gas) Engineer","2145","17-2171.00","global"),
    ("0509","海上石油平台工人","Offshore Oil Platform Worker","8113","47-5013.00","global"),
])
_a("renewable_energy", "新能源", "Renewable Energy", [
    ("0601","太阳能工程师","Solar Energy Engineer","2151","17-2199.11","global"),
    ("0602","风电工程师","Wind Energy Engineer","2151","17-2199.11","global"),
    ("0603","储能系统工程师","Energy Storage Engineer","2151","17-2199.11","global"),
    ("0604","氢能工程师","Hydrogen Energy Engineer","2151","17-2199.11","global"),
    ("0605","风电场运维技术员","Wind Turbine Technician","7412","49-9081.00","global"),
    ("0606","碳交易分析师","Carbon Trading Analyst","2413","13-2051.00","global"),
    ("0607","新能源项目开发经理","Renewable Energy Project Developer","1349","11-9199.00","global"),
    ("0608","生物质能工程师","Biomass Energy Engineer","2151","17-2199.11","global"),
    ("0609","地热工程师","Geothermal Engineer","2151","17-2199.11","global"),
])
_a("environmental", "环保", "Environmental Protection", [
    ("0701","环境工程师","Environmental Engineer","2143","17-2081.00","global"),
    ("0702","污水处理工程师","Wastewater Treatment Engineer","2143","17-2081.00","global"),
    ("0703","废物管理专员","Waste Management Specialist","2143","17-2081.00","global"),
    ("0704","环境影响评价师","Environmental Impact Assessor","2143","19-2041.00","global"),
    ("0705","环境科学家","Environmental Scientist","2133","19-2041.00","global"),
    ("0706","空气质量分析师","Air Quality Analyst","2133","19-2041.01","global"),
    ("0707","生态修复专家","Ecological Restoration Specialist","2133","19-1029.00","global"),
    ("0708","水资源管理师","Water Resources Manager","2143","17-2081.00","global"),
    ("0709","环保合规顾问","Environmental Compliance Consultant","2143","13-1041.01","global"),
    ("0710","土壤修复工程师","Soil Remediation Engineer","2143","17-2081.00","global"),
    ("0711","野生动物保护专家","Wildlife Conservation Specialist","2133","19-1023.00","global"),
])
_a("forestry", "林业", "Forestry", [
    ("0801","护林员","Forest Ranger / Park Ranger","6210","19-1031.03","global"),
    ("0802","木材加工师","Timber Processing Specialist / Sawyer","7521","45-4023.00","global"),
    ("0803","森林消防员","Wildland Firefighter","5411","33-2011.00","global"),
    ("0804","林业工程师","Forestry Engineer / Silviculturist","2132","19-1032.00","global"),
    ("0805","伐木工","Logger / Lumberjack","6210","45-4022.00","global"),
    ("0806","树艺师","Arborist / Tree Surgeon","6113","37-3013.00","global"),
])
_a("agricultural_tech", "农业科技", "Agricultural Technology", [
    ("0901","农业物联网工程师","Agricultural IoT Engineer","2514","15-1252.00","global"),
    ("0902","垂直农场运营经理","Vertical Farm Operations Manager","6111","45-2091.00","global"),
    ("0903","农业生物技术研究员","Agricultural Biotechnology Researcher","2131","19-1013.00","global"),
    ("0904","食品科学家","Food Scientist","2145","19-1012.00","global"),
    ("0905","农业经济学家","Agricultural Economist","2631","19-3011.00","global"),
    ("0906","植物保护员/植检员","Plant Protection / Phytosanitary Inspector","3132","45-2011.00","global"),
    ("0907","昆虫学家","Entomologist","2131","19-1023.00","global"),
    ("0908","土壤科学家","Soil Scientist","2114","19-1013.00","global"),
    ("0909","农产品质量检测员","Agricultural Product Quality Inspector","3257","45-2011.00","global"),
    ("0910","农业气象学家","Agricultural Meteorologist","2112","19-2021.00","global"),
    ("0911","智能温室管理员","Smart Greenhouse Manager","6111","45-2091.00","global"),
    ("0912","农业保险评估师","Agricultural Insurance Assessor","3315","13-1031.02","global"),
])

OCCUPATIONS = O

# === COUNTRIES (45) ===
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

# === COUNTRY PROFILES for AGR ===
# Keys: agri(agriculture gdp share/strength), mine(mining sector), oil(oil&gas sector),
#   renew(renewable investment), env_reg(environmental regulation), mech(farm mechanization),
#   res(resource richness), fish(fishery sector),
#   comp(compensation), wlb(work-life balance), stab(stability),
#   edu(edu quality), intl(international openness), gender(gender equality),
#   reg(regulatory), ot(overtime culture, higher=less OT), safe(safety standards)
CP = {
    # DEVELOPED - HIGH MECHANIZATION
    "US": {"agri":7.0,"mine":6.0,"oil":8.5,"renew":7.0,"env_reg":7.0,"mech":9.5,"res":7.5,"fish":5.5,"comp":8.5,"wlb":6.0,"stab":6.0,"edu":9.0,"intl":8.5,"gender":7.5,"reg":7.0,"ot":5.0,"safe":7.5},
    "CA": {"agri":7.5,"mine":8.5,"oil":8.0,"renew":7.5,"env_reg":7.5,"mech":9.0,"res":8.5,"fish":6.5,"comp":7.5,"wlb":7.5,"stab":7.0,"edu":8.0,"intl":9.0,"gender":8.0,"reg":7.0,"ot":6.5,"safe":8.0},
    "AU": {"agri":6.5,"mine":9.5,"oil":6.5,"renew":7.0,"env_reg":7.5,"mech":9.0,"res":9.5,"fish":6.0,"comp":8.0,"wlb":8.0,"stab":7.5,"edu":8.0,"intl":8.5,"gender":8.0,"reg":7.5,"ot":7.0,"safe":8.5},
    "NZ": {"agri":8.5,"mine":4.0,"oil":3.5,"renew":8.0,"env_reg":8.5,"mech":8.5,"res":4.5,"fish":7.0,"comp":6.5,"wlb":8.5,"stab":7.5,"edu":7.5,"intl":8.0,"gender":8.5,"reg":7.5,"ot":7.5,"safe":8.5},
    "GB": {"agri":5.0,"mine":3.5,"oil":5.5,"renew":8.0,"env_reg":8.0,"mech":8.5,"res":3.5,"fish":5.0,"comp":7.5,"wlb":7.0,"stab":7.0,"edu":8.5,"intl":9.0,"gender":7.5,"reg":7.5,"ot":6.5,"safe":8.0},
    "FR": {"agri":7.5,"mine":3.0,"oil":3.5,"renew":7.0,"env_reg":8.0,"mech":8.5,"res":3.5,"fish":5.5,"comp":7.0,"wlb":8.0,"stab":7.0,"edu":8.0,"intl":7.5,"gender":7.0,"reg":7.5,"ot":7.0,"safe":8.0},
    "DE": {"agri":5.5,"mine":4.5,"oil":3.0,"renew":9.0,"env_reg":9.0,"mech":9.0,"res":4.0,"fish":4.0,"comp":8.0,"wlb":8.0,"stab":8.0,"edu":8.5,"intl":8.0,"gender":7.0,"reg":8.0,"ot":7.5,"safe":8.5},
    "NL": {"agri":8.0,"mine":3.0,"oil":3.5,"renew":8.5,"env_reg":9.0,"mech":9.5,"res":3.0,"fish":6.5,"comp":7.5,"wlb":9.0,"stab":7.5,"edu":8.0,"intl":9.0,"gender":8.5,"reg":7.5,"ot":8.0,"safe":9.0},
    "CH": {"agri":4.5,"mine":2.5,"oil":2.0,"renew":7.0,"env_reg":9.0,"mech":8.5,"res":2.5,"fish":2.5,"comp":9.5,"wlb":8.5,"stab":9.0,"edu":9.0,"intl":8.5,"gender":7.0,"reg":8.0,"ot":7.5,"safe":9.0},
    "SE": {"agri":4.5,"mine":6.0,"oil":2.5,"renew":9.0,"env_reg":9.5,"mech":8.5,"res":6.0,"fish":5.0,"comp":7.0,"wlb":9.0,"stab":8.0,"edu":8.5,"intl":8.5,"gender":9.0,"reg":7.5,"ot":8.5,"safe":9.0},
    "DK": {"agri":7.0,"mine":2.5,"oil":4.0,"renew":9.5,"env_reg":9.5,"mech":9.0,"res":3.0,"fish":7.0,"comp":7.0,"wlb":9.0,"stab":8.0,"edu":8.5,"intl":8.5,"gender":9.0,"reg":7.5,"ot":8.5,"safe":9.0},
    "FI": {"agri":4.5,"mine":5.0,"oil":2.0,"renew":8.0,"env_reg":9.0,"mech":8.5,"res":5.5,"fish":5.0,"comp":6.5,"wlb":9.0,"stab":7.5,"edu":9.0,"intl":8.0,"gender":9.0,"reg":7.5,"ot":8.5,"safe":9.0},
    "IT": {"agri":7.0,"mine":3.5,"oil":3.5,"renew":6.5,"env_reg":7.0,"mech":7.5,"res":3.5,"fish":6.0,"comp":5.5,"wlb":6.5,"stab":5.5,"edu":7.0,"intl":6.5,"gender":5.5,"reg":6.5,"ot":5.5,"safe":7.0},
    "ES": {"agri":7.5,"mine":3.5,"oil":3.0,"renew":7.5,"env_reg":7.0,"mech":7.5,"res":3.5,"fish":6.5,"comp":5.0,"wlb":7.0,"stab":5.0,"edu":7.0,"intl":7.0,"gender":6.5,"reg":6.5,"ot":5.5,"safe":7.0},
    "PT": {"agri":6.5,"mine":3.5,"oil":2.5,"renew":7.0,"env_reg":7.0,"mech":7.0,"res":3.5,"fish":7.0,"comp":4.5,"wlb":7.0,"stab":5.5,"edu":6.5,"intl":7.5,"gender":7.0,"reg":6.0,"ot":6.0,"safe":7.0},
    "IL": {"agri":6.0,"mine":3.0,"oil":3.0,"renew":7.5,"env_reg":7.5,"mech":9.0,"res":3.0,"fish":3.5,"comp":7.5,"wlb":6.0,"stab":5.5,"edu":8.5,"intl":8.0,"gender":7.0,"reg":6.5,"ot":5.0,"safe":7.5},
    "SG": {"agri":2.0,"mine":1.5,"oil":5.5,"renew":6.0,"env_reg":8.5,"mech":8.0,"res":1.5,"fish":4.0,"comp":8.0,"wlb":5.5,"stab":8.0,"edu":8.5,"intl":9.5,"gender":7.0,"reg":8.5,"ot":4.5,"safe":9.0},
    "JP": {"agri":5.0,"mine":3.0,"oil":3.0,"renew":7.0,"env_reg":8.0,"mech":9.0,"res":3.0,"fish":8.5,"comp":7.0,"wlb":4.5,"stab":7.5,"edu":8.0,"intl":5.0,"gender":5.0,"reg":7.5,"ot":3.5,"safe":8.5},
    "KR": {"agri":4.5,"mine":3.0,"oil":3.0,"renew":6.5,"env_reg":7.0,"mech":8.5,"res":3.0,"fish":7.0,"comp":6.5,"wlb":4.0,"stab":6.5,"edu":8.0,"intl":6.0,"gender":4.5,"reg":7.0,"ot":3.0,"safe":7.5},
    "TW": {"agri":4.5,"mine":2.5,"oil":2.5,"renew":6.5,"env_reg":7.0,"mech":8.0,"res":2.5,"fish":6.5,"comp":5.5,"wlb":5.0,"stab":6.0,"edu":7.5,"intl":6.5,"gender":6.0,"reg":6.5,"ot":4.0,"safe":7.5},
    "HK": {"agri":1.5,"mine":1.5,"oil":2.0,"renew":4.0,"env_reg":7.0,"mech":5.0,"res":1.5,"fish":4.5,"comp":7.0,"wlb":4.5,"stab":6.5,"edu":7.5,"intl":9.0,"gender":6.5,"reg":7.0,"ot":3.5,"safe":8.0},
    "CZ": {"agri":5.0,"mine":4.5,"oil":2.5,"renew":6.0,"env_reg":7.0,"mech":7.5,"res":4.5,"fish":3.0,"comp":5.5,"wlb":7.5,"stab":7.0,"edu":7.0,"intl":7.5,"gender":6.5,"reg":7.0,"ot":6.5,"safe":7.5},
    "PL": {"agri":6.5,"mine":6.5,"oil":2.5,"renew":5.5,"env_reg":6.0,"mech":7.0,"res":5.5,"fish":4.0,"comp":5.5,"wlb":7.0,"stab":6.5,"edu":7.0,"intl":7.5,"gender":6.5,"reg":6.5,"ot":6.0,"safe":7.0},
    # LARGE EMERGING ECONOMIES
    "CN": {"agri":7.5,"mine":7.5,"oil":6.5,"renew":9.0,"env_reg":6.0,"mech":7.5,"res":7.0,"fish":9.0,"comp":5.5,"wlb":3.5,"stab":5.5,"edu":7.5,"intl":5.0,"gender":5.5,"reg":6.0,"ot":2.5,"safe":5.5},
    "IN": {"agri":9.0,"mine":7.0,"oil":5.0,"renew":7.5,"env_reg":4.5,"mech":4.0,"res":6.5,"fish":7.5,"comp":3.5,"wlb":4.5,"stab":5.0,"edu":7.0,"intl":7.0,"gender":4.0,"reg":5.0,"ot":4.0,"safe":4.0},
    "BR": {"agri":9.0,"mine":8.0,"oil":7.5,"renew":7.0,"env_reg":5.5,"mech":7.0,"res":9.0,"fish":6.0,"comp":4.0,"wlb":6.0,"stab":4.5,"edu":6.0,"intl":5.0,"gender":5.5,"reg":5.5,"ot":5.0,"safe":5.0},
    "RU": {"agri":6.5,"mine":8.0,"oil":9.5,"renew":3.5,"env_reg":4.0,"mech":6.5,"res":9.5,"fish":7.0,"comp":4.5,"wlb":5.5,"stab":4.0,"edu":7.5,"intl":3.5,"gender":6.0,"reg":4.5,"ot":5.5,"safe":4.5},
    "MX": {"agri":7.0,"mine":6.5,"oil":7.0,"renew":5.5,"env_reg":4.5,"mech":5.5,"res":6.5,"fish":5.5,"comp":4.0,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.5,"gender":5.0,"reg":5.0,"ot":4.5,"safe":4.5},
    "AR": {"agri":9.0,"mine":5.5,"oil":6.0,"renew":5.0,"env_reg":4.5,"mech":7.0,"res":6.5,"fish":5.5,"comp":3.5,"wlb":5.5,"stab":3.5,"edu":6.5,"intl":5.5,"gender":5.5,"reg":4.5,"ot":5.0,"safe":5.0},
    "CL": {"agri":7.0,"mine":9.0,"oil":3.5,"renew":7.0,"env_reg":6.0,"mech":7.0,"res":8.5,"fish":8.0,"comp":4.5,"wlb":6.0,"stab":5.5,"edu":6.0,"intl":6.0,"gender":5.5,"reg":5.5,"ot":5.5,"safe":6.0},
    "CO": {"agri":7.5,"mine":6.0,"oil":7.0,"renew":5.0,"env_reg":4.5,"mech":5.0,"res":6.5,"fish":5.0,"comp":3.5,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.0,"gender":5.0,"reg":5.0,"ot":5.0,"safe":4.5},
    "TR": {"agri":7.5,"mine":5.5,"oil":4.5,"renew":6.0,"env_reg":5.0,"mech":6.0,"res":5.5,"fish":5.5,"comp":4.0,"wlb":5.0,"stab":4.0,"edu":6.5,"intl":5.5,"gender":4.5,"reg":5.0,"ot":4.5,"safe":5.0},
    # SOUTHEAST ASIA — high agriculture
    "TH": {"agri":8.0,"mine":4.0,"oil":3.5,"renew":5.0,"env_reg":4.0,"mech":5.5,"res":4.5,"fish":8.0,"comp":3.5,"wlb":5.5,"stab":5.5,"edu":5.5,"intl":5.5,"gender":6.0,"reg":5.0,"ot":5.5,"safe":5.0},
    "VN": {"agri":8.5,"mine":5.0,"oil":5.5,"renew":5.5,"env_reg":4.0,"mech":4.5,"res":5.5,"fish":8.5,"comp":3.0,"wlb":5.0,"stab":5.0,"edu":5.5,"intl":5.5,"gender":5.5,"reg":5.0,"ot":4.5,"safe":4.5},
    "ID": {"agri":8.5,"mine":7.0,"oil":6.0,"renew":5.0,"env_reg":4.0,"mech":4.0,"res":7.5,"fish":9.0,"comp":3.0,"wlb":5.5,"stab":5.0,"edu":5.0,"intl":4.5,"gender":5.0,"reg":5.0,"ot":5.0,"safe":4.0},
    "MY": {"agri":7.5,"mine":4.5,"oil":6.0,"renew":5.5,"env_reg":5.0,"mech":6.0,"res":5.5,"fish":6.5,"comp":4.5,"wlb":5.5,"stab":6.0,"edu":6.0,"intl":6.5,"gender":5.5,"reg":5.5,"ot":5.0,"safe":5.5},
    "PH": {"agri":8.0,"mine":5.0,"oil":3.5,"renew":4.5,"env_reg":4.0,"mech":3.5,"res":5.0,"fish":8.0,"comp":3.0,"wlb":5.0,"stab":4.5,"edu":5.5,"intl":6.5,"gender":6.5,"reg":4.5,"ot":4.5,"safe":4.0},
    # SOUTH ASIA — very high agriculture
    "PK": {"agri":8.5,"mine":4.5,"oil":4.0,"renew":4.0,"env_reg":3.0,"mech":3.5,"res":4.5,"fish":5.0,"comp":2.5,"wlb":4.5,"stab":3.5,"edu":4.5,"intl":4.5,"gender":3.0,"reg":4.0,"ot":4.5,"safe":3.0},
    "BD": {"agri":9.0,"mine":3.0,"oil":3.5,"renew":3.5,"env_reg":3.0,"mech":3.0,"res":3.0,"fish":8.0,"comp":2.0,"wlb":4.5,"stab":3.5,"edu":4.0,"intl":4.5,"gender":3.5,"reg":3.5,"ot":4.5,"safe":3.0},
    # MIDDLE EAST — oil/gas dominance
    "AE": {"agri":2.5,"mine":3.0,"oil":9.0,"renew":7.5,"env_reg":6.5,"mech":8.0,"res":5.0,"fish":4.0,"comp":8.0,"wlb":5.5,"stab":7.0,"edu":7.0,"intl":8.5,"gender":5.0,"reg":6.5,"ot":5.0,"safe":7.5},
    "SA": {"agri":3.5,"mine":4.0,"oil":9.5,"renew":7.0,"env_reg":5.0,"mech":7.0,"res":5.5,"fish":3.5,"comp":7.0,"wlb":5.5,"stab":6.0,"edu":6.0,"intl":5.5,"gender":3.5,"reg":5.5,"ot":5.0,"safe":6.0},
    # AFRICA
    "ZA": {"agri":6.0,"mine":9.0,"oil":4.0,"renew":5.5,"env_reg":5.5,"mech":5.5,"res":8.5,"fish":5.0,"comp":4.0,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.5,"gender":5.5,"reg":5.0,"ot":5.5,"safe":5.0},
    "NG": {"agri":8.0,"mine":5.0,"oil":8.5,"renew":3.0,"env_reg":3.0,"mech":2.5,"res":6.0,"fish":5.5,"comp":2.5,"wlb":4.5,"stab":3.5,"edu":4.0,"intl":5.0,"gender":4.0,"reg":3.5,"ot":4.5,"safe":3.0},
    "KE": {"agri":8.5,"mine":4.0,"oil":3.0,"renew":5.0,"env_reg":4.5,"mech":3.0,"res":4.0,"fish":4.5,"comp":2.5,"wlb":5.0,"stab":4.0,"edu":4.5,"intl":5.5,"gender":4.5,"reg":4.0,"ot":5.0,"safe":3.5},
    "EG": {"agri":7.5,"mine":4.5,"oil":6.5,"renew":5.0,"env_reg":4.0,"mech":5.0,"res":5.0,"fish":5.5,"comp":2.5,"wlb":5.0,"stab":4.0,"edu":5.0,"intl":5.0,"gender":3.5,"reg":4.5,"ot":4.5,"safe":4.0},
}

# === MID-CATEGORY DEFAULTS ===
MID_DEFAULTS = {
    "crop_farming": {
        "learning_cost":3.0,"education_req":2.0,"growth_coeff":3.5,"career_lifespan":7.5,
        "opportunity":5.5,"market_size":8.5,"supply_demand":4.0,"developed_scarcity":4.5,
        "value_added":3.0,"cost_performance":4.5,"stability":5.0,"safety":5.5,
        "occupational_disease":4.5,"overtime":4.0,"burnout":5.0,
        "skill_versatility":3.5,"career_switch":3.0,"reputation_variance":2.0,
        "ai_resistance":3.5,"social_status":3.5,"remote_friendly":0.5,"autonomy":7.0,
        "family_friendly":5.0,"fulfillment":5.5,"entrepreneurship":6.5,"gender_equality":4.5,
        "age_flexibility":7.0,"social_interaction":4.0,"physical_demand":8.0,"license_barrier":1.0,
        "cycle_sensitivity":8.0,"side_job_compat":3.0,"intl_mobility":2.5,"industry_monopoly":3.0,
        "trend_long":0,"trend_short":-1,"edu":"无要求/中学","age":"16-35",
    },
    "livestock": {
        "learning_cost":3.5,"education_req":2.5,"growth_coeff":3.5,"career_lifespan":7.5,
        "opportunity":5.0,"market_size":7.5,"supply_demand":4.5,"developed_scarcity":5.0,
        "value_added":3.5,"cost_performance":4.5,"stability":5.5,"safety":5.0,
        "occupational_disease":4.5,"overtime":3.5,"burnout":4.5,
        "skill_versatility":3.5,"career_switch":3.0,"reputation_variance":1.5,
        "ai_resistance":5.0,"social_status":3.5,"remote_friendly":0.5,"autonomy":7.0,
        "family_friendly":4.5,"fulfillment":5.5,"entrepreneurship":6.0,"gender_equality":4.0,
        "age_flexibility":6.5,"social_interaction":4.0,"physical_demand":7.5,"license_barrier":1.5,
        "cycle_sensitivity":7.0,"side_job_compat":3.0,"intl_mobility":2.5,"industry_monopoly":3.5,
        "trend_long":0,"trend_short":0,"edu":"无要求/中学","age":"16-35",
    },
    "fishery": {
        "learning_cost":3.0,"education_req":2.0,"growth_coeff":3.0,"career_lifespan":6.5,
        "opportunity":4.5,"market_size":6.0,"supply_demand":4.5,"developed_scarcity":5.0,
        "value_added":3.5,"cost_performance":4.5,"stability":4.5,"safety":3.5,
        "occupational_disease":4.0,"overtime":3.5,"burnout":4.5,
        "skill_versatility":3.0,"career_switch":2.5,"reputation_variance":1.5,
        "ai_resistance":6.0,"social_status":3.5,"remote_friendly":0.5,"autonomy":6.5,
        "family_friendly":3.0,"fulfillment":5.5,"entrepreneurship":5.5,"gender_equality":3.0,
        "age_flexibility":5.5,"social_interaction":5.0,"physical_demand":8.5,"license_barrier":3.0,
        "cycle_sensitivity":7.5,"side_job_compat":3.5,"intl_mobility":3.5,"industry_monopoly":3.5,
        "trend_long":0,"trend_short":-1,"edu":"无要求","age":"16-30",
    },
    "mining": {
        "learning_cost":3.5,"education_req":2.5,"growth_coeff":3.0,"career_lifespan":5.5,
        "opportunity":5.0,"market_size":5.5,"supply_demand":5.5,"developed_scarcity":6.0,
        "value_added":5.0,"cost_performance":5.5,"stability":5.0,"safety":2.5,
        "occupational_disease":2.5,"overtime":3.5,"burnout":4.0,
        "skill_versatility":3.0,"career_switch":2.5,"reputation_variance":2.0,
        "ai_resistance":5.5,"social_status":3.5,"remote_friendly":0.5,"autonomy":3.5,
        "family_friendly":3.0,"fulfillment":4.0,"entrepreneurship":3.5,"gender_equality":2.5,
        "age_flexibility":4.5,"social_interaction":5.0,"physical_demand":9.0,"license_barrier":3.5,
        "cycle_sensitivity":8.0,"side_job_compat":1.5,"intl_mobility":4.0,"industry_monopoly":5.5,
        "trend_long":0,"trend_short":0,"edu":"技校/中学","age":"18-30",
    },
    "oil_gas": {
        "learning_cost":6.0,"education_req":5.5,"growth_coeff":3.5,"career_lifespan":6.5,
        "opportunity":5.5,"market_size":5.0,"supply_demand":6.0,"developed_scarcity":6.5,
        "value_added":7.0,"cost_performance":6.5,"stability":5.5,"safety":3.0,
        "occupational_disease":3.5,"overtime":3.5,"burnout":4.5,
        "skill_versatility":4.5,"career_switch":4.0,"reputation_variance":2.0,
        "ai_resistance":5.5,"social_status":6.0,"remote_friendly":1.0,"autonomy":4.5,
        "family_friendly":3.0,"fulfillment":5.0,"entrepreneurship":4.0,"gender_equality":3.0,
        "age_flexibility":5.0,"social_interaction":5.5,"physical_demand":7.0,"license_barrier":5.0,
        "cycle_sensitivity":8.5,"side_job_compat":1.5,"intl_mobility":6.5,"industry_monopoly":7.0,
        "trend_long":-1,"trend_short":-1,"edu":"本科/大专","age":"22-30",
    },
    "renewable_energy": {
        "learning_cost":6.5,"education_req":6.0,"growth_coeff":8.0,"career_lifespan":7.5,
        "opportunity":7.5,"market_size":6.0,"supply_demand":7.5,"developed_scarcity":7.0,
        "value_added":7.0,"cost_performance":7.0,"stability":6.0,"safety":6.5,
        "occupational_disease":6.5,"overtime":5.5,"burnout":5.5,
        "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":1.5,
        "ai_resistance":6.0,"social_status":7.0,"remote_friendly":3.0,"autonomy":6.0,
        "family_friendly":5.5,"fulfillment":7.5,"entrepreneurship":6.5,"gender_equality":5.5,
        "age_flexibility":5.5,"social_interaction":5.5,"physical_demand":4.5,"license_barrier":4.5,
        "cycle_sensitivity":5.5,"side_job_compat":3.5,"intl_mobility":7.0,"industry_monopoly":4.5,
        "trend_long":4,"trend_short":4,"edu":"本科/硕士","age":"24-32",
    },
    "environmental": {
        "learning_cost":6.0,"education_req":6.0,"growth_coeff":6.5,"career_lifespan":7.5,
        "opportunity":6.5,"market_size":5.5,"supply_demand":6.0,"developed_scarcity":6.0,
        "value_added":6.0,"cost_performance":6.0,"stability":6.0,"safety":7.0,
        "occupational_disease":6.0,"overtime":6.0,"burnout":5.5,
        "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":1.5,
        "ai_resistance":6.5,"social_status":6.0,"remote_friendly":4.0,"autonomy":6.0,
        "family_friendly":6.0,"fulfillment":7.5,"entrepreneurship":5.0,"gender_equality":6.0,
        "age_flexibility":6.0,"social_interaction":6.0,"physical_demand":4.0,"license_barrier":5.0,
        "cycle_sensitivity":4.5,"side_job_compat":3.5,"intl_mobility":6.0,"industry_monopoly":4.0,
        "trend_long":3,"trend_short":3,"edu":"本科/硕士","age":"24-32",
    },
    "forestry": {
        "learning_cost":3.5,"education_req":2.5,"growth_coeff":3.0,"career_lifespan":7.0,
        "opportunity":4.0,"market_size":4.5,"supply_demand":4.5,"developed_scarcity":5.0,
        "value_added":3.5,"cost_performance":4.5,"stability":5.5,"safety":4.0,
        "occupational_disease":4.0,"overtime":5.0,"burnout":5.0,
        "skill_versatility":3.5,"career_switch":3.0,"reputation_variance":1.5,
        "ai_resistance":7.0,"social_status":4.0,"remote_friendly":0.5,"autonomy":6.5,
        "family_friendly":4.5,"fulfillment":6.5,"entrepreneurship":4.0,"gender_equality":3.5,
        "age_flexibility":5.5,"social_interaction":4.0,"physical_demand":8.0,"license_barrier":2.5,
        "cycle_sensitivity":5.5,"side_job_compat":2.5,"intl_mobility":3.0,"industry_monopoly":4.5,
        "trend_long":1,"trend_short":0,"edu":"技校/中学","age":"18-30",
    },
    "agricultural_tech": {
        "learning_cost":6.5,"education_req":6.5,"growth_coeff":7.0,"career_lifespan":7.5,
        "opportunity":6.5,"market_size":5.0,"supply_demand":6.5,"developed_scarcity":6.5,
        "value_added":6.5,"cost_performance":6.5,"stability":6.0,"safety":7.5,
        "occupational_disease":6.5,"overtime":5.5,"burnout":5.5,
        "skill_versatility":6.0,"career_switch":5.5,"reputation_variance":1.5,
        "ai_resistance":6.0,"social_status":6.5,"remote_friendly":4.5,"autonomy":6.5,
        "family_friendly":5.5,"fulfillment":7.0,"entrepreneurship":6.0,"gender_equality":5.5,
        "age_flexibility":5.5,"social_interaction":5.5,"physical_demand":3.0,"license_barrier":3.5,
        "cycle_sensitivity":5.0,"side_job_compat":4.0,"intl_mobility":6.0,"industry_monopoly":3.5,
        "trend_long":3,"trend_short":3,"edu":"本科/硕士","age":"24-32",
    },
}

# === PER-OCCUPATION OVERRIDES ===
OVR = {
    # crop_farming
    "0101": {},  # Grain Farmer — defaults are correct
    "0102": {"fulfillment":6.0,"entrepreneurship":7.0,"cycle_sensitivity":7.0},
    "0103": {"market_size":5.0,"intl_mobility":3.5,"fulfillment":6.5,"social_status":4.0,"cycle_sensitivity":6.5},
    "0104": {"physical_demand":6.5,"fulfillment":6.5,"market_size":5.5,"cycle_sensitivity":7.5,"gender_equality":6.0},
    "0105": {"learning_cost":4.5,"education_req":3.5,"value_added":4.0,"social_status":4.5,"ai_resistance":4.5,"trend_short":2,"growth_coeff":5.5,"fulfillment":6.5,"entrepreneurship":7.0,"edu":"大专/培训","age":"20-35"},
    "0106": {"learning_cost":5.5,"education_req":4.5,"value_added":5.5,"ai_resistance":3.0,"growth_coeff":7.0,"trend_short":4,"trend_long":3,"remote_friendly":2.0,"physical_demand":4.0,"social_status":5.0,"supply_demand":6.5,"developed_scarcity":6.0,"edu":"大专/本科","age":"22-32"},
    "0107": {"learning_cost":7.0,"education_req":7.0,"value_added":6.5,"social_status":6.5,"ai_resistance":6.0,"growth_coeff":5.0,"physical_demand":4.0,"remote_friendly":3.0,"career_switch":5.0,"intl_mobility":5.5,"license_barrier":4.0,"supply_demand":5.5,"edu":"本科/硕士","age":"24-32"},
    "0108": {"learning_cost":6.0,"education_req":4.5,"value_added":6.0,"social_status":6.0,"fulfillment":8.0,"entrepreneurship":8.0,"market_size":4.0,"intl_mobility":5.0,"ai_resistance":7.5,"physical_demand":6.0,"cycle_sensitivity":6.5,"edu":"专业培训/大专","age":"22-35"},
    "0109": {"learning_cost":8.0,"education_req":8.0,"value_added":7.0,"social_status":7.0,"ai_resistance":6.5,"growth_coeff":6.0,"physical_demand":3.0,"remote_friendly":3.5,"supply_demand":6.5,"developed_scarcity":7.0,"intl_mobility":6.5,"fulfillment":7.5,"gender_equality":5.5,"edu":"硕士/博士","age":"26-35"},
    "0110": {"learning_cost":4.0,"education_req":3.0,"physical_demand":6.5,"safety":6.0,"ai_resistance":4.0,"supply_demand":5.0,"market_size":6.0,"edu":"大专/培训","age":"20-30"},
    "0111": {"trend_short":-3,"trend_long":-2,"market_size":5.0,"social_status":3.0,"growth_coeff":1.5,"ai_resistance":4.0,"fulfillment":4.0},
    "0112": {"market_size":5.5,"intl_mobility":3.5,"fulfillment":6.0,"social_status":3.5,"entrepreneurship":7.0,"cycle_sensitivity":7.5},
    "0113": {"physical_demand":6.5,"learning_cost":3.5,"market_size":4.5,"ai_resistance":5.0,"entrepreneurship":7.0,"cycle_sensitivity":6.0,"edu":"培训","age":"18-40"},
    "0114": {"learning_cost":5.0,"education_req":4.0,"value_added":5.0,"ai_resistance":3.5,"growth_coeff":7.5,"trend_short":4,"trend_long":3,"physical_demand":3.0,"remote_friendly":2.5,"social_status":5.0,"supply_demand":6.0,"developed_scarcity":6.0,"safety":7.0,"edu":"培训/大专","age":"20-35"},
    # livestock
    "0201": {"physical_demand":8.0,"autonomy":7.5,"entrepreneurship":7.0,"family_friendly":4.0,"safety":5.0},
    "0202": {"learning_cost":7.5,"education_req":7.5,"value_added":7.0,"social_status":7.0,"ai_resistance":7.5,"physical_demand":5.0,"remote_friendly":1.5,"license_barrier":7.5,"supply_demand":6.5,"developed_scarcity":7.0,"intl_mobility":5.5,"fulfillment":8.0,"career_switch":5.0,"growth_coeff":4.5,"edu":"本科/硕士(兽医学)","age":"24-30"},
    "0203": {"physical_demand":6.5,"safety":5.5,"ai_resistance":4.5,"value_added":4.0,"supply_demand":5.0},
    "0204": {"physical_demand":7.0,"safety":5.0,"ai_resistance":4.0,"market_size":7.0,"cycle_sensitivity":6.5},
    "0205": {"learning_cost":5.0,"education_req":4.5,"value_added":5.0,"ai_resistance":5.5,"physical_demand":5.5,"supply_demand":5.5,"growth_coeff":4.0,"edu":"大专/本科","age":"22-32"},
    "0206": {"learning_cost":4.5,"education_req":4.0,"value_added":4.5,"ai_resistance":6.0,"physical_demand":5.5,"license_barrier":4.5,"social_status":5.0,"gender_equality":7.0,"edu":"大专/培训","age":"20-28"},
    "0207": {"learning_cost":6.5,"education_req":6.5,"value_added":6.0,"social_status":6.0,"ai_resistance":5.5,"physical_demand":2.5,"remote_friendly":3.5,"growth_coeff":5.0,"supply_demand":5.5,"edu":"本科/硕士","age":"24-32"},
    "0208": {"physical_demand":6.0,"entrepreneurship":7.5,"fulfillment":7.5,"safety":5.5,"ai_resistance":7.5,"market_size":4.0,"social_interaction":3.5,"side_job_compat":5.5,"age_flexibility":7.5,"edu":"培训/自学","age":"20-50"},
    "0209": {"learning_cost":5.0,"education_req":4.0,"value_added":5.5,"social_status":5.0,"autonomy":8.0,"social_interaction":6.0,"physical_demand":6.5,"entrepreneurship":7.5,"ai_resistance":6.0,"edu":"大专/经验","age":"28-40"},
    "0210": {"market_size":3.0,"intl_mobility":2.0,"ai_resistance":6.5,"physical_demand":5.0,"trend_short":-2,"trend_long":-2,"growth_coeff":1.5,"social_status":3.0},
    # fishery
    "0301": {"physical_demand":9.5,"safety":2.0,"family_friendly":1.5,"ai_resistance":7.0,"intl_mobility":5.0,"value_added":4.5,"social_interaction":6.0,"burnout":3.5,"overtime":2.5,"occupational_disease":3.0,"gender_equality":2.0,"age_flexibility":4.5,"edu":"无要求","age":"18-30"},
    "0302": {"physical_demand":7.0,"safety":5.0,"ai_resistance":5.0,"entrepreneurship":6.5,"value_added":3.5,"autonomy":7.0,"family_friendly":4.5},
    "0303": {"learning_cost":4.5,"education_req":3.5,"physical_demand":6.5,"safety":5.0,"ai_resistance":5.0,"growth_coeff":5.0,"supply_demand":5.5,"value_added":4.5,"trend_short":1,"edu":"大专/培训","age":"20-30"},
    "0304": {"physical_demand":7.5,"safety":4.5,"ai_resistance":4.0,"value_added":3.0,"market_size":6.5,"gender_equality":4.5,"edu":"培训","age":"18-35"},
    "0305": {"learning_cost":8.0,"education_req":8.0,"value_added":6.5,"social_status":7.0,"ai_resistance":7.0,"physical_demand":4.5,"remote_friendly":3.0,"fulfillment":8.5,"growth_coeff":5.5,"supply_demand":6.0,"intl_mobility":7.0,"gender_equality":6.0,"edu":"硕士/博士","age":"26-35"},
    "0306": {"market_size":2.5,"intl_mobility":3.0,"ai_resistance":7.0,"physical_demand":6.5,"entrepreneurship":6.0,"fulfillment":6.5,"safety":4.5},
    "0307": {"learning_cost":5.0,"education_req":4.5,"value_added":5.0,"social_status":5.5,"ai_resistance":6.5,"physical_demand":4.0,"license_barrier":5.5,"stability":6.5,"remote_friendly":2.0,"safety":6.5,"edu":"大专/本科","age":"24-35"},
    # mining
    "0401": {"physical_demand":9.5,"safety":2.0,"occupational_disease":2.0,"value_added":4.5,"burnout":3.5,"overtime":3.0,"ai_resistance":4.5,"age_flexibility":4.0},
    "0402": {"physical_demand":9.5,"safety":1.5,"occupational_disease":1.5,"value_added":5.0,"burnout":3.0,"overtime":3.0,"ai_resistance":5.0,"age_flexibility":3.5,"family_friendly":2.5},
    "0403": {"learning_cost":7.0,"education_req":7.0,"value_added":8.0,"social_status":7.0,"ai_resistance":6.0,"physical_demand":4.0,"remote_friendly":2.5,"supply_demand":7.0,"developed_scarcity":7.5,"intl_mobility":7.0,"safety":5.0,"license_barrier":5.5,"career_switch":5.0,"growth_coeff":4.0,"edu":"本科/硕士","age":"24-32"},
    "0404": {"learning_cost":7.5,"education_req":7.5,"value_added":7.5,"social_status":7.0,"ai_resistance":6.5,"physical_demand":5.0,"remote_friendly":2.5,"supply_demand":6.5,"developed_scarcity":7.0,"intl_mobility":7.5,"fulfillment":7.0,"safety":5.5,"license_barrier":5.0,"edu":"本科/硕士","age":"24-32"},
    "0405": {"learning_cost":4.5,"education_req":3.5,"value_added":5.5,"safety":1.5,"physical_demand":8.0,"license_barrier":7.0,"ai_resistance":7.0,"supply_demand":6.0,"social_status":4.0,"edu":"专业培训+证书","age":"22-35"},
    "0406": {"learning_cost":7.0,"education_req":7.0,"value_added":7.5,"social_status":7.0,"ai_resistance":7.0,"physical_demand":4.0,"remote_friendly":2.0,"license_barrier":6.5,"safety":6.0,"stability":6.5,"supply_demand":7.0,"developed_scarcity":7.0,"intl_mobility":6.5,"fulfillment":7.0,"growth_coeff":5.0,"edu":"本科/硕士","age":"24-32"},
    "0407": {"value_added":6.0,"family_friendly":2.0,"physical_demand":8.5,"safety":2.5,"comp_bonus":2.0,"supply_demand":6.5,"developed_scarcity":7.0,"intl_mobility":5.0,"cycle_sensitivity":8.5,"social_interaction":4.5,"edu":"技校+证书","age":"20-35"},
    "0408": {"learning_cost":1.5,"education_req":1.0,"value_added":2.0,"safety":1.0,"physical_demand":9.5,"social_status":2.0,"occupational_disease":1.5,"ai_resistance":6.5,"market_size":4.0,"stability":3.0,"entrepreneurship":5.0,"intl_mobility":1.5,"edu":"无要求","age":"16-40"},
    # oil_gas
    "0501": {"learning_cost":7.5,"education_req":7.5,"value_added":8.5,"social_status":7.5,"ai_resistance":6.0,"physical_demand":4.0,"remote_friendly":2.0,"supply_demand":6.5,"developed_scarcity":7.5,"intl_mobility":8.0,"license_barrier":5.5,"growth_coeff":3.0,"career_switch":5.0,"edu":"本科/硕士","age":"24-32"},
    "0502": {"value_added":8.0,"physical_demand":6.0,"safety":2.5,"ai_resistance":5.5,"intl_mobility":7.5,"family_friendly":2.5,"supply_demand":6.5,"edu":"本科","age":"24-32"},
    "0503": {"value_added":7.5,"physical_demand":5.0,"safety":4.0,"ai_resistance":5.5,"intl_mobility":7.0,"license_barrier":5.0,"edu":"本科","age":"24-32"},
    "0504": {"value_added":7.5,"physical_demand":3.5,"safety":4.5,"ai_resistance":5.5,"career_switch":5.5,"growth_coeff":2.5,"edu":"本科","age":"24-32"},
    "0505": {"learning_cost":4.0,"education_req":3.0,"value_added":5.5,"physical_demand":8.0,"safety":2.5,"ai_resistance":5.0,"family_friendly":2.0,"burnout":3.5,"overtime":3.0,"supply_demand":5.5,"social_status":4.5,"edu":"技校/培训","age":"20-30"},
    "0506": {"learning_cost":8.0,"education_req":8.0,"value_added":8.0,"social_status":7.5,"ai_resistance":6.5,"physical_demand":4.0,"remote_friendly":3.0,"fulfillment":7.0,"intl_mobility":8.0,"supply_demand":6.0,"developed_scarcity":7.0,"edu":"硕士/博士","age":"26-35"},
    "0507": {"learning_cost":4.5,"education_req":4.0,"value_added":6.0,"physical_demand":6.0,"safety":3.5,"ai_resistance":5.0,"edu":"大专/技校","age":"20-30"},
    "0508": {"value_added":8.0,"growth_coeff":4.5,"intl_mobility":8.0,"supply_demand":7.0,"developed_scarcity":7.5,"physical_demand":3.5,"safety":4.5,"trend_short":1,"edu":"本科/硕士","age":"24-32"},
    "0509": {"learning_cost":3.5,"education_req":2.5,"value_added":6.5,"physical_demand":9.0,"safety":2.0,"family_friendly":1.5,"burnout":3.0,"overtime":2.5,"ai_resistance":6.0,"occupational_disease":2.5,"social_interaction":5.5,"intl_mobility":7.0,"edu":"培训/技校","age":"20-32"},
    # renewable_energy
    "0601": {"growth_coeff":8.5,"trend_short":5,"supply_demand":8.0,"developed_scarcity":7.5,"physical_demand":3.5,"safety":7.0,"value_added":7.5,"edu":"本科/硕士","age":"24-32"},
    "0602": {"growth_coeff":8.0,"physical_demand":4.0,"supply_demand":7.5,"developed_scarcity":7.0,"value_added":7.0,"edu":"本科/硕士","age":"24-32"},
    "0603": {"growth_coeff":9.0,"trend_short":5,"supply_demand":8.5,"developed_scarcity":8.0,"value_added":7.5,"ai_resistance":6.5,"edu":"本科/硕士","age":"24-32"},
    "0604": {"growth_coeff":8.5,"trend_short":5,"supply_demand":8.0,"developed_scarcity":8.0,"value_added":7.5,"market_size":3.5,"ai_resistance":6.5,"edu":"本科/硕士","age":"24-32"},
    "0605": {"learning_cost":4.0,"education_req":3.5,"value_added":5.0,"physical_demand":8.0,"safety":4.5,"ai_resistance":7.0,"growth_coeff":7.5,"supply_demand":7.0,"social_status":5.0,"remote_friendly":0.5,"edu":"技校/培训","age":"20-30"},
    "0606": {"learning_cost":6.0,"education_req":6.0,"value_added":7.0,"physical_demand":1.5,"remote_friendly":6.5,"ai_resistance":5.0,"growth_coeff":8.0,"trend_short":5,"social_status":6.5,"supply_demand":7.0,"fulfillment":6.5,"career_switch":6.0,"entrepreneurship":5.5,"edu":"本科/硕士","age":"24-32"},
    "0607": {"value_added":7.5,"social_status":7.5,"autonomy":7.0,"social_interaction":7.5,"entrepreneurship":7.5,"growth_coeff":8.5,"physical_demand":2.5,"remote_friendly":4.0,"intl_mobility":7.5,"career_switch":6.0,"edu":"本科/硕士","age":"28-38"},
    "0608": {"growth_coeff":6.5,"market_size":4.0,"physical_demand":4.5,"value_added":6.0,"trend_short":3},
    "0609": {"growth_coeff":6.5,"market_size":3.5,"physical_demand":5.0,"value_added":6.5,"supply_demand":6.5,"trend_short":3},
    # environmental
    "0701": {"value_added":6.5,"supply_demand":6.5,"developed_scarcity":6.5,"license_barrier":5.5,"intl_mobility":6.5,"ai_resistance":6.5},
    "0702": {"physical_demand":5.0,"safety":6.0,"value_added":5.5,"ai_resistance":6.5,"supply_demand":6.0,"remote_friendly":2.5},
    "0703": {"value_added":5.0,"physical_demand":5.5,"safety":5.5,"ai_resistance":5.5,"supply_demand":5.5,"remote_friendly":2.5},
    "0704": {"value_added":6.5,"license_barrier":6.5,"remote_friendly":5.0,"ai_resistance":6.0,"social_interaction":7.0,"intl_mobility":6.5,"entrepreneurship":6.0,"edu":"本科/硕士+资格证","age":"26-35"},
    "0705": {"learning_cost":7.0,"education_req":7.5,"value_added":6.5,"social_status":7.0,"fulfillment":8.0,"physical_demand":3.5,"remote_friendly":4.5,"intl_mobility":7.0,"supply_demand":6.0,"ai_resistance":7.0,"edu":"硕士/博士","age":"26-35"},
    "0706": {"value_added":5.5,"physical_demand":3.0,"remote_friendly":4.0,"ai_resistance":5.5,"supply_demand":5.5,"growth_coeff":6.0},
    "0707": {"physical_demand":5.5,"fulfillment":8.5,"social_status":6.5,"ai_resistance":7.5,"remote_friendly":2.0,"intl_mobility":6.5,"market_size":3.5,"supply_demand":5.5,"growth_coeff":6.0,"gender_equality":6.5},
    "0708": {"value_added":6.5,"license_barrier":5.5,"supply_demand":6.5,"developed_scarcity":6.5,"ai_resistance":6.5,"remote_friendly":3.5,"social_interaction":6.5,"physical_demand":3.5},
    "0709": {"value_added":7.0,"remote_friendly":5.5,"social_interaction":7.5,"entrepreneurship":7.0,"intl_mobility":7.0,"ai_resistance":6.0,"license_barrier":5.5,"career_switch":6.0,"growth_coeff":7.0,"edu":"本科/硕士","age":"26-35"},
    "0710": {"physical_demand":5.5,"safety":5.5,"value_added":6.0,"ai_resistance":6.5,"supply_demand":6.0,"remote_friendly":2.0,"occupational_disease":5.5},
    "0711": {"physical_demand":5.5,"fulfillment":9.0,"social_status":6.5,"ai_resistance":8.0,"remote_friendly":1.5,"family_friendly":4.5,"market_size":3.0,"value_added":5.0,"supply_demand":5.0,"intl_mobility":6.0,"gender_equality":6.5,"growth_coeff":5.5},
    # forestry
    "0801": {"physical_demand":7.0,"safety":4.5,"fulfillment":7.0,"stability":6.5,"ai_resistance":7.5,"social_interaction":4.0,"remote_friendly":0.5,"license_barrier":3.5,"gender_equality":4.0,"social_status":4.5,"edu":"培训/大专","age":"20-35"},
    "0802": {"physical_demand":8.5,"safety":3.5,"ai_resistance":6.0,"value_added":3.5,"occupational_disease":3.5,"edu":"技校/培训","age":"18-35"},
    "0803": {"physical_demand":9.0,"safety":2.0,"ai_resistance":8.5,"fulfillment":8.0,"social_status":6.0,"value_added":4.5,"burnout":3.5,"overtime":3.0,"family_friendly":2.5,"gender_equality":3.0,"occupational_disease":3.0,"cycle_sensitivity":7.0,"edu":"培训+体能","age":"20-35"},
    "0804": {"learning_cost":6.5,"education_req":6.5,"value_added":6.0,"social_status":6.0,"ai_resistance":6.5,"physical_demand":4.5,"remote_friendly":2.5,"supply_demand":5.5,"intl_mobility":5.0,"fulfillment":7.0,"growth_coeff":4.5,"edu":"本科","age":"24-32"},
    "0805": {"physical_demand":9.5,"safety":2.5,"occupational_disease":2.5,"ai_resistance":6.5,"value_added":3.5,"burnout":3.5,"social_status":3.0,"career_lifespan":5.5,"age_flexibility":4.0,"edu":"无要求","age":"18-35"},
    "0806": {"learning_cost":4.5,"education_req":3.5,"physical_demand":7.5,"safety":4.0,"ai_resistance":7.5,"entrepreneurship":6.5,"fulfillment":7.0,"value_added":5.0,"supply_demand":5.5,"developed_scarcity":5.5,"license_barrier":4.0,"social_status":4.5,"edu":"培训+证书","age":"20-40"},
    # agricultural_tech
    "0901": {"learning_cost":7.0,"education_req":6.5,"value_added":7.5,"ai_resistance":5.0,"growth_coeff":8.0,"trend_short":4,"remote_friendly":5.5,"physical_demand":2.0,"supply_demand":7.5,"developed_scarcity":7.5,"social_status":7.0,"intl_mobility":7.0,"edu":"本科/硕士","age":"24-32"},
    "0902": {"value_added":6.0,"growth_coeff":8.0,"trend_short":4,"physical_demand":4.0,"remote_friendly":2.5,"entrepreneurship":7.0,"ai_resistance":5.5,"supply_demand":7.0,"market_size":3.5,"social_status":6.0,"edu":"本科","age":"24-35"},
    "0903": {"learning_cost":8.0,"education_req":8.5,"value_added":7.0,"social_status":7.5,"ai_resistance":7.0,"fulfillment":8.0,"physical_demand":2.5,"remote_friendly":4.0,"intl_mobility":7.5,"supply_demand":7.0,"developed_scarcity":7.5,"growth_coeff":7.5,"edu":"硕士/博士","age":"26-35"},
    "0904": {"learning_cost":7.0,"education_req":7.0,"value_added":6.5,"social_status":6.5,"ai_resistance":5.5,"physical_demand":2.5,"remote_friendly":4.0,"supply_demand":6.0,"intl_mobility":6.5,"market_size":6.0,"license_barrier":4.0,"edu":"本科/硕士","age":"24-32"},
    "0905": {"learning_cost":7.5,"education_req":7.5,"value_added":6.5,"social_status":7.0,"ai_resistance":6.5,"physical_demand":1.5,"remote_friendly":6.5,"intl_mobility":7.0,"fulfillment":6.5,"market_size":4.0,"edu":"硕士/博士","age":"26-35"},
    "0906": {"learning_cost":4.5,"education_req":4.5,"value_added":5.0,"physical_demand":4.5,"license_barrier":5.5,"stability":6.5,"ai_resistance":6.0,"remote_friendly":2.0,"safety":7.0,"social_status":5.0,"edu":"大专/本科","age":"22-30"},
    "0907": {"learning_cost":8.0,"education_req":8.0,"value_added":6.0,"social_status":6.5,"ai_resistance":7.0,"physical_demand":4.0,"remote_friendly":3.0,"fulfillment":8.0,"intl_mobility":7.0,"market_size":3.0,"supply_demand":5.5,"edu":"硕士/博士","age":"26-35"},
    "0908": {"learning_cost":7.5,"education_req":7.5,"value_added":6.0,"social_status":6.5,"ai_resistance":6.5,"physical_demand":4.5,"remote_friendly":3.0,"fulfillment":7.0,"intl_mobility":6.5,"supply_demand":6.0,"edu":"硕士/博士","age":"26-35"},
    "0909": {"learning_cost":4.0,"education_req":4.0,"value_added":5.0,"physical_demand":3.5,"license_barrier":4.5,"stability":6.5,"ai_resistance":4.5,"remote_friendly":2.5,"safety":7.5,"edu":"大专/本科","age":"22-30"},
    "0910": {"learning_cost":7.5,"education_req":7.5,"value_added":6.0,"social_status":6.5,"ai_resistance":6.0,"physical_demand":2.0,"remote_friendly":5.0,"fulfillment":7.0,"intl_mobility":6.5,"market_size":3.5,"supply_demand":5.5,"edu":"本科/硕士","age":"24-32"},
    "0911": {"value_added":5.5,"growth_coeff":7.5,"trend_short":4,"physical_demand":3.5,"remote_friendly":3.0,"ai_resistance":5.0,"entrepreneurship":6.5,"supply_demand":6.5,"edu":"大专/本科","age":"22-32"},
    "0912": {"learning_cost":5.5,"education_req":5.5,"value_added":6.0,"physical_demand":2.0,"remote_friendly":5.5,"ai_resistance":5.0,"social_interaction":7.0,"license_barrier":5.0,"career_switch":6.0,"entrepreneurship":5.5,"market_size":5.5,"edu":"本科","age":"24-32"},
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
    agri_f = (cp["agri"] - 6.0) / 4.0
    mine_f = (cp["mine"] - 5.0) / 5.0
    oil_f  = (cp["oil"] - 5.0) / 5.0
    renew_f = (cp["renew"] - 6.0) / 4.0
    env_f  = (cp["env_reg"] - 6.0) / 4.0
    mech_f = (cp["mech"] - 6.0) / 4.0
    res_f  = (cp["res"] - 5.0) / 5.0
    fish_f = (cp["fish"] - 5.0) / 5.0
    comp_f = (cp["comp"] - 5.0) / 5.0
    stab_f = (cp["stab"] - 5.5) / 4.5
    wlb_f  = (cp["wlb"] - 6.0) / 4.0
    gender_f = (cp["gender"] - 5.5) / 4.5
    edu_f  = (cp["edu"] - 6.0) / 4.0
    intl_f = (cp["intl"] - 6.0) / 4.0
    reg_f  = (cp["reg"] - 5.5) / 4.5
    safe_f = (cp["safe"] - 6.0) / 4.0

    mid = occ["mid"]
    # Sector-specific factor
    if mid == "crop_farming":
        sector_f = agri_f
    elif mid == "livestock":
        sector_f = agri_f * 0.8 + mech_f * 0.2
    elif mid == "fishery":
        sector_f = fish_f
    elif mid == "mining":
        sector_f = mine_f
    elif mid == "oil_gas":
        sector_f = oil_f
    elif mid == "renewable_energy":
        sector_f = renew_f
    elif mid == "environmental":
        sector_f = env_f
    elif mid == "forestry":
        sector_f = (agri_f + res_f) / 2
    elif mid == "agricultural_tech":
        sector_f = (agri_f + mech_f) / 2
    else:
        sector_f = agri_f

    # Value-added: compensation level + mechanization for farming
    s["value_added"] = clamp(s["value_added"] + comp_f * 1.8 + mech_f * 0.3)
    s["cost_performance"] = clamp(s["cost_performance"] + comp_f * 0.6 + sector_f * 0.4)
    # Growth: sector strength + renewable/tech trends
    s["growth_coeff"] = clamp(s["growth_coeff"] + sector_f * 0.8)
    s["career_lifespan"] = clamp(s["career_lifespan"] + stab_f * 0.6)
    # Opportunity: bigger in countries where sector is important
    s["opportunity"] = clamp(s["opportunity"] + sector_f * 1.2)
    s["market_size"] = clamp(s["market_size"] + sector_f * 1.5)
    s["supply_demand"] = clamp(s["supply_demand"] + sector_f * 0.6 + mech_f * 0.3)
    # Developed scarcity
    dev_bonus = 0.8 if cp["mech"] >= 7.5 else (0.0 if cp["mech"] >= 5.0 else -0.8)
    s["developed_scarcity"] = clamp(s["developed_scarcity"] + dev_bonus)
    # Stability
    s["stability"] = clamp(s["stability"] + stab_f * 1.5 + reg_f * 0.3)
    # Safety: strongly affected by country safety standards
    s["safety"] = clamp(s["safety"] + safe_f * 1.2 + reg_f * 0.3)
    s["occupational_disease"] = clamp(s["occupational_disease"] + wlb_f * 0.3 + safe_f * 0.5)
    s["overtime"] = clamp(s["overtime"] + (cp["ot"] - 5.0) / 5.0 * 2.5)
    s["burnout"] = clamp(s["burnout"] + (cp["ot"] - 5.0) / 5.0 * 1.5)
    # Remote: AGR is very low remote, but slight variation
    s["remote_friendly"] = clamp(s["remote_friendly"] + wlb_f * 0.2)
    s["autonomy"] = clamp(s["autonomy"] + wlb_f * 0.3 + sector_f * 0.2)
    s["family_friendly"] = clamp(s["family_friendly"] + wlb_f * 1.5)
    # Social status: varies with compensation and sector importance
    s["social_status"] = clamp(s["social_status"] + sector_f * 0.4 + comp_f * 0.4)
    s["fulfillment"] = clamp(s["fulfillment"] + sector_f * 0.2)
    s["gender_equality"] = clamp(s["gender_equality"] + gender_f * 2.0)
    s["age_flexibility"] = clamp(s["age_flexibility"] + wlb_f * 0.3 + sector_f * 0.15)
    s["entrepreneurship"] = clamp(s["entrepreneurship"] + sector_f * 0.3 + reg_f * 0.3)
    s["intl_mobility"] = clamp(s["intl_mobility"] + intl_f * 1.5)
    # AI resistance: mechanization increases AI threat for basic farming
    if mid in ("crop_farming", "livestock"):
        s["ai_resistance"] = clamp(s["ai_resistance"] - mech_f * 0.4)
    else:
        s["ai_resistance"] = clamp(s["ai_resistance"] + sector_f * 0.15)
    s["learning_cost"] = clamp(s["learning_cost"] + edu_f * 0.3)
    s["education_req"] = clamp(s["education_req"] + edu_f * 0.3)
    s["license_barrier"] = clamp(s["license_barrier"] + reg_f * 0.5)
    s["cycle_sensitivity"] = clamp(s["cycle_sensitivity"] - stab_f * 0.5)
    s["side_job_compat"] = clamp(s["side_job_compat"] + wlb_f * 0.3)
    s["industry_monopoly"] = clamp(s["industry_monopoly"] - sector_f * 0.2 + (1 - cp["reg"] / 10.0) * 0.3)
    s["skill_versatility"] = clamp(s["skill_versatility"] + sector_f * 0.4)
    s["career_switch"] = clamp(s["career_switch"] + sector_f * 0.3 + mech_f * 0.2)
    rep_adj = -0.3 if cp["safe"] >= 7.5 else (0.3 if cp["safe"] < 4.5 else 0.0)
    s["reputation_variance"] = clamp5(s["reputation_variance"] + rep_adj)

    # === SECTOR-SPECIFIC ADJUSTMENTS ===
    # Mining: AU/ZA/BR mining powerhouses
    if mid == "mining":
        s["market_size"] = clamp(s["market_size"] + mine_f * 1.0)
        s["value_added"] = clamp(s["value_added"] + mine_f * 0.5)
        s["safety"] = clamp(s["safety"] + safe_f * 0.5)  # extra safety sensitivity
    # Oil & Gas: SA/RU state monopoly patterns
    if mid == "oil_gas":
        s["market_size"] = clamp(s["market_size"] + oil_f * 1.0)
        s["value_added"] = clamp(s["value_added"] + oil_f * 0.4)
        if cp["oil"] >= 8.0:
            s["industry_monopoly"] = clamp(s["industry_monopoly"] + 1.5)  # Aramco/Gazprom
            s["stability"] = clamp(s["stability"] + 0.8)
    # Fishery: NO(via DK)/JP/ID fishing nations
    if mid == "fishery":
        s["market_size"] = clamp(s["market_size"] + fish_f * 1.2)
        s["value_added"] = clamp(s["value_added"] + fish_f * 0.4)
    # Renewable energy: DK/DE/CN leaders
    if mid == "renewable_energy":
        s["market_size"] = clamp(s["market_size"] + renew_f * 1.0)
        s["supply_demand"] = clamp(s["supply_demand"] + renew_f * 0.5)
        if cp["renew"] >= 8.5:
            s["growth_coeff"] = clamp(s["growth_coeff"] + 0.5)
    # Environmental: strong regulation = more jobs
    if mid == "environmental":
        s["market_size"] = clamp(s["market_size"] + env_f * 1.2)
        s["supply_demand"] = clamp(s["supply_demand"] + env_f * 0.5)
        s["stability"] = clamp(s["stability"] + env_f * 0.5)
    # Crop farming: mechanization reduces physical demand in developed
    if mid == "crop_farming":
        if cp["mech"] >= 8.0:
            s["physical_demand"] = clamp(s["physical_demand"] - 1.5)
        s["value_added"] = clamp(s["value_added"] + agri_f * 0.3)
    # Livestock: mechanization effect
    if mid == "livestock":
        if cp["mech"] >= 8.0:
            s["physical_demand"] = clamp(s["physical_demand"] - 1.0)
    # Agricultural tech: thrives in high-mech + high-agri countries
    if mid == "agricultural_tech":
        s["supply_demand"] = clamp(s["supply_demand"] + mech_f * 0.5 + agri_f * 0.3)
        s["market_size"] = clamp(s["market_size"] + mech_f * 0.5)
    return s

def get_trends(base, cp):
    t_long = base["trend_long"]
    t_short = base["trend_short"]
    # Renewable boost in green-leader countries
    if cp["renew"] >= 8.0:
        t_short = min(5, t_short + 1)
    elif cp["renew"] < 4.0:
        t_short = max(-5, t_short - 1)
    # Oil countries depress farming trends less, boost oil trends
    if cp["oil"] >= 8.0 and base.get("mid_hint", "") == "oil_gas":
        t_long = min(5, t_long + 1)
    if cp["agri"] >= 8.0:
        t_long = min(5, t_long)
    elif cp["agri"] < 3.0:
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
    if scores["safety"] <= 4.0: hz.append("安全风险高"); he.append("high safety risk")
    if scores["physical_demand"] >= 8.0: hz.append("体力要求高"); he.append("high physical demand")
    if scores["license_barrier"] >= 7.0: hz.append("准入门槛高"); he.append("high entry barrier")
    if scores["stability"] >= 7.5: hz.append("就业稳定"); he.append("stable employment")
    elif scores["stability"] <= 4.0: hz.append("就业波动大"); he.append("volatile employment")
    if scores["cycle_sensitivity"] >= 7.5: hz.append("受经济周期影响大"); he.append("highly cyclical")
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
    csv_path = PROJECT_ROOT / "data" / "csv" / "agriculture_resources.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for occ in OCCUPATIONS:
        base = occ_base(occ["id"], occ["mid"])
        for country in COUNTRIES:
            iso = country["iso"]
            cp = CP[iso]
            scores = apply_country_modifiers(base, cp, occ)
            rng = random.Random(hash(f"AGR-{occ['id']}-{iso}") % 10000)
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
            row_id = f"AGR-{occ['id']}-{iso}-general"
            row = {
                "id": row_id,
                "major_category": "农业、资源与环境",
                "major_code": "AGR",
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
                "typical_education": base.get("edu", "中学/无要求"),
                "typical_entry_age": base.get("age", "18-30"),
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
    json_path = PROJECT_ROOT / "data" / "json" / "agriculture_resources.json"
    convert_csv_to_json(str(csv_path), str(json_path))
    print(f"JSON written to {json_path}")

    # Notebook
    from tools.generate_notebook import create_data_notebook
    nb_path = PROJECT_ROOT / "notebooks" / "12_agriculture_resources.ipynb"
    create_data_notebook(
        str(csv_path), str(nb_path),
        title="农业、资源与环境 (AGR) — 完整数据",
        description="86 occupations × 45 countries/regions = 3,870 rows",
    )
    print(f"Notebook written to {nb_path}")


if __name__ == "__main__":
    main()
