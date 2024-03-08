# Loop through slides (*.svs files) and tile them.
# Usage: tile_slides.sh

for file in images/*.svs; do
    echo "Processing $file"
    docker run -v /Users/goecksj/projects/ludwig-use-cases/TCGA_BRCA_histology/:/pyhist/images/ mmunozag/pyhist \
    --patch-size 512 \
    --content-threshold 0.4 \
    --output-downsample 4 \
    --borders 0000 \
    --corners 1010 \
    --percentage-bc 1 \
    --k-const 1000 \
    --minimum_segmentsize 1000 \
    --save-patches --save-tilecrossed-image --info "verbose" --output images/ /pyhist/images/"$file"
done
