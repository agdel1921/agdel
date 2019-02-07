#!/bin/python

import sys, csv

def main(output_file):
    with open(output_file, "wb") as fo:
        writer = csv.writer(fo, delimiter = "\t", quotechar = '"', quoting = csv.QUOTE_MINIMAL)

        writer.writerows([("Postal Code", "City", "Province")])

        for i in xrange(1, 10000):
            city = ""
            postal_code = "%04d" % (i)
            if (i >= 1 and i <= 299) or (i >= 1400 and i <= 2199):
                if i >= 2000 and i <= 2999:
                    city = "JOHANNESBURG"
                elif i >= 1 and i <= 299:
                    city = "PRETORIA"

                state = "GAUTENG"
            elif (i >= 300 and i <= 499) or (i >= 2500 and i <= 2899):
                state = "NORTH WEST"
            elif i >= 500 and i <= 999:
                state = "LIMPOPO"
            elif (i >= 1000 and i <= 1399) or (i >= 2200 and i <= 2499):
                state = "MPUMALANGA"
            elif i >= 2900 and i <= 4730:
                if i >= 3200 and i <= 3299:
                    city = "PIETERMARITZBURG"
                elif i >= 4000 and i <= 4099:
                    city = "DURBAN"
                elif i >= 4100 and i <= 4299:
                    city = "SOUTH COAST"
                elif i >= 4300 and i <= 4499:
                    city = "NORTH COAST"

                state = "KWAZULU NATAL"
            elif i >= 4731 and i<= 6499:
                if i >= 5200 and i <= 5299:
                    city = "EAST LONDON"
                elif i >= 6000 and i <= 6099:
                    city = "PORT ELIZABETH"

                state = "EASTERN CAPE"
            elif i >= 6500 and i <= 8099:
                if i >= 7700 and i<= 8099:
                    city = "CAPE TOWN"
                elif i >= 7300 and i <= 7399:
                    city = "WEST COAST"

                state = "WESTERN CAPE"
            elif i >= 8100 and i <= 8999:
                state = "NORTHERN CAPE"
            elif i >= 9300 and i <= 9999:
                if i >= 9300 and i <= 9399:
                    city = "BLOEMFONTEIN"
                state = "FREE STATE"
            
            writer.writerows([(postal_code, city, state)])


if __name__ == "__main__":

    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print "Usage: ./get_postal_codes.py <full path to output file>"
