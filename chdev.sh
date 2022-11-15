#!/bin/bash

project_directory=$(ls ~/projects | fzf --layout=reverse --border=rounded --height=20 --prompt='Directory: ')

if [ -z "$project_directory" ]; then
  exit 0
fi

echo $project_directory
cd ~/projects/$project_directory

echo $(dirname $0)
# $(dirname $0)/start.py
