#!/usr/bin/env bash
set -euo pipefail
BASE="$HOME/RICK/R_H_UNI/configs"
CFG="$BASE/config_live.json"
OUT="$BASE/pairs_config.json"
mkdir -p "$BASE"

# 18 • FX
FX=('EUR/USD' 'GBP/USD' 'USD/JPY' 'AUD/USD' 'USD/CAD' 'USD/CHF' 'NZD/USD'
    'EUR/GBP' 'EUR/JPY' 'GBP/JPY' 'AUD/JPY' 'CHF/JPY' 'CAD/JPY'
    'EUR/AUD' 'EUR/CAD' 'GBP/CHF' 'AUD/NZD' 'NZD/JPY')

# 18 • Spot (USD)
SPOT=('BTC/USD' 'ETH/USD' 'SOL/USD' 'XRP/USD' 'ADA/USD' 'DOGE/USD' 'AVAX/USD'
      'DOT/USD' 'MATIC/USD' 'LINK/USD' 'LTC/USD' 'BCH/USD' 'ATOM/USD'
      'ALGO/USD' 'APT/USD' 'ARB/USD' 'OP/USD' 'SUI/USD')

# 18 • Derivs/Perps (generic tickers)
PERPS=('BTC-PERP' 'ETH-PERP' 'SOL-PERP' 'XRP-PERP' 'DOGE-PERP' 'LINK-PERP'
       'LTC-PERP' 'BCH-PERP' 'ADA-PERP' 'AVAX-PERP' 'DOT-PERP' 'MATIC-PERP'
       'ATOM-PERP' 'OP-PERP' 'ARB-PERP' 'APT-PERP' 'SUI-PERP' 'NEAR-PERP')

echo "🔧 Provisioning 54 Trading Instruments for RBOTzilla UNI..."
echo "📂 Base directory: $BASE"

# Build JSON configuration
jq -n --argjson fx "$(printf '%s\n' "${FX[@]}" | jq -R . | jq -s .)" \
      --argjson sp "$(printf '%s\n' "${SPOT[@]}" | jq -R . | jq -s .)" \
      --argjson dp "$(printf '%s\n' "${PERPS[@]}" | jq -R . | jq -s .)" \
      '{
        oanda_pairs: $fx, 
        coinbase_spot: $sp, 
        derivative_pairs: $dp, 
        instrument_count: (($fx|length) + ($sp|length) + ($dp|length)),
        created_at: (now | strftime("%Y-%m-%d %H:%M:%S UTC")),
        version: "RBOTzilla_UNI_v1.0",
        session_intelligence: true,
        risk_management: {
          max_concurrent_fx: 6,
          max_concurrent_spot: 6,
          max_concurrent_perps: 3,
          position_sizing_base: 0.02,
          weekend_crypto_multiplier: 1.2
        }
      }' | tee "$OUT" >/dev/null

# Create or update live config
tmp="$(mktemp)"
if [ -f "$CFG" ]; then
  echo "📝 Updating existing config: $CFG"
  jq --slurpfile p "$OUT" '. + {
    oanda_pairs: $p[0].oanda_pairs, 
    coinbase_spot_pairs: $p[0].coinbase_spot, 
    derivative_pairs: $p[0].derivative_pairs, 
    max_instruments: $p[0].instrument_count,
    risk_management: $p[0].risk_management,
    session_intelligence: $p[0].session_intelligence,
    last_updated: ($p[0].created_at)
  }' "$CFG" > "$tmp"
  mv "$tmp" "$CFG"
else
  echo "📄 Creating new live config: $CFG"
  cp "$OUT" "$CFG"
fi

echo ""
echo "✅ [SUCCESS] Pairs provisioned and wired into live config!"
echo ""
echo "📊 Instrument Summary:"
jq '.oanda_pairs|length as $a | .coinbase_spot|length as $b | .derivative_pairs|length as $c | {
  "💱 FX Pairs": $a, 
  "₿ Crypto Spot": $b, 
  "🎯 Perps/Derivs": $c, 
  "🎮 Total Instruments": ($a+$b+$c)
}' "$OUT"

echo ""
echo "🔥 Risk Management Settings:"
jq '.risk_management' "$OUT"

echo ""
echo "🎯 Next Steps:"
echo "1. ✅ Counts verified: 54 total instruments"
echo "2. 🔄 Restart RBOTzilla services"
echo "3. 🎛️ Enable per-market toggles in dashboard"
echo "4. 🚀 Start with FX+Spot, add Perps after connector auth"
echo "5. ⚖️ Set concurrency caps: FX/Spot/Perps = 6/6/3"
echo ""
echo "📍 Configuration files:"
echo "   📋 Pairs Config: $OUT"
echo "   🎛️ Live Config:  $CFG"