
import os
import sys

# Add project root to path
sys.path.append(os.getcwd())

from ocr_module.interface import extract_and_validate

def test_image(image_path):
    print(f"Testing {image_path}...")
    if not os.path.exists(image_path):
        print(f"Error: {image_path} not found")
        return

    try:
        specs, report = extract_and_validate(image_path)
        print("Specs:", specs)
        print("Report:", report)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_image("ocr_module/data/raw/test5.jpeg")
    test_image("ocr_module/data/raw/test11.png")
