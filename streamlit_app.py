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
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = next((m for m in available_models if 'flash' in m), available_models[0])
        model = genai.GenerativeModel(model_name)
    except: model = None

# --- تصميم الهوية البصرية ---
st.markdown("""
    <div style="background: linear-gradient(135deg, #1a1a1a 0%, #2c3e50 100%); padding: 30px; border-radius: 15px; border-top: 5px solid #f39c12; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.4);">
        <h1 style="color: #f39c12; margin: 0; font-size: 3.5em; font-family: 'Trebuchet MS'; letter-spacing: 3px; line-height: 1;">ANDANDI</h1>
        <p style="color: #f39c12; font-size: 1.2em; margin: 0; font-family: 'Arial'; font-weight: bold;">أنداندي</p>
        <p style="color: #ecf0f1; font-size: 1.1em; margin-top: 10px; opacity: 0.8;">حلول الطاقة الشمسية (منزلي - زراعي - صناعي)</p>
    </div>
    """, unsafe_allow_html=True)

# --- اختيار نوع المنظومة ---
st.write("\n")
st.markdown("### 📋 اختر نوع النظام المطلوب")
system_type = st.radio("نوع المنظومة:", ["🏠 منزلي / سكني", "🌾 زراعي (طلمبات)", "🏭 صناعي / ورش"], horizontal=True)

st.write("---")

# ==================== القسم السكني ====================
if system_type == "🏠 منزلي / سكني":
    appliance_cats = {
        "❄️ التبريد": {"مكيف فريون": 1200, "مكيف نسمة": 250, "ثلاجة": 300, "ديب فريزر": 200},
        "🍳 المطبخ": {"غلاية ماء": 2000, "ميكروويف": 1200, "سخان كهربائي": 1500},
        "🏠 المنزل": {"شاشة LED": 120, "مروحة سقف": 80, "مكواة": 1500, "إنترنت": 30}
    }
    selected_items = {}
    tabs = st.tabs(list(appliance_cats.keys()))
    for i, cat in enumerate(appliance_cats.keys()):
        with tabs[i]:
            cols = st.columns(2)
            for j, (name, watt) in enumerate(appliance_cats[cat].items()):
                if cols[j % 2].checkbox(f"{name} ({watt}W)", key=f"c_{name}"):
                    count = cols[j % 2].number_input(f"العدد", 1, 20, 1, key=f"v_{name}")
                    selected_items[name] = watt * count
    
    total_load = sum(selected_items.values())
    if total_load > 0:
        c1, c2 = st.columns(2)
        night_h = c1.slider("🌙 تشغيل ليلي (ساعة):", 1, 15, 6)
        v_sys = c2.radio("⚡ جهد النظام:", [12, 24, 48], index=2, horizontal=True)
        
        inv = math.ceil((total_load * 1.25) / 500) * 500
        bat = math.ceil((total_load * night_h) / (v_sys * 0.5 * 0.85))
        pan = math.ceil(((total_load * 8) + (total_load * night_h)) / (550 * 5 * 0.65))
        
        st.success(f"✅ **النتائج:** إنفيرتر {inv}W | بطاريات {bat}Ah | ألواح {pan} (550W)")

# ==================== القسم الزراعي ====================
elif system_type == "🌾 زراعي (طلمبات)":
    st.markdown("#### 🚜 تصميم منظومة الري الشمسي")
    col1, col2 = st.columns(2)
    with col1:
        acres = st.number_input("📏 عدد الفدادين (Acre):", min_value=1, value=5)
        crop_type = st.selectbox("🌱 نوع المحصول (لاحتياج المياه):", ["برسيم / أعلاف", "نخيل / أشجار", "خضروات", "محاصيل حقلية"])
    
    # حساب تقريبي: الفدان يحتاج حوالي 1 إلى 1.5 حصان حسب المحصول والعمق
    hp_needed = math.ceil(acres * 1.2)
    vfd_size = math.ceil(hp_needed * 0.75 * 1.5) # تحويل للحصان ثم كيلوواط مع معامل أمان
    panels_count = math.ceil((hp_needed * 746 * 1.6) / 550) # 1.6 معامل تعويض الفقد النهاري

    with col2:
        st.info(f"💡 **التحليل:** لري مساحة {acres} فدان محصول ({crop_type})")
        st.metric("قدرة الطلمبة المطلوبة", f"{hp_needed} حصان")
        st.metric("جهاز التشغيل (VFD)", f"{hp_needed} HP / 3-Phase")
        st.metric("عدد الألواح (550W)", f"{panels_count} لوح")
    
    st.warning("⚠️ ملاحظة: الحسابات مبنية على عمق بئر متوسط (40-60 متر). للأعماق الكبيرة يرجى مراجعة م. محمد.")

# ==================== القسم الصناعي ====================
elif system_type == "🏭 صناعي / ورش":
    st.markdown("#### ⚙️ تصميم أحمال الورش والمصانع")
    heavy_load = st.number_input("🔌 إجمالي أحمال الماكينات (واط):", min_value=500, value=5000, step=500)
    motor_start = st.checkbox("🔄 هل توجد محركات تبدأ مباشرة (Direct on Line)؟")
    
    multiplier = 3.0 if motor_start else 1.5
    industrial_inv = math.ceil((heavy_load * multiplier) / 1000)
    industrial_panels = math.ceil((heavy_load * 1.8) / 550)

    res1, res2 = st.columns(2)
    res1.metric("قدرة الإنفيرتر الصناعي", f"{industrial_inv} kW")
    res2.metric("عدد الألواح المطلوبة", f"{industrial_panels} لوح")
    st.write("---")
    st.info("للأنظمة الصناعية يفضل استخدام إنفيرترات Three-Phase لضمان استقرار الجهد.")

# --- التذييل والواتساب ---
st.write("\n\n")
wa_url = f"https://wa.me/249116284817?text=استشارة فنية من م. محمد ({system_type})"
st.markdown(f"""
    <style>
    .wa-float {{ position: fixed; bottom: 20px; right: 20px; background-color: #25d366; color: white;
        border-radius: 50px; text-align: center; padding: 12px 18px; box-shadow: 2px 5px 15px rgba(0,0,0,0.3);
        z-index: 1000; text-decoration: none; font-weight: bold; font-size: 14px; }}
    </style>
    <a href="{wa_url}" class="wa-float" target="_blank">💬 تواصل مع م. محمد</a>
    <div style="text-align: center; color: #95a5a6; padding: 20px; font-size: 0.9em; border-top: 1px solid #34495e;">
        إشراف وتصميم: <b>م. محمد عبد الهادي عيسى</b> <br>
        © 2026 جميع الحقوق محفوظة لـ <b>ANDANDI</b>
    </div>
""", unsafe_allow_html=True)
