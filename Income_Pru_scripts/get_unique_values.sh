#!/bin/bash

if [ -z "$1" ]
then
        echo "Usage: ./get_unique_values.sh <full path to csv file> <column_number>"
	echo "column_number starts from 1"
        exit 10
fi

if [ -z "$2" ]
then
        echo "Usage: ./get_headers.sh <full path to csv file> <column_number>"
	echo "column_number starts from 1"
        exit 11
fi

cut -f $2 $1 | sed -n '1!p' | awk '{$1=$1};1' | sort -fu
