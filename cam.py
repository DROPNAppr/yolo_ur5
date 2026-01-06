from ultralytics import YOLO
import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading

# =========================
# CONFIGURATION
# =========================
MODEL_PATH = "yolo.pt"   # mets ton modèle dans le même dossier
CONF_THRESH = 0.6
CAMERA_ID = 0            # caméra externe USB = 1 (PC interne = 0)

# Paramètres d'ajustement luminosité/contraste
CONTRAST = 1.5       # augmenter le contraste (> 1.0)
BRIGHTNESS = -30         # diminuer la luminosité (négatif)

# =========================
# FONCTION AJUSTEMENT LUMINOSITÉ/CONTRASTE
# =========================
def adjust_brightness_contrast(frame, contrast=1.0, brightness=0):
    """Ajuste le contraste et la luminosité de l'image"""
    # Appliquer le contraste et la luminosité
    adjusted = cv2.convertScaleAbs(frame, alpha=contrast, beta=brightness)
    return adjusted

# =========================
# FONCTION POUR DÉTERMINER LA CAMÉRA DISPONIBLE
# =========================
def find_available_camera(start_id=1, max_id=10):
    """Détecte les caméras disponibles, en commençant par la caméra externe"""
    for i in range(start_id, max_id):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"✅ Caméra détectée à l'index {i}")
            return cap, i
        cap.release()
    return None, -1

# =========================
# FONCTION CAPTURE IMAGE
# =========================
def capture_image(image_path):
    """
    Capture une image via la caméra et l'enregistre.
    
    Args:
        image_path (str): chemin où enregistrer l'image
        
    Returns:
        str: chemin de l'image enregistrée, ou None en cas d'erreur
    """
    print("🔄 Chargement du modèle YOLO...")
    model = YOLO(MODEL_PATH)
    print("✅ Modèle chargé avec succès")
    
    # Essayer d'abord la caméra externe (ID=1)
    cap, camera_id = find_available_camera(start_id=CAMERA_ID, max_id=10)

    if cap is None:
        print("❌ Aucune caméra externe trouvée. Tentative avec caméra interne...")
        cap, camera_id = find_available_camera(start_id=0, max_id=1)

    if cap is None or not cap.isOpened():
        print("❌ Erreur : aucune caméra détectée")
        return None

    print(f"✅ Caméra activée (ID: {camera_id})")
    
    # Capturer une image
    ret, frame = cap.read()
    
    if not ret:
        print("❌ Erreur lecture image")
        cap.release()
        return None
    
    # Ajuster la luminosité et le contraste
    frame = adjust_brightness_contrast(frame, contrast=CONTRAST, brightness=BRIGHTNESS)
    
    # Enregistrer l'image
    cv2.imwrite(image_path, frame)
    print(f"✅ Image enregistrée : {image_path}")
    
    # Libérer la caméra
    cap.release()
    
    return image_path


# =========================
# INTERFACE TKINTER AVEC YOLO EN TEMPS RÉEL
# =========================
def capture_with_yolo_ui():
    """
    Affiche une interface Tkinter avec :
    - Flux caméra en temps réel
    - Détections YOLO (GOOD/BAD) avec numérotation STABLE
    - Boutons pour confirmer (Pick Good / Pick Bad)
    
    Returns:
        tuple: (good_pieces, bad_pieces) - listes des pièces avec numérotation
    """
    print("🔄 Initialisation de l'interface YOLO...")
    model = YOLO(MODEL_PATH)
    
    # Essayer d'abord la caméra externe (ID=1)
    cap, camera_id = find_available_camera(start_id=CAMERA_ID, max_id=10)

    if cap is None:
        print("❌ Aucune caméra externe trouvée. Tentative avec caméra interne...")
        cap, camera_id = find_available_camera(start_id=0, max_id=1)

    if cap is None or not cap.isOpened():
        print("❌ Erreur : aucune caméra détectée")
        return [], []

    print(f"✅ Caméra activée (ID: {camera_id})")
    
    # Variables partagées - TRACKING STABLE DES PIÈCES
    state = {
        "running": True,
        "current_detections": [],
        "good_pieces": [],
        "bad_pieces": [],
        "confirmed": False,
        "piece_tracker": {},  # {centroid_key: original_id}
        "next_piece_id": 1,
        "piece_history": {}  # {original_id: {"status": "GOOD"/"BAD", "last_seen": frame_count}}
    }
    
    # =========================
    # FENÊTRE TKINTER - THÈME SOMBRE
    # =========================
    root = tk.Tk()
    root.title("🎥 Vision System - YOLO Détection")
    root.geometry("1000x700")
    root.configure(bg="#1e1e1e")
    
    # Couleurs thème sombre
    dark_bg = "#1e1e1e"
    dark_fg = "#ffffff"
    dark_secondary = "#2d2d2d"
    dark_accent = "#0d7377"  # Bleu teal
    
    # Frame pour la caméra
    camera_frame = tk.Frame(root, bg=dark_bg)
    camera_frame.grid(row=0, column=0, rowspan=3, padx=10, pady=10, sticky="nsew")
    
    canvas = tk.Canvas(camera_frame, width=700, height=500, bg="black", highlightthickness=0)
    canvas.pack()
    
    # Frame pour les détections
    info_frame = tk.Frame(root, bg=dark_secondary)
    info_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    
    label_detected = tk.Label(info_frame, text="📋 PIÈCES DÉTECTÉES", 
                              font=("Arial", 12, "bold"), bg=dark_secondary, fg=dark_fg)
    label_detected.pack()
    
    # Listbox pour les détections (thème sombre)
    listbox = tk.Listbox(info_frame, width=35, height=20, font=("Arial", 9),
                         bg=dark_secondary, fg=dark_fg, selectmode=tk.SINGLE,
                         highlightthickness=0, borderwidth=0)
    listbox.pack(fill="both", expand=True, padx=5, pady=5)
    
    # Frame pour les boutons
    button_frame = tk.Frame(root, bg=dark_bg)
    button_frame.grid(row=2, column=1, padx=10, pady=10, sticky="ew")
    
    def on_start():
        """Démarre le traitement des pièces"""
        state["confirmed"] = True
        state["running"] = False
        root.quit()
    
    def on_quit():
        """Quitter l'application"""
        state["running"] = False
        root.quit()
    
    # Bouton START
    btn_start = tk.Button(button_frame, text="▶ START", command=on_start,
                         bg=dark_accent, fg=dark_fg, font=("Arial", 11, "bold"),
                         padx=15, pady=8, relief=tk.FLAT, cursor="hand2")
    btn_start.pack(side="left", padx=5, pady=5, fill="both", expand=True)
    
    # Bouton QUITTER
    btn_quit = tk.Button(button_frame, text="✕ QUITTER", command=on_quit,
                        bg="#d32f2f", fg=dark_fg, font=("Arial", 11, "bold"),
                        padx=15, pady=8, relief=tk.FLAT, cursor="hand2")
    btn_quit.pack(side="left", padx=5, pady=5, fill="both", expand=True)
    
    # Bind touche Q pour quitter
    root.bind('q', lambda e: on_quit())
    root.bind('Q', lambda e: on_quit())
    
    # =========================
    # FONCTION DE TRACKING
    # =========================
    def get_centroid(box):
        """Calcule le centroïde d'une boîte de détection"""
        x1, y1, x2, y2 = box.xyxy[0]
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        return (float(cx), float(cy))
    
    def match_detection_to_piece(centroid, threshold=50):
        """
        Associe une détection à une pièce existante ou crée une nouvelle.
        Utilise la distance euclidienne entre centroïdes.
        """
        best_match = None
        best_distance = threshold
        
        # Chercher la pièce la plus proche
        for tracked_centroid, piece_id in state["piece_tracker"].items():
            dist = ((centroid[0] - tracked_centroid[0])**2 + 
                   (centroid[1] - tracked_centroid[1])**2) ** 0.5
            
            if dist < best_distance:
                best_distance = dist
                best_match = (tracked_centroid, piece_id)
        
        # Si une pièce correspondante existe, la réutiliser
        if best_match:
            old_centroid, piece_id = best_match
            # Mettre à jour la position du tracking
            del state["piece_tracker"][old_centroid]
            state["piece_tracker"][centroid] = piece_id
            return piece_id
        
        # Sinon, créer une nouvelle pièce
        new_piece_id = state["next_piece_id"]
        state["next_piece_id"] += 1
        state["piece_tracker"][centroid] = new_piece_id
        return new_piece_id
    
    # =========================
    # BOUCLE DE CAPTURE
    # =========================
    def update_frame():
        """Met à jour le flux caméra et affiche les détections"""
        if not state["running"]:
            return
        
        ret, frame = cap.read()
        if not ret:
            print("❌ Erreur lecture image")
            state["running"] = False
            root.quit()
            return
        
        # Ajuster luminosité/contraste
        frame = adjust_brightness_contrast(frame, contrast=CONTRAST, brightness=BRIGHTNESS)
        
        # Inference YOLO
        results = model(frame, conf=CONF_THRESH)
        
        # Récupérer les résultats
        detections = results[0].boxes
        
        # Variables temporaires pour cette frame
        current_frame_pieces = {}  # {piece_id: {"centroid": ..., "status": ..., "box": ...}}
        pieces_with_position = []  # Liste pour tri spatial
        
        if detections is not None and len(detections) > 0:
            for box in detections:
                # Obtenir le centroïde de cette détection
                centroid = get_centroid(box)
                
                # Associer à une pièce existante ou créer une nouvelle
                piece_id = match_detection_to_piece(centroid)
                
                # Déterminer le statut
                cls_id = int(box.cls[0])
                status = "BAD" if cls_id == 0 else "GOOD"
                
                # Stocker dans l'historique
                state["piece_history"][piece_id] = {
                    "status": status,
                    "last_seen": True
                }
                
                current_frame_pieces[piece_id] = {
                    "centroid": centroid,
                    "status": status,
                    "box": box
                }
                
                # Ajouter à la liste avec position pour tri spatial
                pieces_with_position.append({
                    "original_piece_id": piece_id,
                    "x": centroid[0],
                    "y": centroid[1],
                    "status": status,
                    "box": box
                })
        
        # =========================
        # TRI SPATIAL - NUMÉROTATION FIXE PAR POSITION
        # =========================
        # 6 positions fixes:
        # Haut:  4 (gauche)  3 (centre)  2 (droite)
        # Bas:   5 (gauche)  6 (centre)  1 (droite)
        
        position_to_number = {}
        
        if pieces_with_position:
            frame_height = frame.shape[0]
            frame_width = frame.shape[1]
            median_y = frame_height / 2
            median_x = frame_width / 2
            
            # Séparer haut et bas
            top_pieces = [p for p in pieces_with_position if p["y"] < median_y]
            bottom_pieces = [p for p in pieces_with_position if p["y"] >= median_y]
            
            # Trier chaque groupe de gauche à droite (par X)
            top_pieces.sort(key=lambda p: p["x"])
            bottom_pieces.sort(key=lambda p: p["x"])
            
            # Assigner les numéros fixes selon la position
            # Haut: 4, 3, 2 (de gauche à droite)
            top_numbers = [4, 3, 2]
            for idx, piece in enumerate(top_pieces):
                if idx < len(top_numbers):
                    position_to_number[piece["original_piece_id"]] = top_numbers[idx]
            
            # Bas: 5, 6, 1 (de gauche à droite)
            bottom_numbers = [5, 6, 1]
            for idx, piece in enumerate(bottom_pieces):
                if idx < len(bottom_numbers):
                    position_to_number[piece["original_piece_id"]] = bottom_numbers[idx]
        
        
        # Créer la liste affichée avec les IDs de position
        good_pieces = []
        bad_pieces = []
        detection_info = []
        
        # Trier par numéro de position
        for piece_id in sorted(position_to_number.keys(), key=lambda x: position_to_number[x]):
            position_num = position_to_number[piece_id]
            status = current_frame_pieces[piece_id]["status"]
            
            if status == "GOOD":
                good_pieces.append({"piece_id": position_num, "status": "GOOD"})
                detection_info.append(f"🟢 Piece {position_num}: GOOD")
            else:
                bad_pieces.append({"piece_id": position_num, "status": "BAD"})
                detection_info.append(f"🔴 Piece {position_num}: BAD")
        
        if not detection_info:
            detection_info.append("⚠️ Aucune pièce détectée")
        
        # Stocker les détections
        state["current_detections"] = current_frame_pieces
        state["good_pieces"] = good_pieces
        state["bad_pieces"] = bad_pieces
        
        # Afficher l'image annotée
        annotated = results[0].plot()
        
        # AJOUTER LES TAGS VISUELS AUX PIÈCES
        if pieces_with_position:
            for piece_info in pieces_with_position:
                original_id = piece_info["original_piece_id"]
                position_num = position_to_number.get(original_id, "?")
                box = piece_info["box"]
                status = piece_info["status"]
                
                # Arrondir les coordonnées
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                
                # Couleur selon le statut
                if status == "BAD":
                    color = (0, 0, 255)  # BGR: Rouge
                    text_color = (255, 255, 255)  # Blanc
                else:
                    color = (0, 255, 0)  # BGR: Vert
                    text_color = (255, 255, 255)  # Blanc
                
                # Dessiner un rectangle autour de la boîte
                cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 3)
                
                # Créer un tag avec le numéro de position
                tag_height = 40
                tag_width = 60
                tag_x = x1
                tag_y = max(0, y1 - tag_height - 5)
                
                # Dessiner le rectangle du tag
                cv2.rectangle(
                    annotated,
                    (tag_x, tag_y),
                    (tag_x + tag_width, tag_y + tag_height),
                    color,
                    -1  # Remplir le rectangle
                )
                
                # Dessiner le numéro dans le tag
                cv2.putText(
                    annotated,
                    f"#{position_num}",
                    (tag_x + 5, tag_y + 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.2,
                    text_color,
                    2
                )
        
        # Convertir pour Tkinter
        frame_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
        frame_resized = cv2.resize(frame_rgb, (700, 500))
        img_pil = Image.fromarray(frame_resized)
        img_tk = ImageTk.PhotoImage(img_pil)
        
        canvas.create_image(0, 0, anchor="nw", image=img_tk)
        canvas.image = img_tk
        
        # Mettre à jour la listbox
        listbox.delete(0, tk.END)
        for info in detection_info:
            listbox.insert(tk.END, info)
        
        # Récursif - appelle la fonction chaque 30ms
        root.after(30, update_frame)
    
    # Lancer la mise à jour
    update_frame()
    
    # Afficher la fenêtre
    root.mainloop()
    
    # Libérer la caméra
    cap.release()
    cv2.destroyAllWindows()
    
    print(f"\n✅ Détection terminée")
    print(f"🟢 Pièces GOOD : {[p['piece_id'] for p in state['good_pieces']]}")
    print(f"🔴 Pièces BAD : {[p['piece_id'] for p in state['bad_pieces']]}")
    
    return state["good_pieces"], state["bad_pieces"]


# =========================
# BOUCLE DE DÉMONSTRATION (mode interactif)
# =========================
def main_demo():
    """Boucle de démonstration avec affichage en temps réel"""
    print("🔄 Chargement du modèle YOLO...")
    model = YOLO(MODEL_PATH)
    print("✅ Modèle chargé avec succès")
    
    # Essayer d'abord la caméra externe (ID=1)
    cap, camera_id = find_available_camera(start_id=CAMERA_ID, max_id=10)

    if cap is None:
        print("❌ Aucune caméra externe trouvée. Tentative avec caméra interne...")
        cap, camera_id = find_available_camera(start_id=0, max_id=1)

    if cap is None or not cap.isOpened():
        print("❌ Erreur : aucune caméra détectée")
        return

    print(f"✅ Caméra activée (ID: {camera_id})")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Erreur lecture image")
            break

        # Ajuster la luminosité et le contraste
        frame = adjust_brightness_contrast(frame, contrast=CONTRAST, brightness=BRIGHTNESS)

        # Inference YOLO
        results = model(frame, conf=CONF_THRESH)

        # Récupérer les résultats
        detections = results[0].boxes

        print("----- FRAME -----")
        if detections is None or len(detections) == 0:
            print("Aucune pièce détectée")
        else:
            for box in detections:
                cls_id = int(box.cls[0])
                label = model.names[cls_id]
                conf = float(box.conf[0])

                print(f"✔ Détection : {label} | confiance = {conf:.2f}")

        # Affichage image annotée
        annotated = results[0].plot()
        cv2.imshow("YOLO Detection", annotated)

        # Quitter avec 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("🛑 Arrêt demandé par l'utilisateur")
            break

    # =========================
    # NETTOYAGE
    # =========================
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Caméra arrêtée, programme terminé")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main_demo()

