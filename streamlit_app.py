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
    except:
        model = None
else:
    model = None

# 3. تصميم الهوية البصرية (ANDANDI)
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
    .brand-eng { color: #f39c12; font-size: 3.5em; font-family: 'Arial Black'; margin: 0; line-height: 1; }
    .brand-arb { color: #f39c12; font-size: 1.5em; margin: 0; font-weight: bold; }
    </style>
    <div class="main-header">
        <h1 class="brand-eng">ANDANDI</h1>
        <p class="brand-arb">أنداندي للأنظمة الذكية</p>
        <p style="color: white; opacity: 0.8; margin-top: 15px;">بإشراف م. محمد عبد الهادي عيسى</p>
    </div>
    """, unsafe_allow_html=True)

st.write("\n")

# 4. الأقسام الرئيسية (Tabs)
tabs = st.tabs(["🏠 أحمال المنزل", "🌾 ري المزارع", "⚙️ المختبر الهندسي", "🛡️ الصيانة والضمان"])

# --- القسم الأول: منزلي ---
with tabs[0]:
    st.subheader("💡 تصميم المنظومة السكنية")
    c1, c2 = st.columns(2)
    with c1:
        ac = st.number_input("مكيفات فريون:", 0, 20, 0)
        fans = st.number_input("مراوح سقف:", 0, 50, 4)
    with c2:
        fridge = st.number_input("ثلاجات:", 0, 10, 1)
        lights = st.number_input("لمبات إضاءة:", 0, 100, 10)
    
    total_w = (ac * 1500) + (fridge * 300) + (fans * 80) + (lights * 15)
    st.markdown(f"#### إجمالي الحمل: {total_w} واط")
    
    if total_w > 0:
        inv_size = math.ceil((total_w * 1.3) / 1000)
        st.success(f"المقترح: إنفيرتر بقدرة {inv_size} كيلوواط")

# --- القسم الثاني: زراعي ---
with tabs[1]:
    st.subheader("🚜 تصميم ري مزارع أنداندي")
    col1, col2 = st.columns(2)
    with col1:
        acres = st.number_input("عدد الفدادين:", 1, 500, 5)
        pump_h = st.slider("ساعات التشغيل:", 1, 12, 6)
    with col2:
        hp = math.ceil(acres * 1.2)
        water = hp * 8 * pump_h
        st.metric("قدرة الطلمبة", f"{hp} حصان")
        st.metric("إنتاج المياه اليومي", f"{water} م³")

# --- القسم الثالث: المختبر الهندسي ---
with tabs[2]:
    st.subheader("📐 حاسبة الأسلاك (Cable Sizing)")
    st.write("احسب قطر السلك المناسب لمنع الفقد:")
    cc1, cc2 = st.columns(2)
    with cc1:
        amp = st.number_input("التيار (أمبير):", 1, 400, 30)
    with cc2:
        dist = st.number_input("المسافة (متر):", 1, 200, 20)
    
    wire_size = (dist * amp * 0.04) / 1.5
    st.warning(f"القطر المقترح للسلك: {max(6, math.ceil(wire_size))} mm²")

# --- القسم الرابع: الصيانة والذكاء الاصطناعي ---
with tabs[3]:
    st.subheader("🛡️ مركز الدعم الذكي")
    u_query = st.text_input("اسأل م. محمد عن أي عطل هنا:")
    if st.button("تحليل الاستشارة 🤖"):
        if model:
            with st.spinner("جاري التحليل..."):
                res = model.generate_content(f"أنت خبير طاقة شمسية سوداني، حلل: {u_query}")
                st.info(res.text)
        else:
            st.error("يرجى التأكد من إعداد مفتاح API في السكرت (Secrets).")

# 5. التذييل (Footer)
st.write("---")
st.markdown("### 🏢 من أعمال م. محمد (أنداندي)")
st.image("https://images.unsplash.com/photo-1509391366360-fe5bb626582f?w=800", caption="مشروع ري متكامل")

wa_url = f"https://wa.me/249116284817?text=استشارة من منصة أنداندي"
st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <a href="{wa_url}" target="_blank">
            <button style="background-color: #25d366; color: white; border: none; padding: 15px 35px; border-radius: 30px; font-weight: bold; cursor: pointer;">
                💬 تواصل مع م. محمد عبد الهادي
            </button>
        </a>
        <p style="color: #888; margin-top: 20px;">© 2026 ANDANDI - جميع الحقوق محفوظة</p>
    </div>
""", unsafe_allow_html=True)
