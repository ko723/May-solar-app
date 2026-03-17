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
        model = genai.GenerativeModel('gemini-1.5-flash')
    except: model = None

# --- تصميم الهوية البصرية الفخم (ANDANDI) ---
st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(135deg, #000000 0%, #2c3e50 100%);
        padding: 40px;
        border-radius: 20px;
        border-right: 10px solid #f39c12;
        text-align: center;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5);
    }
    .brand-eng { color: #f39c12; font-size: 4em; font-family: 'Arial Black'; margin: 0; line-height: 1; }
    .brand-arb { color: #f39c12; font-size: 1.5em; margin: 0; font-weight: bold; }
    </style>
    <div class="main-header">
        <h1 class="brand-eng">ANDANDI</h1>
        <p class="brand-arb">أنداندي للأنظمة الذكية</p>
        <p style="color: white; opacity: 0.8; margin-top: 15px;">المنصة الهندسية المتكاملة | م. محمد عبد الهادي عيسى</p>
    </div>
    """, unsafe_allow_html=True)

st.write("\n")

# --- الأقسام الرئيسية ---
tabs = st.tabs(["⚡ حاسبة الأحمال", "🚜 مزارع أنداندي", "⚙️ المختبر الهندسي", "🛡️ الصيانة والضمان"])

# 1. حاسبة الأحمال (المنزلي والصناعي)
with tabs[0]:
    st.subheader("🏠 تصميم المنظومة السكنية والصناعية")
    col_l, col_r = st.columns([2, 1])
    with col_l:
        st.markdown("##### اختر أجهزتك:")
        c1, c2 = st.columns(2)
        ac = c1.number_input("مكيفات فريون (1.5 HP):", 0, 20, 0)
        fridge = c2.number_input("ثلاجات / ديب فريزر:", 0, 10, 1)
        fans = c1.number_input("مراوح سقف:", 0, 50, 4)
        lights = c2.number_input("لمبات إضاءة:", 0, 100, 10)
        
        total_w = (ac * 1500) + (fridge * 300) + (fans * 80) + (lights * 15)
    
    with col_r:
        st.markdown("##### ملخص النظام:")
        st.metric("إجمالي الحمل الحالي", f"{total_w} W")
        v_sys = st.selectbox("جهد النظام الموصى به:", [24, 48], index=1)
        inv_size = math.ceil((total_w * 1.3) / 1000)
        st.info(f"تحتاج إنفيرتر بقدرة {inv_size} كيلوواط.")

# 2. مزارع أنداندي (الري الزراعي المتطور)
with tabs[1]:
    st.subheader("🚜 تصميم ري المزارع")
    st.info("حسابات دقيقة للطلمبات الغاطسة والسطحية.")
    col1, col2 = st.columns(2)
    with col1:
        acres = st.number_input("عدد الفدادين المطلوب ريها:", 1, 500, 5)
        hp = math.ceil(acres * 1.2) # معادلة تقديرية للحصان لكل فدان
        pump_hours = st.slider("ساعات التشغيل اليومية:", 1, 10, 6)
    
    with col2:
        water_flow = hp * 8 * pump_hours 
        st.metric("إنتاجية المياه المتوقعة", f"{water_flow} متر مكعب / يوم")
        diesel_saved = (hp * 0.746 * pump_hours) / 3
        st.success(f"توفير الجازولين المتوقع: **{diesel_saved:.1f} جالون / يومياً**")

# 3. المختبر الهندسي (حساب الكوابل - تم إصلاح الخطأ هنا)
with tabs[2]:
    st.subheader("📐 مختبر أنداندي (حساب الفقد)")
    st.write("احسب قطر السلك المناسب لمنع 'سخونة الأسلاك' وفقد الطاقة:")
    
    col_c1, col_c2 = st.columns(2)
    current = col_c1.number_input("التيار (Amps):", 1, 400, 30)
    distance = col_c2.number_input("طول السلك (متر):", 1, 200, 20)
    
    # حساب مساحة المقطع النحاسي (Voltage Drop < 3%)
    wire_area = (distance * current * 0.04) / 1.5 
    st.warning(f"📍 قطر السلك النحاسي المقترح: **{max(6, math.ceil(wire_area))} mm²**")

# 4. الصيانة والضمان (جيمني الذكي)
with tabs[3]:
    
