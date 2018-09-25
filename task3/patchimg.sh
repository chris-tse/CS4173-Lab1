#! /bin/bash
head -c 54 $1 > header
tail -c +55 $2 > body
cat header body > new.bmp