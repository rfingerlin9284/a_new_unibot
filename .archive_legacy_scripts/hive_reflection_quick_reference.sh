#!/usr/bin/env bash
# HIVE REFLECTION ORCHESTRATOR - QUICK REFERENCE CARD
# PIN: 841921 | Generated: 2025-10-20

cat << 'CARD'

╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║        🧠 HIVE MIND REFLECTION ORCHESTRATOR - QUICK REFERENCE       ║
║                                                                      ║
║              30-Second Autonomous Trade Management                  ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 ESSENTIAL COMMANDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HELP:
  make reflection-help              Show full help menu

TEST (Development):
  make reflection-test              Run single reflection cycle

DAEMON (Development):
  make reflection-daemon            Start 30-second loop (Ctrl+C to stop)
  make reflection-stop              Stop daemon

MONITOR (Anytime):
  make reflection-status            View latest cycle results
  make reflection-logs              Tail real-time logs

VERIFY:
  python3 verify_hive_reflection.py Full system verification

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🚀 DEPLOYMENT (Production - Requires sudo)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

INSTALL SYSTEMD SERVICE:
  sudo bash install_reflection_orchestrator.sh

CHECK STATUS:
  systemctl status reflection_orchestrator.timer

VIEW LOGS:
  journalctl -u reflection_orchestrator.service -f

SWITCH TO LIVE:
  sudo nano /etc/systemd/system/reflection_orchestrator.service
  # Change: --environment practice
  # To:     --environment live
  sudo systemctl restart reflection_orchestrator.service

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 WHAT GETS MONITORED (Every 30 Seconds)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

POSITION LEVEL:
  ✓ Entry/exit prices & profit metrics
  ✓ Stop loss >= 18 pips
  ✓ Risk/reward >= 3.2:1
  ✓ Position age <= 6 hours

ACCOUNT LEVEL:
  ✓ Total positions <= 3
  ✓ Margin utilization <= 35%
  ✓ Daily loss > -5%

HIVE LEVEL:
  ✓ GPT (35%), GROK (35%), DEEPSEEK (30%) consensus
  ✓ Confidence scores
  ✓ Recommendations (HOLD/REDUCE/EXIT/ADD)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 THE 30-SECOND REFLECTION CYCLE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

[1] FETCH POSITIONS           from OANDA API
    └─ Get all open trades
    └─ Calculate profit metrics

[2] VALIDATE CHARTER          check 6 immutable rules
    └─ MIN_SL, MIN_RR, MAX_MARGIN, MAX_POSITIONS, TTL, DAILY_LOSS
    └─ Alert on violations

[3] QUERY HIVE CONSENSUS      ask GPT/GROK/DEEPSEEK
    └─ Get member votes
    └─ Calculate consensus
    └─ Generate recommendations

[4] EXECUTE DECISIONS         take action
    └─ REDUCE: Close 50%
    └─ EXIT: Close 100%
    └─ ADD: Add 25%
    └─ HOLD: No change

[5] LOG DECISIONS             audit trail
    └─ Write to narration.jsonl
    └─ Complete transparency

[6] UPDATE STATUS             for dashboard
    └─ Write hive_status.json
    └─ Real-time metrics

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 OUTPUT FILES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

hive_status.json:
  └─ Updated every 30 seconds
  └─ Current cycle metrics
  └─ Last 5 cycles history
  └─ Read by dashboard

narration.jsonl:
  └─ Appended every reflection cycle
  └─ Complete audit trail
  └─ All decisions & violations
  └─ Timestamps for replay

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔧 TROUBLESHOOTING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

No positions detected?
  → Check OANDA API: make test-broker
  → Verify credentials in master.env

No hive decisions?
  → Lower confidence threshold if needed
  → Check hive member availability

Systemd not working?
  → Check status: systemctl status reflection_orchestrator.timer
  → View logs: journalctl -xe

Charter violations constant?
  → Review narration.jsonl for violation details
  → Check position SL/TP placement

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 DOCUMENTATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

HIVE_REFLECTION_GUIDE.md
  └─ Complete user guide (400+ lines)
  └─ Configuration & monitoring

HIVE_REFLECTION_IMPLEMENTATION_COMPLETE.md
  └─ Architecture & design details (450+ lines)

HIVE_REFLECTION_DELIVERY_SUMMARY.md
  └─ Feature summary & examples (450+ lines)

HIVE_REFLECTION_NEXT_STEPS.md
  └─ Deployment checklist & integration guide

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎓 GETTING STARTED (5 Minutes)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Test the system:
   $ make reflection-test

2. Review the output:
   $ cat hive_status.json | python3 -m json.tool

3. Check documentation:
   $ cat HIVE_REFLECTION_GUIDE.md | head -50

4. Run verification:
   $ python3 verify_hive_reflection.py

5. When confident, deploy:
   $ sudo bash install_reflection_orchestrator.sh

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 FILES CREATED (11 Total)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

CORE (7):
  hive/hive_reflection_orchestrator.py
  hive/charter_compliance_scanner.py
  systemd/reflection_orchestrator.service
  systemd/reflection_orchestrator.timer
  install_reflection_orchestrator.sh
  verify_hive_reflection.py
  Makefile (updated with 7 new targets)

DOCUMENTATION (4):
  HIVE_REFLECTION_GUIDE.md
  HIVE_REFLECTION_IMPLEMENTATION_COMPLETE.md
  HIVE_REFLECTION_DELIVERY_SUMMARY.md
  HIVE_REFLECTION_NEXT_STEPS.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔐 CHARTER RULES (Immutable & Always Enforced)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✓ MIN_SL >= 18 pips              (Never place tighter stops)
✓ MIN_RR >= 3.2:1               (Risk/reward minimum)
✓ MAX_MARGIN <= 35%             (Leverage hard cap)
✓ MAX_POSITIONS <= 3            (Portfolio concentration limit)
✓ MAX_HOLD_TIME <= 6 hours      (Time-to-live protection)
✓ DAILY_LOSS > -5%              (Daily circuit breaker)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ VERIFICATION STATUS (Last Run)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ✅ PASS  Python Imports
  ✅ PASS  Core Files (7/7)
  ✅ PASS  Makefile Targets (7/7)
  ✅ PASS  Systemd Files
  ✅ PASS  Hive Status File
  ⚠️  WARN Narration Log (Created on first trade)

Total: 5/6 PASSED → System is READY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 NEXT ACTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

$ make reflection-test

Your hive mind collective is standing by.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PIN: 841921 | Charter: RBOTzilla UNI Phase 9 | Status: ✅ OPERATIONAL

CARD
