"""
main.py
Point d’entrée principal du système Vision + Robot

Fonctionnement :
1. Le robot va en position HOME
2. Capture d’image via caméra
3. Détection et classification des pièces avec YOLO
4. Séparation des pièces GOOD / BAD
5. Pick & Place automatique vers les bacs correspondants

À lancer sur le Raspberry Pi :
python main.py
"""

import time
import tkinter as tk
from tkinter import messagebox
from cam import capture_with_yolo_ui
from robot_client import RobotClient


# =========================
# CONFIGURATION
# =========================
ROBOT_IP = "192.168.137.132"
IMAGE_PATH = "image.jpg"

GOOD_BIN_NAME = "good bin"
BAD_BIN_NAME = "bad bin"


# =========================
# INTERFACE CONNEXION ROBOT
# =========================
def show_robot_connection_dialog(default_ip="192.168.137.132"):
    """
    Affiche une fenetre tkinter pour configurer l'adresse IP du robot.
    
    Args:
        default_ip (str): Adresse IP par defaut
        
    Returns:
        str: Adresse IP saisie par l'utilisateur, ou None si annulation
    """
    robot_ip = [None]  # Utiliser une liste pour pouvoir modifier dans la fonction interne
    
    def on_connect():
        """Valide la saisie et ferme la fenetre"""
        ip_value = entry_ip.get().strip()
        if not ip_value:
            messagebox.showerror("Erreur", "Veuillez entrer une adresse IP")
            return
        robot_ip[0] = ip_value
        root.quit()
    
    def on_cancel():
        """Annule et ferme la fenetre"""
        root.quit()
    
    # Creer la fenetre principale
    root = tk.Tk()
    root.title("Configuration Robot - Vision System")
    root.geometry("400x200")
    root.resizable(False, False)
    
    # Couleurs theme sombre
    dark_bg = "#1e1e1e"
    dark_fg = "#ffffff"
    dark_secondary = "#2d2d2d"
    dark_accent = "#0d7377"
    
    root.configure(bg=dark_bg)
    
    # Frame principal
    main_frame = tk.Frame(root, bg=dark_bg)
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Titre
    title_label = tk.Label(
        main_frame,
        text="Configuration du Robot",
        font=("Arial", 14, "bold"),
        bg=dark_bg,
        fg=dark_fg
    )
    title_label.pack(pady=(0, 20))
    
    # Frame pour l'adresse IP
    ip_frame = tk.Frame(main_frame, bg=dark_bg)
    ip_frame.pack(fill="x", pady=10)
    
    ip_label = tk.Label(
        ip_frame,
        text="Adresse IP du serveur :",
        font=("Arial", 11),
        bg=dark_bg,
        fg=dark_fg
    )
    ip_label.pack(anchor="w")
    
    entry_ip = tk.Entry(
        ip_frame,
        font=("Arial", 12),
        bg=dark_secondary,
        fg=dark_fg,
        insertbackground=dark_fg,
        relief=tk.FLAT,
        width=30
    )
    entry_ip.pack(fill="x", pady=(5, 0))
    entry_ip.insert(0, default_ip)  # Valeur par defaut
    entry_ip.select_range(0, tk.END)  # Selectionner le texte
    entry_ip.focus()
    
    # Frame pour les boutons
    button_frame = tk.Frame(main_frame, bg=dark_bg)
    button_frame.pack(fill="x", pady=(20, 0))
    
    # Bouton Connexion
    btn_connect = tk.Button(
        button_frame,
        text="Connexion",
        command=on_connect,
        bg=dark_accent,
        fg=dark_fg,
        font=("Arial", 11, "bold"),
        padx=20,
        pady=10,
        relief=tk.FLAT,
        cursor="hand2"
    )
    btn_connect.pack(side="left", padx=(0, 10))
    
    # Bouton Annuler
    btn_cancel = tk.Button(
        button_frame,
        text="Annuler",
        command=on_cancel,
        bg="#444444",
        fg=dark_fg,
        font=("Arial", 11, "bold"),
        padx=20,
        pady=10,
        relief=tk.FLAT,
        cursor="hand2"
    )
    btn_cancel.pack(side="left")
    
    # Bind Enter pour connexion rapide
    entry_ip.bind("<Return>", lambda e: on_connect())
    
    # Centrer la fenetre sur l'ecran
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"+{x}+{y}")
    
    # Afficher la fenetre et attendre la reponse
    root.mainloop()
    root.destroy()
    
    return robot_ip[0]


# =========================
# FONCTIONS UTILES
# =========================
def split_pieces_by_status(detections):
    """
    Sépare les pièces GOOD et BAD à partir des résultats YOLO.

    Args:
        detections (list): résultats YOLO (liste de dict avec 'piece_id' et 'status')

    Returns:
        tuple: (good_pieces, bad_pieces) - listes des IDs de pièces
    """
    good_pieces = []
    bad_pieces = []

    for det in detections:
        piece_id = det.get("piece_id")
        status = det.get("status")

        if piece_id is None or status is None:
            continue

        if status.upper() == "GOOD":
            good_pieces.append(piece_id)
        elif status.upper() == "BAD":
            bad_pieces.append(piece_id)

    return good_pieces, bad_pieces


def process_piece(client, piece_id, bin_name):
    """
    Effectue le pick & place d’une pièce vers un bin donné.

    Args:
        client (RobotClient)
        piece_id (str): ex 'piece 1'
        bin_name (str): 'good bin' ou 'bad bin'
    """
    print(f"➡️ Pick piece {piece_id}")
    response = client.pick_piece(f"piece {piece_id}")

    if response is None or response.get("status") != "success":
        print(f"❌ Échec PICK pour piece {piece_id}")
        return

    time.sleep(0.5)

    print(f"📦 Place piece {piece_id} dans {bin_name}")
    response = client.place_piece(bin_name)

    if response is None or response.get("status") != "success":
        print(f"❌ Échec PLACE pour piece {piece_id} vers {bin_name}")
        return

    time.sleep(0.5)

    print(f"✅ Piece {piece_id} placée avec succès")


# =========================
# MAIN
# =========================
def main():
    print("\n🚀 DÉMARRAGE DU SYSTÈME VISION + ROBOT\n")

    # =========================
    # 0️⃣ AFFICHER L'INTERFACE DE CONFIGURATION
    # =========================
    print("Affichage de l'interface de configuration du robot...")
    robot_ip = show_robot_connection_dialog(ROBOT_IP)
    
    if robot_ip is None:
        print("Annulation par l'utilisateur")
        return
    
    print(f"Adresse IP saisie : {robot_ip}")

    # =========================
    # 1️⃣ CONNEXION ROBOT
    # =========================
    print("\n🌐 Connexion au robot...")
    client = RobotClient(robot_ip)

    if not client.connect():
        print("❌ Impossible de se connecter au robot")
        return

    try:
        # =========================
        # 2️⃣ RETOUR HOME IMMÉDIAT
        # =========================
        print("🏠 Déplacement initial vers HOME")
        response = client.move_home()
        if response is None or response.get("status") != "success":
            print("❌ Échec move_home initial")
            return

        time.sleep(1)

        # =========================
        # 3️⃣ INTERFACE YOLO AVEC TKINTER
        # =========================
        print("\n🎥 Ouverture de l'interface de détection YOLO...")
        good_pieces_list, bad_pieces_list = capture_with_yolo_ui()

        if not good_pieces_list and not bad_pieces_list:
            print("⚠️ Aucune pièce détectée. Fin du cycle.")
            return

        # Extraire les IDs de pièces
        good_pieces = [p["piece_id"] for p in good_pieces_list]
        bad_pieces = [p["piece_id"] for p in bad_pieces_list]

        print(f"\n🟢 Pièces GOOD sélectionnées : {good_pieces}")
        print(f"🔴 Pièces BAD sélectionnées : {bad_pieces}")
        
        # =========================
        # 4️⃣ TRAITEMENT BAD
        # =========================
        print("\n===== 🔴 TRAITEMENT DES PIÈCES BAD =====")
        for piece_id in bad_pieces:
            process_piece(client, piece_id, BAD_BIN_NAME)

        # =========================
        # 5️⃣ TRAITEMENT GOOD
        # =========================
        print("\n===== 🟢 TRAITEMENT DES PIÈCES GOOD =====")
        for piece_id in good_pieces:
            process_piece(client, piece_id, GOOD_BIN_NAME)

        # =========================
        # 6️⃣ FIN DE CYCLE
        # =========================
        print("\n🏠 Retour HOME final")
        client.move_home()

        print("\n✅ CYCLE TERMINÉ AVEC SUCCÈS")

    finally:
        client.disconnect()
        print("🔌 Déconnexion du robot")


# =========================
# ENTRY POINT
# =========================
if __name__ == "__main__":
    main()
