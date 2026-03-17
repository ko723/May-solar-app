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

# ==================== 🏠 القسم السكني المطور ====================
if "🏠" in system_type:
    st.subheader("📋 تحديد أحمال المنزل والاكسسوارات")
    
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
        st.markdown(f"### 📊 ملخص الأحمال: {total_load} واط")
        
        # حسابات المنظومة الأساسية
        v_sys = st.selectbox("جهد النظام (V):", [12, 24, 48], index=2)
        inv_kw = math.ceil((total_load * 1.25) / 1000)
        pan_count = math.ceil((total_load * 2.2) / 550)
        
        # --- قسم الاكسسوارات الذكي ---
        st.markdown("### 🛒 الملحقات والاكسسوارات الفنية (تلقائي)")
        with st.container():
            st.markdown("<div style='background-color: #1e1e1e; padding: 20px; border-radius: 10px; border: 1px solid #f39c12;'>", unsafe_allow_html=True)
            
            # حساب التيار (Amps) لتحديد الأسلاك والبريكرات
            system_amps = (total_load / v_sys) * 1.25
            
            # تحديد مقاس السلك
            if system_amps <= 30: wire_size = 6
            elif system_amps <= 50: wire_size = 10
            elif system_amps <= 80: wire_size = 16
            else: wire_size = 25
            
            # تحديد البريكرات
            breaker_ac = math.ceil((total_load / 220) * 1.5 / 10) * 10
            breaker_dc = math.ceil(system_amps / 10) * 10

            c1, c2, c3 = st.columns(3)
            with c1:
                st.write("**🔌 الكوابل والأسلاك:**")
                st.info(f"أسلاك البطاريات: {wire_size}mm مخصص")
                st.info(f"أسلاك الألواح: 6mm DC")
            with c2:
                st.write("**🛡️ قواطع الحماية:**")
                st.info(f"قاطع DC (البطاريات): {breaker_dc}A")
                st.info(f"قاطع AC (الخروج): {breaker_ac}A")
            with c3:
                st.write("**🏗️ الهيكل والملحقات:**")
                st.info(f"قواعد تثبيت: لعدد {pan_count} لوح")
                st.info(f"تابلوه توزيع حماية متكامل")
            st.markdown("</div>", unsafe_allow_html=True)

# ==================== 🌾 القسم الزراعي المطور ====================
elif "🌾" in system_type:
    st.subheader("🚜 تفاصيل منظومة الري الزراعي")
    acres = st.number_input("المساحة (فدان):", 1, 1000, 5)
    depth = st.number_input("العمق (متر):", 10, 500, 60)
    
    hp = math.ceil((acres * 1.1) + (depth * 0.06))
    panels = math.ceil((hp * 746 * 1.6) / 550)
    
    st.success(f"✅ التصميم: طلمبة {hp} حصان | {panels} لوح")
    
    st.markdown("#### 📦 تفاصيل الملحقات الزراعية:")
    col_z1, col_z2 = st.columns(2)
    with col_z1:
        st.info(f"- جهاز VFD بقدرة {hp} حصان (ماركة INVT أو ما يعادلها)")
        st.info(f"- كابل بحري (Submersible Cable) مقاس 3x10mm بطول {depth + 20} متر")
    with col_z2:
        st.info("- هيكل تثبيت حديد مجلفن مضاد للصدأ")
        st.info("- حساسات مستوى الماء (Sensors) ومفتاح تشغيل طوارئ")

# ==================== 🏭 القسم الصناعي المطور ====================
elif "🏭" in system_type:
    st.subheader("⚙️ منظومة الورش والمصانع")
    ind_w = st.number_input("الحمل الصناعي (kW):", 1.0, 1000.0, 10.0)
    st.error(f"تحتاج إنفيرتر صناعي 3-Phase بقدرة {math.ceil(ind_w * 2)} كيلوواط")
    st.info("الملحقات: كوابل نحاس 25mm + لوحة ATS للتحويل الآلي + نظام تأريض (Earthing).")

# --- التذييل والواتساب ---
st.write("---")
wa_url = f"https://wa.me/249116284817?text=طلب عرض سعر لمنظومة {system_type}"
st.markdown(f"""
    <div style="text-align: center; padding: 25px;">
        <a href="{wa_url}" target="_blank">
            <button style="background-color: #25d366; color: white; border: none; padding: 18px 40px; border-radius: 35px; font-weight: bold; cursor: pointer; font-size: 1.2em;">
                💬 اطلب عرض السعر النهائي من م. محمد
            </button>
        </a>
        <p style="color: #7f8c8d; margin-top: 20px;">تصميم وبرمجة: م. محمد عبد الهادي عيسى | <b>ANDANDI 2026</b></p>
    </div>
""", unsafe_allow_html=True)
