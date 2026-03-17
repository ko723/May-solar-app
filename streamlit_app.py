import streamlit as st
import google.generativeai as genai
import math
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="أنداندي للطاقة الشمسية", page_icon="☀️", layout="wide")

# 2. الربط مع جيمني
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except: model = None
else: model = None

# 3. الهوية البصرية (أنداندي فوق وتحتها أنداندي بالعربي)
st.markdown("""
    <div style="background: linear-gradient(135deg, #000000 0%, #2c3e50 100%); padding: 30px; border-radius: 20px; text-align: center; border-bottom: 5px solid #f39c12;">
        <h1 style="color: #f39c12; margin: 0; font-size: 3.5em; font-family: 'Arial Black';">ANDANDI</h1>
        <p style="color: #f39c12; font-size: 1.5em; margin: 0; font-weight: bold;">أنداندي</p>
        <p style="color: white; opacity: 0.8; margin-top: 10px;">المنصة الهندسية المتكاملة | م. محمد عبد الهادي عيسى</p>
    </div>
    """, unsafe_allow_html=True)

st.write("\n")

# 4. اختيار نوع المنظومة (القائمة القديمة)
st.markdown("### 📋 اختر نوع النظام المطلوب تصميمه")
system_type = st.radio("نوع المنظومة:", ["🏠 منزلي / سكني", "🌾 زراعي (طلمبات ري)", "🏭 صناعي (ورش ومصانع)"], horizontal=True)

st.write("---")

# ==================== القسم السكني (قائمة أحمال شاملة) ====================
if system_type == "🏠 منزلي / سكني":
    st.subheader("🛠️ تحديد أحمال المنزل")
    appliance_cats = {
        "❄️ التبريد": {"مكيف فريون 1.5 حصان": 1500, "مكيف نسمة / ماء": 250, "ثلاجة كبيرة": 300, "ديب فريزر": 250, "مبرد مادة": 150},
        "🏠 الأجهزة العامة": {"مروحة سقف": 80, "شاشة LED": 120, "إضاءة البيت (كاملة)": 200, "راوتر إنترنت": 30, "ريسيفر": 50},
        "🍳 المطبخ والحرارة": {"غلاية ماء": 2000, "ميكروويف": 1200, "خلاط": 400, "مكواة": 1500, "سخان كهربائي": 1500},
        "💦 أخرى": {"مضخة ماء منزلية": 750, "غسالة ملابس": 500, "مكنسة كهربائية": 1400}
    }
    
    selected_items = {}
    col_a, col_b = st.columns(2)
    
    # توزيع القوائم على عمودين
    for i, (cat, items) in enumerate(appliance_cats.items()):
        target_col = col_a if i % 2 == 0 else col_b
        with target_col:
            st.markdown(f"**{cat}**")
            for name, watt in items.items():
                if st.checkbox(f"{name} ({watt}W)", key=f"check_{name}"):
                    count = st.number_input(f"عدد {name}", 1, 50, 1, key=f"num_{name}")
                    selected_items[name] = watt * count

    total_load = sum(selected_items.values())
    
    if total_load > 0:
        st.markdown(f"### إجمالي الحمل المطلوب: {total_load} واط")
        c1, c2 = st.columns(2)
        night_h = c1.slider("ساعات التشغيل ليلاً:", 1, 15, 6)
        v_sys = c2.
        
