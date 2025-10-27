#!/usr/bin/env python3
"""
Pytest Guardrails Test Suite
Validates safety state before any live deployment
"""

import pytest
import os
import json
import subprocess
from pathlib import Path

# Test configuration
PROJECT_ROOT = Path("/home/ing/RICK/R_H_UNI")
REQUIRED_FILES = [
    ".upgrade_toggle",
    "DASH_SYSTEM_UPGRADE/scripts/enable_headless_live.sh",
    "launch_battlestation.sh",
    "ghost_trading_engine.py"
]

class TestGuardrails:
    
    def test_upgrade_toggle_off_or_missing(self):
        """Ensure .upgrade_toggle is OFF or missing (safe state)"""
        toggle_file = PROJECT_ROOT / ".upgrade_toggle"
        
        if toggle_file.exists():
            toggle_value = toggle_file.read_text().strip()
            assert toggle_value == "OFF", f"❌ .upgrade_toggle is '{toggle_value}' (should be OFF)"
            print("✅ .upgrade_toggle is OFF (safe)")
        else:
            print("✅ .upgrade_toggle missing (treat as OFF - safe)")
    
    def test_no_upgrade_target_or_safe(self):
        """Ensure .upgrade_target is not set or is safe"""
        target_file = PROJECT_ROOT / ".upgrade_target"
        
        if target_file.exists():
            target_value = target_file.read_text().strip()
            safe_targets = ["headless", "standalone", ""]
            assert target_value in safe_targets, f"❌ Unknown .upgrade_target: '{target_value}'"
            print(f"✅ .upgrade_target: '{target_value}' (acceptable)")
        else:
            print("✅ .upgrade_target not set (safe)")
    
    def test_no_live_config_or_safe_mode(self):
        """Ensure live/config.json is missing or in safe mode"""
        live_config = PROJECT_ROOT / "live/config.json"
        
        if live_config.exists():
            try:
                config = json.loads(live_config.read_text())
                mode = config.get("mode", "unknown")
                real_money = config.get("real_money", False)
                
                # Allow demo/sandbox modes
                safe_modes = ["demo", "sandbox", "simulation", "test"]
                assert mode in safe_modes or not real_money, f"❌ Live config in unsafe mode: {mode}, real_money: {real_money}"
                print(f"✅ Live config safe: mode={mode}, real_money={real_money}")
            except json.JSONDecodeError:
                pytest.fail("❌ live/config.json exists but is invalid JSON")
        else:
            print("✅ live/config.json not present (safe)")
    
    def test_no_demo_strings_in_env(self):
        """Check for demo/placeholder strings in environment files"""
        env_files = [".env", ".env.local", ".env.production"]
        
        demo_indicators = ["demo", "sandbox", "placeholder", "YOUR_KEY_HERE", "changeme"]
        
        for env_file in env_files:
            env_path = PROJECT_ROOT / env_file
            if env_path.exists():
                content = env_path.read_text().lower()
                found_demo = [indicator for indicator in demo_indicators if indicator in content]
                
                if found_demo:
                    print(f"⚠️  {env_file} contains demo indicators: {found_demo}")
                    # This is a warning, not a failure for .env.sample
                    if env_file != ".env.sample":
                        pytest.fail(f"❌ {env_file} contains demo strings: {found_demo}")
                else:
                    print(f"✅ {env_file} looks production-ready")
    
    def test_required_files_exist(self):
        """Ensure critical files are present"""
        missing_files = []
        
        for required_file in REQUIRED_FILES:
            file_path = PROJECT_ROOT / required_file
            if not file_path.exists():
                missing_files.append(required_file)
        
        assert not missing_files, f"❌ Missing required files: {missing_files}"
        print(f"✅ All required files present: {len(REQUIRED_FILES)} files")
    
    def test_no_active_live_processes(self):
        """Ensure no live trading processes are running"""
        try:
            # Check for processes that might be live trading
            result = subprocess.run(
                ["pgrep", "-f", "live.*trading|oanda.*live|coinbase.*live"],
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                processes = result.stdout.strip().split('\n')
                pytest.fail(f"❌ Live trading processes detected: {processes}")
            else:
                print("✅ No live trading processes detected")
                
        except FileNotFoundError:
            print("⚠️  pgrep not available - skipping process check")
    
    def test_git_clean_state(self):
        """Ensure git working tree is clean"""
        try:
            # Check git status
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=PROJECT_ROOT,
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                changes = result.stdout.strip()
                if changes:
                    print(f"⚠️  Git working tree has changes:\n{changes}")
                    # This is a warning, not a failure
                else:
                    print("✅ Git working tree is clean")
            else:
                print("⚠️  Git status check failed")
                
        except FileNotFoundError:
            print("⚠️  Git not available - skipping git check")
    
    def test_pre_upgrade_tag_exists(self):
        """Check if pre-upgrade tag exists (recommended but not required)"""
        try:
            result = subprocess.run(
                ["git", "tag", "--list", "pre_upgrade_*"],
                cwd=PROJECT_ROOT,
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                tags = result.stdout.strip().split('\n')
                tags = [tag for tag in tags if tag]  # Remove empty strings
                
                if tags:
                    latest_tag = tags[-1]
                    print(f"✅ Pre-upgrade tag found: {latest_tag}")
                else:
                    print("⚠️  No pre-upgrade tag found - consider creating one")
            else:
                print("⚠️  Git tag check failed")
                
        except FileNotFoundError:
            print("⚠️  Git not available - skipping tag check")
    
    def test_battlestation_executable(self):
        """Ensure battlestation launcher is executable"""
        battlestation = PROJECT_ROOT / "launch_battlestation.sh"
        
        if battlestation.exists():
            assert os.access(battlestation, os.X_OK), "❌ launch_battlestation.sh is not executable"
            print("✅ launch_battlestation.sh is executable")
        else:
            pytest.fail("❌ launch_battlestation.sh not found")
    
    def test_dash_system_upgrade_directory(self):
        """Ensure DASH_SYSTEM_UPGRADE directory exists with correct structure"""
        dash_dir = PROJECT_ROOT / "DASH_SYSTEM_UPGRADE"
        
        assert dash_dir.exists(), "❌ DASH_SYSTEM_UPGRADE directory missing"
        assert dash_dir.is_dir(), "❌ DASH_SYSTEM_UPGRADE is not a directory"
        
        # Check for key subdirectories
        expected_dirs = ["scripts", "tools", "assets", "narration", "adapters"]
        missing_dirs = []
        
        for expected_dir in expected_dirs:
            if not (dash_dir / expected_dir).exists():
                missing_dirs.append(expected_dir)
        
        if missing_dirs:
            print(f"⚠️  Missing DASH_SYSTEM_UPGRADE subdirectories: {missing_dirs}")
        else:
            print("✅ DASH_SYSTEM_UPGRADE structure complete")

if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "-s"])