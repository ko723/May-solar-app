
import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="مستشارك الشمسي - م. محمد عبد الهادي", page_icon="☀️", layout="centered")

# الربط مع الخزنة السرية
if "GEMINI_API_KEY" in st.secrets:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    # هذا السطر هو مفتاح الحل:
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("يرجى إضافة GEMINI_API_KEY في إعدادات Secrets")
    st.stop()

# واجهة المستخدم
st.markdown("<h1 style='text-align: center; color: #f39c12;'>⚡ المصمم الشمسي الهندسي</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'><b>تطوير المهندس: محمد عبد الهادي عيسى مختار</b></p>", unsafe_allow_html=True)

# قائمة الأحمال
device_watts = {
    "💡 لمبة LED (12 واط)": 12,
    "🌀 مروحة سقف (75 واط)": 75,
    "📺 شاشة LED (100 واط)": 100,
    "❄️ ثلاجة منزلية (250 واط)": 250,
    "🚿 مكيف نسمة (200 واط)": 200,
    "❄️ مكيف فريون (1200 واط)": 1200,
    "☕ غلاية ماء (2000 واط)": 2000,
    "🔥 هيتر تتش (1500 واط)": 1500
}

devices = st.multiselect("اختر الأجهزة:", list(device_watts.keys()))

total_load = 0
for d in devices:
    total_load += device_watts[d]

if total_load > 0:
    st.info(f"إجمالي الحمل: {total_load} واط")
    
    if st.button("توليد التقرير الهندسي الشامل"):
        with st.spinner('جاري التحليل...'):
            try:
                # طلب التقرير من جيمني
                prompt = f"أنا المهندس محمد عبد الهادي، صممت نظاماً لحمل {total_load} واط. قدم نصيحة فنية بلهجة سودانية مهنية حول الإنفيرتر والبطاريات المناسبة ونظام الـ 48 فولت."
                response = model.generate_content(prompt)
                st.success("التقرير الفني:")
                st.write(response.text)
            except Exception as e:
                # إذا ظهر خطأ 404 مرة أخرى، جرب تبديل اسم الموديل إلى 'models/gemini-1.5-flash'
                st.error(f"عذراً، حدث خطأ: {e}")

st.write("---")
st.caption("تم التطوير بواسطة م. محمد عبد الهادي عيسى © 2026")
