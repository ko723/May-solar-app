import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="مستشارك الشمسي - م. محمد عبد الهادي", page_icon="☀️", layout="centered")

# الربط مع جيمني عبر الخزنة السرية
API_KEY = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')



genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# الواجهة
st.markdown("<h1 style='text-align: center; color: #f39c12;'>⚡ المصمم الشمسي الهندسي المتكامل</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align: center;'><b>تطوير المهندس: محمد عبد الهادي عيسى مختار</b><br>متخصص في أنظمة القوى والتحكم</p>", unsafe_allow_html=True)
st.write("---")

# قائمة الأحمال الشاملة
device_watts = {
    "💡 لمبة LED (12 واط)": 12,
    "🌀 مروحة سقف (75 واط)": 75,
    "📺 شاشة LED (100 واط)": 100,
    "❄️ ثلاجة منزلية (250 واط)": 250,
    "🚿 مكيف نسمة (200 واط)": 200,
    "❄️ مكيف فريون (1200 واط)": 1200,
    "☕ غلاية ماء (2000 واط)": 2000,
    "🔥 هيتر تتش (1500 واط)": 1500,
    "💻 لابتوب (65 واط)": 65,
    "🔌 شاحن موبايل (15 واط)": 15
}

st.subheader("📊 حساب الأحمال وتصميم النظام")

# اختيار الأجهزة والعدد
selected_load = 0
col_dev, col_qty = st.columns([2, 1])

with col_dev:
    devices = st.multiselect("اختر الأجهزة المختارة:", list(device_watts.keys()))

device_counts = {}
with col_qty:
    for device in devices:
        device_counts[device] = st.number_input(f"العدد:", min_value=1, value=1, key=device)

# حساب إجمالي الوات
for device, count in device_counts.items():
    selected_load += device_watts[device] * count

# الحسابات الهندسية الدقيقة
if selected_load > 0:
    st.info(f"⚡ إجمالي حمل الأجهزة: **{selected_load} واط**")
    
    with st.expander("⚙️ متغيرات التصميم (للمهندس فقط)"):
        sys_v = st.selectbox("جهد النظام (V):", [12, 24, 48], index=2 if selected_load > 2000 else 1)
        safety_factor = 1.25  # معامل أمان للأحمال
        efficiency_loss = 0.85 # كفاءة النظام (15% فواقد في الأسلاك والإنفرتر)
        sun_h = 5.5 # ساعات الذروة في السودان
        backup_hours = st.slider("ساعات التشغيل من البطاريات:", 4, 24, 12)

    # 1. حساب الإنفيرتر المناسب (VA)
    # نأخذ في الاعتبار تيار البدء (Surge) للأحمال الحثية مثل المكيف
    surge_multiplier = 1.5 if any("مكيف" in d for d in devices) else 1.2
    inverter_va = (selected_load * surge_multiplier) / 0.8 # Power Factor 0.8
    inverter_kva = inverter_va / 1000

    # 2. حساب عدد الألواح (مع حساب فواقد الغبار والأسلاك)
    total_energy_daily = (selected_load * backup_hours) / efficiency_loss
    panel_watt = 550
    panels_needed = int(total_energy_daily / (panel_watt * sun_h)) + 1

    # 3. حساب البطاريات (Ah)
    # سعة البطارية = (الطاقة الكلية) / (الجهد * عمق التفريغ 50%)
    battery_ah_total = (total_energy_daily) / (sys_v * 0.5)

    if st.button("توليد التقرير الفني الشامل"):
        with st.spinner('جاري معالجة البيانات الفنية...'):
            prompt = (f"أنا المهندس محمد عبد الهادي. صممت نظاماً بحمل {selected_load} واط. "
                      f"النتائج المحسوبة: إنفرتر {inverter_kva:.1f} kVA، عدد الألواح {panels_needed} (لوح 550 واط)، "
                      f"بطاريات بسعة إجمالية {int(battery_ah_total)} Ah عند جهد {sys_v} فولت. "
                      f"الفواقد المحسوبة في النظام 15%. "
                      f"بصفتك خبير، اشرح للزبون بلهجة سودانية مهنية أهمية اختيار إنفرتر (Pure Sine Wave) "
                      f"وكيفية صيانة البطاريات (سواء جل أو ليثيوم) لتدوم طويلاً.")
            
            try:
                response = model.generate_content(prompt)
                
                # عرض النتائج في مربعات
                st.success("✅ التصميم الهندسي المقترح:")
                c1, c2, c3 = st.columns(3)
                c1.metric("قدرة الإنفيرتر", f"{inverter_kva:.1f} kVA")
                c2.metric("عدد الألواح", f"{panels_needed}")
                c3.metric("سعة البطاريات", f"{int(battery_ah_total)} Ah")
                
                st.markdown("### 📝 تحليل الخبير (جيمني):")
                st.write(response.text)
                
                st.warning(f"ملاحظة فنية: تم حساب فواقد بنسبة 15% (أسلاك + حرارة) لضمان استقرار التيار.")
            except:
                st.error("عذراً، حدث خطأ في الاتصال.")

st.write("---")
st.caption("حقوق التطوير محفوظة © 2026 | م. محمد عبد الهادي عيسى")
