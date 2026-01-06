"""
main.py
Point d'entrée principal du système Vision + Robot

À lancer sur le Raspberry Pi :
python main.py
"""

from cam import capture_image          # Capture image caméra
from yolo_inference import run_yolo    # Inference YOLO
from robot_client import RobotClient   # Client robot
import time

# =========================
# CONFIG
# =========================
ROBOT_IP = "192.168.137.1"   # IP du PC RoboDK (serveur)
IMAGE_PATH = "image.jpg"

# =========================
# MAIN PIPELINE
# =========================
def main():
    print("🚀 Démarrage du système Vision + Robot")

    # 1️⃣ Capture image
    print("📸 Capture de l'image...")
    image_path = capture_image(IMAGE_PATH)

    # 2️⃣ YOLO inference
    print("👁️ Analyse YOLO...")
    detections = run_yolo(image_path)

    if not detections or len(detections) == 0:
        print("⚠️ Aucune pièce détectée, arrêt du cycle")
        return

    # 3️⃣ Séparation GOOD / BAD
    bad_pieces = [d["piece_id"] for d in detections if d["status"] == "BAD"]
    good_pieces = [d["piece_id"] for d in detections if d["status"] == "GOOD"]

    print(f"🔴 Pièces BAD : {bad_pieces}")
    print(f"🟢 Pièces GOOD : {good_pieces}")

    # 4️⃣ Connexion robot
    print("🌐 Connexion au robot...")
    client = RobotClient(ROBOT_IP)

    if not client.connect():
        print("❌ Impossible de se connecter au robot")
        return

    try:
        # Optionnel : retour HOME
        print("🏠 Retour HOME")
        client.move_home()
        time.sleep(1)

        # =========================
        # 5️⃣ TRAITEMENT DES PIÈCES BAD
        # =========================
        print("\n===== 🔴 TRAITEMENT BAD =====")

        for pid in bad_pieces:
            print(f"➡️ Pick BAD piece : {pid}")

            response = client.pick_piece(pid)
            if response is None or response.get("status") != "success":
                print(f"❌ Échec pick pièce {pid}")
                continue

            time.sleep(0.5)

            print(f"📦 Place {pid} dans BAD bin")
            response = client.place_piece("bad bin")
            if response is None or response.get("status") != "success":
                print(f"❌ Échec placement BAD bin pour {pid}")
                continue

            time.sleep(0.5)

        # =========================
        # 6️⃣ TRAITEMENT DES PIÈCES GOOD
        # =========================
        print("\n===== 🟢 TRAITEMENT GOOD =====")

        for pid in good_pieces:
            print(f"➡️ Pick GOOD piece : {pid}")

            response = client.pick_piece(pid)
            if response is None or response.get("status") != "success":
                print(f"❌ Échec pick pièce {pid}")
                continue

            time.sleep(0.5)

            print(f"📦 Place {pid} dans GOOD bin")
            response = client.place_piece("good bin")
            if response is None or response.get("status") != "success":
                print(f"❌ Échec placement GOOD bin pour {pid}")
                continue

            time.sleep(0.5)

        print("\n✅ Cycle terminé avec succès")

    finally:
        client.disconnect()
        print("🔌 Déconnexion robot")

# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
