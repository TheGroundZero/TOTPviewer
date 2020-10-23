#!/usr/bin/env python3

################################################################################
##                                                                            ##
## TOTP Viewer                                                                ##
## Display credentials and TOTP tokens of one ore more accounts               ##
##                                                                            ##
## Credentials en TOTP secret are loaded from one or more CSV files           ##
##   or processed from parameters                                             ##
##                                                                            ##
## (c) 2020 TheGroundZero / @DezeStijn                                        ##
##                                                                            ##
################################################################################


import argparse
import csv
import curses
import datetime
import pyotp
import sys
import time


stdscr = None


def main():
	parser = argparse.ArgumentParser(
		prog="TOTPcodes",
		description="Display TOTP tokens for multiple accounts",
	)
	subparsers = parser.add_subparsers(help="sub-command help")

	parser_files = subparsers.add_parser("files", help="files help")
	parser_files.add_argument("-i", "--input", dest="input_files", help="Input CSV file(s) with TOTP tokens", required=True, nargs='+')
	parser_files.set_defaults(func=do_files)

	parser_single = subparsers.add_parser("single", help="single help")
	parser_single.add_argument("-u", "--user", dest="user", help="Username", required=False, default="", nargs='?')
	parser_single.add_argument("-p", "--pass", dest="password", help="Password", required=False, default="", nargs='?')
	parser_single.add_argument("-t", "--totp", dest="totp", help="TOTP", required=True, default="", nargs='?')
	parser_single.set_defaults(func=do_single)

	parser_show = subparsers.add_parser("show", help="show help")
	parser_show.add_argument("-t", "--totp", dest="totp", help="TOTP", required=True, default="", nargs='?')
	parser_show.set_defaults(func=do_show)

	args = parser.parse_args()
	args.func(args)


def do_files(args):
	data = parse_files(args.input_files)
	show_tokens(data)


def do_single(args):
	data = parse_params(args.user, args.password, args.totp)
	show_tokens(data)


def do_show(args):
	totp = calc_totp(args.totp)
	print("{}".format(totp))
	return totp


def parse_files(files):
	output = []
	for file in files:
		with open(file, 'r') as csvfile:
			reader = csv.DictReader(csvfile, dialect='excel')
			data = list(reader)
			output.append(data)
	return output


def parse_params(uname, pw, totp):
	return [[{'username':uname, 'password':pw, 'totp':totp}]]


def show_tokens(input):
	try:
		global stdscr
		stdscr = curses.initscr()
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


def print_list(data):
	line = 0

	for file in data:
		fieldnames = ['username', 'password', 'totp', 'timer']
		line = print_header(line, fieldnames)

		for row in file:
			line = print_row(line, row['username'], row['password'], calc_totp(row['totp']), calc_timer(row['totp']))

	stdscr.refresh()


def calc_totp(key):
	totp = pyotp.TOTP(key)
	return totp.now()


def calc_timer(key):
	totp = pyotp.TOTP(key)
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
	main()
