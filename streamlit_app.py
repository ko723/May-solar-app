import streamlit as st
import google.generativeai as genai
import math

# 1. إعدادات الصفحة
st.set_page_config(page_title="أنداندي للطاقة الشمسية", page_icon="☀️", layout="wide")

# 2. الربط مع جيمني
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
        padding: 35px; border-radius: 20px; text-align: center;
        border-bottom: 5px solid #f39c12; margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.4);
    }
    .brand-eng { color: #f39c12; font-size: 4em; font-family: 'Arial Black'; margin: 0; }
    .brand-arb { color: #f39c12; font-size: 1.5em; margin: 0; font-weight: bold; }
    </style>
    <div class="main-box">
        <h1 class="brand-eng">ANDANDI</h1>
        <p class="brand-arb">أنداندي للأنظمة الذكية</p>
        <p style="color: white; opacity: 0.9;">إشراف م. محمد عبد الهادي عيسى</p>
    </div>
    """, unsafe_allow_html=True)

# 4. اختيار نوع النظام
st.markdown("### 🛠️ مركز التحكم والتصميم الهندسي")
system_type = st.selectbox(
    "ما هو نوع المنظومة التي تريد تصميمها؟",
    ["🏠 المنظومات المنزلية والسكينة", "🌾 منظومات الري الزراعي (الطلمبات)", "🏭 المنظومات الصناعية (الورش والمصانع)"]
)

st.write("---")

# ==================== 🏠 القسم السكني (شامل البطاريات والاكسسوارات) ====================
if "🏠" in system_type:
    st.subheader("📋 تحديد أحمال المنزل")
    
    appliance_cats = {
        "❄️ التبريد": {"مكيف فريون 1.5 حصان": 1500, "مكيف نسمة": 250, "ثلاجة": 300, "ديب فريزر": 250},
        "🏠 الأجهزة": {"مروحة": 80, "شاشة": 120, "إضاءة": 200, "إنترنت": 30},
        "🍳 المطبخ": {"غلاية": 2000, "ميكروويف": 1200, "مكواة": 1500}
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
        st.markdown(f"### 📊 نتائج التصميم الفني")
        
        # مدخلات إضافية للحساب
        c1, c2 = st.columns(2)
        v_sys = c1.selectbox("جهد النظام (V):", [12, 24, 48], index=2)
        night_hours = c2.slider("ساعات التشغيل الليلي (على البطارية):", 1, 15, 6)
        
        # 1. حساب الإنفيرتر والألواح
        inv_kw = math.ceil((total_load * 1.25) / 1000)
        pan_count = math.ceil((total_load * 2.2) / 550)
        
        # 2. حساب البطاريات (بافتراض بطاريات 200Ah)
        # المعادلة: (الحمل * الساعات) / (الجهد * 0.6 كفاءة) / 200Ah
        required_ah = (total_load * night_hours) / (v_sys * 0.6)
        bat_count = math.ceil(required_ah / 200)
        # التأكد من أن عدد البطاريات يناسب الجهد (مثلاً نظام 48V يحتاج مضاعفات 4)
        if v_sys == 48: bat_count = math.ceil(bat_count / 4) * 4
        elif v_sys == 24: bat_count = math.ceil(bat_count / 2) * 2

        # عرض النتائج الأساسية
        res1, res2, res3 = st.columns(3)
        res1.metric("قدرة الإنفيرتر", f"{inv_kw} kW")
        res2.metric("عدد الألواح (550W)", f"{pan_count} لوح")
        res3.metric("عدد البطاريات (200Ah)", f"{bat_count} بطارية")

        # --- قسم الاكسسوارات والملحقات ---
        st.markdown("### 🛒 الملحقات والاكسسوارات الفنية")
        st.info("هذه الملحقات ضرورية لضمان سلامة المنظومة وكفاءتها:")
        
        # حسابات الأسلاك والبريكرات
        system_amps = (total_load / v_sys) * 1.25
        if system_amps <= 30: wire = "6mm"
        elif system_amps <= 60: wire = "10mm"
        else: wire = "16mm أو 25mm"
        
        acc_col1, acc_col2 = st.columns(2)
        with acc_col1:
            st.write("**🔌 الأسلاك والكوابل:**")
            st.write(f"- كوابل البطاريات: {wire} نحاس مخصص")
            st.write(f"- كوابل الألواح: 6mm DC (حسب المسافة)")
            st.write(f"- كوابل الأحمال: 4mm AC")
        with acc_col2:
            st.write("**🛡️ الحماية والتركيب:**")
            
