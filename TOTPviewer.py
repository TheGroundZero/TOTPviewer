#!/usr/bin/env python3

################################################################################
##                                                                            ##
## TOTP Viewer                                                                ##
## Display credentials and TOTP tokens of multiple accounts                   ##
##                                                                            ##
## Credentials en TOTP secret are loaded from one or more CSV files           ##
##                                                                            ##
## (c) 2020 TheGroundZero / @DezeStijn                                        ##
##                                                                            ##
################################################################################


import pyotp
import argparse
import csv
import datetime
import os
import time
import sys
import curses


def main():
	parser = argparse.ArgumentParser(
		prog="TOTPcodes",
		description="Display TOTP tokens for multiple accounts",
	)
	parser.add_argument("-i", "--input", dest="input_files", help="Input CSV file(s) with TOTP tokens", required=True, nargs='+')

	args = parser.parse_args()

	show_tokens(args.input_files)


def show_tokens(input):
	try:
		curses.noecho()
		curses.cbreak()

		while(True):
			print_list(input)
			time.sleep(1)
	except KeyboardInterrupt:
		sys.exit(1)
	finally:
		curses.echo()
		curses.nocbreak()
		curses.endwin()


def print_list(input):
	line = 0

	for file in input:
		with open(file, 'r') as list:
			fieldnames = ['username', 'password', 'totp', 'timer']
			linereader = csv.DictReader(list, dialect='excel')

			line = print_header(line, fieldnames)

			for row in linereader:
				totp = pyotp.TOTP(row['totp'])
				line = print_row(line, row['username'], row['password'], totp.now(), calc_timer(totp))

	stdscr.refresh()


def calc_timer(totp):
	time_remaining = int(round(totp.interval - datetime.datetime.now().timestamp() % totp.interval))
	return time_remaining


def print_header(line, fieldnames):
	print_line(line)
	print_row(line+1, *fieldnames)
	print_line(line+2)
	return line+3


def print_row(line, uname, pw, totp, timer):
	stdscr.addstr(line, 0, "{:<25} | {:<33} | {:^8} | {:^5}".format(uname, pw, totp, timer))
	return line+1


def print_line(line):
	return print_row(line, "-"*25, "-"*33, "-"*8, "-"*5)


if __name__ == "__main__":
	stdscr = curses.initscr()
	main()
