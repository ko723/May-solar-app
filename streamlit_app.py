import streamlit as st
import google.generativeai as genai
import math
import pandas as pd

# 1. إعدادات الصفحة
st.set_page_config(page_title="أنداندي للطاقة الشمسية", page_icon="☀️", layout="wide")

# 2. الربط مع جيمني (للدعم الفني)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
    except: model = None
else: model = None

# 3. الهوية البصرية (ANDANDI)
st.markdown("""
    <style>
    .main-box {
        background: linear-gradient(135deg, #000000 0%, #2c3e50 100%);
        padding: 35px;
        border-radius: 20px;
        text-align: center;
        border-bottom: 5px solid #f39c12;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }
    .brand-eng { color: #f39c12; font-size: 4em; font-family: 'Arial Black'; margin: 0; line-height: 1; }
    .brand-arb { color: #f39c12; font-size: 1.5em; margin: 0; font-weight: bold; }
    </style>
    <div class="main-box">
        <h1 class="brand-eng">ANDANDI</h1>
        <p class="brand-arb">أنداندي للأنظمة الذكية</p>
        <p style="color: white; opacity: 0.9;">بإشراف م. محمد عبد الهادي عيسى</p>
    </div>
    """, unsafe_allow_html=True)

# 4. اختيار نوع النظام داخل مربع أنيق
st.markdown("### 🛠️ مركز التحكم والتصميم")
with st.container():
    st.info("اختر نوع المنظومة من القائمة أدناه لبدء الحسابات الهندسية")
    system_type = st.selectbox(
        "ما هو نوع المنظومة التي تريد تصميمها؟",
        ["🏠 المنظومات المنزلية والسكينة", "🌾 منظومات الري الزراعي (الطلمبات)", "🏭 المنظومات الصناعية (الورش والمصانع)"]
    )

st.write("---")

# ==================== 🏠 القسم السكني ====================
if "🏠" in system_type:
    st.subheader("📋 تحديد أحمال المنزل (خيارات شاملة)")
    
    appliance_cats = {
        "❄️ التبريد والتكييف": {
            "مكيف فريون 1.5 حصان": 1500, "مكيف نسمة / ماء": 250, "ثلاجة كبيرة": 300, 
            "ديب فريزر": 250, "مبرد مادة (كولر)": 150
        },
        "🏠 الأجهزة العامة والإضاءة": {
            "مروحة سقف": 80, "شاشة LED": 120, "إضاءة البيت كاملة": 200, 
            "راوتر إنترنت": 30, "ريسيفر": 50, "لابتوب": 100
        },
        "🍳 أجهزة المطبخ والكي": {
            "غلاية ماء (كاتل)": 2000, "ميكروويف": 1200, "خلاط": 400, 
            "مكواة ملابس": 1500, "سخان كهربائي": 1500, "فرن كهربائي": 2500
        },
        "💦 مضخات وغسالات": {
            "مضخة ماء منزلية": 750, "غسالة ملابس عادية": 500, "غسالة أوتوماتيك": 2000, 
            "مكنسة كهربائية": 1400
        }
    }
    
    selected_items = {}
    cols = st.columns(2)
    for i, (cat, items) in enumerate(appliance_cats.items()):
        with cols[i % 2]:
            with st.expander(f"➕ {cat}", expanded=True):
                for name, watt in items.items():
                    if st.checkbox(f"{name} ({watt}W)", key=f"ch_{name}"):
                        count = st.number_input(f"العدد", 1, 50, 1, key=f"num_{name}")
                        selected_items[name] = watt * count

    total_load = sum(selected_items.values())
    if total_load > 0:
        st.markdown(f"### 📊 إجمالي الحمل المطلوب: {total_load} واط")
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            v_sys = st.selectbox("جهد النظام (V):", [24, 48], index=1)
            night_h = st.slider("ساعات التشغيل ليلاً:", 1, 15, 6)
        
        inv = math.ceil((total_load * 1.3) / 1000)
        pan = math.ceil((total_load * 2.1) / 550)
        
        with res_col2:
            st.success(f"⚡ إنفيرتر: {inv} كيلوواط")
            st.success(f"☀️ ألواح: {pan} لوح (550W)")

# ==================== 🌾 القسم الزراعي ====================
elif "🌾" in system_type:
    st.subheader("🚜 تصميم أنظمة الري والطلمبات")
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            acres = st.number_input("مساحة المزرعة (بالفدان):", 1, 1000, 5)
            depth = st.number_input("عمق البئر الإجمالي (متر):", 10, 500, 60)
        with c2:
            st.info("💡 حسابات بناءً على متوسط احتياج المحصول والعمق")
            # معادلة تقريبية للحصان
            hp_base = (acres * 1.1) + (depth * 0.06)
            hp = math.ceil(hp_base)
            st.metric("قدرة الطلمبة المطلوبة", f"{hp} حصان")
            
            vfd = hp # جهاز الـ VFD غالباً يكون بنفس قدرة الحصان
            panels = math.ceil((hp * 746 * 1.6) / 550)
            
            st.write(f"📦 **المعدات المقترحة:**")
            st.write(f"- جهاز VFD بقدرة: {vfd} HP")
            st.write(f"- عدد الألواح: {panels} لوح (550W)")

# ==================== 🏭 القسم الصناعي ====================
elif "🏭" in system_type:
    st.subheader("⚙️ تصميم أحمال المصانع والورش")
    with st.container():
        ind_load = st.number_input("إجمالي حمل الماكينات بالكيلوواط (kW):", 1.0, 2000.0, 10.0)
        motor_type = st.radio("نوع تشغيل المحركات:", ["نعومة (VFD/Soft Starter)", "تشغيل مباشر (Direct Online)"])
        
        factor = 1.5 if "نعومة" in motor_type else 3.5
        needed_inv = math.ceil(ind_load * factor)
        
        st.error(f"⚠️ القدرة المطلوبة للإنفيرتر: {needed_inv} كيلوواط")
        st.info("يجب استخدام كوابل نحاسية بمقاسات لا تقل عن 16mm لهذا الحمل.")

# --- التذييل والواتساب ---
st.write("\n")
st.write("---")
st.markdown("### 🏢 من أعمال م. محمد عبد الهادي (أنداندي)")
st.image("https://images.unsplash.com/photo-1509391366360-fe5bb626582f?w=800", caption="تنفيذ مشاريع أنداندي الذكية")

wa_url = f"https://wa.me/249116284817?text=طلب استشارة هندسية من م. محمد"
st.markdown(f"""
    <div style="text-align: center; padding: 25px;">
        <a href="{wa_url}" target="_blank">
            <button style="background-color: #25d366; color: white; border: none; padding: 18px 40px; border-radius: 35px; font-weight: bold; cursor: pointer; font-size: 1.2em; box-shadow: 0 5px 15px rgba(0,0,0,0.3);">
                💬 تواصل مباشر مع م. محمد (واتساب)
            </button>
        </a>
        <p style="color: #7f8c8d; margin-top: 25px;">تطوير وإشراف: م. محمد عبد الهادي عيسى | جميع الحقوق محفوظة لـ <b>ANDANDI</b> © 2026</p>
    </div>
""", unsafe_allow_html=True)
            
