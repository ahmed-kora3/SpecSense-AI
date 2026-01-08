import os
import sys

# Ensure we can import from src relative to this file
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

try:
    from .src.core_ocr import OCREngine
    from .src.extraction import SpecificationExtractor, SpecCorrector
    from .src.validation import CableValidator
except ImportError:
    # Fallback for when running as script vs package
    from src.core_ocr import OCREngine
    from src.extraction import SpecificationExtractor, SpecCorrector
    from src.validation import CableValidator

# Import Keyword Tool at module level
try:
    from ocr_module.keyword_gen_module.keyword_tool import CableClassifier, KeywordExtractor
except ImportError:
    try:
        from .keyword_gen_module.keyword_tool import CableClassifier, KeywordExtractor
    except ImportError:
        sys.path.append(os.path.join(os.path.dirname(__file__), 'keyword_gen_module'))
        from keyword_tool import CableClassifier, KeywordExtractor


def extract_and_validate(image_path):
    """
    Extracts cable specifications from an image and validates them.
    
    Args:
        image_path (str): Path to the image file.
        
    Returns:
        tuple: (specs_dict, validation_report_dict)
    """
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image not found: {image_path}")

    try:
        # 1. Initialize OCR Engine
        ocr = OCREngine(languages=['en'])
        
        # 2. Read Text
        results = ocr.read_image(image_path, detail=0)
        full_text = " ".join(results)
        
        # 3. Extract Specifications from Text
        extractor = SpecificationExtractor()
        raw_specs = extractor.extract_specs(full_text)
        
        # 4. Apply Corrections (Fix common OCR errors)
        corrector = SpecCorrector()
        corrected_specs, logs = corrector.correct_all(raw_specs)
        
        # 5. Validate against Engineering Rules
        validator = CableValidator()
        validation_report = validator.validate_cable(corrected_specs)
        
        # Add correction logs to report for visibility if needed
        validation_report['correction_logs'] = logs
        
        # =============================================
        # 6. NEW: Keyword Generation Integration
        # =============================================
        try:
            classifier = CableClassifier()
            kw_extractor = KeywordExtractor()
            
            category = classifier.classify(full_text)
            keywords = kw_extractor.extract_keywords(full_text)
            
            # Merge into specs
            corrected_specs['cable_category'] = category
            if keywords.get('Top Terms'):
                corrected_specs['top_terms'] = ", ".join(keywords['Top Terms'])
            if keywords.get('Conductor Type'):
                corrected_specs['conductor_type_keyword'] = ", ".join(keywords['Conductor Type'])

            # Store full keyword details in report for UI "Generate Keywords" button
            validation_report['keyword_details'] = {
                "category": category,
                "extracted_data": keywords,
                "full_text_debug": full_text
            }

        except Exception as kw_error:
            validation_report.setdefault('warnings', []).append(f"Keyword Gen Failed: {str(kw_error)}")
            validation_report['keyword_details'] = {
                "category": "Error",
                "extracted_data": {},
                "full_text_debug": full_text
            }
        # =============================================
        
        return corrected_specs, validation_report
        
    except Exception as e:
        # Return empty specs and an error report
        error_report = {
            "status": "ERROR",
            "valid": False,
            "errors": [str(e)],
            "warnings": []
        }
        return {}, error_report