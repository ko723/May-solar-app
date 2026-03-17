import streamlit as st
import google.generativeai as genai
import math

# إعدادات الصفحة والتصميم
st.set_page_config(page_title="مستشارك الشمسي - م. محمد عبد الهادي", page_icon="☀️", layout="wide")

# الربط الذكي مع جيمني (تجاوز خطأ 404)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = next((m for m in available_models if 'flash' in m), available_models[0])
        model = genai.GenerativeModel(model_name)
    except:
        model = None
else:
    st.error("يرجى ضبط API Key في الإعدادات")

# --- تنسيق العنوان الفخم ---
st.markdown("""
    <div style="background-color: #0e1117; padding: 30px; border-radius: 20px; border: 2px solid #f39c12; text-align: center; box-shadow: 0px 10px 20px rgba(0,0,0,0.3);">
        <h1 style="color: #f39c12; margin-bottom: 5px; font-size: 2.5em;">☀️ المصمم الشمسي الهندسي</h1>
        <p style="color: #ffffff; font-size: 1.4em;">بواسطة المهندس: <span style="color: #f39c12;"><b>محمد عبد الهادي عيسى مختار</b></span></p>
        <p style="color: #888888;">خبير أنظمة الطاقة المتجددة وقوى الكهرباء</p>
    </div>
    """, unsafe_allow_html=True)

st.write("\n")

# --- مجمع الأجهزة والأيقونات ---
appliance_cats = {
    "❄️ التبريد والتكييف": {
        "مكيف فريون (12000 BTU) 🧊": 1200, "مكيف نسمة (موية) 🌬️": 250, "ثلاجة منزلية ⛄": 300, "ديب فريزر 🧊": 200, "مبرد مياه 💧": 500
    },
    "🍳 أدوات المطبخ": {
        "غلاية ماء (Kettle) ☕": 2000, "ماكينة قهوة ☕": 1000, "ميكروويف 🍲": 1200, "خلاط 🌪️": 400, "هيتير كهربائي 🔥": 1500
    },
    "🏠 أجهزة منزلية وعامة": {
        "شاشة LED كبيرة 📺": 120, "مروحة سقف 🌀": 80, "مروحة عمود 🌀": 60, "مكواة ملابس 💨": 1500, "كمبيوتر 💻": 250, "إنترنت مودم 📡": 30
    },
    "💦 مضخات وإنارة": {
        "مضخة مياه (0.5 حصان) 🚰": 375, "مضخة مياه (1 حصان) 🚰": 750, "كشاف خارجي 💡": 50, "إضاءة البيت كاملة 💡": 150
    }
}

# --- اختيار الأحمال ---
st.markdown("### 🛠️ 1. حدد أجهزتك الكهربائية")
selected_appliances = []

tabs = st.tabs(list(appliance_cats.keys()) + ["➕ جهاز غير موجود"])

for i, category in enumerate(appliance_cats.keys()):
    with tabs[i]:
        cols = st.columns(2)
        for j, (name, watt) in enumerate(appliance_cats[category].items()):
            col_idx = j % 2
            if cols[col_idx].checkbox(f"{name} ({watt}W)", key=name):
                count = cols[col_idx].number_input(f"عدد {name}", min_value=1, value=1, key=f"cnt_{name}")
                selected_appliances.append((name, watt, count))

with tabs[-1]:
    c_name = st.text_input("اسم الجهاز الجديد:")
    c_watt = st.number_input("القدرة (واط):", min_value=0, value=0)
    c_count = st.number_input("الكمية:", min_value=1, value=1, key="custom_cnt")
    if c_name and c_watt > 0:
        if st.checkbox(f"إضافة {c_name} للقائمة"):
            selected_appliances.append((c_name, c_watt, c_count))

# --- حسابات النظام ---
total_load = sum([item[1] * item[2] for item in selected_appliances])

if total_load > 0:
    st.write("---")
    c1, c2 = st.columns(2)
    with c1:
        night_hours = st.select_slider("🌙 كم ساعة تريد التشغيل من البطاريات ليلاً؟", options=list(range(1, 17)), value=6)
    with c2:
        system_volt = st.radio("⚡ فولتية النظام الموصى بها:", [12, 24, 48], index=2, horizontal=True)

    # المعادلات الهندسية (مع مراعاة الكفاءة والفاقد في السودان)
    inv_size = math.ceil((total_load * 1.3) / 500) * 500
    daily_energy_night = total_load * night_hours
    battery_ah = math.ceil((daily_energy_night) / (system_volt * 0.5 * 0.8)) # 0.8 كفاءة تحويل
    num_panels = math.ceil((total_load * 8 + daily_energy_night) / (550 * 5 * 0.65)) # 0.65 كفاءة لوح وحرارة

    # --- النتائج بصورة احترافية ---
    st.markdown("## 📊 نتائج التصميم الفني")
    r1, r2, r3 = st.columns(3)
    r1.metric("حجم الإنفيرتر", f"{inv_size} W")
    r2.metric("سعة البطاريات", f"{battery_ah} Ah")
    r3.metric("عدد الألواح (550W)", f"{num_panels}")

    # --- التقرير والواتساب ---
    whatsapp_num = "249116284817"
    whatsapp_link = f"https://wa.me/{whatsapp_num}?text=مرحباً بشمهندس محمد، قمت بعمل تصميم لحمل {total_load} واط وأرغب في تنفيذ النظام."
    
    st.write("\n")
    st.markdown(f'''
        <a href="{whatsapp_link}" target="_blank">
            <button style="width:100%; background-color:#25D366; color:white; border:none; padding:15px; border-radius:15px; font-weight:bold; font-size:1.2em; cursor:pointer;">
                💬 إرسال النتائج للمهندس محمد عبد الهادي (واتساب)
            </button>
        </a>
        ''', unsafe_allow_html=True)
    
    if st.button("✨ استشارة إضافية من ذكاء جيمني"):
        if model:
            with st.spinner('جاري تحليل الأحمال...'):
                prompt = f"أنا المهندس محمد عبد الهادي، العميل اختار أحمال قيمتها {total_load} واط. وجه له نصيحة سودانية حول جودة البطاريات والأسلاك."
                response = model.generate_content(prompt)
                st.info(response.text)
else:
    st.info("قم باختيار الأجهزة من الأعلى لعرض الحسابات الهندسية.")

st.write("\n\n")
st.caption("تم التطوير بواسطة م. محمد عبد الهادي عيسى © 2026 | جميع الحقوق محفوظة")
