#!/bin/bash
# Save the seedvis API key for vidclone without echoing it: ~/.secrets/seedvis_key (chmod 600).
# Run it in a terminal and paste the key at the prompt — never paste the key into this file.
mkdir -p ~/.secrets && chmod 700 ~/.secrets
read -rsp "Paste your seedvis API key, then Enter: " k; echo
[ -z "$k" ] && { echo "nothing entered, not saved"; exit 1; }
umask 077; printf '%s' "$k" > ~/.secrets/seedvis_key; chmod 600 ~/.secrets/seedvis_key
echo "saved ($(wc -c < ~/.secrets/seedvis_key) characters)"
