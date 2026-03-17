import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="مستشارك الشمسي - م. محمد عبد الهادي", page_icon="☀️")

# الربط مع الخزنة
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # محاولة الاتصال بالموديل بعدة صيغ لحل مشكلة 404
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except:
        model = genai.GenerativeModel('models/gemini-1.5-flash')
else:
    st.error("المفتاح غير موجود في Secrets")
    st.stop()

st.markdown("<h1 style='text-align: center; color: #f39c12;'>⚡ المصمم الشمسي الهندسي</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'><b>تطوير المهندس: محمد عبد الهادي عيسى</b></p>", unsafe_allow_html=True)

# قائمة الأجهزة
device_watts = {
    "💡 لمبة LED (12 واط)": 12,
    "🌀 مروحة سقف (75 واط)": 75,
    "📺 شاشة LED (100 واط)": 100,
    "❄️ ثلاجة (250 واط)": 250,
    "❄️ مكيف فريون (1200 واط)": 1200,
    "☕ غلاية ماء (2000 واط)": 2000
}

devices = st.multiselect("اختر الأجهزة:", list(device_watts.keys()))
total_load = sum([device_watts[d] for d in devices])

if total_load > 0:
    st.info(f"إجمالي الحمل: {total_load} واط")
    if st.button("توليد التقرير الفني"):
        with st.spinner('جاري التحليل...'):
            try:
                # طلب التقرير
                prompt = f"بصفتك خبير طاقة شمسية، قدم نصيحة هندسية لمستخدم في السودان لديه حمل {total_load} واط. اقترح سعة الإنفيرتر والبطاريات بلهجة مهنية."
                response = model.generate_content(prompt)
                st.success("التقرير الفني:")
                st.write(response.text)
            except Exception as e:
                st.error(f"حدث خطأ في النظام: {e}")
                
