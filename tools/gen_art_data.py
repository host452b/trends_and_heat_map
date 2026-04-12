#!/usr/bin/env python3
"""Generate culture_arts_media.csv — ART data for Global Career Development Index."""
import csv, sys, random
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
from tools.score_calculator import load_weights, calculate_composite

# === OCCUPATIONS (200) from categories.yaml ART ===
O = []
def _a(mid, mid_zh, mid_en, items):
    for id_, zh, en, isco, onet, loc in items:
        O.append({"id": id_, "mid": mid, "mid_zh": mid_zh, "mid_en": mid_en,
                   "zh": zh, "en": en, "isco": isco, "onet": onet, "locality": loc})

_a("film_production", "影视制作", "Film & Television Production", [
    ("0101","电影导演","Film Director","2654","27-2012.00","global"),
    ("0102","编剧","Screenwriter","2641","27-3043.00","global"),
    ("0103","制片人","Film/TV Producer","2654","27-2012.01","global"),
    ("0104","演员","Actor / Actress","2655","27-2011.00","global"),
    ("0105","摄影指导","Cinematographer / Director of Photography","2654","27-4031.00","global"),
    ("0106","剪辑师","Film/Video Editor","2654","27-4032.00","global"),
    ("0107","视觉特效师(VFX)","Visual Effects (VFX) Artist","2166","27-1014.00","global"),
    ("0108","灯光师","Lighting Technician / Gaffer","3521","27-4011.00","global"),
    ("0109","美术指导(影视)","Production Designer","2166","27-1027.00","global"),
    ("0110","服装设计师(影视)","Costume Designer","2163","27-1022.00","global"),
    ("0111","综艺编导","Variety Show Director","2654","27-2012.00","global"),
    ("0112","选角导演","Casting Director","2654","27-2012.04","global"),
    ("0113","特技演员","Stunt Performer","2655","27-2011.00","global"),
    ("0114","化妆师(影视)","Film/TV Makeup Artist","5142","39-5091.00","global"),
    ("0115","收音师","Production Sound Mixer","3521","27-4014.00","global"),
    ("0116","电视导演","Television Director","2654","27-2012.00","global"),
    ("0117","场记","Script Supervisor / Continuity Person","2654","27-2012.00","global"),
    ("0118","调色师","Colorist","2654","27-4032.00","global"),
    ("0119","纪录片导演","Documentary Director","2654","27-2012.00","global"),
    ("0120","动作导演/武术指导","Action Director / Stunt Coordinator","2654","27-2012.00","global"),
    ("0121","外景制片","Location Manager","2654","27-2012.00","global"),
    ("0122","后期制作总监","Post-production Supervisor","2654","27-4032.00","global"),
    ("0123","影视发行人","Film Distribution Executive","1349","11-2011.00","global"),
])
_a("music_industry", "音乐产业", "Music Industry", [
    ("0201","歌手","Singer / Vocalist","2652","27-2042.00","global"),
    ("0202","作曲家/词曲创作人","Composer / Songwriter","2652","27-2041.00","global"),
    ("0203","音乐制作人","Music Producer","2652","27-2041.00","global"),
    ("0204","录音工程师","Recording Engineer","3521","27-4014.00","global"),
    ("0205","指挥","Orchestra Conductor","2652","27-2041.01","global"),
    ("0206","DJ/电子音乐人","DJ / Electronic Music Producer","2652","27-2042.00","global"),
    ("0207","器乐演奏家","Instrumental Musician","2652","27-2042.02","global"),
    ("0208","音乐编曲师","Music Arranger","2652","27-2041.00","global"),
    ("0209","声乐教师","Vocal Coach / Voice Teacher","2354","25-1121.00","global"),
    ("0210","调音师/音响师","Sound Engineer / Live Sound Technician","3521","27-4014.00","global"),
    ("0211","K-pop练习生","K-pop Trainee","2655","","regional"),
    ("0212","音乐治疗师(临床)","Clinical Music Therapist","2652","29-1129.00","global"),
    ("0213","音乐版权管理人","Music Rights Manager","2619","13-1199.00","global"),
    ("0214","乐器调律师","Piano/Instrument Tuner","7312","49-9063.00","global"),
])
_a("publishing_writing", "出版写作", "Publishing & Writing", [
    ("0301","小说家/作家","Novelist / Author","2641","27-3043.00","global"),
    ("0302","图书编辑","Book Editor","2641","27-3041.00","global"),
    ("0303","文学经纪人","Literary Agent","3339","13-1011.00","global"),
    ("0304","翻译","Translator","2643","27-3091.00","global"),
    ("0305","技术文档写作","Technical Writer","2641","27-3042.00","global"),
    ("0306","诗人","Poet","2641","27-3043.00","global"),
    ("0307","口译员","Interpreter","2643","27-3091.00","global"),
    ("0308","出版发行人","Publisher","1349","11-2011.00","global"),
    ("0309","漫画家/插画师","Comic Artist / Illustrator","2651","27-1013.00","global"),
    ("0310","书法家","Calligrapher","2651","27-1013.00","regional"),
    ("0311","自出版作者","Self-publishing Author","2641","27-3043.00","global"),
])
_a("stage_performance", "舞台表演", "Stage Performance", [
    ("0401","舞台剧演员","Theatre Actor","2655","27-2011.00","global"),
    ("0402","舞蹈家/舞者","Dancer / Choreographer","2653","27-2031.00","global"),
    ("0403","脱口秀演员","Stand-up Comedian","2655","27-2011.00","global"),
    ("0404","相声/曲艺演员","Crosstalk / Traditional Comedy Performer","2655","27-2011.00","regional"),
    ("0405","魔术师","Magician","2655","27-2011.00","global"),
    ("0406","杂技演员","Acrobat / Circus Performer","2655","27-2011.00","global"),
    ("0407","戏剧导演","Theatre Director","2654","27-2012.02","global"),
    ("0408","舞台监督","Stage Manager","2654","27-2012.04","global"),
    ("0409","歌剧歌手","Opera Singer","2652","27-2042.00","global"),
    ("0410","木偶师","Puppeteer","2655","27-2011.00","global"),
    ("0411","艺伎","Geisha","2655","","country_specific"),
    ("0412","京剧演员","Peking Opera Performer","2655","27-2011.00","regional"),
    ("0413","芭蕾舞者","Ballet Dancer","2653","27-2031.00","global"),
    ("0414","马戏团表演者","Circus Performer","2655","27-2011.00","global"),
    ("0415","即兴戏剧演员","Improv Performer","2655","27-2011.00","global"),
])
_a("museum_heritage", "博物馆与文化遗产", "Museum & Cultural Heritage", [
    ("0501","博物馆策展人","Museum Curator","2621","25-4012.00","global"),
    ("0502","文物修复师","Art/Artifact Conservator","2621","25-4013.00","global"),
    ("0503","考古学家","Archaeologist","2632","19-3091.00","global"),
    ("0504","非物质文化遗产传承人","Intangible Cultural Heritage Practitioner","2651","","regional"),
    ("0505","古建筑修复专家","Heritage Building Restorer","2621","25-4013.00","global"),
    ("0506","博物馆讲解员","Museum Guide / Docent","5113","39-7012.00","global"),
    ("0507","文化遗产保护规划师","Heritage Conservation Planner","2621","25-4013.00","global"),
    ("0508","博物馆教育员","Museum Educator","2621","25-4012.00","global"),
])
_a("design_creative", "设计创意", "Design & Creative", [
    ("0601","平面设计师","Graphic Designer","2166","27-1024.00","global"),
    ("0602","工业设计师","Industrial Designer","2163","27-1021.00","global"),
    ("0603","时装设计师","Fashion Designer","2163","27-1022.00","global"),
    ("0604","室内设计师","Interior Designer","2161","27-1025.00","global"),
    ("0605","珠宝设计师","Jewelry Designer","2163","27-1029.00","global"),
    ("0606","文创产品设计师","Cultural/Creative Product Designer","2163","27-1029.00","global"),
    ("0607","品牌设计师","Brand Identity Designer","2166","27-1024.00","global"),
    ("0608","包装设计师","Packaging Designer","2166","27-1024.00","global"),
    ("0609","展览设计师","Exhibition Designer","2163","27-1027.00","global"),
    ("0610","花艺设计师","Floral Designer","3432","27-1023.00","global"),
    ("0611","家具设计师","Furniture Designer","2163","27-1021.00","global"),
    ("0612","字体设计师","Type Designer / Typographer","2166","27-1024.00","global"),
    ("0613","动态图形设计师","Motion Graphics Designer","2166","27-1014.00","global"),
    ("0614","用户体验设计师(非IT)","Service Designer / Experience Designer","2163","27-1029.00","global"),
])
_a("animation_games", "动画游戏", "Animation & Games", [
    ("0701","2D动画师","2D Animator","2166","27-1014.00","global"),
    ("0702","3D动画师","3D Animator","2166","27-1014.00","global"),
    ("0703","游戏策划","Game Designer / Game Planner","2166","15-1255.01","global"),
    ("0704","游戏美术设计师","Game Artist","2166","27-1014.00","global"),
    ("0705","关卡设计师","Level Designer","2166","15-1255.01","global"),
    ("0706","游戏音效设计师","Game Sound Designer","3521","27-4014.00","global"),
    ("0707","游戏程序员","Game Programmer","2514","15-1252.00","global"),
    ("0708","动作捕捉技术员","Motion Capture Technician","3521","27-4014.00","global"),
    ("0709","游戏叙事设计师","Narrative Designer","2641","27-3043.00","global"),
    ("0710","技术美术(TA)","Technical Artist","2166","27-1014.00","global"),
    ("0711","游戏UI设计师","Game UI Designer","2166","15-1255.01","global"),
    ("0712","游戏测试员(QA)","Game QA Tester","2519","15-1253.00","global"),
    ("0713","概念艺术家","Concept Artist","2651","27-1013.00","global"),
])
_a("advertising_pr", "广告公关", "Advertising & Public Relations", [
    ("0801","广告文案","Advertising Copywriter","2431","27-3043.00","global"),
    ("0802","创意总监","Creative Director","2431","11-2011.00","global"),
    ("0803","公关专员","Public Relations Specialist","2432","27-3031.00","global"),
    ("0804","危机公关专家","Crisis Communications Specialist","2432","27-3031.00","global"),
    ("0805","品牌经理","Brand Manager","1221","11-2021.00","global"),
    ("0806","活动策划师","Event Planner","3332","13-1121.00","global"),
    ("0807","媒介购买","Media Buyer","2431","13-1161.00","global"),
    ("0808","广告客户经理","Account Executive (Advertising)","2431","11-2011.00","global"),
    ("0809","市场研究分析师","Market Research Analyst","2431","13-1161.00","global"),
    ("0810","SEO/SEM专家","SEO/SEM Specialist","2431","13-1161.00","global"),
    ("0811","内容策略师","Content Strategist","2431","27-3043.00","global"),
    ("0812","影响力营销专员","Influencer Marketing Specialist","2431","13-1161.00","global"),
    ("0813","社会化媒体分析师","Social Media Analyst","2431","13-1161.00","global"),
])
_a("news_media", "新闻传媒", "News & Journalism", [
    ("0901","记者","Journalist / Reporter","2642","27-3022.00","global"),
    ("0902","电视主持人/主播","TV Anchor / Presenter","2656","27-3011.00","global"),
    ("0903","摄影记者","Photojournalist","3431","27-4021.00","global"),
    ("0904","新闻编辑","News Editor","2642","27-3041.00","global"),
    ("0905","调查记者","Investigative Journalist","2642","27-3022.00","global"),
    ("0906","数据新闻记者","Data Journalist","2642","27-3022.00","global"),
    ("0907","广播电台主持人","Radio Host","2656","27-3011.00","global"),
    ("0908","战地记者","War Correspondent","2642","27-3022.00","global"),
    ("0909","气象主播","Weather Anchor / Meteorologist Presenter","2656","27-3011.00","global"),
    ("0910","视频记者/多媒体记者","Video Journalist (VJ) / Multimedia Journalist","2642","27-3022.00","global"),
    ("0911","事实核查员","Fact-checker","2642","27-3041.00","global"),
])
_a("new_media", "新媒体内容", "New Media & Digital Content", [
    ("1001","YouTuber/视频博主","YouTuber / Video Content Creator","2642","27-3043.00","global"),
    ("1002","短视频创作者","Short-form Video Creator","2642","27-3043.00","global"),
    ("1003","播客主持人","Podcast Host","2656","27-3011.00","global"),
    ("1004","博客作者","Blogger / Online Writer","2641","27-3043.00","global"),
    ("1005","VTuber(虚拟主播)","VTuber (Virtual YouTuber)","2655","","regional"),
    ("1006","直播带货主播","Livestream Commerce Host","5242","","regional"),
    ("1007","游戏直播主播","Game Streamer","2656","27-2011.00","global"),
    ("1008","KOL/网红","Key Opinion Leader (KOL) / Influencer","2431","27-3043.00","global"),
    ("1009","MCN运营经理","MCN Operations Manager","1349","11-2011.00","global"),
    ("1010","内容审核员","Content Moderator","4132","43-9199.00","global"),
    ("1011","社交媒体经理","Social Media Manager","2431","11-2021.00","global"),
    ("1012","声优/配音演员","Voice Actor (Seiyuu)","2655","27-2011.00","regional"),
])
_a("sports", "体育竞技", "Sports & Esports", [
    ("1101","职业足球运动员","Professional Soccer/Football Player","3421","27-2021.00","global"),
    ("1102","职业篮球运动员","Professional Basketball Player","3421","27-2021.00","global"),
    ("1103","职业网球运动员","Professional Tennis Player","3421","27-2021.00","global"),
    ("1104","职业高尔夫球员","Professional Golfer","3421","27-2021.00","global"),
    ("1105","职业电子竞技选手","Professional Esports Player","3421","27-2021.00","global"),
    ("1106","体育教练","Sports Coach / Trainer","3422","27-2022.00","global"),
    ("1107","裁判员","Sports Referee / Umpire","3422","27-2023.00","global"),
    ("1108","体育经纪人","Sports Agent","3339","13-1011.00","global"),
    ("1109","体育解说员/评论员","Sports Commentator / Analyst","2656","27-3011.00","global"),
    ("1110","职业拳击手/格斗选手","Professional Boxer / MMA Fighter","3421","27-2021.00","global"),
    ("1111","职业游泳运动员","Professional Swimmer","3421","27-2021.00","global"),
    ("1112","职业田径运动员","Professional Track & Field Athlete","3421","27-2021.00","global"),
    ("1113","相扑力士","Sumo Wrestler (Rikishi)","3421","","country_specific"),
    ("1114","电竞教练","Esports Coach","3422","27-2022.00","global"),
    ("1115","运动营养师","Sports Nutritionist","2265","29-1031.00","global"),
    ("1116","体育记者","Sports Journalist","2642","27-3022.00","global"),
    ("1117","体能训练师","Strength & Conditioning Coach","3422","27-2022.00","global"),
    ("1118","运动心理学家","Sports Psychologist","2634","19-3031.02","global"),
    ("1119","赛事运营经理","Sports Event Operations Manager","3332","13-1121.00","global"),
    ("1120","运动医学医生","Sports Medicine Doctor","2212","29-1229.04","global"),
])
_a("exhibitions", "会展", "Exhibitions & Events", [
    ("1201","会展设计师","Exhibition Designer","2163","27-1027.00","global"),
    ("1202","会展组织者","Conference/Exhibition Organizer","3332","13-1121.00","global"),
    ("1203","拍卖师","Auctioneer","3339","27-2099.00","global"),
    ("1204","画廊经营者","Gallery Owner / Dealer","1420","11-9199.00","global"),
    ("1205","艺术品鉴定师","Art Appraiser / Authenticator","2621","13-2023.00","global"),
    ("1206","舞台搭建工","Stagehand / Set Builder","7119","27-4012.00","global"),
    ("1207","艺术博览会策展人","Art Fair Curator","2621","25-4012.00","global"),
])
_a("library_info", "图书馆信息", "Library & Information Science", [
    ("1301","图书馆员","Librarian","2622","25-4022.00","global"),
    ("1302","档案管理员","Archivist","2621","25-4011.00","global"),
    ("1303","信息科学专家","Information Scientist","2622","15-1299.09","global"),
    ("1304","数字档案管理员","Digital Archivist","2621","25-4011.00","global"),
])
_a("cultural_industry_mgmt", "文化产业管理", "Cultural Industry Management", [
    ("1401","IP运营经理","IP Operations Manager","1349","11-2011.00","global"),
    ("1402","文化投资人","Cultural Industry Investor","2411","11-3031.02","global"),
    ("1403","艺人经纪人","Talent Agent / Artist Manager","3339","13-1011.00","global"),
    ("1404","版权管理专员","Copyright/Licensing Manager","2619","11-9199.00","global"),
    ("1405","文化政策研究员","Cultural Policy Researcher","2632","19-3099.00","global"),
    ("1406","艺术节总监","Festival Director","1349","11-2011.00","global"),
    ("1407","剧院经理","Theatre Manager","1349","11-9199.00","global"),
    ("1408","音乐节运营总监","Music Festival Director","1349","11-9199.00","global"),
    ("1409","演出经纪人","Talent Booking Agent","3339","13-1011.00","global"),
])
_a("photography", "摄影", "Photography", [
    ("1501","商业摄影师","Commercial Photographer","3431","27-4021.00","global"),
    ("1502","婚礼摄影师","Wedding Photographer","3431","27-4021.00","global"),
    ("1503","肖像摄影师","Portrait Photographer","3431","27-4021.00","global"),
    ("1504","时尚摄影师","Fashion Photographer","3431","27-4021.00","global"),
    ("1505","纪实摄影师","Documentary Photographer","3431","27-4021.00","global"),
    ("1506","航拍摄影师","Aerial/Drone Photographer","3431","27-4021.00","global"),
])
_a("fine_arts", "美术/纯艺术", "Fine Arts", [
    ("1601","画家/油画家","Painter / Fine Artist","2651","27-1013.00","global"),
    ("1602","雕塑家","Sculptor","2651","27-1013.00","global"),
    ("1603","版画家","Printmaker","2651","27-1013.00","global"),
    ("1604","装置艺术家","Installation Artist","2651","27-1013.00","global"),
    ("1605","行为艺术家","Performance Artist","2655","27-2011.00","global"),
    ("1606","壁画师","Muralist","2651","27-1013.00","global"),
    ("1607","数字艺术家/AI艺术家","Digital / AI Artist","2651","27-1013.00","global"),
    ("1608","艺术评论家","Art Critic","2641","27-3043.00","global"),
])
_a("traditional_performing", "传统表演艺术", "Traditional Performing Arts", [
    ("1701","歌舞伎演员","Kabuki Actor","2655","27-2011.00","country_specific"),
    ("1702","能乐演员","Noh Theatre Performer","2655","27-2011.00","country_specific"),
    ("1703","黑人灵歌/福音歌手","Gospel Singer","2652","27-2042.00","global"),
    ("1704","弗拉门戈舞者","Flamenco Dancer","2653","27-2031.00","regional"),
    ("1705","印度古典舞者","Indian Classical Dancer","2653","27-2031.00","regional"),
    ("1706","粤剧演员","Cantonese Opera Performer","2655","27-2011.00","regional"),
    ("1707","昆曲演员","Kunqu Opera Performer","2655","27-2011.00","regional"),
    ("1708","皮影戏表演者","Shadow Puppetry Performer","2655","27-2011.00","regional"),
    ("1709","评书/说书人","Storyteller (Pingshu)","2655","27-2011.00","regional"),
    ("1710","民族乐器演奏家","Traditional/Folk Instrument Player","2652","27-2042.02","regional"),
    ("1711","二人转演员","Er Ren Zhuan Performer","2655","","country_specific"),
    ("1712","落语家","Rakugo Performer","2655","","country_specific"),
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

# === COUNTRY PROFILES for ART ===
# Keys: ent(entertainment mkt), cre(creative industry), spo(sports mkt), nm(new media),
#   pf(press freedom), ch(cultural heritage), des(design industry),
#   comp(compensation), wlb(work-life balance), stab(stability),
#   edu(edu quality), intl(international openness), gender(gender equality),
#   reg(regulatory), ot(overtime culture, higher=less OT)
CP = {
    "US": {"ent":9.5,"cre":9.0,"spo":9.5,"nm":9.0,"pf":7.5,"ch":6.0,"des":8.5,"comp":9.0,"wlb":6.0,"stab":6.0,"edu":9.0,"intl":8.5,"gender":7.5,"reg":6.5,"ot":5.0},
    "GB": {"ent":8.5,"cre":8.5,"spo":8.5,"nm":8.0,"pf":8.0,"ch":8.0,"des":8.5,"comp":7.5,"wlb":7.0,"stab":7.0,"edu":8.5,"intl":9.0,"gender":7.5,"reg":7.0,"ot":6.5},
    "FR": {"ent":7.5,"cre":8.0,"spo":7.5,"nm":6.5,"pf":8.0,"ch":9.0,"des":8.5,"comp":7.0,"wlb":8.0,"stab":7.0,"edu":8.0,"intl":7.5,"gender":7.0,"reg":7.5,"ot":7.0},
    "DE": {"ent":7.0,"cre":7.5,"spo":8.0,"nm":7.0,"pf":8.5,"ch":8.0,"des":8.5,"comp":8.0,"wlb":8.0,"stab":8.0,"edu":8.5,"intl":8.0,"gender":7.0,"reg":7.5,"ot":7.5},
    "JP": {"ent":8.5,"cre":8.5,"spo":7.5,"nm":8.5,"pf":6.5,"ch":8.5,"des":8.0,"comp":7.0,"wlb":4.5,"stab":7.5,"edu":8.0,"intl":5.0,"gender":5.0,"reg":7.0,"ot":3.5},
    "KR": {"ent":8.5,"cre":8.5,"spo":7.0,"nm":9.0,"pf":7.0,"ch":7.5,"des":7.5,"comp":7.0,"wlb":4.0,"stab":6.5,"edu":8.0,"intl":6.0,"gender":4.5,"reg":6.5,"ot":3.0},
    "CN": {"ent":8.5,"cre":7.5,"spo":8.0,"nm":9.5,"pf":3.5,"ch":9.0,"des":7.0,"comp":6.5,"wlb":3.5,"stab":5.5,"edu":7.5,"intl":5.0,"gender":5.5,"reg":5.0,"ot":2.5},
    "TW": {"ent":6.5,"cre":6.5,"spo":5.0,"nm":7.0,"pf":8.0,"ch":7.0,"des":6.5,"comp":5.5,"wlb":5.0,"stab":6.0,"edu":7.5,"intl":6.5,"gender":6.0,"reg":6.0,"ot":4.0},
    "HK": {"ent":7.0,"cre":7.0,"spo":5.5,"nm":7.5,"pf":5.0,"ch":6.5,"des":7.0,"comp":7.0,"wlb":4.5,"stab":6.5,"edu":7.5,"intl":9.0,"gender":6.5,"reg":6.5,"ot":3.5},
    "SG": {"ent":6.0,"cre":6.5,"spo":5.5,"nm":6.5,"pf":5.5,"ch":5.5,"des":6.5,"comp":8.0,"wlb":5.5,"stab":8.0,"edu":8.5,"intl":9.5,"gender":7.0,"reg":8.0,"ot":4.5},
    "IN": {"ent":9.0,"cre":7.0,"spo":8.0,"nm":8.5,"pf":5.5,"ch":9.0,"des":6.0,"comp":4.5,"wlb":4.5,"stab":5.0,"edu":7.0,"intl":7.0,"gender":4.0,"reg":5.0,"ot":4.0},
    "TH": {"ent":6.0,"cre":5.5,"spo":5.5,"nm":7.0,"pf":5.0,"ch":7.5,"des":5.5,"comp":3.5,"wlb":5.5,"stab":5.5,"edu":5.5,"intl":5.5,"gender":6.0,"reg":5.0,"ot":5.5},
    "VN": {"ent":5.5,"cre":5.0,"spo":5.0,"nm":7.0,"pf":3.5,"ch":7.0,"des":5.0,"comp":3.0,"wlb":5.0,"stab":5.0,"edu":5.5,"intl":5.5,"gender":5.5,"reg":5.0,"ot":4.5},
    "ID": {"ent":6.0,"cre":5.5,"spo":6.0,"nm":7.5,"pf":5.5,"ch":7.5,"des":5.0,"comp":3.5,"wlb":5.5,"stab":5.0,"edu":5.0,"intl":4.5,"gender":5.0,"reg":5.0,"ot":5.0},
    "MY": {"ent":5.5,"cre":5.5,"spo":5.5,"nm":6.5,"pf":5.0,"ch":6.5,"des":5.5,"comp":4.5,"wlb":5.5,"stab":6.0,"edu":6.0,"intl":6.5,"gender":5.5,"reg":5.5,"ot":5.0},
    "PH": {"ent":6.0,"cre":5.0,"spo":5.5,"nm":7.0,"pf":5.5,"ch":6.0,"des":5.0,"comp":3.0,"wlb":5.0,"stab":4.5,"edu":5.5,"intl":6.5,"gender":6.5,"reg":4.5,"ot":4.5},
    "PK": {"ent":5.0,"cre":4.0,"spo":5.5,"nm":5.5,"pf":4.0,"ch":7.0,"des":3.5,"comp":2.5,"wlb":4.5,"stab":3.5,"edu":4.5,"intl":4.5,"gender":3.0,"reg":4.0,"ot":4.5},
    "BD": {"ent":5.0,"cre":4.0,"spo":5.0,"nm":5.5,"pf":4.0,"ch":6.5,"des":3.5,"comp":2.0,"wlb":4.5,"stab":3.5,"edu":4.0,"intl":4.5,"gender":3.5,"reg":3.5,"ot":4.5},
    "AE": {"ent":6.5,"cre":6.5,"spo":7.0,"nm":6.5,"pf":4.5,"ch":5.5,"des":6.5,"comp":8.0,"wlb":5.5,"stab":7.0,"edu":7.0,"intl":8.5,"gender":5.5,"reg":6.5,"ot":5.0},
    "IL": {"ent":6.0,"cre":6.5,"spo":5.5,"nm":6.5,"pf":7.0,"ch":7.0,"des":7.0,"comp":7.5,"wlb":6.0,"stab":5.5,"edu":8.5,"intl":8.0,"gender":7.0,"reg":6.0,"ot":5.0},
    "SA": {"ent":5.0,"cre":4.5,"spo":6.5,"nm":6.0,"pf":3.5,"ch":6.0,"des":4.5,"comp":6.5,"wlb":5.5,"stab":6.0,"edu":6.0,"intl":5.5,"gender":3.5,"reg":5.5,"ot":5.0},
    "TR": {"ent":7.0,"cre":6.0,"spo":7.0,"nm":7.0,"pf":4.5,"ch":8.0,"des":5.5,"comp":4.0,"wlb":5.0,"stab":4.0,"edu":6.5,"intl":5.5,"gender":4.5,"reg":5.0,"ot":4.5},
    "NL": {"ent":6.5,"cre":7.5,"spo":7.0,"nm":7.0,"pf":9.0,"ch":7.5,"des":8.0,"comp":7.5,"wlb":9.0,"stab":7.5,"edu":8.0,"intl":9.0,"gender":8.5,"reg":7.0,"ot":8.0},
    "CH": {"ent":5.5,"cre":7.0,"spo":6.0,"nm":5.5,"pf":9.0,"ch":7.5,"des":8.0,"comp":9.5,"wlb":8.5,"stab":9.0,"edu":9.0,"intl":8.5,"gender":7.0,"reg":7.0,"ot":7.5},
    "SE": {"ent":6.0,"cre":7.0,"spo":6.5,"nm":7.0,"pf":9.5,"ch":7.0,"des":8.5,"comp":7.0,"wlb":9.0,"stab":8.0,"edu":8.5,"intl":8.5,"gender":9.0,"reg":7.0,"ot":8.5},
    "DK": {"ent":5.5,"cre":7.0,"spo":6.0,"nm":6.5,"pf":9.5,"ch":7.0,"des":9.0,"comp":7.0,"wlb":9.0,"stab":8.0,"edu":8.5,"intl":8.5,"gender":9.0,"reg":7.0,"ot":8.5},
    "FI": {"ent":5.0,"cre":6.5,"spo":5.5,"nm":6.0,"pf":9.5,"ch":6.5,"des":7.5,"comp":6.5,"wlb":9.0,"stab":7.5,"edu":9.0,"intl":8.0,"gender":9.0,"reg":7.0,"ot":8.5},
    "IT": {"ent":7.0,"cre":7.5,"spo":8.0,"nm":6.0,"pf":7.0,"ch":9.5,"des":9.0,"comp":5.5,"wlb":6.5,"stab":5.5,"edu":7.0,"intl":6.5,"gender":5.5,"reg":6.5,"ot":5.5},
    "ES": {"ent":6.5,"cre":7.0,"spo":8.0,"nm":6.5,"pf":7.5,"ch":9.0,"des":7.0,"comp":5.0,"wlb":7.0,"stab":5.5,"edu":7.0,"intl":7.0,"gender":6.5,"reg":6.0,"ot":5.5},
    "PT": {"ent":5.0,"cre":5.5,"spo":6.5,"nm":5.5,"pf":8.0,"ch":8.0,"des":5.5,"comp":4.5,"wlb":7.0,"stab":5.5,"edu":6.5,"intl":7.5,"gender":7.0,"reg":6.0,"ot":6.0},
    "PL": {"ent":5.5,"cre":6.0,"spo":6.0,"nm":6.0,"pf":6.5,"ch":7.5,"des":6.0,"comp":5.5,"wlb":7.0,"stab":6.5,"edu":7.0,"intl":7.5,"gender":6.5,"reg":6.5,"ot":6.0},
    "CZ": {"ent":5.5,"cre":6.0,"spo":5.5,"nm":5.5,"pf":7.5,"ch":8.0,"des":6.5,"comp":5.5,"wlb":7.5,"stab":7.0,"edu":7.0,"intl":7.5,"gender":6.5,"reg":6.5,"ot":6.5},
    "RU": {"ent":7.0,"cre":6.5,"spo":7.5,"nm":7.0,"pf":3.5,"ch":8.5,"des":5.5,"comp":4.5,"wlb":5.5,"stab":4.0,"edu":7.5,"intl":3.5,"gender":6.0,"reg":4.5,"ot":5.5},
    "CA": {"ent":7.5,"cre":7.5,"spo":7.5,"nm":7.5,"pf":8.5,"ch":6.5,"des":7.0,"comp":7.5,"wlb":7.5,"stab":7.0,"edu":8.0,"intl":9.0,"gender":8.0,"reg":7.0,"ot":6.5},
    "MX": {"ent":7.0,"cre":6.0,"spo":7.0,"nm":7.0,"pf":5.0,"ch":8.5,"des":5.5,"comp":4.0,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.5,"gender":5.0,"reg":5.0,"ot":4.5},
    "BR": {"ent":7.5,"cre":6.5,"spo":8.5,"nm":7.5,"pf":6.5,"ch":7.0,"des":6.0,"comp":4.5,"wlb":6.0,"stab":4.5,"edu":6.0,"intl":5.0,"gender":5.5,"reg":5.5,"ot":5.0},
    "AR": {"ent":6.5,"cre":6.5,"spo":8.0,"nm":6.0,"pf":7.0,"ch":7.0,"des":6.0,"comp":3.5,"wlb":5.5,"stab":3.5,"edu":6.5,"intl":5.0,"gender":5.5,"reg":4.5,"ot":5.0},
    "CL": {"ent":5.0,"cre":5.5,"spo":5.5,"nm":5.5,"pf":7.5,"ch":6.5,"des":5.5,"comp":4.5,"wlb":6.0,"stab":5.5,"edu":6.0,"intl":6.0,"gender":5.5,"reg":5.5,"ot":5.5},
    "CO": {"ent":5.5,"cre":5.5,"spo":6.0,"nm":6.0,"pf":5.5,"ch":7.0,"des":5.0,"comp":3.5,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.0,"gender":5.0,"reg":5.0,"ot":5.0},
    "AU": {"ent":7.0,"cre":7.5,"spo":8.5,"nm":7.5,"pf":8.0,"ch":6.0,"des":7.0,"comp":8.0,"wlb":8.0,"stab":7.5,"edu":8.0,"intl":8.5,"gender":8.0,"reg":7.0,"ot":7.0},
    "NZ": {"ent":5.5,"cre":6.5,"spo":6.5,"nm":6.0,"pf":9.0,"ch":6.0,"des":6.0,"comp":6.5,"wlb":8.5,"stab":7.5,"edu":7.5,"intl":8.0,"gender":8.5,"reg":7.0,"ot":7.5},
    "ZA": {"ent":5.5,"cre":5.5,"spo":7.0,"nm":5.5,"pf":7.0,"ch":6.5,"des":5.0,"comp":4.0,"wlb":5.5,"stab":4.5,"edu":5.5,"intl":5.5,"gender":5.5,"reg":5.0,"ot":5.5},
    "NG": {"ent":7.0,"cre":5.0,"spo":6.0,"nm":6.5,"pf":5.0,"ch":6.0,"des":4.0,"comp":2.5,"wlb":4.5,"stab":3.5,"edu":4.0,"intl":4.5,"gender":4.0,"reg":3.5,"ot":4.5},
    "KE": {"ent":5.5,"cre":5.0,"spo":6.5,"nm":6.0,"pf":6.0,"ch":6.5,"des":4.5,"comp":2.5,"wlb":5.0,"stab":4.0,"edu":4.5,"intl":5.0,"gender":4.5,"reg":4.0,"ot":5.0},
    "EG": {"ent":6.5,"cre":5.5,"spo":6.0,"nm":6.0,"pf":4.0,"ch":8.5,"des":5.0,"comp":3.0,"wlb":5.0,"stab":4.0,"edu":5.0,"intl":5.0,"gender":3.5,"reg":4.0,"ot":4.5},
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
    # film: high creative, bimodal income, project-based, low stability
    "film_production": _d(5.5,5.0,5.5,6.0, 5.5,5.5,5.0,5.0, 5.5,4.5, 3.5,6.5,6.0,4.0,5.5, 6.0,5.5,3.5, 6.5,6.0,4.0,6.5,3.5,8.0,6.0,5.0,5.0, 7.0,4.0,2.0,7.0,5.5,6.5,5.0, 2,1,"本科","20-30"),
    # music: high fulfillment, extreme variance, gig-based
    "music_industry": _d(6.0,5.0,5.0,6.5, 5.0,5.0,4.5,4.5, 4.5,4.0, 3.0,7.5,6.5,4.5,5.5, 6.5,5.0,4.0, 7.0,6.0,5.0,7.5,3.5,8.5,6.5,5.0,5.5, 7.0,3.5,2.0,6.5,6.5,6.5,4.5, 1,0,"本科/专科","18-28"),
    # publishing: remote-friendly, AI-threatened, low pay
    "publishing_writing": _d(5.0,5.0,4.0,8.0, 4.5,4.5,4.0,4.0, 4.0,4.5, 4.5,8.5,7.0,5.5,5.0, 7.0,6.0,3.0, 4.5,5.5,8.0,8.0,6.5,7.5,7.0,6.0,7.0, 5.0,1.5,1.5,4.5,7.0,6.5,3.5, 0,-1,"本科","22-35"),
    # stage: physical, short career for dancers, high fulfillment, gig-based
    "stage_performance": _d(6.0,4.5,4.5,5.0, 4.5,4.0,4.0,4.0, 3.5,3.5, 3.0,6.5,5.5,4.5,5.5, 5.5,4.5,4.0, 8.0,5.5,2.0,6.5,3.0,8.5,5.5,5.5,4.0, 8.0,6.5,2.0,6.5,5.0,5.5,4.5, 0,-1,"本科/专科","16-25"),
    # museum/heritage: stable, academic, niche
    "museum_heritage": _d(6.5,6.5,4.5,8.5, 4.0,3.5,4.5,5.0, 4.5,4.5, 7.0,8.5,7.5,6.5,4.5, 6.0,5.0,1.0, 7.5,6.5,4.0,6.0,6.5,7.5,3.5,6.0,7.5, 6.5,3.0,3.5,3.5,4.0,5.5,5.5, 1,0,"硕士","24-32"),
    # design: moderate pay, AI-disrupted, freelance-friendly
    "design_creative": _d(5.0,5.0,5.5,7.5, 6.0,6.0,5.5,5.0, 5.5,5.5, 5.0,8.5,7.0,5.0,5.5, 7.0,6.0,2.0, 5.0,5.5,7.0,7.0,5.5,7.5,7.0,5.5,6.5, 6.0,2.5,1.5,5.5,7.0,6.0,3.5, 2,1,"本科","20-28"),
    # animation/games: high demand in JP/KR/CN/US, crunch culture
    "animation_games": _d(5.5,5.0,6.5,7.0, 6.5,6.0,6.0,5.5, 6.0,5.5, 5.0,8.0,6.5,3.5,6.5, 6.5,5.5,2.5, 5.5,5.5,6.5,6.0,4.0,7.5,5.5,5.0,6.0, 5.5,2.5,1.5,6.0,5.5,6.5,5.0, 3,2,"本科","20-28"),
    # advertising/PR: business-creative hybrid, moderate
    "advertising_pr": _d(4.5,5.0,5.5,7.5, 6.0,6.5,5.5,5.0, 5.5,5.5, 5.5,8.5,7.0,4.5,6.0, 7.0,6.5,2.0, 4.5,5.5,6.5,6.0,5.0,6.0,6.0,5.5,6.5, 7.0,2.0,1.5,5.5,6.0,6.0,4.0, 2,1,"本科","22-28"),
    # news/journalism: declining trad, AI-threatened, important social role
    "news_media": _d(5.0,5.5,4.0,7.0, 4.5,5.0,4.5,4.5, 4.5,4.5, 4.5,6.0,6.5,4.0,6.5, 6.5,6.0,2.5, 5.5,6.0,5.5,6.0,4.0,7.5,5.0,5.5,6.5, 7.5,3.5,2.5,5.0,5.5,6.5,4.5, -1,-2,"本科","22-28"),
    # new media: exploding, zero barrier, high entrepreneurship
    "new_media": _d(3.0,3.0,7.0,5.0, 7.5,7.5,6.0,4.5, 4.5,5.0, 2.5,8.5,7.0,3.5,6.5, 6.0,5.5,4.5, 6.0,4.5,8.5,9.0,4.0,7.0,9.0,5.5,4.5, 7.5,2.5,1.0,5.0,8.0,5.0,3.0, 5,4,"无要求","16-30"),
    # sports: extreme income variance, very short career, high physical
    "sports": _d(6.0,4.0,5.0,3.5, 4.5,5.5,5.0,4.5, 5.5,3.5, 3.0,5.5,4.5,3.5,5.5, 4.0,3.5,4.5, 9.0,6.5,1.5,5.0,2.5,8.5,3.5,4.5,2.0, 7.5,9.0,2.5,5.0,3.0,7.0,6.0, 2,1,"高中/体校","14-22"),
    # exhibitions: event-based, social, moderate
    "exhibitions": _d(4.5,4.5,5.0,7.5, 5.5,5.0,5.0,4.5, 5.0,5.0, 5.0,8.0,7.0,5.0,5.0, 6.0,6.0,2.0, 6.5,5.5,4.0,6.0,5.0,6.5,6.5,5.5,6.5, 7.5,4.0,2.0,6.5,5.5,6.0,4.0, 2,1,"本科","22-30"),
    # library: stable, low pay, academic
    "library_info": _d(5.0,5.5,3.5,9.0, 3.5,3.5,3.5,3.5, 3.5,4.5, 8.0,9.0,8.0,7.0,3.5, 5.5,5.0,0.5, 5.0,5.0,5.5,5.5,7.5,6.5,2.5,6.5,8.0, 5.0,1.5,2.5,2.5,4.0,4.5,4.5, 0,-1,"硕士","24-30"),
    # cultural industry mgmt: business + culture, moderate-high
    "cultural_industry_mgmt": _d(5.0,5.5,6.0,7.5, 6.0,5.5,5.5,5.0, 6.5,6.0, 5.5,8.5,7.0,5.0,5.5, 7.0,6.5,2.5, 5.5,6.5,6.0,7.0,5.0,7.0,7.0,5.5,6.5, 7.5,2.0,2.0,5.5,6.0,6.5,4.5, 3,2,"本科/硕士","25-35"),
    # photography: freelance, AI-disrupted, entrepreneurial
    "photography": _d(4.5,4.0,4.5,7.5, 5.0,5.5,4.5,4.0, 4.5,4.5, 4.0,8.0,7.0,5.0,5.0, 6.0,5.5,2.5, 5.0,5.0,5.5,8.0,5.0,7.5,8.0,5.5,6.5, 6.5,3.5,1.5,5.5,7.5,5.0,3.0, 1,0,"本科/专科","20-30"),
    # fine arts: extreme variance, very high fulfillment, niche
    "fine_arts": _d(6.0,5.5,4.0,9.0, 3.5,3.0,3.5,3.5, 3.5,3.0, 3.0,8.5,7.5,6.0,5.0, 5.5,4.5,4.5, 7.5,6.0,6.0,9.0,5.5,9.5,7.5,5.5,8.0, 5.0,3.5,1.0,4.0,7.0,5.5,3.5, 0,-1,"本科/硕士","20-30"),
    # traditional performing: niche, cultural, declining demand
    "traditional_performing": _d(7.0,4.5,3.0,6.0, 3.0,2.5,3.5,3.5, 3.0,3.0, 4.0,7.0,6.0,5.5,4.5, 4.0,3.5,3.0, 9.0,5.5,2.0,5.5,4.0,8.0,3.0,5.0,4.5, 7.0,6.0,2.5,3.5,4.5,4.0,5.0, -2,-2,"专科/师承","12-20"),
}

# === PER-OCCUPATION OVERRIDES ===
OVR = {
    # film_production
    "0101": {"value_added":7.5,"social_status":8.5,"reputation_variance":4.5,"autonomy":9.0,"fulfillment":9.0,"career_lifespan":8.0,"entrepreneurship":7.5,"age":"25-35"},
    "0102": {"remote_friendly":8.0,"ai_resistance":4.5,"value_added":5.0,"autonomy":8.5,"social_status":6.5,"fulfillment":8.5},
    "0103": {"value_added":7.0,"social_status":7.5,"entrepreneurship":8.0,"autonomy":8.0,"supply_demand":5.5,"age":"28-38"},
    "0104": {"reputation_variance":4.5,"value_added":6.0,"social_status":8.0,"stability":2.0,"physical_demand":5.5,"fulfillment":9.0,"gender_equality":4.5,"career_lifespan":5.5,"age":"18-30"},
    "0105": {"learning_cost":6.5,"ai_resistance":7.5,"value_added":6.5,"social_status":7.0,"physical_demand":4.5},
    "0106": {"ai_resistance":5.0,"remote_friendly":7.0,"value_added":5.5},
    "0107": {"growth_coeff":7.5,"supply_demand":7.0,"ai_resistance":5.5,"value_added":6.5,"trend_long":4,"trend_short":3,"remote_friendly":7.0},
    "0108": {"learning_cost":4.0,"education_req":3.5,"value_added":4.0,"social_status":4.5,"physical_demand":5.5,"remote_friendly":1.5},
    "0109": {"ai_resistance":7.0,"fulfillment":8.5,"value_added":5.5,"social_status":6.5},
    "0110": {"ai_resistance":7.5,"fulfillment":8.0,"value_added":5.0,"market_size":4.0},
    "0111": {"stability":4.0,"burnout":6.5,"value_added":5.0,"social_status":5.5},
    "0112": {"social_interaction":8.5,"ai_resistance":7.5,"market_size":3.5,"value_added":5.5},
    "0113": {"physical_demand":9.0,"safety":4.0,"career_lifespan":4.0,"ai_resistance":9.0,"value_added":4.5,"social_status":5.0,"age":"18-28"},
    "0114": {"ai_resistance":7.5,"physical_demand":3.5,"license_barrier":2.5,"value_added":4.5,"entrepreneurship":6.5},
    "0115": {"ai_resistance":7.0,"market_size":4.5,"remote_friendly":2.0,"physical_demand":3.5},
    "0116": {"value_added":6.0,"social_status":7.0,"stability":4.0},
    "0117": {"learning_cost":3.5,"value_added":3.5,"social_status":4.0,"remote_friendly":2.0},
    "0118": {"ai_resistance":5.5,"remote_friendly":7.5,"value_added":5.5,"market_size":4.0},
    "0119": {"fulfillment":9.0,"social_status":7.0,"value_added":5.0,"market_size":4.0},
    "0120": {"physical_demand":8.0,"safety":4.5,"ai_resistance":9.0,"career_lifespan":5.0,"age":"20-35"},
    "0121": {"social_interaction":7.5,"physical_demand":4.5,"remote_friendly":2.0,"value_added":4.5},
    "0122": {"value_added":6.0,"social_status":6.5,"remote_friendly":6.0,"autonomy":7.0},
    "0123": {"value_added":7.0,"social_status":7.0,"entrepreneurship":7.5,"ai_resistance":6.0,"supply_demand":5.0,"age":"30-40"},
    # music_industry
    "0201": {"reputation_variance":4.5,"value_added":5.5,"social_status":7.5,"stability":2.0,"fulfillment":9.5,"gender_equality":4.5,"career_lifespan":5.5},
    "0202": {"remote_friendly":8.0,"ai_resistance":6.5,"value_added":5.0,"fulfillment":9.5,"autonomy":9.0},
    "0203": {"value_added":6.5,"social_status":7.0,"entrepreneurship":8.0,"growth_coeff":6.0,"supply_demand":5.5},
    "0204": {"ai_resistance":6.5,"remote_friendly":4.0,"value_added":5.5,"physical_demand":2.5},
    "0205": {"learning_cost":8.0,"education_req":7.5,"value_added":6.0,"social_status":8.0,"career_lifespan":8.5,"age":"28-40","edu":"硕士"},
    "0206": {"learning_cost":4.0,"education_req":3.0,"entrepreneurship":8.5,"value_added":5.0,"growth_coeff":6.0,"trend_short":2},
    "0207": {"learning_cost":8.0,"education_req":6.5,"career_lifespan":8.0,"ai_resistance":8.0,"value_added":4.5,"fulfillment":9.5},
    "0208": {"remote_friendly":7.5,"ai_resistance":5.5,"value_added":5.0},
    "0209": {"stability":5.5,"value_added":4.0,"career_lifespan":8.0,"ai_resistance":7.5,"license_barrier":2.5,"entrepreneurship":7.0,"fulfillment":8.0},
    "0210": {"physical_demand":4.5,"remote_friendly":2.0,"ai_resistance":7.0,"value_added":4.5},
    "0211": {"learning_cost":7.0,"career_lifespan":2.5,"stability":1.5,"value_added":3.0,"physical_demand":7.5,"burnout":8.0,"age":"12-18","edu":"无要求"},
    "0212": {"education_req":6.5,"license_barrier":4.0,"stability":5.5,"value_added":5.0,"fulfillment":8.5,"social_status":6.0,"ai_resistance":8.0},
    "0213": {"education_req":6.0,"stability":6.0,"value_added":5.5,"ai_resistance":6.0,"remote_friendly":7.0,"social_interaction":6.5},
    "0214": {"learning_cost":5.5,"ai_resistance":8.5,"market_size":3.0,"value_added":3.5,"career_lifespan":9.0,"physical_demand":3.0,"entrepreneurship":7.0},
    # publishing_writing
    "0301": {"reputation_variance":4.0,"value_added":4.0,"autonomy":9.5,"fulfillment":9.0,"remote_friendly":9.5,"entrepreneurship":8.0,"stability":2.5,"ai_resistance":5.5},
    "0302": {"stability":5.5,"value_added":4.0,"ai_resistance":5.0,"social_status":5.5},
    "0303": {"social_interaction":7.5,"value_added":6.0,"entrepreneurship":7.5,"market_size":3.5},
    "0304": {"ai_resistance":3.5,"remote_friendly":9.0,"intl_mobility":8.0,"value_added":4.0,"supply_demand":4.5},
    "0305": {"stability":6.0,"value_added":5.5,"ai_resistance":4.0,"supply_demand":5.0,"growth_coeff":5.0,"remote_friendly":8.5},
    "0306": {"value_added":2.0,"stability":1.5,"market_size":2.0,"reputation_variance":4.5,"fulfillment":9.5,"autonomy":9.5},
    "0307": {"ai_resistance":5.5,"value_added":5.5,"social_interaction":8.0,"physical_demand":2.0,"remote_friendly":5.0,"intl_mobility":8.5},
    "0308": {"value_added":6.5,"social_status":6.5,"entrepreneurship":8.0,"autonomy":8.0,"age":"30-40"},
    "0309": {"ai_resistance":6.5,"fulfillment":9.0,"remote_friendly":8.5,"entrepreneurship":8.0,"value_added":4.0,"reputation_variance":3.5},
    "0310": {"ai_resistance":9.0,"market_size":2.0,"supply_demand":3.0,"fulfillment":9.0,"career_lifespan":9.5,"age":"25-40"},
    "0311": {"education_req":3.0,"entrepreneurship":9.5,"remote_friendly":9.5,"stability":2.0,"value_added":3.5,"autonomy":9.5,"ai_resistance":5.0},
    # stage_performance
    "0401": {"reputation_variance":4.0,"fulfillment":9.0,"social_status":6.0,"value_added":3.5,"stability":2.5},
    "0402": {"physical_demand":8.5,"career_lifespan":3.5,"value_added":3.5,"ai_resistance":9.0,"fulfillment":9.0,"age":"14-22"},
    "0403": {"entrepreneurship":7.5,"social_interaction":9.0,"value_added":4.5,"growth_coeff":6.0,"trend_short":1},
    "0404": {"market_size":2.5,"ai_resistance":9.0,"value_added":3.0,"career_lifespan":7.0},
    "0405": {"entrepreneurship":8.0,"ai_resistance":9.0,"value_added":4.0,"physical_demand":5.0},
    "0406": {"physical_demand":9.5,"safety":4.0,"career_lifespan":3.5,"value_added":3.0,"ai_resistance":9.5,"age":"10-18"},
    "0407": {"value_added":5.5,"social_status":7.0,"autonomy":8.0,"fulfillment":9.0,"career_lifespan":8.0,"age":"28-38"},
    "0408": {"value_added":4.5,"social_interaction":7.5,"stability":4.0,"autonomy":5.5},
    "0409": {"learning_cost":8.0,"education_req":6.5,"value_added":5.0,"social_status":7.5,"ai_resistance":9.0,"fulfillment":9.5,"career_lifespan":5.5},
    "0410": {"market_size":2.0,"ai_resistance":9.5,"fulfillment":8.5,"value_added":3.0},
    "0411": {"market_size":1.5,"ai_resistance":9.5,"value_added":4.0,"learning_cost":8.0,"career_lifespan":5.5,"gender_equality":2.0},
    "0412": {"market_size":2.5,"ai_resistance":9.5,"value_added":3.5,"learning_cost":8.0,"career_lifespan":6.5},
    "0413": {"physical_demand":9.0,"career_lifespan":3.0,"value_added":3.5,"ai_resistance":9.5,"fulfillment":9.5,"learning_cost":8.0,"age":"10-18"},
    "0414": {"physical_demand":9.0,"safety":4.0,"career_lifespan":4.0,"value_added":3.0,"ai_resistance":9.5},
    "0415": {"entrepreneurship":7.0,"value_added":3.5,"growth_coeff":5.5,"social_interaction":9.0},
    # museum_heritage
    "0501": {"social_status":7.0,"value_added":5.5,"autonomy":7.0,"fulfillment":8.0},
    "0502": {"ai_resistance":9.0,"physical_demand":4.5,"value_added":5.0,"market_size":3.0,"career_lifespan":9.0},
    "0503": {"education_req":8.0,"learning_cost":7.5,"ai_resistance":8.0,"physical_demand":5.0,"value_added":5.0,"social_status":7.0,"fulfillment":8.5,"edu":"硕士/博士"},
    "0504": {"ai_resistance":9.5,"market_size":2.0,"value_added":3.5,"career_lifespan":9.5,"fulfillment":9.0,"education_req":4.0,"learning_cost":7.5},
    "0505": {"ai_resistance":9.0,"physical_demand":5.5,"value_added":5.0,"market_size":3.0,"license_barrier":4.0},
    "0506": {"learning_cost":4.0,"education_req":4.0,"value_added":3.0,"social_interaction":9.0,"career_lifespan":7.5,"social_status":4.5},
    "0507": {"education_req":7.0,"value_added":5.0,"social_status":6.5,"ai_resistance":7.0,"market_size":3.0},
    "0508": {"social_interaction":8.0,"value_added":4.0,"education_req":6.0,"fulfillment":8.0},
    # design_creative
    "0601": {"ai_resistance":4.0,"supply_demand":5.0,"value_added":4.5,"remote_friendly":8.0},
    "0602": {"ai_resistance":6.0,"value_added":6.5,"social_status":6.5,"education_req":6.0},
    "0603": {"reputation_variance":3.5,"value_added":5.5,"social_status":7.0,"gender_equality":5.0,"fulfillment":8.5,"entrepreneurship":7.5},
    "0604": {"value_added":5.5,"entrepreneurship":7.5,"remote_friendly":5.5,"physical_demand":3.0,"license_barrier":3.0,"market_size":6.5},
    "0605": {"market_size":4.0,"entrepreneurship":8.0,"value_added":5.0,"ai_resistance":6.5,"physical_demand":3.5},
    "0606": {"market_size":5.0,"entrepreneurship":7.5,"value_added":5.0,"growth_coeff":6.0,"trend_short":2},
    "0607": {"value_added":6.0,"growth_coeff":6.0,"supply_demand":6.0},
    "0608": {"value_added":5.0,"ai_resistance":4.5},
    "0609": {"physical_demand":3.5,"remote_friendly":4.5,"market_size":5.0},
    "0610": {"learning_cost":3.5,"education_req":3.0,"entrepreneurship":8.5,"value_added":4.0,"ai_resistance":7.5,"physical_demand":3.5,"career_lifespan":8.0},
    "0611": {"value_added":5.5,"ai_resistance":6.5,"physical_demand":3.5,"market_size":5.0},
    "0612": {"market_size":3.5,"ai_resistance":5.5,"value_added":5.0,"remote_friendly":8.5},
    "0613": {"growth_coeff":6.5,"supply_demand":6.5,"value_added":6.0,"trend_short":2,"ai_resistance":4.5,"remote_friendly":8.0},
    "0614": {"growth_coeff":6.5,"supply_demand":6.0,"value_added":6.0,"trend_short":2},
    # animation_games
    "0701": {"ai_resistance":5.0,"value_added":5.0,"remote_friendly":7.5},
    "0702": {"growth_coeff":7.0,"supply_demand":6.5,"value_added":6.5,"ai_resistance":5.5,"trend_short":3},
    "0703": {"ai_resistance":7.0,"value_added":6.0,"social_interaction":6.5,"autonomy":6.5},
    "0704": {"ai_resistance":5.0,"value_added":5.5,"remote_friendly":7.0},
    "0705": {"value_added":5.5,"ai_resistance":6.5,"remote_friendly":7.0},
    "0706": {"ai_resistance":7.0,"market_size":4.5,"value_added":5.5},
    "0707": {"value_added":7.0,"growth_coeff":7.0,"supply_demand":7.0,"ai_resistance":6.0,"trend_short":3,"learning_cost":6.0,"education_req":5.5},
    "0708": {"market_size":4.0,"ai_resistance":7.0,"physical_demand":4.0,"remote_friendly":2.5},
    "0709": {"ai_resistance":7.0,"value_added":5.5,"remote_friendly":7.5,"fulfillment":8.0},
    "0710": {"value_added":6.5,"supply_demand":7.0,"growth_coeff":7.0,"ai_resistance":6.0,"learning_cost":6.5,"trend_short":3},
    "0711": {"ai_resistance":5.0,"value_added":5.5,"remote_friendly":7.5},
    "0712": {"learning_cost":3.5,"education_req":3.5,"value_added":4.0,"ai_resistance":5.5,"career_lifespan":6.0,"social_status":4.0},
    "0713": {"ai_resistance":6.0,"fulfillment":8.5,"value_added":5.5,"remote_friendly":7.5,"reputation_variance":3.0},
    # advertising_pr
    "0801": {"ai_resistance":3.5,"remote_friendly":7.5,"value_added":5.0,"fulfillment":6.5},
    "0802": {"value_added":8.0,"social_status":7.5,"autonomy":8.0,"career_lifespan":8.0,"age":"30-40"},
    "0803": {"social_interaction":8.5,"value_added":5.0,"ai_resistance":5.5},
    "0804": {"value_added":7.0,"social_status":7.0,"ai_resistance":7.0,"supply_demand":5.0,"market_size":4.5},
    "0805": {"value_added":7.0,"social_status":7.0,"growth_coeff":6.0,"supply_demand":6.0},
    "0806": {"physical_demand":4.5,"remote_friendly":3.5,"social_interaction":8.5,"entrepreneurship":7.5},
    "0807": {"ai_resistance":4.0,"value_added":5.0,"remote_friendly":7.0},
    "0808": {"social_interaction":8.5,"value_added":5.5,"burnout":6.5},
    "0809": {"ai_resistance":5.0,"value_added":5.5,"remote_friendly":7.0,"education_req":5.5},
    "0810": {"growth_coeff":6.5,"ai_resistance":4.5,"remote_friendly":8.5,"value_added":5.5,"trend_short":2},
    "0811": {"growth_coeff":6.5,"ai_resistance":4.5,"remote_friendly":8.0,"value_added":5.5,"trend_short":2},
    "0812": {"growth_coeff":7.0,"trend_short":3,"value_added":5.5,"remote_friendly":7.5,"supply_demand":6.0},
    "0813": {"ai_resistance":5.0,"remote_friendly":8.0,"value_added":5.0,"growth_coeff":6.0},
    # news_media
    "0901": {"social_status":6.5,"fulfillment":8.0,"safety":5.0,"ai_resistance":6.5,"value_added":4.5},
    "0902": {"value_added":7.0,"social_status":7.5,"reputation_variance":3.5,"stability":5.0,"gender_equality":4.5},
    "0903": {"physical_demand":5.5,"safety":5.0,"ai_resistance":7.0,"value_added":4.0,"remote_friendly":3.0},
    "0904": {"stability":5.5,"ai_resistance":5.0,"value_added":4.5,"remote_friendly":7.0},
    "0905": {"safety":4.0,"fulfillment":9.0,"social_status":7.5,"ai_resistance":7.5,"value_added":5.0,"reputation_variance":3.0},
    "0906": {"growth_coeff":6.0,"ai_resistance":5.5,"value_added":5.5,"remote_friendly":7.5,"trend_short":1},
    "0907": {"value_added":5.0,"social_status":6.0,"stability":4.5,"market_size":4.5},
    "0908": {"safety":2.5,"value_added":5.5,"social_status":8.0,"physical_demand":6.0,"fulfillment":9.0,"reputation_variance":3.5,"family_friendly":2.0},
    "0909": {"stability":5.5,"value_added":5.5,"ai_resistance":5.0,"learning_cost":5.5,"education_req":5.5},
    "0910": {"growth_coeff":5.5,"value_added":4.5,"remote_friendly":5.0,"physical_demand":4.0,"trend_short":0},
    "0911": {"ai_resistance":6.5,"value_added":4.0,"growth_coeff":5.0,"remote_friendly":7.5,"market_size":3.5},
    # new_media
    "1001": {"reputation_variance":4.0,"value_added":5.5,"entrepreneurship":9.5,"fulfillment":8.0,"social_status":5.0},
    "1002": {"value_added":5.0,"entrepreneurship":9.5,"growth_coeff":8.0,"trend_short":5,"social_status":4.5},
    "1003": {"remote_friendly":9.5,"value_added":4.5,"growth_coeff":7.5,"entrepreneurship":9.0},
    "1004": {"remote_friendly":9.5,"value_added":3.5,"ai_resistance":4.5,"career_lifespan":7.0,"entrepreneurship":9.0},
    "1005": {"growth_coeff":7.5,"value_added":4.5,"ai_resistance":5.5,"trend_short":4,"market_size":4.5},
    "1006": {"value_added":6.0,"growth_coeff":8.0,"trend_short":5,"social_interaction":8.5,"market_size":6.0,"entrepreneurship":9.5},
    "1007": {"value_added":5.0,"growth_coeff":7.0,"trend_short":4,"social_interaction":7.5},
    "1008": {"reputation_variance":4.5,"value_added":6.5,"social_status":5.5,"stability":2.0,"entrepreneurship":9.5,"career_lifespan":4.5},
    "1009": {"education_req":5.0,"value_added":6.0,"social_status":5.5,"stability":4.0,"social_interaction":7.5,"entrepreneurship":7.5,"age":"25-35"},
    "1010": {"learning_cost":2.0,"education_req":2.5,"value_added":3.0,"stability":4.5,"burnout":7.5,"ai_resistance":4.5,"fulfillment":3.5,"remote_friendly":7.0,"autonomy":4.0},
    "1011": {"value_added":5.5,"growth_coeff":7.0,"supply_demand":6.5,"trend_short":3,"stability":5.0,"education_req":4.5},
    "1012": {"learning_cost":6.0,"ai_resistance":7.5,"value_added":4.5,"fulfillment":8.0,"market_size":5.5,"remote_friendly":7.5},
    # sports
    "1101": {"value_added":8.0,"reputation_variance":4.5,"social_status":9.0,"intl_mobility":9.0,"market_size":8.0,"career_lifespan":3.0},
    "1102": {"value_added":8.0,"reputation_variance":4.5,"social_status":9.0,"intl_mobility":8.5,"market_size":7.0},
    "1103": {"value_added":7.5,"social_status":8.0,"intl_mobility":9.0,"entrepreneurship":5.0,"market_size":6.0},
    "1104": {"value_added":7.5,"social_status":7.5,"career_lifespan":5.0,"intl_mobility":8.5,"market_size":5.5},
    "1105": {"growth_coeff":8.0,"trend_long":4,"trend_short":4,"value_added":6.0,"career_lifespan":2.5,"physical_demand":5.0,"age":"14-20","market_size":6.5},
    "1106": {"value_added":4.5,"career_lifespan":7.0,"stability":5.0,"physical_demand":6.0,"license_barrier":3.5,"fulfillment":7.5,"age":"25-40","edu":"本科"},
    "1107": {"value_added":4.0,"career_lifespan":6.0,"stability":5.0,"ai_resistance":7.5,"physical_demand":5.5,"license_barrier":3.5,"age":"25-35","edu":"无要求"},
    "1108": {"value_added":7.0,"social_status":6.5,"social_interaction":8.5,"career_lifespan":7.5,"physical_demand":2.0,"entrepreneurship":8.0,"edu":"本科","age":"25-35"},
    "1109": {"physical_demand":2.0,"value_added":5.5,"social_status":6.0,"remote_friendly":5.0,"career_lifespan":7.5,"social_interaction":8.5,"edu":"本科","age":"28-38"},
    "1110": {"value_added":6.5,"safety":3.0,"career_lifespan":2.5,"physical_demand":9.5,"reputation_variance":4.5,"social_status":7.0},
    "1111": {"value_added":5.0,"career_lifespan":3.0,"social_status":6.5,"market_size":4.5},
    "1112": {"value_added":5.0,"career_lifespan":3.0,"social_status":6.5,"market_size":5.0},
    "1113": {"market_size":1.5,"ai_resistance":9.5,"value_added":5.5,"career_lifespan":3.5,"physical_demand":9.5,"social_status":7.0},
    "1114": {"growth_coeff":7.5,"value_added":5.5,"career_lifespan":6.5,"physical_demand":3.0,"trend_short":3,"edu":"无要求","age":"22-32"},
    "1115": {"education_req":6.0,"license_barrier":3.5,"value_added":5.0,"career_lifespan":7.5,"physical_demand":3.0,"ai_resistance":7.0,"edu":"本科","age":"24-32"},
    "1116": {"physical_demand":3.0,"value_added":4.5,"social_interaction":7.5,"career_lifespan":7.5,"remote_friendly":5.0,"edu":"本科","age":"22-30"},
    "1117": {"license_barrier":3.5,"value_added":4.5,"career_lifespan":6.5,"physical_demand":7.0,"ai_resistance":7.5,"edu":"本科","age":"22-32"},
    "1118": {"education_req":8.0,"learning_cost":7.5,"value_added":6.0,"career_lifespan":8.0,"physical_demand":2.0,"ai_resistance":7.5,"social_status":7.0,"edu":"硕士/博士","age":"26-34"},
    "1119": {"value_added":5.5,"social_interaction":8.5,"career_lifespan":7.5,"physical_demand":3.0,"entrepreneurship":7.0,"edu":"本科","age":"25-35"},
    "1120": {"education_req":8.0,"learning_cost":8.0,"value_added":7.0,"career_lifespan":8.0,"physical_demand":3.5,"license_barrier":7.0,"ai_resistance":7.5,"social_status":8.0,"edu":"博士","age":"28-35"},
    # exhibitions
    "1201": {"ai_resistance":6.0,"value_added":5.5,"fulfillment":7.0,"remote_friendly":4.5},
    "1202": {"social_interaction":8.5,"value_added":5.5,"entrepreneurship":7.0},
    "1203": {"social_interaction":9.0,"ai_resistance":7.5,"value_added":5.5,"social_status":6.0,"career_lifespan":8.0,"license_barrier":3.0},
    "1204": {"entrepreneurship":9.0,"value_added":6.0,"social_status":6.5,"autonomy":8.5,"reputation_variance":3.5,"age":"30-40"},
    "1205": {"learning_cost":7.0,"education_req":7.0,"ai_resistance":8.0,"value_added":6.0,"market_size":3.5,"social_status":6.5},
    "1206": {"learning_cost":3.0,"education_req":2.5,"value_added":3.5,"physical_demand":7.5,"safety":6.5,"social_status":3.5,"edu":"高中/大专","age":"18-30"},
    "1207": {"social_status":6.5,"value_added":5.5,"social_interaction":8.0,"fulfillment":7.5},
    # library_info
    "1301": {"ai_resistance":4.5,"social_interaction":6.0,"fulfillment":7.0},
    "1302": {"ai_resistance":6.0,"value_added":3.5,"fulfillment":7.0},
    "1303": {"growth_coeff":5.0,"supply_demand":4.5,"value_added":5.0,"remote_friendly":7.0,"ai_resistance":5.0,"trend_short":0},
    "1304": {"growth_coeff":5.5,"supply_demand":5.0,"value_added":4.5,"ai_resistance":5.5,"remote_friendly":7.0,"trend_short":1},
    # cultural_industry_mgmt
    "1401": {"growth_coeff":7.0,"supply_demand":6.0,"value_added":7.0,"trend_short":3,"entrepreneurship":8.0},
    "1402": {"value_added":8.0,"social_status":7.5,"reputation_variance":3.5,"autonomy":8.5,"entrepreneurship":9.0,"age":"30-45"},
    "1403": {"social_interaction":9.0,"value_added":6.5,"social_status":6.0,"entrepreneurship":8.0,"reputation_variance":3.0},
    "1404": {"value_added":5.5,"remote_friendly":7.0,"ai_resistance":5.5},
    "1405": {"education_req":7.5,"value_added":5.0,"stability":7.0,"remote_friendly":7.0,"social_status":6.5,"fulfillment":7.5,"edu":"硕士/博士"},
    "1406": {"value_added":6.5,"social_status":7.0,"social_interaction":8.5,"autonomy":8.0,"entrepreneurship":7.5,"age":"30-40"},
    "1407": {"value_added":5.5,"stability":6.0,"social_interaction":7.5,"autonomy":7.0},
    "1408": {"value_added":6.5,"social_interaction":8.5,"entrepreneurship":7.5,"stability":4.5,"age":"28-38"},
    "1409": {"social_interaction":8.5,"value_added":5.5,"entrepreneurship":7.5},
    # photography
    "1501": {"value_added":5.0,"entrepreneurship":8.5,"social_interaction":6.5},
    "1502": {"value_added":5.0,"entrepreneurship":9.0,"social_interaction":7.5,"stability":4.5,"cycle_sensitivity":6.0},
    "1503": {"value_added":4.5,"entrepreneurship":8.5,"social_interaction":7.0},
    "1504": {"value_added":6.0,"social_status":6.5,"market_size":4.5,"intl_mobility":6.5},
    "1505": {"value_added":4.0,"fulfillment":8.5,"social_status":6.0,"market_size":3.5},
    "1506": {"growth_coeff":6.0,"value_added":5.0,"ai_resistance":6.0,"trend_short":2,"physical_demand":3.0,"license_barrier":2.5},
    # fine_arts
    "1601": {"fulfillment":9.5,"reputation_variance":4.5,"autonomy":9.5,"value_added":3.5,"career_lifespan":9.5},
    "1602": {"physical_demand":5.5,"value_added":3.5,"ai_resistance":8.5,"fulfillment":9.5},
    "1603": {"market_size":2.0,"value_added":3.0,"ai_resistance":8.0},
    "1604": {"physical_demand":5.0,"value_added":3.5,"fulfillment":9.5,"market_size":2.5,"ai_resistance":8.0},
    "1605": {"physical_demand":6.0,"value_added":3.0,"market_size":2.0,"ai_resistance":9.5,"fulfillment":9.5},
    "1606": {"physical_demand":5.5,"value_added":3.5,"entrepreneurship":7.0,"ai_resistance":8.0},
    "1607": {"growth_coeff":6.5,"ai_resistance":4.0,"value_added":4.0,"trend_short":2,"remote_friendly":8.5},
    "1608": {"education_req":7.5,"value_added":4.0,"social_status":6.5,"remote_friendly":8.0,"fulfillment":8.0,"market_size":2.5,"learning_cost":7.0},
    # traditional_performing
    "1701": {"market_size":1.5,"value_added":4.0,"social_status":7.0,"ai_resistance":9.5,"career_lifespan":7.0},
    "1702": {"market_size":1.5,"value_added":3.5,"social_status":7.0,"ai_resistance":9.5},
    "1703": {"market_size":3.5,"value_added":3.5,"social_status":5.5},
    "1704": {"market_size":2.5,"value_added":3.5,"social_status":6.0,"physical_demand":7.0,"intl_mobility":5.5},
    "1705": {"market_size":3.0,"value_added":3.0,"social_status":6.0,"physical_demand":6.5},
    "1706": {"market_size":2.0,"value_added":3.0,"career_lifespan":6.5},
    "1707": {"market_size":1.5,"value_added":3.5,"social_status":6.5,"career_lifespan":6.5},
    "1708": {"market_size":1.5,"value_added":2.5,"ai_resistance":9.5,"physical_demand":4.5},
    "1709": {"market_size":2.0,"value_added":3.0,"social_interaction":8.5},
    "1710": {"market_size":3.0,"value_added":3.5,"fulfillment":8.5,"intl_mobility":5.0},
    "1711": {"market_size":1.5,"value_added":2.5},
    "1712": {"market_size":1.5,"value_added":3.0,"social_status":6.0},
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
    ent_f = (cp["ent"] - 6.0) / 4.0
    cre_f = (cp["cre"] - 6.0) / 4.0
    comp_f = (cp["comp"] - 5.0) / 5.0
    stab_f = (cp["stab"] - 5.5) / 4.5
    wlb_f = (cp["wlb"] - 6.0) / 4.0
    gender_f = (cp["gender"] - 5.5) / 4.5
    edu_f = (cp["edu"] - 6.0) / 4.0
    intl_f = (cp["intl"] - 6.0) / 4.0
    reg_f = (cp["reg"] - 5.5) / 4.5
    pf_f = (cp["pf"] - 6.0) / 4.0
    nm_f = (cp["nm"] - 6.0) / 4.0
    spo_f = (cp["spo"] - 6.0) / 4.0
    des_f = (cp["des"] - 6.0) / 4.0
    ch_f = (cp["ch"] - 6.0) / 4.0

    mid = occ["mid"]
    # Sector-specific factors
    if mid in ("film_production","music_industry","stage_performance","traditional_performing"):
        sector_f = ent_f
    elif mid in ("design_creative","animation_games","photography","fine_arts"):
        sector_f = (cre_f + des_f) / 2
    elif mid in ("new_media",):
        sector_f = nm_f
    elif mid in ("sports",):
        sector_f = spo_f
    elif mid in ("news_media",):
        sector_f = (ent_f + pf_f) / 2
    elif mid in ("museum_heritage","traditional_performing"):
        sector_f = ch_f
    elif mid in ("advertising_pr",):
        sector_f = (ent_f + cre_f) / 2
    else:
        sector_f = cre_f

    s["value_added"] = clamp(s["value_added"] + comp_f * 2.0 + cre_f * 0.3)
    s["cost_performance"] = clamp(s["cost_performance"] + comp_f * 0.8 + cre_f * 0.5)
    s["growth_coeff"] = clamp(s["growth_coeff"] + sector_f * 0.8 + cre_f * 0.3)
    s["career_lifespan"] = clamp(s["career_lifespan"] + stab_f * 0.6)
    s["opportunity"] = clamp(s["opportunity"] + sector_f * 1.2 + cre_f * 0.3)
    s["market_size"] = clamp(s["market_size"] + sector_f * 1.5 + ent_f * 0.3)
    s["supply_demand"] = clamp(s["supply_demand"] + cre_f * 0.6 + sector_f * 0.5)
    dev_bonus = 0.8 if cp["cre"] >= 7.5 else (0.0 if cp["cre"] >= 5.0 else -0.8)
    s["developed_scarcity"] = clamp(s["developed_scarcity"] + dev_bonus)
    s["stability"] = clamp(s["stability"] + stab_f * 1.5 + reg_f * 0.3)
    s["safety"] = clamp(s["safety"] + wlb_f * 0.3 + reg_f * 0.3)
    s["occupational_disease"] = clamp(s["occupational_disease"] + wlb_f * 0.5)
    s["overtime"] = clamp(s["overtime"] + (cp["ot"] - 5.0) / 5.0 * 2.5)
    s["burnout"] = clamp(s["burnout"] + (cp["ot"] - 5.0) / 5.0 * 1.5)
    s["remote_friendly"] = clamp(s["remote_friendly"] + wlb_f * 0.4)
    s["autonomy"] = clamp(s["autonomy"] + wlb_f * 0.4 + cre_f * 0.2)
    s["family_friendly"] = clamp(s["family_friendly"] + wlb_f * 1.5)
    s["social_status"] = clamp(s["social_status"] + cre_f * 0.5 + comp_f * 0.4)
    s["fulfillment"] = clamp(s["fulfillment"] + cre_f * 0.3)
    s["gender_equality"] = clamp(s["gender_equality"] + gender_f * 2.0)
    s["age_flexibility"] = clamp(s["age_flexibility"] + wlb_f * 0.3 + cre_f * 0.2)
    s["entrepreneurship"] = clamp(s["entrepreneurship"] + cre_f * 0.4 + reg_f * 0.3)
    s["intl_mobility"] = clamp(s["intl_mobility"] + intl_f * 1.5)
    s["ai_resistance"] = clamp(s["ai_resistance"] + cre_f * 0.15)
    s["learning_cost"] = clamp(s["learning_cost"] + edu_f * 0.3)
    s["education_req"] = clamp(s["education_req"] + edu_f * 0.3)
    s["license_barrier"] = clamp(s["license_barrier"] + reg_f * 0.4)
    s["cycle_sensitivity"] = clamp(s["cycle_sensitivity"] - stab_f * 0.5)
    s["side_job_compat"] = clamp(s["side_job_compat"] + wlb_f * 0.3)
    s["industry_monopoly"] = clamp(s["industry_monopoly"] - cre_f * 0.3 + (1 - cp["reg"] / 10.0) * 0.3)
    s["skill_versatility"] = clamp(s["skill_versatility"] + cre_f * 0.4)
    s["career_switch"] = clamp(s["career_switch"] + cre_f * 0.3)
    rep_adj = -0.3 if cp["cre"] >= 7.5 else (0.3 if cp["cre"] < 5.0 else 0.0)
    s["reputation_variance"] = clamp5(s["reputation_variance"] + rep_adj)
    # Press freedom boost for news_media
    if mid == "news_media":
        s["safety"] = clamp(s["safety"] + pf_f * 0.8)
        s["autonomy"] = clamp(s["autonomy"] + pf_f * 0.6)
        s["fulfillment"] = clamp(s["fulfillment"] + pf_f * 0.3)
    # Sports special
    if mid == "sports":
        s["market_size"] = clamp(s["market_size"] + spo_f * 1.0)
        s["value_added"] = clamp(s["value_added"] + spo_f * 0.5)
    return s

def get_trends(base, cp):
    t_long = base["trend_long"]
    t_short = base["trend_short"]
    if cp.get("cre", 6) >= 8.0:
        t_short = min(5, t_short + 1)
    elif cp.get("cre", 6) < 4.0:
        t_short = max(-5, t_short - 1)
    if cp["ent"] >= 8.0:
        t_long = min(5, t_long + 1)
    elif cp["ent"] < 4.0:
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
    csv_path = PROJECT_ROOT / "data" / "csv" / "culture_arts_media.csv"
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    rows = []
    for occ in OCCUPATIONS:
        base = occ_base(occ["id"], occ["mid"])
        for country in COUNTRIES:
            iso = country["iso"]
            cp = CP[iso]
            scores = apply_country_modifiers(base, cp, occ)
            rng = random.Random(hash(f"ART-{occ['id']}-{iso}") % 10000)
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
            row_id = f"ART-{occ['id']}-{iso}-general"
            row = {
                "id": row_id,
                "major_category": "文化、艺术与传媒",
                "major_code": "ART",
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
                "typical_entry_age": base.get("age", "20-28"),
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
    json_path = PROJECT_ROOT / "data" / "json" / "culture_arts_media.json"
    convert_csv_to_json(str(csv_path), str(json_path))
    print(f"JSON written to {json_path}")

    # Notebook
    from tools.generate_notebook import create_data_notebook
    nb_path = PROJECT_ROOT / "notebooks" / "08_culture_arts_media.ipynb"
    create_data_notebook(
        str(csv_path), str(nb_path),
        title="文化、艺术与传媒 (ART) — 完整数据",
        description="200 occupations × 45 countries/regions = 9,000 rows",
    )
    print(f"Notebook written to {nb_path}")


if __name__ == "__main__":
    main()
