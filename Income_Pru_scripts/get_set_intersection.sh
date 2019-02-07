#!/bin/bash

if [ -z "$1" ]
then
        echo "Usage: ./get_set_intersection.sh <full path to csv file 1> <column number in file 1 to join on> <full path to csv file 2> <column number in file 2 to join on> <full path to output file>"
        exit 10
fi

if [ -z "$2" ]
then
        echo "Usage: ./get_set_intersection.sh <full path to csv file 1> <column number in file 1 to join on> <full path to csv file 2> <column number in file 2 to join on> <full path to output file>"
        exit 11
fi

if [ -z "$3" ]
then
        echo "Usage: ./get_set_intersection.sh <full path to csv file 1> <column number in file 1 to join on> <full path to csv file 2> <column number in file 2 to join on> <full path to output file>"
        exit 12
fi

if [ -z "$4" ]
then
        echo "Usage: ./get_set_intersection.sh <full path to csv file 1> <column number in file 1 to join on> <full path to csv file 2> <column number in file 2 to join on> <full path to output file>"
        exit 13
fi

#join -i -t $'\t' -1 $2 -2 $4 <(sed 1d "$1" | sort -f) <(sed 1d "$3" | sort -f)

comm -12 <(cut -f $2 $1 | sed -n '1!p' | awk '{$1=$1};1' | sort -u) <(cut -f $4 $3 | sed -n '1!p' | awk '{$1=$1};1' | sort -u)
