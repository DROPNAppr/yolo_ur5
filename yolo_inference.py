from ultralytics import YOLO

# Le modèle est dans le MÊME dossier que ce fichier
model = YOLO("yolo.pt")

def run_yolo(image_path):
    results = model(image_path)[0]

    detections = []

    for i, box in enumerate(results.boxes):
        cls_id = int(box.cls[0])

        status = "BAD" if cls_id == 0 else "GOOD"

        detections.append({
            "piece_id": i + 1,
            "status": status
        })

    return detections
