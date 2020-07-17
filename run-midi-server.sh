#!/bin/bash

python cli.py \
    --mode midi \
    --modelIn models/jazz_progressions-12d.mdl.fasttext \
    --inPort 'VMini Out' \
    --outPort 'IAC Driver IAC - Bus 1'