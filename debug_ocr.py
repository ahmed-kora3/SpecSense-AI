import os
import sys

# Ensure imports work
sys.path.append(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), 'ocr_module', 'src'))
sys.path.append(os.path.join(os.getcwd(), 'ocr_module'))

from ocr_module.src.core_ocr import OCREngine
from ocr_module.src.extraction import SpecificationExtractor, SpecCorrector
from ocr_module.src.validation import CableValidator

def debug_ocr_image():
    # Test specific invalid files identified by user
    files_to_test = [
        "c:/Users/HP/Desktop/Cable_AI_System - Copy/ocr_module/data/raw/test5.jpeg",
        "c:/Users/HP/Desktop/Cable_AI_System - Copy/ocr_module/data/raw/test11.png"
    ]
    
    ocr = OCREngine(languages=['en'])
    
    for img_path in files_to_test:
        print(f"\n{'='*40}")
        print(f"Testing: {os.path.basename(img_path)}")
        
        if not os.path.exists(img_path):
            print("❌ File not found.")
            continue
    
        try:
            results = ocr.read_image(img_path, detail=0)
            
            full_text = " ".join(results)
            print(f"\n--- FULL TEXT for {os.path.basename(img_path)} ---", flush=True)
            print(full_text.encode('utf-8', errors='replace').decode('utf-8'))
            
            # EXTRACT AND VALIDATE TO SEE WHY IT FAILS
            extractor = SpecificationExtractor()
            raw_specs = extractor.extract_specs(full_text)
            print(f"\n--- EXTRACTED SPECS ---", flush=True)
            print(raw_specs)
            
            corrector = SpecCorrector()
            corrected_specs, _ = corrector.correct_all(raw_specs)
            
            validator = CableValidator()
            report = validator.validate_cable(corrected_specs)
            
            print("\n--- VALIDATION REPORT ---", flush=True)
            print(f"Status: {report['status']}")
            for err in report['errors']:
                print(f" - {err}")
            print("\n" + "="*40, flush=True)
                
        except Exception as e:
            print(f"\n❌ OCR Failed: {e}")

if __name__ == "__main__":
    with open("debug_output.txt", "w", encoding="utf-8") as f:
        sys.stdout = f
        debug_ocr_image()
        sys.stdout = sys.__stdout__
