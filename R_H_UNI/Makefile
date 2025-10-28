SHELL := /usr/bin/env bash
BASE  := /home/ing/RICK/RICK_LIVE_PROTOTYPE/R_H_UNI
PY    := python3

export PYTHONPATH := $(BASE):$(PYTHONPATH)
export PATH := $(HOME)/.local/bin:$(PATH)

REQS = python-dotenv requests

.PHONY: help deps audit guardian.start guardian.stop guardian.logs status trade.buy trade.sell

help:
	@echo "Targets: deps | audit | guardian.start|stop|logs | status | trade.buy SYMBOL= XXX UNITS= N [DRY=1] | trade.sell ..."

deps:
	@$(PY) - <<'PY'
import subprocess, sys
mods = "$(REQS)".split()
for m in mods:
    try:
        __import__(m.replace('-','_'))
    except Exception:
        try:
            subprocess.check_call([sys.executable,"-m","pip","install","--user",m])
        except Exception:
            pass
PY

audit: deps
	@bash $(BASE)/scripts/audit_sync.sh

guardian.start: deps
	@echo "(placeholder) enable guardian service here" && true

guardian.stop:
	@echo "(placeholder) stop guardian service here" && true

guardian.logs:
	@echo "(placeholder) tail guardian logs here" && true

status:
	@$(PY) $(BASE)/tools/status.py

trade.buy:
	@test -n "$(SYMBOL)" -a -n "$(UNITS)" || (echo "usage: make trade.buy SYMBOL=GBPUSD UNITS=2000 [DRY=1]"; exit 2)
	@echo "(placeholder) pg_trade --venue oanda --symbol $(SYMBOL) --side buy --units $(UNITS) $(if $(DRY),--dry-run,)" && true

trade.sell:
	@test -n "$(SYMBOL)" -a -n "$(UNITS)" || (echo "usage: make trade.sell SYMBOL=GBPUSD UNITS=2000 [DRY=1]"; exit 2)
	@echo "(placeholder) pg_trade --venue oanda --symbol $(SYMBOL) --side sell --units $(UNITS) $(if $(DRY),--dry-run,)" && true
