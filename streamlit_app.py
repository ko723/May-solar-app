import streamlit as st
import google.generativeai as genai
import math

# إعدادات الصفحة
st.set_page_config(page_title="مستشارك الشمسي - م. محمد عبد الهادي", page_icon="☀️", layout="wide")

# الربط الذكي مع جيمني
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = next((m for m in available_models if 'flash' in m), available_models[0])
        model = genai.GenerativeModel(model_name)
    except:
        model = None
else:
    st.error("يرجى ضبط API Key في Secrets")

# --- تنسيق العنوان ---
st.markdown("""
    <div style="background-color: #0e1117; padding: 20px; border-radius: 15px; border: 2px solid #f39c12; text-align: center;">
        <h2 style="color: #f39c12; margin: 0;">⚡ المصمم الشمسي الهندسي</h2>
        <p style="color: #ffffff; margin: 5px 0 0 0;">المهندس: <b>محمد عبد الهادي عيسى مختار</b></p>
    </div>
    """, unsafe_allow_html=True)

# --- قاعدة بيانات الأجهزة ---
appliance_cats = {
    "❄️ التبريد": {"مكيف فريون": 1200, "مكيف نسمة": 250, "ثلاجة": 300, "ديب فريزر": 200},
    "🍳 المطبخ": {"غلاية ☕": 2000, "ماكينة قهوة": 1000, "ميكروويف": 1200, "سخان": 1500},
    "🏠 المنزل": {"شاشة LED": 120, "مروحة سقف": 80, "مروحة عمود": 60, "مكواة": 1500, "إنترنت": 30},
    "💦 أخرى": {"مضخة 1 حصان": 750, "مضخة 0.5 حصان": 375, "إضاءة": 150}
}

st.write("\n")
st.markdown("### 🛠️ 1. اختر الأجهزة والكمية")

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
                    count = st.number_input(f"العدد لـ {name}", 1, 50, 1, key=f"num_{name}")
                    selected_items[name] = watt * count

with tabs[-1]:
    c_name = st.text_input("اسم الجهاز:")
    c_watt = st.number_input("الواط:", 0, 5000, 0)
    c_num = st.number_input("الكمية:", 1, 50, 1, key="c_num")
    if c_name and c_watt > 0:
        selected_items[c_name] = c_watt * c_num

# --- عرض الإجمالي تحت الاختيارات مباشرة ---
total_load = sum(selected_items.values())
if total_load > 0:
    st.markdown(f"""
        <div style="background-color: #f39c12; padding: 10px; border-radius: 10px; text-align: center; margin-top: 20px;">
            <h3 style="color: #000; margin: 0;">إجمالي الحمل الحالي: {total_load} واط</h3>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")
    col_v1, col_v2 = st.columns(2)
    with col_v1:
        night_h = st.slider("🌙 ساعات التشغيل الليلي:", 1, 15, 6)
    with col_v2:
        v_sys = st.radio("⚡ فولتية النظام:", [12, 24, 48], index=2, horizontal=True)

    # الحسابات
    inv = math.ceil((total_load * 1.3) / 500) * 500
    bat = math.ceil((total_load * night_h) / (v_sys * 0.5 * 0.8))
    pan = math.ceil(((total_load * 8) + (total_load * night_h)) / (550 * 5 * 0.65))

    st.markdown("### 📊 التقرير الفني")
    r1, r2, r3 = st.columns(3)
    r1.metric("الإنفيرتر", f"{inv} W")
    r2.metric("البطاريات", f"{bat} Ah")
    r3.metric("الألواح (550W)", f"{pan}")

    if st.button("✨ استشارة ذكية"):
        if model:
            res = model.generate_content(f"بصفتك مهندس سوداني، انصح العميل الذي لديه حمل {total_load} واط.")
            st.info(res.text)

# --- تذييل الصفحة (واتساب) ---
st.write("\n\n")
st.write("---")
w_link = f"https://wa.me/249116284817?text=استشارة فنية: حمل {total_load} واط"
st.markdown(f"""
    <div style="text-align: center;">
        <p style="margin-bottom: 5px;">للتواصل والدعم الفني المباشر:</p>
        <a href="{w_link}" target="_blank">
            <button style="background-color: #25D366; color: white; border: none; padding: 8px 15px; border-radius: 20px; cursor: pointer; font-size: 0.9em;">
                💬 مراسلة المهندس محمد عبد الهادي
            </button>
        </a>
    </div>
""", unsafe_allow_html=True)

st.caption("<p style='text-align: center;'>تم التطوير بواسطة م. محمد عبد الهادي عيسى © 2026</p>", unsafe_allow_html=True)
