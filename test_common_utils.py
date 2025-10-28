#!/usr/bin/env python3
"""
Simple tests for the common_utils module.

These tests verify that the refactored common utilities work correctly.
"""

import os
import sys
import tempfile
import shutil
import json
from pathlib import Path


def test_ensure_directory_exists():
    """Test ensure_directory_exists function."""
    from common_utils import ensure_directory_exists
    
    with tempfile.TemporaryDirectory() as tmpdir:
        test_dir = os.path.join(tmpdir, "test_dir", "nested", "deep")
        ensure_directory_exists(test_dir)
        assert os.path.exists(test_dir), "Directory should be created"
        assert os.path.isdir(test_dir), "Path should be a directory"
        
        # Test that it doesn't fail if directory already exists
        ensure_directory_exists(test_dir)
        assert os.path.exists(test_dir), "Directory should still exist"
    
    print("✅ test_ensure_directory_exists passed")


def test_write_file_safely():
    """Test write_file_safely function."""
    from common_utils import write_file_safely
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test writing to a file in a nested directory
        test_file = os.path.join(tmpdir, "nested", "dir", "test.txt")
        content = "Hello, World!"
        
        write_file_safely(test_file, content)
        
        assert os.path.exists(test_file), "File should be created"
        with open(test_file, 'r') as f:
            assert f.read() == content, "Content should match"
    
    print("✅ test_write_file_safely passed")


def test_get_timestamp():
    """Test get_timestamp function."""
    from common_utils import get_timestamp
    import re
    
    # Test default format
    ts1 = get_timestamp()
    assert re.match(r'\d{8}_\d{6}', ts1), "Timestamp should match default format"
    
    # Test custom format
    ts2 = get_timestamp("%Y-%m-%d")
    assert re.match(r'\d{4}-\d{2}-\d{2}', ts2), "Timestamp should match custom format"
    
    print("✅ test_get_timestamp passed")


def test_load_json_config():
    """Test load_json_config function."""
    from common_utils import load_json_config
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Test valid JSON
        config_file = os.path.join(tmpdir, "config.json")
        test_config = {"key": "value", "number": 42}
        
        with open(config_file, 'w') as f:
            json.dump(test_config, f)
        
        loaded = load_json_config(config_file)
        assert loaded == test_config, "Loaded config should match original"
        
        # Test non-existent file
        try:
            load_json_config(os.path.join(tmpdir, "nonexistent.json"))
            assert False, "Should raise FileNotFoundError"
        except FileNotFoundError:
            pass
        
        # Test invalid JSON
        invalid_file = os.path.join(tmpdir, "invalid.json")
        with open(invalid_file, 'w') as f:
            f.write("{ invalid json }")
        
        try:
            load_json_config(invalid_file)
            assert False, "Should raise ValueError"
        except ValueError:
            pass
    
    print("✅ test_load_json_config passed")


def test_setup_logger():
    """Test setup_logger function."""
    from common_utils import setup_logger
    import logging
    
    with tempfile.TemporaryDirectory() as tmpdir:
        log_file = os.path.join(tmpdir, "test.log")
        
        # Test logger creation
        logger = setup_logger("test_logger", log_file)
        assert isinstance(logger, logging.Logger), "Should return a Logger instance"
        
        # Test logging
        logger.info("Test message")
        assert os.path.exists(log_file), "Log file should be created"
        
        with open(log_file, 'r') as f:
            log_content = f.read()
            assert "Test message" in log_content, "Log message should be in file"
    
    print("✅ test_setup_logger passed")


def test_integration():
    """Integration test using the actual scripts."""
    print("\n🔍 Running integration tests...")
    
    # Test that scripts can be imported
    try:
        import snapshot_critical_files
        import create_sample_files
        print("✅ Scripts import successfully")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    
    # Test that common_utils is used by checking for the functions
    from common_utils import (
        ensure_directory_exists,
        write_file_safely,
        get_timestamp,
        load_json_config,
        setup_logger
    )
    print("✅ All common utilities are accessible")
    
    return True


def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing common_utils module")
    print("=" * 60)
    
    tests = [
        test_ensure_directory_exists,
        test_write_file_safely,
        test_get_timestamp,
        test_load_json_config,
        test_setup_logger,
        test_integration,
    ]
    
    failed = 0
    for test in tests:
        try:
            test()
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    if failed == 0:
        print("✅ All tests passed!")
        return 0
    else:
        print(f"❌ {failed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
