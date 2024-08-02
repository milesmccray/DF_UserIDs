from bs4 import BeautifulSoup
import requests
import json
import re
from datetime import date


def create_JSON():
	today = str(date.today())
	"""Parses dustkid/rankings html and creates JSON of User:ID"""
	request = requests.get('https://dustkid.com/rankings/all')
	html = BeautifulSoup(request.content, 'html.parser')

	user_name = {}
	user_ids = {}
	pattern = 'profile\/([0-9]+)\/.*>(.*)<'  # Regex pattern

	# Grabs the levels the 6th <p> tag (Overall User List) and then grabs all the associated <a> tags
	user_data = (html.find_all('p')[5]).find_all('a')
	for user_string in user_data:
		try:
			user_id = re.search(pattern, str(user_string)).group(1)
			user_name = re.search(pattern, str(user_string)).group(2)
			user_ids[user_id] = user_name
		except AttributeError:  # Incase it fails, skip
			continue

	# Adds creation date to json
	fmt_user_ids = {'Date': today, 'Users': user_ids}

	# Writes fmt_user_ids to a json file in same directory
	with open('dk_users.json', 'w') as f:
		json.dump(fmt_user_ids, f, indent=4, ensure_ascii=False)


create_JSON()
