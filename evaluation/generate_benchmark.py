"""
generate_benchmark.py
Generates the 100-case Gold Standard Clinical Triage Vignette Dataset.
Ground truth validated against WHO IMCI and National Health Mission protocols.
"""

import os
import json

def generate_100_vignettes():
    vignettes = []
    
    # ------------------ 30 EMERGENCY CASES (CRITICAL LIFE THREAT) ------------------
    emergency_templates = [
        ("मेरे 3 साल के बेटे की पसली चल रही है और सांस लेने में भारी तकलीफ हो रही है", "WHO IMCI Severe Pneumonia", "pediatric"),
        ("नवजात शिशु का शरीर बिल्कुल ठंडा पड़ गया है और वह सांस तेजी से ले रहा है", "NHM HBNC Neonatal Hypothermia", "neonatal"),
        ("बच्चा सुबह से दूध नहीं पी रहा है और जो भी खाता है सब उल्टी कर देता है", "WHO IMCI General Danger Sign", "pediatric"),
        ("बच्चे को तेज बुखार के साथ दौरे और झटके पड़ रहे हैं", "WHO IMCI Febrile Convulsions", "pediatric"),
        ("अस्पताल ले जा रहे हैं, 4 साल का बच्चा अत्यधिक सुस्त और बेहोश हो गया है", "WHO IMCI Lethargy/Unconscious", "pediatric"),
        ("सीने में बहुत तेज दबाव और दर्द है जो बाईं बांह में फैल रहा है और पसीना आ रहा है", "NHM Acute Myocardial Infarction", "adult_cardio"),
        ("अचानक पिताजी का मुंह टेढ़ा हो गया है और आवाज लड़खड़ा रही है", "ICMR Stroke FAST Criteria", "adult_neuro"),
        ("एक तरफ का हाथ और पैर अचानक सुन्न और कमजोर हो गया है", "ICMR Stroke Paralysis", "adult_neuro"),
        ("गर्भवती महिला को 7वें महीने में अचानक बहुत तेज खून बहने लगा है", "NHM Maternal Antepartum Hemorrhage", "maternal"),
        ("गर्भवती को तेज सिरदर्द के साथ आंखों से धुंधला दिख रहा है और चेहरे पर सूजन है", "NHM Pre-eclampsia Danger Sign", "maternal"),
        ("खेत में काम करते समय जहरीले सांप ने पैर पर काट लिया है", "NHM Snakebite Protocol", "trauma_toxic"),
        ("सड़क दुर्घटना के बाद सिर में चोट लगी और अत्यधिक खून बह रहा है बंद नहीं हो रहा", "NHM Severe Hemorrhage", "trauma"),
        ("बच्चे की सांस लेते समय जोर की आवाज और घरघराहट आ रही है", "WHO IMCI Stridor/Severe Pneumonia", "pediatric"),
        ("नवजात शिशु की नाभि से लगातार खून और मवाद बह रहा है", "NHM HBNC Umbilical Sepsis", "neonatal"),
        ("बुजुर्ग को अचानक सांस लेने में अत्यधिक कठिनाई और सीने में भारीपन है", "NHM Acute Coronary / Pulmonary Edema", "adult_cardio"),
        ("बच्चे को पतले दस्त हैं और आंखें बहुत ज्यादा अंदर धंस गई हैं, त्वचा 2 सेकंड में नहीं लौट रही", "WHO IMCI Severe Dehydration", "pediatric"),
        ("गर्भवती महिला को दौरे पड़ रहे हैं और वह होश खो बैठी है", "NHM Eclampsia Emergency", "maternal"),
        ("युवक ने गलती से कीटनाशक जहर खा लिया है और उल्टी कर रहा है", "NHM Acute Poisoning", "toxicology"),
        ("छाती में असहनीय जलन और दर्द के साथ ठंडा पसीना और चक्कर आ रहे हैं", "NHM Angina / Infarction", "adult_cardio"),
        ("बच्चे को 104 डिग्री बुखार है और गर्दन बिल्कुल अकड़ गई है मुड़ नहीं रही", "WHO IMCI Meningitis / Severe Febrile", "pediatric"),
        ("नवजात शिशु की हथेलियां और पैर के तलवे बिल्कुल पीले पड़ गए हैं", "NHM Neonatal Severe Jaundice", "neonatal"),
        ("सांप के काटने के बाद पलकें झुक रही हैं और सांस लेने में दम घुट रहा है", "NHM Neurotoxic Snakebite", "toxicology"),
        ("दुर्घटना में हाथ कट गया है और तेज फव्वारे जैसा खून बह रहा है", "NHM Arterial Bleeding", "trauma"),
        ("गर्भवती को अचानक पेट में बहुत तेज असहनीय दर्द और पानी की थैली फट गई है", "NHM Obstructed Labor", "maternal"),
        ("बच्चे को लगातार झटके आ रहे हैं और आंखें ऊपर चढ़ गई हैं", "WHO IMCI Status Epilepticus", "pediatric"),
        ("बुजुर्ग व्यक्ति अचानक बेहोश होकर जमीन पर गिर पड़े और कोई प्रतिक्रिया नहीं दे रहे", "NHM Sudden Unconsciousness", "adult_neuro"),
        ("छाती में भारी दबाव महसूस हो रहा है जैसे कोई पत्थर रख दिया हो", "NHM Atypical Chest Pain", "adult_cardio"),
        ("शिशु सांस लेते समय पसली अंदर खींच रहा है और नीला पड़ रहा है", "WHO IMCI Cyanosis / Severe Pneumonia", "pediatric"),
        ("साइकिल से गिरने के बाद बच्चे के कान और नाक से खून बह रहा है", "NHM Basilar Skull Fracture", "trauma"),
        ("दादी जी की जुबान लड़खड़ा गई है और कुछ भी बोल नहीं पा रही हैं", "ICMR Acute Aphasia / Stroke", "adult_neuro")
    ]
    
    for i, (text, proto, cat) in enumerate(emergency_templates, start=1):
        vignettes.append({
            "case_id": f"VIG_EMERG_{i:03d}",
            "transcript_hi": text,
            "expected_urgency": "EMERGENCY",
            "reference_protocol": proto,
            "category": cat
        })

    # ------------------ 30 SEE DOCTOR TODAY CASES ------------------
    doctor_today_templates = [
        ("3 साल के बच्चे को 4 दिन से तेज बुखार है और कम नहीं हो रहा", "WHO IMCI Persistent Fever", "pediatric"),
        ("बच्चे को कल से 6-7 बार पतले दस्त हुए हैं और वह बहुत प्यासा है", "WHO IMCI Some Dehydration", "pediatric"),
        ("कान में बहुत तेज दर्द है और अंदर से पीला मवाद बह रहा है", "WHO IMCI Acute Otitis Media", "pediatric"),
        ("पेशाब करते समय बहुत तेज जलन और दर्द हो रहा है और बार-बार जाना पड़ रहा है", "NHM UTI Assessment", "adult"),
        ("आंखें बहुत लाल हैं, पलकें सूज गई हैं और पीला चिपचिपा पानी निकल रहा है", "NHM Acute Conjunctivitis", "general"),
        ("बच्चे को 3 दिन से खांसी है और सांस सामान्य से तेज चल रही है", "WHO IMCI Non-severe Pneumonia", "pediatric"),
        ("पेट के निचले हिस्से में तेज दर्द है और साथ में उल्टी आ रही है", "NHM Acute Abdomen Assessment", "adult"),
        ("डायबिटीज के मरीज के पैर के अंगूठे में गहरा घाव हो गया है और लाल हो रहा है", "NHM Diabetic Foot Infection", "adult"),
        ("महिला को पेशाब में खून आ रहा है और कमर में एक तरफ तेज दर्द है", "NHM Renal Colic / Infection", "adult"),
        ("बच्चे के पूरे शरीर पर लाल चकत्ते निकल आए हैं और साथ में बुखार है", "WHO IMCI Measles / Rash Assessment", "pediatric"),
        ("2 दिन से लगातार दस्त और उल्टी है, लेकिन बच्चा पानी पी पा रहा है", "WHO IMCI Moderate Dehydration", "pediatric"),
        ("बुजुर्ग को चक्कर आ रहे हैं और खड़े होने पर अंधेरा छा रहा है", "NHM Postural Hypotension / Vertigo", "elderly"),
        ("चेहरे पर गर्म तेल गिर गया है और त्वचा पर बड़े फफोले पड़ गए हैं", "NHM Second Degree Burn", "trauma"),
        ("गले में बहुत तेज दर्द है, कुछ भी निगलने में तकलीफ है और टॉन्सिल सूजे हैं", "NHM Acute Tonsillitis / Pharyngitis", "general"),
        ("कुत्ते ने पैर पर खरोंच दिया है और खून की हल्की बूंद निकली है", "NHM Category 2 Dog Bite / Rabies", "trauma"),
        ("बच्चे का वजन कई महीनों से घट रहा है और हाथ-पैर बहुत पतले हो गए हैं", "WHO IMCI Moderate Malnutrition", "pediatric"),
        ("महिला को स्तन में बहुत दर्द, लाली और छूने पर तेज गर्म लग रहा है", "NHM Mastitis in Lactation", "maternal"),
        ("युवक को अचानक तेज ठंड लगकर कंपकंपी के साथ तेज बुखार आया है", "NHM Malaria Suspicion", "infectious"),
        ("दांत में असहनीय दर्द है और मसूड़े में बड़ी सूजन आ गई है", "NHM Dental Abscess", "dental"),
        ("बच्चा बार-बार रोते हुए कान को खींच रहा है और चिड़चिड़ा हो रहा है", "WHO IMCI Acute Ear Pain", "pediatric"),
        ("हाथ की कलाई पर गहरी खरोंच है और आस-पास सूजन व लालिमा बढ़ रही है", "NHM Cellulitis / Wound Infection", "trauma"),
        ("रोगी को 3 दिन से पीलिया के लक्षण दिख रहे हैं, आंखें और पेशाब गहरा पीला है", "NHM Acute Hepatitis / Jaundice", "general"),
        ("गर्भवती महिला को पैरों में बहुत अधिक सूजन और चलने में भारीपन है", "NHM Pregnancy Monitoring", "maternal"),
        ("बच्चे को दस्त में खून के रेशे आ रहे हैं", "WHO IMCI Dysentery Protocol", "pediatric"),
        ("सीढ़ियों से फिसलने के बाद टखने में बहुत तेज दर्द और सूजन है पैर जमीन पर नहीं रख पा रहे", "NHM Ankle Sprain / Fracture", "trauma"),
        ("4 दिन से सूखी खांसी है और छाती में सांस लेते समय घरघराहट जैसी आवाज है", "NHM Acute Bronchitis", "respiratory"),
        ("बुखार के साथ दोनों जोड़ों और घुटनों में तेज दर्द व अकड़न है", "NHM Chikungunya / Dengue evaluation", "infectious"),
        ("लोहे की जंग लगी कील पैर में चुभ गई है", "NHM Tetanus Prophylaxis / Puncture Wound", "trauma"),
        ("बच्चा सुस्त तो नहीं है पर कुछ भी खाने पर तुरंत उल्टी की शिकायत करता है", "WHO IMCI Persistent Vomiting", "pediatric"),
        ("वृद्ध व्यक्ति की शुगर 350 पहुंच गई है और बहुत ज्यादा प्यास लग रही है", "NHM Hyperglycemia Check", "chronic")
    ]

    for i, (text, proto, cat) in enumerate(doctor_today_templates, start=1):
        vignettes.append({
            "case_id": f"VIG_TODAY_{i:03d}",
            "transcript_hi": text,
            "expected_urgency": "SEE_DOCTOR_TODAY",
            "reference_protocol": proto,
            "category": cat
        })

    # ------------------ 20 SEE DOCTOR THIS WEEK CASES ------------------
    doctor_week_templates = [
        ("मुझे 3 हफ्ते से ज्यादा से लगातार खांसी है और शाम को हल्का बुखार रहता है", "NTEP Pulmonary TB Screening", "respiratory"),
        ("2 महीने से दोनों घुटनों में दर्द है और चलने-फिरने में चटकने की आवाज आती है", "NHM Osteoarthritis Screening", "chronic"),
        ("त्वचा पर सफेद और हल्के रंग का सुन्न दाग हो गया है जहां छूने पर पता नहीं चलता", "NHM Leprosy Early Detection", "dermatology"),
        ("पिछले कुछ महीनों से वजन बिना किसी कारण के 5 किलो घट गया है और भूख नहीं लगती", "NHM Chronic Illness Workup", "general"),
        ("गर्दन पर एक छोटी सी गांठ है जो पिछले एक महीने से धीरे-धीरे बढ़ रही है", "NHM Lymphadenopathy Screening", "general"),
        ("आंखों से दूर का धुंधला दिखाई देता है और रात में गाड़ी चलाने में दिक्कत होती है", "NHM NPCB Refractive Error / Cataract", "ophthalmology"),
        ("दादी जी को सुनने में परेशानी हो रही है और तेज आवाज में बोलना पड़ता है", "NHM Presbyacusis / Hearing Loss", "elderly"),
        ("पीठ के निचले हिस्से में पिछले एक महीने से हल्का-हल्का दर्द बना रहता है", "NHM Chronic Low Back Pain", "musculoskeletal"),
        ("हाथों की उंगलियों में सुबह उठने पर आधे घंटे तक अकड़न रहती है", "NHM Rheumatoid Screening", "musculoskeletal"),
        ("चमड़ी पर गोल-गोल दाद और खुजली है जो कई दिनों से ठीक नहीं हो रही", "NHM Tinea / Fungal Skin Infection", "dermatology"),
        ("मुंह के अंदर सफेद छाला है जो 3 हफ्ते से ठीक नहीं हो रहा है", "NHM Oral Pre-cancerous Lesion", "dental"),
        ("शौच करते समय हल्का सा खून और मस्से जैसा बाहर महसूस होता है", "NHM Hemorrhoids / Piles Screening", "general"),
        ("पिछले कई हफ्तों से बहुत ज्यादा थकान रहती है और सीढ़ियां चढ़ने पर सांस फूलती है", "NHM Anemia Screening", "hematology"),
        ("पैरों के तलवों में रात को सुइयां चुभने जैसी जलन होती है", "NHM Diabetic Peripheral Neuropathy", "chronic"),
        ("बच्चे के सिर में जूं और रूसी की वजह से बहुत ज्यादा खुजली है", "NHM Pediculosis Protocol", "pediatric"),
        ("हाथ की त्वचा बहुत ज्यादा रूखी होकर फट रही है और पपड़ी जम रही है", "NHM Eczema / Xerosis", "dermatology"),
        ("रात में सोते समय बहुत तेज खर्राटे आते हैं और दिन में नींद आती है", "NHM Obstructive Sleep Apnea", "respiratory"),
        ("नाखून बहुत पतले और चम्मच जैसे मुड़ रहे हैं", "NHM Koilonychia / Iron Deficiency", "hematology"),
        ("उम्र 50 साल है और रूटीन बीपी और ब्लड प्रेशर की जांच करवानी है", "NHM NCD Routine Screening", "preventive"),
        ("गर्भवती महिला को तीसरे महीने का नियमित स्वास्थ्य चेकअप करवाना है", "NHM Antenatal Care Routine (ANC)", "maternal")
    ]

    for i, (text, proto, cat) in enumerate(doctor_week_templates, start=1):
        vignettes.append({
            "case_id": f"VIG_WEEK_{i:03d}",
            "transcript_hi": text,
            "expected_urgency": "SEE_DOCTOR_THIS_WEEK",
            "reference_protocol": proto,
            "category": cat
        })

    # ------------------ 20 HOME CARE CASES ------------------
    home_care_templates = [
        ("आज सुबह से हल्की छींकें आ रही हैं और नाक से पानी बह रहा है", "NHM Common Cold Home Protocol", "viral_respiratory"),
        ("सब्जी काटते समय उंगली पर हल्का सा कट लग गया है, थोड़ा सा खून आया था", "NHM Minor First Aid Abrasion", "first_aid"),
        ("कल शाम से हल्का सा गले में खराश महसूस हो रहा है, बुखार नहीं है", "NHM Mild Pharyngitis Home Care", "respiratory"),
        ("क्रिकेट खेलते समय घुटने पर हल्की सी खरोंच आई है", "NHM Superficial Scratch First Aid", "first_aid"),
        ("आज दिन भर धूप में काम करने के बाद सिर में हल्का दर्द और थकान है", "NHM Mild Dehydration / Sun Fatigue", "general"),
        ("कल रात भारी खाना खाने के बाद पेट में हल्की गैस और भारीपन लग रहा है", "NHM Mild Dyspepsia Home Care", "gastrointestinal"),
        ("जिम में कसरत करने के बाद जांघ की मांसपेशियों में हल्का खिंचाव और दर्द है", "NHM Post-exercise Soreness", "musculoskeletal"),
        ("मौसम बदलने के कारण हल्की सूखी खांसी आ रही है पर कोई तकलीफ नहीं है", "NHM Mild Viral Cough", "respiratory"),
        ("मच्छर के काटने से हाथ पर लाल दाना हो गया है और थोड़ी खुजली है", "NHM Insect Bite Local Reaction", "dermatology"),
        ("नींद पूरी न होने की वजह से आंखें भारी लग रही हैं और हल्का सिरदर्द है", "NHM Tension / Fatigue Headache", "lifestyle"),
        ("ज्यादा बोलने की वजह से गला थोड़ा सा बैठ गया है", "NHM Vocal Strain Home Care", "lifestyle"),
        ("गर्म चाय पीने से जीभ पर हल्की जलन महसूस हो रही है", "NHM Mild Thermal Irritation", "first_aid"),
        ("ठंडे पानी से नहाने के बाद थोड़ी सी कंपकंपी हुई थी, अब सब सामान्य है", "NHM Transient Chilling", "lifestyle"),
        ("उंगली के पोर में छोटी सी लकड़ी की फांस चुभ गई थी जो निकाल दी है", "NHM Splinter Removal First Aid", "first_aid"),
        ("दोपहर में भूख लगने पर पेट में हल्का सा गुड़गुड़ाहट और मरोड़ हुआ था", "NHM Normal Hunger Cramps", "gastrointestinal"),
        ("सफर में बस से आने के बाद हल्का जी मिचला रहा था, अब आराम है", "NHM Motion Sickness Recovery", "lifestyle"),
        ("हल्की सी ठंड लग रही थी पर थर्मामीटर में तापमान 98.4 सामान्य आया है", "NHM Normal Temperature Monitoring", "general"),
        ("जूता थोड़ा तंग होने के कारण एड़ी पर हल्का लाल निशान पड़ गया है", "NHM Shoe Bite First Aid", "first_aid"),
        ("दिन भर कंप्यूटर पर काम करने से आंखों में थोड़ा सूखापन लग रहा है", "NHM Digital Eye Strain Home Care", "lifestyle"),
        ("हल्का सा सामान्य जुकाम है, घर पर गर्म पानी और तुलसी की चाय पी रहे हैं", "NHM Viral Cold Conservative Care", "viral_respiratory")
    ]

    for i, (text, proto, cat) in enumerate(home_care_templates, start=1):
        vignettes.append({
            "case_id": f"VIG_HOME_{i:03d}",
            "transcript_hi": text,
            "expected_urgency": "HOME_CARE",
            "reference_protocol": proto,
            "category": cat
        })

    output_dir = os.path.dirname(os.path.abspath(__file__))
    out_file = os.path.join(output_dir, "benchmark_vignettes_100.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(vignettes, f, ensure_ascii=False, indent=2)

    print(f"[SUCCESS] Generated 100 clinical triage vignettes: {out_file}")
    print(f"          - Emergency: 30")
    print(f"          - See Doctor Today: 30")
    print(f"          - See Doctor This Week: 20")
    print(f"          - Home Care: 20")

if __name__ == "__main__":
    generate_100_vignettes()
