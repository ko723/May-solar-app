import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="مستشارك الشمسي - م. محمد عبد الهادي", page_icon="☀️")

# الربط مع الخزنة
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("المفتاح غير موجود في Secrets")
    st.stop()

st.title("⚡ المصمم الشمسي الهندسي")
st.write(f"تطوير المهندس: محمد عبد الهادي عيسى")

# --- الجزء السحري لحل مشكلة الـ 404 ---
try:
    # سنبحث عن الموديل المتاح تلقائياً في حسابك
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    # سنختار أول موديل فلاش متاح
    model_name = next((m for m in available_models if 'flash' in m), available_models[0])
    model = genai.GenerativeModel(model_name)
except Exception as e:
    st.error(f"فشل في العثور على الموديل: {e}")
    st.stop()

# قائمة الأحمال
device_watts = {"💡 لمبة": 12, "🌀 مروحة": 75, "📺 شاشة": 100, "❄️ ثلاجة": 250, "❄️ مكيف فريون": 1200, "☕ غلاية": 2000}
devices = st.multiselect("اختر الأجهزة:", list(device_watts.keys()))
total_load = sum([device_watts[d] for d in devices])

if total_load > 0:
    st.info(f"إجمالي الحمل: {total_load} واط")
    if st.button("توليد التقرير الفني"):
        try:
            response = model.generate_content(f"أنا المهندس محمد عبد الهادي، حملي {total_load} واط. أعطني نصيحة سودانية.")
            st.success("التقرير:")
            st.write(response.text)
        except Exception as e:
            st.error(f"خطأ: {e}")
            
