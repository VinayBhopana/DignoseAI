#!/bin/bash

# Ensure the backend directory is in the PYTHONPATH
export PYTHONPATH=$PYTHONPATH:$(pwd)

uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
