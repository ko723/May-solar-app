import streamlit as st
import google.generativeai as genai
import math

# إعدادات الصفحة
st.set_page_config(page_title="مستشارك الشمسي", page_icon="☀️", layout="wide")

# الربط الذكي مع جيمني
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = next((m for m in available_models if 'flash' in m), available_models[0])
        model = genai.GenerativeModel(model_name)
    except:
        model = None

# --- تنسيق العنوان بدون الاسم ---
st.markdown("""
    <div style="background-color: #0e1117; padding: 15px; border-radius: 10px; border-bottom: 3px solid #f39c12; text-align: center;">
        <h2 style="color: #f39c12; margin: 0;">☀️ المصمم الشمسي الآلي</h2>
    </div>
    """, unsafe_allow_html=True)

# --- قاعدة بيانات الأجهزة ---
appliance_cats = {
    "❄️ التبريد": {"مكيف فريون": 1200, "مكيف نسمة": 250, "ثلاجة": 300, "ديب فريزر": 200},
    "🍳 المطبخ": {"غلاية ماء": 2000, "ميكروويف": 1200, "سخان كهربائي": 1500},
    "🏠 المنزل": {"شاشة LED": 120, "مروحة سقف": 80, "مكواة": 1500, "إنترنت": 30},
    "💦 أخرى": {"مضخة 1 حصان": 750, "إضاءة البيت": 150}
}

st.write("\n")
st.markdown("##### 🛠️ اختر الأجهزة والكمية")

selected_items = {}

# عرض الأجهزة في تبويبات
tabs = st.tabs(list(appliance_cats.keys()) + ["➕ جهاز مخصص"])

for i, cat in enumerate(appliance_cats.keys()):
    with tabs[i]:
        cols = st.columns(2)
        for j, (name, watt) in enumerate(appliance_cats[cat].items()):
            c_idx = j % 2
            with cols[c_idx]:
                if st.checkbox(f"{name} ({watt}W)", key=f"chk_{name}"):
                    count = st.number_input(f"العدد", 1, 20, 1, key=f"num_{name}")
                    selected_items[name] = watt * count

with tabs[-1]:
    c_name = st.text_input("اسم الجهاز:")
    c_watt = st.number_input("الواط:", 0, 5000, 0)
    c_num = st.number_input("الكمية:", 1, 20, 1)
    if c_name and c_watt > 0:
        selected_items[c_name] = c_watt * c_num

# --- عرض الإجمالي المنسق ---
total_load = sum(selected_items.values())
if total_load > 0:
    st.markdown(f"""
        <div style="background-color: #2c3e50; padding: 10px; border-radius: 8px; text-align: center; border: 1px solid #f39c12;">
            <span style="color: #f39c12; font-size: 1.2em; font-weight: bold;">إجمالي الحمل: {total_load} واط</span>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        night_h = st.slider("🌙 ساعات التشغيل ليلاً:", 1, 15, 6)
    with col_v2:
        v_sys = st.radio("⚡ فولتية النظام:", [12, 24, 48], index=2, horizontal=True)

    # الحسابات الهندسية
    inv = math.ceil((total_load * 1.25) / 500) * 500
    bat = math.ceil((total_load * night_h) / (v_sys * 0.5 * 0.8))
    pan = math.ceil(((total_load * 8) + (total_load * night_h)) / (550 * 5 * 0.65))

    st.markdown("#### 📊 التقرير الفني المبدئي")
    r1, r2, r3 = st.columns(3)
    r1.metric("الإنفيرتر", f"{inv} W")
    r2.metric("البطاريات", f"{bat} Ah")
    r3.metric("الألواح", f"{pan}")

# --- أيقونة الواتساب والاسم في الأسفل ---
st.write("\n\n")
st.write("---")

whatsapp_url = f"https://wa.me/249116284817?text=طلب استشارة: حمل {total_load} واط"

# كود HTML للأيقونة الجانبية والاسم المنسق
st.markdown(f"""
    <style>
    .floating-whatsapp {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #25d366;
        color: white;
        border-radius: 50px;
        text-align: center;
        padding: 10px 15px;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        z-index: 100;
        text-decoration: none;
        font-size: 14px;
        font-weight: bold;
    }}
    .footer-name {{
        text-align: center;
        color: #7f8c8d;
        font-size: 0.9em;
        margin-top: 20px;
    }}
    </style>
    
    <a href="{whatsapp_url}" class="floating-whatsapp" target="_blank">
        💬 واتساب الدعم
    </a>
    
    <div class="footer-name">
        تطوير وتصميم المهندس: <b>محمد عبد الهادي عيسى مختار</b> <br>
        © 2026 جميع الحقوق محفوظة
    </div>
""", unsafe_allow_html=True)
