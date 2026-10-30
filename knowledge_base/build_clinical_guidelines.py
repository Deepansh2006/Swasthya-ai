"""
build_clinical_guidelines.py
Constructs the clinical guideline repository from official WHO IMCI, NHM ASHA Modules,
and ICMR triage protocols. Generates structured JSONL chunks with metadata.
"""

import os
import json

GUIDELINE_CHUNKS = [
    # ------------------ WHO IMCI PEDIATRIC GENERAL DANGER SIGNS ------------------
    {
        "id": "WHO_IMCI_DANGER_01",
        "protocol": "WHO IMCI Chart Booklet (2014) - Section 1",
        "source": "WHO Integrated Management of Childhood Illness (IMCI)",
        "page": 12,
        "category": "pediatric_emergency",
        "target_group": "infant_child",
        "title_en": "General Danger Signs in Children (Age 2 Months to 5 Years)",
        "content_en": (
            "A child with any general danger sign has a serious problem and requires URGENT attention "
            "and immediate referral to a hospital. Check for: "
            "1. Child is unable to drink or breastfeed. "
            "2. Child vomits everything consumed. "
            "3. Child has had convulsions or fits during this illness. "
            "4. Child is lethargic or unconscious. "
            "Action: Give first dose of appropriate antibiotic if indicated. Keep child warm. "
            "Refer URGENTLY to hospital. Call 108 ambulance immediately."
        ),
        "content_hi": (
            "2 महीने से 5 वर्ष के बच्चों में खतरे के मुख्य लक्षण (General Danger Signs): "
            "यदि बच्चा स्तनपान या कुछ भी पीने में असमर्थ है, जो भी खाता-पीता है सब उल्टी कर देता है, "
            "बीमारी के दौरान दौरे या झटके पड़े हों, या बच्चा अत्यधिक सुस्त या बेहोश है। "
            "यह एक गंभीर आपात स्थिति है। तुरंत 108 एम्बुलेंस बुलाकर नजदीकी बड़े अस्पताल ले जाएं।"
        ),
        "triage_urgency": "EMERGENCY",
        "keywords": ["vomits everything", "unable to drink", "convulsions", "lethargic", "unconscious", 
                     "दूध नहीं पी रहा", "उल्टी सब कुछ", "दौरे", "झटके", "सुस्त", "बेहोश"]
    },
    {
        "id": "WHO_IMCI_RESP_01",
        "protocol": "WHO IMCI Chart Booklet (2014) - Section 2",
        "source": "WHO Integrated Management of Childhood Illness (IMCI)",
        "page": 15,
        "category": "pediatric_respiratory",
        "target_group": "infant_child",
        "title_en": "Cough or Difficult Breathing - Severe Pneumonia Assessment",
        "content_en": (
            "Assess any child with cough or difficult breathing. "
            "Signs of Severe Pneumonia or Very Severe Disease: "
            "- Any general danger sign OR "
            "- Chest indrawing (lower chest wall goes in when child breathes in) OR "
            "- Stridor in calm child. "
            "Fast breathing thresholds: Age 2-11 months: 50 breaths/min or more. "
            "Age 12 months to 5 years: 40 breaths/min or more. "
            "Triage Classification: Severe Pneumonia -> URGENT referral to hospital. "
            "Non-severe pneumonia with fast breathing -> See doctor today for oral amoxicillin."
        ),
        "content_hi": (
            "खांसी या सांस लेने में कठिनाई - निमोनिया का आकलन: "
            "यदि बच्चे की छाती सांस लेते समय अंदर धंस रही है (Chest indrawing), सांस लेते समय आवाज आ रही है (Stridor), "
            "या सांस की गति बहुत तेज है (2-11 माह में 50+ प्रति मिनट, 1-5 वर्ष में 40+ प्रति मिनट)। "
            "छाती धंसने या खतरे के लक्षण होने पर तुरंत अस्पताल जाएं (Emergency)। "
            "केवल तेज सांस होने पर आज ही प्राथमिक स्वास्थ्य केंद्र (PHC) में डॉक्टर को दिखाएं।"
        ),
        "triage_urgency": "EMERGENCY",
        "keywords": ["chest indrawing", "fast breathing", "stridor", "pneumonia", "difficulty breathing",
                     "छाती धंसना", "तेज सांस", "पसली चलना", "सांस फूलना", "घरघराहट"]
    },
    {
        "id": "WHO_IMCI_DIARRHEA_01",
        "protocol": "WHO IMCI Chart Booklet (2014) - Section 3",
        "source": "WHO Integrated Management of Childhood Illness (IMCI)",
        "page": 18,
        "category": "pediatric_gastrointestinal",
        "target_group": "infant_child",
        "title_en": "Diarrhoea and Dehydration Triage Classification",
        "content_en": (
            "Classify dehydration in child with loose stools: "
            "1. Severe Dehydration (Two of: lethargic/unconscious, sunken eyes, unable to drink/drinking poorly, "
            "skin pinch goes back very slowly > 2 sec). -> Triage: EMERGENCY. Immediate IV fluids. "
            "2. Some Dehydration (Two of: restless/irritable, sunken eyes, drinks eagerly/thirsty, "
            "skin pinch goes back slowly). -> Triage: SEE_DOCTOR_TODAY. Start ORS and Zinc, visit PHC today. "
            "3. No Dehydration: -> Triage: HOME_CARE. Extra fluids, continuation of breastfeeding, ORS, watch for danger signs."
        ),
        "content_hi": (
            "दस्त और निर्जलीकरण (Dehydration) का वर्गीकरण: "
            "1. गंभीर निर्जलीकरण: आंखें अंदर धंसना, त्वचा खींचने पर 2 सेकंड से ज्यादा में लौटना, बच्चा सुस्त या बेहोश होना। तुरंत अस्पताल ले जाएं (EMERGENCY)। "
            "2. मध्यम निर्जलीकरण: बच्चा चिड़चिड़ा है, प्यास बहुत अधिक है, आंखें धंसी हैं। आज ही स्वास्थ्य केंद्र जाकर ओआरएस (ORS) और जिंक शुरू करें (SEE_DOCTOR_TODAY)। "
            "3. निर्जलीकरण के लक्षण नहीं: घर पर ओआरएस घोल, छाछ, नारियल पानी और पर्याप्त तरल पदार्थ दें (HOME_CARE)।"
        ),
        "triage_urgency": "SEE_DOCTOR_TODAY",
        "keywords": ["diarrhea", "loose motion", "dehydration", "sunken eyes", "skin pinch", "ORS",
                     "दस्त", "पतले दस्त", "उल्टी दस्त", "आंखें धंसना", "पानी की कमी", "ओआरएस"]
    },
    {
        "id": "WHO_IMCI_FEVER_01",
        "protocol": "WHO IMCI Chart Booklet (2014) - Section 4",
        "source": "WHO Integrated Management of Childhood Illness (IMCI)",
        "page": 22,
        "category": "pediatric_fever",
        "target_group": "infant_child",
        "title_en": "Fever Assessment and Malaria / Meningitis Red Flags",
        "content_en": (
            "Assess child with fever: "
            "Very Severe Febrile Disease: Any general danger sign OR stiff neck OR bulging fontanelle in infants. "
            "Triage: EMERGENCY. High risk of cerebral malaria or meningitis. "
            "Fever present for more than 7 days, or fever with persistent pain/vomiting: "
            "Triage: SEE_DOCTOR_TODAY. Test for malaria, dengue, or bacterial infection. "
            "Mild fever on day 1-2 without danger signs, rash, or stiffness: "
            "Triage: HOME_CARE. Keep child cool, offer fluids, monitor temperature, seek care if fever exceeds 3 days."
        ),
        "content_hi": (
            "बुखार का आकलन (Fever Assessment): "
            "यदि तेज बुखार के साथ गर्दन में अकड़न है, सिर का तालू फूला हुआ है, या बच्चा बेहोश/सुस्त है, "
            "तो यह मस्तिष्क ज्वर (Meningitis) का संकेत हो सकता है। तुरंत अस्पताल ले जाएं (EMERGENCY)। "
            "यदि बुखार 3 दिन से अधिक समय से है या साथ में तेज बदन दर्द/उल्टी है, तो आज ही डॉक्टर को दिखाएं (SEE_DOCTOR_TODAY)। "
            "पहले दिन का हल्का बुखार बिना किसी खतरे के लक्षण के होने पर घर पर आराम और तरल पदार्थ दें (HOME_CARE)।"
        ),
        "triage_urgency": "SEE_DOCTOR_TODAY",
        "keywords": ["fever", "stiff neck", "high temperature", "meningitis", "malaria", "dengue",
                     "बुखार", "तेज बुखार", "गर्दन अकड़ना", "ठंड लगकर बुखार", "सिरदर्द"]
    },

    # ------------------ NHM ASHA MATERNAL & PREGNANCY PROTOCOLS ------------------
    {
        "id": "NHM_ASHA_PREG_01",
        "protocol": "National Health Mission - ASHA Training Module 6",
        "source": "Ministry of Health and Family Welfare, Govt. of India",
        "page": 35,
        "category": "maternal_emergency",
        "target_group": "pregnant_woman",
        "title_en": "Danger Signs During Pregnancy (Maternal Red Flags)",
        "content_en": (
            "Any of the following signs in a pregnant woman is a medical EMERGENCY: "
            "1. Vaginal bleeding at any stage of pregnancy. "
            "2. Severe headache with blurred vision, dizziness, or swelling of hands/face (Pre-eclampsia/Eclampsia). "
            "3. Convulsions or loss of consciousness. "
            "4. High fever with chills and foul-smelling vaginal discharge. "
            "5. Severe abdominal pain or water breaking prematurely. "
            "Action: Do not wait. Call 108 ambulance immediately and transport to the nearest FRU / District Hospital."
        ),
        "content_hi": (
            "गर्भावस्था में खतरे के प्रमुख लक्षण (राष्ट्रीय स्वास्थ्य मिशन दिशानिर्देश): "
            "गर्भावस्था के किसी भी महीने में योनि से रक्तस्राव (Bleeding), तेज सिरदर्द के साथ आंखों से धुंधला दिखना, "
            "हाथों-चेहरे पर अचानक सूजन, दौरे पड़ना, तेज पेट दर्द या तेज बुखार आना अत्यंत गंभीर हैं। "
            "बिना किसी देरी के तुरंत 108 एम्बुलेंस को कॉल करें और गर्भवती महिला को निकटतम अस्पताल ले जाएं।"
        ),
        "triage_urgency": "EMERGENCY",
        "keywords": ["pregnancy bleeding", "blurred vision", "swelling face", "eclampsia", "labor pain",
                     "गर्भावस्था में खून", "धुंधला दिखना", "चेहरे पर सूजन", "गर्भवती तेज दर्द", "रक्तस्राव"]
    },
    {
        "id": "NHM_ASHA_NEWBORN_01",
        "protocol": "National Health Mission - ASHA Training Module 7 (HBNC)",
        "source": "MOHFW - Home Based Newborn Care",
        "page": 42,
        "category": "neonatal_emergency",
        "target_group": "neonate",
        "title_en": "Newborn Danger Signs (First 28 Days of Life)",
        "content_en": (
            "Immediate referral criteria for newborns under 28 days: "
            "1. Body cold to touch (severe hypothermia) despite warming. "
            "2. Temperature > 37.5 C (fever in a newborn is always an emergency). "
            "3. Fast breathing (> 60 breaths per minute) or chest in-drawing. "
            "4. Yellow palms or soles in first week of life (severe neonatal jaundice). "
            "5. Bleeding from umbilical stump or discharge with foul odor. "
            "Action: Wrap newborn skin-to-skin (KMC), transport immediately to SNCU via 108."
        ),
        "content_hi": (
            "नवजात शिशु (जन्म से 28 दिन) के खतरे के लक्षण: "
            "शिशु के हाथ-पैर या शरीर का ठंडा पड़ना (Hypothermia), 1 माह से छोटे शिशु को बुखार आना, "
            "सांस की गति 60 प्रति मिनट से तेज होना, हथेलियों व तलवों का पीला पड़ना, या नाभि से खून/मवाद बहना। "
            "नवजात में यह सभी लक्षण इमरजेंसी हैं। तुरंत 108 बुलाकर नजदीकी विशेष नवजात शिशु इकाई (SNCU) पहुंचें।"
        ),
        "triage_urgency": "EMERGENCY",
        "keywords": ["newborn cold", "hypothermia", "newborn fever", "fast breathing neonate", "jaundice soles",
                     "नवजात ठंडा", "छोटे बच्चे को बुखार", "नाभि से मवाद", "पीलिया नवजात", "कमजोर रोना"]
    },

    # ------------------ ADULT ACUTE EMERGENCIES (NHM / ICMR) ------------------
    {
        "id": "NHM_ADULT_CARDIO_01",
        "protocol": "NHM Emergency Medical Protocol - Acute Coronary & Stroke",
        "source": "National Health Mission & ICMR Guidelines",
        "page": 14,
        "category": "adult_cardiovascular",
        "target_group": "adult_elderly",
        "title_en": "Acute Chest Pain and Suspected Heart Attack (Myocardial Infarction)",
        "content_en": (
            "Recognize acute myocardial infarction: "
            "- Severe, squeezing, crushing pain or heaviness in center of chest lasting > 15 minutes. "
            "- Pain radiating to left arm, shoulder, jaw, neck, or back. "
            "- Associated with profuse cold sweating, shortness of breath, dizziness, or nausea. "
            "Action: Do not walk or exert. Call 108 immediately. Keep patient seated comfortably. "
            "Transport with urgency to facility with ECG capability."
        ),
        "content_hi": (
            "हार्ट अटैक (दिल का दौरा) एवं सीने में तेज दर्द: "
            "छाती के बीचों-बीच भारीपन, दबाव या तेज चुभन महसूस होना जो बाईं बांह, कंधे, जबड़े या पीठ तक फैल रहा हो, "
            "और साथ में पसीना आना, सांस फूलना या घबराहट होना। "
            "यह जानलेवा आपात स्थिति है। मरीज को चलने न दें, आराम से बैठाएं और तुरंत 108 एम्बुलेंस पर कॉल करें।"
        ),
        "triage_urgency": "EMERGENCY",
        "keywords": ["chest pain", "heart attack", "sweating chest", "left arm pain", "breathlessness",
                     "छाती में दर्द", "सीने में भारीपन", "बाईं बांह में दर्द", "पसीना आना", "दिल का दौरा"]
    },
    {
        "id": "NHM_ADULT_STROKE_01",
        "protocol": "NHM Emergency Medical Protocol - Stroke FAST Criteria",
        "source": "ICMR Guidelines for Management of Stroke",
        "page": 8,
        "category": "adult_neurological",
        "target_group": "adult_elderly",
        "title_en": "Acute Stroke Identification (FAST Protocol)",
        "content_en": (
            "Check for Stroke using F.A.S.T.: "
            "- Face: Sudden facial drooping or asymmetry when smiling. "
            "- Arm: Sudden weakness or numbness in one arm or leg. "
            "- Speech: Sudden slurred speech or inability to speak. "
            "- Time: Immediate emergency hospital transport required. "
            "Window of intervention is under 4.5 hours. Call 108 immediately."
        ),
        "content_hi": (
            "लकवा या ब्रेन स्ट्रोक (Brain Stroke / FAST लक्षण): "
            "अचानक मुंह या चेहरे का टेढ़ा हो जाना, एक तरफ के हाथ या पैर में कमजोरी/सुन्नपन आ जाना, "
            "या अचानक आवाज का लड़खड़ाना अथवा बोलने में असमर्थ होना। "
            "तुरंत 108 पर कॉल करें। पहले 4.5 घंटे (Golden Hours) में अस्पताल पहुंचना मरीज की जान बचा सकता है।"
        ),
        "triage_urgency": "EMERGENCY",
        "keywords": ["stroke", "facial drooping", "arm weakness", "slurred speech", "paralysis",
                     "लकवा", "मुंह टेढ़ा", "हाथ पैर सुन्न", "आवाज लड़खड़ाना", "स्ट्रोक"]
    },
    {
        "id": "NHM_ACUTE_TRAUMA_01",
        "protocol": "NHM First Aid & Emergency Management Protocol",
        "source": "National Health Mission - Primary Emergency Care",
        "page": 28,
        "category": "acute_trauma_poisoning",
        "target_group": "all",
        "title_en": "Snakebite, Severe Bleeding, and Unconsciousness",
        "content_en": (
            "Critical Life-Threatening Emergencies: "
            "1. Snakebite: Immobilize bitten limb with a splint. Keep calm. Do NOT cut, burn, or apply tourniquet. Rush to hospital for anti-snake venom (ASV). "
            "2. Severe Uncontrolled Bleeding: Apply firm, continuous direct pressure with a clean cloth. "
            "3. Sudden Unresponsiveness or Seizures lasting > 5 minutes: Protect airway, place on side (recovery position), call 108."
        ),
        "content_hi": (
            "सर्पदंश (सांप का काटना), भारी रक्तस्राव और बेहोशी: "
            "1. सांप के काटने पर: काटे हुए हिस्से को हिलाएं नहीं (लकड़ी की खपच्ची बांधें)। चीरा न लगाएं, रस्सी से कसकर न बांधें। तुरंत 108 बुलाकर अस्पताल जाएं। "
            "2. बहुत अधिक खून बहने पर: साफ कपड़े से घाव को लगातार जोर से दबाकर रखें। "
            "3. बेहोश होने या लंबे समय तक दौरे पड़ने पर: करवट से लिटाएं और तुरंत अस्पताल ले जाएं।"
        ),
        "triage_urgency": "EMERGENCY",
        "keywords": ["snakebite", "heavy bleeding", "unconscious", "head injury", "convulsion",
                     "सांप का काटना", "खून बहना", "बेहोशी", "गंभीर चोट", "जहरीला कीड़ा"]
    },

    # ------------------ SUB-ACUTE & ROUTINE PHC CONDITIONS ------------------
    {
        "id": "NHM_PRIMARY_COUGH_01",
        "protocol": "National Tuberculosis Elimination Programme (NTEP) & NHM",
        "source": "Central TB Division, MOHFW",
        "page": 16,
        "category": "subacute_respiratory",
        "target_group": "adult",
        "title_en": "Chronic Cough Lasting Over Two Weeks (TB Screening)",
        "content_en": (
            "Any individual presenting with cough lasting for 2 weeks or more, accompanied by "
            "low-grade evening fever, night sweats, unexplained weight loss, or blood in sputum: "
            "Triage: SEE_DOCTOR_THIS_WEEK. Visit the nearest Primary Health Centre or Ayushman Arogya Mandir "
            "for free sputum testing (NAAT / Microscopy) and chest X-ray under NTEP."
        ),
        "content_hi": (
            "2 सप्ताह से अधिक समय से खांसी (टीबी की जांच): "
            "यदि खांसी 2 हफ्ते से ज्यादा से है, साथ में शाम को हल्का बुखार, रात में पसीना, या वजन घट रहा है, "
            "तो इस सप्ताह नजदीकी प्राथमिक स्वास्थ्य केंद्र (PHC) या आरोग्य मंदिर में जाकर बलगम की मुफ्त जांच करवाएं। "
            "यह टीबी (Tuberculosis) की जांच के लिए आवश्यक है।"
        ),
        "triage_urgency": "SEE_DOCTOR_THIS_WEEK",
        "keywords": ["cough two weeks", "night sweats", "weight loss", "blood sputum", "TB test",
                     "पुरानी खांसी", "दो हफ्ते से खांसी", "रात में पसीना", "वजन कम होना", "बलगम"]
    },
    {
        "id": "NHM_PRIMARY_COLD_01",
        "protocol": "NHM Community Health Worker Guidelines - Common Minor Ailments",
        "source": "National Health Mission - Ayushman Arogya Mandir Protocols",
        "page": 9,
        "category": "routine_homecare",
        "target_group": "all",
        "title_en": "Common Cold, Mild Sore Throat, and Day 1 Mild Illness",
        "content_en": (
            "Mild viral upper respiratory symptoms: runny nose, mild sore throat, occasional dry cough, low-grade fever < 100 F. "
            "Triage: HOME_CARE. "
            "Guidance: "
            "1. Take warm water, ginger/tulsi herbal tea, and steam inhalation. "
            "2. Frequent handwashing and adequate sleep. "
            "3. Red-flag watch: If breathing becomes difficult, chest pain arises, or fever persists beyond 3 days, visit a doctor."
        ),
        "content_hi": (
            "सामान्य जुकाम, हल्का गले में दर्द और घरेलू देखभाल: "
            "यदि केवल नाक बह रही है, हल्का गले में खराश है या 1 दिन से हल्का बुखार है बिना किसी खतरे के लक्षण के, "
            "तो यह सामान्य वायरल संक्रमण हो सकता है। "
            "घर पर पर्याप्त आराम करें, गुनगुना पानी पिएं, भाप लें और पौष्टिक आहार लें (HOME_CARE)। "
            "यदि 3 दिन बाद भी आराम न मिले या सांस लेने में परेशानी हो, तो डॉक्टर को दिखाएं।"
        ),
        "triage_urgency": "HOME_CARE",
        "keywords": ["common cold", "runny nose", "mild throat pain", "mild fever", "home care",
                     "जुकाम", "सर्दी", "नाक बहना", "हल्की खराश", "घरेलू देखभाल"]
    }
]

def main():
    target_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(target_dir, "processed_chunks", "guidelines_chunks.jsonl")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        for chunk in GUIDELINE_CHUNKS:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
            
    print(f"[SUCCESS] Compiled {len(GUIDELINE_CHUNKS)} clinical guideline chunks to: {output_file}")

if __name__ == "__main__":
    main()
