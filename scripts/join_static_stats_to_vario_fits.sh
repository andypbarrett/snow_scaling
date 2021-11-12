#! /bin/bash

#join static and vario_fit files based on circle_id

for sd_file in `cat sd_vario_fitlist`
    do
    gjoin --nocheck-order -a 1 -t , -e -9999 -o auto joinbase $sd_file > temp
    mv temp joinbase
    done

#cp joinbase static_stats_vario_fits_v8.txt
cp joinbase sd_vario_fits_v8.txt
