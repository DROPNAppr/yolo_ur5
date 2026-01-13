# 🤖 Robot Sorting System - Enhanced Interface

## Overview
This enhanced sorting system provides a complete graphical user interface (GUI) for automated piece detection and sorting using vision (YOLO) and robotic control.

## Features

### ✨ Main Features
- **Professional GUI Interface** - User-friendly interface with real-time feedback
- **Robot Connection Management** - Easy connection setup and status monitoring
- **Automated Detection** - Integration with YOLO-based piece classification
- **Complete Sorting Workflow** - Automatic pick and place for all detected pieces
- **Progress Tracking** - Real-time progress bar and activity log
- **Error Handling** - Robust error handling with clear user feedback
- **Home Position Management** - Automatic return to home after sorting

### 🎯 Workflow
1. **Connect** to the robot server
2. **Detect** pieces using YOLO vision system
3. **Review** classification results (good/bad pieces)
4. **Sort** all pieces automatically
5. **Return** to home position

## Installation

### Requirements
Install required packages:
```bash
pip install -r requirement.txt
```

### Additional Dependencies
The interface uses:
- `tkinter` (usually included with Python)
- `threading` (standard library)
- `socket` (standard library)
- `json` (standard library)

## Usage

### Quick Start
```bash
python run_sorting_system.py
```

Or directly:
```bash
python sorting_interface.py
```

### Step-by-Step Guide

#### 1. Launch the Application
```bash
python run_sorting_system.py
```

#### 2. Connect to Robot
- Enter the robot's IP address (default: 192.168.137.1)
- Click **"Connect"** button
- Wait for connection confirmation
- Robot will automatically move to home position

#### 3. Start Detection
- Click **"🎥 Start Detection"** button
- The YOLO detection window will open
- Review and confirm detected pieces
- Results will be displayed in the interface:
  - 🟢 Good Pieces count and list
  - 🔴 Bad Pieces count and list

#### 4. Start Sorting
- Click **"▶️ Start Sorting"** button
- The system will automatically:
  - Pick each bad piece and place in bad bin
  - Pick each good piece and place in good bin
  - Track progress with progress bar
  - Log all activities
  - Return to home position when complete

#### 5. Monitor Progress
- Watch the progress bar for completion status
- Read the activity log for detailed information
- Current piece being processed is shown in real-time

## File Structure

```
yolo_ur5/
├── sorting_interface.py      # Main GUI application (NEW)
├── run_sorting_system.py     # Simple launcher (NEW)
├── robot_client.py            # Robot communication client
├── cam.py                     # Camera capture with YOLO UI
├── positions.py               # Robot position definitions
├── yolo_inference.py          # YOLO detection logic
├── client_example.py          # Example client code
├── main.py                    # Original main script
└── README_SORTING_INTERFACE.md # This file
```

## Configuration

### Robot IP Address
Default IP: `192.168.137.1`

You can change this in the interface or modify the default in `sorting_interface.py`:
```python
self.robot_ip = "192.168.137.1"  # Change this line
```

### Bin Names
The system uses predefined bin names:
- Good pieces → `"good bin"`
- Bad pieces → `"bad bin"`

These should match the positions defined in `positions.py`.

### Piece Positions
Piece positions are defined in `positions.py`:
```python
PIECES = {
    1: {"position": [...], "orientation": [...]},
    2: {"position": [...], "orientation": [...]},
    # ... up to piece 6
}
```

## Interface Components

### Connection Section
- **IP Address Input**: Enter robot server IP
- **Connect Button**: Establish connection
- **Status Indicator**: Shows connection state (● Not Connected / ● Connected)

### Detection Section
- **Start Detection Button**: Launch YOLO detection
- **Results Display**: 
  - Good pieces count and list
  - Bad pieces count and list

### Sorting Section
- **Start Sorting Button**: Begin automated sorting
- **Progress Bar**: Visual progress indicator
- **Progress Label**: X/Y pieces processed
- **Activity Log**: Detailed operation log with timestamps

### Footer
- **Return to Home Button**: Manual home position command
- **Exit Button**: Close application safely

## Activity Log

The activity log shows:
- ℹ️ INFO: General information
- ✅ SUCCESS: Successful operations
- ❌ ERROR: Failed operations
- ⚠️ WARNING: Warnings and alerts

Each entry includes a timestamp in HH:MM:SS format.

## Troubleshooting

### Connection Issues
**Problem**: Cannot connect to robot
**Solutions**:
1. Verify robot server is running on the target machine
2. Check IP address is correct
3. Ensure port 5000 is not blocked by firewall
4. Verify network connectivity (ping the IP)

### Detection Issues
**Problem**: No pieces detected
**Solutions**:
1. Check camera is working properly
2. Ensure good lighting conditions
3. Verify YOLO model file (yolo.pt) exists
4. Check piece positions in camera view

### Sorting Issues
**Problem**: Pieces not picked/placed correctly
**Solutions**:
1. Verify positions.py has correct coordinates
2. Check robot calibration
3. Ensure gripper is functioning
4. Review activity log for specific errors

### GUI Issues
**Problem**: Interface doesn't display correctly
**Solutions**:
1. Ensure tkinter is installed
2. Check display settings
3. Try running on a different monitor
4. Update Python to latest version

## Advanced Usage

### Running Multiple Sorting Cycles
1. Complete first sorting cycle
2. Rearrange pieces on the workspace
3. Click "Start Detection" again
4. Click "Start Sorting" for the new batch

### Manual Home Return
Use the "🏠 Return to Home" button at any time to manually send the robot to home position (when not sorting).

### Changing Detection Settings
Modify YOLO parameters in:
- `yolo_inference.py` - Detection thresholds
- `cam.py` - Camera settings

## API Reference

### SortingInterface Class

#### Methods
- `connect_robot()`: Connect to robot server
- `disconnect_robot()`: Disconnect from robot
- `start_detection()`: Launch YOLO detection
- `start_sorting()`: Begin automated sorting
- `process_piece(piece_id, bin_name, status_type)`: Sort single piece
- `return_home()`: Move robot to home position
- `log_message(message, level)`: Add entry to activity log

#### Properties
- `robot_client`: RobotClient instance
- `good_pieces`: List of good piece IDs
- `bad_pieces`: List of bad piece IDs
- `is_connected`: Connection status
- `is_sorting`: Sorting process status
- `processed_pieces`: Count of processed pieces
- `total_pieces`: Total pieces to process

## Safety Notes

⚠️ **Important Safety Information**:
1. Ensure robot workspace is clear before sorting
2. Do not interrupt robot during pick/place operations
3. Emergency stop should be accessible at all times
4. Verify all positions are within robot's safe workspace
5. Test with slow speeds first before full operation

## Development

### Customization
To customize the interface:
1. Edit color scheme in `SortingInterface.__init__()`
2. Modify layout in `create_widgets()`
3. Add custom features by extending the class

### Integration
To integrate with other systems:
```python
from sorting_interface import SortingInterface

# Create custom interface
app = SortingInterface()
# Customize as needed
app.run()
```

## Version History

### Version 2.0 (Current)
- ✅ Complete GUI interface
- ✅ Automated sorting workflow
- ✅ Progress tracking
- ✅ Activity logging
- ✅ Error handling
- ✅ Threading for non-blocking operations

### Version 1.0 (Original)
- Basic command-line interface
- Manual sorting commands
- Simple YOLO integration

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review activity log for error details
3. Verify all dependencies are installed
4. Check robot server logs

## License

This project is part of the YOLO UR5 sorting system.

---

**Last Updated**: January 2026
**Compatible With**: Python 3.7+, UR5 Robot, YOLO v8+
