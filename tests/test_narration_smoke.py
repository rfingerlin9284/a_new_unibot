"""
Narration Smoke Test - Verify hardened logging works (Phase 8)
PIN: 841921
"""
import json
from pathlib import Path
from util.narration_logger import log_event, start_listener

def test_write_narration_line():
    """Test that narration can write and parse JSON"""
    import tempfile
    with tempfile.TemporaryDirectory() as tmp_dir:
        p = Path(tmp_dir) / "narration.jsonl"
        
        # Override default path for test
        import util.narration_hardened as nh
        old_path = nh.DEFAULT_PATH
        nh.DEFAULT_PATH = p
        nh._writer_started = False
        
        try:
            start_listener()
            log_event("PACK_ROUTED", regime="bull", pack="momentum_v2", reason="test")
            
            assert p.exists(), f"Log file not created: {p}"
            content = p.read_text().strip()
            assert content, "Log file is empty"
            
            obj = json.loads(content)
            assert obj["event"] == "PACK_ROUTED", f"Wrong event type: {obj['event']}"
            assert obj["pack"] == "momentum_v2", f"Wrong pack: {obj['pack']}"
            
            print("✅ test_write_narration_line PASSED")
            return True
        except Exception as e:
            print(f"❌ test_write_narration_line FAILED: {e}")
            return False
        finally:
            nh.DEFAULT_PATH = old_path
            nh._writer_started = False

if __name__ == "__main__":
    success = test_write_narration_line()
    exit(0 if success else 1)
