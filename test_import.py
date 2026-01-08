
import sys
import os
sys.path.append(os.getcwd())

print("Attempting import...")
try:
    from ocr_module.keyword_gen_module.keyword_tool import CableClassifier
    print("Import Successful")
    c = CableClassifier()
    print("Class Instantiated")
except Exception as e:
    print(f"Import Failed: {e}")
    import traceback
    traceback.print_exc()
