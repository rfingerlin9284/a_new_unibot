#!/usr/bin/env bash
# Usage: pecho CHANNEL "Header text" "- Bullet 1" "- Bullet 2"
# Creates clean, color-coded blocks with separators

_pecho_color() {
  case "${1^^}" in
    TRADE)     echo 39  ;; # Bright blue
    SIGNAL)    echo 214 ;; # Orange
    GATE)      echo 203 ;; # Pink/red
    PROTECTION) echo 135 ;; # Purple
    PROFIT)    echo 82  ;; # Green
    LOSS)      echo 196 ;; # Red
    SYSTEM)    echo 244 ;; # Gray
    INFO)      echo 45  ;; # Cyan
    WARN)      echo 226 ;; # Yellow
    ERROR)     echo 196 ;; # Red
    *)         echo 81  ;; # Bright cyan default
  esac
}

pecho() {
  local channel="${1:-INFO}"; shift || true
  local color=$(_pecho_color "$channel")
  local reset="\033[0m"
  local fg="\033[38;5;${color}m"
  local bold="\033[1m"
  
  # Top border
  printf "${fg}┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓${reset}\n"
  printf "${fg}┃${reset} ${bold}${fg}%-15s${reset} ${fg}│${reset} %s\n" "${channel^^}" "$(date '+%H:%M:%S')"
  printf "${fg}┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩${reset}\n"
  
  # Message lines with clean spacing
  for line in "$@"; do
    if [[ "$line" =~ ^[[:space:]]*[-•] ]]; then
      # Bullet point
      printf "  ${fg}•${reset} %s\n" "${line#*[-• ]}"
    else
      # Regular text with indent
      printf "    %s\n" "$line"
    fi
  done
  
  # Bottom border + blank separator
  printf "${fg}└────────────────────────────────────────────────────────────────┘${reset}\n"
  printf "\n"  # Blank line between blocks
}

export -f pecho
