#!/bin/bash

# google HTTP time update
/bin/date -s "$(/usr/bin/wget -qSO- --max-redirect=0 google.com 2>&1 | /bin/grep Date: | /usr/bin/cut -d' ' -f5-8)Z"
