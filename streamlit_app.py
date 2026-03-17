import streamlit as st
import google.generativeai as genai
import math
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="أنداندي للطاقة الشمسية", page_icon="☀️", layout="wide")

# الربط مع جيمني (تجاوز خطأ 404)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = next((m for m in available_models if 'flash' in m), available_models[0])
        model = genai.GenerativeModel(model_name)
    except: model = None

# --- تصميم الهوية البصرية (أنداندي فوق) ---
st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%); padding: 30px; border-radius: 15px; border-top: 5px solid #f39c12; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.4);">
        <h1 style="color: #f39c12; margin: 0; font-size: 3em; font-family: 'Trebuchet MS'; letter-spacing: 2px;">ANDANDI</h1>
        <p style="color: #ecf0f1; font-size: 1.2em; margin-top: 5px; opacity: 0.9;">للحلول والأنظمة الشمسية المتكاملة</p>
    </div>
    """, unsafe_allow_html=True)

# --- قاعدة بيانات الأجهزة ---
appliance_cats = {
    "❄️ التبريد والتكييف": {"مكيف فريون": 1200, "مكيف نسمة": 250, "ثلاجة": 300, "ديب فريزر": 200},
    "🍳 أجهزة المطبخ": {"غلاية ماء": 2000, "ميكروويف": 1200, "سخان كهربائي": 1500, "خلاط": 400},
    "🏠 أحمال المنزل": {"شاشة LED": 120, "مروحة سقف": 80, "مكواة": 1500, "إنترنت": 30},
    "💦 مضخات وإنارة": {"مضخة 1 حصان": 750, "مضخة 0.5 حصان": 375, "إضاءة البيت": 150}
}

st.write("\n")
col_input, col_chart = st.columns([1, 1], gap="large")

with col_input:
    st.markdown("#### 🛠️ 1. اختيار الأجهزة")
    selected_items = {}
    tabs = st.tabs(list(appliance_cats.keys()))
    for i, cat in enumerate(appliance_cats.keys()):
        with tabs[i]:
            for name, watt in appliance_cats[cat].items():
                c1, c2 = st.columns([2, 1])
                if c1.checkbox(f"{name} ({watt}W)", key=f"c_{name}"):
                    count = c2.number_input(f"العدد", 1, 20, 1, key=f"v_{name}")
                    selected_items[name] = watt * count

total_load = sum(selected_items.values())

with col_chart:
    if total_load > 0:
        st.markdown("#### 📊 تحليل استهلاك النظام")
        df = pd.DataFrame(list(selected_items.items()), columns=['الجهاز', 'الواط'])
        st.bar_chart(df.set_index('الجهاز'), color="#f39c12")
    else:
        st.info("قم باختيار الأجهزة لعرض الرسم البياني للحمل.")

# --- الحسابات الهندسية ---
if total_load > 0:
    st.write("---")
    st.markdown("#### ⚙️ 2. مدخلات التصميم الفني")
    c1, c2, c3 = st.columns(3)
    with c1:
        night_h = st.slider("🌙 ساعات التشغيل ليلاً:", 1, 15, 6)
    with c2:
        v_sys = st.radio("⚡ جهد النظام (V):", [12, 24, 48], index=2, horizontal=True)
    with c3:
        margin = st.select_slider("🛡️ معامل الأمان:", options=[1.1, 1.2, 1.3], value=1.2, format_func=lambda x: f"{int((x-1)*100)}%")

    # معادلات م. أنداندي (محمد)
    inv = math.ceil((total_load * margin) / 500) * 500
    bat = math.ceil((total_load * night_h) / (v_sys * 0.5 * 0.85))
    pan = math.ceil(((total_load * 8) + (total_load * night_h)) / (550 * 5 * 0.65))

    st.markdown(f"""
        <div style="background-color: #2c3e50; padding: 12px; border-radius: 10px; border: 1px solid #f39c12; text-align: center; margin-bottom: 20px;">
            <h3 style="color: #f39c12; margin: 0;">الحمل المطلوب: {total_load} واط</h3>
        </div>
    """, unsafe_allow_html=True)

    res1, res2, res3 = st.columns(3)
    res1.metric("م. إنفيرتر (W)", f"{inv} W")
    res2.metric("م. بطاريات (Ah)", f"{bat} Ah")
    res3.metric("م. ألواح (550W)", f"{pan}")

    # --- التوصيات الفنية ---
    st.write("---")
    st.markdown("#### 💡 3. توصيات م. أنداندي للتركيب")
    exp1, exp2 = st.columns(2)
    with exp1:
        with st.expander("📍 توجيه المصفوفة"):
            st.write("- **الاتجاه:** جنوب جغرافي.")
            st.write("- **الميل:** 15-20 درجة.")
    with exp2:
        with st.expander("🔌 الكوابل والحماية"):
            st.write("- استخدم كابلات نحاسية معتمدة.")
            st.write("- تأكد من وجود قواطع DC للحماية.")

# --- التذييل والواتساب ---
st.write("\n\n")
wa_url = f"https://wa.me/249116284817?text=طلب استشارة فنية من م. أنداندي: حمل {total_load} واط"
st.markdown(f"""
    <style>
    .wa-float {{
        position: fixed; bottom: 20px; right: 20px; background-color: #25d366; color: white;
        border-radius: 50px; text-align: center; padding: 12px 18px; box-shadow: 2px 5px 15px rgba(0,0,0,0.3);
        z-index: 1000; text-decoration: none; font-weight: bold; font-size: 14px;
    }}
    </style>
    <a href="{wa_url}" class="wa-float" target="_blank">💬 تواصل مع م. أنداندي</a>
    <div style="text-align: center; color: #95a5a6; padding: 20px; font-size: 0.9em; border-top: 1px solid #34495e;">
        تصميم وإشراف: <b>م. أنداندي محمد عبد الهادي عيسى</b> <br>
        متخصص في هندسة القوى الكهربائية © 2026
    </div>
""", unsafe_allow_html=True)
        
