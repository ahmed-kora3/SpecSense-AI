
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from ocr_module.interface import extract_and_validate

def verify_file(path):
    print(f"Verifying {path}...")
    try:
        specs, report = extract_and_validate(path)
        
        category = specs.get('cable_category')
        top_terms = specs.get('top_terms')
        
        print(f"  Category: {category}")
        print(f"  Top Terms: {top_terms}")
        
        if category and top_terms:
            print("  [PASS] - New fields found.")
        else:
            print("  [FAIL] - New fields missing.")
            
    except Exception as e:
        print(f"  [ERROR] - {e}")

if __name__ == "__main__":
    verify_file("ocr_module/data/raw/test5.jpeg")
    verify_file("ocr_module/data/raw/test11.png")
