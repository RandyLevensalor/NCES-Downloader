#!/bin/bash
TOTAL=44039
clear
EMAIL="email@example.com"

function send_email {
    local subject="$1"
    local body="$2"
    echo "$body" | mail -s "$subject" "$EMAIL"
}

while true; do

  COMPLETED=$(find saved_pages | wc -l)
  if [ "$COMPLETED" -ge $TOTAL ]; then
    echo "Done!"
    send_email "Done" "The program schools_by_zip.py is done."
    break
  fi
  result=$((COMPLETED * 100 / TOTAL))
  echo "Result: $COMPLETED ($result%)"
  sleep 5
  clear

  pgrep -f "/usr/local/Cellar/python@3.11/3.11.3/Frameworks/Python.framework/Versions/3.11/Resources/Python.app/Contents/MacOS/Python schools_by_zip.py" > /dev/null
  if [ $? -ne 0 ]; then
    echo "The program schools_by_zip.py is no longer running."
    send_email "No longer running" "The program schools_by_zip.py is no longer running."
    exit 1
  fi

done



