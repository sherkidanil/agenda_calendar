#!/bin/bash

python generate_calendar.py
git add .
git commit -m "$1"
git push -u origin main
