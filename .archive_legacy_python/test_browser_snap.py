#!/usr/bin/env python3
"""
test_browser_snap.py - Test browser automation with snap's chromedriver
PIN 841921 Approved
"""

import sys
from pathlib import Path

# Add project root to path
PROJECT_ROOT = Path("/home/ing/RICK/R_H_UNI")
sys.path.insert(0, str(PROJECT_ROOT))

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    import time
    
    print("🧪 Testing browser automation with snap's chromedriver...")
    
    # Setup Chrome options
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    # Use snap's chromedriver (version 141.x matches Chromium)
    chromedriver_path = "/snap/bin/chromium.chromedriver"
    service = Service(chromedriver_path)
    
    print(f"✅ Using chromedriver: {chromedriver_path}")
    
    # Create driver
    driver = webdriver.Chrome(service=service, options=options)
    
    print("✅ Chrome driver created successfully")
    
    # Test navigation
    driver.get("https://www.google.com")
    print(f"✅ Navigated to Google - Title: {driver.title}")
    
    # Clean up
    driver.quit()
    print("✅ Browser automation test PASSED")
    
    print("\n" + "="*60)
    print("🎯 BROWSER HIVE READY FOR INTEGRATION")
    print("="*60)
    print("\nNext steps:")
    print("1. Test individual AI providers (ChatGPT, Grok, DeepSeek)")
    print("2. Implement provider-specific selectors and flows")
    print("3. Create safe orchestration layer")
    print("4. Integrate with Rick's hive mind module")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
