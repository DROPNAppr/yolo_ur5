# 🤖 Robot Sorting Dashboard - Live Vision System

## Overview
Complete sorting dashboard with **embedded live camera feed** showing real-time YOLO detection. Uses the exact `pick_piece()` and `place_piece()` functions from client_example.

## Key Features

### 📹 Live Camera Feed
- **Real-time video stream** embedded in the dashboard
- **YOLO detection overlay** showing piece IDs and status
- **Color-coded boxes**: Green for GOOD pieces, Red for BAD pieces
- **Stable piece tracking** - pieces keep same ID during detection

### 🎯 Smart Detection
- Continuous YOLO inference on live feed
- Automatic piece numbering and tracking
- Visual feedback with bounding boxes and labels
- Capture & Detect to finalize piece selection

### 🤖 Robot Control
- Uses **exact functions from client_example.py**:
  - `pick_piece(piece_name)` - Pick using piece name
  - `place_piece(bin_name)` - Place in bin
- **No position calculations** - all handled server-side
- Automatic return to home position

### 📊 Real-time Dashboard
- Live camera view (900x650)
- Detection results panel
- Progress tracking
- Activity log with timestamps

## Quick Start

```bash
python run_sorting_system.py
```

## Step-by-Step Usage

### 1. Launch Dashboard
```bash
python run_sorting_system.py
```
The dashboard opens showing camera area and control panel.

### 2. Start Camera
- Click **"📹 Start Camera"** button
- Camera feed appears with live YOLO detection
- Pieces are automatically detected and labeled
- Each piece gets a unique ID (Piece 1, Piece 2, etc.)

### 3. Connect Robot
- Enter robot IP address (default: 192.168.137.1)
- Click **"🔗 Connect Robot"**
- Wait for green "● Connected" status
- Robot moves to home position automatically

### 4. Finalize Detection
- Position pieces in camera view
- Wait for detections to stabilize
- Click **"🎯 Capture & Detect"**
- Detection results appear in right panel:
  - 🟢 GOOD Pieces count and list
  - 🔴 BAD Pieces count and list

### 5. Start Sorting
- Click **"▶️ START SORTING"**
- Watch automated process:
  - Picks each BAD piece → places in "bad bin"
  - Picks each GOOD piece → places in "good bin"
  - Returns to home position
- Progress bar shows completion status
- Activity log shows detailed status

## Interface Layout

```
┌──────────────────────────────────────────────────────────────────┐
│  🤖 Robot Sorting Dashboard                                      │
│  Live Vision System & Automated Sorting                          │
├────────────────────────────────────┬─────────────────────────────┤
│  📹 LIVE CAMERA - YOLO DETECTION  │  Robot Connection           │
│  ┌──────────────────────────────┐ │  IP: [192.168.137.1]        │
│  │                              │ │  [🔗 Connect Robot]         │
│  │   [Live Camera Feed]         │ │  ● Connected                │
│  │   [YOLO Detection Boxes]     │ ├─────────────────────────────┤
│  │   [Piece IDs & Labels]       │ │  Detection Results          │
│  │                              │ │  🟢 GOOD: 3                 │
│  │        900 x 650             │ │  Pieces: 1, 3, 5            │
│  │                              │ │  🔴 BAD: 2                  │
│  │                              │ │  Pieces: 2, 4               │
│  └──────────────────────────────┘ ├─────────────────────────────┤
│  [📹 Start] [⏸ Stop] [🎯 Detect] │  Sorting Control            │
│                                    │  [▶️ START SORTING]         │
│                                    │  Progress: [████░] 4/5      │
│                                    ├─────────────────────────────┤
│                                    │  Activity Log               │
│                                    │  [14:23] ✅ Picked piece 1 │
│                                    │  [14:24] ✅ Placed in bin  │
└────────────────────────────────────┴─────────────────────────────┘
```

## Functions Used (Exact from client_example.py)

### pick_piece(piece_name)
```python
# Example usage in the dashboard
piece_name = f"piece {piece_id}"  # e.g., "piece 1", "piece 2"
response = self.robot_client.pick_piece(piece_name)
```

Sends command to robot server:
```json
{
    "command": "pick_piece",
    "piece": "piece 1"
}
```

### place_piece(location_name)
```python
# Example usage in the dashboard
bin_name = "good bin"  # or "bad bin"
response = self.robot_client.place_piece(bin_name)
```

Sends command to robot server:
```json
{
    "command": "place_piece",
    "location": "good bin"
}
```

## Workflow Diagram

```
[Launch Dashboard]
        ↓
[Start Camera] → Live feed with YOLO detection
        ↓
[Connect Robot] → Establishes connection, moves to HOME
        ↓
[Position Pieces] → Place pieces in camera view
        ↓
[Capture & Detect] → Finalizes detected pieces
        ↓              (Good: [1,3,5], Bad: [2,4])
        ↓
[START SORTING] → Automated process:
        ↓
    For each BAD piece:
        ├─ pick_piece("piece 2")
        ├─ place_piece("bad bin")
        ├─ pick_piece("piece 4")
        └─ place_piece("bad bin")
        ↓
    For each GOOD piece:
        ├─ pick_piece("piece 1")
        ├─ place_piece("good bin")
        ├─ pick_piece("piece 3")
        ├─ place_piece("good bin")
        ├─ pick_piece("piece 5")
        └─ place_piece("good bin")
        ↓
[Return HOME] → move_home()
        ↓
[Complete!] → Success message
```

## Camera Feed Features

### Visual Indicators
- **Bounding Boxes**: 
  - Green boxes = GOOD pieces
  - Red boxes = BAD pieces
  - 3-pixel thick lines

- **Labels**: 
  - Format: "Piece {ID}: {STATUS}"
  - Example: "Piece 1: GOOD"
  - White text on colored background

- **Stable Tracking**:
  - Pieces keep same ID throughout session
  - Uses centroid-based tracking
  - Threshold: 50 pixels for matching

### Image Adjustments
- **Contrast**: 1.5x (configurable)
- **Brightness**: -30 (configurable)
- **Resolution**: 900x650 display
- **FPS**: ~30 frames per second

## Configuration

### Camera Settings
Edit in `sorting_dashboard.py`:
```python
self.camera_id = 0          # Camera index (0=built-in, 1=USB)
self.conf_thresh = 0.6      # YOLO confidence threshold
self.contrast = 1.5         # Image contrast adjustment
self.brightness = -30       # Image brightness adjustment
```

### Robot IP
Default: `192.168.137.1`
Change in interface or edit:
```python
self.robot_ip = "192.168.137.1"
```

## Technical Details

### Technologies Used
- **Tkinter**: GUI framework
- **OpenCV**: Camera capture and image processing
- **Ultralytics YOLO**: Object detection
- **PIL/Pillow**: Image conversion for display
- **Threading**: Non-blocking operations
- **Socket**: Robot communication

### Performance
- **Camera FPS**: ~30 FPS
- **YOLO Inference**: Real-time on GPU/CPU
- **UI Updates**: 30ms delay between frames
- **Pick & Place**: 2-3 seconds per piece

### Memory Usage
- YOLO model: ~100-200 MB
- Camera buffer: ~10 MB
- GUI: ~50 MB
- Total: ~200-300 MB

## Troubleshooting

### Camera Issues

**Problem**: "No camera found"
- Check camera is connected
- Try different camera_id values (0, 1, 2)
- Verify camera works with other apps
- Check camera permissions

**Problem**: Black screen
- Adjust brightness/contrast settings
- Check lighting conditions
- Try different camera

### Detection Issues

**Problem**: No pieces detected
- Improve lighting
- Check YOLO model file (yolo.pt) exists
- Lower conf_thresh value
- Ensure pieces are in frame

**Problem**: Pieces jumping IDs
- Increase tracking threshold
- Reduce camera movement
- Improve lighting consistency

### Robot Issues

**Problem**: "Failed to pick piece"
- Verify piece positions in server
- Check robot calibration
- Ensure piece names match server definitions

**Problem**: "Failed to place piece"
- Verify bin positions in server
- Check gripper is functioning
- Ensure bin names are "good bin" and "bad bin"

## Files Structure

```
yolo_ur5/
├── sorting_dashboard.py          # Main dashboard (NEW - Use this!)
├── run_sorting_system.py         # Launcher
├── robot_client.py                # Robot communication
├── yolo.pt                        # YOLO model file
├── positions.py                   # Position definitions (server-side)
└── README_DASHBOARD.md            # This file
```

## Requirements

```bash
pip install ultralytics opencv-python pillow tk
```

Or use existing:
```bash
pip install -r requirement.txt
```

## Advantages of This Approach

✅ **Live Visual Feedback**: See exactly what robot will pick
✅ **No Position Calculations**: Server handles all positions
✅ **Simple Functions**: Just pick_piece() and place_piece()
✅ **Intuitive Interface**: Watch detection in real-time
✅ **Error Prevention**: Verify detections before sorting
✅ **Professional Look**: Complete dashboard view

## Example Session

```
Terminal Output:
======================================================================
  🤖 ROBOT SORTING DASHBOARD - LIVE VISION SYSTEM
======================================================================

Starting dashboard with embedded camera feed...

Features:
  📹 Live camera with YOLO detection
  🔗 Robot connection management
  🎯 Real-time piece detection
  ▶️  Automated sorting workflow
  📊 Progress tracking

Activity Log in Dashboard:
[14:20:15] ℹ️ Dashboard initialized
[14:20:16] ℹ️ Start camera to begin detection
[14:20:20] ✅ YOLO model loaded
[14:20:20] ✅ Camera found at index 0
[14:20:25] ℹ️ Connecting to robot at 192.168.137.1...
[14:20:26] ✅ Connected to robot!
[14:20:27] ✅ Robot at home position
[14:20:35] ✅ Detected: 3 good, 2 bad
[14:20:40] ℹ️ Starting sorting of 5 pieces...
[14:20:41] ℹ️ Picking BAD piece 2...
[14:20:43] ℹ️ Placing piece 2 in bad bin...
[14:20:44] ✅ Piece 2 sorted successfully!
[14:20:45] ℹ️ Picking BAD piece 4...
[14:20:47] ℹ️ Placing piece 4 in bad bin...
[14:20:48] ✅ Piece 4 sorted successfully!
[14:20:49] ℹ️ Picking GOOD piece 1...
[14:20:51] ℹ️ Placing piece 1 in good bin...
[14:20:52] ✅ Piece 1 sorted successfully!
[14:20:53] ℹ️ Picking GOOD piece 3...
[14:20:55] ℹ️ Placing piece 3 in good bin...
[14:20:56] ✅ Piece 3 sorted successfully!
[14:20:57] ℹ️ Picking GOOD piece 5...
[14:20:59] ℹ️ Placing piece 5 in good bin...
[14:21:00] ✅ Piece 5 sorted successfully!
[14:21:01] ℹ️ Sorting complete! Returning to home...
[14:21:03] ✅ Robot returned to home

[Success Message Box]
Successfully sorted 5 of 5 pieces!
```

## Safety Notes

⚠️ **Important**:
1. Keep workspace clear during operation
2. Verify detections before sorting
3. Emergency stop must be accessible
4. Test with slow speeds first
5. Monitor camera feed during sorting

## Support

For issues:
1. Check activity log in dashboard
2. Verify camera feed is working
3. Test robot connection separately
4. Review this documentation

---

**Ready to Use**: Just run `python run_sorting_system.py`

**Date**: January 2026
