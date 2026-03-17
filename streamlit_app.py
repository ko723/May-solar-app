import streamlit as st
import math

# 1. إعدادات الصفحة (توضع في أول سطر دائماً)
st.set_page_config(page_title="ANDANDI", page_icon="☀️", layout="wide")

# إخفاء القوائم الجانبية للزبائن
hide_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;} .stAppDeployButton {display:none;}</style>"""
st.markdown(hide_style, unsafe_allow_html=True)

# 2. الهوية البصرية
st.markdown("""
    <div style="background: linear-gradient(135deg, #000 0%, #2c3e50 100%); padding: 30px; border-radius: 20px; text-align: center; border-bottom: 5px solid #f39c12;">
        <h1 style="color: #f39c12; margin: 0; font-size: 3em; font-family: 'Arial Black';">ANDANDI</h1>
        <p style="color: #f39c12; font-size: 1.2em; font-weight: bold;">أنداندي للأنظمة الذكية - م. محمد عبد الهادي</p>
    </div>
    """, unsafe_allow_html=True)

# 3. الاختيارات
system_type = st.selectbox("اختر نوع المنظومة:", ["🏠 منزلي / سكني", "🌾 زراعي / طلمبات", "🏭 صناعي / ورش"])

if "🏠" in system_type:
    st.subheader("📋 تحديد الأحمال المنزلية")
    load = st.number_input("أدخل إجمالي الحمل (واط):", 0, 50000, 1000)
    v_sys = st.selectbox("جهد النظام (V):", [12, 24, 48], index=2)
    h_night = st.slider("ساعات التشغيل ليلاً:", 1, 15, 6)
    
    # حسابات
    inv = math.ceil((load * 1.3) / 1000)
    pan = math.ceil((load * 2.2) / 550)
    bat = math.ceil((load * h_night) / (v_sys * 0.6 * 200))
    if v_sys == 48: bat = math.ceil(bat/4)*4
    
    st.markdown(f'<div style="text-align:center; background:#f39c12; color:black; padding:10px; border-radius:50px; font-size:1.5em; font-weight:bold;">⚡ {load} W</div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    c1.metric("الإنفيرتر", f"{inv} kW")
    c2.metric("الألواح", f"{pan} لوح")
    c3.metric("البطاريات", f"{bat} بطارية")

# 4. حقوق الملكية والواتساب
st.write("---")
st.markdown(f"""
    <div style="text-align: center;">
        <a href="https://wa.me/249116284817" target="_blank">
            <button style="background-color: #25d366; color: white; border: none; padding: 15px 30px; border-radius: 30px; font-weight: bold; cursor: pointer;">💬 تواصل مع م. محمد</button>
        </a>
        <p style="margin-top: 20px; color: #888;">ANDANDI © 2026 | جميع الحقوق محفوظة</p>
    </div>
    """, unsafe_allow_html=True)
