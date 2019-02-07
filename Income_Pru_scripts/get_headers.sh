#!/bin/bash

if [ -z "$1" ]
then
	echo "Usage: ./get_headers.sh <full path to csv file>"
	exit 10
fi

IN="$(head -n 1 $1 | sed 's/\t/;/g')"

n=1
IFS=';' read -ra ADDR <<< "$IN"
for i in "${ADDR[@]}"; do
    echo $n $i
    n=$((n+1))
done
