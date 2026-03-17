import streamlit as st
import google.generativeai as genai
import math
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="أنداندي للطاقة الشمسية", page_icon="☀️", layout="wide")

# الربط مع جيمني
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = next((m for m in available_models if 'flash' in m), available_models[0])
        model = genai.GenerativeModel(model_name)
    except: model = None

# --- تصميم الهوية البصرية (أنداندي فوق عربي وإنجليزي) ---
st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%); padding: 30px; border-radius: 15px; border-top: 5px solid #f39c12; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.4);">
        <h1 style="color: #f39c12; margin: 0; font-size: 3.5em; font-family: 'Trebuchet MS'; letter-spacing: 3px; line-height: 1;">ANDANDI</h1>
        <p style="color: #f39c12; font-size: 1.2em; margin: 0; font-family: 'Arial'; font-weight: bold;">أنداندي</p>
        <p style="color: #ecf0f1; font-size: 1.1em; margin-top: 10px; opacity: 0.8; letter-spacing: 1px;">لحلول الطاقة المتكاملة والأنظمة الذكية</p>
    </div>
    """, unsafe_allow_html=True)

# --- قاعدة بيانات الأجهزة ---
appliance_cats = {
    "❄️ التبريد": {"مكيف فريون": 1200, "مكيف نسمة": 250, "ثلاجة": 300, "ديب فريزر": 200},
    "🍳 المطبخ": {"غلاية ماء": 2000, "ميكروويف": 1200, "سخان كهربائي": 1500, "خلاط": 400},
    "🏠 المنزل": {"شاشة LED": 120, "مروحة سقف": 80, "مكواة": 1500, "إنترنت": 30},
    "💦 أخرى": {"مضخة 1 حصان": 750, "مضخة 0.5 حصان": 375, "إضاءة البيت": 150}
}

st.write("\n")
selected_items = {}
st.markdown("### 🛠️ 1. اختيار الأحمال")
tabs = st.tabs(list(appliance_cats.keys()) + ["➕ إضافة جهاز مخصص"])

for i, cat in enumerate(appliance_cats.keys()):
    with tabs[i]:
        cols = st.columns(2)
        for j, (name, watt) in enumerate(appliance_cats[cat].items()):
            if cols[j % 2].checkbox(f"{name} ({watt}W)", key=f"c_{name}"):
                count = cols[j % 2].number_input(f"العدد", 1, 20, 1, key=f"v_{name}")
                selected_items[name] = watt * count

with tabs[-1]:
    c_name = st.text_input("اسم الجهاز:")
    c_watt = st.number_input("القدرة (W):", 0, 5000, 0)
    c_num = st.number_input("الكمية:", 1, 20, 1)
    if c_name and c_watt > 0 and st.checkbox(f"تأكيد {c_name}"):
        selected_items[c_name] = c_watt * c_num

total_load = sum(selected_items.values())

if total_load > 0:
    st.markdown(f"""<div style="background-color: #2c3e50; padding: 10px; border-radius: 10px; border: 1px solid #f39c12; text-align: center; margin-top: 15px;">
        <h3 style="color: #f39c12; margin: 0;">الحمل التصميمي: {total_load} واط</h3></div>""", unsafe_allow_html=True)

    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1: night_h = st.slider("🌙 تشغيل ليلي (ساعة):", 1, 15, 6)
    with c2: v_sys = st.radio("⚡ جهد النظام:", [12, 24, 48], index=2, horizontal=True)
    with c3: cost_kwh = st.number_input("💸 سعر الكيلوواط (اختياري):", 0, 500, 100)

    # الحسابات الهندسية
    inv = math.ceil((total_load * 1.25) / 500) * 500
    bat = math.ceil((total_load * night_h) / (v_sys * 0.5 * 0.85))
    pan = math.ceil(((total_load * 8) + (total_load * night_h)) / (550 * 5 * 0.65))

    st.markdown("#### 📊 نتائج التصميم")
    r1, r2, r3 = st.columns(3)
    r1.metric("م. إنفيرتر", f"{inv} W")
    r2.metric("م. بطاريات", f"{bat} Ah")
    r3.metric("م. ألواح", f"{pan}")

    # --- ميزة خرافية: حاسبة التوفير ---
    st.write("---")
    st.markdown("#### 💰 2. الجدوى الاقتصادية")
    monthly_save = (total_load * 12 * 30 / 1000) * cost_kwh
    st.success(f"توفيرك الشهري المتوقع هو حوالي **{monthly_save:,.0f} جنيه سوداني** (بناءً على 12 ساعة تشغيل)")

    # --- توصيات التركيب ---
    st.write("---")
    st.markdown("#### 💡 3. توصيات م. محمد للتركيب")
    e1, e2 = st.columns(2)
    with e1:
        with st.expander("📍 زوايا الميل"):
            st.write("يفضل ميل 15 درجة شتاءً و10 درجات صيفاً في السودان.")
    with e2:
        with st.expander("🛡️ الحماية"):
            st.write("يجب تركيب مانع صواعق (Surge Arrestor) لحماية الإنفيرتر.")

# --- قسم معرض الأعمال (كيف تضيف أعمالك) ---
st.write("---")
st.markdown("### 🏢 معرض أعمال م. محمد (أنداندي)")
st.info("💡 لإضافة صورك الخاصة: ارفع الصور على GitHub في مجلد اسمه images ثم استبدل الروابط أدناه بأسماء صورك.")

work_cols = st.columns(3)
# مثال لصور أعمال (يمكنك استبدال الروابط بصور حقيقية لمشاريعك)
with work_cols[0]:
    st.image("https://images.unsplash.com/photo-1509391366360-fe5bb626582f?w=400", caption="تركيب مصفوفة 12 لوح - كاريما")
with work_cols[1]:
    st.image("https://images.unsplash.com/photo-1548337138-e87d889cc369?w=400", caption="بنك بطاريات ليثيوم 48 فولت")
with work_cols[2]:
    st.image("https://images.unsplash.com/photo-1613665813446-82a78c468a1d?w=400", caption="نظام تشغيل مكيفات فريون")

# --- التذييل والواتساب الجانبي ---
st.write("\n\n")
wa_url = f"https://wa.me/249116284817?text=استشارة فنية من م. محمد: حمل {total_load} واط"
st.markdown(f"""
    <style>
    .wa-float {{ position: fixed; bottom: 20px; right: 20px; background-color: #25d366; color: white;
        border-radius: 50px; text-align: center; padding: 12px 18px; box-shadow: 2px 5px 15px rgba(0,0,0,0.3);
        z-index: 1000; text-decoration: none; font-weight: bold; font-size: 14px; }}
    </style>
    <a href="{wa_url}" class="wa-float" target="_blank">💬 تواصل مع م. محمد</a>
    <div style="text-align: center; color: #95a5a6; padding: 20px; font-size: 0.9em; border-top: 1px solid #34495e;">
        إشراف وتصميم: <b>م. محمد عبد الهادي عيسى</b> <br>
        © 2026 جميع الحقوق محفوظة لـ <b>ANDANDI</b>
    </div>
""", unsafe_allow_html=True)
