#!/usr/bin/env python3
"""Generate legal_social.csv — LAW data for Global Career Development Index.
72 occupations x 45 countries. Compact format.
"""
import csv, sys, random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from tools.score_calculator import load_weights, calculate_composite

# ---------------------------------------------------------------------------
# OCCUPATIONS (from categories.yaml LAW section)
# ---------------------------------------------------------------------------
_OCC_RAW = [
    # lawyers (19)
    ("0101","lawyers","律师各专业","Lawyers (Specializations)","公司法律师","Corporate Lawyer","2611","23-1011.00","global"),
    ("0102","lawyers","律师各专业","Lawyers (Specializations)","刑事辩护律师","Criminal Defense Lawyer","2611","23-1011.00","global"),
    ("0103","lawyers","律师各专业","Lawyers (Specializations)","知识产权律师","Intellectual Property Lawyer","2611","23-1011.00","global"),
    ("0104","lawyers","律师各专业","Lawyers (Specializations)","移民律师","Immigration Lawyer","2611","23-1011.00","global"),
    ("0105","lawyers","律师各专业","Lawyers (Specializations)","家庭法律师","Family Lawyer","2611","23-1011.00","global"),
    ("0106","lawyers","律师各专业","Lawyers (Specializations)","劳动法律师","Employment / Labor Lawyer","2611","23-1011.00","global"),
    ("0107","lawyers","律师各专业","Lawyers (Specializations)","税法律师","Tax Lawyer","2611","23-1011.00","global"),
    ("0108","lawyers","律师各专业","Lawyers (Specializations)","环境法律师","Environmental Lawyer","2611","23-1011.00","global"),
    ("0109","lawyers","律师各专业","Lawyers (Specializations)","国际法律师","International Lawyer","2611","23-1011.00","global"),
    ("0110","lawyers","律师各专业","Lawyers (Specializations)","医疗纠纷律师","Medical Malpractice Lawyer","2611","23-1011.00","global"),
    ("0111","lawyers","律师各专业","Lawyers (Specializations)","房地产律师","Real Estate Lawyer","2611","23-1011.00","global"),
    ("0112","lawyers","律师各专业","Lawyers (Specializations)","并购律师","M&A Lawyer","2611","23-1011.00","global"),
    ("0113","lawyers","律师各专业","Lawyers (Specializations)","隐私与数据保护律师","Privacy & Data Protection Lawyer","2611","23-1011.00","global"),
    ("0114","lawyers","律师各专业","Lawyers (Specializations)","破产律师","Bankruptcy Lawyer","2611","23-1011.00","global"),
    ("0115","lawyers","律师各专业","Lawyers (Specializations)","海事律师","Maritime / Admiralty Lawyer","2611","23-1011.00","global"),
    ("0116","lawyers","律师各专业","Lawyers (Specializations)","体育法律师","Sports Lawyer","2611","23-1011.00","global"),
    ("0117","lawyers","律师各专业","Lawyers (Specializations)","娱乐法律师","Entertainment Lawyer","2611","23-1011.00","global"),
    ("0118","lawyers","律师各专业","Lawyers (Specializations)","人权律师","Human Rights Lawyer","2611","23-1011.00","global"),
    ("0119","lawyers","律师各专业","Lawyers (Specializations)","航空法律师","Aviation Lawyer","2611","23-1011.00","global"),
    # judges (3)
    ("0201","judges","法官","Judges","法官","Judge","2612","23-1023.00","global"),
    ("0202","judges","法官","Judges","行政法法官","Administrative Law Judge","2612","23-1021.00","global"),
    ("0203","judges","法官","Judges","最高法院法官/大法官","Supreme Court Justice","2612","23-1023.00","global"),
    # prosecutors (2)
    ("0301","prosecutors","检察官","Prosecutors","检察官","Prosecutor","2611","23-1011.00","global"),
    ("0302","prosecutors","检察官","Prosecutors","反腐检察官","Anti-Corruption Prosecutor","2611","23-1011.00","global"),
    # notary_arbitration (4)
    ("0401","notary_arbitration","公证与仲裁","Notary & Arbitration","公证人","Notary Public","2619","23-2011.00","global"),
    ("0402","notary_arbitration","公证与仲裁","Notary & Arbitration","公证人(大陆法系)","Civil Law Notary","2619","","regional"),
    ("0403","notary_arbitration","公证与仲裁","Notary & Arbitration","仲裁员","Arbitrator","2619","23-1022.00","global"),
    ("0404","notary_arbitration","公证与仲裁","Notary & Arbitration","调解员","Mediator","2619","23-1022.00","global"),
    # legal_support (5)
    ("0501","legal_support","法律助理/律师助理","Legal Support","律师助理","Paralegal","3411","23-2011.00","global"),
    ("0502","legal_support","法律助理/律师助理","Legal Support","法律秘书","Legal Secretary","3411","43-6012.00","global"),
    ("0503","legal_support","法律助理/律师助理","Legal Support","法律翻译","Legal Translator","2643","27-3091.00","global"),
    ("0504","legal_support","法律助理/律师助理","Legal Support","专利代理人","Patent Agent","2619","23-2011.00","global"),
    ("0505","legal_support","法律助理/律师助理","Legal Support","商标代理人","Trademark Agent","2619","23-2011.00","global"),
    # social_work (7)
    ("0601","social_work","社会工作","Social Work","社会工作者","Social Worker","2635","21-1021.00","global"),
    ("0602","social_work","社会工作","Social Work","社区组织者","Community Organizer","3412","21-1094.00","global"),
    ("0603","social_work","社会工作","Social Work","儿童福利社工","Child Welfare Social Worker","2635","21-1021.00","global"),
    ("0604","social_work","社会工作","Social Work","医务社工","Medical Social Worker","2635","21-1022.00","global"),
    ("0605","social_work","社会工作","Social Work","学校社工","School Social Worker","2635","21-1021.00","global"),
    ("0606","social_work","社会工作","Social Work","社区发展工作者","Community Development Worker","3412","21-1094.00","global"),
    ("0607","social_work","社会工作","Social Work","社会政策分析师","Social Policy Analyst","2632","19-3094.00","global"),
    # ngo_humanitarian (8)
    ("0701","ngo_humanitarian","NGO与人道主义","NGO & Humanitarian","NGO项目经理","NGO Program Manager","1114","11-9199.00","global"),
    ("0702","ngo_humanitarian","NGO与人道主义","NGO & Humanitarian","筹款经理","Fundraising Manager","1114","11-2031.00","global"),
    ("0703","ngo_humanitarian","NGO与人道主义","NGO & Humanitarian","志愿者管理协调员","Volunteer Coordinator","1114","11-9151.00","global"),
    ("0704","ngo_humanitarian","NGO与人道主义","NGO & Humanitarian","人道主义援助工作者","Humanitarian Aid Worker","2635","21-1099.00","global"),
    ("0705","ngo_humanitarian","NGO与人道主义","NGO & Humanitarian","难民安置官员","Refugee Resettlement Officer","2635","21-1099.00","global"),
    ("0706","ngo_humanitarian","NGO与人道主义","NGO & Humanitarian","人权倡导者","Human Rights Advocate","2619","21-1099.00","global"),
    ("0707","ngo_humanitarian","NGO与人道主义","NGO & Humanitarian","灾害救援工作者","Disaster Relief Worker","2635","21-1099.00","global"),
    ("0708","ngo_humanitarian","NGO与人道主义","NGO & Humanitarian","环保NGO倡导者","Environmental NGO Advocate","2635","21-1099.00","global"),
    # religious (8)
    ("0801","religious","宗教","Religious","基督教牧师","Christian Pastor / Minister","2636","21-2011.00","global"),
    ("0802","religious","宗教","Religious","佛教僧侣","Buddhist Monk / Nun","2636","21-2011.00","global"),
    ("0803","religious","宗教","Religious","伊斯兰阿訇/伊玛目","Islamic Imam","2636","21-2011.00","global"),
    ("0804","religious","宗教","Religious","犹太拉比","Rabbi","2636","21-2011.00","global"),
    ("0805","religious","宗教","Religious","天主教神父","Catholic Priest","2636","21-2011.00","global"),
    ("0806","religious","宗教","Religious","道教道士","Taoist Priest","2636","21-2011.00","regional"),
    ("0807","religious","宗教","Religious","印度教祭司","Hindu Priest (Pandit)","2636","21-2011.00","regional"),
    ("0808","religious","宗教","Religious","军队牧师","Military Chaplain","2636","21-2011.00","global"),
    # psychosocial_services (8)
    ("0901","psychosocial_services","心理社会服务","Psychosocial Services","婚姻家庭咨询师","Marriage & Family Therapist","2634","21-1013.00","global"),
    ("0902","psychosocial_services","心理社会服务","Psychosocial Services","戒瘾辅导员","Substance Abuse Counselor","2634","21-1011.00","global"),
    ("0903","psychosocial_services","心理社会服务","Psychosocial Services","危机干预咨询师","Crisis Intervention Counselor","2634","21-1023.00","global"),
    ("0904","psychosocial_services","心理社会服务","Psychosocial Services","职业康复咨询师","Vocational Rehabilitation Counselor","2634","21-1015.00","global"),
    ("0905","psychosocial_services","心理社会服务","Psychosocial Services","赏金猎人","Bounty Hunter / Bail Enforcement Agent","5414","33-9011.00","country_specific"),
    ("0906","psychosocial_services","心理社会服务","Psychosocial Services","保释担保人","Bail Bondsman","3312","13-2099.00","country_specific"),
    ("0907","psychosocial_services","心理社会服务","Psychosocial Services","家庭暴力受害者倡导者","Domestic Violence Advocate","2635","21-1099.00","global"),
    ("0908","psychosocial_services","心理社会服务","Psychosocial Services","遗产规划顾问","Estate Planning Advisor","2611","23-1011.00","global"),
    # compliance_regulation (8)
    ("1001","compliance_regulation","合规与监管","Compliance & Regulation","数据保护官(DPO)","Data Protection Officer (DPO)","2619","13-1041.00","global"),
    ("1002","compliance_regulation","合规与监管","Compliance & Regulation","法规事务专员","Regulatory Affairs Specialist","2619","13-1041.00","global"),
    ("1003","compliance_regulation","合规与监管","Compliance & Regulation","反垄断合规专员","Antitrust Compliance Specialist","2619","13-1041.00","global"),
    ("1004","compliance_regulation","合规与监管","Compliance & Regulation","贸易合规专员","Trade Compliance Specialist","2619","13-1041.06","global"),
    ("1005","compliance_regulation","合规与监管","Compliance & Regulation","选举监督员","Election Observer / Monitor","3354","21-1099.00","global"),
    ("1006","compliance_regulation","合规与监管","Compliance & Regulation","知识产权分析师","Intellectual Property Analyst","2619","23-2011.00","global"),
    ("1007","compliance_regulation","合规与监管","Compliance & Regulation","法律科技产品经理","Legal Tech Product Manager","2511","15-1299.09","global"),
    ("1008","compliance_regulation","合规与监管","Compliance & Regulation","法律AI训练师","Legal AI Trainer / Specialist","2619","15-1299.09","global"),
]

OCCUPATIONS = [{"id":r[0],"mid":r[1],"mid_zh":r[2],"mid_en":r[3],"zh":r[4],"en":r[5],"isco":r[6],"onet":r[7],"locality":r[8]} for r in _OCC_RAW]

# ---------------------------------------------------------------------------
# COUNTRIES (same 45)
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
# COUNTRY PROFILES — LAW-specific dimensions
# (legal_market, rule_of_law, lawyer_pay, ngo_sector, religious_diversity,
#  social_services, wlb, gender, intl, comp, edu, reg)
# All 0-10 scale.
# ---------------------------------------------------------------------------
COUNTRY_PROFILES = {
    # East Asia
    "CN": {"legal_market":7.5,"rule_of_law":5.0,"lawyer_pay":6.0,"ngo_sector":3.0,"religious_diversity":4.0,"social_services":5.5,"wlb":3.5,"gender":5.5,"intl":5.0,"comp":6.0,"edu":7.5,"reg":6.0},
    "JP": {"legal_market":7.0,"rule_of_law":8.0,"lawyer_pay":7.0,"ngo_sector":5.5,"religious_diversity":5.0,"social_services":7.5,"wlb":5.0,"gender":5.0,"intl":5.0,"comp":7.0,"edu":8.0,"reg":7.0},
    "KR": {"legal_market":6.5,"rule_of_law":7.5,"lawyer_pay":6.5,"ngo_sector":6.0,"religious_diversity":6.5,"social_services":7.0,"wlb":4.5,"gender":4.5,"intl":5.5,"comp":6.5,"edu":8.0,"reg":6.5},
    "TW": {"legal_market":6.0,"rule_of_law":7.5,"lawyer_pay":5.5,"ngo_sector":6.5,"religious_diversity":7.0,"social_services":6.5,"wlb":5.0,"gender":6.0,"intl":5.5,"comp":5.5,"edu":7.5,"reg":6.5},
    "HK": {"legal_market":7.5,"rule_of_law":7.0,"lawyer_pay":8.5,"ngo_sector":5.0,"religious_diversity":5.5,"social_services":6.5,"wlb":4.5,"gender":6.5,"intl":9.0,"comp":8.0,"edu":7.5,"reg":7.0},
    # Southeast Asia
    "SG": {"legal_market":7.0,"rule_of_law":9.0,"lawyer_pay":8.0,"ngo_sector":4.0,"religious_diversity":8.0,"social_services":7.0,"wlb":5.5,"gender":7.0,"intl":9.0,"comp":8.5,"edu":8.5,"reg":8.5},
    "TH": {"legal_market":4.5,"rule_of_law":5.5,"lawyer_pay":4.0,"ngo_sector":5.0,"religious_diversity":4.5,"social_services":5.0,"wlb":6.0,"gender":6.0,"intl":4.5,"comp":3.5,"edu":5.5,"reg":5.0},
    "VN": {"legal_market":4.0,"rule_of_law":4.5,"lawyer_pay":3.5,"ngo_sector":3.0,"religious_diversity":4.0,"social_services":5.0,"wlb":5.0,"gender":5.5,"intl":4.5,"comp":3.0,"edu":5.5,"reg":5.0},
    "ID": {"legal_market":5.0,"rule_of_law":5.0,"lawyer_pay":4.0,"ngo_sector":5.5,"religious_diversity":6.0,"social_services":4.5,"wlb":5.5,"gender":5.0,"intl":4.0,"comp":3.5,"edu":5.0,"reg":5.0},
    "MY": {"legal_market":5.5,"rule_of_law":6.0,"lawyer_pay":5.0,"ngo_sector":4.5,"religious_diversity":6.5,"social_services":5.5,"wlb":5.5,"gender":5.5,"intl":6.0,"comp":4.5,"edu":6.0,"reg":5.5},
    "PH": {"legal_market":5.0,"rule_of_law":4.5,"lawyer_pay":3.5,"ngo_sector":6.5,"religious_diversity":4.5,"social_services":4.5,"wlb":5.0,"gender":6.5,"intl":6.0,"comp":3.0,"edu":5.5,"reg":4.5},
    # South Asia
    "IN": {"legal_market":7.0,"rule_of_law":5.5,"lawyer_pay":5.5,"ngo_sector":7.0,"religious_diversity":9.0,"social_services":4.5,"wlb":4.5,"gender":4.5,"intl":5.5,"comp":4.5,"edu":7.0,"reg":5.5},
    "PK": {"legal_market":4.5,"rule_of_law":3.5,"lawyer_pay":3.0,"ngo_sector":5.5,"religious_diversity":3.5,"social_services":3.5,"wlb":4.5,"gender":3.0,"intl":4.0,"comp":2.5,"edu":4.5,"reg":4.0},
    "BD": {"legal_market":3.5,"rule_of_law":3.5,"lawyer_pay":2.5,"ngo_sector":7.5,"religious_diversity":3.5,"social_services":3.5,"wlb":4.5,"gender":3.5,"intl":4.0,"comp":2.0,"edu":4.0,"reg":3.5},
    # Middle East
    "AE": {"legal_market":6.5,"rule_of_law":7.0,"lawyer_pay":8.0,"ngo_sector":3.0,"religious_diversity":5.0,"social_services":6.0,"wlb":5.5,"gender":5.0,"intl":8.0,"comp":8.0,"edu":7.0,"reg":6.5},
    "IL": {"legal_market":7.0,"rule_of_law":7.5,"lawyer_pay":7.0,"ngo_sector":7.5,"religious_diversity":6.5,"social_services":7.0,"wlb":6.0,"gender":7.0,"intl":7.5,"comp":7.0,"edu":8.5,"reg":6.0},
    "SA": {"legal_market":5.0,"rule_of_law":5.0,"lawyer_pay":6.5,"ngo_sector":2.0,"religious_diversity":2.0,"social_services":5.5,"wlb":5.0,"gender":3.5,"intl":5.0,"comp":7.0,"edu":6.0,"reg":5.0},
    "TR": {"legal_market":5.5,"rule_of_law":4.5,"lawyer_pay":4.0,"ngo_sector":4.5,"religious_diversity":4.0,"social_services":5.5,"wlb":5.0,"gender":4.5,"intl":5.0,"comp":4.0,"edu":6.5,"reg":5.0},
    # Western Europe — strong legal tradition
    "GB": {"legal_market":9.0,"rule_of_law":9.0,"lawyer_pay":8.5,"ngo_sector":8.0,"religious_diversity":7.0,"social_services":7.5,"wlb":7.0,"gender":7.5,"intl":9.0,"comp":7.5,"edu":8.5,"reg":7.5},
    "FR": {"legal_market":7.5,"rule_of_law":8.0,"lawyer_pay":6.5,"ngo_sector":7.0,"religious_diversity":6.0,"social_services":8.5,"wlb":8.0,"gender":7.0,"intl":7.5,"comp":6.5,"edu":8.0,"reg":8.0},
    "DE": {"legal_market":8.0,"rule_of_law":8.5,"lawyer_pay":7.0,"ngo_sector":7.5,"religious_diversity":6.5,"social_services":8.5,"wlb":8.0,"gender":7.0,"intl":7.5,"comp":7.5,"edu":8.0,"reg":8.0},
    "NL": {"legal_market":7.0,"rule_of_law":8.5,"lawyer_pay":7.0,"ngo_sector":8.0,"religious_diversity":7.0,"social_services":9.0,"wlb":9.0,"gender":8.5,"intl":9.0,"comp":7.5,"edu":8.0,"reg":7.5},
    "CH": {"legal_market":7.0,"rule_of_law":9.5,"lawyer_pay":9.0,"ngo_sector":7.5,"religious_diversity":6.5,"social_services":8.5,"wlb":8.5,"gender":7.0,"intl":8.5,"comp":9.0,"edu":9.0,"reg":7.5},
    # Nordic
    "SE": {"legal_market":6.0,"rule_of_law":9.0,"lawyer_pay":7.0,"ngo_sector":8.0,"religious_diversity":5.5,"social_services":9.5,"wlb":9.0,"gender":9.0,"intl":8.0,"comp":7.0,"edu":8.5,"reg":7.5},
    "DK": {"legal_market":5.5,"rule_of_law":9.0,"lawyer_pay":7.0,"ngo_sector":8.0,"religious_diversity":5.0,"social_services":9.5,"wlb":9.0,"gender":9.0,"intl":8.0,"comp":7.5,"edu":8.5,"reg":7.5},
    "FI": {"legal_market":5.0,"rule_of_law":9.0,"lawyer_pay":6.5,"ngo_sector":7.5,"religious_diversity":4.5,"social_services":9.5,"wlb":9.0,"gender":9.0,"intl":7.5,"comp":6.5,"edu":9.0,"reg":7.5},
    # Southern Europe
    "IT": {"legal_market":6.5,"rule_of_law":6.5,"lawyer_pay":5.5,"ngo_sector":6.5,"religious_diversity":4.5,"social_services":7.0,"wlb":6.5,"gender":5.5,"intl":6.5,"comp":5.5,"edu":7.0,"reg":6.5},
    "ES": {"legal_market":6.0,"rule_of_law":7.0,"lawyer_pay":5.0,"ngo_sector":6.5,"religious_diversity":4.5,"social_services":7.0,"wlb":7.0,"gender":6.5,"intl":6.5,"comp":5.0,"edu":7.0,"reg":6.5},
    "PT": {"legal_market":5.0,"rule_of_law":7.0,"lawyer_pay":4.5,"ngo_sector":6.0,"religious_diversity":4.0,"social_services":7.0,"wlb":7.0,"gender":7.0,"intl":7.0,"comp":4.5,"edu":6.5,"reg":6.0},
    # Eastern Europe
    "PL": {"legal_market":5.5,"rule_of_law":6.5,"lawyer_pay":5.0,"ngo_sector":6.0,"religious_diversity":3.5,"social_services":6.5,"wlb":7.0,"gender":6.5,"intl":7.0,"comp":5.0,"edu":7.0,"reg":6.5},
    "CZ": {"legal_market":5.0,"rule_of_law":7.0,"lawyer_pay":5.0,"ngo_sector":6.0,"religious_diversity":4.5,"social_services":7.0,"wlb":7.5,"gender":6.5,"intl":7.0,"comp":5.5,"edu":7.0,"reg":6.5},
    "RU": {"legal_market":6.0,"rule_of_law":3.5,"lawyer_pay":4.5,"ngo_sector":3.5,"religious_diversity":5.0,"social_services":5.5,"wlb":5.5,"gender":6.0,"intl":3.5,"comp":4.5,"edu":7.5,"reg":4.5},
    # North America — US most litigious, highest lawyer pay
    "US": {"legal_market":9.5,"rule_of_law":8.0,"lawyer_pay":9.5,"ngo_sector":9.0,"religious_diversity":8.5,"social_services":6.5,"wlb":5.5,"gender":7.5,"intl":8.0,"comp":9.0,"edu":9.0,"reg":6.5},
    "CA": {"legal_market":7.5,"rule_of_law":8.5,"lawyer_pay":7.5,"ngo_sector":8.0,"religious_diversity":8.0,"social_services":8.0,"wlb":7.5,"gender":8.0,"intl":8.5,"comp":7.5,"edu":8.0,"reg":7.0},
    "MX": {"legal_market":5.0,"rule_of_law":4.0,"lawyer_pay":4.0,"ngo_sector":5.5,"religious_diversity":4.0,"social_services":5.0,"wlb":5.5,"gender":5.0,"intl":5.0,"comp":3.5,"edu":5.5,"reg":4.5},
    # South America
    "BR": {"legal_market":6.5,"rule_of_law":5.0,"lawyer_pay":5.0,"ngo_sector":6.5,"religious_diversity":7.0,"social_services":6.0,"wlb":6.0,"gender":5.5,"intl":4.5,"comp":4.5,"edu":6.0,"reg":5.5},
    "AR": {"legal_market":5.5,"rule_of_law":4.5,"lawyer_pay":4.0,"ngo_sector":6.0,"religious_diversity":5.0,"social_services":5.5,"wlb":5.5,"gender":5.5,"intl":5.0,"comp":3.5,"edu":6.5,"reg":4.5},
    "CL": {"legal_market":5.0,"rule_of_law":6.5,"lawyer_pay":5.0,"ngo_sector":6.0,"religious_diversity":4.5,"social_services":6.0,"wlb":6.0,"gender":5.5,"intl":5.5,"comp":5.0,"edu":6.0,"reg":5.5},
    "CO": {"legal_market":5.0,"rule_of_law":4.5,"lawyer_pay":4.0,"ngo_sector":6.0,"religious_diversity":4.5,"social_services":5.0,"wlb":5.5,"gender":5.0,"intl":4.5,"comp":3.5,"edu":5.5,"reg":5.0},
    # Oceania
    "AU": {"legal_market":7.5,"rule_of_law":8.5,"lawyer_pay":7.5,"ngo_sector":7.5,"religious_diversity":7.5,"social_services":8.0,"wlb":8.0,"gender":8.0,"intl":8.0,"comp":7.5,"edu":8.0,"reg":7.0},
    "NZ": {"legal_market":6.0,"rule_of_law":9.0,"lawyer_pay":6.5,"ngo_sector":7.5,"religious_diversity":7.0,"social_services":8.5,"wlb":8.5,"gender":8.5,"intl":7.5,"comp":6.5,"edu":7.5,"reg":7.0},
    # Africa
    "ZA": {"legal_market":6.0,"rule_of_law":5.5,"lawyer_pay":5.0,"ngo_sector":7.0,"religious_diversity":7.5,"social_services":5.0,"wlb":5.5,"gender":5.5,"intl":5.0,"comp":4.0,"edu":5.5,"reg":5.0},
    "NG": {"legal_market":5.0,"rule_of_law":3.5,"lawyer_pay":3.5,"ngo_sector":6.0,"religious_diversity":7.0,"social_services":3.5,"wlb":4.5,"gender":4.0,"intl":4.0,"comp":2.5,"edu":4.0,"reg":3.5},
    "KE": {"legal_market":4.5,"rule_of_law":4.5,"lawyer_pay":3.5,"ngo_sector":7.5,"religious_diversity":7.0,"social_services":4.0,"wlb":5.0,"gender":4.5,"intl":5.0,"comp":2.5,"edu":4.5,"reg":4.0},
    "EG": {"legal_market":5.0,"rule_of_law":4.0,"lawyer_pay":3.5,"ngo_sector":4.0,"religious_diversity":3.5,"social_services":5.0,"wlb":5.0,"gender":3.5,"intl":4.5,"comp":2.5,"edu":5.0,"reg":4.5},
}

# ---------------------------------------------------------------------------
# OCCUPATION BASE PROFILES
# ---------------------------------------------------------------------------
def occ_base(oid):
    B = {
        # ===== LAWYERS (01xx) =====
        "0101": {  # Corporate Lawyer
            "learning_cost":8.0,"education_req":8.0,"growth_coeff":7.5,"career_lifespan":8.0,
            "opportunity":7.0,"market_size":6.0,"supply_demand":6.5,"developed_scarcity":6.0,
            "value_added":9.0,"cost_performance":7.0,"stability":7.0,"safety":9.5,
            "occupational_disease":6.0,"overtime":3.5,"burnout":3.5,
            "skill_versatility":7.0,"career_switch":6.5,"reputation_variance":2.0,
            "ai_resistance":6.0,"social_status":8.5,"remote_friendly":5.5,"autonomy":6.5,
            "family_friendly":4.0,"fulfillment":6.5,"entrepreneurship":7.5,"gender_equality":5.5,
            "age_flexibility":6.5,"social_interaction":7.5,"physical_demand":0.5,"license_barrier":9.0,
            "cycle_sensitivity":4.0,"side_job_compat":3.0,"intl_mobility":7.0,"industry_monopoly":4.0,
            "trend_long":3,"trend_short":2,"edu":"法学博士/硕士","age":"25-30",
        },
        "0102": {  # Criminal Defense Lawyer
            "learning_cost":7.5,"education_req":7.5,"growth_coeff":5.0,"career_lifespan":8.0,
            "opportunity":5.5,"market_size":5.5,"supply_demand":5.0,"developed_scarcity":5.0,
            "value_added":6.5,"cost_performance":5.5,"stability":6.5,"safety":7.5,
            "occupational_disease":5.5,"overtime":4.0,"burnout":3.5,
            "skill_versatility":6.0,"career_switch":5.5,"reputation_variance":3.0,
            "ai_resistance":7.5,"social_status":7.0,"remote_friendly":3.5,"autonomy":7.0,
            "family_friendly":4.0,"fulfillment":7.5,"entrepreneurship":7.0,"gender_equality":5.0,
            "age_flexibility":7.0,"social_interaction":8.5,"physical_demand":1.0,"license_barrier":9.0,
            "cycle_sensitivity":2.5,"side_job_compat":3.0,"intl_mobility":4.5,"industry_monopoly":3.5,
            "trend_long":1,"trend_short":0,"edu":"法学博士/硕士","age":"25-30",
        },
        "0103": {  # IP Lawyer
            "learning_cost":8.5,"education_req":8.5,"growth_coeff":8.0,"career_lifespan":8.0,
            "opportunity":7.5,"market_size":5.0,"supply_demand":7.5,"developed_scarcity":7.5,
            "value_added":9.5,"cost_performance":7.5,"stability":7.0,"safety":9.5,
            "occupational_disease":6.5,"overtime":4.0,"burnout":4.0,
            "skill_versatility":6.5,"career_switch":6.0,"reputation_variance":1.5,
            "ai_resistance":6.5,"social_status":8.5,"remote_friendly":6.0,"autonomy":7.0,
            "family_friendly":4.5,"fulfillment":7.0,"entrepreneurship":7.5,"gender_equality":5.5,
            "age_flexibility":6.5,"social_interaction":7.0,"physical_demand":0.5,"license_barrier":9.0,
            "cycle_sensitivity":3.5,"side_job_compat":3.5,"intl_mobility":8.0,"industry_monopoly":4.0,
            "trend_long":4,"trend_short":3,"edu":"法学博士+理工背景","age":"26-32",
        },
        "0104": {  # Immigration Lawyer
            "learning_cost":7.0,"education_req":7.0,"growth_coeff":6.5,"career_lifespan":7.5,
            "opportunity":6.5,"market_size":5.0,"supply_demand":6.0,"developed_scarcity":5.5,
            "value_added":6.5,"cost_performance":6.0,"stability":6.5,"safety":8.5,
            "occupational_disease":6.0,"overtime":4.5,"burnout":4.5,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":2.5,
            "ai_resistance":6.5,"social_status":7.0,"remote_friendly":5.5,"autonomy":7.0,
            "family_friendly":5.0,"fulfillment":7.0,"entrepreneurship":7.0,"gender_equality":6.0,
            "age_flexibility":6.5,"social_interaction":8.0,"physical_demand":0.5,"license_barrier":8.5,
            "cycle_sensitivity":4.0,"side_job_compat":4.0,"intl_mobility":7.5,"industry_monopoly":3.5,
            "trend_long":3,"trend_short":2,"edu":"法学博士/硕士","age":"25-30",
        },
        "0105": {  # Family Lawyer
            "learning_cost":7.0,"education_req":7.0,"growth_coeff":4.5,"career_lifespan":8.0,
            "opportunity":5.5,"market_size":6.0,"supply_demand":5.0,"developed_scarcity":4.5,
            "value_added":5.5,"cost_performance":5.0,"stability":7.0,"safety":8.0,
            "occupational_disease":5.5,"overtime":5.0,"burnout":4.0,
            "skill_versatility":5.0,"career_switch":5.0,"reputation_variance":2.5,
            "ai_resistance":7.0,"social_status":6.5,"remote_friendly":4.5,"autonomy":6.5,
            "family_friendly":5.0,"fulfillment":6.5,"entrepreneurship":6.5,"gender_equality":6.5,
            "age_flexibility":7.0,"social_interaction":8.5,"physical_demand":0.5,"license_barrier":8.5,
            "cycle_sensitivity":2.0,"side_job_compat":3.5,"intl_mobility":4.0,"industry_monopoly":3.0,
            "trend_long":1,"trend_short":0,"edu":"法学博士/硕士","age":"25-30",
        },
        "0106": {  # Employment / Labor Lawyer
            "learning_cost":7.5,"education_req":7.5,"growth_coeff":5.5,"career_lifespan":8.0,
            "opportunity":6.0,"market_size":5.5,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":7.0,"cost_performance":6.0,"stability":7.0,"safety":9.0,
            "occupational_disease":6.0,"overtime":4.5,"burnout":4.0,
            "skill_versatility":6.0,"career_switch":6.0,"reputation_variance":2.0,
            "ai_resistance":6.5,"social_status":7.5,"remote_friendly":5.0,"autonomy":6.5,
            "family_friendly":4.5,"fulfillment":6.5,"entrepreneurship":6.5,"gender_equality":5.5,
            "age_flexibility":6.5,"social_interaction":7.5,"physical_demand":0.5,"license_barrier":8.5,
            "cycle_sensitivity":3.5,"side_job_compat":3.0,"intl_mobility":5.5,"industry_monopoly":3.5,
            "trend_long":2,"trend_short":1,"edu":"法学博士/硕士","age":"25-30",
        },
        "0107": {  # Tax Lawyer
            "learning_cost":8.0,"education_req":8.0,"growth_coeff":6.0,"career_lifespan":8.5,
            "opportunity":6.0,"market_size":5.0,"supply_demand":6.5,"developed_scarcity":6.5,
            "value_added":8.5,"cost_performance":7.0,"stability":7.5,"safety":9.5,
            "occupational_disease":6.5,"overtime":4.0,"burnout":4.0,
            "skill_versatility":6.0,"career_switch":6.0,"reputation_variance":1.5,
            "ai_resistance":5.5,"social_status":8.0,"remote_friendly":6.0,"autonomy":6.5,
            "family_friendly":4.5,"fulfillment":5.5,"entrepreneurship":7.0,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":6.5,"physical_demand":0.5,"license_barrier":9.0,
            "cycle_sensitivity":3.0,"side_job_compat":3.5,"intl_mobility":6.5,"industry_monopoly":4.0,
            "trend_long":2,"trend_short":1,"edu":"法学博士/硕士+会计","age":"25-32",
        },
        "0108": {  # Environmental Lawyer
            "learning_cost":7.5,"education_req":7.5,"growth_coeff":6.5,"career_lifespan":7.5,
            "opportunity":5.5,"market_size":4.0,"supply_demand":6.0,"developed_scarcity":6.0,
            "value_added":6.5,"cost_performance":5.5,"stability":6.5,"safety":9.0,
            "occupational_disease":6.5,"overtime":5.0,"burnout":4.5,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":2.0,
            "ai_resistance":6.5,"social_status":7.0,"remote_friendly":5.0,"autonomy":6.5,
            "family_friendly":5.0,"fulfillment":7.5,"entrepreneurship":5.5,"gender_equality":6.0,
            "age_flexibility":6.5,"social_interaction":7.0,"physical_demand":1.0,"license_barrier":8.5,
            "cycle_sensitivity":3.0,"side_job_compat":3.0,"intl_mobility":6.0,"industry_monopoly":3.5,
            "trend_long":3,"trend_short":3,"edu":"法学博士/硕士","age":"25-30",
        },
        "0109": {  # International Lawyer
            "learning_cost":8.5,"education_req":8.5,"growth_coeff":7.0,"career_lifespan":8.0,
            "opportunity":5.5,"market_size":3.5,"supply_demand":6.5,"developed_scarcity":7.0,
            "value_added":9.0,"cost_performance":7.0,"stability":7.0,"safety":8.5,
            "occupational_disease":6.0,"overtime":4.0,"burnout":4.0,
            "skill_versatility":7.0,"career_switch":6.5,"reputation_variance":1.5,
            "ai_resistance":7.0,"social_status":9.0,"remote_friendly":5.5,"autonomy":7.0,
            "family_friendly":3.5,"fulfillment":7.5,"entrepreneurship":6.5,"gender_equality":5.5,
            "age_flexibility":6.0,"social_interaction":8.0,"physical_demand":0.5,"license_barrier":9.0,
            "cycle_sensitivity":3.0,"side_job_compat":2.5,"intl_mobility":9.5,"industry_monopoly":4.5,
            "trend_long":3,"trend_short":2,"edu":"法学博士+LLM","age":"26-32",
        },
        "0110": {  # Medical Malpractice Lawyer
            "learning_cost":8.0,"education_req":8.0,"growth_coeff":5.5,"career_lifespan":8.0,
            "opportunity":5.0,"market_size":4.0,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":7.5,"cost_performance":6.0,"stability":6.5,"safety":9.0,
            "occupational_disease":6.0,"overtime":4.5,"burnout":4.0,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":2.5,
            "ai_resistance":6.5,"social_status":7.5,"remote_friendly":4.5,"autonomy":6.5,
            "family_friendly":4.5,"fulfillment":6.5,"entrepreneurship":7.0,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":7.5,"physical_demand":0.5,"license_barrier":9.0,
            "cycle_sensitivity":2.5,"side_job_compat":3.0,"intl_mobility":4.5,"industry_monopoly":3.5,
            "trend_long":2,"trend_short":1,"edu":"法学博士/硕士","age":"26-32",
        },
        "0111": {  # Real Estate Lawyer
            "learning_cost":7.0,"education_req":7.0,"growth_coeff":5.0,"career_lifespan":8.0,
            "opportunity":6.0,"market_size":5.5,"supply_demand":5.0,"developed_scarcity":4.5,
            "value_added":7.0,"cost_performance":6.0,"stability":6.5,"safety":9.5,
            "occupational_disease":6.5,"overtime":5.0,"burnout":5.0,
            "skill_versatility":5.0,"career_switch":5.0,"reputation_variance":2.0,
            "ai_resistance":5.5,"social_status":7.0,"remote_friendly":5.0,"autonomy":6.5,
            "family_friendly":5.0,"fulfillment":5.5,"entrepreneurship":7.0,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":7.0,"physical_demand":1.0,"license_barrier":8.5,
            "cycle_sensitivity":6.5,"side_job_compat":3.5,"intl_mobility":4.0,"industry_monopoly":3.5,
            "trend_long":1,"trend_short":0,"edu":"法学博士/硕士","age":"25-30",
        },
        "0112": {  # M&A Lawyer
            "learning_cost":8.5,"education_req":8.5,"growth_coeff":7.5,"career_lifespan":7.5,
            "opportunity":6.5,"market_size":4.0,"supply_demand":7.0,"developed_scarcity":7.0,
            "value_added":9.5,"cost_performance":7.0,"stability":6.5,"safety":9.5,
            "occupational_disease":5.5,"overtime":2.5,"burnout":3.0,
            "skill_versatility":7.0,"career_switch":7.0,"reputation_variance":1.5,
            "ai_resistance":6.0,"social_status":9.0,"remote_friendly":5.0,"autonomy":6.0,
            "family_friendly":3.0,"fulfillment":6.5,"entrepreneurship":7.0,"gender_equality":5.0,
            "age_flexibility":5.5,"social_interaction":8.0,"physical_demand":0.5,"license_barrier":9.5,
            "cycle_sensitivity":6.0,"side_job_compat":2.0,"intl_mobility":8.0,"industry_monopoly":5.0,
            "trend_long":3,"trend_short":2,"edu":"法学博士/硕士+MBA","age":"26-32",
        },
        "0113": {  # Privacy & Data Protection Lawyer
            "learning_cost":7.5,"education_req":7.5,"growth_coeff":8.5,"career_lifespan":7.0,
            "opportunity":8.0,"market_size":4.5,"supply_demand":8.0,"developed_scarcity":8.0,
            "value_added":8.5,"cost_performance":7.5,"stability":7.0,"safety":9.5,
            "occupational_disease":6.5,"overtime":4.5,"burnout":4.5,
            "skill_versatility":7.0,"career_switch":6.5,"reputation_variance":1.5,
            "ai_resistance":6.0,"social_status":8.0,"remote_friendly":6.5,"autonomy":7.0,
            "family_friendly":5.0,"fulfillment":7.0,"entrepreneurship":7.0,"gender_equality":6.0,
            "age_flexibility":6.0,"social_interaction":7.0,"physical_demand":0.5,"license_barrier":8.5,
            "cycle_sensitivity":3.0,"side_job_compat":4.0,"intl_mobility":8.0,"industry_monopoly":3.5,
            "trend_long":4,"trend_short":5,"edu":"法学博士/硕士+技术背景","age":"25-32",
        },
        "0114": {  # Bankruptcy Lawyer
            "learning_cost":7.5,"education_req":7.5,"growth_coeff":5.0,"career_lifespan":8.0,
            "opportunity":5.0,"market_size":4.0,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":7.5,"cost_performance":6.0,"stability":6.5,"safety":9.5,
            "occupational_disease":6.5,"overtime":4.0,"burnout":4.0,
            "skill_versatility":5.5,"career_switch":5.5,"reputation_variance":2.0,
            "ai_resistance":6.0,"social_status":7.0,"remote_friendly":5.5,"autonomy":6.5,
            "family_friendly":5.0,"fulfillment":5.5,"entrepreneurship":6.5,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":7.0,"physical_demand":0.5,"license_barrier":8.5,
            "cycle_sensitivity":7.0,"side_job_compat":3.0,"intl_mobility":5.0,"industry_monopoly":3.5,
            "trend_long":1,"trend_short":0,"edu":"法学博士/硕士","age":"25-30",
        },
        "0115": {  # Maritime / Admiralty Lawyer
            "learning_cost":8.0,"education_req":8.0,"growth_coeff":4.5,"career_lifespan":8.0,
            "opportunity":3.5,"market_size":2.5,"supply_demand":6.0,"developed_scarcity":6.5,
            "value_added":8.0,"cost_performance":6.0,"stability":7.0,"safety":9.0,
            "occupational_disease":6.5,"overtime":5.0,"burnout":4.5,
            "skill_versatility":4.5,"career_switch":4.0,"reputation_variance":1.5,
            "ai_resistance":7.0,"social_status":7.5,"remote_friendly":4.5,"autonomy":6.5,
            "family_friendly":4.5,"fulfillment":6.5,"entrepreneurship":5.5,"gender_equality":4.5,
            "age_flexibility":7.0,"social_interaction":6.5,"physical_demand":1.0,"license_barrier":9.0,
            "cycle_sensitivity":4.5,"side_job_compat":2.5,"intl_mobility":8.5,"industry_monopoly":5.0,
            "trend_long":1,"trend_short":0,"edu":"法学博士/硕士","age":"26-32",
        },
        "0116": {  # Sports Lawyer
            "learning_cost":7.5,"education_req":7.5,"growth_coeff":6.0,"career_lifespan":7.5,
            "opportunity":4.0,"market_size":2.5,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":7.5,"cost_performance":6.0,"stability":5.5,"safety":9.5,
            "occupational_disease":6.5,"overtime":4.5,"burnout":4.5,
            "skill_versatility":5.5,"career_switch":5.5,"reputation_variance":2.5,
            "ai_resistance":6.5,"social_status":7.5,"remote_friendly":5.0,"autonomy":6.5,
            "family_friendly":4.5,"fulfillment":7.0,"entrepreneurship":7.0,"gender_equality":5.0,
            "age_flexibility":6.0,"social_interaction":8.0,"physical_demand":0.5,"license_barrier":8.5,
            "cycle_sensitivity":4.5,"side_job_compat":3.5,"intl_mobility":6.5,"industry_monopoly":4.5,
            "trend_long":2,"trend_short":1,"edu":"法学博士/硕士","age":"25-30",
        },
        "0117": {  # Entertainment Lawyer
            "learning_cost":7.5,"education_req":7.5,"growth_coeff":6.5,"career_lifespan":7.5,
            "opportunity":5.0,"market_size":3.5,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":8.0,"cost_performance":6.5,"stability":5.5,"safety":9.5,
            "occupational_disease":6.0,"overtime":4.0,"burnout":4.0,
            "skill_versatility":6.0,"career_switch":6.0,"reputation_variance":2.5,
            "ai_resistance":6.5,"social_status":8.0,"remote_friendly":5.5,"autonomy":7.0,
            "family_friendly":4.5,"fulfillment":7.5,"entrepreneurship":7.5,"gender_equality":5.5,
            "age_flexibility":6.0,"social_interaction":8.5,"physical_demand":0.5,"license_barrier":8.5,
            "cycle_sensitivity":5.0,"side_job_compat":3.5,"intl_mobility":7.0,"industry_monopoly":4.5,
            "trend_long":2,"trend_short":2,"edu":"法学博士/硕士","age":"25-30",
        },
        "0118": {  # Human Rights Lawyer
            "learning_cost":7.5,"education_req":7.5,"growth_coeff":5.0,"career_lifespan":7.5,
            "opportunity":4.0,"market_size":3.0,"supply_demand":4.5,"developed_scarcity":5.0,
            "value_added":4.5,"cost_performance":4.0,"stability":5.0,"safety":6.5,
            "occupational_disease":5.5,"overtime":4.5,"burnout":3.5,
            "skill_versatility":6.0,"career_switch":5.5,"reputation_variance":3.5,
            "ai_resistance":7.5,"social_status":7.5,"remote_friendly":4.5,"autonomy":7.0,
            "family_friendly":4.0,"fulfillment":9.0,"entrepreneurship":4.0,"gender_equality":6.5,
            "age_flexibility":6.5,"social_interaction":8.5,"physical_demand":1.5,"license_barrier":8.0,
            "cycle_sensitivity":2.5,"side_job_compat":2.5,"intl_mobility":8.0,"industry_monopoly":3.0,
            "trend_long":2,"trend_short":1,"edu":"法学博士/硕士","age":"25-32",
        },
        "0119": {  # Aviation Lawyer
            "learning_cost":8.0,"education_req":8.0,"growth_coeff":5.5,"career_lifespan":8.0,
            "opportunity":3.5,"market_size":2.0,"supply_demand":6.0,"developed_scarcity":6.5,
            "value_added":8.5,"cost_performance":6.5,"stability":7.0,"safety":9.0,
            "occupational_disease":6.5,"overtime":4.5,"burnout":4.5,
            "skill_versatility":4.5,"career_switch":4.0,"reputation_variance":1.5,
            "ai_resistance":6.5,"social_status":8.0,"remote_friendly":5.0,"autonomy":6.5,
            "family_friendly":4.5,"fulfillment":6.5,"entrepreneurship":5.0,"gender_equality":4.5,
            "age_flexibility":7.0,"social_interaction":6.5,"physical_demand":0.5,"license_barrier":9.0,
            "cycle_sensitivity":5.0,"side_job_compat":2.5,"intl_mobility":8.5,"industry_monopoly":5.5,
            "trend_long":2,"trend_short":1,"edu":"法学博士/硕士","age":"26-32",
        },
        # ===== JUDGES (02xx) =====
        "0201": {  # Judge
            "learning_cost":9.0,"education_req":9.0,"growth_coeff":4.0,"career_lifespan":9.5,
            "opportunity":3.0,"market_size":3.5,"supply_demand":4.0,"developed_scarcity":4.0,
            "value_added":7.5,"cost_performance":6.0,"stability":9.5,"safety":8.0,
            "occupational_disease":6.5,"overtime":5.5,"burnout":4.5,
            "skill_versatility":5.0,"career_switch":4.0,"reputation_variance":1.5,
            "ai_resistance":8.5,"social_status":9.5,"remote_friendly":2.5,"autonomy":8.5,
            "family_friendly":5.5,"fulfillment":8.5,"entrepreneurship":1.0,"gender_equality":5.0,
            "age_flexibility":8.0,"social_interaction":7.5,"physical_demand":0.5,"license_barrier":9.5,
            "cycle_sensitivity":1.0,"side_job_compat":0.5,"intl_mobility":3.5,"industry_monopoly":9.0,
            "trend_long":0,"trend_short":0,"edu":"法学博士/硕士+多年执业","age":"35-50",
        },
        "0202": {  # Administrative Law Judge
            "learning_cost":8.5,"education_req":8.5,"growth_coeff":4.0,"career_lifespan":9.0,
            "opportunity":3.0,"market_size":3.0,"supply_demand":4.0,"developed_scarcity":4.0,
            "value_added":7.0,"cost_performance":5.5,"stability":9.0,"safety":8.5,
            "occupational_disease":6.5,"overtime":6.0,"burnout":5.0,
            "skill_versatility":5.0,"career_switch":4.0,"reputation_variance":1.5,
            "ai_resistance":7.5,"social_status":8.5,"remote_friendly":3.0,"autonomy":8.0,
            "family_friendly":6.0,"fulfillment":7.5,"entrepreneurship":1.0,"gender_equality":5.5,
            "age_flexibility":8.0,"social_interaction":7.0,"physical_demand":0.5,"license_barrier":9.5,
            "cycle_sensitivity":1.0,"side_job_compat":0.5,"intl_mobility":3.0,"industry_monopoly":9.0,
            "trend_long":0,"trend_short":0,"edu":"法学博士/硕士","age":"35-50",
        },
        "0203": {  # Supreme Court Justice
            "learning_cost":9.5,"education_req":9.5,"growth_coeff":3.5,"career_lifespan":9.5,
            "opportunity":1.0,"market_size":1.0,"supply_demand":2.0,"developed_scarcity":2.0,
            "value_added":8.0,"cost_performance":5.0,"stability":10.0,"safety":7.5,
            "occupational_disease":6.5,"overtime":5.0,"burnout":4.0,
            "skill_versatility":5.0,"career_switch":3.0,"reputation_variance":2.5,
            "ai_resistance":9.5,"social_status":10.0,"remote_friendly":2.0,"autonomy":9.5,
            "family_friendly":5.0,"fulfillment":9.5,"entrepreneurship":0.5,"gender_equality":4.5,
            "age_flexibility":9.0,"social_interaction":7.0,"physical_demand":0.5,"license_barrier":10.0,
            "cycle_sensitivity":0.5,"side_job_compat":0.5,"intl_mobility":3.0,"industry_monopoly":10.0,
            "trend_long":0,"trend_short":0,"edu":"法学博士+长期司法经验","age":"45-60",
        },
        # ===== PROSECUTORS (03xx) =====
        "0301": {  # Prosecutor
            "learning_cost":8.0,"education_req":8.0,"growth_coeff":4.5,"career_lifespan":8.5,
            "opportunity":4.0,"market_size":4.0,"supply_demand":4.5,"developed_scarcity":4.5,
            "value_added":6.5,"cost_performance":5.5,"stability":8.5,"safety":7.0,
            "occupational_disease":6.0,"overtime":4.5,"burnout":4.0,
            "skill_versatility":5.5,"career_switch":5.5,"reputation_variance":2.0,
            "ai_resistance":7.5,"social_status":8.5,"remote_friendly":2.5,"autonomy":6.5,
            "family_friendly":5.0,"fulfillment":7.5,"entrepreneurship":1.5,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":8.0,"physical_demand":0.5,"license_barrier":9.0,
            "cycle_sensitivity":1.5,"side_job_compat":1.0,"intl_mobility":3.5,"industry_monopoly":8.5,
            "trend_long":0,"trend_short":0,"edu":"法学博士/硕士","age":"25-32",
        },
        "0302": {  # Anti-Corruption Prosecutor
            "learning_cost":8.0,"education_req":8.0,"growth_coeff":5.0,"career_lifespan":8.0,
            "opportunity":3.0,"market_size":2.5,"supply_demand":5.0,"developed_scarcity":5.0,
            "value_added":6.5,"cost_performance":5.0,"stability":7.5,"safety":5.5,
            "occupational_disease":5.5,"overtime":4.0,"burnout":3.5,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":3.0,
            "ai_resistance":7.5,"social_status":8.5,"remote_friendly":2.0,"autonomy":6.0,
            "family_friendly":4.0,"fulfillment":8.5,"entrepreneurship":1.0,"gender_equality":5.0,
            "age_flexibility":6.5,"social_interaction":7.5,"physical_demand":1.0,"license_barrier":9.0,
            "cycle_sensitivity":1.5,"side_job_compat":0.5,"intl_mobility":4.0,"industry_monopoly":8.5,
            "trend_long":1,"trend_short":1,"edu":"法学博士/硕士","age":"28-35",
        },
        # ===== NOTARY_ARBITRATION (04xx) =====
        "0401": {  # Notary Public
            "learning_cost":5.0,"education_req":5.0,"growth_coeff":3.5,"career_lifespan":8.5,
            "opportunity":5.0,"market_size":5.5,"supply_demand":4.5,"developed_scarcity":3.5,
            "value_added":5.0,"cost_performance":5.5,"stability":8.0,"safety":9.5,
            "occupational_disease":7.0,"overtime":6.5,"burnout":6.5,
            "skill_versatility":3.5,"career_switch":3.5,"reputation_variance":1.5,
            "ai_resistance":5.0,"social_status":6.0,"remote_friendly":3.0,"autonomy":6.0,
            "family_friendly":6.5,"fulfillment":5.0,"entrepreneurship":5.5,"gender_equality":5.5,
            "age_flexibility":7.5,"social_interaction":7.0,"physical_demand":0.5,"license_barrier":7.5,
            "cycle_sensitivity":2.5,"side_job_compat":3.5,"intl_mobility":2.5,"industry_monopoly":6.0,
            "trend_long":0,"trend_short":-1,"edu":"法学本科/硕士","age":"25-35",
        },
        "0402": {  # Civil Law Notary (continental Europe — very important in DE/FR)
            "learning_cost":8.0,"education_req":8.0,"growth_coeff":4.0,"career_lifespan":9.0,
            "opportunity":3.5,"market_size":3.5,"supply_demand":5.0,"developed_scarcity":5.0,
            "value_added":8.0,"cost_performance":6.5,"stability":9.0,"safety":9.5,
            "occupational_disease":7.0,"overtime":6.5,"burnout":6.0,
            "skill_versatility":4.0,"career_switch":3.5,"reputation_variance":1.0,
            "ai_resistance":6.0,"social_status":8.0,"remote_friendly":2.5,"autonomy":7.5,
            "family_friendly":6.0,"fulfillment":6.5,"entrepreneurship":6.5,"gender_equality":5.0,
            "age_flexibility":7.5,"social_interaction":7.0,"physical_demand":0.5,"license_barrier":9.5,
            "cycle_sensitivity":2.0,"side_job_compat":2.0,"intl_mobility":2.5,"industry_monopoly":7.5,
            "trend_long":0,"trend_short":-1,"edu":"法学硕士+国家考试","age":"28-35",
        },
        "0403": {  # Arbitrator
            "learning_cost":8.0,"education_req":8.0,"growth_coeff":6.0,"career_lifespan":8.5,
            "opportunity":4.5,"market_size":3.5,"supply_demand":6.0,"developed_scarcity":6.0,
            "value_added":8.5,"cost_performance":6.5,"stability":7.0,"safety":9.5,
            "occupational_disease":6.5,"overtime":5.5,"burnout":5.0,
            "skill_versatility":6.0,"career_switch":5.5,"reputation_variance":1.5,
            "ai_resistance":7.5,"social_status":8.5,"remote_friendly":4.5,"autonomy":8.5,
            "family_friendly":5.5,"fulfillment":7.5,"entrepreneurship":7.0,"gender_equality":5.0,
            "age_flexibility":8.0,"social_interaction":7.5,"physical_demand":0.5,"license_barrier":8.5,
            "cycle_sensitivity":3.5,"side_job_compat":4.0,"intl_mobility":8.0,"industry_monopoly":5.0,
            "trend_long":2,"trend_short":2,"edu":"法学硕士+行业经验","age":"35-50",
        },
        "0404": {  # Mediator
            "learning_cost":6.0,"education_req":6.0,"growth_coeff":6.0,"career_lifespan":8.0,
            "opportunity":5.0,"market_size":4.5,"supply_demand":5.5,"developed_scarcity":5.0,
            "value_added":6.0,"cost_performance":5.5,"stability":6.5,"safety":9.0,
            "occupational_disease":6.5,"overtime":6.0,"burnout":5.5,
            "skill_versatility":6.5,"career_switch":6.0,"reputation_variance":2.0,
            "ai_resistance":7.5,"social_status":7.0,"remote_friendly":5.0,"autonomy":7.5,
            "family_friendly":6.0,"fulfillment":7.5,"entrepreneurship":7.0,"gender_equality":6.5,
            "age_flexibility":7.5,"social_interaction":9.0,"physical_demand":0.5,"license_barrier":6.5,
            "cycle_sensitivity":3.0,"side_job_compat":5.0,"intl_mobility":6.0,"industry_monopoly":3.5,
            "trend_long":2,"trend_short":2,"edu":"法学/心理学学位","age":"30-45",
        },
        # ===== LEGAL_SUPPORT (05xx) =====
        "0501": {  # Paralegal
            "learning_cost":4.0,"education_req":4.0,"growth_coeff":5.0,"career_lifespan":7.0,
            "opportunity":6.0,"market_size":6.5,"supply_demand":5.0,"developed_scarcity":4.0,
            "value_added":4.5,"cost_performance":5.5,"stability":6.5,"safety":9.5,
            "occupational_disease":6.5,"overtime":5.0,"burnout":5.0,
            "skill_versatility":5.0,"career_switch":5.0,"reputation_variance":1.5,
            "ai_resistance":4.0,"social_status":5.0,"remote_friendly":6.0,"autonomy":4.5,
            "family_friendly":6.0,"fulfillment":5.0,"entrepreneurship":3.5,"gender_equality":7.0,
            "age_flexibility":6.5,"social_interaction":6.5,"physical_demand":0.5,"license_barrier":4.0,
            "cycle_sensitivity":3.5,"side_job_compat":4.5,"intl_mobility":5.0,"industry_monopoly":3.5,
            "trend_long":2,"trend_short":0,"edu":"大专/本科","age":"20-28",
        },
        "0502": {  # Legal Secretary
            "learning_cost":3.0,"education_req":3.0,"growth_coeff":3.0,"career_lifespan":7.0,
            "opportunity":5.0,"market_size":6.0,"supply_demand":4.0,"developed_scarcity":3.5,
            "value_added":3.5,"cost_performance":4.5,"stability":6.0,"safety":9.5,
            "occupational_disease":7.0,"overtime":5.5,"burnout":5.5,
            "skill_versatility":4.0,"career_switch":4.5,"reputation_variance":1.5,
            "ai_resistance":3.0,"social_status":4.0,"remote_friendly":5.5,"autonomy":3.5,
            "family_friendly":6.5,"fulfillment":4.0,"entrepreneurship":2.5,"gender_equality":7.5,
            "age_flexibility":7.0,"social_interaction":6.5,"physical_demand":0.5,"license_barrier":2.5,
            "cycle_sensitivity":3.5,"side_job_compat":5.0,"intl_mobility":4.0,"industry_monopoly":3.0,
            "trend_long":0,"trend_short":-2,"edu":"大专/高中","age":"18-25",
        },
        "0503": {  # Legal Translator
            "learning_cost":6.5,"education_req":6.5,"growth_coeff":5.5,"career_lifespan":7.5,
            "opportunity":5.0,"market_size":3.5,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":6.0,"cost_performance":5.5,"stability":6.0,"safety":9.5,
            "occupational_disease":7.0,"overtime":5.5,"burnout":5.5,
            "skill_versatility":6.0,"career_switch":5.5,"reputation_variance":1.5,
            "ai_resistance":4.5,"social_status":6.0,"remote_friendly":8.0,"autonomy":7.0,
            "family_friendly":6.5,"fulfillment":6.0,"entrepreneurship":6.5,"gender_equality":7.0,
            "age_flexibility":7.0,"social_interaction":5.5,"physical_demand":0.5,"license_barrier":5.0,
            "cycle_sensitivity":3.0,"side_job_compat":7.5,"intl_mobility":7.5,"industry_monopoly":2.5,
            "trend_long":1,"trend_short":-1,"edu":"法学/语言本科","age":"22-28",
        },
        "0504": {  # Patent Agent
            "learning_cost":7.5,"education_req":7.5,"growth_coeff":6.5,"career_lifespan":8.0,
            "opportunity":6.0,"market_size":4.0,"supply_demand":6.5,"developed_scarcity":6.5,
            "value_added":7.5,"cost_performance":6.5,"stability":7.0,"safety":9.5,
            "occupational_disease":6.5,"overtime":5.0,"burnout":5.0,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":1.5,
            "ai_resistance":5.5,"social_status":7.0,"remote_friendly":6.5,"autonomy":6.5,
            "family_friendly":5.5,"fulfillment":6.5,"entrepreneurship":7.0,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":6.0,"physical_demand":0.5,"license_barrier":8.0,
            "cycle_sensitivity":3.0,"side_job_compat":4.5,"intl_mobility":7.0,"industry_monopoly":4.0,
            "trend_long":3,"trend_short":2,"edu":"理工+法学","age":"24-30",
        },
        "0505": {  # Trademark Agent
            "learning_cost":6.0,"education_req":6.0,"growth_coeff":5.5,"career_lifespan":8.0,
            "opportunity":5.5,"market_size":4.0,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":6.5,"cost_performance":6.0,"stability":7.0,"safety":9.5,
            "occupational_disease":6.5,"overtime":5.5,"burnout":5.5,
            "skill_versatility":5.0,"career_switch":5.0,"reputation_variance":1.5,
            "ai_resistance":5.0,"social_status":6.5,"remote_friendly":6.5,"autonomy":6.5,
            "family_friendly":5.5,"fulfillment":5.5,"entrepreneurship":6.5,"gender_equality":6.0,
            "age_flexibility":7.0,"social_interaction":6.0,"physical_demand":0.5,"license_barrier":7.0,
            "cycle_sensitivity":3.0,"side_job_compat":5.0,"intl_mobility":6.5,"industry_monopoly":4.0,
            "trend_long":2,"trend_short":1,"edu":"法学本科/硕士","age":"22-28",
        },
        # ===== SOCIAL_WORK (06xx) =====
        "0601": {  # Social Worker
            "learning_cost":5.5,"education_req":5.5,"growth_coeff":5.0,"career_lifespan":7.5,
            "opportunity":6.0,"market_size":6.5,"supply_demand":5.5,"developed_scarcity":5.0,
            "value_added":4.0,"cost_performance":4.5,"stability":6.5,"safety":7.5,
            "occupational_disease":5.5,"overtime":5.0,"burnout":3.5,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":2.0,
            "ai_resistance":7.5,"social_status":5.5,"remote_friendly":3.5,"autonomy":5.5,
            "family_friendly":5.5,"fulfillment":7.5,"entrepreneurship":3.0,"gender_equality":7.5,
            "age_flexibility":7.0,"social_interaction":9.0,"physical_demand":2.0,"license_barrier":6.0,
            "cycle_sensitivity":2.0,"side_job_compat":3.0,"intl_mobility":5.0,"industry_monopoly":3.5,
            "trend_long":2,"trend_short":1,"edu":"社工本科/硕士","age":"22-28",
        },
        "0602": {  # Community Organizer
            "learning_cost":4.0,"education_req":4.0,"growth_coeff":4.5,"career_lifespan":7.0,
            "opportunity":5.0,"market_size":5.0,"supply_demand":4.5,"developed_scarcity":4.0,
            "value_added":3.5,"cost_performance":4.0,"stability":5.5,"safety":7.5,
            "occupational_disease":6.0,"overtime":5.0,"burnout":4.0,
            "skill_versatility":6.0,"career_switch":5.5,"reputation_variance":2.5,
            "ai_resistance":8.0,"social_status":5.0,"remote_friendly":3.0,"autonomy":6.5,
            "family_friendly":5.0,"fulfillment":7.5,"entrepreneurship":5.0,"gender_equality":7.0,
            "age_flexibility":7.5,"social_interaction":9.5,"physical_demand":2.5,"license_barrier":3.0,
            "cycle_sensitivity":2.5,"side_job_compat":4.5,"intl_mobility":4.0,"industry_monopoly":2.5,
            "trend_long":1,"trend_short":1,"edu":"本科/大专","age":"22-30",
        },
        "0603": {  # Child Welfare Social Worker
            "learning_cost":5.5,"education_req":5.5,"growth_coeff":5.0,"career_lifespan":7.0,
            "opportunity":5.5,"market_size":5.5,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":4.0,"cost_performance":4.0,"stability":6.5,"safety":7.0,
            "occupational_disease":5.0,"overtime":4.5,"burnout":3.0,
            "skill_versatility":5.0,"career_switch":4.5,"reputation_variance":2.5,
            "ai_resistance":8.0,"social_status":5.5,"remote_friendly":2.5,"autonomy":5.5,
            "family_friendly":5.0,"fulfillment":7.5,"entrepreneurship":2.5,"gender_equality":8.0,
            "age_flexibility":6.5,"social_interaction":9.0,"physical_demand":2.5,"license_barrier":6.5,
            "cycle_sensitivity":2.0,"side_job_compat":2.5,"intl_mobility":4.5,"industry_monopoly":4.0,
            "trend_long":2,"trend_short":1,"edu":"社工硕士","age":"23-30",
        },
        "0604": {  # Medical Social Worker
            "learning_cost":6.0,"education_req":6.0,"growth_coeff":5.5,"career_lifespan":7.5,
            "opportunity":5.5,"market_size":5.0,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":4.5,"cost_performance":4.5,"stability":7.0,"safety":8.0,
            "occupational_disease":5.5,"overtime":5.0,"burnout":3.5,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":1.5,
            "ai_resistance":7.5,"social_status":5.5,"remote_friendly":3.0,"autonomy":5.5,
            "family_friendly":5.5,"fulfillment":7.5,"entrepreneurship":2.5,"gender_equality":7.5,
            "age_flexibility":6.5,"social_interaction":9.0,"physical_demand":2.0,"license_barrier":6.5,
            "cycle_sensitivity":1.5,"side_job_compat":2.5,"intl_mobility":5.0,"industry_monopoly":4.0,
            "trend_long":2,"trend_short":2,"edu":"社工硕士","age":"23-30",
        },
        "0605": {  # School Social Worker
            "learning_cost":5.5,"education_req":5.5,"growth_coeff":5.0,"career_lifespan":7.5,
            "opportunity":5.5,"market_size":5.5,"supply_demand":5.0,"developed_scarcity":5.0,
            "value_added":4.0,"cost_performance":4.5,"stability":7.0,"safety":8.5,
            "occupational_disease":6.0,"overtime":6.0,"burnout":4.0,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":2.0,
            "ai_resistance":7.5,"social_status":5.5,"remote_friendly":3.0,"autonomy":5.5,
            "family_friendly":6.5,"fulfillment":7.0,"entrepreneurship":2.5,"gender_equality":7.5,
            "age_flexibility":7.0,"social_interaction":9.0,"physical_demand":1.5,"license_barrier":6.0,
            "cycle_sensitivity":1.5,"side_job_compat":3.0,"intl_mobility":4.5,"industry_monopoly":4.0,
            "trend_long":2,"trend_short":1,"edu":"社工本科/硕士","age":"23-28",
        },
        "0606": {  # Community Development Worker
            "learning_cost":4.5,"education_req":4.5,"growth_coeff":4.5,"career_lifespan":7.0,
            "opportunity":5.0,"market_size":5.0,"supply_demand":4.5,"developed_scarcity":4.0,
            "value_added":3.5,"cost_performance":4.0,"stability":5.5,"safety":7.5,
            "occupational_disease":6.0,"overtime":5.5,"burnout":4.0,
            "skill_versatility":6.0,"career_switch":5.5,"reputation_variance":2.0,
            "ai_resistance":7.5,"social_status":5.0,"remote_friendly":3.0,"autonomy":6.0,
            "family_friendly":5.0,"fulfillment":7.0,"entrepreneurship":5.0,"gender_equality":7.0,
            "age_flexibility":7.5,"social_interaction":9.0,"physical_demand":3.0,"license_barrier":3.5,
            "cycle_sensitivity":2.5,"side_job_compat":4.0,"intl_mobility":5.5,"industry_monopoly":3.0,
            "trend_long":1,"trend_short":1,"edu":"本科/大专","age":"22-30",
        },
        "0607": {  # Social Policy Analyst
            "learning_cost":7.0,"education_req":7.0,"growth_coeff":5.5,"career_lifespan":8.0,
            "opportunity":4.5,"market_size":3.5,"supply_demand":5.0,"developed_scarcity":5.0,
            "value_added":6.0,"cost_performance":5.5,"stability":7.0,"safety":9.5,
            "occupational_disease":7.0,"overtime":6.0,"burnout":5.5,
            "skill_versatility":6.5,"career_switch":6.0,"reputation_variance":1.5,
            "ai_resistance":6.0,"social_status":6.5,"remote_friendly":6.0,"autonomy":6.0,
            "family_friendly":6.0,"fulfillment":7.0,"entrepreneurship":3.5,"gender_equality":6.5,
            "age_flexibility":7.0,"social_interaction":7.0,"physical_demand":0.5,"license_barrier":6.5,
            "cycle_sensitivity":2.0,"side_job_compat":3.5,"intl_mobility":6.5,"industry_monopoly":5.0,
            "trend_long":2,"trend_short":1,"edu":"硕士/博士","age":"24-30",
        },
        # ===== NGO_HUMANITARIAN (07xx) =====
        "0701": {  # NGO Program Manager
            "learning_cost":5.5,"education_req":5.5,"growth_coeff":5.5,"career_lifespan":7.0,
            "opportunity":5.5,"market_size":5.0,"supply_demand":5.0,"developed_scarcity":4.5,
            "value_added":5.0,"cost_performance":4.5,"stability":5.0,"safety":7.5,
            "occupational_disease":6.0,"overtime":4.5,"burnout":4.0,
            "skill_versatility":7.0,"career_switch":6.5,"reputation_variance":2.0,
            "ai_resistance":7.0,"social_status":6.5,"remote_friendly":5.5,"autonomy":7.0,
            "family_friendly":4.5,"fulfillment":8.0,"entrepreneurship":6.0,"gender_equality":7.0,
            "age_flexibility":6.5,"social_interaction":8.5,"physical_demand":2.0,"license_barrier":3.5,
            "cycle_sensitivity":3.5,"side_job_compat":3.0,"intl_mobility":8.0,"industry_monopoly":2.5,
            "trend_long":2,"trend_short":1,"edu":"本科/硕士","age":"24-30",
        },
        "0702": {  # Fundraising Manager
            "learning_cost":4.5,"education_req":4.5,"growth_coeff":5.0,"career_lifespan":7.0,
            "opportunity":5.0,"market_size":5.0,"supply_demand":5.0,"developed_scarcity":4.5,
            "value_added":5.0,"cost_performance":5.0,"stability":5.0,"safety":9.0,
            "occupational_disease":6.5,"overtime":5.0,"burnout":4.5,
            "skill_versatility":6.5,"career_switch":6.5,"reputation_variance":2.0,
            "ai_resistance":6.0,"social_status":6.0,"remote_friendly":5.5,"autonomy":6.5,
            "family_friendly":5.0,"fulfillment":7.0,"entrepreneurship":6.5,"gender_equality":7.0,
            "age_flexibility":7.0,"social_interaction":9.0,"physical_demand":1.0,"license_barrier":2.5,
            "cycle_sensitivity":5.0,"side_job_compat":4.0,"intl_mobility":6.5,"industry_monopoly":2.0,
            "trend_long":2,"trend_short":1,"edu":"本科","age":"22-28",
        },
        "0703": {  # Volunteer Coordinator
            "learning_cost":3.5,"education_req":3.5,"growth_coeff":4.0,"career_lifespan":6.5,
            "opportunity":5.0,"market_size":5.0,"supply_demand":4.0,"developed_scarcity":3.5,
            "value_added":3.5,"cost_performance":4.0,"stability":5.0,"safety":8.5,
            "occupational_disease":6.5,"overtime":5.5,"burnout":4.5,
            "skill_versatility":5.5,"career_switch":5.5,"reputation_variance":2.0,
            "ai_resistance":7.0,"social_status":5.0,"remote_friendly":4.5,"autonomy":6.0,
            "family_friendly":5.5,"fulfillment":7.5,"entrepreneurship":4.5,"gender_equality":7.5,
            "age_flexibility":7.5,"social_interaction":9.5,"physical_demand":2.0,"license_barrier":2.0,
            "cycle_sensitivity":3.5,"side_job_compat":5.0,"intl_mobility":5.5,"industry_monopoly":2.0,
            "trend_long":1,"trend_short":0,"edu":"本科/大专","age":"22-30",
        },
        "0704": {  # Humanitarian Aid Worker
            "learning_cost":5.0,"education_req":5.0,"growth_coeff":5.5,"career_lifespan":6.5,
            "opportunity":5.0,"market_size":4.0,"supply_demand":5.0,"developed_scarcity":4.5,
            "value_added":4.0,"cost_performance":3.5,"stability":4.0,"safety":4.5,
            "occupational_disease":4.5,"overtime":3.5,"burnout":3.0,
            "skill_versatility":6.5,"career_switch":5.5,"reputation_variance":2.0,
            "ai_resistance":8.0,"social_status":7.0,"remote_friendly":2.0,"autonomy":6.5,
            "family_friendly":2.5,"fulfillment":9.0,"entrepreneurship":3.5,"gender_equality":6.5,
            "age_flexibility":6.0,"social_interaction":9.0,"physical_demand":5.5,"license_barrier":3.5,
            "cycle_sensitivity":3.0,"side_job_compat":1.5,"intl_mobility":9.5,"industry_monopoly":2.5,
            "trend_long":2,"trend_short":2,"edu":"本科/硕士","age":"22-30",
        },
        "0705": {  # Refugee Resettlement Officer
            "learning_cost":5.0,"education_req":5.0,"growth_coeff":5.5,"career_lifespan":7.0,
            "opportunity":4.5,"market_size":3.5,"supply_demand":5.0,"developed_scarcity":5.0,
            "value_added":4.5,"cost_performance":4.0,"stability":5.5,"safety":6.5,
            "occupational_disease":5.5,"overtime":4.5,"burnout":3.5,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":2.5,
            "ai_resistance":7.5,"social_status":6.0,"remote_friendly":3.0,"autonomy":5.5,
            "family_friendly":4.0,"fulfillment":8.5,"entrepreneurship":2.5,"gender_equality":6.5,
            "age_flexibility":6.5,"social_interaction":9.0,"physical_demand":3.0,"license_barrier":5.0,
            "cycle_sensitivity":3.0,"side_job_compat":2.0,"intl_mobility":8.5,"industry_monopoly":3.5,
            "trend_long":2,"trend_short":2,"edu":"本科/硕士","age":"23-30",
        },
        "0706": {  # Human Rights Advocate
            "learning_cost":5.5,"education_req":5.5,"growth_coeff":5.0,"career_lifespan":7.0,
            "opportunity":4.0,"market_size":3.0,"supply_demand":4.5,"developed_scarcity":4.5,
            "value_added":4.0,"cost_performance":3.5,"stability":4.5,"safety":5.5,
            "occupational_disease":5.5,"overtime":4.0,"burnout":3.0,
            "skill_versatility":6.0,"career_switch":5.5,"reputation_variance":3.5,
            "ai_resistance":8.0,"social_status":7.0,"remote_friendly":4.5,"autonomy":7.0,
            "family_friendly":4.0,"fulfillment":9.0,"entrepreneurship":4.0,"gender_equality":7.0,
            "age_flexibility":6.5,"social_interaction":9.0,"physical_demand":2.5,"license_barrier":3.0,
            "cycle_sensitivity":2.5,"side_job_compat":3.0,"intl_mobility":8.5,"industry_monopoly":2.5,
            "trend_long":1,"trend_short":1,"edu":"本科/硕士","age":"23-30",
        },
        "0707": {  # Disaster Relief Worker
            "learning_cost":4.5,"education_req":4.5,"growth_coeff":5.0,"career_lifespan":6.5,
            "opportunity":5.0,"market_size":4.5,"supply_demand":5.0,"developed_scarcity":4.5,
            "value_added":3.5,"cost_performance":3.5,"stability":4.0,"safety":4.0,
            "occupational_disease":4.0,"overtime":3.0,"burnout":2.5,
            "skill_versatility":6.0,"career_switch":5.0,"reputation_variance":2.0,
            "ai_resistance":8.5,"social_status":6.5,"remote_friendly":1.5,"autonomy":6.0,
            "family_friendly":2.5,"fulfillment":8.5,"entrepreneurship":2.5,"gender_equality":6.0,
            "age_flexibility":5.5,"social_interaction":8.5,"physical_demand":7.0,"license_barrier":3.5,
            "cycle_sensitivity":3.5,"side_job_compat":2.0,"intl_mobility":8.5,"industry_monopoly":2.5,
            "trend_long":2,"trend_short":2,"edu":"本科/培训","age":"22-30",
        },
        "0708": {  # Environmental NGO Advocate
            "learning_cost":5.0,"education_req":5.0,"growth_coeff":6.0,"career_lifespan":7.0,
            "opportunity":5.0,"market_size":4.0,"supply_demand":5.0,"developed_scarcity":4.5,
            "value_added":4.0,"cost_performance":3.5,"stability":4.5,"safety":7.0,
            "occupational_disease":6.0,"overtime":4.5,"burnout":3.5,
            "skill_versatility":6.0,"career_switch":5.5,"reputation_variance":2.5,
            "ai_resistance":7.5,"social_status":6.5,"remote_friendly":5.0,"autonomy":7.0,
            "family_friendly":4.5,"fulfillment":8.5,"entrepreneurship":5.0,"gender_equality":7.0,
            "age_flexibility":6.5,"social_interaction":8.5,"physical_demand":3.0,"license_barrier":2.5,
            "cycle_sensitivity":3.0,"side_job_compat":3.5,"intl_mobility":7.5,"industry_monopoly":2.5,
            "trend_long":3,"trend_short":3,"edu":"本科/硕士","age":"22-30",
        },
        # ===== RELIGIOUS (08xx) =====
        "0801": {  # Christian Pastor / Minister
            "learning_cost":5.5,"education_req":5.0,"growth_coeff":3.5,"career_lifespan":9.0,
            "opportunity":5.0,"market_size":5.5,"supply_demand":4.5,"developed_scarcity":4.0,
            "value_added":4.0,"cost_performance":4.0,"stability":7.0,"safety":8.5,
            "occupational_disease":6.5,"overtime":4.5,"burnout":4.0,
            "skill_versatility":5.5,"career_switch":4.5,"reputation_variance":3.0,
            "ai_resistance":9.0,"social_status":7.0,"remote_friendly":3.0,"autonomy":7.5,
            "family_friendly":5.5,"fulfillment":9.0,"entrepreneurship":4.5,"gender_equality":5.0,
            "age_flexibility":8.5,"social_interaction":9.5,"physical_demand":1.5,"license_barrier":5.5,
            "cycle_sensitivity":1.0,"side_job_compat":3.5,"intl_mobility":5.5,"industry_monopoly":3.5,
            "trend_long":0,"trend_short":0,"edu":"神学本科/硕士","age":"24-35",
        },
        "0802": {  # Buddhist Monk / Nun
            "learning_cost":4.0,"education_req":3.0,"growth_coeff":2.5,"career_lifespan":9.5,
            "opportunity":3.0,"market_size":3.0,"supply_demand":3.0,"developed_scarcity":3.0,
            "value_added":2.0,"cost_performance":3.0,"stability":7.5,"safety":9.0,
            "occupational_disease":7.5,"overtime":7.0,"burnout":7.0,
            "skill_versatility":3.5,"career_switch":3.0,"reputation_variance":2.0,
            "ai_resistance":9.5,"social_status":7.0,"remote_friendly":2.0,"autonomy":7.0,
            "family_friendly":2.0,"fulfillment":9.0,"entrepreneurship":2.0,"gender_equality":3.5,
            "age_flexibility":9.0,"social_interaction":7.5,"physical_demand":3.0,"license_barrier":5.0,
            "cycle_sensitivity":0.5,"side_job_compat":1.0,"intl_mobility":4.0,"industry_monopoly":4.0,
            "trend_long":-1,"trend_short":-1,"edu":"寺院教育","age":"15-30",
        },
        "0803": {  # Islamic Imam
            "learning_cost":5.5,"education_req":5.0,"growth_coeff":3.5,"career_lifespan":9.0,
            "opportunity":5.0,"market_size":5.0,"supply_demand":4.5,"developed_scarcity":4.0,
            "value_added":3.5,"cost_performance":3.5,"stability":7.0,"safety":7.0,
            "occupational_disease":6.5,"overtime":4.5,"burnout":4.5,
            "skill_versatility":4.5,"career_switch":3.5,"reputation_variance":3.5,
            "ai_resistance":9.0,"social_status":7.5,"remote_friendly":2.5,"autonomy":7.0,
            "family_friendly":5.5,"fulfillment":8.5,"entrepreneurship":3.5,"gender_equality":2.5,
            "age_flexibility":8.0,"social_interaction":9.5,"physical_demand":1.5,"license_barrier":6.0,
            "cycle_sensitivity":0.5,"side_job_compat":3.0,"intl_mobility":5.0,"industry_monopoly":4.5,
            "trend_long":1,"trend_short":0,"edu":"伊斯兰学院","age":"22-30",
        },
        "0804": {  # Rabbi
            "learning_cost":7.0,"education_req":7.0,"growth_coeff":3.5,"career_lifespan":9.0,
            "opportunity":3.0,"market_size":2.0,"supply_demand":4.0,"developed_scarcity":4.5,
            "value_added":5.0,"cost_performance":4.5,"stability":7.5,"safety":7.5,
            "occupational_disease":6.5,"overtime":5.0,"burnout":5.0,
            "skill_versatility":5.5,"career_switch":4.5,"reputation_variance":2.0,
            "ai_resistance":9.0,"social_status":8.0,"remote_friendly":3.0,"autonomy":7.5,
            "family_friendly":5.5,"fulfillment":8.5,"entrepreneurship":4.0,"gender_equality":4.0,
            "age_flexibility":8.5,"social_interaction":9.5,"physical_demand":1.0,"license_barrier":7.5,
            "cycle_sensitivity":0.5,"side_job_compat":3.0,"intl_mobility":5.5,"industry_monopoly":4.5,
            "trend_long":0,"trend_short":0,"edu":"犹太神学院","age":"25-32",
        },
        "0805": {  # Catholic Priest
            "learning_cost":6.5,"education_req":6.0,"growth_coeff":2.5,"career_lifespan":9.5,
            "opportunity":3.5,"market_size":4.5,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":3.5,"cost_performance":3.5,"stability":8.0,"safety":8.0,
            "occupational_disease":6.5,"overtime":5.0,"burnout":4.5,
            "skill_versatility":4.5,"career_switch":3.5,"reputation_variance":3.5,
            "ai_resistance":9.0,"social_status":7.5,"remote_friendly":2.5,"autonomy":6.5,
            "family_friendly":2.0,"fulfillment":9.0,"entrepreneurship":2.0,"gender_equality":1.5,
            "age_flexibility":8.5,"social_interaction":9.0,"physical_demand":1.5,"license_barrier":7.0,
            "cycle_sensitivity":0.5,"side_job_compat":1.5,"intl_mobility":6.0,"industry_monopoly":5.0,
            "trend_long":-1,"trend_short":-1,"edu":"神学院","age":"25-35",
        },
        "0806": {  # Taoist Priest
            "learning_cost":4.5,"education_req":3.5,"growth_coeff":2.5,"career_lifespan":9.0,
            "opportunity":2.5,"market_size":2.0,"supply_demand":3.0,"developed_scarcity":3.0,
            "value_added":2.5,"cost_performance":3.0,"stability":6.5,"safety":9.0,
            "occupational_disease":7.5,"overtime":6.5,"burnout":6.5,
            "skill_versatility":3.0,"career_switch":3.0,"reputation_variance":2.5,
            "ai_resistance":9.5,"social_status":5.5,"remote_friendly":2.0,"autonomy":7.0,
            "family_friendly":5.0,"fulfillment":8.0,"entrepreneurship":3.0,"gender_equality":4.5,
            "age_flexibility":9.0,"social_interaction":7.0,"physical_demand":2.5,"license_barrier":4.5,
            "cycle_sensitivity":0.5,"side_job_compat":2.5,"intl_mobility":2.0,"industry_monopoly":4.0,
            "trend_long":-1,"trend_short":0,"edu":"道观教育","age":"18-30",
        },
        "0807": {  # Hindu Priest (Pandit)
            "learning_cost":4.5,"education_req":3.5,"growth_coeff":3.0,"career_lifespan":9.0,
            "opportunity":4.0,"market_size":4.0,"supply_demand":3.5,"developed_scarcity":3.0,
            "value_added":3.0,"cost_performance":3.5,"stability":6.5,"safety":8.5,
            "occupational_disease":7.0,"overtime":5.0,"burnout":5.5,
            "skill_versatility":3.5,"career_switch":3.0,"reputation_variance":3.0,
            "ai_resistance":9.5,"social_status":7.0,"remote_friendly":2.0,"autonomy":7.0,
            "family_friendly":5.5,"fulfillment":8.5,"entrepreneurship":4.0,"gender_equality":2.5,
            "age_flexibility":8.5,"social_interaction":9.0,"physical_demand":2.0,"license_barrier":5.0,
            "cycle_sensitivity":0.5,"side_job_compat":3.5,"intl_mobility":4.5,"industry_monopoly":4.0,
            "trend_long":0,"trend_short":0,"edu":"家族传承/学院","age":"18-30",
        },
        "0808": {  # Military Chaplain
            "learning_cost":6.0,"education_req":6.0,"growth_coeff":3.5,"career_lifespan":8.0,
            "opportunity":3.0,"market_size":2.5,"supply_demand":4.5,"developed_scarcity":5.0,
            "value_added":5.5,"cost_performance":5.0,"stability":8.0,"safety":6.5,
            "occupational_disease":5.5,"overtime":5.0,"burnout":4.0,
            "skill_versatility":5.0,"career_switch":4.5,"reputation_variance":2.0,
            "ai_resistance":9.0,"social_status":7.0,"remote_friendly":1.5,"autonomy":5.5,
            "family_friendly":4.0,"fulfillment":8.5,"entrepreneurship":1.5,"gender_equality":4.5,
            "age_flexibility":7.5,"social_interaction":9.0,"physical_demand":3.0,"license_barrier":7.0,
            "cycle_sensitivity":1.0,"side_job_compat":1.0,"intl_mobility":5.5,"industry_monopoly":6.5,
            "trend_long":0,"trend_short":0,"edu":"神学硕士+军事训练","age":"26-35",
        },
        # ===== PSYCHOSOCIAL_SERVICES (09xx) =====
        "0901": {  # Marriage & Family Therapist
            "learning_cost":6.5,"education_req":6.5,"growth_coeff":5.5,"career_lifespan":8.0,
            "opportunity":5.5,"market_size":5.0,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":5.5,"cost_performance":5.0,"stability":6.5,"safety":9.0,
            "occupational_disease":6.0,"overtime":5.5,"burnout":4.0,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":2.0,
            "ai_resistance":8.0,"social_status":6.5,"remote_friendly":6.0,"autonomy":7.5,
            "family_friendly":6.0,"fulfillment":7.5,"entrepreneurship":7.0,"gender_equality":7.5,
            "age_flexibility":7.5,"social_interaction":9.5,"physical_demand":0.5,"license_barrier":7.0,
            "cycle_sensitivity":2.0,"side_job_compat":5.5,"intl_mobility":4.5,"industry_monopoly":3.0,
            "trend_long":2,"trend_short":2,"edu":"硕士/博士","age":"26-32",
        },
        "0902": {  # Substance Abuse Counselor
            "learning_cost":5.0,"education_req":5.0,"growth_coeff":5.0,"career_lifespan":7.0,
            "opportunity":5.5,"market_size":5.0,"supply_demand":5.5,"developed_scarcity":5.0,
            "value_added":4.0,"cost_performance":4.0,"stability":6.0,"safety":7.5,
            "occupational_disease":5.5,"overtime":5.0,"burnout":3.0,
            "skill_versatility":5.0,"career_switch":4.5,"reputation_variance":2.5,
            "ai_resistance":8.0,"social_status":5.5,"remote_friendly":4.0,"autonomy":6.0,
            "family_friendly":5.0,"fulfillment":7.5,"entrepreneurship":4.5,"gender_equality":7.0,
            "age_flexibility":7.0,"social_interaction":9.0,"physical_demand":1.5,"license_barrier":6.0,
            "cycle_sensitivity":2.0,"side_job_compat":4.0,"intl_mobility":4.0,"industry_monopoly":3.5,
            "trend_long":2,"trend_short":1,"edu":"本科/硕士","age":"24-30",
        },
        "0903": {  # Crisis Intervention Counselor
            "learning_cost":5.5,"education_req":5.5,"growth_coeff":5.5,"career_lifespan":7.0,
            "opportunity":5.5,"market_size":4.5,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":4.5,"cost_performance":4.0,"stability":6.0,"safety":6.5,
            "occupational_disease":5.0,"overtime":4.0,"burnout":2.5,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":2.0,
            "ai_resistance":8.5,"social_status":6.0,"remote_friendly":4.0,"autonomy":6.0,
            "family_friendly":4.5,"fulfillment":8.0,"entrepreneurship":3.5,"gender_equality":7.0,
            "age_flexibility":6.5,"social_interaction":9.5,"physical_demand":2.0,"license_barrier":6.5,
            "cycle_sensitivity":2.0,"side_job_compat":3.5,"intl_mobility":5.0,"industry_monopoly":3.5,
            "trend_long":2,"trend_short":2,"edu":"硕士","age":"24-30",
        },
        "0904": {  # Vocational Rehabilitation Counselor
            "learning_cost":5.5,"education_req":5.5,"growth_coeff":5.0,"career_lifespan":7.5,
            "opportunity":5.0,"market_size":4.5,"supply_demand":5.0,"developed_scarcity":5.0,
            "value_added":4.5,"cost_performance":4.5,"stability":6.5,"safety":9.0,
            "occupational_disease":6.5,"overtime":6.0,"burnout":5.0,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":1.5,
            "ai_resistance":7.5,"social_status":5.5,"remote_friendly":4.5,"autonomy":6.0,
            "family_friendly":6.0,"fulfillment":7.5,"entrepreneurship":4.0,"gender_equality":7.0,
            "age_flexibility":7.0,"social_interaction":8.5,"physical_demand":1.5,"license_barrier":6.0,
            "cycle_sensitivity":2.5,"side_job_compat":4.0,"intl_mobility":4.5,"industry_monopoly":4.0,
            "trend_long":1,"trend_short":1,"edu":"硕士","age":"24-30",
        },
        "0905": {  # Bounty Hunter / Bail Enforcement Agent
            "learning_cost":3.0,"education_req":2.5,"growth_coeff":3.0,"career_lifespan":5.5,
            "opportunity":3.0,"market_size":2.0,"supply_demand":4.0,"developed_scarcity":3.5,
            "value_added":4.5,"cost_performance":4.5,"stability":3.5,"safety":3.0,
            "occupational_disease":3.5,"overtime":3.5,"burnout":3.5,
            "skill_versatility":4.0,"career_switch":4.0,"reputation_variance":4.5,
            "ai_resistance":7.5,"social_status":3.5,"remote_friendly":1.0,"autonomy":8.0,
            "family_friendly":3.0,"fulfillment":5.5,"entrepreneurship":7.0,"gender_equality":3.5,
            "age_flexibility":5.0,"social_interaction":7.0,"physical_demand":7.5,"license_barrier":5.5,
            "cycle_sensitivity":3.0,"side_job_compat":5.0,"intl_mobility":1.5,"industry_monopoly":3.0,
            "trend_long":0,"trend_short":-1,"edu":"高中/培训","age":"21-35",
        },
        "0906": {  # Bail Bondsman
            "learning_cost":3.0,"education_req":3.0,"growth_coeff":3.0,"career_lifespan":6.5,
            "opportunity":3.5,"market_size":2.5,"supply_demand":4.0,"developed_scarcity":3.5,
            "value_added":5.5,"cost_performance":5.5,"stability":4.5,"safety":5.5,
            "occupational_disease":5.5,"overtime":4.5,"burnout":4.5,
            "skill_versatility":4.0,"career_switch":4.5,"reputation_variance":4.0,
            "ai_resistance":6.5,"social_status":4.0,"remote_friendly":3.0,"autonomy":7.5,
            "family_friendly":4.5,"fulfillment":4.5,"entrepreneurship":8.0,"gender_equality":4.5,
            "age_flexibility":6.5,"social_interaction":7.5,"physical_demand":3.0,"license_barrier":5.5,
            "cycle_sensitivity":3.5,"side_job_compat":4.0,"intl_mobility":1.5,"industry_monopoly":4.0,
            "trend_long":0,"trend_short":-1,"edu":"高中/大专","age":"22-35",
        },
        "0907": {  # Domestic Violence Advocate
            "learning_cost":4.5,"education_req":4.5,"growth_coeff":5.0,"career_lifespan":7.0,
            "opportunity":5.0,"market_size":4.5,"supply_demand":5.0,"developed_scarcity":5.0,
            "value_added":3.5,"cost_performance":3.5,"stability":5.5,"safety":6.5,
            "occupational_disease":5.0,"overtime":4.5,"burnout":3.0,
            "skill_versatility":5.5,"career_switch":5.0,"reputation_variance":2.0,
            "ai_resistance":8.5,"social_status":5.5,"remote_friendly":3.5,"autonomy":5.5,
            "family_friendly":4.5,"fulfillment":8.0,"entrepreneurship":3.0,"gender_equality":8.0,
            "age_flexibility":7.0,"social_interaction":9.0,"physical_demand":2.5,"license_barrier":4.5,
            "cycle_sensitivity":2.0,"side_job_compat":3.0,"intl_mobility":5.0,"industry_monopoly":3.5,
            "trend_long":2,"trend_short":2,"edu":"本科/硕士","age":"23-30",
        },
        "0908": {  # Estate Planning Advisor
            "learning_cost":7.0,"education_req":7.0,"growth_coeff":5.5,"career_lifespan":8.5,
            "opportunity":5.5,"market_size":4.5,"supply_demand":5.5,"developed_scarcity":5.5,
            "value_added":7.5,"cost_performance":6.5,"stability":7.0,"safety":9.5,
            "occupational_disease":6.5,"overtime":5.5,"burnout":5.5,
            "skill_versatility":5.5,"career_switch":5.5,"reputation_variance":1.5,
            "ai_resistance":6.0,"social_status":7.0,"remote_friendly":5.5,"autonomy":7.0,
            "family_friendly":5.5,"fulfillment":6.5,"entrepreneurship":7.0,"gender_equality":5.5,
            "age_flexibility":7.5,"social_interaction":7.5,"physical_demand":0.5,"license_barrier":7.5,
            "cycle_sensitivity":2.5,"side_job_compat":4.0,"intl_mobility":5.0,"industry_monopoly":4.0,
            "trend_long":2,"trend_short":1,"edu":"法学/金融硕士","age":"26-32",
        },
        # ===== COMPLIANCE_REGULATION (10xx) =====
        "1001": {  # Data Protection Officer (DPO)
            "learning_cost":6.5,"education_req":6.5,"growth_coeff":8.0,"career_lifespan":7.0,
            "opportunity":7.5,"market_size":5.0,"supply_demand":7.5,"developed_scarcity":7.5,
            "value_added":7.5,"cost_performance":7.0,"stability":7.0,"safety":9.5,
            "occupational_disease":6.5,"overtime":5.5,"burnout":5.0,
            "skill_versatility":7.0,"career_switch":6.5,"reputation_variance":1.5,
            "ai_resistance":6.0,"social_status":7.0,"remote_friendly":7.0,"autonomy":7.0,
            "family_friendly":6.0,"fulfillment":6.5,"entrepreneurship":6.0,"gender_equality":6.5,
            "age_flexibility":6.5,"social_interaction":7.0,"physical_demand":0.5,"license_barrier":6.5,
            "cycle_sensitivity":2.5,"side_job_compat":4.5,"intl_mobility":7.5,"industry_monopoly":3.0,
            "trend_long":4,"trend_short":4,"edu":"法学/IT硕士","age":"26-32",
        },
        "1002": {  # Regulatory Affairs Specialist
            "learning_cost":6.0,"education_req":6.0,"growth_coeff":5.5,"career_lifespan":8.0,
            "opportunity":6.0,"market_size":5.5,"supply_demand":6.0,"developed_scarcity":5.5,
            "value_added":6.5,"cost_performance":6.0,"stability":7.0,"safety":9.5,
            "occupational_disease":7.0,"overtime":6.0,"burnout":5.5,
            "skill_versatility":5.5,"career_switch":5.5,"reputation_variance":1.5,
            "ai_resistance":5.5,"social_status":6.5,"remote_friendly":6.0,"autonomy":6.0,
            "family_friendly":6.0,"fulfillment":5.5,"entrepreneurship":4.5,"gender_equality":6.0,
            "age_flexibility":7.0,"social_interaction":7.0,"physical_demand":0.5,"license_barrier":6.0,
            "cycle_sensitivity":2.5,"side_job_compat":3.5,"intl_mobility":6.0,"industry_monopoly":4.0,
            "trend_long":2,"trend_short":2,"edu":"本科/硕士","age":"24-30",
        },
        "1003": {  # Antitrust Compliance Specialist
            "learning_cost":7.0,"education_req":7.0,"growth_coeff":6.0,"career_lifespan":7.5,
            "opportunity":5.5,"market_size":3.5,"supply_demand":6.0,"developed_scarcity":6.5,
            "value_added":7.5,"cost_performance":6.5,"stability":7.0,"safety":9.5,
            "occupational_disease":6.5,"overtime":5.0,"burnout":5.0,
            "skill_versatility":5.5,"career_switch":5.5,"reputation_variance":1.5,
            "ai_resistance":6.0,"social_status":7.0,"remote_friendly":6.0,"autonomy":6.5,
            "family_friendly":5.5,"fulfillment":6.0,"entrepreneurship":4.5,"gender_equality":5.5,
            "age_flexibility":6.5,"social_interaction":7.0,"physical_demand":0.5,"license_barrier":7.0,
            "cycle_sensitivity":2.5,"side_job_compat":3.0,"intl_mobility":7.0,"industry_monopoly":4.5,
            "trend_long":2,"trend_short":2,"edu":"法学/经济学硕士","age":"25-32",
        },
        "1004": {  # Trade Compliance Specialist
            "learning_cost":6.0,"education_req":6.0,"growth_coeff":6.0,"career_lifespan":7.5,
            "opportunity":6.0,"market_size":4.5,"supply_demand":6.0,"developed_scarcity":5.5,
            "value_added":6.5,"cost_performance":6.0,"stability":7.0,"safety":9.5,
            "occupational_disease":7.0,"overtime":5.5,"burnout":5.5,
            "skill_versatility":5.5,"career_switch":5.5,"reputation_variance":1.5,
            "ai_resistance":5.5,"social_status":6.5,"remote_friendly":6.0,"autonomy":6.0,
            "family_friendly":5.5,"fulfillment":5.5,"entrepreneurship":4.5,"gender_equality":5.5,
            "age_flexibility":7.0,"social_interaction":7.0,"physical_demand":0.5,"license_barrier":6.0,
            "cycle_sensitivity":4.0,"side_job_compat":3.0,"intl_mobility":7.5,"industry_monopoly":4.0,
            "trend_long":2,"trend_short":2,"edu":"本科/硕士","age":"24-30",
        },
        "1005": {  # Election Observer / Monitor
            "learning_cost":4.0,"education_req":4.0,"growth_coeff":4.0,"career_lifespan":6.0,
            "opportunity":3.5,"market_size":2.5,"supply_demand":4.0,"developed_scarcity":4.0,
            "value_added":3.5,"cost_performance":3.5,"stability":4.0,"safety":6.0,
            "occupational_disease":6.0,"overtime":4.5,"burnout":5.0,
            "skill_versatility":5.0,"career_switch":5.0,"reputation_variance":2.5,
            "ai_resistance":7.5,"social_status":6.0,"remote_friendly":2.0,"autonomy":5.5,
            "family_friendly":4.0,"fulfillment":7.0,"entrepreneurship":2.0,"gender_equality":6.0,
            "age_flexibility":7.0,"social_interaction":8.0,"physical_demand":3.0,"license_barrier":4.5,
            "cycle_sensitivity":3.5,"side_job_compat":5.0,"intl_mobility":7.5,"industry_monopoly":3.5,
            "trend_long":1,"trend_short":0,"edu":"本科","age":"25-40",
        },
        "1006": {  # Intellectual Property Analyst
            "learning_cost":6.5,"education_req":6.5,"growth_coeff":6.5,"career_lifespan":7.5,
            "opportunity":6.0,"market_size":4.5,"supply_demand":6.0,"developed_scarcity":6.0,
            "value_added":7.0,"cost_performance":6.5,"stability":7.0,"safety":9.5,
            "occupational_disease":6.5,"overtime":5.5,"burnout":5.0,
            "skill_versatility":6.0,"career_switch":6.0,"reputation_variance":1.5,
            "ai_resistance":5.5,"social_status":6.5,"remote_friendly":6.5,"autonomy":6.5,
            "family_friendly":5.5,"fulfillment":6.5,"entrepreneurship":6.0,"gender_equality":6.0,
            "age_flexibility":6.5,"social_interaction":6.5,"physical_demand":0.5,"license_barrier":6.5,
            "cycle_sensitivity":3.0,"side_job_compat":4.5,"intl_mobility":7.0,"industry_monopoly":3.5,
            "trend_long":3,"trend_short":2,"edu":"理工+法学","age":"24-30",
        },
        "1007": {  # Legal Tech Product Manager
            "learning_cost":6.5,"education_req":6.0,"growth_coeff":8.0,"career_lifespan":6.5,
            "opportunity":7.0,"market_size":3.5,"supply_demand":7.5,"developed_scarcity":7.5,
            "value_added":8.0,"cost_performance":7.0,"stability":5.5,"safety":9.5,
            "occupational_disease":6.5,"overtime":4.5,"burnout":4.5,
            "skill_versatility":7.5,"career_switch":7.0,"reputation_variance":2.0,
            "ai_resistance":5.5,"social_status":7.0,"remote_friendly":7.5,"autonomy":7.5,
            "family_friendly":5.5,"fulfillment":7.0,"entrepreneurship":8.5,"gender_equality":6.0,
            "age_flexibility":5.5,"social_interaction":7.5,"physical_demand":0.5,"license_barrier":3.5,
            "cycle_sensitivity":5.0,"side_job_compat":5.0,"intl_mobility":7.5,"industry_monopoly":3.0,
            "trend_long":4,"trend_short":5,"edu":"法学+技术背景","age":"26-32",
        },
        "1008": {  # Legal AI Trainer / Specialist
            "learning_cost":5.5,"education_req":5.5,"growth_coeff":7.5,"career_lifespan":5.5,
            "opportunity":6.5,"market_size":3.0,"supply_demand":7.0,"developed_scarcity":7.0,
            "value_added":6.5,"cost_performance":6.5,"stability":5.0,"safety":9.5,
            "occupational_disease":6.5,"overtime":5.0,"burnout":5.0,
            "skill_versatility":6.5,"career_switch":6.5,"reputation_variance":2.5,
            "ai_resistance":4.5,"social_status":6.0,"remote_friendly":8.0,"autonomy":7.0,
            "family_friendly":6.0,"fulfillment":6.5,"entrepreneurship":7.0,"gender_equality":6.5,
            "age_flexibility":6.0,"social_interaction":6.0,"physical_demand":0.5,"license_barrier":3.5,
            "cycle_sensitivity":5.0,"side_job_compat":6.0,"intl_mobility":7.0,"industry_monopoly":3.5,
            "trend_long":3,"trend_short":5,"edu":"法学+AI/数据","age":"24-30",
        },
    }
    return B.get(oid, {})


# ---------------------------------------------------------------------------
# SCORE DIMENSIONS & HELPERS
# ---------------------------------------------------------------------------
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

def clamp(v, lo=0.0, hi=10.0): return max(lo, min(hi, round(v, 1)))
def clamp5(v): return max(0.0, min(5.0, round(v, 1)))


def apply_country_modifiers(base, cp, oid):
    """Adjust base scores using LAW-specific country profiles."""
    s = dict(base)
    mid = oid[:2]  # first 2 digits -> mid-category

    # Core factors normalized to approx [-1, +1]
    law_f   = (cp["legal_market"] - 6.0) / 4.0
    rol_f   = (cp["rule_of_law"] - 6.0) / 4.0
    pay_f   = (cp["lawyer_pay"] - 5.5) / 4.5
    ngo_f   = (cp["ngo_sector"] - 5.5) / 4.5
    rel_f   = (cp["religious_diversity"] - 5.0) / 5.0
    soc_f   = (cp["social_services"] - 6.0) / 4.0
    wlb_f   = (cp["wlb"] - 6.0) / 4.0
    gender_f= (cp["gender"] - 5.5) / 4.5
    intl_f  = (cp["intl"] - 6.0) / 4.0
    comp_f  = (cp["comp"] - 5.5) / 4.5
    edu_f   = (cp["edu"] - 6.0) / 4.0
    reg_f   = (cp["reg"] - 5.5) / 4.5

    # --- Value added / pay: lawyers driven by lawyer_pay; social/NGO by social_services
    if mid in ("01","02","03","04"):  # legal roles
        s["value_added"] = clamp(s["value_added"] + pay_f * 2.0)
        s["cost_performance"] = clamp(s["cost_performance"] + pay_f * 1.0 + rol_f * 0.5)
    elif mid in ("06","07"):  # social work / NGO
        s["value_added"] = clamp(s["value_added"] + soc_f * 1.0 + ngo_f * 0.5)
        s["cost_performance"] = clamp(s["cost_performance"] + soc_f * 0.8)
    elif mid == "08":  # religious
        s["value_added"] = clamp(s["value_added"] + rel_f * 0.5 + comp_f * 0.5)
        s["cost_performance"] = clamp(s["cost_performance"] + comp_f * 0.5)
    else:  # psychosocial, compliance
        s["value_added"] = clamp(s["value_added"] + comp_f * 1.5)
        s["cost_performance"] = clamp(s["cost_performance"] + comp_f * 1.0)

    # --- Stability: rule of law is primary driver for legal; social_services for social
    if mid in ("01","02","03","04","05"):
        s["stability"] = clamp(s["stability"] + rol_f * 1.5)
    elif mid in ("06","07"):
        s["stability"] = clamp(s["stability"] + soc_f * 1.0 + ngo_f * 0.5)
    elif mid == "08":
        s["stability"] = clamp(s["stability"] + rel_f * 0.5)
    else:
        s["stability"] = clamp(s["stability"] + rol_f * 1.0)

    # --- Growth: legal_market drives lawyer growth; ngo_sector drives NGO
    if mid in ("01","02","03","04","05","10"):
        s["growth_coeff"] = clamp(s["growth_coeff"] + law_f * 0.8 + rol_f * 0.3)
    elif mid in ("06","07"):
        s["growth_coeff"] = clamp(s["growth_coeff"] + ngo_f * 0.8 + soc_f * 0.3)
    elif mid == "08":
        s["growth_coeff"] = clamp(s["growth_coeff"] + rel_f * 0.5)
    else:
        s["growth_coeff"] = clamp(s["growth_coeff"] + law_f * 0.5 + soc_f * 0.3)

    # --- Career lifespan: longer where rule_of_law is strong
    s["career_lifespan"] = clamp(s["career_lifespan"] + rol_f * 0.5)

    # --- Opportunity & market size
    if mid in ("01","02","03","04","05","10"):
        s["opportunity"] = clamp(s["opportunity"] + law_f * 1.2)
        s["market_size"] = clamp(s["market_size"] + law_f * 1.5)
    elif mid in ("06","07"):
        s["opportunity"] = clamp(s["opportunity"] + ngo_f * 1.0 + soc_f * 0.5)
        s["market_size"] = clamp(s["market_size"] + soc_f * 1.0 + ngo_f * 0.5)
    elif mid == "08":
        s["opportunity"] = clamp(s["opportunity"] + rel_f * 1.0)
        s["market_size"] = clamp(s["market_size"] + rel_f * 1.0)
    else:
        s["opportunity"] = clamp(s["opportunity"] + law_f * 0.5 + soc_f * 0.5)
        s["market_size"] = clamp(s["market_size"] + law_f * 0.5 + soc_f * 0.5)

    # --- Supply-demand & developed scarcity
    s["supply_demand"] = clamp(s["supply_demand"] + law_f * 0.5 + rol_f * 0.5)
    dev_bonus = 0.8 if cp["rule_of_law"] >= 7.5 else (-0.5 if cp["rule_of_law"] < 5.0 else 0.0)
    s["developed_scarcity"] = clamp(s["developed_scarcity"] + dev_bonus)

    # --- Safety: rule_of_law affects safety for lawyers/prosecutors
    if mid in ("01","02","03"):
        s["safety"] = clamp(s["safety"] + rol_f * 0.8)
    else:
        s["safety"] = clamp(s["safety"] + rol_f * 0.3)

    # --- Overtime / burnout: WLB-driven
    s["overtime"] = clamp(s["overtime"] + wlb_f * 1.5)
    s["burnout"] = clamp(s["burnout"] + wlb_f * 1.0)
    s["occupational_disease"] = clamp(s["occupational_disease"] + wlb_f * 0.8)

    # --- Remote friendly: slightly better where legal market is digital
    s["remote_friendly"] = clamp(s["remote_friendly"] + law_f * 0.5 + wlb_f * 0.3)

    # --- Autonomy
    s["autonomy"] = clamp(s["autonomy"] + rol_f * 0.5 + wlb_f * 0.3)

    # --- Family friendly
    s["family_friendly"] = clamp(s["family_friendly"] + wlb_f * 1.5)

    # --- Social status: lawyers high where legal market is large
    if mid in ("01","02","03","04"):
        s["social_status"] = clamp(s["social_status"] + law_f * 0.8 + pay_f * 0.5)
    elif mid == "08":
        s["social_status"] = clamp(s["social_status"] + rel_f * 0.8)
    else:
        s["social_status"] = clamp(s["social_status"] + soc_f * 0.5)

    # --- NGO-specific: fulfillment, intl_mobility
    if mid == "07":
        s["fulfillment"] = clamp(s["fulfillment"] + ngo_f * 0.5)
        s["intl_mobility"] = clamp(s["intl_mobility"] + intl_f * 1.2 + ngo_f * 0.5)
    else:
        s["fulfillment"] = clamp(s["fulfillment"] + rol_f * 0.3)
        s["intl_mobility"] = clamp(s["intl_mobility"] + intl_f * 1.0)

    # --- Religious-specific: religious_diversity drives opportunity
    if mid == "08":
        s["fulfillment"] = clamp(s["fulfillment"] + rel_f * 0.3)

    # --- License barrier: higher in regulated legal markets
    if mid in ("01","02","03","04"):
        s["license_barrier"] = clamp(s["license_barrier"] + reg_f * 0.5 + rol_f * 0.3)
    else:
        s["license_barrier"] = clamp(s["license_barrier"] + reg_f * 0.3)

    # --- Gender equality
    s["gender_equality"] = clamp(s["gender_equality"] + gender_f * 2.0)

    # --- Age flexibility
    s["age_flexibility"] = clamp(s["age_flexibility"] + wlb_f * 0.5)

    # --- Entrepreneurship: higher where legal market is developed
    s["entrepreneurship"] = clamp(s["entrepreneurship"] + law_f * 0.5 + reg_f * 0.3)

    # --- AI resistance: minimal country variation
    s["ai_resistance"] = clamp(s["ai_resistance"] + edu_f * 0.2)

    # --- Education / learning cost
    s["learning_cost"] = clamp(s["learning_cost"] + edu_f * 0.3)
    s["education_req"] = clamp(s["education_req"] + edu_f * 0.3)

    # --- Skill versatility / career switch
    s["skill_versatility"] = clamp(s["skill_versatility"] + law_f * 0.3 + edu_f * 0.2)
    s["career_switch"] = clamp(s["career_switch"] + law_f * 0.3)

    # --- Reputation variance: higher where rule_of_law is weak
    s["reputation_variance"] = clamp5(s["reputation_variance"] - rol_f * 0.5)

    # --- Cycle sensitivity
    s["cycle_sensitivity"] = clamp(s["cycle_sensitivity"] - rol_f * 0.3)

    # --- Side job
    s["side_job_compat"] = clamp(s["side_job_compat"] + wlb_f * 0.3 + law_f * 0.2)

    # --- Industry monopoly
    s["industry_monopoly"] = clamp(s["industry_monopoly"] + reg_f * 0.3)

    return s


def get_trends(base, cp):
    t_long = base["trend_long"]
    t_short = base["trend_short"]
    if cp["legal_market"] >= 8.0:
        t_short = min(5, t_short + 1)
    elif cp["legal_market"] < 5.0:
        t_short = max(-5, t_short - 1)
    if cp["rule_of_law"] >= 8.0:
        t_long = min(5, t_long)
    elif cp["rule_of_law"] < 4.5:
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
    if scores["value_added"] >= 8.0:
        hz.append("薪资回报高"); he.append("high compensation")
    elif scores["value_added"] <= 4.0:
        hz.append("薪资水平偏低"); he.append("relatively low pay")
    if scores["license_barrier"] >= 8.0:
        hz.append("准入门槛高"); he.append("high entry barrier")
    if scores["stability"] >= 8.5:
        hz.append("就业极其稳定"); he.append("extremely stable employment")
    elif scores["stability"] >= 7.5:
        hz.append("就业稳定"); he.append("stable employment")
    if scores["fulfillment"] >= 8.0:
        hz.append("职业成就感高"); he.append("high job fulfillment")
    if scores["burnout"] <= 3.5:
        hz.append("过劳风险高"); he.append("high burnout risk")
    if scores["ai_resistance"] >= 8.0:
        hz.append("AI替代抗性强"); he.append("strong AI resistance")
    elif scores["ai_resistance"] <= 4.0:
        hz.append("AI替代风险高"); he.append("high AI displacement risk")
    if scores["intl_mobility"] >= 8.0:
        hz.append("国际流动性高"); he.append("high international mobility")
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
    csv_path = PROJECT_ROOT / "data" / "csv" / "legal_social.csv"
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
            ns = hash(f"LAW-{occ['id']}-{iso}") % 10000
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

            row_id = f"LAW-{occ['id']}-{iso}-general"
            row = {
                "id": row_id,
                "major_category": "法律与社会服务",
                "major_code": "LAW",
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
    json_path = PROJECT_ROOT / "data" / "json" / "legal_social.json"
    convert_csv_to_json(str(csv_path), str(json_path))
    print(f"JSON written to {json_path}")

    # Notebook
    from tools.generate_notebook import create_data_notebook
    nb_path = PROJECT_ROOT / "notebooks" / "07_legal_social.ipynb"
    create_data_notebook(
        str(csv_path), str(nb_path),
        title="法律与社会服务 (LAW) — 完整数据",
        description="72 occupations × 45 countries/regions = 3,240 rows",
    )
    print(f"Notebook written to {nb_path}")


if __name__ == "__main__":
    main()
