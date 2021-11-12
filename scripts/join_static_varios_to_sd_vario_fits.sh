#! /bin/bash

#join static and vario_fit files based on circle_id

for static_vario_file in `cat fitlist`
    do
    gjoin --nocheck-order -a 1 -t , -e -9999 -o auto joinbase $static_vario_file > temp
    mv temp joinbase
    done

#cp joinbase static_varios_sd_vario_fits_v8.txt
cp joinbase static_vario_fits_v8.txt
