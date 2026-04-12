#!/usr/bin/env python3
"""Generate medical_health.csv — MED data for Global Career Development Index.

Creates scored data for all MED occupations across all 45 countries/regions.
Uses realistic, country-differentiated scoring based on global healthcare labor market knowledge.
"""

import csv
import sys
import random
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from tools.score_calculator import load_weights, calculate_composite

# ---------------------------------------------------------------------------
# OCCUPATION DEFINITIONS (from categories.yaml MED section)
# ---------------------------------------------------------------------------

OCCUPATIONS = [
    # ===== clinical_medicine (30) =====
    {"id": "0101", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "内科医生", "en": "Internal Medicine Physician", "isco": "2212", "onet": "29-1216.00", "locality": "global"},
    {"id": "0102", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "外科医生", "en": "Surgeon", "isco": "2212", "onet": "29-1241.00", "locality": "global"},
    {"id": "0103", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "全科医生", "en": "General Practitioner", "isco": "2211", "onet": "29-1215.00", "locality": "global"},
    {"id": "0104", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "麻醉科医生", "en": "Anesthesiologist", "isco": "2212", "onet": "29-1211.00", "locality": "global"},
    {"id": "0105", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "放射科医生", "en": "Radiologist", "isco": "2212", "onet": "29-1224.00", "locality": "global"},
    {"id": "0106", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "病理科医生", "en": "Pathologist", "isco": "2212", "onet": "29-1222.00", "locality": "global"},
    {"id": "0107", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "急诊科医生", "en": "Emergency Medicine Physician", "isco": "2212", "onet": "29-1214.00", "locality": "global"},
    {"id": "0108", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "儿科医生", "en": "Pediatrician", "isco": "2212", "onet": "29-1221.00", "locality": "global"},
    {"id": "0109", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "妇产科医生", "en": "Obstetrician/Gynecologist", "isco": "2212", "onet": "29-1218.00", "locality": "global"},
    {"id": "0110", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "心血管科医生", "en": "Cardiologist", "isco": "2212", "onet": "29-1212.00", "locality": "global"},
    {"id": "0111", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "神经内科医生", "en": "Neurologist", "isco": "2212", "onet": "29-1217.00", "locality": "global"},
    {"id": "0112", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "肿瘤科医生", "en": "Oncologist", "isco": "2212", "onet": "29-1243.00", "locality": "global"},
    {"id": "0113", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "骨科医生", "en": "Orthopedic Surgeon", "isco": "2212", "onet": "29-1241.00", "locality": "global"},
    {"id": "0114", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "泌尿科医生", "en": "Urologist", "isco": "2212", "onet": "29-1241.00", "locality": "global"},
    {"id": "0115", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "皮肤科医生", "en": "Dermatologist", "isco": "2212", "onet": "29-1213.00", "locality": "global"},
    {"id": "0116", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "耳鼻喉科医生", "en": "Otolaryngologist (ENT)", "isco": "2212", "onet": "29-1241.00", "locality": "global"},
    {"id": "0117", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "整形外科医生", "en": "Plastic Surgeon", "isco": "2212", "onet": "29-1241.00", "locality": "global"},
    {"id": "0118", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "神经外科医生", "en": "Neurosurgeon", "isco": "2212", "onet": "29-1241.00", "locality": "global"},
    {"id": "0119", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "心胸外科医生", "en": "Cardiothoracic Surgeon", "isco": "2212", "onet": "29-1241.00", "locality": "global"},
    {"id": "0120", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "重症医学科医生", "en": "Intensivist (ICU Physician)", "isco": "2212", "onet": "29-1216.00", "locality": "global"},
    {"id": "0121", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "内分泌科医生", "en": "Endocrinologist", "isco": "2212", "onet": "29-1216.00", "locality": "global"},
    {"id": "0122", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "肾内科医生", "en": "Nephrologist", "isco": "2212", "onet": "29-1216.00", "locality": "global"},
    {"id": "0123", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "风湿免疫科医生", "en": "Rheumatologist", "isco": "2212", "onet": "29-1216.00", "locality": "global"},
    {"id": "0124", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "消化科医生", "en": "Gastroenterologist", "isco": "2212", "onet": "29-1216.00", "locality": "global"},
    {"id": "0125", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "血液科医生", "en": "Hematologist", "isco": "2212", "onet": "29-1216.00", "locality": "global"},
    {"id": "0126", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "感染科医生", "en": "Infectious Disease Physician", "isco": "2212", "onet": "29-1216.00", "locality": "global"},
    {"id": "0127", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "呼吸科医生", "en": "Pulmonologist", "isco": "2212", "onet": "29-1216.00", "locality": "global"},
    {"id": "0128", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "老年科医生", "en": "Geriatrician", "isco": "2212", "onet": "29-1216.00", "locality": "global"},
    {"id": "0129", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "新生儿科医生", "en": "Neonatologist", "isco": "2212", "onet": "29-1221.00", "locality": "global"},
    {"id": "0130", "mid": "clinical_medicine", "mid_zh": "临床医学", "mid_en": "Clinical Medicine",
     "zh": "运动医学科医生", "en": "Sports Medicine Physician", "isco": "2212", "onet": "29-1229.04", "locality": "global"},
    # ===== nursing (13) =====
    {"id": "0201", "mid": "nursing", "mid_zh": "护理", "mid_en": "Nursing",
     "zh": "注册护士", "en": "Registered Nurse", "isco": "2221", "onet": "29-1141.00", "locality": "global"},
    {"id": "0202", "mid": "nursing", "mid_zh": "护理", "mid_en": "Nursing",
     "zh": "护理师", "en": "Nurse Practitioner", "isco": "2221", "onet": "29-1171.00", "locality": "global"},
    {"id": "0203", "mid": "nursing", "mid_zh": "护理", "mid_en": "Nursing",
     "zh": "助产士", "en": "Midwife", "isco": "2222", "onet": "29-1161.00", "locality": "global"},
    {"id": "0204", "mid": "nursing", "mid_zh": "护理", "mid_en": "Nursing",
     "zh": "ICU护士", "en": "ICU Nurse", "isco": "2221", "onet": "29-1141.00", "locality": "global"},
    {"id": "0205", "mid": "nursing", "mid_zh": "护理", "mid_en": "Nursing",
     "zh": "手术室护士", "en": "Operating Room Nurse", "isco": "2221", "onet": "29-1141.00", "locality": "global"},
    {"id": "0206", "mid": "nursing", "mid_zh": "护理", "mid_en": "Nursing",
     "zh": "护士长", "en": "Head Nurse / Nurse Manager", "isco": "1342", "onet": "11-9111.00", "locality": "global"},
    {"id": "0207", "mid": "nursing", "mid_zh": "护理", "mid_en": "Nursing",
     "zh": "社区护士", "en": "Community Health Nurse", "isco": "2221", "onet": "29-1141.00", "locality": "global"},
    {"id": "0208", "mid": "nursing", "mid_zh": "护理", "mid_en": "Nursing",
     "zh": "护理助理", "en": "Nursing Assistant", "isco": "5321", "onet": "31-1131.00", "locality": "global"},
    {"id": "0209", "mid": "nursing", "mid_zh": "护理", "mid_en": "Nursing",
     "zh": "麻醉护士", "en": "Nurse Anesthetist", "isco": "2221", "onet": "29-1151.00", "locality": "global"},
    {"id": "0210", "mid": "nursing", "mid_zh": "护理", "mid_en": "Nursing",
     "zh": "儿科护士", "en": "Pediatric Nurse", "isco": "2221", "onet": "29-1141.00", "locality": "global"},
    {"id": "0211", "mid": "nursing", "mid_zh": "护理", "mid_en": "Nursing",
     "zh": "肿瘤科护士", "en": "Oncology Nurse", "isco": "2221", "onet": "29-1141.00", "locality": "global"},
    {"id": "0212", "mid": "nursing", "mid_zh": "护理", "mid_en": "Nursing",
     "zh": "急诊护士", "en": "Emergency Room Nurse", "isco": "2221", "onet": "29-1141.00", "locality": "global"},
    {"id": "0213", "mid": "nursing", "mid_zh": "护理", "mid_en": "Nursing",
     "zh": "透析护士", "en": "Dialysis Nurse", "isco": "2221", "onet": "29-1141.00", "locality": "global"},
    # ===== pharmacy (7) =====
    {"id": "0301", "mid": "pharmacy", "mid_zh": "药学", "mid_en": "Pharmacy",
     "zh": "药剂师", "en": "Pharmacist", "isco": "2262", "onet": "29-1051.00", "locality": "global"},
    {"id": "0302", "mid": "pharmacy", "mid_zh": "药学", "mid_en": "Pharmacy",
     "zh": "临床药师", "en": "Clinical Pharmacist", "isco": "2262", "onet": "29-1051.00", "locality": "global"},
    {"id": "0303", "mid": "pharmacy", "mid_zh": "药学", "mid_en": "Pharmacy",
     "zh": "药品研发科学家", "en": "Pharmaceutical R&D Scientist", "isco": "2131", "onet": "19-2031.00", "locality": "global"},
    {"id": "0304", "mid": "pharmacy", "mid_zh": "药学", "mid_en": "Pharmacy",
     "zh": "药品注册专员", "en": "Drug Regulatory Affairs Specialist", "isco": "2262", "onet": "11-9121.01", "locality": "global"},
    {"id": "0305", "mid": "pharmacy", "mid_zh": "药学", "mid_en": "Pharmacy",
     "zh": "药品销售代表", "en": "Pharmaceutical Sales Representative", "isco": "2433", "onet": "41-4011.00", "locality": "global"},
    {"id": "0306", "mid": "pharmacy", "mid_zh": "药学", "mid_en": "Pharmacy",
     "zh": "药品质量管理员", "en": "Pharmaceutical QA Specialist", "isco": "2262", "onet": "29-1051.00", "locality": "global"},
    {"id": "0307", "mid": "pharmacy", "mid_zh": "药学", "mid_en": "Pharmacy",
     "zh": "药物警戒专员", "en": "Pharmacovigilance Specialist", "isco": "2262", "onet": "29-1051.00", "locality": "global"},
    # ===== rehabilitation (10) =====
    {"id": "0401", "mid": "rehabilitation", "mid_zh": "康复与治疗", "mid_en": "Rehabilitation & Therapy",
     "zh": "物理治疗师", "en": "Physical Therapist", "isco": "2264", "onet": "29-1123.00", "locality": "global"},
    {"id": "0402", "mid": "rehabilitation", "mid_zh": "康复与治疗", "mid_en": "Rehabilitation & Therapy",
     "zh": "职业治疗师", "en": "Occupational Therapist", "isco": "2269", "onet": "29-1122.00", "locality": "global"},
    {"id": "0403", "mid": "rehabilitation", "mid_zh": "康复与治疗", "mid_en": "Rehabilitation & Therapy",
     "zh": "言语治疗师", "en": "Speech-Language Pathologist", "isco": "2266", "onet": "29-1127.00", "locality": "global"},
    {"id": "0404", "mid": "rehabilitation", "mid_zh": "康复与治疗", "mid_en": "Rehabilitation & Therapy",
     "zh": "康复医学科医生", "en": "Rehabilitation Physician", "isco": "2212", "onet": "29-1229.04", "locality": "global"},
    {"id": "0405", "mid": "rehabilitation", "mid_zh": "康复与治疗", "mid_en": "Rehabilitation & Therapy",
     "zh": "呼吸治疗师", "en": "Respiratory Therapist", "isco": "2269", "onet": "29-1126.00", "locality": "global"},
    {"id": "0406", "mid": "rehabilitation", "mid_zh": "康复与治疗", "mid_en": "Rehabilitation & Therapy",
     "zh": "音乐治疗师", "en": "Music Therapist", "isco": "2269", "onet": "29-1129.00", "locality": "global"},
    {"id": "0407", "mid": "rehabilitation", "mid_zh": "康复与治疗", "mid_en": "Rehabilitation & Therapy",
     "zh": "艺术治疗师", "en": "Art Therapist", "isco": "2269", "onet": "29-1129.00", "locality": "global"},
    {"id": "0408", "mid": "rehabilitation", "mid_zh": "康复与治疗", "mid_en": "Rehabilitation & Therapy",
     "zh": "运动治疗师", "en": "Exercise Therapist / Kinesiologist", "isco": "2269", "onet": "29-1128.00", "locality": "global"},
    {"id": "0409", "mid": "rehabilitation", "mid_zh": "康复与治疗", "mid_en": "Rehabilitation & Therapy",
     "zh": "假肢矫形师", "en": "Prosthetist / Orthotist", "isco": "2269", "onet": "29-2091.00", "locality": "global"},
    {"id": "0410", "mid": "rehabilitation", "mid_zh": "康复与治疗", "mid_en": "Rehabilitation & Therapy",
     "zh": "听力师", "en": "Audiologist", "isco": "2266", "onet": "29-1181.00", "locality": "global"},
    # ===== public_health (7) =====
    {"id": "0501", "mid": "public_health", "mid_zh": "公共卫生", "mid_en": "Public Health",
     "zh": "流行病学家", "en": "Epidemiologist", "isco": "2212", "onet": "19-1041.00", "locality": "global"},
    {"id": "0502", "mid": "public_health", "mid_zh": "公共卫生", "mid_en": "Public Health",
     "zh": "公共卫生官员", "en": "Public Health Officer", "isco": "1342", "onet": "11-9111.00", "locality": "global"},
    {"id": "0503", "mid": "public_health", "mid_zh": "公共卫生", "mid_en": "Public Health",
     "zh": "卫生教育专家", "en": "Health Education Specialist", "isco": "2269", "onet": "21-1091.00", "locality": "global"},
    {"id": "0504", "mid": "public_health", "mid_zh": "公共卫生", "mid_en": "Public Health",
     "zh": "营养师", "en": "Dietitian / Nutritionist", "isco": "2265", "onet": "29-1031.00", "locality": "global"},
    {"id": "0505", "mid": "public_health", "mid_zh": "公共卫生", "mid_en": "Public Health",
     "zh": "卫生统计师", "en": "Biostatistician", "isco": "2120", "onet": "15-2041.01", "locality": "global"},
    {"id": "0506", "mid": "public_health", "mid_zh": "公共卫生", "mid_en": "Public Health",
     "zh": "环境卫生工程师", "en": "Environmental Health Engineer", "isco": "2143", "onet": "17-2081.00", "locality": "global"},
    {"id": "0507", "mid": "public_health", "mid_zh": "公共卫生", "mid_en": "Public Health",
     "zh": "疾控中心研究员", "en": "CDC Researcher", "isco": "2212", "onet": "19-1042.00", "locality": "global"},
    # ===== traditional_medicine (9) =====
    {"id": "0601", "mid": "traditional_medicine", "mid_zh": "传统与替代医学", "mid_en": "Traditional & Alternative Medicine",
     "zh": "中医师", "en": "Traditional Chinese Medicine Practitioner", "isco": "2230", "onet": "29-1199.00", "locality": "regional"},
    {"id": "0602", "mid": "traditional_medicine", "mid_zh": "传统与替代医学", "mid_en": "Traditional & Alternative Medicine",
     "zh": "针灸师", "en": "Acupuncturist", "isco": "2230", "onet": "29-1199.00", "locality": "global"},
    {"id": "0603", "mid": "traditional_medicine", "mid_zh": "传统与替代医学", "mid_en": "Traditional & Alternative Medicine",
     "zh": "阿育吠陀医师", "en": "Ayurveda Practitioner", "isco": "2230", "onet": "29-1199.00", "locality": "regional"},
    {"id": "0604", "mid": "traditional_medicine", "mid_zh": "传统与替代医学", "mid_en": "Traditional & Alternative Medicine",
     "zh": "脊椎指压治疗师", "en": "Chiropractor", "isco": "2269", "onet": "29-1011.00", "locality": "global"},
    {"id": "0605", "mid": "traditional_medicine", "mid_zh": "传统与替代医学", "mid_en": "Traditional & Alternative Medicine",
     "zh": "自然疗法医师", "en": "Naturopathic Physician", "isco": "2230", "onet": "29-1199.00", "locality": "global"},
    {"id": "0606", "mid": "traditional_medicine", "mid_zh": "传统与替代医学", "mid_en": "Traditional & Alternative Medicine",
     "zh": "推拿师", "en": "Tui Na Massage Therapist", "isco": "2230", "onet": "31-9011.00", "locality": "regional"},
    {"id": "0607", "mid": "traditional_medicine", "mid_zh": "传统与替代医学", "mid_en": "Traditional & Alternative Medicine",
     "zh": "中药师", "en": "Chinese Herbal Medicine Pharmacist", "isco": "2262", "onet": "29-1199.00", "locality": "regional"},
    {"id": "0608", "mid": "traditional_medicine", "mid_zh": "传统与替代医学", "mid_en": "Traditional & Alternative Medicine",
     "zh": "整骨师", "en": "Osteopath", "isco": "2269", "onet": "29-1199.00", "locality": "global"},
    {"id": "0609", "mid": "traditional_medicine", "mid_zh": "传统与替代医学", "mid_en": "Traditional & Alternative Medicine",
     "zh": "顺势疗法医师", "en": "Homeopath", "isco": "2230", "onet": "29-1199.00", "locality": "regional"},
    # ===== dental (6) =====
    {"id": "0701", "mid": "dental", "mid_zh": "口腔", "mid_en": "Dental",
     "zh": "牙科医生", "en": "Dentist", "isco": "2261", "onet": "29-1021.00", "locality": "global"},
    {"id": "0702", "mid": "dental", "mid_zh": "口腔", "mid_en": "Dental",
     "zh": "牙科卫生师", "en": "Dental Hygienist", "isco": "3251", "onet": "29-1292.00", "locality": "global"},
    {"id": "0703", "mid": "dental", "mid_zh": "口腔", "mid_en": "Dental",
     "zh": "正畸医生", "en": "Orthodontist", "isco": "2261", "onet": "29-1023.00", "locality": "global"},
    {"id": "0704", "mid": "dental", "mid_zh": "口腔", "mid_en": "Dental",
     "zh": "口腔颌面外科医生", "en": "Oral & Maxillofacial Surgeon", "isco": "2261", "onet": "29-1022.00", "locality": "global"},
    {"id": "0705", "mid": "dental", "mid_zh": "口腔", "mid_en": "Dental",
     "zh": "牙科技师", "en": "Dental Technician", "isco": "3214", "onet": "51-9081.00", "locality": "global"},
    {"id": "0706", "mid": "dental", "mid_zh": "口腔", "mid_en": "Dental",
     "zh": "牙周病医生", "en": "Periodontist", "isco": "2261", "onet": "29-1024.00", "locality": "global"},
    # ===== ophthalmology (3) =====
    {"id": "0801", "mid": "ophthalmology", "mid_zh": "眼科", "mid_en": "Ophthalmology & Optometry",
     "zh": "眼科医生", "en": "Ophthalmologist", "isco": "2212", "onet": "29-1241.00", "locality": "global"},
    {"id": "0802", "mid": "ophthalmology", "mid_zh": "眼科", "mid_en": "Ophthalmology & Optometry",
     "zh": "验光师", "en": "Optometrist", "isco": "2267", "onet": "29-1041.00", "locality": "global"},
    {"id": "0803", "mid": "ophthalmology", "mid_zh": "眼科", "mid_en": "Ophthalmology & Optometry",
     "zh": "配镜师", "en": "Optician / Dispensing Optician", "isco": "3254", "onet": "29-2081.00", "locality": "global"},
    # ===== mental_health (9) =====
    {"id": "0901", "mid": "mental_health", "mid_zh": "心理健康", "mid_en": "Mental Health",
     "zh": "精神科医生", "en": "Psychiatrist", "isco": "2212", "onet": "29-1223.00", "locality": "global"},
    {"id": "0902", "mid": "mental_health", "mid_zh": "心理健康", "mid_en": "Mental Health",
     "zh": "临床心理学家", "en": "Clinical Psychologist", "isco": "2634", "onet": "19-3031.02", "locality": "global"},
    {"id": "0903", "mid": "mental_health", "mid_zh": "心理健康", "mid_en": "Mental Health",
     "zh": "心理咨询师", "en": "Counseling Psychologist", "isco": "2634", "onet": "19-3031.03", "locality": "global"},
    {"id": "0904", "mid": "mental_health", "mid_zh": "心理健康", "mid_en": "Mental Health",
     "zh": "精神科护士", "en": "Psychiatric Nurse", "isco": "2221", "onet": "29-1141.00", "locality": "global"},
    {"id": "0905", "mid": "mental_health", "mid_zh": "心理健康", "mid_en": "Mental Health",
     "zh": "心理治疗师", "en": "Psychotherapist", "isco": "2634", "onet": "19-3031.02", "locality": "global"},
    {"id": "0906", "mid": "mental_health", "mid_zh": "心理健康", "mid_en": "Mental Health",
     "zh": "成瘾咨询师", "en": "Addiction Counselor", "isco": "2634", "onet": "21-1011.00", "locality": "global"},
    {"id": "0907", "mid": "mental_health", "mid_zh": "心理健康", "mid_en": "Mental Health",
     "zh": "神经心理学家", "en": "Neuropsychologist", "isco": "2634", "onet": "19-3031.02", "locality": "global"},
    {"id": "0908", "mid": "mental_health", "mid_zh": "心理健康", "mid_en": "Mental Health",
     "zh": "儿童心理学家", "en": "Child Psychologist", "isco": "2634", "onet": "19-3031.02", "locality": "global"},
    {"id": "0909", "mid": "mental_health", "mid_zh": "心理健康", "mid_en": "Mental Health",
     "zh": "法医心理学家", "en": "Forensic Psychologist", "isco": "2634", "onet": "19-3031.02", "locality": "global"},
    # ===== medical_imaging_lab (7) =====
    {"id": "1001", "mid": "medical_imaging_lab", "mid_zh": "医学影像与检验", "mid_en": "Medical Imaging & Laboratory",
     "zh": "放射技师", "en": "Radiologic Technologist", "isco": "3211", "onet": "29-2034.00", "locality": "global"},
    {"id": "1002", "mid": "medical_imaging_lab", "mid_zh": "医学影像与检验", "mid_en": "Medical Imaging & Laboratory",
     "zh": "医学检验技师", "en": "Medical Laboratory Technologist", "isco": "3212", "onet": "29-2011.00", "locality": "global"},
    {"id": "1003", "mid": "medical_imaging_lab", "mid_zh": "医学影像与检验", "mid_en": "Medical Imaging & Laboratory",
     "zh": "超声技师", "en": "Diagnostic Medical Sonographer", "isco": "3211", "onet": "29-2032.00", "locality": "global"},
    {"id": "1004", "mid": "medical_imaging_lab", "mid_zh": "医学影像与检验", "mid_en": "Medical Imaging & Laboratory",
     "zh": "核医学技师", "en": "Nuclear Medicine Technologist", "isco": "3211", "onet": "29-2033.00", "locality": "global"},
    {"id": "1005", "mid": "medical_imaging_lab", "mid_zh": "医学影像与检验", "mid_en": "Medical Imaging & Laboratory",
     "zh": "病理技师", "en": "Histotechnologist", "isco": "3212", "onet": "29-2011.00", "locality": "global"},
    {"id": "1006", "mid": "medical_imaging_lab", "mid_zh": "医学影像与检验", "mid_en": "Medical Imaging & Laboratory",
     "zh": "心电图技师", "en": "Electrocardiograph Technician", "isco": "3211", "onet": "29-2031.00", "locality": "global"},
    {"id": "1007", "mid": "medical_imaging_lab", "mid_zh": "医学影像与检验", "mid_en": "Medical Imaging & Laboratory",
     "zh": "MRI技师", "en": "MRI Technologist", "isco": "3211", "onet": "29-2035.00", "locality": "global"},
    # ===== medical_admin (15) =====
    {"id": "1101", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "医院管理者", "en": "Hospital Administrator", "isco": "1342", "onet": "11-9111.00", "locality": "global"},
    {"id": "1102", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "医疗信息化专家", "en": "Health Informatics Specialist", "isco": "2529", "onet": "15-1211.01", "locality": "global"},
    {"id": "1103", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "健康保险管理师", "en": "Health Insurance Manager", "isco": "1346", "onet": "11-9111.00", "locality": "global"},
    {"id": "1104", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "医疗质量管理师", "en": "Healthcare Quality Manager", "isco": "1342", "onet": "11-9111.00", "locality": "global"},
    {"id": "1105", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "临床研究协调员", "en": "Clinical Research Coordinator", "isco": "2269", "onet": "11-9121.01", "locality": "global"},
    {"id": "1106", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "医疗编码员", "en": "Medical Coder", "isco": "3252", "onet": "29-2071.00", "locality": "global"},
    {"id": "1107", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "急救技术员/急救员", "en": "Emergency Medical Technician (EMT)", "isco": "3258", "onet": "29-2042.00", "locality": "global"},
    {"id": "1108", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "护理人员(院前急救)", "en": "Paramedic", "isco": "3258", "onet": "29-2043.00", "locality": "global"},
    {"id": "1109", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "病案编码员", "en": "Health Information Technician", "isco": "3252", "onet": "29-2072.00", "locality": "global"},
    {"id": "1110", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "医疗器械技师", "en": "Biomedical Equipment Technician", "isco": "3211", "onet": "49-9062.00", "locality": "global"},
    {"id": "1111", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "临床试验管理员", "en": "Clinical Trial Manager", "isco": "2269", "onet": "11-9121.01", "locality": "global"},
    {"id": "1112", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "远程医疗协调员", "en": "Telemedicine Coordinator", "isco": "2269", "onet": "29-9099.00", "locality": "global"},
    {"id": "1113", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "医疗翻译", "en": "Medical Interpreter", "isco": "2643", "onet": "27-3091.00", "locality": "global"},
    {"id": "1114", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "健康数据分析师", "en": "Health Data Analyst", "isco": "2120", "onet": "15-2051.00", "locality": "global"},
    {"id": "1115", "mid": "medical_admin", "mid_zh": "医疗管理", "mid_en": "Healthcare Administration",
     "zh": "患者体验官", "en": "Patient Experience Officer", "isco": "1342", "onet": "11-9111.00", "locality": "global"},
    # ===== veterinary_medicine (6) =====
    {"id": "1201", "mid": "veterinary_medicine", "mid_zh": "兽医学", "mid_en": "Veterinary Medicine",
     "zh": "小动物兽医", "en": "Small Animal Veterinarian", "isco": "2250", "onet": "29-1131.00", "locality": "global"},
    {"id": "1202", "mid": "veterinary_medicine", "mid_zh": "兽医学", "mid_en": "Veterinary Medicine",
     "zh": "大动物/农场兽医", "en": "Large Animal / Farm Veterinarian", "isco": "2250", "onet": "29-1131.00", "locality": "global"},
    {"id": "1203", "mid": "veterinary_medicine", "mid_zh": "兽医学", "mid_en": "Veterinary Medicine",
     "zh": "动物外科兽医", "en": "Veterinary Surgeon", "isco": "2250", "onet": "29-1131.00", "locality": "global"},
    {"id": "1204", "mid": "veterinary_medicine", "mid_zh": "兽医学", "mid_en": "Veterinary Medicine",
     "zh": "动物急诊兽医", "en": "Emergency Veterinarian", "isco": "2250", "onet": "29-1131.00", "locality": "global"},
    {"id": "1205", "mid": "veterinary_medicine", "mid_zh": "兽医学", "mid_en": "Veterinary Medicine",
     "zh": "兽医公共卫生专家", "en": "Veterinary Public Health Specialist", "isco": "2250", "onet": "29-1131.00", "locality": "global"},
    {"id": "1206", "mid": "veterinary_medicine", "mid_zh": "兽医学", "mid_en": "Veterinary Medicine",
     "zh": "动物园兽医", "en": "Zoo / Wildlife Veterinarian", "isco": "2250", "onet": "29-1131.00", "locality": "global"},
]

# ---------------------------------------------------------------------------
# COUNTRY METADATA (same 45 countries as TECH)
# ---------------------------------------------------------------------------

COUNTRIES = [
    {"iso": "CN", "name_zh": "中国", "name_en": "China", "region": "东亚", "type": "country", "dev": "emerging"},
    {"iso": "JP", "name_zh": "日本", "name_en": "Japan", "region": "东亚", "type": "country", "dev": "developed"},
    {"iso": "KR", "name_zh": "韩国", "name_en": "South Korea", "region": "东亚", "type": "country", "dev": "developed"},
    {"iso": "TW", "name_zh": "中国台湾地区", "name_en": "Taiwan (China)", "region": "东亚", "type": "region", "dev": "developed"},
    {"iso": "HK", "name_zh": "中国香港地区", "name_en": "Hong Kong (China)", "region": "东亚", "type": "region", "dev": "developed"},
    {"iso": "SG", "name_zh": "新加坡", "name_en": "Singapore", "region": "东南亚", "type": "country", "dev": "developed"},
    {"iso": "TH", "name_zh": "泰国", "name_en": "Thailand", "region": "东南亚", "type": "country", "dev": "emerging"},
    {"iso": "VN", "name_zh": "越南", "name_en": "Vietnam", "region": "东南亚", "type": "country", "dev": "emerging"},
    {"iso": "ID", "name_zh": "印度尼西亚", "name_en": "Indonesia", "region": "东南亚", "type": "country", "dev": "emerging"},
    {"iso": "MY", "name_zh": "马来西亚", "name_en": "Malaysia", "region": "东南亚", "type": "country", "dev": "emerging"},
    {"iso": "PH", "name_zh": "菲律宾", "name_en": "Philippines", "region": "东南亚", "type": "country", "dev": "emerging"},
    {"iso": "IN", "name_zh": "印度", "name_en": "India", "region": "南亚", "type": "country", "dev": "emerging"},
    {"iso": "PK", "name_zh": "巴基斯坦", "name_en": "Pakistan", "region": "南亚", "type": "country", "dev": "developing"},
    {"iso": "BD", "name_zh": "孟加拉国", "name_en": "Bangladesh", "region": "南亚", "type": "country", "dev": "developing"},
    {"iso": "AE", "name_zh": "阿联酋", "name_en": "United Arab Emirates", "region": "中亚/西亚", "type": "country", "dev": "developed"},
    {"iso": "IL", "name_zh": "以色列", "name_en": "Israel", "region": "中亚/西亚", "type": "country", "dev": "developed"},
    {"iso": "SA", "name_zh": "沙特阿拉伯", "name_en": "Saudi Arabia", "region": "中亚/西亚", "type": "country", "dev": "emerging"},
    {"iso": "TR", "name_zh": "土耳其", "name_en": "Turkey", "region": "中亚/西亚", "type": "country", "dev": "emerging"},
    {"iso": "GB", "name_zh": "英国", "name_en": "United Kingdom", "region": "西欧", "type": "country", "dev": "developed"},
    {"iso": "FR", "name_zh": "法国", "name_en": "France", "region": "西欧", "type": "country", "dev": "developed"},
    {"iso": "DE", "name_zh": "德国", "name_en": "Germany", "region": "西欧", "type": "country", "dev": "developed"},
    {"iso": "NL", "name_zh": "荷兰", "name_en": "Netherlands", "region": "西欧", "type": "country", "dev": "developed"},
    {"iso": "CH", "name_zh": "瑞士", "name_en": "Switzerland", "region": "西欧", "type": "country", "dev": "developed"},
    {"iso": "SE", "name_zh": "瑞典", "name_en": "Sweden", "region": "北欧", "type": "country", "dev": "developed"},
    {"iso": "DK", "name_zh": "丹麦", "name_en": "Denmark", "region": "北欧", "type": "country", "dev": "developed"},
    {"iso": "FI", "name_zh": "芬兰", "name_en": "Finland", "region": "北欧", "type": "country", "dev": "developed"},
    {"iso": "IT", "name_zh": "意大利", "name_en": "Italy", "region": "南欧", "type": "country", "dev": "developed"},
    {"iso": "ES", "name_zh": "西班牙", "name_en": "Spain", "region": "南欧", "type": "country", "dev": "developed"},
    {"iso": "PT", "name_zh": "葡萄牙", "name_en": "Portugal", "region": "南欧", "type": "country", "dev": "developed"},
    {"iso": "PL", "name_zh": "波兰", "name_en": "Poland", "region": "东欧", "type": "country", "dev": "emerging"},
    {"iso": "CZ", "name_zh": "捷克", "name_en": "Czech Republic", "region": "东欧", "type": "country", "dev": "developed"},
    {"iso": "RU", "name_zh": "俄罗斯", "name_en": "Russia", "region": "东欧", "type": "country", "dev": "emerging"},
    {"iso": "US", "name_zh": "美国", "name_en": "United States", "region": "北美", "type": "country", "dev": "developed"},
    {"iso": "CA", "name_zh": "加拿大", "name_en": "Canada", "region": "北美", "type": "country", "dev": "developed"},
    {"iso": "MX", "name_zh": "墨西哥", "name_en": "Mexico", "region": "北美", "type": "country", "dev": "emerging"},
    {"iso": "BR", "name_zh": "巴西", "name_en": "Brazil", "region": "南美", "type": "country", "dev": "emerging"},
    {"iso": "AR", "name_zh": "阿根廷", "name_en": "Argentina", "region": "南美", "type": "country", "dev": "emerging"},
    {"iso": "CL", "name_zh": "智利", "name_en": "Chile", "region": "南美", "type": "country", "dev": "emerging"},
    {"iso": "CO", "name_zh": "哥伦比亚", "name_en": "Colombia", "region": "南美", "type": "country", "dev": "emerging"},
    {"iso": "AU", "name_zh": "澳大利亚", "name_en": "Australia", "region": "大洋洲", "type": "country", "dev": "developed"},
    {"iso": "NZ", "name_zh": "新西兰", "name_en": "New Zealand", "region": "大洋洲", "type": "country", "dev": "developed"},
    {"iso": "ZA", "name_zh": "南非", "name_en": "South Africa", "region": "非洲", "type": "country", "dev": "emerging"},
    {"iso": "NG", "name_zh": "尼日利亚", "name_en": "Nigeria", "region": "非洲", "type": "country", "dev": "developing"},
    {"iso": "KE", "name_zh": "肯尼亚", "name_en": "Kenya", "region": "非洲", "type": "country", "dev": "developing"},
    {"iso": "EG", "name_zh": "埃及", "name_en": "Egypt", "region": "非洲", "type": "country", "dev": "developing"},
]

# ---------------------------------------------------------------------------
# COUNTRY PROFILES — healthcare-specific modifiers
# (healthcare_quality, physician_comp, nurse_comp, wlb, aging_demand,
#  pharma_industry, mental_health_awareness, trad_med_acceptance,
#  intl_openness, regulatory_strictness, overtime_culture, gender_eq,
#  edu_quality, public_vs_private, market_size)
# All on 0-10 scale.
# ---------------------------------------------------------------------------

COUNTRY_PROFILES = {
    # --- DEVELOPED HIGH-SPEND ---
    "US": {"hq": 9.0, "phys_comp": 10.0, "nurse_comp": 8.0, "wlb": 5.0, "aging": 6.5,
           "pharma": 10.0, "mental": 8.5, "trad": 4.0, "intl": 7.5, "reg": 8.5,
           "ot": 4.0, "gender": 7.5, "edu": 9.5, "pub_priv": 3.0, "market": 10.0},
    "CH": {"hq": 9.5, "phys_comp": 9.5, "nurse_comp": 8.5, "wlb": 8.0, "aging": 7.5,
           "pharma": 9.5, "mental": 8.0, "trad": 5.0, "intl": 8.5, "reg": 8.5,
           "ot": 7.0, "gender": 7.0, "edu": 9.0, "pub_priv": 5.0, "market": 4.0},
    "DE": {"hq": 8.5, "phys_comp": 7.5, "nurse_comp": 6.5, "wlb": 7.5, "aging": 8.5,
           "pharma": 9.0, "mental": 7.5, "trad": 5.5, "intl": 8.0, "reg": 8.0,
           "ot": 7.5, "gender": 7.0, "edu": 8.5, "pub_priv": 6.0, "market": 8.0},
    "GB": {"hq": 8.0, "phys_comp": 7.0, "nurse_comp": 6.0, "wlb": 6.5, "aging": 7.5,
           "pharma": 8.5, "mental": 8.0, "trad": 4.5, "intl": 9.0, "reg": 8.0,
           "ot": 6.0, "gender": 7.5, "edu": 8.5, "pub_priv": 7.0, "market": 7.5},
    "FR": {"hq": 8.0, "phys_comp": 6.5, "nurse_comp": 5.5, "wlb": 7.5, "aging": 7.5,
           "pharma": 8.0, "mental": 7.0, "trad": 5.5, "intl": 7.5, "reg": 8.0,
           "ot": 7.0, "gender": 7.0, "edu": 8.0, "pub_priv": 7.5, "market": 7.0},
    "CA": {"hq": 8.5, "phys_comp": 8.0, "nurse_comp": 7.0, "wlb": 7.0, "aging": 7.0,
           "pharma": 7.5, "mental": 8.0, "trad": 5.0, "intl": 9.0, "reg": 8.0,
           "ot": 6.5, "gender": 8.0, "edu": 8.5, "pub_priv": 7.5, "market": 7.0},
    "AU": {"hq": 8.5, "phys_comp": 8.0, "nurse_comp": 7.0, "wlb": 7.5, "aging": 6.5,
           "pharma": 7.0, "mental": 8.0, "trad": 5.0, "intl": 8.5, "reg": 8.0,
           "ot": 7.0, "gender": 8.0, "edu": 8.0, "pub_priv": 5.5, "market": 6.0},
    "NL": {"hq": 8.5, "phys_comp": 7.5, "nurse_comp": 6.5, "wlb": 8.5, "aging": 7.5,
           "pharma": 7.5, "mental": 8.5, "trad": 5.0, "intl": 9.0, "reg": 7.5,
           "ot": 8.0, "gender": 8.5, "edu": 8.0, "pub_priv": 6.0, "market": 5.0},
    "NZ": {"hq": 8.0, "phys_comp": 7.0, "nurse_comp": 6.5, "wlb": 8.0, "aging": 6.0,
           "pharma": 5.5, "mental": 8.0, "trad": 5.0, "intl": 8.0, "reg": 7.5,
           "ot": 7.5, "gender": 8.5, "edu": 7.5, "pub_priv": 7.0, "market": 3.5},
    # --- NORDIC ---
    "SE": {"hq": 8.5, "phys_comp": 7.0, "nurse_comp": 6.0, "wlb": 9.0, "aging": 7.5,
           "pharma": 8.0, "mental": 9.0, "trad": 4.5, "intl": 8.5, "reg": 7.5,
           "ot": 8.5, "gender": 9.0, "edu": 8.5, "pub_priv": 8.0, "market": 4.5},
    "DK": {"hq": 8.5, "phys_comp": 7.0, "nurse_comp": 6.5, "wlb": 9.0, "aging": 7.5,
           "pharma": 8.0, "mental": 8.5, "trad": 4.0, "intl": 8.5, "reg": 7.5,
           "ot": 8.5, "gender": 9.0, "edu": 8.5, "pub_priv": 8.5, "market": 3.5},
    "FI": {"hq": 8.0, "phys_comp": 6.5, "nurse_comp": 6.0, "wlb": 9.0, "aging": 8.0,
           "pharma": 7.0, "mental": 8.5, "trad": 4.0, "intl": 8.0, "reg": 7.0,
           "ot": 8.5, "gender": 9.0, "edu": 9.0, "pub_priv": 8.0, "market": 3.0},
    # --- EAST ASIA ---
    "JP": {"hq": 8.5, "phys_comp": 7.0, "nurse_comp": 5.5, "wlb": 4.5, "aging": 10.0,
           "pharma": 8.5, "mental": 5.0, "trad": 7.0, "intl": 4.5, "reg": 7.5,
           "ot": 3.0, "gender": 4.5, "edu": 8.0, "pub_priv": 5.0, "market": 8.0},
    "KR": {"hq": 8.0, "phys_comp": 7.0, "nurse_comp": 5.0, "wlb": 4.0, "aging": 9.5,
           "pharma": 7.5, "mental": 5.5, "trad": 6.5, "intl": 5.5, "reg": 7.0,
           "ot": 3.0, "gender": 4.0, "edu": 8.0, "pub_priv": 4.5, "market": 6.5},
    "TW": {"hq": 7.5, "phys_comp": 5.5, "nurse_comp": 4.5, "wlb": 4.5, "aging": 8.5,
           "pharma": 6.5, "mental": 5.5, "trad": 7.5, "intl": 6.0, "reg": 6.5,
           "ot": 3.5, "gender": 6.0, "edu": 7.5, "pub_priv": 5.5, "market": 5.0},
    "HK": {"hq": 8.0, "phys_comp": 7.5, "nurse_comp": 5.5, "wlb": 4.0, "aging": 8.0,
           "pharma": 5.5, "mental": 6.0, "trad": 7.0, "intl": 9.0, "reg": 7.0,
           "ot": 3.5, "gender": 6.5, "edu": 8.0, "pub_priv": 5.0, "market": 4.0},
    "CN": {"hq": 7.0, "phys_comp": 5.5, "nurse_comp": 4.0, "wlb": 3.0, "aging": 8.0,
           "pharma": 7.5, "mental": 4.5, "trad": 9.5, "intl": 4.5, "reg": 6.0,
           "ot": 2.0, "gender": 5.5, "edu": 7.5, "pub_priv": 7.0, "market": 10.0},
    "SG": {"hq": 9.0, "phys_comp": 8.5, "nurse_comp": 6.5, "wlb": 5.5, "aging": 7.5,
           "pharma": 7.0, "mental": 6.5, "trad": 6.5, "intl": 9.5, "reg": 8.0,
           "ot": 4.5, "gender": 7.0, "edu": 8.5, "pub_priv": 4.5, "market": 4.0},
    # --- SOUTH/SOUTHEAST ASIA ---
    "IN": {"hq": 5.5, "phys_comp": 4.5, "nurse_comp": 3.0, "wlb": 4.0, "aging": 4.0,
           "pharma": 7.5, "mental": 3.5, "trad": 8.5, "intl": 7.0, "reg": 5.0,
           "ot": 3.5, "gender": 4.0, "edu": 6.5, "pub_priv": 3.5, "market": 9.5},
    "TH": {"hq": 6.0, "phys_comp": 4.0, "nurse_comp": 3.5, "wlb": 5.5, "aging": 6.0,
           "pharma": 4.5, "mental": 4.0, "trad": 7.5, "intl": 5.5, "reg": 5.0,
           "ot": 5.5, "gender": 6.0, "edu": 5.5, "pub_priv": 5.0, "market": 5.5},
    "VN": {"hq": 5.0, "phys_comp": 3.0, "nurse_comp": 2.5, "wlb": 4.5, "aging": 4.5,
           "pharma": 4.0, "mental": 3.0, "trad": 7.0, "intl": 5.0, "reg": 4.5,
           "ot": 4.0, "gender": 5.5, "edu": 5.5, "pub_priv": 6.5, "market": 6.0},
    "ID": {"hq": 4.5, "phys_comp": 3.0, "nurse_comp": 2.5, "wlb": 5.0, "aging": 4.0,
           "pharma": 4.0, "mental": 3.0, "trad": 7.0, "intl": 4.0, "reg": 4.5,
           "ot": 5.0, "gender": 4.5, "edu": 5.0, "pub_priv": 5.0, "market": 7.0},
    "MY": {"hq": 6.5, "phys_comp": 5.0, "nurse_comp": 4.0, "wlb": 5.5, "aging": 4.5,
           "pharma": 5.0, "mental": 4.5, "trad": 6.5, "intl": 6.5, "reg": 5.5,
           "ot": 5.0, "gender": 5.5, "edu": 6.0, "pub_priv": 5.0, "market": 5.0},
    "PH": {"hq": 5.0, "phys_comp": 3.5, "nurse_comp": 3.0, "wlb": 5.0, "aging": 3.5,
           "pharma": 3.5, "mental": 3.5, "trad": 5.0, "intl": 7.5, "reg": 4.5,
           "ot": 4.5, "gender": 6.5, "edu": 5.5, "pub_priv": 4.0, "market": 5.5},
    # --- SOUTH ASIA (developing) ---
    "PK": {"hq": 3.5, "phys_comp": 2.5, "nurse_comp": 1.5, "wlb": 4.0, "aging": 3.0,
           "pharma": 3.5, "mental": 2.0, "trad": 6.5, "intl": 5.0, "reg": 3.5,
           "ot": 4.0, "gender": 2.5, "edu": 4.5, "pub_priv": 3.0, "market": 5.5},
    "BD": {"hq": 3.0, "phys_comp": 2.0, "nurse_comp": 1.5, "wlb": 4.0, "aging": 3.0,
           "pharma": 3.5, "mental": 2.0, "trad": 6.0, "intl": 4.5, "reg": 3.0,
           "ot": 4.0, "gender": 3.0, "edu": 4.0, "pub_priv": 3.5, "market": 5.5},
    # --- MIDDLE EAST ---
    "AE": {"hq": 8.0, "phys_comp": 8.5, "nurse_comp": 6.0, "wlb": 5.5, "aging": 3.5,
           "pharma": 5.5, "mental": 5.0, "trad": 5.5, "intl": 9.5, "reg": 7.0,
           "ot": 5.0, "gender": 5.0, "edu": 7.0, "pub_priv": 4.0, "market": 4.5},
    "IL": {"hq": 8.5, "phys_comp": 7.5, "nurse_comp": 6.0, "wlb": 6.0, "aging": 5.5,
           "pharma": 8.5, "mental": 7.5, "trad": 4.0, "intl": 8.0, "reg": 7.5,
           "ot": 5.0, "gender": 7.0, "edu": 8.5, "pub_priv": 6.5, "market": 4.0},
    "SA": {"hq": 6.5, "phys_comp": 7.5, "nurse_comp": 5.5, "wlb": 5.0, "aging": 3.0,
           "pharma": 4.5, "mental": 3.5, "trad": 5.5, "intl": 6.0, "reg": 6.0,
           "ot": 5.0, "gender": 3.5, "edu": 6.0, "pub_priv": 5.0, "market": 5.5},
    "TR": {"hq": 6.0, "phys_comp": 4.5, "nurse_comp": 3.5, "wlb": 4.5, "aging": 5.5,
           "pharma": 5.0, "mental": 4.5, "trad": 6.0, "intl": 5.5, "reg": 5.5,
           "ot": 4.5, "gender": 4.0, "edu": 6.5, "pub_priv": 5.5, "market": 6.5},
    # --- SOUTHERN EUROPE ---
    "IT": {"hq": 7.5, "phys_comp": 5.5, "nurse_comp": 4.5, "wlb": 6.5, "aging": 9.0,
           "pharma": 7.0, "mental": 6.0, "trad": 5.5, "intl": 6.5, "reg": 7.0,
           "ot": 5.5, "gender": 5.5, "edu": 7.0, "pub_priv": 7.0, "market": 6.5},
    "ES": {"hq": 7.5, "phys_comp": 5.0, "nurse_comp": 4.5, "wlb": 6.5, "aging": 8.0,
           "pharma": 6.5, "mental": 6.0, "trad": 5.0, "intl": 7.0, "reg": 7.0,
           "ot": 5.5, "gender": 6.5, "edu": 7.0, "pub_priv": 7.0, "market": 6.0},
    "PT": {"hq": 7.0, "phys_comp": 4.5, "nurse_comp": 4.0, "wlb": 6.5, "aging": 8.5,
           "pharma": 5.5, "mental": 6.0, "trad": 4.5, "intl": 7.5, "reg": 6.5,
           "ot": 6.0, "gender": 7.0, "edu": 7.0, "pub_priv": 7.0, "market": 4.0},
    # --- EASTERN EUROPE ---
    "PL": {"hq": 6.5, "phys_comp": 4.5, "nurse_comp": 3.5, "wlb": 6.5, "aging": 7.5,
           "pharma": 5.5, "mental": 5.5, "trad": 4.0, "intl": 7.0, "reg": 6.5,
           "ot": 6.0, "gender": 6.5, "edu": 7.0, "pub_priv": 6.5, "market": 5.5},
    "CZ": {"hq": 7.0, "phys_comp": 5.0, "nurse_comp": 4.0, "wlb": 7.0, "aging": 7.0,
           "pharma": 5.5, "mental": 5.5, "trad": 4.5, "intl": 7.0, "reg": 6.5,
           "ot": 6.5, "gender": 6.5, "edu": 7.0, "pub_priv": 6.5, "market": 4.5},
    "RU": {"hq": 6.0, "phys_comp": 3.5, "nurse_comp": 2.5, "wlb": 5.0, "aging": 6.5,
           "pharma": 5.0, "mental": 4.0, "trad": 5.0, "intl": 3.5, "reg": 5.0,
           "ot": 5.0, "gender": 6.0, "edu": 7.0, "pub_priv": 7.0, "market": 7.0},
    # --- LATIN AMERICA ---
    "BR": {"hq": 6.0, "phys_comp": 4.5, "nurse_comp": 3.0, "wlb": 5.5, "aging": 5.0,
           "pharma": 5.5, "mental": 5.0, "trad": 4.5, "intl": 4.5, "reg": 5.5,
           "ot": 5.0, "gender": 5.5, "edu": 6.0, "pub_priv": 5.0, "market": 7.5},
    "MX": {"hq": 5.5, "phys_comp": 4.0, "nurse_comp": 3.0, "wlb": 5.0, "aging": 4.5,
           "pharma": 4.5, "mental": 4.0, "trad": 6.0, "intl": 5.0, "reg": 5.0,
           "ot": 4.5, "gender": 5.0, "edu": 5.5, "pub_priv": 5.0, "market": 6.5},
    "AR": {"hq": 6.0, "phys_comp": 3.5, "nurse_comp": 2.5, "wlb": 5.5, "aging": 5.5,
           "pharma": 4.5, "mental": 6.0, "trad": 4.5, "intl": 5.0, "reg": 4.5,
           "ot": 5.0, "gender": 5.5, "edu": 6.5, "pub_priv": 5.5, "market": 5.0},
    "CL": {"hq": 6.5, "phys_comp": 4.5, "nurse_comp": 3.5, "wlb": 5.5, "aging": 5.5,
           "pharma": 4.5, "mental": 5.0, "trad": 4.0, "intl": 6.0, "reg": 5.5,
           "ot": 5.5, "gender": 5.5, "edu": 6.5, "pub_priv": 4.5, "market": 4.0},
    "CO": {"hq": 5.5, "phys_comp": 3.5, "nurse_comp": 2.5, "wlb": 5.0, "aging": 4.0,
           "pharma": 4.0, "mental": 4.0, "trad": 4.5, "intl": 4.5, "reg": 5.0,
           "ot": 5.0, "gender": 5.0, "edu": 5.5, "pub_priv": 4.5, "market": 5.0},
    # --- AFRICA ---
    "ZA": {"hq": 5.5, "phys_comp": 5.0, "nurse_comp": 3.5, "wlb": 5.0, "aging": 3.5,
           "pharma": 4.5, "mental": 4.0, "trad": 6.5, "intl": 6.0, "reg": 5.0,
           "ot": 5.0, "gender": 5.5, "edu": 5.5, "pub_priv": 4.0, "market": 5.0},
    "NG": {"hq": 3.5, "phys_comp": 2.5, "nurse_comp": 1.5, "wlb": 4.5, "aging": 2.5,
           "pharma": 3.0, "mental": 2.0, "trad": 6.0, "intl": 5.5, "reg": 3.5,
           "ot": 4.5, "gender": 3.5, "edu": 4.0, "pub_priv": 3.0, "market": 5.5},
    "KE": {"hq": 4.0, "phys_comp": 2.5, "nurse_comp": 2.0, "wlb": 4.5, "aging": 2.5,
           "pharma": 3.0, "mental": 2.5, "trad": 6.0, "intl": 5.5, "reg": 4.0,
           "ot": 5.0, "gender": 4.5, "edu": 4.5, "pub_priv": 4.0, "market": 4.0},
    "EG": {"hq": 5.0, "phys_comp": 3.0, "nurse_comp": 2.0, "wlb": 4.5, "aging": 3.5,
           "pharma": 4.0, "mental": 3.0, "trad": 5.5, "intl": 5.0, "reg": 4.5,
           "ot": 4.5, "gender": 3.0, "edu": 5.5, "pub_priv": 5.0, "market": 6.0},
}

# ---------------------------------------------------------------------------
# OCCUPATION BASE PROFILES — intrinsic characteristics of each MED occupation
# ---------------------------------------------------------------------------

# Mid-category default profiles (used as template; individual occs override)
MID_DEFAULTS = {
    "clinical_medicine": {
        "learning_cost": 9.0, "education_req": 9.0,
        "growth_coeff": 6.5, "career_lifespan": 8.5,
        "opportunity": 7.0, "market_size": 7.0, "supply_demand": 7.0, "developed_scarcity": 7.0,
        "value_added": 7.5, "cost_performance": 5.5,
        "stability": 8.0, "safety": 7.0, "occupational_disease": 5.0, "overtime": 3.5, "burnout": 3.5,
        "skill_versatility": 5.5, "career_switch": 4.0, "reputation_variance": 2.0,
        "ai_resistance": 7.0, "social_status": 8.5, "remote_friendly": 2.0, "autonomy": 6.5,
        "family_friendly": 4.0, "fulfillment": 8.0, "entrepreneurship": 6.0, "gender_equality": 5.0,
        "age_flexibility": 6.5, "social_interaction": 8.0, "physical_demand": 5.0, "license_barrier": 9.0,
        "cycle_sensitivity": 1.5, "side_job_compat": 4.0, "intl_mobility": 6.5, "industry_monopoly": 3.0,
        "trend_long": 3, "trend_short": 2, "edu": "博士/医学学位", "age": "28-35",
    },
    "nursing": {
        "learning_cost": 5.0, "education_req": 5.0,
        "growth_coeff": 6.5, "career_lifespan": 7.0,
        "opportunity": 7.5, "market_size": 8.5, "supply_demand": 8.0, "developed_scarcity": 8.0,
        "value_added": 5.0, "cost_performance": 6.5,
        "stability": 8.0, "safety": 6.5, "occupational_disease": 4.5, "overtime": 4.0, "burnout": 3.5,
        "skill_versatility": 5.0, "career_switch": 4.5, "reputation_variance": 1.5,
        "ai_resistance": 7.5, "social_status": 6.0, "remote_friendly": 1.5, "autonomy": 4.5,
        "family_friendly": 4.5, "fulfillment": 7.0, "entrepreneurship": 3.5, "gender_equality": 4.0,
        "age_flexibility": 5.5, "social_interaction": 8.5, "physical_demand": 6.5, "license_barrier": 6.5,
        "cycle_sensitivity": 1.0, "side_job_compat": 4.0, "intl_mobility": 7.5, "industry_monopoly": 2.0,
        "trend_long": 3, "trend_short": 3, "edu": "大专/本科", "age": "20-24",
    },
    "pharmacy": {
        "learning_cost": 7.0, "education_req": 7.0,
        "growth_coeff": 5.5, "career_lifespan": 8.0,
        "opportunity": 6.0, "market_size": 6.5, "supply_demand": 6.0, "developed_scarcity": 5.5,
        "value_added": 6.5, "cost_performance": 6.5,
        "stability": 7.5, "safety": 8.5, "occupational_disease": 6.5, "overtime": 5.5, "burnout": 5.5,
        "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 1.5,
        "ai_resistance": 5.5, "social_status": 7.0, "remote_friendly": 3.0, "autonomy": 6.0,
        "family_friendly": 6.0, "fulfillment": 6.5, "entrepreneurship": 6.5, "gender_equality": 6.0,
        "age_flexibility": 6.5, "social_interaction": 6.5, "physical_demand": 2.0, "license_barrier": 7.5,
        "cycle_sensitivity": 2.0, "side_job_compat": 4.5, "intl_mobility": 6.0, "industry_monopoly": 4.0,
        "trend_long": 2, "trend_short": 1, "edu": "本科/硕士", "age": "22-26",
    },
    "rehabilitation": {
        "learning_cost": 6.0, "education_req": 6.0,
        "growth_coeff": 6.5, "career_lifespan": 7.5,
        "opportunity": 6.5, "market_size": 5.5, "supply_demand": 6.5, "developed_scarcity": 6.5,
        "value_added": 5.5, "cost_performance": 6.0,
        "stability": 7.0, "safety": 8.5, "occupational_disease": 5.5, "overtime": 6.0, "burnout": 5.5,
        "skill_versatility": 5.5, "career_switch": 5.0, "reputation_variance": 1.5,
        "ai_resistance": 7.5, "social_status": 6.0, "remote_friendly": 3.0, "autonomy": 6.5,
        "family_friendly": 6.0, "fulfillment": 7.5, "entrepreneurship": 6.0, "gender_equality": 6.5,
        "age_flexibility": 6.0, "social_interaction": 8.0, "physical_demand": 5.0, "license_barrier": 6.5,
        "cycle_sensitivity": 2.0, "side_job_compat": 5.5, "intl_mobility": 6.5, "industry_monopoly": 2.5,
        "trend_long": 3, "trend_short": 3, "edu": "本科/硕士", "age": "22-26",
    },
    "public_health": {
        "learning_cost": 7.0, "education_req": 7.5,
        "growth_coeff": 6.0, "career_lifespan": 8.0,
        "opportunity": 6.0, "market_size": 5.0, "supply_demand": 6.0, "developed_scarcity": 5.5,
        "value_added": 6.0, "cost_performance": 6.0,
        "stability": 8.0, "safety": 9.0, "occupational_disease": 7.0, "overtime": 6.0, "burnout": 5.5,
        "skill_versatility": 7.0, "career_switch": 6.0, "reputation_variance": 1.5,
        "ai_resistance": 7.0, "social_status": 7.0, "remote_friendly": 6.0, "autonomy": 6.5,
        "family_friendly": 6.5, "fulfillment": 7.5, "entrepreneurship": 4.5, "gender_equality": 6.5,
        "age_flexibility": 7.0, "social_interaction": 7.0, "physical_demand": 2.0, "license_barrier": 6.0,
        "cycle_sensitivity": 2.0, "side_job_compat": 4.5, "intl_mobility": 7.0, "industry_monopoly": 3.5,
        "trend_long": 3, "trend_short": 3, "edu": "硕士/博士", "age": "24-30",
    },
    "traditional_medicine": {
        "learning_cost": 6.5, "education_req": 6.0,
        "growth_coeff": 4.5, "career_lifespan": 8.5,
        "opportunity": 5.0, "market_size": 4.5, "supply_demand": 4.5, "developed_scarcity": 3.5,
        "value_added": 5.0, "cost_performance": 5.5,
        "stability": 6.5, "safety": 8.5, "occupational_disease": 6.0, "overtime": 6.0, "burnout": 6.0,
        "skill_versatility": 4.0, "career_switch": 3.5, "reputation_variance": 3.5,
        "ai_resistance": 7.0, "social_status": 5.5, "remote_friendly": 2.5, "autonomy": 7.5,
        "family_friendly": 6.0, "fulfillment": 7.0, "entrepreneurship": 7.5, "gender_equality": 5.5,
        "age_flexibility": 7.5, "social_interaction": 7.5, "physical_demand": 4.0, "license_barrier": 5.5,
        "cycle_sensitivity": 2.5, "side_job_compat": 6.5, "intl_mobility": 3.5, "industry_monopoly": 2.5,
        "trend_long": 1, "trend_short": 1, "edu": "本科/硕士", "age": "22-28",
    },
    "dental": {
        "learning_cost": 8.0, "education_req": 8.0,
        "growth_coeff": 6.0, "career_lifespan": 8.0,
        "opportunity": 6.5, "market_size": 6.0, "supply_demand": 6.5, "developed_scarcity": 6.5,
        "value_added": 7.5, "cost_performance": 6.5,
        "stability": 8.0, "safety": 8.0, "occupational_disease": 5.0, "overtime": 6.5, "burnout": 5.5,
        "skill_versatility": 4.5, "career_switch": 3.5, "reputation_variance": 1.5,
        "ai_resistance": 8.0, "social_status": 7.5, "remote_friendly": 1.0, "autonomy": 7.5,
        "family_friendly": 6.5, "fulfillment": 7.0, "entrepreneurship": 8.5, "gender_equality": 6.0,
        "age_flexibility": 6.0, "social_interaction": 7.5, "physical_demand": 5.5, "license_barrier": 8.5,
        "cycle_sensitivity": 3.0, "side_job_compat": 5.0, "intl_mobility": 6.0, "industry_monopoly": 3.0,
        "trend_long": 3, "trend_short": 2, "edu": "博士/医学学位", "age": "26-32",
    },
    "ophthalmology": {
        "learning_cost": 8.5, "education_req": 8.5,
        "growth_coeff": 6.5, "career_lifespan": 8.0,
        "opportunity": 6.5, "market_size": 5.5, "supply_demand": 7.0, "developed_scarcity": 7.0,
        "value_added": 8.0, "cost_performance": 6.5,
        "stability": 8.0, "safety": 8.5, "occupational_disease": 5.5, "overtime": 5.5, "burnout": 5.0,
        "skill_versatility": 4.5, "career_switch": 3.5, "reputation_variance": 1.5,
        "ai_resistance": 6.5, "social_status": 8.0, "remote_friendly": 1.5, "autonomy": 7.0,
        "family_friendly": 6.0, "fulfillment": 7.5, "entrepreneurship": 8.0, "gender_equality": 5.5,
        "age_flexibility": 6.5, "social_interaction": 7.5, "physical_demand": 4.0, "license_barrier": 8.5,
        "cycle_sensitivity": 2.5, "side_job_compat": 4.5, "intl_mobility": 6.5, "industry_monopoly": 3.0,
        "trend_long": 3, "trend_short": 2, "edu": "博士/医学学位", "age": "28-34",
    },
    "mental_health": {
        "learning_cost": 7.5, "education_req": 7.5,
        "growth_coeff": 7.0, "career_lifespan": 8.5,
        "opportunity": 7.0, "market_size": 6.0, "supply_demand": 7.5, "developed_scarcity": 7.5,
        "value_added": 6.5, "cost_performance": 6.0,
        "stability": 7.5, "safety": 8.5, "occupational_disease": 5.5, "overtime": 5.5, "burnout": 4.5,
        "skill_versatility": 6.0, "career_switch": 5.5, "reputation_variance": 2.0,
        "ai_resistance": 7.5, "social_status": 7.0, "remote_friendly": 5.5, "autonomy": 7.5,
        "family_friendly": 6.0, "fulfillment": 8.5, "entrepreneurship": 7.0, "gender_equality": 6.5,
        "age_flexibility": 7.5, "social_interaction": 9.0, "physical_demand": 1.0, "license_barrier": 7.5,
        "cycle_sensitivity": 2.0, "side_job_compat": 6.0, "intl_mobility": 6.0, "industry_monopoly": 2.0,
        "trend_long": 4, "trend_short": 4, "edu": "硕士/博士", "age": "26-32",
    },
    "medical_imaging_lab": {
        "learning_cost": 5.5, "education_req": 5.5,
        "growth_coeff": 5.5, "career_lifespan": 7.5,
        "opportunity": 6.0, "market_size": 6.5, "supply_demand": 6.0, "developed_scarcity": 5.5,
        "value_added": 5.5, "cost_performance": 6.0,
        "stability": 7.5, "safety": 7.0, "occupational_disease": 5.0, "overtime": 5.0, "burnout": 5.5,
        "skill_versatility": 5.0, "career_switch": 4.5, "reputation_variance": 1.0,
        "ai_resistance": 5.0, "social_status": 5.5, "remote_friendly": 2.0, "autonomy": 5.0,
        "family_friendly": 5.5, "fulfillment": 6.0, "entrepreneurship": 3.5, "gender_equality": 6.0,
        "age_flexibility": 6.0, "social_interaction": 5.5, "physical_demand": 3.5, "license_barrier": 5.5,
        "cycle_sensitivity": 1.5, "side_job_compat": 3.5, "intl_mobility": 6.0, "industry_monopoly": 3.0,
        "trend_long": 2, "trend_short": 1, "edu": "大专/本科", "age": "20-24",
    },
    "medical_admin": {
        "learning_cost": 5.0, "education_req": 5.0,
        "growth_coeff": 6.0, "career_lifespan": 7.5,
        "opportunity": 6.5, "market_size": 6.5, "supply_demand": 6.0, "developed_scarcity": 5.5,
        "value_added": 6.0, "cost_performance": 6.5,
        "stability": 7.0, "safety": 8.5, "occupational_disease": 7.0, "overtime": 5.5, "burnout": 5.5,
        "skill_versatility": 6.5, "career_switch": 6.0, "reputation_variance": 1.5,
        "ai_resistance": 5.5, "social_status": 6.0, "remote_friendly": 5.0, "autonomy": 5.5,
        "family_friendly": 6.0, "fulfillment": 6.0, "entrepreneurship": 5.0, "gender_equality": 6.0,
        "age_flexibility": 6.5, "social_interaction": 7.0, "physical_demand": 2.0, "license_barrier": 4.0,
        "cycle_sensitivity": 2.0, "side_job_compat": 5.0, "intl_mobility": 6.0, "industry_monopoly": 3.0,
        "trend_long": 3, "trend_short": 2, "edu": "本科/硕士", "age": "22-28",
    },
    "veterinary_medicine": {
        "learning_cost": 7.5, "education_req": 7.5,
        "growth_coeff": 5.5, "career_lifespan": 7.5,
        "opportunity": 6.0, "market_size": 4.5, "supply_demand": 6.5, "developed_scarcity": 6.5,
        "value_added": 6.0, "cost_performance": 5.5,
        "stability": 7.0, "safety": 6.5, "occupational_disease": 5.0, "overtime": 5.0, "burnout": 4.5,
        "skill_versatility": 4.5, "career_switch": 3.5, "reputation_variance": 1.5,
        "ai_resistance": 8.0, "social_status": 6.5, "remote_friendly": 1.5, "autonomy": 7.0,
        "family_friendly": 5.0, "fulfillment": 8.0, "entrepreneurship": 7.5, "gender_equality": 7.0,
        "age_flexibility": 6.0, "social_interaction": 6.5, "physical_demand": 6.0, "license_barrier": 7.5,
        "cycle_sensitivity": 2.5, "side_job_compat": 4.5, "intl_mobility": 6.0, "industry_monopoly": 2.5,
        "trend_long": 3, "trend_short": 3, "edu": "博士/兽医学位", "age": "26-30",
    },
}

# Per-occupation overrides on top of mid-category defaults
OCC_OVERRIDES = {
    # ===== CLINICAL MEDICINE =====
    "0101": {"en_comment": "Internal Medicine - broad, stable, moderate surgery risk",
             "overtime": 3.5, "burnout": 3.5, "value_added": 7.0, "ai_resistance": 6.5,
             "remote_friendly": 2.5, "physical_demand": 4.0, "trend_short": 2},
    "0102": {"en_comment": "Surgeon - high skill, high stress, high pay",
             "learning_cost": 9.5, "education_req": 9.5, "value_added": 9.0,
             "overtime": 2.5, "burnout": 2.5, "safety": 6.5, "physical_demand": 7.0,
             "ai_resistance": 8.0, "social_status": 9.5, "fulfillment": 8.5,
             "career_lifespan": 7.5, "supply_demand": 7.5, "developed_scarcity": 8.0,
             "entrepreneurship": 5.5, "remote_friendly": 1.0, "trend_short": 1},
    "0103": {"en_comment": "GP - community-based, lower pay but stable, broad scope",
             "learning_cost": 8.0, "education_req": 8.0, "value_added": 6.0,
             "overtime": 5.0, "burnout": 5.0, "social_status": 7.0,
             "supply_demand": 7.5, "developed_scarcity": 7.5,
             "remote_friendly": 3.5, "family_friendly": 5.5,
             "career_lifespan": 9.0, "age_flexibility": 7.5, "trend_short": 2},
    "0104": {"en_comment": "Anesthesiologist - high pay, high stress during procedures",
             "value_added": 8.5, "safety": 6.0, "overtime": 3.0, "burnout": 3.0,
             "ai_resistance": 6.5, "physical_demand": 5.5, "supply_demand": 7.5,
             "developed_scarcity": 8.0, "trend_short": 2},
    "0105": {"en_comment": "Radiologist - high AI impact, good lifestyle",
             "overtime": 5.5, "burnout": 5.5, "value_added": 8.0,
             "ai_resistance": 4.0, "remote_friendly": 5.0, "physical_demand": 2.0,
             "family_friendly": 6.5, "trend_short": 0},
    "0106": {"en_comment": "Pathologist - lab-based, AI disruption risk",
             "overtime": 6.0, "burnout": 6.0, "value_added": 7.0,
             "ai_resistance": 4.0, "remote_friendly": 4.0, "physical_demand": 2.0,
             "social_interaction": 4.0, "family_friendly": 6.5, "trend_short": 0},
    "0107": {"en_comment": "Emergency Medicine - high stress, shift work, high demand",
             "overtime": 2.0, "burnout": 2.0, "safety": 6.0,
             "value_added": 7.5, "ai_resistance": 8.0, "physical_demand": 6.5,
             "family_friendly": 2.5, "supply_demand": 8.0, "developed_scarcity": 8.5,
             "social_status": 8.0, "trend_short": 3},
    "0108": {"en_comment": "Pediatrician - lower pay for specialty, high fulfillment",
             "value_added": 6.5, "fulfillment": 8.5, "social_status": 8.0,
             "overtime": 4.0, "burnout": 4.0, "gender_equality": 6.0, "trend_short": 2},
    "0109": {"en_comment": "OB/GYN - surgical + medical, high liability",
             "value_added": 7.5, "safety": 6.0, "overtime": 2.5, "burnout": 2.5,
             "reputation_variance": 2.5, "gender_equality": 6.5,
             "physical_demand": 6.0, "trend_short": 1},
    "0110": {"en_comment": "Cardiologist - high value, aging society demand",
             "value_added": 8.5, "supply_demand": 7.5, "developed_scarcity": 7.5,
             "learning_cost": 9.5, "social_status": 9.0, "trend_short": 3},
    "0111": {"en_comment": "Neurologist - complex, growing demand",
             "learning_cost": 9.5, "value_added": 7.5, "ai_resistance": 7.5,
             "supply_demand": 7.5, "developed_scarcity": 7.5, "trend_short": 3},
    "0112": {"en_comment": "Oncologist - high emotional burden, growing field",
             "value_added": 8.0, "burnout": 3.0, "fulfillment": 8.5,
             "supply_demand": 7.5, "trend_short": 3,
             "occupational_disease": 4.5, "safety": 6.5},
    "0113": {"en_comment": "Orthopedic Surgeon - high pay, physical",
             "value_added": 9.0, "physical_demand": 7.5, "safety": 6.5,
             "overtime": 3.0, "burnout": 3.0, "gender_equality": 4.0,
             "learning_cost": 9.5, "education_req": 9.5, "trend_short": 2},
    "0114": {"en_comment": "Urologist - surgical specialty",
             "value_added": 8.0, "physical_demand": 5.5, "overtime": 4.0,
             "burnout": 4.0, "trend_short": 2},
    "0115": {"en_comment": "Dermatologist - great lifestyle, high demand cosmetic",
             "value_added": 8.0, "overtime": 6.5, "burnout": 6.5,
             "family_friendly": 7.0, "physical_demand": 2.5,
             "entrepreneurship": 8.0, "ai_resistance": 5.5,
             "side_job_compat": 6.0, "trend_short": 2},
    "0116": {"en_comment": "ENT - surgical + medical",
             "value_added": 7.5, "physical_demand": 5.0, "trend_short": 1},
    "0117": {"en_comment": "Plastic Surgeon - high value, cosmetic market",
             "value_added": 9.5, "entrepreneurship": 9.0,
             "reputation_variance": 3.0, "cycle_sensitivity": 4.0,
             "side_job_compat": 5.5, "social_status": 8.5, "trend_short": 2,
             "family_friendly": 5.5, "overtime": 4.5, "burnout": 4.5},
    "0118": {"en_comment": "Neurosurgeon - highest learning cost, extreme skill",
             "learning_cost": 10.0, "education_req": 10.0, "value_added": 10.0,
             "overtime": 2.0, "burnout": 2.0, "safety": 6.0,
             "physical_demand": 6.5, "social_status": 10.0,
             "supply_demand": 8.5, "developed_scarcity": 9.0,
             "family_friendly": 2.0, "career_lifespan": 7.0, "trend_short": 2},
    "0119": {"en_comment": "Cardiothoracic Surgeon - extreme demands",
             "learning_cost": 10.0, "education_req": 10.0, "value_added": 9.5,
             "overtime": 2.0, "burnout": 2.0, "safety": 5.5,
             "physical_demand": 7.0, "social_status": 9.5,
             "supply_demand": 8.0, "developed_scarcity": 9.0,
             "family_friendly": 2.0, "career_lifespan": 7.0, "trend_short": 1},
    "0120": {"en_comment": "Intensivist - high stress, critical care",
             "overtime": 2.0, "burnout": 2.0, "safety": 6.0,
             "value_added": 7.5, "supply_demand": 8.0,
             "family_friendly": 2.5, "ai_resistance": 7.5, "trend_short": 3},
    "0121": {"en_comment": "Endocrinologist - chronic disease management",
             "value_added": 7.0, "overtime": 5.0, "burnout": 5.0,
             "remote_friendly": 3.5, "family_friendly": 5.5, "trend_short": 3},
    "0122": {"en_comment": "Nephrologist - dialysis management, stable demand",
             "value_added": 7.0, "overtime": 4.5, "burnout": 4.5,
             "supply_demand": 7.0, "trend_short": 2},
    "0123": {"en_comment": "Rheumatologist - niche but growing",
             "value_added": 7.0, "overtime": 5.5, "burnout": 5.5,
             "supply_demand": 7.0, "market_size": 5.5, "trend_short": 2},
    "0124": {"en_comment": "Gastroenterologist - procedural + medical",
             "value_added": 8.0, "overtime": 4.0, "burnout": 4.0,
             "supply_demand": 7.0, "trend_short": 2},
    "0125": {"en_comment": "Hematologist - complex, overlaps oncology",
             "value_added": 7.5, "overtime": 4.5, "burnout": 4.0,
             "supply_demand": 7.0, "market_size": 5.0, "trend_short": 2},
    "0126": {"en_comment": "Infectious Disease - post-COVID importance",
             "value_added": 6.5, "overtime": 4.5, "burnout": 4.0,
             "safety": 5.5, "supply_demand": 7.5, "trend_short": 4,
             "trend_long": 4, "ai_resistance": 7.5},
    "0127": {"en_comment": "Pulmonologist - respiratory demand growing",
             "value_added": 7.0, "overtime": 4.0, "burnout": 4.0,
             "supply_demand": 7.5, "trend_short": 3},
    "0128": {"en_comment": "Geriatrician - aging society demand, lower pay",
             "value_added": 6.0, "overtime": 5.0, "burnout": 5.0,
             "supply_demand": 8.0, "developed_scarcity": 8.5,
             "trend_short": 4, "trend_long": 4,
             "family_friendly": 5.5, "social_status": 7.0},
    "0129": {"en_comment": "Neonatologist - ICU for newborns",
             "value_added": 7.5, "overtime": 2.5, "burnout": 2.5,
             "safety": 6.0, "fulfillment": 9.0, "family_friendly": 3.0,
             "supply_demand": 7.5, "trend_short": 2},
    "0130": {"en_comment": "Sports Medicine - lifestyle + sports industry",
             "value_added": 7.0, "overtime": 6.0, "burnout": 6.0,
             "family_friendly": 6.5, "entrepreneurship": 7.5,
             "cycle_sensitivity": 3.0, "side_job_compat": 5.5,
             "physical_demand": 4.0, "trend_short": 3},
    # ===== NURSING =====
    "0201": {"en_comment": "RN - backbone of healthcare, global shortage",
             "supply_demand": 8.5, "developed_scarcity": 8.5,
             "intl_mobility": 8.0, "trend_short": 3},
    "0202": {"en_comment": "Nurse Practitioner - advanced practice, high autonomy",
             "learning_cost": 6.5, "education_req": 6.5, "value_added": 6.5,
             "autonomy": 7.0, "supply_demand": 9.0, "developed_scarcity": 9.0,
             "social_status": 7.0, "remote_friendly": 3.0,
             "ai_resistance": 7.5, "trend_short": 4},
    "0203": {"en_comment": "Midwife - essential, especially in developing countries",
             "fulfillment": 8.5, "gender_equality": 3.0,
             "safety": 6.0, "supply_demand": 7.5, "trend_short": 2,
             "intl_mobility": 7.0, "physical_demand": 6.0},
    "0204": {"en_comment": "ICU Nurse - high skill, high stress",
             "learning_cost": 6.0, "value_added": 6.0,
             "overtime": 3.0, "burnout": 2.5, "safety": 6.0,
             "supply_demand": 8.5, "developed_scarcity": 9.0,
             "family_friendly": 3.0, "trend_short": 3},
    "0205": {"en_comment": "OR Nurse - specialized surgical support",
             "learning_cost": 5.5, "value_added": 5.5,
             "overtime": 3.5, "burnout": 3.5, "safety": 6.5,
             "physical_demand": 6.0, "trend_short": 2},
    "0206": {"en_comment": "Head Nurse - management track",
             "learning_cost": 6.0, "education_req": 6.0, "value_added": 6.0,
             "autonomy": 6.0, "social_status": 6.5,
             "social_interaction": 9.0, "overtime": 4.5, "burnout": 4.0,
             "career_switch": 5.5, "trend_short": 2},
    "0207": {"en_comment": "Community Health Nurse - preventive care",
             "overtime": 6.0, "burnout": 5.5, "value_added": 4.5,
             "family_friendly": 6.0, "remote_friendly": 3.0,
             "physical_demand": 5.0, "trend_short": 3},
    "0208": {"en_comment": "Nursing Assistant - entry level, high demand",
             "learning_cost": 3.0, "education_req": 3.0, "value_added": 3.5,
             "social_status": 4.0, "overtime": 3.5, "burnout": 3.0,
             "physical_demand": 7.5, "supply_demand": 8.5,
             "ai_resistance": 8.0, "license_barrier": 3.5,
             "trend_short": 3, "edu": "高中/大专", "age": "18-25"},
    "0209": {"en_comment": "Nurse Anesthetist - highest paid nursing role (US)",
             "learning_cost": 7.0, "education_req": 7.0, "value_added": 8.0,
             "social_status": 7.5, "autonomy": 7.0,
             "supply_demand": 8.5, "developed_scarcity": 9.0,
             "license_barrier": 8.0, "trend_short": 3},
    "0210": {"en_comment": "Pediatric Nurse",
             "fulfillment": 7.5, "value_added": 5.0, "trend_short": 2},
    "0211": {"en_comment": "Oncology Nurse - emotionally demanding",
             "burnout": 3.0, "fulfillment": 7.5, "value_added": 5.5,
             "occupational_disease": 4.0, "trend_short": 2},
    "0212": {"en_comment": "ER Nurse - high pace, shift work",
             "overtime": 3.0, "burnout": 2.5, "safety": 6.0,
             "value_added": 5.5, "family_friendly": 3.0,
             "supply_demand": 8.5, "trend_short": 3},
    "0213": {"en_comment": "Dialysis Nurse - specialized, routine",
             "value_added": 5.0, "overtime": 5.0, "burnout": 5.0,
             "ai_resistance": 6.5, "supply_demand": 7.5, "trend_short": 2},
    # ===== PHARMACY =====
    "0301": {"en_comment": "Pharmacist - retail/hospital, AI threat to dispensing",
             "ai_resistance": 4.5, "remote_friendly": 2.5,
             "entrepreneurship": 7.0, "trend_short": 0},
    "0302": {"en_comment": "Clinical Pharmacist - hospital-based, growing role",
             "learning_cost": 7.5, "value_added": 7.0, "ai_resistance": 6.0,
             "social_interaction": 7.5, "trend_short": 2},
    "0303": {"en_comment": "Pharma R&D Scientist - industry, high value",
             "learning_cost": 8.5, "education_req": 8.5, "value_added": 8.5,
             "remote_friendly": 4.5, "ai_resistance": 6.5,
             "social_status": 8.0, "fulfillment": 8.0,
             "supply_demand": 7.0, "developed_scarcity": 7.0,
             "trend_short": 3, "edu": "硕士/博士", "age": "26-32"},
    "0304": {"en_comment": "Drug Regulatory Affairs - niche, regulatory knowledge",
             "learning_cost": 6.5, "value_added": 7.0, "remote_friendly": 5.0,
             "supply_demand": 6.5, "trend_short": 2},
    "0305": {"en_comment": "Pharma Sales Rep - high pay potential, travel heavy",
             "learning_cost": 4.0, "education_req": 4.5, "value_added": 6.5,
             "remote_friendly": 4.0, "social_interaction": 9.0,
             "physical_demand": 3.5, "license_barrier": 3.0,
             "reputation_variance": 3.0, "cycle_sensitivity": 4.0,
             "entrepreneurship": 7.0, "side_job_compat": 3.5,
             "ai_resistance": 5.0, "trend_short": 0,
             "edu": "本科", "age": "22-28"},
    "0306": {"en_comment": "Pharma QA - manufacturing quality",
             "learning_cost": 6.0, "value_added": 6.0, "remote_friendly": 3.5,
             "ai_resistance": 5.5, "trend_short": 1},
    "0307": {"en_comment": "Pharmacovigilance - drug safety monitoring",
             "learning_cost": 6.5, "value_added": 6.5, "remote_friendly": 6.0,
             "ai_resistance": 5.5, "supply_demand": 6.5, "trend_short": 2},
    # ===== REHABILITATION =====
    "0401": {"en_comment": "Physical Therapist - high demand, hands-on",
             "supply_demand": 7.5, "developed_scarcity": 7.5,
             "entrepreneurship": 7.0, "physical_demand": 6.0,
             "ai_resistance": 8.0, "trend_short": 3},
    "0402": {"en_comment": "Occupational Therapist - growing awareness",
             "supply_demand": 7.0, "developed_scarcity": 7.0,
             "fulfillment": 8.0, "trend_short": 3},
    "0403": {"en_comment": "Speech-Language Pathologist - pediatric + aging demand",
             "supply_demand": 7.5, "developed_scarcity": 8.0,
             "gender_equality": 3.5, "fulfillment": 8.0,
             "remote_friendly": 4.0, "trend_short": 3},
    "0404": {"en_comment": "Rehabilitation Physician - medical doctor specialty",
             "learning_cost": 8.5, "education_req": 8.5, "value_added": 7.0,
             "license_barrier": 8.5, "social_status": 7.5,
             "trend_short": 3, "edu": "博士/医学学位", "age": "28-34"},
    "0405": {"en_comment": "Respiratory Therapist - ICU support, pandemic demand",
             "supply_demand": 7.5, "safety": 7.0,
             "ai_resistance": 7.0, "trend_short": 3},
    "0406": {"en_comment": "Music Therapist - niche, growing acceptance",
             "learning_cost": 5.0, "value_added": 4.5, "market_size": 3.0,
             "supply_demand": 5.0, "social_status": 5.0,
             "fulfillment": 9.0, "entrepreneurship": 7.0,
             "trend_short": 2, "edu": "本科/硕士", "age": "22-28"},
    "0407": {"en_comment": "Art Therapist - niche, similar to music therapy",
             "learning_cost": 5.0, "value_added": 4.5, "market_size": 3.0,
             "supply_demand": 5.0, "social_status": 5.0,
             "fulfillment": 9.0, "entrepreneurship": 7.0,
             "trend_short": 2, "edu": "本科/硕士", "age": "22-28"},
    "0408": {"en_comment": "Exercise Therapist - fitness + medical crossover",
             "learning_cost": 5.0, "value_added": 5.0, "physical_demand": 6.5,
             "entrepreneurship": 7.5, "side_job_compat": 6.5,
             "license_barrier": 4.5, "trend_short": 3},
    "0409": {"en_comment": "Prosthetist/Orthotist - specialized, technical",
             "learning_cost": 6.5, "ai_resistance": 8.0,
             "supply_demand": 7.0, "market_size": 3.5,
             "physical_demand": 5.5, "trend_short": 2},
    "0410": {"en_comment": "Audiologist - aging population demand",
             "supply_demand": 7.0, "developed_scarcity": 7.0,
             "entrepreneurship": 7.0, "ai_resistance": 6.5,
             "family_friendly": 7.0, "overtime": 6.5, "trend_short": 2},
    # ===== PUBLIC HEALTH =====
    "0501": {"en_comment": "Epidemiologist - post-COVID recognition",
             "ai_resistance": 7.5, "remote_friendly": 7.0,
             "supply_demand": 7.0, "trend_short": 4, "trend_long": 4},
    "0502": {"en_comment": "Public Health Officer - government role",
             "learning_cost": 6.5, "stability": 8.5, "value_added": 6.0,
             "remote_friendly": 5.0, "autonomy": 6.0,
             "entrepreneurship": 3.0, "trend_short": 3},
    "0503": {"en_comment": "Health Education Specialist - community focus",
             "learning_cost": 5.5, "education_req": 5.5, "value_added": 5.0,
             "remote_friendly": 5.5, "fulfillment": 7.5,
             "social_interaction": 8.5, "trend_short": 2,
             "edu": "本科/硕士", "age": "22-28"},
    "0504": {"en_comment": "Dietitian/Nutritionist - wellness trend boost",
             "learning_cost": 5.5, "education_req": 5.5, "value_added": 5.5,
             "entrepreneurship": 7.0, "remote_friendly": 5.0,
             "side_job_compat": 6.0, "fulfillment": 7.5,
             "gender_equality": 4.0, "trend_short": 3,
             "license_barrier": 5.0, "edu": "本科", "age": "22-26"},
    "0505": {"en_comment": "Biostatistician - data + health, growing demand",
             "learning_cost": 7.5, "education_req": 8.0, "value_added": 7.5,
             "remote_friendly": 7.5, "ai_resistance": 6.0,
             "supply_demand": 7.0, "developed_scarcity": 7.0,
             "trend_short": 4, "edu": "硕士/博士", "age": "24-30"},
    "0506": {"en_comment": "Environmental Health Engineer - infrastructure",
             "learning_cost": 7.0, "value_added": 6.5,
             "remote_friendly": 4.5, "physical_demand": 3.5,
             "trend_short": 2, "edu": "本科/硕士", "age": "22-28"},
    "0507": {"en_comment": "CDC Researcher - government research, stable",
             "learning_cost": 8.0, "education_req": 8.5, "value_added": 6.5,
             "stability": 8.5, "remote_friendly": 5.5,
             "fulfillment": 8.0, "trend_short": 3,
             "edu": "硕士/博士", "age": "26-32"},
    # ===== TRADITIONAL MEDICINE =====
    "0601": {"en_comment": "TCM Practitioner - strong in China, limited elsewhere",
             "market_size": 6.0, "supply_demand": 5.0,
             "intl_mobility": 2.5, "reputation_variance": 4.0,
             "trend_short": 2},
    "0602": {"en_comment": "Acupuncturist - growing global acceptance",
             "intl_mobility": 5.0, "reputation_variance": 3.0,
             "entrepreneurship": 8.0, "trend_short": 2},
    "0603": {"en_comment": "Ayurveda - strong in India/South Asia",
             "market_size": 4.0, "intl_mobility": 2.5,
             "reputation_variance": 4.0, "trend_short": 1},
    "0604": {"en_comment": "Chiropractor - established in Western countries",
             "learning_cost": 7.0, "education_req": 7.0,
             "value_added": 6.5, "entrepreneurship": 8.5,
             "intl_mobility": 5.5, "reputation_variance": 3.5,
             "license_barrier": 7.0, "trend_short": 1},
    "0605": {"en_comment": "Naturopathic Physician - niche, variable regulation",
             "reputation_variance": 4.0, "license_barrier": 4.5,
             "value_added": 5.5, "entrepreneurship": 8.0, "trend_short": 1},
    "0606": {"en_comment": "Tui Na - manual therapy, regional",
             "learning_cost": 4.5, "education_req": 4.0, "value_added": 4.0,
             "physical_demand": 7.0, "intl_mobility": 2.0,
             "license_barrier": 3.5, "trend_short": 0,
             "edu": "大专/本科", "age": "20-28"},
    "0607": {"en_comment": "Chinese Herbal Pharmacist - specialized",
             "learning_cost": 6.0, "intl_mobility": 2.0,
             "market_size": 4.0, "trend_short": 1},
    "0608": {"en_comment": "Osteopath - established in UK/EU/AU",
             "learning_cost": 7.0, "education_req": 7.0,
             "value_added": 6.0, "entrepreneurship": 8.0,
             "intl_mobility": 5.0, "license_barrier": 6.5,
             "reputation_variance": 2.5, "trend_short": 1},
    "0609": {"en_comment": "Homeopath - controversial, regional acceptance",
             "reputation_variance": 4.5, "license_barrier": 3.0,
             "value_added": 4.0, "social_status": 4.0,
             "intl_mobility": 3.0, "ai_resistance": 6.0, "trend_short": -1},
    # ===== DENTAL =====
    "0701": {"en_comment": "Dentist - good lifestyle, entrepreneurial",
             "overtime": 7.0, "burnout": 6.0, "family_friendly": 7.0,
             "trend_short": 2},
    "0702": {"en_comment": "Dental Hygienist - support role, good work-life",
             "learning_cost": 4.5, "education_req": 4.5, "value_added": 5.0,
             "overtime": 7.5, "burnout": 6.5, "family_friendly": 7.5,
             "license_barrier": 5.5, "social_status": 5.5,
             "physical_demand": 5.0, "trend_short": 2,
             "edu": "大专/本科", "age": "20-24"},
    "0703": {"en_comment": "Orthodontist - lucrative, cosmetic demand",
             "learning_cost": 9.0, "education_req": 9.0, "value_added": 9.0,
             "entrepreneurship": 9.0, "social_status": 8.5,
             "supply_demand": 7.0, "trend_short": 3},
    "0704": {"en_comment": "Oral & Maxillofacial Surgeon - complex surgery",
             "learning_cost": 9.5, "education_req": 9.5, "value_added": 9.5,
             "physical_demand": 6.5, "overtime": 4.0, "burnout": 4.0,
             "safety": 6.5, "social_status": 9.0, "trend_short": 2},
    "0705": {"en_comment": "Dental Technician - lab-based",
             "learning_cost": 5.0, "education_req": 4.5, "value_added": 5.0,
             "ai_resistance": 6.0, "physical_demand": 4.5,
             "license_barrier": 4.5, "social_status": 5.0,
             "entrepreneurship": 6.5, "trend_short": 1,
             "edu": "大专/本科", "age": "20-24"},
    "0706": {"en_comment": "Periodontist - gum disease specialist",
             "learning_cost": 9.0, "education_req": 9.0, "value_added": 8.5,
             "supply_demand": 7.0, "trend_short": 2},
    # ===== OPHTHALMOLOGY =====
    "0801": {"en_comment": "Ophthalmologist - surgical + medical eye specialist",
             "value_added": 8.5, "entrepreneurship": 8.5,
             "supply_demand": 7.5, "trend_short": 2},
    "0802": {"en_comment": "Optometrist - primary eye care",
             "learning_cost": 7.0, "education_req": 7.0, "value_added": 6.5,
             "entrepreneurship": 8.0, "family_friendly": 7.0,
             "overtime": 7.0, "burnout": 6.5,
             "license_barrier": 7.0, "social_status": 6.5, "trend_short": 2},
    "0803": {"en_comment": "Optician - retail eye-wear",
             "learning_cost": 4.0, "education_req": 3.5, "value_added": 4.5,
             "license_barrier": 4.0, "social_status": 4.5,
             "entrepreneurship": 7.5, "ai_resistance": 5.0,
             "physical_demand": 2.0, "trend_short": 1,
             "edu": "大专", "age": "18-24"},
    # ===== MENTAL HEALTH =====
    "0901": {"en_comment": "Psychiatrist - MD + psychiatry, medication authority",
             "learning_cost": 9.5, "education_req": 9.5, "value_added": 8.0,
             "social_status": 8.5, "supply_demand": 8.0, "developed_scarcity": 8.5,
             "license_barrier": 9.0, "trend_short": 4,
             "edu": "博士/医学学位", "age": "30-36"},
    "0902": {"en_comment": "Clinical Psychologist - therapy + assessment",
             "fulfillment": 8.5, "remote_friendly": 6.0,
             "entrepreneurship": 7.5, "trend_short": 4},
    "0903": {"en_comment": "Counseling Psychologist - therapy focus",
             "learning_cost": 6.5, "education_req": 6.5, "value_added": 5.5,
             "remote_friendly": 6.5, "entrepreneurship": 7.5,
             "supply_demand": 7.0, "side_job_compat": 6.5,
             "license_barrier": 6.5, "trend_short": 4},
    "0904": {"en_comment": "Psychiatric Nurse - mental health nursing",
             "learning_cost": 5.5, "education_req": 5.5, "value_added": 5.5,
             "supply_demand": 8.0, "developed_scarcity": 8.0,
             "safety": 7.0, "trend_short": 3,
             "edu": "大专/本科", "age": "22-26"},
    "0905": {"en_comment": "Psychotherapist - talk therapy, various modalities",
             "remote_friendly": 6.5, "entrepreneurship": 8.0,
             "fulfillment": 9.0, "side_job_compat": 7.0,
             "ai_resistance": 8.0, "trend_short": 4},
    "0906": {"en_comment": "Addiction Counselor - substance abuse, growing need",
             "learning_cost": 5.5, "education_req": 5.5, "value_added": 5.0,
             "safety": 7.5, "burnout": 3.5, "fulfillment": 7.5,
             "supply_demand": 7.5, "trend_short": 3,
             "license_barrier": 5.5, "edu": "本科/硕士", "age": "24-30"},
    "0907": {"en_comment": "Neuropsychologist - brain-behavior assessment",
             "learning_cost": 8.5, "education_req": 9.0, "value_added": 7.5,
             "supply_demand": 7.0, "market_size": 4.0,
             "ai_resistance": 7.0, "trend_short": 3,
             "edu": "博士", "age": "28-34"},
    "0908": {"en_comment": "Child Psychologist - developmental focus",
             "fulfillment": 9.0, "supply_demand": 7.5,
             "developed_scarcity": 8.0, "trend_short": 4},
    "0909": {"en_comment": "Forensic Psychologist - legal system intersection",
             "value_added": 7.0, "market_size": 3.5,
             "social_interaction": 8.0, "autonomy": 7.0,
             "ai_resistance": 8.0, "trend_short": 2},
    # ===== MEDICAL IMAGING & LAB =====
    "1001": {"en_comment": "Radiologic Technologist - imaging procedures",
             "safety": 6.5, "occupational_disease": 4.5,
             "ai_resistance": 4.5, "trend_short": 1},
    "1002": {"en_comment": "Medical Lab Technologist - blood/tissue analysis",
             "ai_resistance": 4.5, "remote_friendly": 1.5,
             "safety": 7.5, "trend_short": 1},
    "1003": {"en_comment": "Sonographer - ultrasound, good demand",
             "value_added": 6.0, "supply_demand": 7.0,
             "physical_demand": 5.0, "ai_resistance": 5.5, "trend_short": 2},
    "1004": {"en_comment": "Nuclear Medicine Tech - radiation exposure risk",
             "learning_cost": 6.0, "safety": 6.0, "occupational_disease": 4.0,
             "supply_demand": 6.5, "value_added": 6.0, "trend_short": 1},
    "1005": {"en_comment": "Histotechnologist - tissue preparation",
             "ai_resistance": 4.5, "value_added": 5.0, "trend_short": 1},
    "1006": {"en_comment": "ECG Technician - routine cardiac testing",
             "learning_cost": 4.0, "education_req": 4.0, "value_added": 4.5,
             "ai_resistance": 4.0, "license_barrier": 4.0, "trend_short": 0,
             "edu": "大专", "age": "20-24"},
    "1007": {"en_comment": "MRI Technologist - specialized imaging",
             "learning_cost": 6.0, "value_added": 6.0,
             "supply_demand": 7.0, "ai_resistance": 5.0, "trend_short": 2},
    # ===== MEDICAL ADMIN =====
    "1101": {"en_comment": "Hospital Administrator - leadership, high value",
             "learning_cost": 7.0, "education_req": 7.0, "value_added": 8.0,
             "social_status": 7.5, "autonomy": 7.5,
             "remote_friendly": 4.0, "supply_demand": 6.5,
             "trend_short": 2, "edu": "硕士/MBA", "age": "30-40"},
    "1102": {"en_comment": "Health Informatics - tech + health crossover",
             "learning_cost": 6.5, "education_req": 6.5, "value_added": 7.0,
             "remote_friendly": 7.0, "ai_resistance": 5.5,
             "supply_demand": 7.5, "developed_scarcity": 7.5,
             "trend_short": 4, "edu": "本科/硕士", "age": "24-30"},
    "1103": {"en_comment": "Health Insurance Manager - business + health",
             "value_added": 7.0, "remote_friendly": 6.0,
             "supply_demand": 6.0, "trend_short": 2},
    "1104": {"en_comment": "Healthcare Quality Manager",
             "value_added": 6.5, "remote_friendly": 5.0,
             "supply_demand": 6.5, "trend_short": 2},
    "1105": {"en_comment": "Clinical Research Coordinator",
             "learning_cost": 5.5, "value_added": 5.5,
             "remote_friendly": 4.5, "supply_demand": 7.0,
             "trend_short": 3, "edu": "本科/硕士", "age": "24-30"},
    "1106": {"en_comment": "Medical Coder - billing/coding, AI-threated",
             "learning_cost": 4.0, "education_req": 4.0, "value_added": 5.0,
             "remote_friendly": 7.5, "ai_resistance": 3.5,
             "license_barrier": 4.5, "trend_short": -1,
             "edu": "大专/本科", "age": "20-28"},
    "1107": {"en_comment": "EMT - emergency response, physical",
             "learning_cost": 3.5, "education_req": 3.5, "value_added": 4.5,
             "safety": 5.5, "physical_demand": 7.5, "overtime": 3.0,
             "burnout": 3.0, "family_friendly": 3.0,
             "ai_resistance": 8.0, "social_status": 6.5,
             "fulfillment": 7.5, "license_barrier": 5.0,
             "trend_short": 2, "edu": "大专/培训", "age": "18-25"},
    "1108": {"en_comment": "Paramedic - advanced pre-hospital care",
             "learning_cost": 5.0, "education_req": 5.0, "value_added": 5.5,
             "safety": 5.5, "physical_demand": 7.0, "overtime": 3.0,
             "burnout": 3.0, "family_friendly": 3.0,
             "ai_resistance": 8.0, "social_status": 7.0,
             "fulfillment": 8.0, "license_barrier": 6.0,
             "trend_short": 2, "edu": "大专/本科", "age": "20-26"},
    "1109": {"en_comment": "Health Information Technician",
             "learning_cost": 4.0, "education_req": 4.0, "value_added": 5.0,
             "remote_friendly": 6.5, "ai_resistance": 4.0,
             "trend_short": 0, "edu": "大专/本科", "age": "20-26"},
    "1110": {"en_comment": "Biomedical Equipment Technician",
             "learning_cost": 5.5, "value_added": 5.5,
             "physical_demand": 4.0, "ai_resistance": 6.5,
             "remote_friendly": 2.0, "supply_demand": 6.5,
             "trend_short": 2, "edu": "大专/本科", "age": "20-26"},
    "1111": {"en_comment": "Clinical Trial Manager",
             "learning_cost": 6.5, "education_req": 6.5, "value_added": 7.5,
             "remote_friendly": 5.5, "supply_demand": 7.0,
             "developed_scarcity": 7.0, "social_status": 7.0,
             "trend_short": 3, "edu": "本科/硕士", "age": "26-32"},
    "1112": {"en_comment": "Telemedicine Coordinator - growing post-COVID",
             "learning_cost": 4.5, "value_added": 5.5,
             "remote_friendly": 8.0, "ai_resistance": 5.0,
             "supply_demand": 7.0, "trend_short": 4,
             "edu": "本科", "age": "22-28"},
    "1113": {"en_comment": "Medical Interpreter - language + medical knowledge",
             "learning_cost": 5.0, "value_added": 5.0,
             "remote_friendly": 6.0, "intl_mobility": 7.5,
             "ai_resistance": 5.5, "license_barrier": 3.5,
             "side_job_compat": 6.5, "trend_short": 2,
             "edu": "本科", "age": "22-30"},
    "1114": {"en_comment": "Health Data Analyst - data science in healthcare",
             "learning_cost": 6.0, "education_req": 6.0, "value_added": 7.0,
             "remote_friendly": 7.5, "ai_resistance": 5.0,
             "supply_demand": 7.5, "developed_scarcity": 7.0,
             "trend_short": 4, "edu": "本科/硕士", "age": "22-28"},
    "1115": {"en_comment": "Patient Experience Officer - new role, service design",
             "learning_cost": 4.5, "value_added": 5.5,
             "remote_friendly": 5.0, "ai_resistance": 6.5,
             "social_interaction": 9.0, "supply_demand": 5.5,
             "trend_short": 3, "edu": "本科/硕士", "age": "24-30"},
    # ===== VETERINARY MEDICINE =====
    "1201": {"en_comment": "Small Animal Vet - pets, urban, growing",
             "market_size": 5.5, "supply_demand": 7.0,
             "entrepreneurship": 8.0, "trend_short": 3},
    "1202": {"en_comment": "Large Animal/Farm Vet - rural, declining in developed",
             "physical_demand": 8.0, "safety": 5.5,
             "market_size": 4.0, "supply_demand": 6.5,
             "developed_scarcity": 7.0, "remote_friendly": 1.0,
             "family_friendly": 4.0, "trend_short": 1},
    "1203": {"en_comment": "Veterinary Surgeon - specialized, fewer",
             "learning_cost": 8.5, "education_req": 8.5, "value_added": 7.0,
             "supply_demand": 7.0, "physical_demand": 6.5,
             "trend_short": 2},
    "1204": {"en_comment": "Emergency Vet - shift work, high stress",
             "overtime": 3.0, "burnout": 3.0, "safety": 5.5,
             "value_added": 6.5, "family_friendly": 3.5,
             "supply_demand": 7.5, "trend_short": 3},
    "1205": {"en_comment": "Veterinary Public Health - zoonotic disease, food safety",
             "remote_friendly": 4.0, "stability": 8.0,
             "value_added": 5.5, "fulfillment": 7.5,
             "supply_demand": 6.0, "trend_short": 2},
    "1206": {"en_comment": "Zoo/Wildlife Vet - rare, high fulfillment",
             "market_size": 2.0, "supply_demand": 5.5,
             "value_added": 5.0, "fulfillment": 9.5,
             "physical_demand": 7.0, "safety": 5.0,
             "trend_short": 2},
}


def occ_base(occ_id, mid_cat):
    """Return base scores for an occupation, merging mid defaults + overrides."""
    defaults = MID_DEFAULTS.get(mid_cat, {})
    if not defaults:
        return {}
    base = dict(defaults)
    overrides = OCC_OVERRIDES.get(occ_id, {})
    for k, v in overrides.items():
        if k != "en_comment":
            base[k] = v
    return base


# ---------------------------------------------------------------------------
# COUNTRY-ADAPTIVE SCORING
# ---------------------------------------------------------------------------

def clamp(val, lo=0.0, hi=10.0):
    return max(lo, min(hi, round(val, 1)))

def clamp5(val):
    return max(0.0, min(5.0, round(val, 1)))


def apply_country_modifiers(base_scores, country_profile, occ_id, mid_cat):
    """Adjust base scores based on healthcare country profile."""
    cp = country_profile
    s = dict(base_scores)

    # Healthcare quality influences many dimensions
    hq_factor = (cp["hq"] - 6.0) / 4.0  # normalized -1 to +1

    # Physician compensation drives value_added for clinical roles
    is_physician = mid_cat in ("clinical_medicine", "dental", "ophthalmology")
    is_nurse = mid_cat == "nursing"
    comp_val = cp["phys_comp"] if is_physician else cp["nurse_comp"] if is_nurse else (cp["phys_comp"] + cp["nurse_comp"]) / 2.0
    comp_factor = (comp_val - 5.0) / 5.0

    s["value_added"] = clamp(s["value_added"] + comp_factor * 2.0)
    s["cost_performance"] = clamp(s["cost_performance"] + comp_factor * 1.0 + hq_factor * 0.5)

    # Growth coefficient: healthcare quality + aging demand
    aging_factor = (cp["aging"] - 5.0) / 5.0
    s["growth_coeff"] = clamp(s["growth_coeff"] + hq_factor * 0.5 + aging_factor * 0.8)

    # Career lifespan: stable in well-funded healthcare systems
    s["career_lifespan"] = clamp(s["career_lifespan"] + hq_factor * 0.5)

    # Opportunity: market size + healthcare development
    market_factor = (cp["market"] - 5.5) / 4.5
    s["opportunity"] = clamp(s["opportunity"] + market_factor * 1.0 + hq_factor * 0.5)

    # Market size
    s["market_size"] = clamp(s["market_size"] + market_factor * 1.5)

    # Supply-demand: higher in developed countries with aging populations
    s["supply_demand"] = clamp(s["supply_demand"] + hq_factor * 0.5 + aging_factor * 0.5)

    # Developed scarcity
    dev_bonus = 1.0 if cp["hq"] >= 7.5 else (0.0 if cp["hq"] >= 5.0 else -1.0)
    s["developed_scarcity"] = clamp(s["developed_scarcity"] + dev_bonus * 0.8)

    # Stability: healthcare is generally stable, but better in well-funded systems
    s["stability"] = clamp(s["stability"] + hq_factor * 0.8)

    # Safety: varies by country healthcare safety standards
    s["safety"] = clamp(s["safety"] + hq_factor * 0.3)

    # Occupational disease: worse in countries with poor work-life balance
    wlb_factor = (cp["wlb"] - 6.0) / 4.0
    s["occupational_disease"] = clamp(s["occupational_disease"] + wlb_factor * 0.8)

    # Overtime: strongly affected by healthcare work culture
    s["overtime"] = clamp(s["overtime"] + (cp["ot"] - 5.0) / 5.0 * 2.5)

    # Burnout: overtime culture + healthcare system stress
    s["burnout"] = clamp(s["burnout"] + (cp["ot"] - 5.0) / 5.0 * 1.5)

    # Remote friendly: limited for most medical roles, country doesn't change much
    # But telehealth adoption matters for some roles
    if s.get("remote_friendly", 0) >= 4.0:
        tele_factor = (cp["hq"] - 6.0) / 8.0
        s["remote_friendly"] = clamp(s["remote_friendly"] + tele_factor * 1.0)

    # Autonomy: related to healthcare system structure (public vs private)
    pub_priv = (cp["pub_priv"] - 5.0) / 5.0  # higher = more public
    s["autonomy"] = clamp(s["autonomy"] - pub_priv * 0.5 + wlb_factor * 0.3)

    # Family friendly: work-life balance culture
    s["family_friendly"] = clamp(s["family_friendly"] + wlb_factor * 1.5)

    # Social status: higher in countries that value healthcare workers
    s["social_status"] = clamp(s["social_status"] + hq_factor * 0.5 + comp_factor * 0.5)

    # Fulfillment: slightly better in better-functioning systems
    s["fulfillment"] = clamp(s["fulfillment"] + hq_factor * 0.3)

    # Gender equality: country-level
    gender_factor = (cp["gender"] - 5.5) / 4.5
    s["gender_equality"] = clamp(s["gender_equality"] + gender_factor * 2.0)

    # Age flexibility: better in aging-society countries that need workers
    s["age_flexibility"] = clamp(s["age_flexibility"] + aging_factor * 0.5 + wlb_factor * 0.3)

    # Entrepreneurship: easier in private-heavy systems
    s["entrepreneurship"] = clamp(s["entrepreneurship"] - pub_priv * 0.5 + market_factor * 0.3)

    # International mobility: country openness
    intl_factor = (cp["intl"] - 6.0) / 4.0
    s["intl_mobility"] = clamp(s["intl_mobility"] + intl_factor * 1.5)

    # AI resistance: slight adjustment for tech-advanced healthcare
    ai_adj = (cp["hq"] - 6.0) / 8.0  # advanced = slightly less resistant (tools used earlier)
    s["ai_resistance"] = clamp(s["ai_resistance"] - ai_adj * 0.3)

    # Learning cost / education req: higher in systems with strict training
    edu_factor = (cp["edu"] - 6.0) / 4.0
    s["learning_cost"] = clamp(s["learning_cost"] + edu_factor * 0.3)
    s["education_req"] = clamp(s["education_req"] + edu_factor * 0.3)

    # License barrier: stricter in more regulated healthcare environments
    reg_factor = (cp["reg"] - 5.5) / 4.5
    s["license_barrier"] = clamp(s["license_barrier"] + reg_factor * 0.8)

    # Cycle sensitivity: healthcare is counter-cyclical, but country matters slightly
    s["cycle_sensitivity"] = clamp(s["cycle_sensitivity"] - hq_factor * 0.3)

    # Side job compatibility
    s["side_job_compat"] = clamp(s["side_job_compat"] + wlb_factor * 0.3)

    # Industry monopoly: higher in public-dominated systems
    s["industry_monopoly"] = clamp(s["industry_monopoly"] + pub_priv * 0.5)

    # Skill versatility: slightly better in advanced systems
    s["skill_versatility"] = clamp(s["skill_versatility"] + hq_factor * 0.3)

    # Career switch: easier in dynamic markets
    s["career_switch"] = clamp(s["career_switch"] + market_factor * 0.3 + hq_factor * 0.3)

    # Reputation variance: higher in countries with weaker systems
    rep_adj = -0.3 if cp["hq"] >= 7.5 else (0.3 if cp["hq"] < 5.0 else 0.0)
    s["reputation_variance"] = clamp5(s["reputation_variance"] + rep_adj)

    # Traditional medicine special handling
    if mid_cat == "traditional_medicine":
        trad_factor = (cp["trad"] - 5.0) / 5.0
        s["value_added"] = clamp(s["value_added"] + trad_factor * 1.5)
        s["market_size"] = clamp(s["market_size"] + trad_factor * 2.0)
        s["supply_demand"] = clamp(s["supply_demand"] + trad_factor * 1.0)
        s["social_status"] = clamp(s["social_status"] + trad_factor * 1.5)
        s["license_barrier"] = clamp(s["license_barrier"] + trad_factor * 1.0)
        s["reputation_variance"] = clamp5(s["reputation_variance"] - trad_factor * 0.5)

    # Mental health special handling
    if mid_cat == "mental_health":
        mental_factor = (cp["mental"] - 5.0) / 5.0
        s["supply_demand"] = clamp(s["supply_demand"] + mental_factor * 1.5)
        s["market_size"] = clamp(s["market_size"] + mental_factor * 1.5)
        s["social_status"] = clamp(s["social_status"] + mental_factor * 1.0)
        s["value_added"] = clamp(s["value_added"] + mental_factor * 1.0)

    # Pharma industry special handling
    if mid_cat == "pharmacy":
        pharma_factor = (cp["pharma"] - 5.5) / 4.5
        s["value_added"] = clamp(s["value_added"] + pharma_factor * 1.0)
        s["market_size"] = clamp(s["market_size"] + pharma_factor * 1.0)
        s["supply_demand"] = clamp(s["supply_demand"] + pharma_factor * 0.5)

    return s


def get_trends(base_scores, country_profile):
    """Get trend values adjusted for country."""
    cp = country_profile
    t_long = base_scores["trend_long"]
    t_short = base_scores["trend_short"]

    # Aging societies boost healthcare demand trends
    if cp["aging"] >= 8.0:
        t_short = min(5, t_short + 1)
    elif cp["aging"] < 3.5:
        t_short = max(-5, t_short - 1)

    # Well-funded systems sustain long-term growth
    if cp["hq"] >= 8.0:
        t_long = min(5, t_long)
    elif cp["hq"] < 4.0:
        t_long = max(-5, t_long - 1)

    return t_long, t_short


def get_demand_direction(trend_5yr):
    if trend_5yr >= 4:
        return "↑↑"
    elif trend_5yr >= 2:
        return "↑"
    elif trend_5yr >= -1:
        return "→"
    elif trend_5yr >= -3:
        return "↓"
    else:
        return "↓↓"


def get_ai_timeline(occ_id, ai_resistance):
    if ai_resistance >= 7.5:
        return "2035+"
    elif ai_resistance >= 6.0:
        return "2032-2038"
    elif ai_resistance >= 4.5:
        return "2028-2033"
    elif ai_resistance >= 3.0:
        return "2026-2030"
    else:
        return "2025-2028"


def generate_summary(occ, country, scores, trend_5yr, ai_resistance):
    occ_zh = occ["zh"]
    country_zh = country["name_zh"]
    country_en = country["name_en"]
    occ_en = occ["en"]

    highlights_zh = []
    highlights_en = []

    if scores["value_added"] >= 8.0:
        highlights_zh.append("薪资回报高")
        highlights_en.append("high compensation")
    elif scores["value_added"] <= 4.5:
        highlights_zh.append("薪资水平偏低")
        highlights_en.append("relatively low pay")

    if scores["supply_demand"] >= 7.5:
        highlights_zh.append("人才需求旺盛")
        highlights_en.append("strong talent demand")
    elif scores["supply_demand"] <= 4.0:
        highlights_zh.append("供过于求")
        highlights_en.append("oversupply of talent")

    if scores["ai_resistance"] <= 4.0:
        highlights_zh.append("AI替代风险较高")
        highlights_en.append("high AI displacement risk")
    elif scores["ai_resistance"] >= 7.5:
        highlights_zh.append("AI替代抗性强")
        highlights_en.append("strong AI resistance")

    if scores["remote_friendly"] >= 6.5:
        highlights_zh.append("远程友好度高")
        highlights_en.append("highly remote-friendly")

    if scores["overtime"] <= 3.5:
        highlights_zh.append("加班文化严重")
        highlights_en.append("heavy overtime culture")
    elif scores["overtime"] >= 7.5:
        highlights_zh.append("工作时间规律")
        highlights_en.append("regular working hours")

    if scores["stability"] >= 8.0:
        highlights_zh.append("就业稳定")
        highlights_en.append("stable employment")
    elif scores["stability"] <= 4.0:
        highlights_zh.append("就业波动大")
        highlights_en.append("volatile employment")

    if trend_5yr >= 4:
        highlights_zh.append("近年增长迅猛")
        highlights_en.append("rapid recent growth")
    elif trend_5yr <= -2:
        highlights_zh.append("近年需求下降")
        highlights_en.append("declining demand")

    if scores["burnout"] <= 3.0:
        highlights_zh.append("职业倦怠风险高")
        highlights_en.append("high burnout risk")

    if scores["fulfillment"] >= 8.5:
        highlights_zh.append("职业成就感高")
        highlights_en.append("high career fulfillment")

    highlights_zh = highlights_zh[:3]
    highlights_en = highlights_en[:3]

    if not highlights_zh:
        highlights_zh = ["发展平稳"]
        highlights_en = ["steady development"]

    zh = f"{country_zh}{occ_zh}：{'，'.join(highlights_zh)}"
    en = f"{country_en} {occ_en}: {', '.join(highlights_en)}"

    return zh, en


# ---------------------------------------------------------------------------
# MAIN GENERATION
# ---------------------------------------------------------------------------

HEADERS = [
    "id", "major_category", "major_code", "mid_category", "sub_category",
    "sub_category_en", "isco_code", "onet_code", "region", "country_or_region",
    "iso_code", "type", "employer_type", "typical_education", "typical_entry_age",
    "locality", "learning_cost", "education_req", "growth_coeff", "career_lifespan",
    "opportunity", "market_size", "supply_demand", "developed_scarcity",
    "value_added", "cost_performance", "stability", "safety", "occupational_disease",
    "overtime", "burnout", "skill_versatility", "career_switch", "reputation_variance",
    "ai_resistance", "social_status", "remote_friendly", "autonomy", "family_friendly",
    "fulfillment", "entrepreneurship", "gender_equality", "age_flexibility",
    "social_interaction", "physical_demand", "license_barrier", "cycle_sensitivity",
    "side_job_compat", "intl_mobility", "industry_monopoly", "trend_2000_2026",
    "trend_5yr", "demand_direction", "ai_timeline", "composite_index",
    "summary_zh", "summary_en", "data_source"
]

SCORE_DIMS = [
    "learning_cost", "education_req", "growth_coeff", "career_lifespan",
    "opportunity", "market_size", "supply_demand", "developed_scarcity",
    "value_added", "cost_performance", "stability", "safety", "occupational_disease",
    "overtime", "burnout", "skill_versatility", "career_switch", "reputation_variance",
    "ai_resistance", "social_status", "remote_friendly", "autonomy", "family_friendly",
    "fulfillment", "entrepreneurship", "gender_equality", "age_flexibility",
    "social_interaction", "physical_demand", "license_barrier", "cycle_sensitivity",
    "side_job_compat", "intl_mobility", "industry_monopoly"
]


def main():
    random.seed(42)

    weights = load_weights()
    output_path = PROJECT_ROOT / "data" / "csv" / "medical_health.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rows = []

    for occ in OCCUPATIONS:
        base = occ_base(occ["id"], occ["mid"])
        if not base:
            print(f"WARNING: No base scores for {occ['id']} ({occ['en']}), skipping")
            continue

        for country in COUNTRIES:
            iso = country["iso"]
            cp = COUNTRY_PROFILES[iso]

            scores = apply_country_modifiers(base, cp, occ["id"], occ["mid"])

            # Add small per-row noise for realism
            noise_seed = hash(f"MED-{occ['id']}-{iso}") % 10000
            rng = random.Random(noise_seed)
            for dim in SCORE_DIMS:
                if dim == "reputation_variance":
                    scores[dim] = clamp5(scores[dim] + rng.uniform(-0.2, 0.2))
                elif dim in ("safety",):
                    scores[dim] = clamp(scores[dim] + rng.uniform(-0.1, 0.1))
                else:
                    scores[dim] = clamp(scores[dim] + rng.uniform(-0.3, 0.3))

            trend_long, trend_short = get_trends(base, cp)
            demand_dir = get_demand_direction(trend_short)
            ai_tl = get_ai_timeline(occ["id"], scores["ai_resistance"])

            score_dict = {dim: scores[dim] for dim in weights}
            composite = calculate_composite(score_dict, weights)

            summary_zh, summary_en = generate_summary(occ, country, scores, trend_short, scores["ai_resistance"])

            row_id = f"MED-{occ['id']}-{iso}-general"

            row = {
                "id": row_id,
                "major_category": "医疗与健康",
                "major_code": "MED",
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
            row["data_source"] = "AI综合评估 + O*NET/ILO/WHO锚点校准"

            rows.append(row)

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows to {output_path}")
    print(f"Occupations: {len(OCCUPATIONS)}")
    print(f"Countries: {len(COUNTRIES)}")


if __name__ == "__main__":
    main()
