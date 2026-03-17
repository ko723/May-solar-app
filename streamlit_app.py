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

# --- تصميم الهوية البصرية (أنداندي فوق) ---
st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%); padding: 30px; border-radius: 15px; border-top: 5px solid #f39c12; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.4);">
        <h1 style="color: #f39c12; margin: 0; font-size: 3em; font-family: 'Trebuchet MS'; letter-spacing: 2px;">ANDANDI</h1>
        <p style="color: #ecf0f1; font-size: 1.2em; margin-top: 5px; opacity: 0.9;">للحلول والأنظمة الشمسية المتكاملة</p>
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
st.markdown("#### 🛠️ 1. خطوة التصميم: اختر الأحمال والكمية")
selected_items = {}
tabs = st.tabs(list(appliance_cats.keys()) + ["➕ إضافة جهاز مخصص"])
for i, cat in enumerate(appliance_cats.keys()):
    with tabs[i]:
        cols = st.columns(2)
        for j, (name, watt) in enumerate(appliance_cats[cat].items()):
            col_idx = j % 2
            if cols[col_idx].checkbox(f"{name} ({watt}W)", key=f"c_{name}"):
                count = cols[col_idx].number_input(f"العدد", 1, 20, 1, key=f"v_{name}")
                selected_items[name] = watt * count

with tabs[-1]:
    c_name = st.text_input("اسم الجهاز الجديد:")
    c_watt = st.number_input("القدرة (W):", min_value=0, value=0)
    c_num = st.number_input("الكمية:", min_value=1, value=1)
    if c_name and c_watt > 0 and st.checkbox(f"تأكيد إضافة {c_name}"):
        selected_items[c_name] = c_watt * c_num

# --- حساب الإجمالي الفوري ---
total_load = sum(selected_items.values())
if total_load > 0:
    st.markdown(f"""
        <div style="background-color: #2c3e50; padding: 12px; border-radius: 10px; border: 1px solid #f39c12; text-align: center; margin-top: 20px;">
            <h3 style="color: #f39c12; margin: 0;">إجمالي الحمل المطلوب: {total_load} واط</h3>
        </div>
    """, unsafe_allow_html=True)

    st.write("---")
    c1, c2, c3 = st.columns(3)
    with c1: night_h = st.slider("🌙 ساعات التشغيل ليلاً:", 1, 15, 6)
    with c2: v_sys = st.radio("⚡ جهد النظام (V):", [12, 24, 48], index=2, horizontal=True)
    with c3: margin = st.select_slider("🛡️ معامل الأمان:", options=[1.1, 1.2, 1.3], value=1.2, format_func=lambda x: f"{int((x-1)*100)}%")

    # معادلات م. محمد (أنداندي)
    inv = math.ceil((total_load * margin) / 500) * 500
    bat = math.ceil((total_load * night_h) / (v_sys * 0.5 * 0.85))
    pan = math.ceil(((total_load * 8) + (total_load * night_h)) / (550 * 5 * 0.65))

    st.markdown("#### 📊 التقرير الفني المبدئي")
    r1, r2, r3 = st.columns(3)
    r1.metric("م. إنفيرتر (W)", f"{inv} W")
    r2.metric("م. بطاريات (Ah)", f"{bat} Ah")
    r3.metric("م. ألواح (550W)", f"{pan}")

    # --- ميزة مثيرة 1: الرسم البياني الذكي ---
    st.write("---")
    st.markdown("#### 🔄 2. توزيع الطاقة (Dashboard)")
    load_energy = total_load / 1000 # الواط
    bat_energy = (bat * v_sys) / 1000 # كيلوواط ساعة
    pan_energy = (pan * 550) / 1000 # كيلوواط ساعة للوح
    energy_dist = {"الحمل المباشر (kW)": load_energy, "طاقة المصفوفة الشمسية (kW)": pan_energy, "سعة التخزين (kWh)": bat_energy}
    
    col1, col2 = st.columns([1, 1], gap="large")
    with col1:
        st.write("- **الأحمال:** كيلوواط")
        st.write("- **المصفوفة:** كيلوواط")
        st.write("- **البطاريات:** كيلوواط ساعة")
        df_dist = pd.DataFrame(list(energy_dist.items()), columns=['النوع', 'القيمة'])
        st.bar_chart(df_dist.set_index('النوع'), color="#f39c12")
    with col2:
        st.info("يوضح هذا الرسم توزيع طاقة النظام. تأكد أن طاقة المصفوفة أكبر من الأحمال المباشرة لضمان شحن البطاريات.")

    # --- التوصيات الفنية وجيمني ---
    st.write("---")
    st.markdown("#### 💡 3. توصيات م. محمد للتركيب")
    exp1, exp2 = st.columns(2)
    with exp1:
        with st.expander("📍 توجيه المصفوفة الشمسية"):
            st.write("- **الاتجاه:** جنوب جغرافي.")
            st.write("- **الميل:** 15-20 درجة.")
            st.write("- **التظليل:** تأكد من عدم وجود تظليل.")
    with exp2:
        with st.expander("🔌 الكوابل والحماية"):
            st.write("- كوابل نحاسية DC معتمدة.")
            st.write("- قواطع حماية DC مناسبة.")
            st.write("- توصيل الألواح: انتبه لتوافقه مع جهد الإنفيرتر.")

    st.write("\n")
    if st.button("✨ استشارة جيمني الذكية حول التوصيل"):
        if model:
            with st.spinner('جاري التحليل...'):
                res = model.generate_content(f"بصفتك مهندس سوداني، انصح العميل حول ترتيب توصيل الألواح {pan} لوح لنظام {v_sys} فولت.")
                st.info(res.text)

# --- ميزة مثيرة 2: معرض أعمال م. محمد ---
st.write("---")
with st.expander("🏢 معرض أعمال م. محمد (أنظمة سابقة)"):
    st.write("هنا يمكنك إضافة صور لمشاريعك السابقة لتبرز جودة عملك.")
    st.image("https://images.unsplash.com/photo-1594917633215-a7442f4c4786?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwxfDB8MXxyYW5kb218MHx8c29sYXIgaW5zdGFsbGF0aW9ufHx8fHx8MTY5MzYxNTUyMQ&ixlib=rb-4.0.3&q=80&w=400", caption="مشروع نظام شمسي متكامل")

# --- التذييل والواتساب الجانبي ---
st.write("\n\n")
wa_url = f"https://wa.me/249116284817?text=طلب استشارة فنية من م. محمد: حمل {total_load} واط"
st.markdown(f"""
    <style>
    .wa-float {{
        position: fixed; bottom: 20px; right: 20px; background-color: #25d366; color: white;
        border-radius: 50px; text-align: center; padding: 12px 18px; box-shadow: 2px 5px 15px rgba(0,0,0,0.3);
        z-index: 1000; text-decoration: none; font-weight: bold; font-size: 14px;
    }}
    </style>
    <a href="{wa_url}" class="wa-float" target="_blank">💬 تواصل مع م. محمد عبد الهادي</a>
    <div style="text-align: center; color: #95a5a6; padding: 20px; font-size: 0.9em; border-top: 1px solid #34495e;">
        تصميم وإشراف: <b>م. محمد عبد الهادي عيسى</b> <br>
        تطوير وبرمجة © 2026 جميع الحقوق محفوظة
    </div>
""", unsafe_allow_html=True)
    
