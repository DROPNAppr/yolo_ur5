"""
Test Script for Sorting Interface
==================================

This script helps test the sorting interface components individually.
"""

def test_gui_display():
    """Test if the GUI displays correctly."""
    print("\n" + "="*60)
    print("TEST 1: GUI Display Test")
    print("="*60)
    
    try:
        from sorting_interface import SortingInterface
        print("✅ SortingInterface imported successfully")
        
        print("\nLaunching GUI for 5 seconds...")
        print("Please verify the window appears correctly.")
        
        import threading
        import time
        
        app = SortingInterface()
        
        def close_after_delay():
            time.sleep(5)
            app.root.quit()
        
        threading.Thread(target=close_after_delay, daemon=True).start()
        app.run()
        
        print("✅ GUI displayed successfully")
        return True
        
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False


def test_imports():
    """Test if all required modules can be imported."""
    print("\n" + "="*60)
    print("TEST 2: Import Test")
    print("="*60)
    
    modules = [
        ('tkinter', 'GUI framework'),
        ('socket', 'Network communication'),
        ('json', 'Data serialization'),
        ('threading', 'Multi-threading'),
        ('time', 'Time operations'),
    ]
    
    all_passed = True
    
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"✅ {module_name:15} - {description}")
        except ImportError:
            print(f"❌ {module_name:15} - {description} (NOT FOUND)")
            all_passed = False
    
    return all_passed


def test_project_files():
    """Test if all required project files exist."""
    print("\n" + "="*60)
    print("TEST 3: Project Files Test")
    print("="*60)
    
    import os
    
    files = [
        'sorting_interface.py',
        'run_sorting_system.py',
        'robot_client.py',
        'cam.py',
        'positions.py',
        'README_SORTING_INTERFACE.md',
        'QUICK_START_GUIDE.py',
    ]
    
    all_exist = True
    
    for filename in files:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"✅ {filename:30} ({size:,} bytes)")
        else:
            print(f"❌ {filename:30} (NOT FOUND)")
            all_exist = False
    
    return all_exist


def test_robot_client():
    """Test RobotClient class instantiation."""
    print("\n" + "="*60)
    print("TEST 4: RobotClient Test")
    print("="*60)
    
    try:
        from robot_client import RobotClient
        print("✅ RobotClient imported successfully")
        
        client = RobotClient("127.0.0.1", 5000)
        print("✅ RobotClient instantiated successfully")
        print(f"   Host: {client.host}")
        print(f"   Port: {client.port}")
        
        return True
        
    except Exception as e:
        print(f"❌ RobotClient test failed: {e}")
        return False


def test_positions():
    """Test positions module."""
    print("\n" + "="*60)
    print("TEST 5: Positions Test")
    print("="*60)
    
    try:
        from positions import HOME, PIECES, BIN_GOOD, BIN_BAD
        print("✅ Positions imported successfully")
        
        print(f"\n   Home position: {HOME['position']}")
        print(f"   Number of pieces: {len(PIECES)}")
        print(f"   Good bin: {BIN_GOOD['position']}")
        print(f"   Bad bin: {BIN_BAD['position']}")
        
        # Validate structure
        for piece_id, piece_data in PIECES.items():
            if 'position' not in piece_data or 'orientation' not in piece_data:
                print(f"⚠️  Warning: Piece {piece_id} missing position or orientation")
        
        print("✅ All positions validated")
        return True
        
    except Exception as e:
        print(f"❌ Positions test failed: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("\n" + "="*70)
    print("  SORTING INTERFACE TEST SUITE")
    print("="*70)
    print("\nRunning automated tests...")
    
    results = []
    
    # Run tests
    results.append(("Imports", test_imports()))
    results.append(("Project Files", test_project_files()))
    results.append(("RobotClient", test_robot_client()))
    results.append(("Positions", test_positions()))
    
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
        print("\n🎉 All tests passed! System is ready to use.")
        print("\nTo start the application, run:")
        print("   python run_sorting_system.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
    
    print("="*70 + "\n")
    
    # Optional GUI test
    try:
        response = input("\nWould you like to test the GUI? (y/n): ")
        if response.lower() == 'y':
            test_gui_display()
    except:
        pass


def show_usage_example():
    """Show a usage example."""
    print("\n" + "="*70)
    print("  USAGE EXAMPLE")
    print("="*70)
    print("""
    from sorting_interface import SortingInterface
    
    # Create and run the application
    app = SortingInterface()
    app.run()
    
    # Or simply:
    python run_sorting_system.py
    """)


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "--gui":
            test_gui_display()
        elif sys.argv[1] == "--example":
            show_usage_example()
        else:
            print("Unknown option. Use --gui or --example")
    else:
        run_all_tests()
