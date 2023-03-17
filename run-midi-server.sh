#!/bin/bash

python cli.py \
    --mode midi \
    --modelIn models/maestro_progressions-12d.mdl.fasttext \
    --inPort 'VI49 Out' \
    --octaveOffset 0 \
    --spread 1.0 \
    --outPort 'M6'