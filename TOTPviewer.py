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
import signal
import sys


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
		while(True):
			clear_screen()
			print_list(input)
			time.sleep(1)
	except KeyboardInterrupt:
		sys.exit(1)


def print_list(input):
	for file in input:
		with open(file, 'r') as list:
			fieldnames = ['username', 'password', 'totp', 'timer']
			linereader = csv.DictReader(list, dialect='excel')

			print_line()
			print_row(*fieldnames)
			print_line()

			for row in linereader:
				totp = pyotp.TOTP(row['totp'])
				print_row(row['username'], row['password'], totp.now(), calc_timer(totp))


def clear_screen():
	os.system('cls' if os.name=='nt' else 'clear')


def calc_timer(totp):
	time_remaining = int(round(totp.interval - datetime.datetime.now().timestamp() % totp.interval))
	return time_remaining


def print_row(uname, pw, totp, timer):
	print("{:<25} | {:<33} | {:^8} | {:^5}".format(uname, pw, totp, timer))


def print_line():
	print_row("-"*25, "-"*33, "-"*8, "-"*5)


def exit_gracefully(signum, frame):
	signal.signal(signal.SIGINT, original_sigint)
	keep_running = False


if __name__ == "__main__":
	main()
