#!/usr/bin/env bash
# Nonblocking public endpoint probe. Internal link validation lives in check_site.py.
set -u
domain="https://carolinadelacerda.com"
echo "Current UTC: $(date -u +%FT%TZ)"
echo "DNS results:"
getent ahostsv4 carolinadelacerda.com | head -5 || true
echo "Public HTTP checks:"
failed=0
for path in / /about/ /resume/ /contact/ /robots.txt /sitemap.xml /assets/carolina-headshot.webp; do
  result=$(curl -A "CarolinaPortfolioAudit/1.0" --connect-timeout 6 --max-time 12 -sS -L -o /dev/null \
    -w "http=%{http_code} redirect=%{num_redirects} total=%{time_total}s url=%{url_effective}" \
    "$domain$path" 2>&1)
  status=$?
  echo "$path $result"
  if [ "$status" -ne 0 ]; then echo "WARNING: curl returned $status for $path"; failed=$((failed+1)); continue; fi
  case "$result" in *"http=200 "*) ;; *) echo "WARNING: unexpected HTTP status $path"; failed=$((failed+1));; esac
done
echo "PUBLIC CHECKS FINISHED: $failed warning(s)."
# Do not fail repository static validation for DNS, propagation or external hosting issues.
exit 0
