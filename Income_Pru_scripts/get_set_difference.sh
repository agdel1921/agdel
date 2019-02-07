#!/bin/bash

if [ -z "$1" ]
then
        echo "Usage: ./get_set_difference.sh <fullpath to file 1> <column number in file 1> <fullpath to file 2> <column number in file 2>"
        exit 10
fi

if [ -z "$2" ]
then
        echo "Usage: ./get_set_difference.sh <fullpath to file 1> <column number in file 1> <fullpath to file 2> <column number in file 2>"
        exit 10
fi

if [ -z "$3" ]
then
        echo "Usage: ./get_set_difference.sh <fullpath to file 1> <column number in file 1> <fullpath to file 2> <column number in file 2>"
        exit 10
fi

if [ -z "$4" ]
then
        echo "Usage: ./get_set_difference.sh <fullpath to file 1> <column number in file 1> <fullpath to file 2> <column number in file 2>"
        exit 10
fi

comm -23 <(awk -v col=$2 -F "\"*\t\"*" '{print $col}' "$1" | sed 1d | awk '{$1=$1};1' | sort -f -k $2 | uniq) <(awk -v col=$4 -F "\"*\t\"*" '{print $col}' "$3" | sed 1d | awk '{$1=$1};1' | sort -f -k $4 | uniq)
