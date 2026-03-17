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

# 3. الهوية البصرية الاحترافية (ANDANDI)
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
    .footer-box {
        text-align: center; padding: 30px; border-top: 1px solid #444; margin-top: 50px;
    }
    </style>
    <div class="main-box">
        <h1 class="brand-eng">ANDANDI</h1>
        <p class="brand-arb">أنداندي للأنظمة الذكية</p>
        <p style="color: white; opacity: 0.9;">بإشراف م. محمد عبد الهادي عيسى</p>
    </div>
    """, unsafe_allow_html=True)

# 4. اختيار نوع النظام
st.markdown("### 🛠️ مركز التحكم والتصميم الهندسي")
system_type = st.selectbox(
    "ما هو نوع المنظومة التي تريد تصميمها؟",
    ["🏠 المنظومات المنزلية والسكينة", "🌾 منظومات الري الزراعي (الطلمبات)", "🏭 المنظومات الصناعية (الورش والمصانع)"]
)

st.write("---")

# ==================== 🏠 القسم السكني (شامل كل شيء) ====================
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
        st.markdown(f"### 📊 النتائج الفنية للمنظومة")
        
        c1, c2 = st.columns(2)
        v_sys = c1.selectbox("جهد النظام (V):", [12, 24, 48], index=2)
        night_hours = c2.slider("ساعات التشغيل الليلي المطلوب:", 1, 15, 6)
        
        # الحسابات الهندسية
        inv_kw = math.ceil((total_load * 1.25) / 1000)
        pan_count = math.ceil((total_load * 2.2) / 550)
        
        # حساب البطاريات (200Ah)
        req_ah = (total_load * night_hours) / (v_sys * 0.6)
        bat_count = math.ceil(req_ah / 200)
        if v_sys == 48: bat_count = math.ceil(bat_count / 4) * 4
        elif v_sys == 24: bat_count = math.ceil(bat_count / 2) * 2

        # العرض الرئيسي
        r1, r2, r3 = st.columns(3)
        r1.metric("الإنفيرتر", f"{inv_kw} kW")
        r2.metric("الألواح (550W)", f"{pan_count} لوح")
        r3.metric("البطاريات (200Ah)", f"{bat_count} بطارية")

        # --- قسم الاكسسوارات والملحقات ---
        st.markdown("### 🛒 الملحقات والاكسسوارات الفنية")
        amps = (total_load / v_sys) * 1.25
        wire = "10mm" if amps < 60 else "16mm"
        
        acc1, acc2 = st.columns(2)
        with acc1:
            st.write("**🔌 الكوابل:**")
            st.info(f"- كابل بطاريات: {wire} نحاس")
            st.info(f"- كابل ألواح: 6mm DC")
        with acc2:
            st.write("**🛡️ الحماية:**")
            st.info(f"- قاطع بطارية: {math.ceil(amps/10)*10}A DC")
            st.info(f"- قاطع خروج: 32A AC")

# ==================== 🌾 القسم الزراعي ====================
elif "🌾" in system_type:
    st.subheader("🚜 تصميم أنظمة الري")
    acres = st.number_input("المساحة (فدان):", 1, 1000, 5)
    depth = st.number_input("العمق (متر):", 10, 500, 60)
    hp = math.ceil((acres * 1.1) + (depth * 0.06))
    st.success(f"المطلوب: طلمبة {hp} حصان")
    st.info(f"الملحقات: جهاز VFD {hp}HP + كابل بحري + هياكل تثبيت.")

# ==================== 🏭 القسم الصناعي ====================
elif "🏭" in system_type:
    st.subheader("⚙️ المنظومات الصناعية")
    ind_w = st.number_input("الحمل (kW):", 1.0, 2000.0, 10.0)
    st.error(f"تحتاج إنفيرتر 3-Phase بقدرة {math.ceil(ind_w * 2)} كيلوواط")

# --- التذييل الثابت (حقوق الملكية) ---
st.markdown(f"""
    <div class="footer-box">
        <a href="https://wa.me/249116284817" target="_blank" style="text-decoration: none;">
            <button style="background-color: #25d366; color: white; border: none; padding: 15px 35px; border-radius: 30px; font-weight: bold; cursor: pointer; font-size: 1.1em;">
                💬 تواصل مباشر مع م. محمد عبد الهادي
            </button>
        </a>
        <br><br>
        <p style="color: #f39c12; font-weight: bold; font-size: 1.2em; margin-bottom: 5px;">ANDANDI © 2026</p>
        <p style="color: #888; margin-top: 0;">جميع الحقوق محفوظة | تصميم وإشراف: م. محمد عبد الهادي عيسى</p>
        <p style="color: #555; font-size: 0.8em;">هندسة القوى الكهربائية - السودان</p>
    </div>
    """, unsafe_allow_html=True)
