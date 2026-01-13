"""
Sorting Interface - Complete GUI for Robot Sorting System

This application provides a complete interface for:
1. Connecting to the robot
2. Detecting and classifying pieces using YOLO
3. Automatically sorting all pieces into good/bad bins
4. Returning to home position
"""

import tkinter as tk
from tkinter import messagebox, ttk
import threading
import time
from robot_client import RobotClient
from cam import capture_with_yolo_ui


class SortingInterface:
    """
    Main GUI interface for the sorting system.
    """
    
    def __init__(self):
        """Initialize the sorting interface."""
        self.root = tk.Tk()
        self.root.title("Robot Sorting System - Vision & Automation")
        self.root.geometry("800x700")
        self.root.resizable(False, False)
        
        # Theme colors
        self.dark_bg = "#1e1e1e"
        self.dark_fg = "#ffffff"
        self.dark_secondary = "#2d2d2d"
        self.dark_accent = "#0d7377"
        self.success_color = "#4caf50"
        self.error_color = "#f44336"
        self.warning_color = "#ff9800"
        
        self.root.configure(bg=self.dark_bg)
        
        # Robot client
        self.robot_client = None
        self.robot_ip = "192.168.137.1"
        self.is_connected = False
        
        # Detection results
        self.good_pieces = []
        self.bad_pieces = []
        
        # Sorting state
        self.is_sorting = False
        self.current_piece = None
        self.total_pieces = 0
        self.processed_pieces = 0
        
        # Build UI
        self.create_widgets()
        
    def create_widgets(self):
        """Create all UI widgets."""
        # Main container
        main_container = tk.Frame(self.root, bg=self.dark_bg)
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # ===== HEADER =====
        header_frame = tk.Frame(main_container, bg=self.dark_bg)
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="🤖 Robot Sorting System",
            font=("Arial", 20, "bold"),
            bg=self.dark_bg,
            fg=self.dark_fg
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Automated Piece Detection & Sorting",
            font=("Arial", 11),
            bg=self.dark_bg,
            fg="#888888"
        )
        subtitle_label.pack()
        
        # ===== CONNECTION SECTION =====
        connection_frame = tk.LabelFrame(
            main_container,
            text=" Connection Settings ",
            font=("Arial", 12, "bold"),
            bg=self.dark_bg,
            fg=self.dark_fg,
            relief=tk.GROOVE,
            borderwidth=2
        )
        connection_frame.pack(fill="x", pady=(0, 15))
        
        # IP Address input
        ip_frame = tk.Frame(connection_frame, bg=self.dark_bg)
        ip_frame.pack(fill="x", padx=15, pady=10)
        
        tk.Label(
            ip_frame,
            text="Robot IP Address:",
            font=("Arial", 10),
            bg=self.dark_bg,
            fg=self.dark_fg
        ).pack(side="left", padx=(0, 10))
        
        self.ip_entry = tk.Entry(
            ip_frame,
            font=("Arial", 10),
            bg=self.dark_secondary,
            fg=self.dark_fg,
            insertbackground=self.dark_fg,
            relief=tk.FLAT,
            width=20
        )
        self.ip_entry.pack(side="left", padx=(0, 10))
        self.ip_entry.insert(0, self.robot_ip)
        
        # Connection button
        self.connect_btn = tk.Button(
            ip_frame,
            text="Connect",
            command=self.connect_robot,
            bg=self.dark_accent,
            fg=self.dark_fg,
            font=("Arial", 10, "bold"),
            padx=20,
            pady=5,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.connect_btn.pack(side="left", padx=(0, 10))
        
        # Connection status
        self.connection_status = tk.Label(
            ip_frame,
            text="● Not Connected",
            font=("Arial", 10, "bold"),
            bg=self.dark_bg,
            fg=self.error_color
        )
        self.connection_status.pack(side="left")
        
        # ===== DETECTION SECTION =====
        detection_frame = tk.LabelFrame(
            main_container,
            text=" Piece Detection ",
            font=("Arial", 12, "bold"),
            bg=self.dark_bg,
            fg=self.dark_fg,
            relief=tk.GROOVE,
            borderwidth=2
        )
        detection_frame.pack(fill="x", pady=(0, 15))
        
        self.detect_btn = tk.Button(
            detection_frame,
            text="🎥 Start Detection",
            command=self.start_detection,
            bg=self.dark_accent,
            fg=self.dark_fg,
            font=("Arial", 11, "bold"),
            padx=30,
            pady=10,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.detect_btn.pack(pady=15)
        
        # Detection results
        results_frame = tk.Frame(detection_frame, bg=self.dark_bg)
        results_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        # Good pieces
        good_frame = tk.Frame(results_frame, bg=self.dark_secondary, relief=tk.RAISED, borderwidth=1)
        good_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        tk.Label(
            good_frame,
            text="🟢 Good Pieces",
            font=("Arial", 11, "bold"),
            bg=self.dark_secondary,
            fg=self.success_color
        ).pack(pady=5)
        
        self.good_pieces_label = tk.Label(
            good_frame,
            text="0",
            font=("Arial", 24, "bold"),
            bg=self.dark_secondary,
            fg=self.dark_fg
        )
        self.good_pieces_label.pack(pady=10)
        
        self.good_list_label = tk.Label(
            good_frame,
            text="None",
            font=("Arial", 9),
            bg=self.dark_secondary,
            fg="#888888",
            wraplength=250
        )
        self.good_list_label.pack(pady=(0, 10))
        
        # Bad pieces
        bad_frame = tk.Frame(results_frame, bg=self.dark_secondary, relief=tk.RAISED, borderwidth=1)
        bad_frame.pack(side="left", fill="both", expand=True, padx=(5, 0))
        
        tk.Label(
            bad_frame,
            text="🔴 Bad Pieces",
            font=("Arial", 11, "bold"),
            bg=self.dark_secondary,
            fg=self.error_color
        ).pack(pady=5)
        
        self.bad_pieces_label = tk.Label(
            bad_frame,
            text="0",
            font=("Arial", 24, "bold"),
            bg=self.dark_secondary,
            fg=self.dark_fg
        )
        self.bad_pieces_label.pack(pady=10)
        
        self.bad_list_label = tk.Label(
            bad_frame,
            text="None",
            font=("Arial", 9),
            bg=self.dark_secondary,
            fg="#888888",
            wraplength=250
        )
        self.bad_list_label.pack(pady=(0, 10))
        
        # ===== SORTING SECTION =====
        sorting_frame = tk.LabelFrame(
            main_container,
            text=" Automated Sorting ",
            font=("Arial", 12, "bold"),
            bg=self.dark_bg,
            fg=self.dark_fg,
            relief=tk.GROOVE,
            borderwidth=2
        )
        sorting_frame.pack(fill="both", expand=True, pady=(0, 15))
        
        self.sort_btn = tk.Button(
            sorting_frame,
            text="▶️ Start Sorting",
            command=self.start_sorting,
            bg=self.success_color,
            fg=self.dark_fg,
            font=("Arial", 12, "bold"),
            padx=40,
            pady=12,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.sort_btn.pack(pady=15)
        
        # Progress bar
        progress_container = tk.Frame(sorting_frame, bg=self.dark_bg)
        progress_container.pack(fill="x", padx=15, pady=(0, 10))
        
        tk.Label(
            progress_container,
            text="Progress:",
            font=("Arial", 10, "bold"),
            bg=self.dark_bg,
            fg=self.dark_fg
        ).pack(anchor="w")
        
        self.progress_bar = ttk.Progressbar(
            progress_container,
            mode='determinate',
            length=400,
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill="x", pady=5)
        
        self.progress_label = tk.Label(
            progress_container,
            text="0/0 pieces processed",
            font=("Arial", 9),
            bg=self.dark_bg,
            fg="#888888"
        )
        self.progress_label.pack(anchor="w")
        
        # Status log
        log_container = tk.Frame(sorting_frame, bg=self.dark_bg)
        log_container.pack(fill="both", expand=True, padx=15, pady=(10, 15))
        
        tk.Label(
            log_container,
            text="Activity Log:",
            font=("Arial", 10, "bold"),
            bg=self.dark_bg,
            fg=self.dark_fg
        ).pack(anchor="w")
        
        # Create scrollbar and text widget for log
        log_scroll_frame = tk.Frame(log_container, bg=self.dark_bg)
        log_scroll_frame.pack(fill="both", expand=True, pady=(5, 0))
        
        scrollbar = tk.Scrollbar(log_scroll_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.log_text = tk.Text(
            log_scroll_frame,
            height=6,
            bg=self.dark_secondary,
            fg=self.dark_fg,
            font=("Courier New", 9),
            relief=tk.FLAT,
            yscrollcommand=scrollbar.set,
            state=tk.DISABLED
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.log_text.yview)
        
        # ===== FOOTER =====
        footer_frame = tk.Frame(main_container, bg=self.dark_bg)
        footer_frame.pack(fill="x")
        
        self.home_btn = tk.Button(
            footer_frame,
            text="🏠 Return to Home",
            command=self.return_home,
            bg="#444444",
            fg=self.dark_fg,
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.home_btn.pack(side="left", padx=(0, 10))
        
        self.exit_btn = tk.Button(
            footer_frame,
            text="❌ Exit",
            command=self.exit_application,
            bg=self.error_color,
            fg=self.dark_fg,
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        )
        self.exit_btn.pack(side="right")
        
        # Configure progress bar style
        style = ttk.Style()
        style.theme_use('default')
        style.configure(
            "Custom.Horizontal.TProgressbar",
            troughcolor=self.dark_secondary,
            background=self.dark_accent,
            thickness=20
        )
        
    def log_message(self, message, level="INFO"):
        """
        Add message to the activity log.
        
        Args:
            message (str): Message to log
            level (str): Log level (INFO, SUCCESS, ERROR, WARNING)
        """
        self.log_text.config(state=tk.NORMAL)
        timestamp = time.strftime("%H:%M:%S")
        
        # Color coding
        if level == "SUCCESS":
            prefix = "✅"
        elif level == "ERROR":
            prefix = "❌"
        elif level == "WARNING":
            prefix = "⚠️"
        else:
            prefix = "ℹ️"
        
        log_entry = f"[{timestamp}] {prefix} {message}\n"
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
        
    def connect_robot(self):
        """Connect to the robot server."""
        self.robot_ip = self.ip_entry.get().strip()
        
        if not self.robot_ip:
            messagebox.showerror("Error", "Please enter a valid IP address")
            return
        
        self.log_message(f"Connecting to robot at {self.robot_ip}...")
        self.connect_btn.config(state=tk.DISABLED, text="Connecting...")
        
        def connect_thread():
            try:
                self.robot_client = RobotClient(self.robot_ip)
                
                if self.robot_client.connect():
                    self.is_connected = True
                    self.root.after(0, self.on_connection_success)
                else:
                    self.root.after(0, self.on_connection_failed)
            except Exception as e:
                self.root.after(0, lambda: self.on_connection_error(str(e)))
        
        threading.Thread(target=connect_thread, daemon=True).start()
    
    def on_connection_success(self):
        """Handle successful connection."""
        self.log_message("Successfully connected to robot!", "SUCCESS")
        self.connection_status.config(text="● Connected", fg=self.success_color)
        self.connect_btn.config(text="Disconnect", state=tk.NORMAL, command=self.disconnect_robot)
        self.detect_btn.config(state=tk.NORMAL)
        self.home_btn.config(state=tk.NORMAL)
        
        # Move to home position
        self.log_message("Moving robot to home position...")
        try:
            response = self.robot_client.move_home()
            if response and response.get("status") == "success":
                self.log_message("Robot at home position", "SUCCESS")
            else:
                self.log_message("Failed to move to home position", "WARNING")
        except Exception as e:
            self.log_message(f"Error moving to home: {str(e)}", "ERROR")
    
    def on_connection_failed(self):
        """Handle connection failure."""
        self.log_message("Failed to connect to robot", "ERROR")
        self.connection_status.config(text="● Connection Failed", fg=self.error_color)
        self.connect_btn.config(state=tk.NORMAL, text="Connect")
        messagebox.showerror("Connection Error", 
                           f"Could not connect to robot at {self.robot_ip}\n\n"
                           "Please check:\n"
                           "1. Robot server is running\n"
                           "2. IP address is correct\n"
                           "3. Network connection is active")
    
    def on_connection_error(self, error_msg):
        """Handle connection error."""
        self.log_message(f"Connection error: {error_msg}", "ERROR")
        self.connection_status.config(text="● Error", fg=self.error_color)
        self.connect_btn.config(state=tk.NORMAL, text="Connect")
        messagebox.showerror("Connection Error", f"Error: {error_msg}")
    
    def disconnect_robot(self):
        """Disconnect from robot."""
        if self.robot_client:
            self.robot_client.disconnect()
            self.is_connected = False
            self.log_message("Disconnected from robot", "INFO")
            self.connection_status.config(text="● Not Connected", fg=self.error_color)
            self.connect_btn.config(text="Connect", command=self.connect_robot)
            self.detect_btn.config(state=tk.DISABLED)
            self.sort_btn.config(state=tk.DISABLED)
            self.home_btn.config(state=tk.DISABLED)
    
    def start_detection(self):
        """Start piece detection using YOLO."""
        self.log_message("Starting piece detection...")
        self.detect_btn.config(state=tk.DISABLED, text="Detecting...")
        
        def detection_thread():
            try:
                # Call the YOLO UI
                good_pieces_list, bad_pieces_list = capture_with_yolo_ui()
                
                # Extract piece IDs
                self.good_pieces = [p["piece_id"] for p in good_pieces_list]
                self.bad_pieces = [p["piece_id"] for p in bad_pieces_list]
                
                self.root.after(0, self.on_detection_complete)
            except Exception as e:
                self.root.after(0, lambda: self.on_detection_error(str(e)))
        
        threading.Thread(target=detection_thread, daemon=True).start()
    
    def on_detection_complete(self):
        """Handle detection completion."""
        self.detect_btn.config(state=tk.NORMAL, text="🎥 Start Detection")
        
        if not self.good_pieces and not self.bad_pieces:
            self.log_message("No pieces detected", "WARNING")
            messagebox.showwarning("No Pieces", "No pieces were detected. Please try again.")
            return
        
        # Update UI with results
        self.good_pieces_label.config(text=str(len(self.good_pieces)))
        self.bad_pieces_label.config(text=str(len(self.bad_pieces)))
        
        if self.good_pieces:
            good_list = ", ".join([str(p) for p in self.good_pieces])
            self.good_list_label.config(text=f"Pieces: {good_list}")
        else:
            self.good_list_label.config(text="None")
        
        if self.bad_pieces:
            bad_list = ", ".join([str(p) for p in self.bad_pieces])
            self.bad_list_label.config(text=f"Pieces: {bad_list}")
        else:
            self.bad_list_label.config(text="None")
        
        self.log_message(f"Detection complete: {len(self.good_pieces)} good, {len(self.bad_pieces)} bad", "SUCCESS")
        
        # Enable sorting
        self.sort_btn.config(state=tk.NORMAL)
    
    def on_detection_error(self, error_msg):
        """Handle detection error."""
        self.detect_btn.config(state=tk.NORMAL, text="🎥 Start Detection")
        self.log_message(f"Detection error: {error_msg}", "ERROR")
        messagebox.showerror("Detection Error", f"Error during detection:\n{error_msg}")
    
    def start_sorting(self):
        """Start the automated sorting process."""
        if not self.is_connected:
            messagebox.showerror("Error", "Robot not connected")
            return
        
        if not self.good_pieces and not self.bad_pieces:
            messagebox.showwarning("No Pieces", "No pieces to sort")
            return
        
        self.is_sorting = True
        self.sort_btn.config(state=tk.DISABLED, text="⏸️ Sorting...")
        self.detect_btn.config(state=tk.DISABLED)
        
        self.total_pieces = len(self.good_pieces) + len(self.bad_pieces)
        self.processed_pieces = 0
        self.progress_bar['maximum'] = self.total_pieces
        self.progress_bar['value'] = 0
        
        self.log_message(f"Starting sorting of {self.total_pieces} pieces...")
        
        def sorting_thread():
            try:
                # Sort bad pieces first
                for piece_id in self.bad_pieces:
                    if not self.is_sorting:
                        break
                    self.root.after(0, lambda p=piece_id: self.process_piece(p, "bad bin", "BAD"))
                    time.sleep(0.5)  # Small delay for UI update
                
                # Sort good pieces
                for piece_id in self.good_pieces:
                    if not self.is_sorting:
                        break
                    self.root.after(0, lambda p=piece_id: self.process_piece(p, "good bin", "GOOD"))
                    time.sleep(0.5)  # Small delay for UI update
                
                # Return to home
                self.root.after(0, self.on_sorting_complete)
            except Exception as e:
                self.root.after(0, lambda: self.on_sorting_error(str(e)))
        
        threading.Thread(target=sorting_thread, daemon=True).start()
    
    def process_piece(self, piece_id, bin_name, status_type):
        """
        Process a single piece (pick and place).
        
        Args:
            piece_id: ID of the piece
            bin_name: Name of the bin ('good bin' or 'bad bin')
            status_type: Type of piece ('GOOD' or 'BAD')
        """
        self.current_piece = piece_id
        piece_name = f"piece {piece_id}"
        
        # Pick the piece
        self.log_message(f"Picking {status_type} piece {piece_id}...")
        try:
            response = self.robot_client.pick_piece(piece_name)
            
            if response is None or response.get("status") != "success":
                self.log_message(f"Failed to pick piece {piece_id}", "ERROR")
                self.processed_pieces += 1
                self.update_progress()
                return
            
            time.sleep(0.5)
            
            # Place the piece
            self.log_message(f"Placing piece {piece_id} in {bin_name}...")
            response = self.robot_client.place_piece(bin_name)
            
            if response is None or response.get("status") != "success":
                self.log_message(f"Failed to place piece {piece_id}", "ERROR")
            else:
                self.log_message(f"Piece {piece_id} sorted successfully", "SUCCESS")
            
            self.processed_pieces += 1
            self.update_progress()
            
        except Exception as e:
            self.log_message(f"Error processing piece {piece_id}: {str(e)}", "ERROR")
            self.processed_pieces += 1
            self.update_progress()
    
    def update_progress(self):
        """Update the progress bar and label."""
        self.progress_bar['value'] = self.processed_pieces
        self.progress_label.config(text=f"{self.processed_pieces}/{self.total_pieces} pieces processed")
        self.root.update()
    
    def on_sorting_complete(self):
        """Handle sorting completion."""
        self.is_sorting = False
        self.log_message("Sorting complete! Returning to home position...")
        
        try:
            response = self.robot_client.move_home()
            if response and response.get("status") == "success":
                self.log_message("Robot returned to home position", "SUCCESS")
            else:
                self.log_message("Failed to return to home", "WARNING")
        except Exception as e:
            self.log_message(f"Error returning to home: {str(e)}", "ERROR")
        
        self.sort_btn.config(state=tk.NORMAL, text="▶️ Start Sorting")
        self.detect_btn.config(state=tk.NORMAL)
        
        messagebox.showinfo("Sorting Complete", 
                          f"Successfully processed {self.processed_pieces} of {self.total_pieces} pieces!")
    
    def on_sorting_error(self, error_msg):
        """Handle sorting error."""
        self.is_sorting = False
        self.sort_btn.config(state=tk.NORMAL, text="▶️ Start Sorting")
        self.detect_btn.config(state=tk.NORMAL)
        self.log_message(f"Sorting error: {error_msg}", "ERROR")
        messagebox.showerror("Sorting Error", f"Error during sorting:\n{error_msg}")
    
    def return_home(self):
        """Return robot to home position."""
        if not self.is_connected:
            messagebox.showerror("Error", "Robot not connected")
            return
        
        self.log_message("Returning to home position...")
        self.home_btn.config(state=tk.DISABLED)
        
        def home_thread():
            try:
                response = self.robot_client.move_home()
                if response and response.get("status") == "success":
                    self.root.after(0, lambda: self.log_message("Robot at home position", "SUCCESS"))
                else:
                    self.root.after(0, lambda: self.log_message("Failed to move to home", "ERROR"))
            except Exception as e:
                self.root.after(0, lambda: self.log_message(f"Error: {str(e)}", "ERROR"))
            finally:
                self.root.after(0, lambda: self.home_btn.config(state=tk.NORMAL))
        
        threading.Thread(target=home_thread, daemon=True).start()
    
    def exit_application(self):
        """Exit the application."""
        if self.is_sorting:
            messagebox.showwarning("Sorting Active", "Please wait for sorting to complete")
            return
        
        if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            if self.robot_client and self.is_connected:
                self.robot_client.disconnect()
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """Start the GUI application."""
        # Center window on screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"+{x}+{y}")
        
        self.root.mainloop()


def main():
    """Main entry point."""
    app = SortingInterface()
    app.run()


if __name__ == "__main__":
    main()
