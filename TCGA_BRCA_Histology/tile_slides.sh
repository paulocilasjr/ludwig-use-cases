#!/bin/bash
# Make images directory and copy all files there.
# mkdir images
# find . -type f -name '*.svs' -exec cp {} images/ \;

input_list=$1

# Loop through slides (*.svs files) and tile them.
#for file in images/*.svs; do
while IFS= read -r file; do
    echo "Processing $file"
    podman run -v $(pwd):/pyhist/images/ mmunozag/pyhist \
    --patch-size 512 \
    --content-threshold 0.4 \
    --output-downsample 4 \
    --borders 0000 \
    --corners 1010 \
    --percentage-bc 1 \
    --k-const 1000 \
    --minimum_segmentsize 1000 \
    --save-patches --save-tilecrossed-image --info "verbose" --output images/  /pyhist/images/"$file"
done < "$input_list"
