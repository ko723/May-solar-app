import streamlit as st
import google.generativeai as genai
import math

# إعدادات الصفحة
st.set_page_config(page_title="أنداندي - أوفلاين", page_icon="☀️", layout="wide")

# الربط مع جيمني (سيعمل فقط في حال وجود إنترنت)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-1.5-flash')
    else: model = None
except: model = None

# الهوية البصرية
st.markdown("""
    <style>
    .main-box {
        background: linear-gradient(135deg, #000 0%, #2c3e50 100%);
        padding: 30px; border-radius: 20px; text-align: center;
        border-bottom: 5px solid #f39c12; margin-bottom: 20px;
    }
    .brand-eng { color: #f39c12; font-size: 3.5em; font-family: 'Arial Black'; margin: 0; }
    .load-badge {
        background-color: #f39c12; color: black; padding: 10px 20px;
        border-radius: 50px; font-size: 1.5em; font-weight: bold; display: inline-block;
    }
    </style>
    <div class="main-box">
        <h1 class="brand-eng">ANDANDI</h1>
        <p style="color: #f39c12; font-size: 1.2em; font-weight: bold;">أنداندي للأنظمة الذكية</p>
    </div>
    """, unsafe_allow_html=True)

# القائمة الرئيسية
system_type = st.selectbox("نوع النظام:", ["🏠 منزلي", "🌾 زراعي", "🏭 صناعي"])

if "🏠" in system_type:
    st.subheader("📋 حساب الأحمال المنزلية")
    # (هنا توضع قائمة الأحمال التي برمجناها سابقاً)
    # ملاحظة: المعادلات الرياضية هنا تعمل أوفلاين تماماً
    load = st.number_input("أدخل إجمالي الأحمال يدوياً (W) أو اختر من القائمة:", 0, 50000, 1000)
    
    st.markdown(f'<div style="text-align:center"><div class="load-badge">⚡ {load} W</div></div>', unsafe_allow_html=True)
    
    v = st.selectbox("جهد النظام:", [12, 24, 48], index=2)
    h = st.slider("ساعات التشغيل ليلاً:", 1, 15, 6)
    
    # حسابات البطاريات (أوفلاين)
    bats = math.ceil((load * h) / (v * 0.6 * 200))
    if v == 48: bats = math.ceil(bats/4)*4
    
    st.success(f"النتيجة: تحتاج {bats} بطارية (200Ah)")

# حقوق الملكية (Footer)
st.markdown("""
    <div style="text-align: center; margin-top: 50px; border-top: 1px solid #444; padding: 20px;">
        <p style="color: #f39c12; font-weight: bold;">ANDANDI © 2026</p>
        <p style="color: #888; font-size: 0.9em;">جميع الحقوق محفوظة | م. محمد عبد الهادي عيسى</p>
    </div>
    """, unsafe_allow_html=True)
