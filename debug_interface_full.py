
import os
import sys
import traceback

# Add project root
sys.path.append(os.getcwd())

print("--- STARTING DEBUG ---")
try:
    from ocr_module.interface import extract_and_validate
    print("Imported extract_and_validate successfully.")
    
    # Run on a test file
    img_path = "ocr_module/data/raw/test5.jpeg"
    if os.path.exists(img_path):
        specs, report = extract_and_validate(img_path)
        print("Execution complete.")
        print(f"Category: {specs.get('cable_category')}")
        print(f"Top Terms: {specs.get('top_terms')}")
        
    else:
        print(f"File not found: {img_path}")
        
except Exception as e:
    print("CRITICAL ERROR during execution:")
    traceback.print_exc()

print("--- END DEBUG ---")
