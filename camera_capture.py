#!/bin/bash

# cam-capture.sh
# A CLI tool to capture images using Pi Camera (libcamera)

OUTDIR="$HOME/Pictures"
FILENAME="capture_$(date +%Y%m%d_%H%M%S).jpg"
FULLPATH="$OUTDIR/$FILENAME"

mkdir -p "$OUTDIR"

echo "Capturing image to $FULLPATH ..."
libcamera-jpeg -o "$FULLPATH"

if [ $? -eq 0 ]; then
    echo "Image saved successfully!"
else
    echo "Failed to capture image."
fi

