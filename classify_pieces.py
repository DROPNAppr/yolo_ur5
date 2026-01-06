from cam import capture_image
from yolo_inference import run_yolo
from robot_client import RobotClient

ROBOT_IP = "192.168.1.100"  # IP du PC robot

def main():
    # 1. Capture image
    image_path = capture_image("image.jpg")

    # 2. YOLO
    detections = run_yolo(image_path)

    bad = [d["piece_id"] for d in detections if d["status"] == "BAD"]
    good = [d["piece_id"] for d in detections if d["status"] == "GOOD"]

    print("BAD :", bad)
    print("GOOD :", good)

    # 3. Envoi au robot
    client = RobotClient(ROBOT_IP)
    client.connect()
    response = client.send_sorting_command(bad, good)
    client.disconnect()

    print("Réponse robot :", response)

if __name__ == "__main__":
    main()
