# R_H_UNI
UNIBOT JUST COINBASE AND OANDA

Stochastic-first policy
-----------------------

This project follows a "stochastic-first" policy: randomness is treated as
the default and reproducible (deterministic) runs are only an explicit opt-in
for debugging or auditing. Use the helpers in `stochastic.py` for randomness
and `wolf_packs.stochastic_config.load_thresholds()` to load thresholds with the
standard jitter applied.

Before running live trading, add structured logging and run a dry-run demo to
inspect behavior under realistic variability.

GS test results
---------------

Recent GS (gold-standard) tests were executed locally against `tests/wolf_packs`.
- Tests run: 2
- Passed: 2
- JUnit XML: `artifacts/20250926_041644/reports/gs_junit.xml`
- Log file: `artifacts/20250926_041644/reports/gs_test_log.txt`

To re-run the GS tests locally, see `scripts/run_gs_battery.sh` or run the
`bin/run_gs_tests.sh` helper. Generated artifacts are written under `artifacts/`.

## Dashboard (Read-Only)

The RICK dashboard provides real-time monitoring without execution paths.

### Quick Start

```bash
# Install dependencies
pip install streamlit pandas numpy websocket-client requests pyyaml plotly

# Run dashboard
DATA_ROOT=thefolder MODE=ghost streamlit run dashboard/app/main.py --server.port=8501

# Or use the launcher script
./scripts/launch_dashboard.sh
```

### Data Sources

- **Filesystem:** Reads from `thefolder/` (configurable via `DATA_ROOT` env var)
- **WebSocket:** Live signals from `ws://localhost:5056` (optional, graceful if unavailable)
- **HTTP:** Status page at `http://localhost:8080/status.html` (optional)

### Features

- Strategies leaderboard (win rate, Sharpe, VaR, RR)
- P&L aggregation from JSON files
- Live signals monitoring
- Data catalog browser
- Charter compliance footer (PIN 841921, RR≥3.2, -5% halt, ≤6h TTL)

### Configuration

Copy `.env.example` to `.env` and customize:
```bash
MODE=ghost
DATA_ROOT=thefolder
WS_URL=ws://localhost:5056
STATUS_HTTP_URL=http://localhost:8080/status.html
STREAMLIT_PORT=8501
```

**No write/execute paths are exposed by the dashboard.**
