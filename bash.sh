#!/usr/bin/env bash

python main.py --im_path1 16.png --im_path2 15.png --im_path3 117.png --sign realistic --smooth 5


IFS='/'; for file in input/face/*; do read -a str <<< "$file"; python main.py --im_path1 90.png --im_path2 "${str[2]}" --im_path3 "${str[2]}" --sign realistic --smooth 5; done