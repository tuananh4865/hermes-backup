#!/bin/bash
# Wrapper: auto-activate OmniVoice venv before running python script
VENV_PY="/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python"
if [ ! -f "$VENV_PY" ]; then
  VENV_PY="$(which python3)"
fi
exec "$VENV_PY" "$@"
