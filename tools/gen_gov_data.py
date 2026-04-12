#!/usr/bin/env python3
"""Generate gov_public.csv — GOV data for Global Career Development Index.
50 occupations × 45 countries. Compact format.
"""
import csv, sys, random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from tools.score_calculator import load_weights, calculate_composite

# ---------------------------------------------------------------------------
# OCCUPATIONS (from categories.yaml GOV section)
# ---------------------------------------------------------------------------
# Compact: (id, mid, mid_zh, mid_en, zh, en, isco, onet, locality)
_OCC_RAW = [
    # central_civil_service
    ("0101","central_civil_service","中央/联邦公务员","Central/Federal Civil Service","中央政府公务员","Central Government Civil Servant","1112","11-1031.00","global"),
    ("0102","central_civil_service","中央/联邦公务员","Central/Federal Civil Service","外交官","Diplomat","2422","11-1031.00","global"),
    ("0103","central_civil_service","中央/联邦公务员","Central/Federal Civil Service","政策分析师","Policy Analyst","2422","19-3094.00","global"),
    ("0104","central_civil_service","中央/联邦公务员","Central/Federal Civil Service","财政预算官员","Budget Analyst","2411","13-2031.00","global"),
    ("0105","central_civil_service","中央/联邦公务员","Central/Federal Civil Service","税务官员","Tax Official","3353","13-2081.00","global"),
    ("0106","central_civil_service","中央/联邦公务员","Central/Federal Civil Service","立法助理/政策顾问","Legislative Assistant / Policy Advisor","2422","19-3094.00","global"),
    ("0107","central_civil_service","中央/联邦公务员","Central/Federal Civil Service","政府发言人/新闻官","Government Spokesperson / Press Secretary","2432","27-3031.00","global"),
    # local_civil_service
    ("0201","local_civil_service","地方公务员","Local Civil Service","地方政府公务员","Local Government Officer","3354","11-1031.00","global"),
    ("0202","local_civil_service","地方公务员","Local Civil Service","城管执法人员","Urban Management Officer (Chengguan)","3355","","country_specific"),
    ("0203","local_civil_service","地方公务员","Local Civil Service","民政事务员","Civil Affairs Officer","3354","21-1099.00","global"),
    ("0204","local_civil_service","地方公务员","Local Civil Service","社区干部/街道办事员","Community/Street Office Official","3354","","country_specific"),
    ("0205","local_civil_service","地方公务员","Local Civil Service","镇长/区长","Mayor / District Governor","1112","11-1031.00","global"),
    ("0206","local_civil_service","地方公务员","Local Civil Service","规划审批官员","Planning & Zoning Officer","3354","19-3051.00","global"),
    ("0207","local_civil_service","地方公务员","Local Civil Service","公共卫生巡查员","Public Health Inspector","3257","29-9011.00","global"),
    # judicial_admin
    ("0301","judicial_admin","司法行政","Judicial Administration","法院书记员","Court Clerk","3411","43-4031.00","global"),
    ("0302","judicial_admin","司法行政","Judicial Administration","法警","Court Marshal / Bailiff","5412","33-3011.00","global"),
    ("0303","judicial_admin","司法行政","Judicial Administration","监狱管理人员","Corrections Officer","5413","33-3012.00","global"),
    ("0304","judicial_admin","司法行政","Judicial Administration","缓刑官/假释官","Probation / Parole Officer","3412","21-1092.00","global"),
    # public_institutions
    ("0401","public_institutions","事业单位/公共机构","Public Institutions","事业编制人员","Public Institution Staff (Shiye Bian)","3354","","country_specific"),
    ("0402","public_institutions","事业单位/公共机构","Public Institutions","公共图书馆馆长","Public Library Director","1345","11-9121.01","global"),
    ("0403","public_institutions","事业单位/公共机构","Public Institutions","政府统计人员","Government Statistician","2120","15-2041.00","global"),
    ("0404","public_institutions","事业单位/公共机构","Public Institutions","气象预报员","Meteorologist","2112","19-2021.00","global"),
    # international_org
    ("0501","international_org","国际组织","International Organizations","联合国职员","United Nations Staff","2422","11-1031.00","global"),
    ("0502","international_org","国际组织","International Organizations","国际组织项目官员","International Organization Program Officer","2422","11-9199.00","global"),
    ("0503","international_org","国际组织","International Organizations","国际发展顾问","International Development Advisor","2422","19-3094.00","global"),
    ("0504","international_org","国际组织","International Organizations","翻译/口译(国际组织)","International Organization Translator/Interpreter","2643","27-3091.00","global"),
    # military
    ("0601","military","军事","Military","军官","Military Officer","0110","55-1011.00","global"),
    ("0602","military","军事","Military","士兵/士官","Enlisted Soldier / NCO","0210","55-3019.00","global"),
    ("0603","military","军事","Military","军事情报分析师","Military Intelligence Analyst","0110","55-3017.00","global"),
    ("0604","military","军事","Military","军医","Military Physician","2212","29-1216.00","global"),
    ("0605","military","军事","Military","军事工程师","Military Engineer","0110","55-1012.00","global"),
    # police_law_enforcement
    ("0701","police_law_enforcement","警察执法","Police & Law Enforcement","警察","Police Officer","5412","33-3051.00","global"),
    ("0702","police_law_enforcement","警察执法","Police & Law Enforcement","刑事侦探","Criminal Investigator / Detective","5412","33-3021.00","global"),
    ("0703","police_law_enforcement","警察执法","Police & Law Enforcement","辅警/协警","Auxiliary Police Officer","5412","","regional"),
    ("0704","police_law_enforcement","警察执法","Police & Law Enforcement","交通警察","Traffic Police Officer","5412","33-3051.00","global"),
    ("0705","police_law_enforcement","警察执法","Police & Law Enforcement","网络警察","Cybercrime Police Officer","5412","33-3021.00","global"),
    ("0706","police_law_enforcement","警察执法","Police & Law Enforcement","海关官员","Customs Officer","3351","33-3021.06","global"),
    ("0707","police_law_enforcement","警察执法","Police & Law Enforcement","边防警察","Border Patrol Agent","5412","33-3051.01","global"),
    # fire_emergency
    ("0801","fire_emergency","消防应急","Fire & Emergency Services","消防员","Firefighter","5411","33-2011.00","global"),
    ("0802","fire_emergency","消防应急","Fire & Emergency Services","消防队长","Fire Captain","5411","33-1021.01","global"),
    ("0803","fire_emergency","消防应急","Fire & Emergency Services","应急管理专员","Emergency Management Specialist","5419","13-1061.00","global"),
    ("0804","fire_emergency","消防应急","Fire & Emergency Services","灾害救援协调员","Disaster Relief Coordinator","5419","13-1061.00","global"),
    # intelligence_security
    ("0901","intelligence_security","情报安全","Intelligence & National Security","情报分析师","Intelligence Analyst","2422","33-3021.06","global"),
    ("0902","intelligence_security","情报安全","Intelligence & National Security","网络安全分析师(政府)","Government Cybersecurity Analyst","2529","15-1212.00","global"),
    ("0903","intelligence_security","情报安全","Intelligence & National Security","反恐专家","Counter-terrorism Specialist","5412","33-3021.06","global"),
    ("0904","intelligence_security","情报安全","Intelligence & National Security","密码学专家(政府)","Government Cryptographer","2529","15-1212.00","global"),
    ("0905","intelligence_security","情报安全","Intelligence & National Security","签证官员","Visa Officer / Immigration Officer","3351","33-3021.06","global"),
    ("0906","intelligence_security","情报安全","Intelligence & National Security","环境保护执法员","Environmental Enforcement Officer","3355","33-9032.00","global"),
    ("0907","intelligence_security","情报安全","Intelligence & National Security","食品药品监管员","Food & Drug Inspector","3257","45-2011.00","global"),
    ("0908","intelligence_security","情报安全","Intelligence & National Security","劳动监察员","Labor Inspector","3355","13-1041.00","global"),
]

OCCUPATIONS = [{"id":r[0],"mid":r[1],"mid_zh":r[2],"mid_en":r[3],"zh":r[4],"en":r[5],"isco":r[6],"onet":r[7],"locality":r[8]} for r in _OCC_RAW]

# ---------------------------------------------------------------------------
# COUNTRIES (same 45 as other generators)
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# COUNTRY PROFILES — GOV-specific dimensions
# (gov_size, civil_pay, mil_spend, police_trust, pub_stab, exam_sys, corruption,
#  wlb, gender, intl, comp, edu, reg)
# All 0-10 scale.
# ---------------------------------------------------------------------------
COUNTRY_PROFILES = {
    # East Asia — strong exam systems, high stability
    "CN": {"gov_size":9.0,"civil_pay":5.5,"mil_spend":7.0,"police_trust":6.5,"pub_stab":8.5,"exam_sys":9.5,"corruption":4.5,"wlb":4.0,"gender":5.5,"intl":5.0,"comp":5.0,"edu":7.5,"reg":6.0},
    "JP": {"gov_size":7.0,"civil_pay":7.0,"mil_spend":5.5,"police_trust":8.0,"pub_stab":9.0,"exam_sys":8.5,"corruption":7.5,"wlb":5.5,"gender":5.0,"intl":5.0,"comp":7.0,"edu":8.0,"reg":7.0},
    "KR": {"gov_size":6.5,"civil_pay":6.5,"mil_spend":6.5,"police_trust":6.5,"pub_stab":7.5,"exam_sys":9.0,"corruption":6.5,"wlb":5.0,"gender":4.5,"intl":5.5,"comp":6.5,"edu":8.0,"reg":6.5},
    "TW": {"gov_size":6.0,"civil_pay":5.5,"mil_spend":5.0,"police_trust":7.0,"pub_stab":7.5,"exam_sys":8.5,"corruption":6.5,"wlb":5.5,"gender":6.0,"intl":5.5,"comp":5.5,"edu":7.5,"reg":6.5},
    "HK": {"gov_size":5.5,"civil_pay":7.5,"mil_spend":2.0,"police_trust":5.5,"pub_stab":7.0,"exam_sys":6.0,"corruption":8.0,"wlb":5.0,"gender":6.5,"intl":8.5,"comp":7.5,"edu":7.5,"reg":7.0},
    # Southeast Asia
    "SG": {"gov_size":5.0,"civil_pay":9.0,"mil_spend":6.0,"police_trust":9.0,"pub_stab":9.5,"exam_sys":7.0,"corruption":9.5,"wlb":5.5,"gender":7.0,"intl":9.0,"comp":8.5,"edu":8.5,"reg":8.5},
    "TH": {"gov_size":7.5,"civil_pay":4.0,"mil_spend":5.5,"police_trust":4.5,"pub_stab":6.0,"exam_sys":5.5,"corruption":4.0,"wlb":6.0,"gender":6.0,"intl":4.5,"comp":3.5,"edu":5.5,"reg":5.0},
    "VN": {"gov_size":8.5,"civil_pay":3.0,"mil_spend":5.0,"police_trust":5.5,"pub_stab":7.5,"exam_sys":7.0,"corruption":3.5,"wlb":5.5,"gender":5.5,"intl":4.5,"comp":3.0,"edu":5.5,"reg":5.5},
    "ID": {"gov_size":7.5,"civil_pay":3.5,"mil_spend":4.0,"police_trust":4.0,"pub_stab":6.0,"exam_sys":5.5,"corruption":3.5,"wlb":5.5,"gender":5.0,"intl":4.0,"comp":3.5,"edu":5.0,"reg":5.0},
    "MY": {"gov_size":7.0,"civil_pay":5.0,"mil_spend":4.0,"police_trust":5.0,"pub_stab":7.0,"exam_sys":6.0,"corruption":5.0,"wlb":5.5,"gender":5.5,"intl":6.0,"comp":4.5,"edu":6.0,"reg":5.5},
    "PH": {"gov_size":7.0,"civil_pay":3.0,"mil_spend":3.5,"police_trust":3.5,"pub_stab":5.0,"exam_sys":5.0,"corruption":3.0,"wlb":5.5,"gender":6.5,"intl":6.0,"comp":3.0,"edu":5.5,"reg":4.5},
    # South Asia
    "IN": {"gov_size":8.0,"civil_pay":5.0,"mil_spend":6.5,"police_trust":4.0,"pub_stab":7.0,"exam_sys":9.0,"corruption":3.5,"wlb":5.0,"gender":4.5,"intl":5.5,"comp":4.5,"edu":7.0,"reg":5.5},
    "PK": {"gov_size":7.5,"civil_pay":3.0,"mil_spend":7.5,"police_trust":3.0,"pub_stab":5.0,"exam_sys":6.5,"corruption":2.5,"wlb":4.5,"gender":3.0,"intl":4.0,"comp":2.5,"edu":4.5,"reg":4.0},
    "BD": {"gov_size":7.0,"civil_pay":2.5,"mil_spend":4.0,"police_trust":3.0,"pub_stab":5.5,"exam_sys":6.5,"corruption":2.5,"wlb":4.5,"gender":3.5,"intl":4.0,"comp":2.0,"edu":4.0,"reg":3.5},
    # Middle East
    "AE": {"gov_size":7.0,"civil_pay":8.5,"mil_spend":6.5,"police_trust":8.5,"pub_stab":8.5,"exam_sys":4.0,"corruption":7.5,"wlb":5.5,"gender":5.0,"intl":7.5,"comp":8.0,"edu":7.0,"reg":6.5},
    "IL": {"gov_size":6.5,"civil_pay":6.5,"mil_spend":9.0,"police_trust":6.0,"pub_stab":6.5,"exam_sys":5.5,"corruption":6.5,"wlb":6.0,"gender":7.0,"intl":7.5,"comp":7.0,"edu":8.5,"reg":6.0},
    "SA": {"gov_size":8.5,"civil_pay":7.5,"mil_spend":8.5,"police_trust":6.5,"pub_stab":7.5,"exam_sys":4.0,"corruption":5.0,"wlb":5.0,"gender":3.5,"intl":5.0,"comp":7.0,"edu":6.0,"reg":5.0},
    "TR": {"gov_size":7.5,"civil_pay":4.0,"mil_spend":6.5,"police_trust":4.5,"pub_stab":5.5,"exam_sys":7.0,"corruption":4.0,"wlb":5.0,"gender":4.5,"intl":5.0,"comp":4.0,"edu":6.5,"reg":5.0},
    # Western Europe
    "GB": {"gov_size":6.0,"civil_pay":6.5,"mil_spend":5.5,"police_trust":7.0,"pub_stab":7.5,"exam_sys":6.0,"corruption":8.0,"wlb":7.5,"gender":7.5,"intl":8.5,"comp":7.0,"edu":8.5,"reg":7.5},
    "FR": {"gov_size":8.5,"civil_pay":6.0,"mil_spend":5.5,"police_trust":5.5,"pub_stab":8.0,"exam_sys":8.0,"corruption":7.0,"wlb":8.0,"gender":7.0,"intl":7.5,"comp":6.5,"edu":8.0,"reg":7.5},
    "DE": {"gov_size":6.5,"civil_pay":7.0,"mil_spend":4.5,"police_trust":7.5,"pub_stab":8.5,"exam_sys":7.0,"corruption":8.0,"wlb":8.5,"gender":7.0,"intl":7.5,"comp":7.5,"edu":8.0,"reg":8.0},
    "NL": {"gov_size":6.0,"civil_pay":7.0,"mil_spend":4.0,"police_trust":7.5,"pub_stab":8.0,"exam_sys":5.5,"corruption":8.5,"wlb":9.0,"gender":8.5,"intl":8.5,"comp":7.5,"edu":8.0,"reg":7.5},
    "CH": {"gov_size":5.0,"civil_pay":8.5,"mil_spend":3.5,"police_trust":8.5,"pub_stab":9.5,"exam_sys":5.5,"corruption":9.0,"wlb":8.5,"gender":7.0,"intl":8.0,"comp":9.0,"edu":9.0,"reg":7.5},
    # Nordic
    "SE": {"gov_size":7.5,"civil_pay":7.0,"mil_spend":4.5,"police_trust":8.0,"pub_stab":8.5,"exam_sys":5.0,"corruption":9.0,"wlb":9.0,"gender":9.0,"intl":8.0,"comp":7.0,"edu":8.5,"reg":7.5},
    "DK": {"gov_size":7.5,"civil_pay":7.5,"mil_spend":4.0,"police_trust":8.5,"pub_stab":8.5,"exam_sys":5.0,"corruption":9.5,"wlb":9.0,"gender":9.0,"intl":8.0,"comp":7.5,"edu":8.5,"reg":7.5},
    "FI": {"gov_size":7.0,"civil_pay":6.5,"mil_spend":4.5,"police_trust":9.0,"pub_stab":8.5,"exam_sys":5.0,"corruption":9.0,"wlb":9.0,"gender":9.0,"intl":7.5,"comp":6.5,"edu":9.0,"reg":7.5},
    # Southern Europe
    "IT": {"gov_size":7.5,"civil_pay":5.5,"mil_spend":4.0,"police_trust":5.5,"pub_stab":7.0,"exam_sys":7.0,"corruption":5.5,"wlb":6.5,"gender":5.5,"intl":6.5,"comp":5.5,"edu":7.0,"reg":6.5},
    "ES": {"gov_size":7.0,"civil_pay":5.5,"mil_spend":3.5,"police_trust":6.5,"pub_stab":7.0,"exam_sys":8.0,"corruption":6.0,"wlb":7.0,"gender":6.5,"intl":6.5,"comp":5.0,"edu":7.0,"reg":6.5},
    "PT": {"gov_size":6.5,"civil_pay":4.5,"mil_spend":3.5,"police_trust":7.0,"pub_stab":7.0,"exam_sys":6.5,"corruption":6.5,"wlb":7.0,"gender":7.0,"intl":7.0,"comp":4.5,"edu":6.5,"reg":6.0},
    # Eastern Europe
    "PL": {"gov_size":6.5,"civil_pay":4.5,"mil_spend":5.0,"police_trust":5.5,"pub_stab":6.5,"exam_sys":5.5,"corruption":6.0,"wlb":7.0,"gender":6.5,"intl":7.0,"comp":5.0,"edu":7.0,"reg":6.5},
    "CZ": {"gov_size":6.0,"civil_pay":5.0,"mil_spend":4.0,"police_trust":6.0,"pub_stab":7.5,"exam_sys":5.5,"corruption":6.5,"wlb":7.5,"gender":6.5,"intl":7.0,"comp":5.5,"edu":7.0,"reg":6.5},
    "RU": {"gov_size":8.5,"civil_pay":4.0,"mil_spend":8.5,"police_trust":3.5,"pub_stab":6.0,"exam_sys":5.0,"corruption":3.0,"wlb":5.5,"gender":6.0,"intl":3.5,"comp":4.5,"edu":7.5,"reg":4.5},
    # North America
    "US": {"gov_size":5.5,"civil_pay":7.0,"mil_spend":9.5,"police_trust":5.0,"pub_stab":7.0,"exam_sys":6.0,"corruption":7.5,"wlb":6.0,"gender":7.5,"intl":8.0,"comp":7.5,"edu":9.0,"reg":6.5},
    "CA": {"gov_size":6.0,"civil_pay":7.5,"mil_spend":4.0,"police_trust":7.0,"pub_stab":8.0,"exam_sys":5.5,"corruption":8.0,"wlb":7.5,"gender":8.0,"intl":8.5,"comp":7.5,"edu":8.0,"reg":7.0},
    "MX": {"gov_size":7.0,"civil_pay":3.5,"mil_spend":4.0,"police_trust":3.0,"pub_stab":5.0,"exam_sys":4.5,"corruption":3.0,"wlb":5.5,"gender":5.0,"intl":5.0,"comp":3.5,"edu":5.5,"reg":4.5},
    # South America
    "BR": {"gov_size":8.0,"civil_pay":5.5,"mil_spend":4.0,"police_trust":3.5,"pub_stab":6.5,"exam_sys":7.5,"corruption":3.5,"wlb":6.0,"gender":5.5,"intl":4.5,"comp":4.5,"edu":6.0,"reg":5.5},
    "AR": {"gov_size":8.0,"civil_pay":3.5,"mil_spend":3.0,"police_trust":3.5,"pub_stab":4.5,"exam_sys":4.5,"corruption":3.5,"wlb":5.5,"gender":5.5,"intl":5.0,"comp":3.5,"edu":6.5,"reg":4.5},
    "CL": {"gov_size":5.5,"civil_pay":5.0,"mil_spend":4.0,"police_trust":5.5,"pub_stab":6.5,"exam_sys":5.0,"corruption":6.5,"wlb":6.0,"gender":5.5,"intl":5.5,"comp":5.0,"edu":6.0,"reg":5.5},
    "CO": {"gov_size":7.0,"civil_pay":3.5,"mil_spend":5.0,"police_trust":3.5,"pub_stab":5.0,"exam_sys":5.0,"corruption":3.5,"wlb":5.5,"gender":5.0,"intl":4.5,"comp":3.5,"edu":5.5,"reg":5.0},
    # Oceania
    "AU": {"gov_size":6.0,"civil_pay":7.5,"mil_spend":5.0,"police_trust":7.5,"pub_stab":8.0,"exam_sys":5.5,"corruption":8.0,"wlb":8.0,"gender":8.0,"intl":8.0,"comp":7.5,"edu":8.0,"reg":7.0},
    "NZ": {"gov_size":5.5,"civil_pay":6.5,"mil_spend":3.5,"police_trust":8.5,"pub_stab":8.5,"exam_sys":5.0,"corruption":9.0,"wlb":8.5,"gender":8.5,"intl":7.5,"comp":6.5,"edu":7.5,"reg":7.0},
    # Africa
    "ZA": {"gov_size":7.0,"civil_pay":4.5,"mil_spend":3.5,"police_trust":3.5,"pub_stab":5.0,"exam_sys":4.5,"corruption":3.5,"wlb":5.5,"gender":5.5,"intl":5.0,"comp":4.0,"edu":5.5,"reg":5.0},
    "NG": {"gov_size":7.5,"civil_pay":3.0,"mil_spend":4.5,"police_trust":2.5,"pub_stab":4.0,"exam_sys":4.0,"corruption":2.0,"wlb":4.5,"gender":4.0,"intl":4.0,"comp":2.5,"edu":4.0,"reg":3.5},
    "KE": {"gov_size":7.0,"civil_pay":3.5,"mil_spend":4.5,"police_trust":3.0,"pub_stab":4.5,"exam_sys":4.5,"corruption":2.5,"wlb":5.0,"gender":4.5,"intl":5.0,"comp":2.5,"edu":4.5,"reg":4.0},
    "EG": {"gov_size":8.5,"civil_pay":3.0,"mil_spend":7.0,"police_trust":4.0,"pub_stab":5.5,"exam_sys":5.5,"corruption":3.0,"wlb":5.0,"gender":3.5,"intl":4.5,"comp":2.5,"edu":5.0,"reg":4.5},
}

# ---------------------------------------------------------------------------
# OCCUPATION BASE PROFILES
# Keys: learning_cost, education_req, growth_coeff, career_lifespan,
#   opportunity, market_size, supply_demand, developed_scarcity,
#   value_added, cost_performance, stability, safety, occupational_disease,
#   overtime, burnout, skill_versatility, career_switch, reputation_variance,
#   ai_resistance, social_status, remote_friendly, autonomy,
#   family_friendly, fulfillment, entrepreneurship, gender_equality,
#   age_flexibility, social_interaction, physical_demand, license_barrier,
#   cycle_sensitivity, side_job_compat, intl_mobility, industry_monopoly,
#   trend_long, trend_short, edu, age
# ---------------------------------------------------------------------------
def occ_base(oid):
    B = {
        # ===== CENTRAL CIVIL SERVICE =====
        "0101": {  # Central Government Civil Servant
            "learning_cost":6.0,"education_req":7.0,"growth_coeff":4.0,"career_lifespan":9.0,
            "opportunity":4.5,"market_size":5.0,"supply_demand":3.5,"developed_scarcity":3.0,
            "value_added":5.5,"cost_performance":5.0,"stability":9.5,"safety":9.0,
            "occupational_disease":7.5,"overtime":6.5,"burnout":6.0,
            "skill_versatility":5.5,"career_switch":4.0,"reputation_variance":2.5,
            "ai_resistance":6.5,"social_status":8.5,"remote_friendly":3.0,"autonomy":4.0,
            "family_friendly":6.5,"fulfillment":6.5,"entrepreneurship":1.5,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":7.0,"physical_demand":1.0,"license_barrier":8.5,
            "cycle_sensitivity":1.5,"side_job_compat":1.0,"intl_mobility":3.0,"industry_monopoly":8.0,
            "trend_long":0,"trend_short":0,"edu":"本科/硕士","age":"22-30",
        },
        "0102": {  # Diplomat
            "learning_cost":7.5,"education_req":8.0,"growth_coeff":4.5,"career_lifespan":8.5,
            "opportunity":3.0,"market_size":2.0,"supply_demand":4.0,"developed_scarcity":4.0,
            "value_added":7.0,"cost_performance":5.5,"stability":9.0,"safety":7.0,
            "occupational_disease":7.0,"overtime":5.0,"burnout":5.5,
            "skill_versatility":6.0,"career_switch":4.5,"reputation_variance":2.0,
            "ai_resistance":7.5,"social_status":9.0,"remote_friendly":2.0,"autonomy":5.0,
            "family_friendly":4.0,"fulfillment":8.0,"entrepreneurship":1.0,"gender_equality":5.0,
            "age_flexibility":6.0,"social_interaction":9.0,"physical_demand":1.5,"license_barrier":9.0,
            "cycle_sensitivity":1.0,"side_job_compat":0.5,"intl_mobility":9.5,"industry_monopoly":9.0,
            "trend_long":0,"trend_short":0,"edu":"硕士/博士","age":"25-32",
        },
        "0103": {  # Policy Analyst
            "learning_cost":6.5,"education_req":7.5,"growth_coeff":5.0,"career_lifespan":8.0,
            "opportunity":5.0,"market_size":4.0,"supply_demand":5.0,"developed_scarcity":4.5,
            "value_added":6.5,"cost_performance":5.5,"stability":8.0,"safety":9.5,
            "occupational_disease":7.0,"overtime":6.0,"burnout":5.5,
            "skill_versatility":6.5,"career_switch":5.5,"reputation_variance":1.5,
            "ai_resistance":6.0,"social_status":7.5,"remote_friendly":5.5,"autonomy":5.5,
            "family_friendly":6.0,"fulfillment":7.0,"entrepreneurship":3.0,"gender_equality":6.0,
            "age_flexibility":6.5,"social_interaction":7.0,"physical_demand":0.5,"license_barrier":7.0,
            "cycle_sensitivity":2.0,"side_job_compat":2.5,"intl_mobility":5.5,"industry_monopoly":6.5,
            "trend_long":1,"trend_short":1,"edu":"硕士","age":"24-30",
        },
        "0104": {  # Budget Analyst
            "learning_cost":6.0,"education_req":6.5,"growth_coeff":4.0,"career_lifespan":8.5,
            "opportunity":4.5,"market_size":4.5,"supply_demand":4.5,"developed_scarcity":4.0,
            "value_added":6.0,"cost_performance":5.5,"stability":9.0,"safety":9.5,
            "occupational_disease":7.5,"overtime":6.0,"burnout":5.5,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":1.5,
            "ai_resistance":5.0,"social_status":7.0,"remote_friendly":4.5,"autonomy":4.5,
            "family_friendly":6.5,"fulfillment":5.5,"entrepreneurship":2.0,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":6.0,"physical_demand":0.5,"license_barrier":7.5,
            "cycle_sensitivity":2.0,"side_job_compat":1.5,"intl_mobility":4.0,"industry_monopoly":7.0,
            "trend_long":0,"trend_short":0,"edu":"本科/硕士","age":"23-30",
        },
        "0105": {  # Tax Official
            "learning_cost":5.5,"education_req":6.0,"growth_coeff":3.5,"career_lifespan":9.0,
            "opportunity":5.0,"market_size":5.5,"supply_demand":4.0,"developed_scarcity":3.5,
            "value_added":5.5,"cost_performance":5.5,"stability":9.5,"safety":9.0,
            "occupational_disease":7.5,"overtime":6.5,"burnout":5.5,
            "skill_versatility":4.5,"career_switch":4.0,"reputation_variance":3.0,
            "ai_resistance":4.5,"social_status":6.5,"remote_friendly":4.0,"autonomy":4.0,
            "family_friendly":6.5,"fulfillment":5.0,"entrepreneurship":1.5,"gender_equality":5.5,
            "age_flexibility":7.5,"social_interaction":6.5,"physical_demand":1.0,"license_barrier":8.0,
            "cycle_sensitivity":1.5,"side_job_compat":1.0,"intl_mobility":3.0,"industry_monopoly":8.0,
            "trend_long":-1,"trend_short":-1,"edu":"本科","age":"22-28",
        },
        "0106": {  # Legislative Assistant / Policy Advisor
            "learning_cost":6.5,"education_req":7.5,"growth_coeff":5.0,"career_lifespan":7.5,
            "opportunity":4.0,"market_size":3.0,"supply_demand":4.5,"developed_scarcity":4.5,
            "value_added":6.5,"cost_performance":5.0,"stability":7.0,"safety":9.5,
            "occupational_disease":7.0,"overtime":5.5,"burnout":5.0,
            "skill_versatility":6.5,"career_switch":6.0,"reputation_variance":2.0,
            "ai_resistance":6.0,"social_status":7.5,"remote_friendly":4.5,"autonomy":5.0,
            "family_friendly":5.5,"fulfillment":7.0,"entrepreneurship":3.0,"gender_equality":5.5,
            "age_flexibility":6.0,"social_interaction":8.0,"physical_demand":0.5,"license_barrier":7.0,
            "cycle_sensitivity":3.0,"side_job_compat":2.0,"intl_mobility":5.0,"industry_monopoly":7.0,
            "trend_long":0,"trend_short":1,"edu":"硕士","age":"25-32",
        },
        "0107": {  # Government Spokesperson / Press Secretary
            "learning_cost":5.5,"education_req":6.5,"growth_coeff":4.5,"career_lifespan":7.0,
            "opportunity":3.5,"market_size":2.5,"supply_demand":4.0,"developed_scarcity":4.5,
            "value_added":6.0,"cost_performance":5.0,"stability":6.5,"safety":8.0,
            "occupational_disease":6.5,"overtime":4.5,"burnout":4.5,
            "skill_versatility":6.5,"career_switch":6.5,"reputation_variance":3.5,
            "ai_resistance":6.5,"social_status":7.5,"remote_friendly":3.5,"autonomy":4.5,
            "family_friendly":4.5,"fulfillment":6.5,"entrepreneurship":3.5,"gender_equality":5.5,
            "age_flexibility":5.5,"social_interaction":9.5,"physical_demand":1.0,"license_barrier":6.0,
            "cycle_sensitivity":3.0,"side_job_compat":2.0,"intl_mobility":4.5,"industry_monopoly":7.5,
            "trend_long":0,"trend_short":0,"edu":"本科/硕士","age":"26-35",
        },
        # ===== LOCAL CIVIL SERVICE =====
        "0201": {  # Local Government Officer
            "learning_cost":5.0,"education_req":5.5,"growth_coeff":3.5,"career_lifespan":9.0,
            "opportunity":5.0,"market_size":7.0,"supply_demand":3.0,"developed_scarcity":2.5,
            "value_added":4.5,"cost_performance":5.0,"stability":9.0,"safety":9.0,
            "occupational_disease":7.5,"overtime":6.5,"burnout":6.0,
            "skill_versatility":5.0,"career_switch":3.5,"reputation_variance":2.5,
            "ai_resistance":6.0,"social_status":7.0,"remote_friendly":2.5,"autonomy":3.5,
            "family_friendly":6.5,"fulfillment":5.5,"entrepreneurship":1.5,"gender_equality":5.5,
            "age_flexibility":7.5,"social_interaction":7.5,"physical_demand":1.5,"license_barrier":8.0,
            "cycle_sensitivity":1.5,"side_job_compat":1.0,"intl_mobility":2.0,"industry_monopoly":8.0,
            "trend_long":0,"trend_short":0,"edu":"本科","age":"22-28",
        },
        "0202": {  # Chengguan
            "learning_cost":3.0,"education_req":3.5,"growth_coeff":2.0,"career_lifespan":7.5,
            "opportunity":4.0,"market_size":4.0,"supply_demand":3.0,"developed_scarcity":1.5,
            "value_added":3.0,"cost_performance":4.0,"stability":7.5,"safety":6.0,
            "occupational_disease":5.5,"overtime":5.5,"burnout":4.5,
            "skill_versatility":3.0,"career_switch":3.0,"reputation_variance":4.5,
            "ai_resistance":5.5,"social_status":3.5,"remote_friendly":1.0,"autonomy":3.5,
            "family_friendly":5.0,"fulfillment":3.5,"entrepreneurship":1.0,"gender_equality":4.0,
            "age_flexibility":6.5,"social_interaction":7.5,"physical_demand":6.0,"license_barrier":5.0,
            "cycle_sensitivity":1.5,"side_job_compat":1.0,"intl_mobility":1.0,"industry_monopoly":7.0,
            "trend_long":-1,"trend_short":-1,"edu":"高中/大专","age":"20-30",
        },
        "0203": {  # Civil Affairs Officer
            "learning_cost":4.5,"education_req":5.0,"growth_coeff":3.5,"career_lifespan":8.5,
            "opportunity":4.5,"market_size":5.5,"supply_demand":3.5,"developed_scarcity":2.5,
            "value_added":4.5,"cost_performance":5.0,"stability":8.5,"safety":9.0,
            "occupational_disease":7.5,"overtime":6.5,"burnout":6.0,
            "skill_versatility":5.0,"career_switch":3.5,"reputation_variance":2.0,
            "ai_resistance":6.0,"social_status":6.0,"remote_friendly":2.5,"autonomy":3.5,
            "family_friendly":6.5,"fulfillment":6.5,"entrepreneurship":1.5,"gender_equality":5.5,
            "age_flexibility":7.5,"social_interaction":8.0,"physical_demand":2.0,"license_barrier":7.0,
            "cycle_sensitivity":1.5,"side_job_compat":1.0,"intl_mobility":2.0,"industry_monopoly":7.5,
            "trend_long":0,"trend_short":0,"edu":"本科","age":"22-28",
        },
        "0204": {  # Community/Street Office Official
            "learning_cost":3.5,"education_req":4.0,"growth_coeff":3.0,"career_lifespan":8.0,
            "opportunity":5.0,"market_size":6.0,"supply_demand":3.0,"developed_scarcity":2.0,
            "value_added":3.5,"cost_performance":4.5,"stability":8.0,"safety":8.5,
            "occupational_disease":7.0,"overtime":5.5,"burnout":5.5,
            "skill_versatility":4.5,"career_switch":3.5,"reputation_variance":2.5,
            "ai_resistance":6.0,"social_status":5.0,"remote_friendly":2.0,"autonomy":3.0,
            "family_friendly":6.0,"fulfillment":5.5,"entrepreneurship":1.5,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":8.5,"physical_demand":2.5,"license_barrier":5.5,
            "cycle_sensitivity":1.5,"side_job_compat":1.0,"intl_mobility":1.5,"industry_monopoly":7.5,
            "trend_long":0,"trend_short":0,"edu":"大专/本科","age":"22-30",
        },
        "0205": {  # Mayor / District Governor
            "learning_cost":7.0,"education_req":7.5,"growth_coeff":5.5,"career_lifespan":7.0,
            "opportunity":2.0,"market_size":2.0,"supply_demand":3.0,"developed_scarcity":3.0,
            "value_added":7.5,"cost_performance":5.0,"stability":6.0,"safety":7.5,
            "occupational_disease":6.0,"overtime":4.0,"burnout":4.0,
            "skill_versatility":7.0,"career_switch":5.5,"reputation_variance":4.0,
            "ai_resistance":8.0,"social_status":9.0,"remote_friendly":1.5,"autonomy":7.5,
            "family_friendly":3.5,"fulfillment":8.0,"entrepreneurship":2.0,"gender_equality":4.5,
            "age_flexibility":5.0,"social_interaction":9.5,"physical_demand":2.0,"license_barrier":9.0,
            "cycle_sensitivity":3.0,"side_job_compat":0.5,"intl_mobility":3.5,"industry_monopoly":9.0,
            "trend_long":0,"trend_short":0,"edu":"硕士/博士","age":"35-50",
        },
        "0206": {  # Planning & Zoning Officer
            "learning_cost":5.5,"education_req":6.0,"growth_coeff":4.0,"career_lifespan":8.5,
            "opportunity":4.5,"market_size":4.5,"supply_demand":4.0,"developed_scarcity":3.5,
            "value_added":5.5,"cost_performance":5.5,"stability":8.5,"safety":9.5,
            "occupational_disease":7.5,"overtime":6.5,"burnout":5.5,
            "skill_versatility":5.0,"career_switch":4.5,"reputation_variance":2.5,
            "ai_resistance":5.5,"social_status":6.5,"remote_friendly":3.5,"autonomy":4.5,
            "family_friendly":6.5,"fulfillment":6.0,"entrepreneurship":2.0,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":6.5,"physical_demand":2.0,"license_barrier":7.5,
            "cycle_sensitivity":2.0,"side_job_compat":1.5,"intl_mobility":3.0,"industry_monopoly":7.5,
            "trend_long":0,"trend_short":0,"edu":"本科/硕士","age":"23-30",
        },
        "0207": {  # Public Health Inspector
            "learning_cost":5.0,"education_req":5.5,"growth_coeff":4.5,"career_lifespan":8.5,
            "opportunity":5.0,"market_size":5.0,"supply_demand":4.5,"developed_scarcity":3.5,
            "value_added":5.0,"cost_performance":5.5,"stability":8.5,"safety":7.5,
            "occupational_disease":6.0,"overtime":6.5,"burnout":5.5,
            "skill_versatility":5.0,"career_switch":4.5,"reputation_variance":2.0,
            "ai_resistance":6.0,"social_status":6.0,"remote_friendly":2.0,"autonomy":5.0,
            "family_friendly":6.0,"fulfillment":6.5,"entrepreneurship":2.0,"gender_equality":6.0,
            "age_flexibility":7.0,"social_interaction":7.0,"physical_demand":3.5,"license_barrier":7.0,
            "cycle_sensitivity":1.5,"side_job_compat":1.5,"intl_mobility":3.5,"industry_monopoly":7.0,
            "trend_long":1,"trend_short":1,"edu":"本科","age":"22-28",
        },
        # ===== JUDICIAL ADMIN =====
        "0301": {  # Court Clerk
            "learning_cost":4.5,"education_req":5.0,"growth_coeff":3.0,"career_lifespan":8.5,
            "opportunity":4.5,"market_size":4.5,"supply_demand":3.5,"developed_scarcity":3.0,
            "value_added":4.5,"cost_performance":5.0,"stability":9.0,"safety":8.5,
            "occupational_disease":7.0,"overtime":6.5,"burnout":5.5,
            "skill_versatility":4.0,"career_switch":4.0,"reputation_variance":1.5,
            "ai_resistance":4.5,"social_status":5.5,"remote_friendly":3.0,"autonomy":3.5,
            "family_friendly":6.5,"fulfillment":5.0,"entrepreneurship":1.0,"gender_equality":6.0,
            "age_flexibility":7.5,"social_interaction":6.0,"physical_demand":1.0,"license_barrier":7.0,
            "cycle_sensitivity":1.0,"side_job_compat":1.0,"intl_mobility":2.5,"industry_monopoly":8.0,
            "trend_long":-1,"trend_short":-1,"edu":"本科","age":"22-28",
        },
        "0302": {  # Court Marshal / Bailiff
            "learning_cost":4.0,"education_req":4.5,"growth_coeff":2.5,"career_lifespan":7.5,
            "opportunity":4.0,"market_size":3.5,"supply_demand":3.5,"developed_scarcity":3.0,
            "value_added":4.0,"cost_performance":4.5,"stability":8.5,"safety":6.5,
            "occupational_disease":5.5,"overtime":6.0,"burnout":5.5,
            "skill_versatility":3.5,"career_switch":3.5,"reputation_variance":2.0,
            "ai_resistance":6.5,"social_status":5.0,"remote_friendly":1.0,"autonomy":3.5,
            "family_friendly":5.5,"fulfillment":5.0,"entrepreneurship":1.0,"gender_equality":4.5,
            "age_flexibility":6.0,"social_interaction":6.5,"physical_demand":5.0,"license_barrier":7.0,
            "cycle_sensitivity":1.0,"side_job_compat":1.0,"intl_mobility":2.0,"industry_monopoly":8.0,
            "trend_long":0,"trend_short":0,"edu":"大专/本科","age":"22-30",
        },
        "0303": {  # Corrections Officer
            "learning_cost":3.5,"education_req":4.0,"growth_coeff":2.5,"career_lifespan":7.0,
            "opportunity":4.5,"market_size":4.0,"supply_demand":4.5,"developed_scarcity":4.5,
            "value_added":4.0,"cost_performance":4.5,"stability":8.0,"safety":4.5,
            "occupational_disease":4.5,"overtime":5.5,"burnout":3.5,
            "skill_versatility":3.0,"career_switch":3.0,"reputation_variance":2.5,
            "ai_resistance":7.0,"social_status":4.0,"remote_friendly":0.5,"autonomy":3.0,
            "family_friendly":4.5,"fulfillment":4.5,"entrepreneurship":1.0,"gender_equality":4.0,
            "age_flexibility":5.5,"social_interaction":7.0,"physical_demand":6.0,"license_barrier":6.5,
            "cycle_sensitivity":1.0,"side_job_compat":1.0,"intl_mobility":2.0,"industry_monopoly":8.5,
            "trend_long":0,"trend_short":0,"edu":"高中/大专","age":"20-30",
        },
        "0304": {  # Probation / Parole Officer
            "learning_cost":5.0,"education_req":5.5,"growth_coeff":3.5,"career_lifespan":8.0,
            "opportunity":4.5,"market_size":3.5,"supply_demand":4.5,"developed_scarcity":4.0,
            "value_added":5.0,"cost_performance":5.0,"stability":8.0,"safety":6.5,
            "occupational_disease":5.5,"overtime":6.0,"burnout":4.5,
            "skill_versatility":5.0,"career_switch":4.5,"reputation_variance":2.0,
            "ai_resistance":6.5,"social_status":5.5,"remote_friendly":3.0,"autonomy":5.0,
            "family_friendly":5.5,"fulfillment":6.5,"entrepreneurship":1.5,"gender_equality":5.5,
            "age_flexibility":6.5,"social_interaction":8.0,"physical_demand":2.5,"license_barrier":7.0,
            "cycle_sensitivity":1.0,"side_job_compat":1.0,"intl_mobility":3.0,"industry_monopoly":8.0,
            "trend_long":0,"trend_short":0,"edu":"本科","age":"23-30",
        },
        # ===== PUBLIC INSTITUTIONS =====
        "0401": {  # Shiye Bian
            "learning_cost":5.0,"education_req":5.5,"growth_coeff":3.5,"career_lifespan":8.5,
            "opportunity":5.5,"market_size":6.5,"supply_demand":3.0,"developed_scarcity":2.5,
            "value_added":4.5,"cost_performance":5.5,"stability":8.0,"safety":9.0,
            "occupational_disease":7.5,"overtime":6.5,"burnout":6.0,
            "skill_versatility":5.0,"career_switch":4.0,"reputation_variance":2.0,
            "ai_resistance":5.5,"social_status":6.0,"remote_friendly":3.0,"autonomy":4.0,
            "family_friendly":6.5,"fulfillment":5.5,"entrepreneurship":2.0,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":6.5,"physical_demand":1.5,"license_barrier":7.0,
            "cycle_sensitivity":1.5,"side_job_compat":2.0,"intl_mobility":2.0,"industry_monopoly":7.0,
            "trend_long":0,"trend_short":-1,"edu":"本科/硕士","age":"22-30",
        },
        "0402": {  # Public Library Director
            "learning_cost":5.5,"education_req":6.5,"growth_coeff":3.0,"career_lifespan":8.5,
            "opportunity":3.5,"market_size":3.0,"supply_demand":3.5,"developed_scarcity":3.5,
            "value_added":4.5,"cost_performance":4.5,"stability":8.5,"safety":9.5,
            "occupational_disease":7.5,"overtime":7.5,"burnout":7.0,
            "skill_versatility":5.0,"career_switch":4.5,"reputation_variance":1.5,
            "ai_resistance":6.0,"social_status":6.0,"remote_friendly":3.5,"autonomy":6.0,
            "family_friendly":7.5,"fulfillment":7.0,"entrepreneurship":2.0,"gender_equality":7.0,
            "age_flexibility":8.0,"social_interaction":6.5,"physical_demand":1.5,"license_barrier":6.5,
            "cycle_sensitivity":1.0,"side_job_compat":2.5,"intl_mobility":3.5,"industry_monopoly":7.0,
            "trend_long":-1,"trend_short":-1,"edu":"硕士","age":"28-40",
        },
        "0403": {  # Government Statistician
            "learning_cost":6.5,"education_req":7.0,"growth_coeff":4.5,"career_lifespan":8.5,
            "opportunity":4.5,"market_size":3.5,"supply_demand":5.0,"developed_scarcity":4.5,
            "value_added":5.5,"cost_performance":5.5,"stability":8.5,"safety":9.5,
            "occupational_disease":7.5,"overtime":6.5,"burnout":5.5,
            "skill_versatility":6.0,"career_switch":5.5,"reputation_variance":1.5,
            "ai_resistance":4.5,"social_status":6.5,"remote_friendly":5.5,"autonomy":5.5,
            "family_friendly":7.0,"fulfillment":6.0,"entrepreneurship":2.5,"gender_equality":6.0,
            "age_flexibility":7.0,"social_interaction":5.0,"physical_demand":0.5,"license_barrier":7.0,
            "cycle_sensitivity":1.5,"side_job_compat":2.5,"intl_mobility":5.0,"industry_monopoly":7.0,
            "trend_long":1,"trend_short":1,"edu":"硕士","age":"24-30",
        },
        "0404": {  # Meteorologist
            "learning_cost":7.0,"education_req":7.5,"growth_coeff":4.5,"career_lifespan":8.5,
            "opportunity":3.5,"market_size":3.0,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":5.5,"cost_performance":5.0,"stability":8.5,"safety":9.0,
            "occupational_disease":7.0,"overtime":6.0,"burnout":5.5,
            "skill_versatility":4.5,"career_switch":4.0,"reputation_variance":1.5,
            "ai_resistance":5.5,"social_status":6.5,"remote_friendly":5.0,"autonomy":5.5,
            "family_friendly":6.5,"fulfillment":7.0,"entrepreneurship":2.0,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":5.0,"physical_demand":2.0,"license_barrier":7.5,
            "cycle_sensitivity":1.0,"side_job_compat":2.0,"intl_mobility":5.5,"industry_monopoly":7.5,
            "trend_long":1,"trend_short":2,"edu":"硕士/博士","age":"24-30",
        },
        # ===== INTERNATIONAL ORG =====
        "0501": {  # UN Staff
            "learning_cost":7.5,"education_req":8.5,"growth_coeff":4.5,"career_lifespan":8.0,
            "opportunity":2.5,"market_size":1.5,"supply_demand":3.5,"developed_scarcity":3.5,
            "value_added":8.0,"cost_performance":6.0,"stability":8.0,"safety":7.5,
            "occupational_disease":7.0,"overtime":5.5,"burnout":5.5,
            "skill_versatility":6.5,"career_switch":5.0,"reputation_variance":1.5,
            "ai_resistance":7.0,"social_status":9.0,"remote_friendly":4.5,"autonomy":5.5,
            "family_friendly":5.0,"fulfillment":8.5,"entrepreneurship":1.5,"gender_equality":7.5,
            "age_flexibility":5.5,"social_interaction":8.5,"physical_demand":1.5,"license_barrier":8.5,
            "cycle_sensitivity":2.0,"side_job_compat":1.0,"intl_mobility":9.5,"industry_monopoly":8.0,
            "trend_long":0,"trend_short":0,"edu":"硕士/博士","age":"27-35",
        },
        "0502": {  # Intl Org Program Officer
            "learning_cost":7.0,"education_req":8.0,"growth_coeff":5.0,"career_lifespan":7.5,
            "opportunity":3.5,"market_size":2.0,"supply_demand":4.5,"developed_scarcity":4.5,
            "value_added":7.5,"cost_performance":6.0,"stability":7.0,"safety":7.5,
            "occupational_disease":7.0,"overtime":5.5,"burnout":5.0,
            "skill_versatility":7.0,"career_switch":5.5,"reputation_variance":1.5,
            "ai_resistance":6.5,"social_status":8.0,"remote_friendly":5.0,"autonomy":6.0,
            "family_friendly":5.0,"fulfillment":8.0,"entrepreneurship":2.5,"gender_equality":7.5,
            "age_flexibility":5.5,"social_interaction":8.0,"physical_demand":2.0,"license_barrier":7.5,
            "cycle_sensitivity":2.5,"side_job_compat":1.5,"intl_mobility":9.5,"industry_monopoly":7.0,
            "trend_long":1,"trend_short":1,"edu":"硕士","age":"26-34",
        },
        "0503": {  # Intl Development Advisor
            "learning_cost":7.0,"education_req":8.0,"growth_coeff":5.0,"career_lifespan":7.5,
            "opportunity":3.5,"market_size":2.0,"supply_demand":5.0,"developed_scarcity":5.0,
            "value_added":7.5,"cost_performance":5.5,"stability":6.5,"safety":6.5,
            "occupational_disease":6.5,"overtime":5.5,"burnout":5.0,
            "skill_versatility":7.0,"career_switch":6.0,"reputation_variance":2.0,
            "ai_resistance":7.0,"social_status":8.0,"remote_friendly":5.5,"autonomy":6.5,
            "family_friendly":4.0,"fulfillment":8.5,"entrepreneurship":3.5,"gender_equality":7.0,
            "age_flexibility":5.5,"social_interaction":8.5,"physical_demand":3.0,"license_barrier":7.0,
            "cycle_sensitivity":3.0,"side_job_compat":2.0,"intl_mobility":9.5,"industry_monopoly":6.0,
            "trend_long":1,"trend_short":1,"edu":"硕士/博士","age":"28-38",
        },
        "0504": {  # Intl Org Translator/Interpreter
            "learning_cost":7.0,"education_req":7.5,"growth_coeff":4.0,"career_lifespan":7.0,
            "opportunity":3.0,"market_size":2.0,"supply_demand":4.5,"developed_scarcity":5.0,
            "value_added":7.0,"cost_performance":5.5,"stability":7.0,"safety":9.0,
            "occupational_disease":6.5,"overtime":5.5,"burnout":5.5,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":1.5,
            "ai_resistance":4.5,"social_status":7.5,"remote_friendly":5.5,"autonomy":5.0,
            "family_friendly":5.0,"fulfillment":7.0,"entrepreneurship":3.5,"gender_equality":7.0,
            "age_flexibility":5.5,"social_interaction":8.0,"physical_demand":1.0,"license_barrier":8.0,
            "cycle_sensitivity":2.0,"side_job_compat":3.5,"intl_mobility":9.0,"industry_monopoly":6.5,
            "trend_long":-1,"trend_short":-2,"edu":"硕士","age":"25-32",
        },
        # ===== MILITARY =====
        "0601": {  # Military Officer
            "learning_cost":7.0,"education_req":7.0,"growth_coeff":4.5,"career_lifespan":7.5,
            "opportunity":3.5,"market_size":3.0,"supply_demand":4.5,"developed_scarcity":4.0,
            "value_added":6.5,"cost_performance":5.5,"stability":8.5,"safety":3.5,
            "occupational_disease":4.0,"overtime":3.5,"burnout":4.0,
            "skill_versatility":5.5,"career_switch":4.5,"reputation_variance":2.5,
            "ai_resistance":7.5,"social_status":8.5,"remote_friendly":0.5,"autonomy":4.5,
            "family_friendly":3.0,"fulfillment":7.5,"entrepreneurship":1.0,"gender_equality":3.5,
            "age_flexibility":4.0,"social_interaction":7.5,"physical_demand":7.0,"license_barrier":8.5,
            "cycle_sensitivity":1.5,"side_job_compat":0.5,"intl_mobility":3.5,"industry_monopoly":9.5,
            "trend_long":0,"trend_short":1,"edu":"本科/军校","age":"18-25",
        },
        "0602": {  # Enlisted Soldier / NCO
            "learning_cost":3.5,"education_req":3.0,"growth_coeff":3.0,"career_lifespan":6.0,
            "opportunity":5.0,"market_size":5.0,"supply_demand":4.0,"developed_scarcity":4.0,
            "value_added":3.5,"cost_performance":4.5,"stability":7.5,"safety":3.0,
            "occupational_disease":3.5,"overtime":2.5,"burnout":3.5,
            "skill_versatility":4.0,"career_switch":3.5,"reputation_variance":3.0,
            "ai_resistance":7.0,"social_status":5.5,"remote_friendly":0.5,"autonomy":2.0,
            "family_friendly":2.5,"fulfillment":6.0,"entrepreneurship":1.0,"gender_equality":3.0,
            "age_flexibility":3.0,"social_interaction":7.0,"physical_demand":9.0,"license_barrier":5.0,
            "cycle_sensitivity":1.5,"side_job_compat":0.5,"intl_mobility":2.5,"industry_monopoly":9.5,
            "trend_long":0,"trend_short":0,"edu":"高中/大专","age":"18-22",
        },
        "0603": {  # Military Intelligence Analyst
            "learning_cost":7.5,"education_req":7.5,"growth_coeff":5.5,"career_lifespan":7.5,
            "opportunity":3.5,"market_size":2.0,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":7.5,"cost_performance":6.0,"stability":8.5,"safety":5.0,
            "occupational_disease":5.5,"overtime":4.0,"burnout":4.5,
            "skill_versatility":6.0,"career_switch":5.0,"reputation_variance":1.5,
            "ai_resistance":6.5,"social_status":7.5,"remote_friendly":3.0,"autonomy":4.5,
            "family_friendly":3.5,"fulfillment":7.5,"entrepreneurship":1.5,"gender_equality":4.0,
            "age_flexibility":5.0,"social_interaction":5.5,"physical_demand":3.0,"license_barrier":9.0,
            "cycle_sensitivity":1.5,"side_job_compat":0.5,"intl_mobility":3.0,"industry_monopoly":9.5,
            "trend_long":1,"trend_short":2,"edu":"本科/硕士","age":"22-28",
        },
        "0604": {  # Military Physician
            "learning_cost":9.0,"education_req":9.0,"growth_coeff":5.0,"career_lifespan":8.0,
            "opportunity":3.5,"market_size":2.5,"supply_demand":6.0,"developed_scarcity":6.0,
            "value_added":7.5,"cost_performance":5.5,"stability":9.0,"safety":5.0,
            "occupational_disease":5.0,"overtime":4.5,"burnout":4.5,
            "skill_versatility":7.0,"career_switch":6.5,"reputation_variance":1.0,
            "ai_resistance":7.5,"social_status":8.5,"remote_friendly":1.0,"autonomy":5.5,
            "family_friendly":3.5,"fulfillment":8.5,"entrepreneurship":2.0,"gender_equality":5.0,
            "age_flexibility":5.5,"social_interaction":7.5,"physical_demand":5.0,"license_barrier":9.5,
            "cycle_sensitivity":0.5,"side_job_compat":1.0,"intl_mobility":5.0,"industry_monopoly":9.0,
            "trend_long":0,"trend_short":1,"edu":"医学本科+","age":"24-30",
        },
        "0605": {  # Military Engineer
            "learning_cost":7.5,"education_req":7.0,"growth_coeff":5.0,"career_lifespan":7.5,
            "opportunity":3.5,"market_size":2.5,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":7.0,"cost_performance":5.5,"stability":8.5,"safety":4.5,
            "occupational_disease":5.0,"overtime":4.0,"burnout":4.5,
            "skill_versatility":6.5,"career_switch":5.5,"reputation_variance":1.5,
            "ai_resistance":6.5,"social_status":7.5,"remote_friendly":1.5,"autonomy":4.5,
            "family_friendly":3.5,"fulfillment":7.0,"entrepreneurship":2.0,"gender_equality":3.5,
            "age_flexibility":5.0,"social_interaction":6.0,"physical_demand":5.0,"license_barrier":8.5,
            "cycle_sensitivity":1.0,"side_job_compat":0.5,"intl_mobility":3.5,"industry_monopoly":9.5,
            "trend_long":1,"trend_short":2,"edu":"本科/硕士","age":"22-28",
        },
        # ===== POLICE & LAW ENFORCEMENT =====
        "0701": {  # Police Officer
            "learning_cost":4.5,"education_req":4.5,"growth_coeff":3.5,"career_lifespan":7.5,
            "opportunity":5.5,"market_size":6.5,"supply_demand":4.5,"developed_scarcity":4.0,
            "value_added":5.0,"cost_performance":5.0,"stability":8.5,"safety":4.0,
            "occupational_disease":4.0,"overtime":4.0,"burnout":3.5,
            "skill_versatility":4.5,"career_switch":3.5,"reputation_variance":3.5,
            "ai_resistance":7.0,"social_status":6.5,"remote_friendly":0.5,"autonomy":4.0,
            "family_friendly":4.0,"fulfillment":6.5,"entrepreneurship":1.0,"gender_equality":4.0,
            "age_flexibility":5.0,"social_interaction":8.0,"physical_demand":7.0,"license_barrier":7.5,
            "cycle_sensitivity":1.0,"side_job_compat":1.0,"intl_mobility":2.5,"industry_monopoly":9.0,
            "trend_long":0,"trend_short":0,"edu":"大专/本科","age":"20-28",
        },
        "0702": {  # Detective
            "learning_cost":6.0,"education_req":5.5,"growth_coeff":4.0,"career_lifespan":7.5,
            "opportunity":4.5,"market_size":4.0,"supply_demand":5.0,"developed_scarcity":4.5,
            "value_added":6.0,"cost_performance":5.5,"stability":8.0,"safety":4.5,
            "occupational_disease":4.5,"overtime":3.5,"burnout":3.5,
            "skill_versatility":5.5,"career_switch":4.5,"reputation_variance":2.5,
            "ai_resistance":7.0,"social_status":7.0,"remote_friendly":1.5,"autonomy":5.5,
            "family_friendly":3.5,"fulfillment":7.5,"entrepreneurship":2.0,"gender_equality":4.0,
            "age_flexibility":5.5,"social_interaction":7.5,"physical_demand":5.5,"license_barrier":8.0,
            "cycle_sensitivity":1.0,"side_job_compat":1.0,"intl_mobility":3.0,"industry_monopoly":9.0,
            "trend_long":0,"trend_short":0,"edu":"本科","age":"22-30",
        },
        "0703": {  # Auxiliary Police
            "learning_cost":2.5,"education_req":2.5,"growth_coeff":2.0,"career_lifespan":6.0,
            "opportunity":5.5,"market_size":5.0,"supply_demand":3.0,"developed_scarcity":2.0,
            "value_added":2.5,"cost_performance":3.5,"stability":5.5,"safety":4.5,
            "occupational_disease":4.5,"overtime":4.0,"burnout":4.0,
            "skill_versatility":3.0,"career_switch":3.0,"reputation_variance":3.5,
            "ai_resistance":5.5,"social_status":3.5,"remote_friendly":0.5,"autonomy":2.5,
            "family_friendly":4.0,"fulfillment":4.0,"entrepreneurship":1.0,"gender_equality":4.0,
            "age_flexibility":5.5,"social_interaction":7.0,"physical_demand":6.5,"license_barrier":4.0,
            "cycle_sensitivity":2.0,"side_job_compat":1.5,"intl_mobility":1.5,"industry_monopoly":7.5,
            "trend_long":-1,"trend_short":-1,"edu":"高中/大专","age":"18-28",
        },
        "0704": {  # Traffic Police
            "learning_cost":4.0,"education_req":4.0,"growth_coeff":3.0,"career_lifespan":7.0,
            "opportunity":5.0,"market_size":5.5,"supply_demand":4.0,"developed_scarcity":3.5,
            "value_added":4.5,"cost_performance":4.5,"stability":8.5,"safety":5.0,
            "occupational_disease":4.5,"overtime":4.5,"burnout":4.0,
            "skill_versatility":3.5,"career_switch":3.0,"reputation_variance":3.0,
            "ai_resistance":5.5,"social_status":5.5,"remote_friendly":0.5,"autonomy":3.5,
            "family_friendly":4.5,"fulfillment":5.0,"entrepreneurship":1.0,"gender_equality":4.0,
            "age_flexibility":5.5,"social_interaction":7.5,"physical_demand":6.0,"license_barrier":7.0,
            "cycle_sensitivity":1.0,"side_job_compat":1.0,"intl_mobility":2.0,"industry_monopoly":8.5,
            "trend_long":-1,"trend_short":-1,"edu":"大专/本科","age":"20-28",
        },
        "0705": {  # Cybercrime Police
            "learning_cost":6.5,"education_req":6.0,"growth_coeff":6.0,"career_lifespan":7.5,
            "opportunity":5.0,"market_size":3.5,"supply_demand":6.5,"developed_scarcity":6.0,
            "value_added":6.5,"cost_performance":5.5,"stability":8.0,"safety":8.0,
            "occupational_disease":6.5,"overtime":4.5,"burnout":4.5,
            "skill_versatility":6.5,"career_switch":5.5,"reputation_variance":2.0,
            "ai_resistance":5.5,"social_status":7.0,"remote_friendly":4.5,"autonomy":5.0,
            "family_friendly":5.0,"fulfillment":7.0,"entrepreneurship":2.0,"gender_equality":5.0,
            "age_flexibility":5.5,"social_interaction":5.5,"physical_demand":1.5,"license_barrier":8.0,
            "cycle_sensitivity":1.5,"side_job_compat":1.0,"intl_mobility":4.0,"industry_monopoly":8.5,
            "trend_long":2,"trend_short":3,"edu":"本科/硕士","age":"22-28",
        },
        "0706": {  # Customs Officer
            "learning_cost":5.0,"education_req":5.5,"growth_coeff":3.5,"career_lifespan":8.5,
            "opportunity":4.5,"market_size":4.0,"supply_demand":4.0,"developed_scarcity":3.5,
            "value_added":5.5,"cost_performance":5.5,"stability":9.0,"safety":7.0,
            "occupational_disease":6.5,"overtime":5.5,"burnout":5.0,
            "skill_versatility":4.5,"career_switch":4.0,"reputation_variance":2.5,
            "ai_resistance":5.0,"social_status":6.5,"remote_friendly":1.5,"autonomy":4.0,
            "family_friendly":5.5,"fulfillment":5.5,"entrepreneurship":1.0,"gender_equality":5.0,
            "age_flexibility":6.5,"social_interaction":6.5,"physical_demand":3.0,"license_barrier":8.0,
            "cycle_sensitivity":2.0,"side_job_compat":0.5,"intl_mobility":4.5,"industry_monopoly":8.5,
            "trend_long":0,"trend_short":0,"edu":"本科","age":"22-28",
        },
        "0707": {  # Border Patrol
            "learning_cost":4.0,"education_req":4.0,"growth_coeff":3.0,"career_lifespan":7.0,
            "opportunity":4.5,"market_size":4.0,"supply_demand":4.5,"developed_scarcity":4.0,
            "value_added":4.5,"cost_performance":4.5,"stability":8.5,"safety":4.5,
            "occupational_disease":4.5,"overtime":4.0,"burnout":4.0,
            "skill_versatility":3.5,"career_switch":3.0,"reputation_variance":2.5,
            "ai_resistance":6.5,"social_status":5.5,"remote_friendly":0.5,"autonomy":3.5,
            "family_friendly":3.5,"fulfillment":6.0,"entrepreneurship":1.0,"gender_equality":3.5,
            "age_flexibility":5.0,"social_interaction":6.5,"physical_demand":7.5,"license_barrier":7.5,
            "cycle_sensitivity":1.5,"side_job_compat":0.5,"intl_mobility":2.5,"industry_monopoly":9.0,
            "trend_long":0,"trend_short":1,"edu":"高中/大专","age":"18-28",
        },
        # ===== FIRE & EMERGENCY =====
        "0801": {  # Firefighter
            "learning_cost":4.5,"education_req":4.0,"growth_coeff":3.5,"career_lifespan":6.5,
            "opportunity":5.0,"market_size":5.5,"supply_demand":4.5,"developed_scarcity":4.0,
            "value_added":4.5,"cost_performance":5.0,"stability":8.5,"safety":3.0,
            "occupational_disease":3.0,"overtime":4.5,"burnout":4.0,
            "skill_versatility":4.0,"career_switch":3.5,"reputation_variance":1.0,
            "ai_resistance":8.0,"social_status":7.5,"remote_friendly":0.5,"autonomy":3.5,
            "family_friendly":3.5,"fulfillment":8.5,"entrepreneurship":1.0,"gender_equality":3.0,
            "age_flexibility":4.0,"social_interaction":7.5,"physical_demand":9.0,"license_barrier":7.0,
            "cycle_sensitivity":0.5,"side_job_compat":1.5,"intl_mobility":3.0,"industry_monopoly":9.0,
            "trend_long":0,"trend_short":0,"edu":"高中/大专","age":"18-25",
        },
        "0802": {  # Fire Captain
            "learning_cost":6.0,"education_req":5.5,"growth_coeff":4.0,"career_lifespan":7.0,
            "opportunity":3.5,"market_size":3.0,"supply_demand":5.0,"developed_scarcity":4.5,
            "value_added":6.0,"cost_performance":5.5,"stability":8.5,"safety":3.5,
            "occupational_disease":3.5,"overtime":4.0,"burnout":4.0,
            "skill_versatility":5.0,"career_switch":4.5,"reputation_variance":1.0,
            "ai_resistance":8.0,"social_status":8.0,"remote_friendly":0.5,"autonomy":5.5,
            "family_friendly":3.5,"fulfillment":8.5,"entrepreneurship":1.5,"gender_equality":3.0,
            "age_flexibility":4.5,"social_interaction":8.0,"physical_demand":8.0,"license_barrier":7.5,
            "cycle_sensitivity":0.5,"side_job_compat":1.0,"intl_mobility":3.0,"industry_monopoly":9.0,
            "trend_long":0,"trend_short":0,"edu":"大专/本科","age":"25-35",
        },
        "0803": {  # Emergency Management Specialist
            "learning_cost":5.5,"education_req":6.0,"growth_coeff":5.5,"career_lifespan":8.0,
            "opportunity":5.0,"market_size":4.0,"supply_demand":5.5,"developed_scarcity":5.0,
            "value_added":6.0,"cost_performance":5.5,"stability":7.5,"safety":6.5,
            "occupational_disease":5.5,"overtime":5.0,"burnout":4.5,
            "skill_versatility":6.5,"career_switch":5.5,"reputation_variance":1.5,
            "ai_resistance":6.5,"social_status":6.5,"remote_friendly":4.0,"autonomy":5.5,
            "family_friendly":4.5,"fulfillment":7.5,"entrepreneurship":3.0,"gender_equality":5.5,
            "age_flexibility":6.0,"social_interaction":7.5,"physical_demand":4.0,"license_barrier":6.5,
            "cycle_sensitivity":2.0,"side_job_compat":2.0,"intl_mobility":5.5,"industry_monopoly":7.0,
            "trend_long":2,"trend_short":2,"edu":"本科/硕士","age":"24-32",
        },
        "0804": {  # Disaster Relief Coordinator
            "learning_cost":5.5,"education_req":6.0,"growth_coeff":5.0,"career_lifespan":7.5,
            "opportunity":4.0,"market_size":3.0,"supply_demand":5.0,"developed_scarcity":5.0,
            "value_added":5.5,"cost_performance":5.0,"stability":7.0,"safety":5.5,
            "occupational_disease":5.0,"overtime":4.5,"burnout":4.5,
            "skill_versatility":6.5,"career_switch":5.5,"reputation_variance":1.5,
            "ai_resistance":7.0,"social_status":7.0,"remote_friendly":3.5,"autonomy":6.0,
            "family_friendly":3.5,"fulfillment":8.5,"entrepreneurship":2.5,"gender_equality":6.0,
            "age_flexibility":5.5,"social_interaction":8.5,"physical_demand":5.0,"license_barrier":6.0,
            "cycle_sensitivity":2.5,"side_job_compat":2.0,"intl_mobility":7.5,"industry_monopoly":6.5,
            "trend_long":2,"trend_short":2,"edu":"本科/硕士","age":"25-35",
        },
        # ===== INTELLIGENCE & SECURITY =====
        "0901": {  # Intelligence Analyst
            "learning_cost":7.0,"education_req":7.5,"growth_coeff":5.5,"career_lifespan":7.5,
            "opportunity":3.5,"market_size":2.5,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":7.5,"cost_performance":6.0,"stability":8.0,"safety":6.0,
            "occupational_disease":5.5,"overtime":4.5,"burnout":4.5,
            "skill_versatility":6.0,"career_switch":5.0,"reputation_variance":2.0,
            "ai_resistance":6.0,"social_status":7.5,"remote_friendly":3.5,"autonomy":5.0,
            "family_friendly":4.0,"fulfillment":7.5,"entrepreneurship":1.5,"gender_equality":4.5,
            "age_flexibility":5.5,"social_interaction":5.5,"physical_demand":1.5,"license_barrier":9.0,
            "cycle_sensitivity":1.5,"side_job_compat":0.5,"intl_mobility":3.5,"industry_monopoly":9.5,
            "trend_long":1,"trend_short":2,"edu":"硕士","age":"24-30",
        },
        "0902": {  # Govt Cybersecurity Analyst
            "learning_cost":7.0,"education_req":7.0,"growth_coeff":7.0,"career_lifespan":7.0,
            "opportunity":5.5,"market_size":3.5,"supply_demand":7.5,"developed_scarcity":7.0,
            "value_added":7.5,"cost_performance":6.0,"stability":8.0,"safety":9.0,
            "occupational_disease":6.5,"overtime":5.0,"burnout":5.0,
            "skill_versatility":7.0,"career_switch":6.0,"reputation_variance":1.5,
            "ai_resistance":5.5,"social_status":7.5,"remote_friendly":5.0,"autonomy":5.5,
            "family_friendly":5.5,"fulfillment":7.0,"entrepreneurship":3.0,"gender_equality":5.0,
            "age_flexibility":5.5,"social_interaction":5.0,"physical_demand":1.0,"license_barrier":8.0,
            "cycle_sensitivity":1.5,"side_job_compat":1.5,"intl_mobility":5.5,"industry_monopoly":8.0,
            "trend_long":3,"trend_short":4,"edu":"本科/硕士","age":"22-28",
        },
        "0903": {  # Counter-terrorism Specialist
            "learning_cost":7.5,"education_req":7.0,"growth_coeff":5.0,"career_lifespan":7.0,
            "opportunity":3.0,"market_size":2.0,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":7.5,"cost_performance":5.5,"stability":8.0,"safety":3.5,
            "occupational_disease":4.0,"overtime":3.5,"burnout":4.0,
            "skill_versatility":5.0,"career_switch":4.0,"reputation_variance":2.0,
            "ai_resistance":7.5,"social_status":7.5,"remote_friendly":1.0,"autonomy":4.5,
            "family_friendly":3.0,"fulfillment":8.0,"entrepreneurship":1.0,"gender_equality":3.5,
            "age_flexibility":4.0,"social_interaction":6.0,"physical_demand":7.5,"license_barrier":9.0,
            "cycle_sensitivity":2.0,"side_job_compat":0.5,"intl_mobility":4.0,"industry_monopoly":9.5,
            "trend_long":1,"trend_short":2,"edu":"本科/军校","age":"22-30",
        },
        "0904": {  # Govt Cryptographer
            "learning_cost":8.5,"education_req":8.5,"growth_coeff":6.0,"career_lifespan":7.5,
            "opportunity":3.0,"market_size":1.5,"supply_demand":7.0,"developed_scarcity":8.0,
            "value_added":8.5,"cost_performance":6.0,"stability":8.5,"safety":9.0,
            "occupational_disease":7.0,"overtime":5.5,"burnout":5.0,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":1.0,
            "ai_resistance":6.0,"social_status":8.0,"remote_friendly":4.5,"autonomy":6.0,
            "family_friendly":5.0,"fulfillment":7.5,"entrepreneurship":2.5,"gender_equality":4.5,
            "age_flexibility":5.0,"social_interaction":4.0,"physical_demand":0.5,"license_barrier":9.5,
            "cycle_sensitivity":1.0,"side_job_compat":1.0,"intl_mobility":4.5,"industry_monopoly":9.5,
            "trend_long":2,"trend_short":3,"edu":"硕士/博士","age":"24-30",
        },
        "0905": {  # Visa/Immigration Officer
            "learning_cost":4.5,"education_req":5.0,"growth_coeff":3.5,"career_lifespan":8.5,
            "opportunity":5.0,"market_size":5.0,"supply_demand":4.0,"developed_scarcity":3.5,
            "value_added":5.0,"cost_performance":5.0,"stability":8.5,"safety":7.5,
            "occupational_disease":7.0,"overtime":6.0,"burnout":5.5,
            "skill_versatility":4.5,"career_switch":4.0,"reputation_variance":2.5,
            "ai_resistance":5.0,"social_status":6.0,"remote_friendly":2.5,"autonomy":4.0,
            "family_friendly":5.5,"fulfillment":5.0,"entrepreneurship":1.0,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":7.5,"physical_demand":1.5,"license_barrier":7.5,
            "cycle_sensitivity":2.0,"side_job_compat":0.5,"intl_mobility":4.5,"industry_monopoly":8.5,
            "trend_long":0,"trend_short":0,"edu":"本科","age":"22-30",
        },
        "0906": {  # Environmental Enforcement Officer
            "learning_cost":5.0,"education_req":5.5,"growth_coeff":5.0,"career_lifespan":8.0,
            "opportunity":4.5,"market_size":4.0,"supply_demand":4.5,"developed_scarcity":4.0,
            "value_added":5.0,"cost_performance":5.0,"stability":8.0,"safety":7.0,
            "occupational_disease":5.5,"overtime":6.0,"burnout":5.5,
            "skill_versatility":5.0,"career_switch":4.5,"reputation_variance":2.0,
            "ai_resistance":6.0,"social_status":6.0,"remote_friendly":2.0,"autonomy":5.0,
            "family_friendly":5.5,"fulfillment":7.0,"entrepreneurship":2.0,"gender_equality":5.5,
            "age_flexibility":6.5,"social_interaction":6.5,"physical_demand":4.0,"license_barrier":7.0,
            "cycle_sensitivity":2.0,"side_job_compat":1.5,"intl_mobility":3.5,"industry_monopoly":7.5,
            "trend_long":2,"trend_short":2,"edu":"本科","age":"22-28",
        },
        "0907": {  # Food & Drug Inspector
            "learning_cost":5.5,"education_req":6.0,"growth_coeff":4.5,"career_lifespan":8.5,
            "opportunity":4.5,"market_size":4.5,"supply_demand":4.5,"developed_scarcity":4.0,
            "value_added":5.5,"cost_performance":5.5,"stability":8.5,"safety":7.5,
            "occupational_disease":6.0,"overtime":6.0,"burnout":5.5,
            "skill_versatility":5.0,"career_switch":4.5,"reputation_variance":2.0,
            "ai_resistance":5.5,"social_status":6.5,"remote_friendly":2.5,"autonomy":5.0,
            "family_friendly":6.0,"fulfillment":6.5,"entrepreneurship":2.0,"gender_equality":6.0,
            "age_flexibility":7.0,"social_interaction":6.5,"physical_demand":3.5,"license_barrier":7.5,
            "cycle_sensitivity":1.0,"side_job_compat":1.5,"intl_mobility":4.0,"industry_monopoly":7.5,
            "trend_long":1,"trend_short":1,"edu":"本科","age":"22-28",
        },
        "0908": {  # Labor Inspector
            "learning_cost":5.0,"education_req":5.5,"growth_coeff":4.0,"career_lifespan":8.5,
            "opportunity":4.5,"market_size":4.5,"supply_demand":4.0,"developed_scarcity":3.5,
            "value_added":5.0,"cost_performance":5.0,"stability":8.5,"safety":7.5,
            "occupational_disease":6.5,"overtime":6.5,"burnout":5.5,
            "skill_versatility":5.0,"career_switch":4.5,"reputation_variance":2.0,
            "ai_resistance":6.0,"social_status":6.0,"remote_friendly":2.5,"autonomy":5.0,
            "family_friendly":6.0,"fulfillment":6.0,"entrepreneurship":1.5,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":7.0,"physical_demand":3.0,"license_barrier":7.0,
            "cycle_sensitivity":1.5,"side_job_compat":1.5,"intl_mobility":3.5,"industry_monopoly":7.5,
            "trend_long":0,"trend_short":0,"edu":"本科","age":"22-28",
        },
    }
    return B.get(oid, {})


# ---------------------------------------------------------------------------
# SCORING
# ---------------------------------------------------------------------------
def clamp(v, lo=0.0, hi=10.0):
    return max(lo, min(hi, round(v, 1)))

def clamp5(v):
    return max(0.0, min(5.0, round(v, 1)))

SCORE_DIMS = [
    "learning_cost","education_req","growth_coeff","career_lifespan",
    "opportunity","market_size","supply_demand","developed_scarcity",
    "value_added","cost_performance","stability","safety","occupational_disease",
    "overtime","burnout","skill_versatility","career_switch","reputation_variance",
    "ai_resistance","social_status","remote_friendly","autonomy","family_friendly",
    "fulfillment","entrepreneurship","gender_equality","age_flexibility",
    "social_interaction","physical_demand","license_barrier","cycle_sensitivity",
    "side_job_compat","intl_mobility","industry_monopoly",
]

def apply_country_modifiers(base, cp, oid):
    """Adjust base scores using GOV-specific country profiles."""
    s = dict(base)
    mid = oid[:2]  # first 2 digits → mid-category

    # Core factors
    stab_f = (cp["pub_stab"] - 6.0) / 4.0
    pay_f  = (cp["civil_pay"] - 5.0) / 5.0
    wlb_f  = (cp["wlb"] - 6.0) / 4.0
    corr_f = (cp["corruption"] - 5.0) / 5.0  # higher = cleaner
    exam_f = (cp["exam_sys"] - 6.0) / 4.0
    mil_f  = (cp["mil_spend"] - 5.0) / 5.0
    trust_f = (cp["police_trust"] - 5.0) / 5.0
    gov_f  = (cp["gov_size"] - 6.5) / 3.5
    intl_f = (cp["intl"] - 6.0) / 4.0
    gender_f = (cp["gender"] - 5.5) / 4.5
    comp_f = (cp["comp"] - 5.0) / 5.0
    edu_f  = (cp["edu"] - 6.0) / 4.0

    # --- Stability: extremely high for civil servants, modulated by country stability
    s["stability"] = clamp(s["stability"] + stab_f * 1.5 + corr_f * 0.5)

    # --- Value added (pay): civil_pay is primary driver
    s["value_added"] = clamp(s["value_added"] + pay_f * 2.0)
    s["cost_performance"] = clamp(s["cost_performance"] + pay_f * 1.0 + stab_f * 0.5)

    # --- Growth: limited in gov, but affected by gov_size expansion
    s["growth_coeff"] = clamp(s["growth_coeff"] + gov_f * 0.5 + stab_f * 0.3)

    # --- Career lifespan: longer in stable countries
    s["career_lifespan"] = clamp(s["career_lifespan"] + stab_f * 0.8)

    # --- Opportunity & market size: bigger gov = more jobs
    s["opportunity"] = clamp(s["opportunity"] + gov_f * 1.0)
    s["market_size"] = clamp(s["market_size"] + gov_f * 1.5)

    # --- Supply-demand: exam systems create artificial scarcity in some countries
    s["supply_demand"] = clamp(s["supply_demand"] + exam_f * 0.8 - gov_f * 0.3)
    s["developed_scarcity"] = clamp(s["developed_scarcity"] + exam_f * 0.5)

    # --- Safety: varies by role type
    if mid in ("06", "07", "08"):  # military, police, fire
        s["safety"] = clamp(s["safety"] + trust_f * 0.5 + stab_f * 0.3)
    else:
        s["safety"] = clamp(s["safety"] + stab_f * 0.3)

    # --- Overtime/burnout: WLB-driven
    s["overtime"] = clamp(s["overtime"] + wlb_f * 1.5)
    s["burnout"] = clamp(s["burnout"] + wlb_f * 1.0)

    # --- Occupational disease: WLB effect
    s["occupational_disease"] = clamp(s["occupational_disease"] + wlb_f * 0.8)

    # --- Remote: generally very low for GOV, minimal country variation
    s["remote_friendly"] = clamp(s["remote_friendly"] + wlb_f * 0.5)

    # --- Autonomy
    s["autonomy"] = clamp(s["autonomy"] + corr_f * 0.5 + wlb_f * 0.3)

    # --- Family friendly
    s["family_friendly"] = clamp(s["family_friendly"] + wlb_f * 1.5)

    # --- Social status: higher where gov jobs are prestigious (exam systems, pay)
    s["social_status"] = clamp(s["social_status"] + exam_f * 0.8 + pay_f * 0.5)

    # --- Military-specific: mil_spend affects military roles
    if mid == "06":
        s["value_added"] = clamp(s["value_added"] + mil_f * 1.0)
        s["opportunity"] = clamp(s["opportunity"] + mil_f * 0.8)
        s["social_status"] = clamp(s["social_status"] + mil_f * 0.5)

    # --- Police-specific: trust affects police roles
    if mid == "07":
        s["social_status"] = clamp(s["social_status"] + trust_f * 0.8)
        s["fulfillment"] = clamp(s["fulfillment"] + trust_f * 0.5)
        s["safety"] = clamp(s["safety"] + trust_f * 0.3)

    # --- International org: intl_mobility boost
    if mid == "05":
        s["intl_mobility"] = clamp(s["intl_mobility"] + intl_f * 1.0)
        s["value_added"] = clamp(s["value_added"] + intl_f * 0.5)
    else:
        s["intl_mobility"] = clamp(s["intl_mobility"] + intl_f * 0.5)

    # --- License barrier: exam systems increase barrier
    s["license_barrier"] = clamp(s["license_barrier"] + exam_f * 0.8)

    # --- Entrepreneurship: always very low in gov
    s["entrepreneurship"] = clamp(s["entrepreneurship"] + corr_f * 0.2)

    # --- Gender equality
    s["gender_equality"] = clamp(s["gender_equality"] + gender_f * 2.0)

    # --- Age flexibility
    s["age_flexibility"] = clamp(s["age_flexibility"] + wlb_f * 0.5)

    # --- Fulfillment: corruption inversely affects (cleaner = more fulfilling)
    s["fulfillment"] = clamp(s["fulfillment"] + corr_f * 0.5)

    # --- Cycle sensitivity: gov jobs are counter-cyclical mostly
    s["cycle_sensitivity"] = clamp(s["cycle_sensitivity"] - stab_f * 0.3)

    # --- Side job: generally prohibited in gov
    s["side_job_compat"] = clamp(s["side_job_compat"] + corr_f * 0.3)

    # --- AI resistance: doesn't vary much by country
    s["ai_resistance"] = clamp(s["ai_resistance"] + edu_f * 0.2)

    # --- Education/learning
    s["learning_cost"] = clamp(s["learning_cost"] + edu_f * 0.3)
    s["education_req"] = clamp(s["education_req"] + edu_f * 0.3 + exam_f * 0.3)

    # --- Skill versatility / career switch
    s["skill_versatility"] = clamp(s["skill_versatility"] + edu_f * 0.3)
    s["career_switch"] = clamp(s["career_switch"] + corr_f * 0.3)

    # --- Reputation variance: higher in corrupt countries
    s["reputation_variance"] = clamp5(s["reputation_variance"] - corr_f * 0.5)

    # --- Industry monopoly: gov is always monopolistic
    s["industry_monopoly"] = clamp(s["industry_monopoly"] + gov_f * 0.2)

    return s


def get_trends(base, cp):
    t_long = base["trend_long"]
    t_short = base["trend_short"]
    # Countries with growing gov sector
    if cp["gov_size"] >= 8.0:
        t_short = min(5, t_short + 1)
    elif cp["gov_size"] < 5.5:
        t_short = max(-5, t_short - 1)
    # Stable countries maintain trends
    if cp["pub_stab"] >= 8.0:
        t_long = min(5, t_long)
    elif cp["pub_stab"] < 5.0:
        t_long = max(-5, t_long - 1)
    return t_long, t_short


def get_demand_direction(t5):
    if t5 >= 4: return "↑↑"
    if t5 >= 2: return "↑"
    if t5 >= -1: return "→"
    if t5 >= -3: return "↓"
    return "↓↓"


def get_ai_timeline(oid, ai_r):
    if ai_r >= 7.5: return "2035+"
    if ai_r >= 6.0: return "2032-2038"
    if ai_r >= 4.5: return "2028-2033"
    if ai_r >= 3.0: return "2026-2030"
    return "2025-2028"


def generate_summary(occ, country, scores, t5, ai_r):
    hz, he = [], []
    if scores["stability"] >= 8.5:
        hz.append("就业极其稳定"); he.append("extremely stable employment")
    elif scores["stability"] >= 7.5:
        hz.append("就业稳定"); he.append("stable employment")
    if scores["value_added"] >= 7.5:
        hz.append("薪资回报高"); he.append("high compensation")
    elif scores["value_added"] <= 4.0:
        hz.append("薪资水平偏低"); he.append("relatively low pay")
    if scores["license_barrier"] >= 8.0:
        hz.append("准入门槛高"); he.append("high entry barrier")
    if scores["safety"] <= 4.5:
        hz.append("职业安全风险高"); he.append("high safety risk")
    if scores["ai_resistance"] >= 7.0:
        hz.append("AI替代抗性强"); he.append("strong AI resistance")
    if scores["fulfillment"] >= 8.0:
        hz.append("职业成就感高"); he.append("high job fulfillment")
    if scores["remote_friendly"] <= 2.0:
        hz.append("无法远程办公"); he.append("no remote work possible")
    if scores["physical_demand"] >= 7.0:
        hz.append("体能要求高"); he.append("high physical demands")
    if t5 >= 3:
        hz.append("近年需求增长"); he.append("growing demand")
    elif t5 <= -2:
        hz.append("近年需求下降"); he.append("declining demand")
    hz, he = hz[:3], he[:3]
    if not hz:
        hz, he = ["发展平稳"], ["steady development"]
    zh = f"{country['name_zh']}{occ['zh']}：{'，'.join(hz)}"
    en = f"{country['name_en']} {occ['en']}: {', '.join(he)}"
    return zh, en


# ---------------------------------------------------------------------------
# HEADERS (same schema as other generators)
# ---------------------------------------------------------------------------
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
    "summary_zh","summary_en","data_source",
]


def main():
    random.seed(42)
    weights = load_weights()
    csv_path = PROJECT_ROOT / "data" / "csv" / "gov_public.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []

    for occ in OCCUPATIONS:
        base = occ_base(occ["id"])
        if not base:
            print(f"WARNING: No base for {occ['id']} ({occ['en']}), skip")
            continue
        for country in COUNTRIES:
            iso = country["iso"]
            cp = COUNTRY_PROFILES[iso]
            scores = apply_country_modifiers(base, cp, occ["id"])

            # Per-row noise
            ns = hash(f"GOV-{occ['id']}-{iso}") % 10000
            rng = random.Random(ns)
            for dim in SCORE_DIMS:
                if dim == "reputation_variance":
                    scores[dim] = clamp5(scores[dim] + rng.uniform(-0.2, 0.2))
                elif dim == "safety":
                    scores[dim] = clamp(scores[dim] + rng.uniform(-0.1, 0.1))
                else:
                    scores[dim] = clamp(scores[dim] + rng.uniform(-0.3, 0.3))

            t_long, t_short = get_trends(base, cp)
            demand_dir = get_demand_direction(t_short)
            ai_tl = get_ai_timeline(occ["id"], scores["ai_resistance"])

            score_dict = {d: scores[d] for d in weights}
            composite = calculate_composite(score_dict, weights)

            summary_zh, summary_en = generate_summary(occ, country, scores, t_short, scores["ai_resistance"])

            row_id = f"GOV-{occ['id']}-{iso}-general"
            row = {
                "id": row_id,
                "major_category": "公共管理与公务员",
                "major_code": "GOV",
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
            row["trend_2000_2026"] = t_long
            row["trend_5yr"] = t_short
            row["demand_direction"] = demand_dir
            row["ai_timeline"] = ai_tl
            row["composite_index"] = composite
            row["summary_zh"] = summary_zh
            row["summary_en"] = summary_en
            row["data_source"] = "AI综合评估 + O*NET/ILO/OECD锚点校准"
            rows.append(row)

    # Write CSV
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated {len(rows)} rows to {csv_path}")
    print(f"Occupations: {len(OCCUPATIONS)}, Countries: {len(COUNTRIES)}")

    # JSON
    from tools.csv_to_json import convert_csv_to_json
    json_path = PROJECT_ROOT / "data" / "json" / "gov_public.json"
    convert_csv_to_json(str(csv_path), str(json_path))
    print(f"JSON written to {json_path}")

    # Notebook
    from tools.generate_notebook import create_data_notebook
    nb_path = PROJECT_ROOT / "notebooks" / "06_gov_public.ipynb"
    create_data_notebook(
        str(csv_path), str(nb_path),
        title="公共管理与公务员 (GOV) — 完整数据",
        description="50 occupations × 45 countries/regions = 2,250 rows",
    )
    print(f"Notebook written to {nb_path}")


if __name__ == "__main__":
    main()
