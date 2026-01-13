"""
Test Dashboard - Quick test for the sorting dashboard
"""

def test_imports():
    """Test if all required packages are available."""
    print("\n" + "="*60)
    print("Testing Required Packages...")
    print("="*60)
    
    required = [
        ('tkinter', 'GUI framework'),
        ('cv2', 'OpenCV - Camera'),
        ('PIL', 'Pillow - Image processing'),
        ('ultralytics', 'YOLO model'),
        ('numpy', 'Numerical operations'),
    ]
    
    all_ok = True
    for package, description in required:
        try:
            if package == 'PIL':
                from PIL import Image, ImageTk
            else:
                __import__(package)
            print(f"✅ {package:15} - {description}")
        except ImportError:
            print(f"❌ {package:15} - {description} (MISSING!)")
            all_ok = False
    
    return all_ok


def test_files():
    """Test if required files exist."""
    print("\n" + "="*60)
    print("Checking Required Files...")
    print("="*60)
    
    import os
    
    files = [
        ('sorting_dashboard.py', 'Main dashboard'),
        ('robot_client.py', 'Robot communication'),
        ('yolo.pt', 'YOLO model'),
    ]
    
    all_ok = True
    for filename, description in files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename:25} - {description} ({size:,} bytes)")
        else:
            print(f"❌ {filename:25} - {description} (NOT FOUND!)")
            all_ok = False
    
    return all_ok


def test_camera():
    """Test if camera is accessible."""
    print("\n" + "="*60)
    print("Testing Camera Access...")
    print("="*60)
    
    try:
        import cv2
        
        # Try different camera indices
        for i in range(3):
            cap = cv2.VideoCapture(i)
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                if ret:
                    print(f"✅ Camera found at index {i}")
                    print(f"   Resolution: {frame.shape[1]}x{frame.shape[0]}")
                    return True
        
        print("❌ No working camera found")
        return False
        
    except Exception as e:
        print(f"❌ Camera test failed: {e}")
        return False


def test_yolo():
    """Test if YOLO model can be loaded."""
    print("\n" + "="*60)
    print("Testing YOLO Model...")
    print("="*60)
    
    try:
        from ultralytics import YOLO
        import os
        
        if not os.path.exists('yolo.pt'):
            print("❌ yolo.pt not found")
            return False
        
        print("Loading YOLO model...")
        model = YOLO('yolo.pt')
        print("✅ YOLO model loaded successfully")
        print(f"   Model: {model.model_name if hasattr(model, 'model_name') else 'YOLO'}")
        return True
        
    except Exception as e:
        print(f"❌ YOLO test failed: {e}")
        return False


def test_robot_client():
    """Test if RobotClient can be imported."""
    print("\n" + "="*60)
    print("Testing Robot Client...")
    print("="*60)
    
    try:
        from robot_client import RobotClient
        
        # Test instantiation
        client = RobotClient("127.0.0.1", 5000)
        print("✅ RobotClient imported successfully")
        print(f"   Default host: {client.host}")
        print(f"   Default port: {client.port}")
        
        # Check methods
        methods = ['connect', 'disconnect', 'pick_piece', 'place_piece', 'move_home']
        for method in methods:
            if hasattr(client, method):
                print(f"   ✅ Method: {method}()")
            else:
                print(f"   ❌ Missing method: {method}()")
        
        return True
        
    except Exception as e:
        print(f"❌ RobotClient test failed: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("  SORTING DASHBOARD TEST SUITE")
    print("="*70)
    
    results = []
    
    results.append(("Package Imports", test_imports()))
    results.append(("Required Files", test_files()))
    results.append(("Camera Access", test_camera()))
    results.append(("YOLO Model", test_yolo()))
    results.append(("Robot Client", test_robot_client()))
    
    # Summary
    print("\n" + "="*70)
    print("  TEST SUMMARY")
    print("="*70)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:20} {status}")
    
    print("\n" + "-"*70)
    print(f"Total: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Dashboard is ready to use.")
        print("\n" + "="*70)
        print("  TO START THE DASHBOARD:")
        print("="*70)
        print("\n  python run_sorting_system.py")
        print("\n  OR")
        print("\n  python sorting_dashboard.py")
        print("\n" + "="*70)
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        print("\nCommon fixes:")
        if not results[0][1]:
            print("  - Install packages: pip install ultralytics opencv-python pillow")
        if not results[2][1]:
            print("  - Check camera connection")
        if not results[3][1]:
            print("  - Ensure yolo.pt model file exists")
    
    print("\n")


if __name__ == "__main__":
    run_all_tests()
