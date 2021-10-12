import os
from shutil import copy2
import platform
import re
from os.path import isfile
from datetime import datetime
import sys

from tqdm import tqdm

USE_YEAR_ONLY = True

def log_problems(problems):
	if len(problems) > 0:
		f = open("problems.log", "w")
		f.write(str(problems))
		f.close()

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() != 'Windows':
        return os.path.getctime(path_to_file)
    else:
        stat = os.stat(path_to_file)
        try:
            return stat.st_birthtime
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return stat.st_mtime

def get_file_list():
	files = []
	skip_list = ['problems.log', os.path.basename(__file__)]
	for f in os.listdir():
		if f in skip_list:
			continue
		if f[0] == '.':
			continue
		if os.path.isdir(f):
			continue
		files.append(f)
	return files

print(os.path.basename(__file__))

def sort_by_name():
	problems = []
	for f in tqdm(get_file_list()):
		result = re.search(r'[0-9]{8}', f)
		if result:
			res = result.group(0)
			my_date = res[0:4]

			if not USE_YEAR_ONLY:
				my_date += '/' + res[4:6]

			os.makedirs(my_date, exist_ok=True)
			if os.path.isfile(f):
				try:
					copy2(f, my_date + '/' + f)
				except:
					problems.append(f)
		else:
			print(f'Cant sort: {f}')
			problems.append(f)

	log_problems(problems)


def sort_by_created():
	problems = []
	for f in tqdm(get_file_list()):
		date_cr = datetime.utcfromtimestamp(creation_date(f))

		folder_format = '%Y'
		if not USE_YEAR_ONLY:
			folder_format += '/%m'

		my_date = datetime.strftime(date_cr, folder_format)
		os.makedirs(my_date, exist_ok=True)
		if os.path.isfile(f):
			try:
				copy2(f, my_date + '/' + f)
			except:
				print(f'Cant sort: {f}')
				problems.append(f)

	log_problems(problems)

def print_usage():
	print('Usage: py sort.py [name|created]')

print(sys.argv[0] )

if len(sys.argv) < 2:
	print_usage()
else:
	action_type = sys.argv[1]
	if action_type not in ['name', 'created']:
		print_usage()
	else:
		if action_type == 'name':
			sort_by_name()
		if action_type == 'created':
			sort_by_created()
