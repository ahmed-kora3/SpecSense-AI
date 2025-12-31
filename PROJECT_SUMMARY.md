# 🔌 Unified Cable AI System - Complete Project Overview

## 📋 Project Structure

This is a **two-part integrated system** for comprehensive cable inspection and specification:

### **Part 1: Cable Detection & Physical Analysis System** 
📁 Location: `Cable_AI_System/`

**Purpose:** Detects cables in images using AI vision and estimates physical properties.

**Key Components:**
- **Model:** YOLOv8 (detection/segmentation)
- **Input:** Images of cable cross-sections
- **Process:**
  1. Image Detection → Bounding box detection
  2. Calibration → Convert pixels to mm (18.5 pixels = 1mm)
  3. Rule-Based Classification → Assigns specs based on diameter

**Main Files:**
- `train_model.py` - Trains YOLOv8 segmentation model
- `get_specs.py` - Runs inference and generates inspection reports
- `data.yaml` - Dataset configuration
- `Cable_Dataset/` - Training images and labels

**Output:** 
- Visual reports with bounding boxes
- CSV inspection results
- Estimated specifications (Voltage, Insulation, Sheath, etc.)

**Tech Stack:** PyTorch, OpenCV, YOLOv8, Ultralytics

---

### **Part 2: OCR & Specification Validation System**
📁 Location: `OCR-Model-main/`

**Purpose:** Extracts cable specifications from document images and validates against engineering standards.

**Key Components:**

#### **Stage 1: OCR Extraction**
- **Engine:** EasyOCR (multilingual - English & Arabic)
- **File:** `main.py`
- **Input:** Document/image containing cable specifications text
- **Process:** Optical character recognition with hybrid Regex pattern extraction
- **Output:** `validation/latest_specs.json`

#### **Stage 2: Post-OCR Correction**
- **Class:** `SpecCorrector` (in `src/extraction.py`)
- **Fixes:**
  - OCR errors (e.g., "NxS notation" parsing: "4x16mm2" → Cores: 4, Size: 16mm²)
  - Unit standardization (MΩkm → MΩ·km)
  - Ambiguity handling (marks unclear values as UNVERIFIABLE)

#### **Stage 3: Strict 10-Point Validation**
- **Class:** `CableValidator` (in `src/validation.py`)
- **Engineering Rules:**
  1. Cable Type validation
  2. Voltage consistency (no mixed AC/DC)
  3. Current/Size ampacity checks
  4. Insulation material validation
  5. Conductor count verification
  6. Sheath material checks
  7. Armor type validation
  8. Temperature operating range (-40°C to 105°C)
  9. Insulation resistance (≥1 MΩ)
  10. Physical cable dimensions

#### **Stage 4: Keyword Analysis**
- **Module:** `keyword_gen_module/keyword_tool.py`
- **Function:** Categorizes cables (Low/Medium Voltage) and generates indexing keywords

**Main Execution:**
- `main.py` → Extract specs from image
- `validation/valid.py` → Validate, correct, analyze
- `keyword_gen_module/keyword_tool.py` → Generate keywords

**Tech Stack:** EasyOCR, PyPDF2, python-docx, Pandas, SpaCy

---

## 🔄 System Integration Points

| Component | Input | Output | Purpose |
|-----------|-------|--------|---------|
| **Cable Detection** | Image of cable | Diameter + Estimated Specs | Physical inspection |
| **OCR Extraction** | Document/Spec Image | Raw specifications JSON | Data capture |
| **Correction Engine** | Raw OCR specs | Cleaned specifications | Error fixing |
| **Validation Engine** | Corrected specs | Pass/Fail + Violations | Quality assurance |
| **Keyword Analysis** | Validated specs | Categories + Keywords | Classification |

---

## 📊 Data Flow

```
Cable Image (JPG/PNG)
    ↓
[YOLOv8 Detection] → Diameter (mm)
    ↓
[Rule-Based Classification] → Estimated Specs (Voltage, Insulation, etc.)
    ↓
[Inspection Report] → CSV/JSON Output

Specification Document/Image
    ↓
[EasyOCR Extraction] → Raw Text/Specs JSON
    ↓
[SpecCorrector] → Cleaned Specifications
    ↓
[CableValidator] → 10-Point Engineering Check
    ↓
[Keyword Analysis] → Categories & Indexed Keywords
    ↓
[Final Report] → JSON/CSV with Validation Results
```

---

## 🎯 UI Requirements (For Unified Interface)

### **Key Features Needed:**

1. **Dual Input Module**
   - Cable image upload (for detection system)
   - Specification document upload (for OCR system)

2. **Processing Dashboard**
   - Real-time processing status
   - Progress indicators
   - Error/warning messages

3. **Results Display**
   - **Physical Analysis Tab**
     - Annotated image with bounding box
     - Diameter measurements
     - Estimated specifications
     - Status (Pass/Fail)
   
   - **Specification Validation Tab**
     - Extracted specifications table
     - Corrections applied
     - Validation violations (if any)
     - Confidence scores
   
   - **Keywords & Classification Tab**
     - Voltage category
     - Cable type
     - Top keywords
     - Search tags

4. **Export Options**
   - CSV (inspection results)
   - JSON (raw data)
   - PDF (formatted report)
   - Excel (with multiple sheets)

5. **Batch Processing**
   - Process multiple images
   - Batch validation
   - Comparison reports

---

## 🛠️ Technology Stack

**Backend:**
- Python 3.10+
- YOLOv8 (Ultralytics)
- EasyOCR
- PyTorch
- OpenCV

**Data Processing:**
- Pandas
- NumPy
- RegEx pattern matching

**Optional Enhancement:**
- FastAPI/Flask (for REST API)
- Streamlit/Tkinter (for UI)
- PostgreSQL (for database storage)

---

## 📁 Key Files for UI Integration

### Cable Detection System:
- `get_specs.py` - Main inference function
- `Cable_Dataset/` - Test images

### OCR System:
- `main.py` - Entry point
- `validation/valid.py` - Full pipeline execution
- `OCR-Model-main/keyword_gen_module/` - Keyword generation

---

## ✨ Next Steps for UI Development

1. **Choose UI Framework**
   - Streamlit (fastest, no frontend skills needed)
   - Flask + React (full-stack control)
   - Tkinter (simple desktop app)
   - PyQt/PySide (professional desktop)

2. **API Layer** (if using web UI)
   - Wrap both systems in REST endpoints
   - Handle file uploads
   - Manage background processing

3. **Database** (optional)
   - Store inspection history
   - Track corrections
   - Generate reports

4. **Config Management**
   - Model paths
   - Calibration factors
   - Validation rules

