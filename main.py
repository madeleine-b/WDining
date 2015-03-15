import os
import requests
import logging
import string
import re

import jinja2
import webapp2
import datetime

from bs4 import BeautifulSoup

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)

class MainPage(webapp2.RequestHandler):

    def get(self):

        template = JINJA_ENVIRONMENT.get_template('index.html')

        menus = menuUrls()

		lulu = requests.get(menus[0])
		bates = requests.get(menus[1])
		pom = requests.get(menus[2])
		stone = requests.get(menus[3])
		tower = requests.get(menus[4])

		lulu_soup = BeautifulSoup(lulu.text).div
		bates_soup = BeautifulSoup(bates.text).div
		pom_soup = BeautifulSoup(pom.text).div
		stone_soup = BeautifulSoup(stone.text).div
		tower_soup = BeautifulSoup(tower.text).div

		lulu_items = []
		bates_items = []
		pom_items = []
		stone_items = []
		tower_items = []

		for node in lulu_soup.findAll('p'):
			lulu_items.append(''.join(node.findAll(text=True)).encode('utf-8'))
		for node in bates_soup.findAll('p'):
			bates_items.append(''.join(node.findAll(text=True)).encode('utf-8'))
		for node in pom_soup.findAll('p'):
			pom_items.append(''.join(node.findAll(text=True)).encode('utf-8'))
		for node in stone_soup.findAll('p'):
			stone_items.append(''.join(node.findAll(text=True)).encode('utf-8'))
		for node in tower_soup.findAll('p'):
			tower_items.append(''.join(node.findAll(text=True)).encode('utf-8'))

		lulu_items = cleanList(lulu_items)
		bates_items = cleanList(bates_items)
		pom_items = cleanList(pom_items)
		stone_items = cleanList(stone_items)
		tower_items = cleanList(tower_items)

        template_values = {}
        self.response.write(template.render(template_values))

    def menuUrls():
		now = datetime.datetime.now()

		dd = "%d" % (now.day)
		mm = "%d" % (now.month)

		if len(dd) < 2:
			dd = "0"+dd
		if len(mm) < 2:
			mm = "0"+mm

		menus = ['menus/bplc/menu_'+mm+dd+'.htm','menus/bates/menu_'+mm+dd+'.htm','menus/pomeroy/menu_'+mm+dd+'.htm']
		menus.append('menus/stonedavis/menu_'+mm+dd+'.htm')
		menus.append('menus/tower/menu_'+mm+dd+'.htm')

		for i in range(len(menus)):
			menus[i] = "http://www.wellesleyfresh.com/"+menus[i]
		return menus

	def cleanList(items):
		keywords = [" if ", "Offered Daily:", "Offered", "Offered daily", "Offered daily:", "Home-style Dinner", "Homestyle Lunch", "Homestyle lunch", "Homestyle Dinner", "Homestyle dinner", "Late Night", "Late Nite", "Late night", "Hot Bar", "hot bar", "Hot bar", "Home-style Lunch", "!supportLineBreakNewLine", "endif", "Continental", "Pizza/Pasta", "Pizza/pasta", "breakfast", "Served", "Brunch", "Dinner", "Daily", "daily", "Lunch", "Breakfast", "served", "continental", "brunch", "lunch", "dinner", "grill", "fusion", "daily", "continental breakfast", "soup", "pizza", "homestyle", "home-style", "home", "style"]
		alphabet = []
		for p in range(len(string.ascii_letters)):
			alphabet.append(string.ascii_letters[p])

		temp = []

		for i in items:
			i = i.replace(b'\r\n', ' ').replace(b'\xc2\xa0', ' ').replace(b'\xe2\x80\x99', '\'').replace(b'\xc2\x92', '\'')
			i = re.sub("[\(\[].*?[\)\]]", "", i) #removes stuff between parentheses and brackets
			i = ' '.join(i.split()) #removes more than one space between words
			i = i.replace(" and", ',').replace(b'\x2D', '').replace("or ", ',') #sometimes the and-replacement is tricky

			for k in keywords:
				i = i.replace(k, '')
			
			i = i.strip()

			pos_list = i.split(",")
			for p in pos_list:
				p = p.strip()
				if p.lower() not in keywords and len(p)>1 and p[0] in alphabet:
					temp.append(p) 

			pos_list = i.split(";")
			if len(pos_list) > 1:
				temp.pop() #means we found a list separated by semi-colons and don't want the original list to be added as one item
				for p in pos_list:
					p = p.strip()
					if p not in temp and p.lower() not in keywords and len(p)>1 and p[0] in alphabet:
						temp.append(p) 

		return temp

application = webapp2.WSGIApplication([
    ('/', MainPage)
], debug=True)