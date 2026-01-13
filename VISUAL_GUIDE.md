# 🎯 QUICK START - Sorting Dashboard

## ONE COMMAND TO RUN:

```bash
python run_sorting_system.py
```

---

## DASHBOARD OVERVIEW

```
╔═══════════════════════════════════════════════════════════════════════╗
║  🤖 Robot Sorting Dashboard - Live Vision System                     ║
╠═══════════════════════════════════╦═══════════════════════════════════╣
║  📹 LIVE CAMERA                   ║  ROBOT CONNECTION                 ║
║  ┌─────────────────────────────┐  ║  ┌─────────────────────────────┐ ║
║  │                             │  ║  │ IP: [192.168.137.1]         │ ║
║  │                             │  ║  │ [🔗 Connect Robot]          │ ║
║  │     LIVE VIDEO FEED         │  ║  │ Status: ● Connected         │ ║
║  │     WITH YOLO BOXES         │  ║  └─────────────────────────────┘ ║
║  │                             │  ║                                   ║
║  │  ┌──────────────┐           │  ║  DETECTION RESULTS                ║
║  │  │ Piece 1:GOOD │           │  ║  ┌─────────────────────────────┐ ║
║  │  └──────────────┘           │  ║  │  🟢 GOOD PIECES             │ ║
║  │        ┌──────────────┐     │  ║  │     Count: 3                │ ║
║  │        │ Piece 2:BAD  │     │  ║  │     Pieces: 1, 3, 5         │ ║
║  │        └──────────────┘     │  ║  └─────────────────────────────┘ ║
║  │                             │  ║  ┌─────────────────────────────┐ ║
║  │      900 x 650 pixels       │  ║  │  🔴 BAD PIECES              │ ║
║  │                             │  ║  │     Count: 2                │ ║
║  └─────────────────────────────┘  ║  │     Pieces: 2, 4            │ ║
║  [📹 Start] [⏸ Stop] [🎯 Detect] ║  └─────────────────────────────┘ ║
║                                   ║                                   ║
║                                   ║  SORTING CONTROL                  ║
║                                   ║  ┌─────────────────────────────┐ ║
║                                   ║  │  ▶️ START SORTING           │ ║
║                                   ║  └─────────────────────────────┘ ║
║                                   ║  Progress: [████████░░] 4/5      ║
║                                   ║                                   ║
║                                   ║  ACTIVITY LOG                     ║
║                                   ║  ┌─────────────────────────────┐ ║
║                                   ║  │ [14:23] ✅ Picked piece 1  │ ║
║                                   ║  │ [14:24] ✅ Placed in bin   │ ║
║                                   ║  │ [14:25] ℹ️ Sorting...      │ ║
║                                   ║  └─────────────────────────────┘ ║
╚═══════════════════════════════════╩═══════════════════════════════════╝
```

---

## 4 SIMPLE STEPS

### STEP 1: START CAMERA 📹
```
Click: [📹 Start Camera]
```
- Camera feed appears
- YOLO detects pieces automatically
- Pieces get labeled with IDs

### STEP 2: CONNECT ROBOT 🔗
```
1. Enter IP: 192.168.137.1
2. Click: [🔗 Connect Robot]
```
- Status turns green: ● Connected
- Robot moves to home position

### STEP 3: CAPTURE & DETECT 🎯
```
Click: [🎯 Capture & Detect]
```
- Results appear in right panel:
  - 🟢 GOOD: 3 (Pieces: 1, 3, 5)
  - 🔴 BAD: 2 (Pieces: 2, 4)

### STEP 4: START SORTING ▶️
```
Click: [▶️ START SORTING]
```
- Automated process begins:
  - Picks all BAD pieces → bad bin
  - Picks all GOOD pieces → good bin
  - Returns to home
  - Shows success message

---

## WHAT YOU SEE

### Camera Feed Shows:
- ✅ Live video from camera
- ✅ Green boxes around GOOD pieces
- ✅ Red boxes around BAD pieces
- ✅ Labels: "Piece 1: GOOD"
- ✅ Real-time updates

### Right Panel Shows:
- ✅ Connection status
- ✅ Count of GOOD pieces
- ✅ Count of BAD pieces
- ✅ List of piece IDs
- ✅ Progress bar
- ✅ Activity log with timestamps

---

## FUNCTIONS USED

### Exactly from client_example.py:

```python
# PICK A PIECE
pick_piece("piece 1")
pick_piece("piece 2")

# PLACE IN BIN
place_piece("good bin")
place_piece("bad bin")

# RETURN HOME
move_home()
```

**No positions needed!** Server handles everything.

---

## EXAMPLE SESSION

```
[14:20:00] ℹ️ Dashboard initialized
[14:20:05] ℹ️ Starting camera...
[14:20:06] ✅ YOLO model loaded
[14:20:06] ✅ Camera found at index 0
           
[Camera shows live feed with boxes]

[14:20:15] ℹ️ Connecting to robot...
[14:20:16] ✅ Connected to robot!
[14:20:17] ✅ Robot at home position

[Click Capture & Detect]
[14:20:25] ✅ Detected: 3 good, 2 bad

[Click START SORTING]
[14:20:30] ℹ️ Starting sorting of 5 pieces...
[14:20:31] ℹ️ Picking BAD piece 2...
[14:20:33] ℹ️ Placing piece 2 in bad bin...
[14:20:34] ✅ Piece 2 sorted successfully!
[14:20:35] ℹ️ Picking BAD piece 4...
[14:20:37] ℹ️ Placing piece 4 in bad bin...
[14:20:38] ✅ Piece 4 sorted successfully!
[14:20:39] ℹ️ Picking GOOD piece 1...
[14:20:41] ℹ️ Placing piece 1 in good bin...
[14:20:42] ✅ Piece 1 sorted successfully!
[14:20:43] ℹ️ Picking GOOD piece 3...
[14:20:45] ℹ️ Placing piece 3 in good bin...
[14:20:46] ✅ Piece 3 sorted successfully!
[14:20:47] ℹ️ Picking GOOD piece 5...
[14:20:49] ℹ️ Placing piece 5 in good bin...
[14:20:50] ✅ Piece 5 sorted successfully!
[14:20:51] ℹ️ Sorting complete! Returning to home...
[14:20:53] ✅ Robot returned to home

[Success Message]
Successfully sorted 5 of 5 pieces!
```

---

## CONTROLS

### Camera Controls:
- **📹 Start Camera**: Begin video feed
- **⏸ Stop Camera**: Stop video feed
- **🎯 Capture & Detect**: Finalize detections

### Robot Controls:
- **🔗 Connect Robot**: Establish connection
- **▶️ START SORTING**: Begin automated sorting

---

## DETECTION VISUALIZATION

### On Camera Feed:

```
┌─────────────────┐
│ Piece 1: GOOD   │  ← Green box with white label
└─────────────────┘

┌─────────────────┐
│ Piece 2: BAD    │  ← Red box with white label
└─────────────────┘
```

### In Results Panel:

```
🟢 GOOD PIECES
   Count: 3
   Pieces: 1, 3, 5

🔴 BAD PIECES
   Count: 2
   Pieces: 2, 4
```

---

## TROUBLESHOOTING

### Camera not working?
- Check camera is plugged in
- Try different USB port
- Close other apps using camera

### No detections?
- Improve lighting
- Move pieces into frame
- Check yolo.pt file exists

### Robot not connecting?
- Verify IP address
- Check robot server is running
- Test with ping command

---

## TEST BEFORE RUNNING

```bash
python test_dashboard.py
```

This checks:
- ✅ All packages installed
- ✅ Camera accessible
- ✅ YOLO model found
- ✅ Robot client working

---

## SUMMARY

**What It Does:**
1. Shows live camera with YOLO detection
2. Connects to robot
3. Detects and classifies pieces
4. Automatically sorts all pieces
5. Returns robot to home

**How It Works:**
- Uses exact `pick_piece()` and `place_piece()` functions
- No position calculations needed
- Server handles all robot movements
- Visual confirmation before sorting

**Why It's Great:**
- See exactly what robot will pick
- Real-time visual feedback
- Simple and intuitive
- Professional dashboard
- Complete automation

---

## READY TO GO!

```bash
python run_sorting_system.py
```

**That's it!** 🎉

---

For detailed docs: `README_DASHBOARD.md`
