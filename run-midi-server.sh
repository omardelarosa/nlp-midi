#!/bin/bash

python cli.py \
    --mode midi \
    --modelIn models/maestro_progressions-12d.mdl.fasttext \
    --inPort 'VMini Out' \
    --octaveOffset 0 \
    --spread 1.0 \
    --outPort 'IAC Driver IAC - Bus 1'