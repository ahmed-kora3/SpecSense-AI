import streamlit as st
import pandas as pd
import cv2
import numpy as np
import tempfile
import os
from PIL import Image

# --- Page Config ---
st.set_page_config(page_title="SpecSense AI", layout="wide", page_icon="⚡")

# --- Styling ---
st.markdown("""
    <style>
    .header-title { font-size: 3rem; font-weight: 800; color: #0E1117; text-align: center; }
    .header-sub { font-size: 1.2rem; color: #555; text-align: center; margin-bottom: 25px; }
    .success-box { padding: 15px; background-color: #D4EDDA; color: #155724; border-radius: 5px; margin-bottom: 10px; }
    .error-box { padding: 15px; background-color: #F8D7DA; color: #721C24; border-radius: 5px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- Header ---
st.markdown('<div class="header-title">⚡ SpecSense AI</div>', unsafe_allow_html=True)
st.markdown('<div class="header-sub">Intelligent Cable Inspection & Document Analysis System</div>', unsafe_allow_html=True)
st.divider()

# --- Sidebar ---
st.sidebar.title("🎛️ System Control")
mode = st.sidebar.radio("Select Module:", 
    ["👁️ Vision Inspection (Cross-Section)", 
     "📄 Datasheet OCR & Validation"])

st.sidebar.info("✅ System Active\n🚀 GPU Acceleration: Enabled")

# =========================================================
# MODULE 1: VISION INSPECTION (YOLO)
# =========================================================
# =========================================================
# MODULE 1: VISION INSPECTION (YOLO)
# =========================================================
if mode == "👁️ Vision Inspection (Cross-Section)":
    st.subheader("🔍 Automated Geometry Analysis")
    st.write("Upload cross-section images to detect cable diameter and defects.")
    
    uploaded_files = st.file_uploader("Upload Images", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
    
    if uploaded_files:
        if st.button("🚀 Start AI Analysis", type="primary"):
            from vision_module.interface import analyze_cable_image
            
            for uploaded_file in uploaded_files:
                st.divider()
                st.markdown(f"### 🖼️ Analyzing: {uploaded_file.name}")
                
                # Save temp
                tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") 
                tfile.write(uploaded_file.read())
                tfile.close() 
                
                c1, c2 = st.columns(2)
                c1.image(uploaded_file, caption="Original Image", use_container_width=True)
                
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    try:
                        processed_img, data = analyze_cable_image(tfile.name)
                        
                        if data and "Error" in data[0]:
                            st.error(f"❌ {data[0]['Error']}")
                        elif processed_img is not None:
                            # Convert colors for display
                            rgb_img = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
                            c2.image(rgb_img, caption="AI Result", use_container_width=True)
                            
                            if data:
                                st.success(f"✅ Analysis Complete")
                                df = pd.DataFrame(data)
                                st.table(df)
                            else:
                                st.warning("⚠️ No cable detected.")
                    except ImportError:
                        st.error("❌ 'vision_module' missing or corrupt.")
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
            from ocr_module.interface import extract_and_validate
            
            for uploaded_doc in uploaded_docs:
                st.divider()
                st.markdown(f"### 📄 Processing: {uploaded_doc.name}")
                
                # Handle File Type
                if uploaded_doc.type == "application/pdf":
                    suffix = ".pdf"
                elif uploaded_doc.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or uploaded_doc.name.endswith(".docx"):
                    suffix = ".docx"
                else:
                    suffix = ".jpg"
                    
                tfile = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
                tfile.write(uploaded_doc.read())
                tfile.close()
                
                # Preview (Small)
                if suffix == ".jpg":
                     st.image(uploaded_doc, caption="Preview", width=200)
                
                with st.spinner(f"Reading {uploaded_doc.name}..."):
                    try:
                        specs, report = extract_and_validate(tfile.name)
                        
                        # 1. Show Extracted Data
                        st.markdown("**📋 Extracted Specifications**")
                        clean_specs = {k.replace('_', ' ').title(): v for k, v in specs.items() if v}
                        if clean_specs:
                            st.table(pd.DataFrame(list(clean_specs.items()), columns=["Parameter", "Value"]))
                        else:
                            st.warning("No specifications found.")
                        
                        # 2. Show Validation Report
                        st.markdown("**🛡️ Engineering Validation**")
                        status = report.get("status", "UNKNOWN")
                        
                        if status == "READY":
                            st.success("✅ Status: APPROVED (Ready)")
                        elif status == "UNVERIFIABLE":
                            st.warning(f"⚠️ Status: {status} (Missing Critical Info)")
                        else:
                            st.error(f"❌ Status: {status} (Violations Found)")
                        
                        if report.get("errors"):
                            for err in report["errors"]:
                                st.error(f"  - {err}")

                    except Exception as e:
                        st.error(f"❌ System Error: {e}")

# --- Footer ---
st.markdown("---")
st.markdown("© 2025 SpecSense AI | Graduation Project")