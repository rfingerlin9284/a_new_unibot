# RBOTzilla Prelude (Prepended Instructions)

- File rule: **Self-contained** under `RICK_LIVE_PROTOTYPE/R_H_UNI`. Do not reference files outside this pack unless explicitly configured.
- Orders: **MUST** route via `pg_trade` so correlation/margin gates apply.
- Guardian: Assume the daemon enforces BE+5, time stops, ATR trailing, partial scale-outs, giveback exits.
- Session: Avoid fresh exposure near weekend close; tighten or flatten off-hours.
- Prioritize capital preservation: reduce margin to <=35% before adding risk.
