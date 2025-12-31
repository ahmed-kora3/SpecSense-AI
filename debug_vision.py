import cv2
import os
from ultralytics import YOLO

def debug_model():
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(base_dir, "vision_module", "best.pt")
    
    # Use the specific user uploaded image if possible
    img_path = "C:/Users/HP/.gemini/antigravity/brain/50096220-b2eb-4670-a8e2-d9eb80a2feb3/uploaded_image_1767211538158.png"
    if not os.path.exists(img_path):
         # Fallback to train image if user image is gone
         img_path = os.path.join(base_dir, "vision_module", "Cable_Dataset", "images", "train", "image-1.jpg.jpg")
    
    print(f"DEBUG: Model Path: {model_path}", flush=True)
    print(f"DEBUG: Image Path: {img_path}", flush=True)
    
    if not os.path.exists(model_path):
        print("❌ Model 'best.pt' NOT FOUND.", flush=True)
        return
        
    if not os.path.exists(img_path):
        print("❌ Test image NOT FOUND.", flush=True)
        return

    # Load Model
    print("Loading model...", flush=True)
    model = YOLO(model_path)
    
    # Print Class Names
    print("\nModel Classes:", flush=True)
    print(model.names, flush=True)
    
    with open("vision_classes.txt", "w") as f:
        f.write(str(model.names))
        
    # Run Inference
    print("\nRunning Inference...", flush=True)
    results = model(img_path, conf=0.01) # Ultra Low threshold
    
    print("\n--- RESULTS ---")
    for r in results:
        print(f"Boxes found: {len(r.boxes)}")
        for box in r.boxes:
            print(f" - Class: {int(box.cls)} ({model.names[int(box.cls)]}) | Conf: {float(box.conf):.2f}")
            
    if len(results[0].boxes) == 0:
        print("\n⚠️ NO DETECTIONS FOUND.")
        print("Possible causes:\n1. Model is not trained on these images.\n2. Model is generic (COCO) and 'cable' is not a class.\n3. Defective training.")

if __name__ == "__main__":
    debug_model()
