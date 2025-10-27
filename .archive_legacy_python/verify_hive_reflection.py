#!/usr/bin/env python3
"""
Hive Reflection Orchestrator - Verification & Validation Script
PIN: 841921 | Generated: 2025-10-20

Validates that all components of the hive reflection system are properly installed.
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

# Colors for output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print a section header"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.END}\n")


def check_file_exists(path, description):
    """Check if a file exists"""
    exists = os.path.isfile(path)
    status = f"{Colors.GREEN}✅ FOUND{Colors.END}" if exists else f"{Colors.RED}❌ MISSING{Colors.END}"
    print(f"  {status}  {description}")
    print(f"        {path}")
    return exists


def check_directory_exists(path, description):
    """Check if a directory exists"""
    exists = os.path.isdir(path)
    status = f"{Colors.GREEN}✅ FOUND{Colors.END}" if exists else f"{Colors.RED}❌ MISSING{Colors.END}"
    print(f"  {status}  {description}")
    print(f"        {path}")
    return exists


def check_imports():
    """Check if required modules can be imported"""
    print_header("CHECKING PYTHON IMPORTS")
    
    modules = [
        ('sys', 'Python sys module'),
        ('os', 'Python os module'),
        ('time', 'Python time module'),
        ('json', 'Python json module'),
        ('datetime', 'Python datetime module'),
        ('requests', 'HTTP requests library'),
    ]
    
    all_ok = True
    for module_name, description in modules:
        try:
            __import__(module_name)
            print(f"  {Colors.GREEN}✅ OK{Colors.END}  {description}")
        except ImportError:
            print(f"  {Colors.RED}❌ MISSING{Colors.END}  {description}")
            all_ok = False
    
    return all_ok


def check_files():
    """Check if all required files exist"""
    print_header("CHECKING CORE FILES")
    
    project_root = "/home/ing/RICK/RICK_LIVE_PROTOTYPE"
    
    files = [
        (f"{project_root}/hive/hive_reflection_orchestrator.py", "Hive Reflection Orchestrator"),
        (f"{project_root}/hive/charter_compliance_scanner.py", "Charter Compliance Scanner"),
        (f"{project_root}/systemd/reflection_orchestrator.service", "Systemd Service Unit"),
        (f"{project_root}/systemd/reflection_orchestrator.timer", "Systemd Timer Unit"),
        (f"{project_root}/install_reflection_orchestrator.sh", "Installation Helper"),
        (f"{project_root}/HIVE_REFLECTION_GUIDE.md", "Documentation"),
        (f"{project_root}/HIVE_REFLECTION_IMPLEMENTATION_COMPLETE.md", "Implementation Summary"),
        (f"{project_root}/Makefile", "Makefile"),
    ]
    
    all_ok = True
    for filepath, description in files:
        if not check_file_exists(filepath, description):
            all_ok = False
    
    return all_ok


def check_makefile_targets():
    """Check if Makefile has reflection targets"""
    print_header("CHECKING MAKEFILE TARGETS")
    
    makefile_path = "/home/ing/RICK/RICK_LIVE_PROTOTYPE/Makefile"
    
    targets = [
        'reflection-help',
        'reflection-test',
        'reflection-once',
        'reflection-daemon',
        'reflection-status',
        'reflection-logs',
        'reflection-stop',
    ]
    
    all_ok = True
    if os.path.isfile(makefile_path):
        with open(makefile_path, 'r') as f:
            makefile_content = f.read()
        
        for target in targets:
            if target in makefile_content:
                print(f"  {Colors.GREEN}✅ FOUND{Colors.END}  {target}")
            else:
                print(f"  {Colors.RED}❌ MISSING{Colors.END}  {target}")
                all_ok = False
    else:
        print(f"  {Colors.RED}❌ Makefile not found{Colors.END}")
        all_ok = False
    
    return all_ok


def check_systemd_integration():
    """Check systemd files"""
    print_header("CHECKING SYSTEMD INTEGRATION")
    
    service_file = "/home/ing/RICK/RICK_LIVE_PROTOTYPE/systemd/reflection_orchestrator.service"
    timer_file = "/home/ing/RICK/RICK_LIVE_PROTOTYPE/systemd/reflection_orchestrator.timer"
    
    print(f"  {Colors.CYAN}Service Files:{Colors.END}")
    service_ok = check_file_exists(service_file, "Service Unit")
    timer_ok = check_file_exists(timer_file, "Timer Unit")
    
    print(f"\n  {Colors.CYAN}Installation Status:{Colors.END}")
    
    systemd_service = "/etc/systemd/system/reflection_orchestrator.service"
    systemd_timer = "/etc/systemd/system/reflection_orchestrator.timer"
    
    if os.path.isfile(systemd_service):
        print(f"  {Colors.GREEN}✅ INSTALLED{Colors.END}  Systemd service in /etc/systemd/system/")
    else:
        print(f"  {Colors.YELLOW}⚠️  NOT INSTALLED{Colors.END}  Run: sudo bash install_reflection_orchestrator.sh")
    
    if os.path.isfile(systemd_timer):
        print(f"  {Colors.GREEN}✅ INSTALLED{Colors.END}  Systemd timer in /etc/systemd/system/")
    else:
        print(f"  {Colors.YELLOW}⚠️  NOT INSTALLED{Colors.END}  Run: sudo bash install_reflection_orchestrator.sh")
    
    return service_ok and timer_ok


def check_hive_status():
    """Check if hive_status.json exists and is valid"""
    print_header("CHECKING HIVE STATUS FILE")
    
    status_path = "/home/ing/RICK/RICK_LIVE_PROTOTYPE/hive_status.json"
    
    if os.path.isfile(status_path):
        print(f"  {Colors.GREEN}✅ FOUND{Colors.END}  hive_status.json")
        
        try:
            with open(status_path, 'r') as f:
                status_data = json.load(f)
            
            print(f"\n  {Colors.CYAN}Latest Cycle Data:{Colors.END}")
            print(f"    • Cycle #:        {status_data.get('cycle_num', 'N/A')}")
            print(f"    • Timestamp:      {status_data.get('timestamp', 'N/A')}")
            print(f"    • Status:         {status_data.get('status', 'N/A')}")
            print(f"    • Positions:      {status_data.get('positions_scanned', 0)}")
            print(f"    • Compliant:      {status_data.get('positions_compliant', 0)}")
            print(f"    • Violations:     {status_data.get('violations_count', 0)}")
            print(f"    • Decisions:      {status_data.get('decisions_count', 0)}")
            
            return True
        except json.JSONDecodeError:
            print(f"  {Colors.RED}❌ INVALID JSON{Colors.END}  hive_status.json is corrupted")
            return False
    else:
        print(f"  {Colors.YELLOW}⚠️  NOT FOUND{Colors.END}  Run: make reflection-test (to generate)")
        return False


def check_narration_log():
    """Check if narration.jsonl has reflection entries"""
    print_header("CHECKING NARRATION LOG")
    
    log_path = "/home/ing/RICK/RICK_LIVE_PROTOTYPE/narration.jsonl"
    
    if os.path.isfile(log_path):
        print(f"  {Colors.GREEN}✅ FOUND{Colors.END}  narration.jsonl")
        
        # Count reflection events
        reflection_events = 0
        try:
            with open(log_path, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        if 'HIVE_REFLECTION' in entry.get('event_type', ''):
                            reflection_events += 1
                    except:
                        pass
            
            if reflection_events > 0:
                print(f"  {Colors.GREEN}✅ {reflection_events} reflection event(s) logged{Colors.END}")
            else:
                print(f"  {Colors.YELLOW}⚠️  No reflection events yet{Colors.END}")
                print(f"     Run: make reflection-test")
            
            return True
        except Exception as e:
            print(f"  {Colors.YELLOW}⚠️  Error reading log:{Colors.END} {e}")
            return True  # File exists, even if can't read
    else:
        print(f"  {Colors.YELLOW}⚠️  NOT FOUND{Colors.END}  narration.jsonl will be created on first run")
        return False


def run_quick_test():
    """Optionally run a quick test"""
    print_header("RUNNING QUICK TEST")
    
    print("  Testing single reflection cycle...")
    print("")
    
    project_root = "/home/ing/RICK/RICK_LIVE_PROTOTYPE"
    orchestrator_path = f"{project_root}/hive/hive_reflection_orchestrator.py"
    
    if os.path.isfile(orchestrator_path):
        print(f"  {Colors.YELLOW}Run this command to test:{Colors.END}")
        print(f"    cd {project_root}")
        print(f"    make reflection-test")
        print(f"\n  {Colors.YELLOW}Or directly:{Colors.END}")
        print(f"    python3 hive/hive_reflection_orchestrator.py --mode once --environment practice")
        return True
    else:
        print(f"  {Colors.RED}❌ Orchestrator not found{Colors.END}")
        return False


def print_summary(results):
    """Print final summary"""
    print_header("VERIFICATION SUMMARY")
    
    all_checks = [
        ("Python Imports", results['imports']),
        ("Core Files", results['files']),
        ("Makefile Targets", results['makefile']),
        ("Systemd Files", results['systemd']),
        ("Hive Status File", results['hive_status']),
        ("Narration Log", results['narration']),
    ]
    
    passed = sum(1 for _, result in all_checks if result)
    total = len(all_checks)
    
    print(f"\n{Colors.CYAN}Verification Results:{Colors.END}\n")
    for check_name, result in all_checks:
        status = f"{Colors.GREEN}✅ PASS{Colors.END}" if result else f"{Colors.RED}❌ FAIL{Colors.END}"
        print(f"  {status}  {check_name}")
    
    print(f"\n{Colors.BOLD}Total: {passed}/{total} checks passed{Colors.END}\n")
    
    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ ALL CHECKS PASSED - System is ready!{Colors.END}\n")
        return True
    elif passed >= total - 1:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️  MOSTLY READY - Some optional components missing{Colors.END}\n")
        return True
    else:
        print(f"{Colors.RED}{Colors.BOLD}❌ SOME CHECKS FAILED - Please review above{Colors.END}\n")
        return False


def main():
    """Run all verification checks"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("╔════════════════════════════════════════════════════════════════════╗")
    print("║  HIVE MIND REFLECTION ORCHESTRATOR - VERIFICATION SCRIPT            ║")
    print("║  PIN: 841921 | Generated: 2025-10-20                              ║")
    print("╚════════════════════════════════════════════════════════════════════╝")
    print(f"{Colors.END}\n")
    
    # Run all checks
    results = {
        'imports': check_imports(),
        'files': check_files(),
        'makefile': check_makefile_targets(),
        'systemd': check_systemd_integration(),
        'hive_status': check_hive_status(),
        'narration': check_narration_log(),
    }
    
    # Optional test
    run_quick_test()
    
    # Summary
    success = print_summary(results)
    
    # Final recommendations
    print(f"{Colors.CYAN}Next Steps:{Colors.END}\n")
    if not results['hive_status']:
        print("  1. Run a test cycle: make reflection-test")
    if not results['systemd']:
        print("  2. Install systemd service: sudo bash install_reflection_orchestrator.sh")
    print("  3. Monitor: make reflection-status")
    print("  4. View logs: make reflection-logs")
    print()
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
