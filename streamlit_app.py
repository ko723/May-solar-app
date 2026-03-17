import streamlit as st
import google.generativeai as genai
import math
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="أنداندي للحلول المتكاملة", page_icon="⚡", layout="wide")

# الربط مع جيمني
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    try:
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        model_name = next((m for m in available_models if 'flash' in m), available_models[0])
        model = genai.GenerativeModel(model_name)
    except: model = None

# --- الهوية البصرية المطورة ---
st.markdown("""
    <div style="background: linear-gradient(135deg, #0f0f0f 0%, #232526 100%); padding: 35px; border-radius: 20px; border-bottom: 5px solid #f39c12; text-align: center; box-shadow: 0 15px 35px rgba(0,0,0,0.6);">
        <h1 style="color: #f39c12; margin: 0; font-size: 3.8em; font-family: 'Arial Black'; letter-spacing: 5px;">ANDANDI</h1>
        <p style="color: #f39c12; font-size: 1.5em; margin: 0; font-weight: bold;">أنداندي</p>
        <p style="color: #ffffff; font-size: 1.1em; margin-top: 10px; opacity: 0.8;">المنصة الهندسية الموحدة | م. محمد عبد الهادي عيسى</p>
    </div>
    """, unsafe_allow_html=True)

st.write("\n")

# --- شريط جانبي (Sidebar) للميزات الإضافية ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3222/3222672.png", width=100)
    st.title("مركز التحكم")
    st.info("مرحباً بك في منصة أنداندي. اختر القسم المناسب لبدء التصميم الهندسي.")
    st.markdown("---")
    st.write("📍 **موقعنا:** السودان")
    st.write("☀️ **متوسط الإشعاع:** 6.5 kWh/m²/day")

# --- الأقسام الرئيسية ---
menu = st.tabs(["🏠 المنظومات المنزلية", "🌾 ري ومزارع أنداندي", "🏭 قطاع الصناعة", "📐 الحاسبة الهندسية"])

# 1. القسم المنزلي
with menu[0]:
    st.subheader("💡 تصميم الأحمال المنزلية")
    appliance_cats = {
        "❄️ التبريد": {"مكيف فريون": 1200, "مكيف نسمة": 250, "ثلاجة": 300, "ديب فريزر": 200},
        "🏠 الأساسيات": {"شاشة LED": 120, "مروحة سقف": 80, "إضاءة": 150, "إنترنت": 30},
        "🔥 أحمال حرارية": {"غلاية ماء": 2000, "سخان": 1500, "مكواة": 1500}
    }
    
    selected_items = {}
    cols = st.columns(3)
    for idx, (cat, items) in enumerate(appliance_cats.items()):
        with cols[idx]:
            st.markdown(f"**{cat}**")
            for name, watt in items.items():
                if st.checkbox(f"{name}", key=f"home_{name}"):
                    num = st.number_input(f"العدد ({name})", 1, 50, 1, key=f"num_{name}")
                    selected_items[name] = watt * num

    total_h = sum(selected_items.values())
    if total_h > 0:
        st.write("---")
        v_sys = st.selectbox("⚡ فولتية النظام:", [12, 24, 48], index=2)
        # تحذير هندسي ذكي
        if total_h > 2000 and v_sys < 48:
            st.warning("⚠️ نصيحة م. محمد: للحمل العالي (>2000W) يفضل استخدام نظام 48V لتقليل الفاقد.")
        
        inv = math.ceil((total_h * 1.3) / 500) * 500
        pan = math.ceil((total_h * 1.8) / 550)
        st.success(f"🔍 المواصفة المقترحة: إنفيرتر {inv}W | ألواح {pan} (550W)")

# 2. القسم الزراعي
with menu[1]:
    st.subheader("🌾 تصميم ري أنداندي الذكي")
    c1, c2 = st.columns(2)
    acres = c1.number_input("كم عدد الفدادين؟", 1, 1000, 5)
    depth = c2.number_input("عمق البئر (متر):", 10, 300, 50)
    
    # معادلة هندسية متطورة للطلمبات
    hp = math.ceil((acres * 0.8) + (depth * 0.05))
    st.metric("القدرة المطلوبة للطلمبة", f"{hp} HP")
    st.write(f"تحتاج إلى جهاز VFD بقدرة {math.ceil(hp * 1.1)} حصان ومصفوفة ألواح حوالي {math.ceil(hp * 3)} لوح.")

# 3. القسم الصناعي
with menu[2]:
    st.subheader("🏭 الحلول الصناعية والورش")
    st.info("هذا القسم مخصص للمحركات الثقيلة (3-Phase).")
    load_ind = st.number_input("إجمالي الحمل الصناعي (kW):", 1.0, 500.0, 5.0)
    st.write(f"يتطلب نظام مخصص بقدرة {load_ind * 1.5} kVA مع نظام حماية Overload متطور.")

# 4. الحاسبة الهندسية (الميزة الجديدة)
with menu[3]:
    st.subheader("📐 حاسبة قطر الأسلاك (Cable Sizer)")
    st.write("احسب قطر السلك النحاسي لتجنب الحرائق والفاقد:")
    amp = st.number_input("التيار المار (Amps):", 1, 500, 20)
    dist = st.number_input("المسافة بين الألواح والإنفيرتر (متر):", 1, 100, 10)
    
    # حساب تقريبي لقطر السلك
    wire_sq = (dist * amp * 0.04) / 2  # معادلة مبسطة لهبوط الجهد
    st.write(f"📍 القطر المقترح للسلك: **{max(4.0, math.ceil(wire_sq))} mm²**")

# --- التذييل والواتساب ---
st.write("\n\n")
st.markdown("---")
wa_url = f"https://wa.me/249116284817?text=استشارة من منصة أنداندي"
st.markdown(f"""
    <div style="text-align: center;">
        <a href="{wa_url}" target="_blank" style="text-decoration: none;">
            <button style="background-color: #25d366; color: white; border: none; padding: 15px 30px; border-radius: 30px; font-weight: bold; cursor: pointer; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                💬 استشارة م. محمد عبد الهادي (واتساب)
            </button>
        </a>
        <p style="color: #7f8c8d; margin-top: 20px; font-size: 0.9em;">
            تصميم وإشراف: <b>م. محمد عبد الهادي عيسى</b> | © 2026 <b>ANDANDI</b>
        </p>
    </div>
""", unsafe_allow_html=True)
    
