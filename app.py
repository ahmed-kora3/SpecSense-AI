import streamlit as st
import pandas as pd
import cv2
import numpy as np
import tempfile
import os
import base64
from PIL import Image

# ==========================================
# 1. PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="SpecSense AI", 
    layout="wide", 
    page_icon="logo.png"
)

# Sidebar Logo (Official Streamlit Method)
st.logo("logo.png", icon_image="logo.png")

# ==========================================
# 2. CUSTOM STYLING (CSS)
# ==========================================
# --- Styling ---
st.markdown("""
    <style>
    .header-container {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 10px;
    }
    .header-title { 
        font-size: 3.5rem; 
        font-weight: 800; 
        color: #FFFFFF;  /* <--- تم التغيير هنا إلى الأبيض */
        margin: 0; 
        padding-left: 20px;
        text-shadow: 2px 2px 4px #000000; /* (اختياري) ظل خفيف عشان الكلام يظهر لو الخلفية فاتحة */
    }
    .header-sub { 
        font-size: 1.2rem; 
        color: #F0F0F0;  /* <--- تم تفتيح لون العنوان الفرعي أيضاً */
        text-align: center; 
        margin-bottom: 25px; 
    }
    /* ... باقي الـ CSS كما هو ... */
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. HEADER SECTION (With Base64 Logo Fix)
# ==========================================
def get_base64_image(image_path):
    """Converts image to base64 string for HTML embedding"""
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except Exception:
        return ""

# Load and convert logo
logo_b64 = get_base64_image("logo.png")

# Display Header with Flexbox Layout
st.markdown(f"""
    <div class="header-container">
        <img src="data:image/png;base64,{logo_b64}" style="height: 90px;">
        <span class="header-title">SpecSense AI</span>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="header-sub">Intelligent Cable Inspection & Document Analysis System</div>', unsafe_allow_html=True)
st.divider()

# ==========================================
# 4. SIDEBAR CONTROL
# ==========================================
st.sidebar.title("🎛️ System Control")
mode = st.sidebar.radio("Select Module:", 
    ["👁️ Vision Inspection (Cross-Section)", 
     "📄 Datasheet OCR & Validation"])

st.sidebar.success("✅ System Active\n🚀 GPU Acceleration: Enabled")

# =========================================================
# MODULE 1: VISION INSPECTION (YOLO)
# =========================================================
if mode == "👁️ Vision Inspection (Cross-Section)":
    st.subheader("🔍 Automated Geometry Analysis")
    st.write("Upload cross-section images to detect cable diameter and defects.")
    
    uploaded_files = st.file_uploader("Upload Images", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("🚀 Start AI Analysis", type="primary"):
            # Import Logic Here (Lazy Loading)
            try:
                from vision_module.interface import analyze_cable_image
                
                for uploaded_file in uploaded_files:
                    st.divider()
                    st.markdown(f"### 🖼️ Analyzing: {uploaded_file.name}")
                    
                    # Create Temp File
                    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") 
                    tfile.write(uploaded_file.read())
                    tfile.close() 
                    
                    # Layout
                    c1, c2 = st.columns(2)
                    c1.image(uploaded_file, caption="Original Image", use_container_width=True)
                    
                    with st.spinner(f"Processing {uploaded_file.name}..."):
                        processed_img, data = analyze_cable_image(tfile.name)
                        
                        # Handle Results
                        if data and "Error" in data[0]:
                            st.error(f"❌ {data[0]['Error']}")
                        elif processed_img is not None:
                            # Convert BGR to RGB
                            rgb_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
                            c2.image(rgb_img, caption="AI Result", use_container_width=True)
                            
                            if data:
                                st.markdown('<div class="success-box">✅ Detection Successful</div>', unsafe_allow_html=True)
                                df = pd.DataFrame(data)
                                st.table(df)
                            else:
                                st.warning("⚠️ No cable detected. Try adjusting lighting.")
                                
                    # Cleanup
                    os.unlink(tfile.name)

            except ImportError:
                st.error("❌ Error: 'vision_module' not found. Please check folder structure.")
            except Exception as e:
                st.error(f"❌ Unexpected Error: {e}")

# =========================================================
# MODULE 2: OCR & VALIDATION (EasyOCR + Logic)
# =========================================================
elif mode == "📄 Datasheet OCR & Validation":
    st.subheader("📝 Smart Datasheet Extraction")
    st.write("Upload datasheets or catalogs to extract technical specs and validate them.")
    
    uploaded_docs = st.file_uploader("Upload Documents", type=['jpg', 'png', 'jpeg', 'pdf', 'docx'], accept_multiple_files=True)
    
    if uploaded_docs:
        if st.button("🔍 Extract & Validate All", type="primary"):
            # Import Logic Here (Lazy Loading)
            try:
                from ocr_module.interface import extract_and_validate
                
                for uploaded_doc in uploaded_docs:
                    st.divider()
                    st.markdown(f"### 📄 Processing: {uploaded_doc.name}")
                    
                    # Handle File Extensions
                    file_ext = os.path.splitext(uploaded_doc.name)[1].lower()
                    suffix = file_ext if file_ext in ['.pdf', '.docx', '.jpg', '.png', '.jpeg'] else ".jpg"
                    
                    # Create Temp File
                    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                    tfile.write(uploaded_doc.read())
                    tfile.close()
                    
                    # Simple Preview for Images
                    if suffix in ['.jpg', '.png', '.jpeg']:
                         st.image(uploaded_doc, caption="Document Preview", width=250)
                    
                    with st.spinner(f"Reading {uploaded_doc.name}..."):
                        specs, report = extract_and_validate(tfile.name)
                        
                        # 1. Extracted Data Section
                        st.markdown("**📋 Extracted Specifications**")
                        # Clean Keys for Display (e.g., voltage_rating -> Voltage Rating)
                        clean_specs = {k.replace('_', ' ').title(): v for k, v in specs.items() if v}
                        
                        if clean_specs:
                            st.table(pd.DataFrame(list(clean_specs.items()), columns=["Parameter", "Value"]))
                        else:
                            st.warning("⚠️ No specifications could be extracted.")
                        
                        # 2. Validation Report Section
                        st.markdown("**🛡️ Engineering Validation**")
                        status = report.get("status", "UNKNOWN")
                        
                        if status == "READY":
                            st.markdown('<div class="success-box">✅ Status: APPROVED (Ready for Production)</div>', unsafe_allow_html=True)
                        elif status == "UNVERIFIABLE":
                            st.warning(f"⚠️ Status: {status} (Missing Critical Information)")
                        else:
                            st.markdown(f'<div class="error-box">❌ Status: {status} (Violations Found)</div>', unsafe_allow_html=True)
                        
                        # Show Specific Errors
                        if report.get("errors"):
                            for err in report["errors"]:
                                st.error(f"🔴 {err}")
                        elif status == "READY":
                            st.info("✨ No engineering violations detected.")

                    # Cleanup
                    os.unlink(tfile.name)

            except ImportError:
                st.error("❌ Error: 'ocr_module' not found. Please check folder structure.")
            except Exception as e:
                st.error(f"❌ System Error: {e}")

# ==========================================
# 5. FOOTER
# ==========================================
st.markdown("---")
st.markdown("<p style='text-align: center; color: #888;'>© 2025 SpecSense AI | Graduation Project System</p>", unsafe_allow_html=True)