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
        # Using 'en' as default. You can add 'ar' if Arabic support determines it's needed.
        ocr = OCREngine(languages=['en'])
        
        # 2. Read Text
        # detail=0 returns a list of strings
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