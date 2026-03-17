import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة واسمك الذي يظهر في عنوان المتصفح
st.set_page_config(
    page_title="تطبيق المهندس محمد عبد الهادي عيسى",
    page_icon="☀️",
    layout="centered"
)

# 2. ربط مفتاحك الخاص (الذي أرسلته) بكود الذكاء الاصطناعي
API_KEY = "AIzaSyDWV2SwBtS76SAxUuEXPwIi7A5ybzg3JM8"
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. تصميم واجهة التطبيق (البراندينج الخاص بك)
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #f39c12;
        font-size: 40px;
        font-weight: bold;
    }
    .sub-title {
        text-align: center;
        color: #2c3e50;
        font-size: 20px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-title">☀️ مستشارك الشمسي الذكي</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">إشراف وتطوير: المهندس محمد عبد الهادي عيسى مختار</p>', unsafe_allow_html=True)
st.write("---")

# 4. قسم مدخلات المستخدم (هندسة القوى)
st.info("مرحباً بك! أدخل تفاصيل حملك الكهربائي وسأقوم بتحليل النظام الأمثل لك.")

col1, col2 = st.columns(2)
with col1:
    load_watts = st.number_input("إجمالي الأحمال (وات):", min_value=0, step=100, help="اجمع قدرة الأجهزة التي تريد تشغيلها")
with col2:
    city_name = st.text_input("المدينة/المنطقة:", placeholder="مثلاً: الخرطوم، كريمة...")

# 5. منطق عمل التطبيق والاتصال بجيمني
if st.button("توليد التقرير الفني"):
    if load_watts > 0:
        with st.spinner('جاري تحليل البيانات بذكاء جيمني...'):
            try:
                # صياغة الطلب ليكون هندسياً دقيقاً
                prompt = (f"أنا مهندس كهرباء، أحتاج اقتراحاً فنياً لنظام طاقة شمسية مستقل (Off-grid) "
                         f"لحمل قدره {load_watts} وات في مدينة {city_name}. "
                         f"يرجى تحديد: عدد الألواح، سعة البطاريات، وقدرة الإنفرتر باختصار شديد وبلغة هندسية.")
                
                response = model.generate_content(prompt)
                
                st.success("✅ التقرير الفني المقترح:")
                st.markdown(response.text)
                
            except Exception as e:
                st.error("حدث خطأ في الاتصال. تأكد من صلاحية المفتاح أو اتصال الإنترنت.")
    else:
        st.warning("الرجاء إدخال قيمة الحمل الكهربائي أولاً.")

# 6. تذييل الصفحة الثابت (Footer)
st.write("---")
st.markdown("""
    <div style='text-align: center; color: gray; font-size: 14px;'>
        حقوق التطوير محفوظة © 2026 | م. محمد عبد الهادي عيسى <br>
        تخصص هندسة القوى الكهربائية
    </div>
    """, unsafe_allow_html=True)

