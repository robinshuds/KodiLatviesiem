# -*- coding: utf-8 -*-

import sys
import os
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import pyxbmct
import network
import CommonFunctions
import time
from datetime import date
import datetime
import random

common = CommonFunctions
common.plugin = "dzivaistv"

loadingMessages = [
	"rūķīši smagi pūš un tik strādā",
	"biti vairojas",
	"mēs būvējam cik ātri varam",
	"nepievērs uzmanību vīrietim kas slēpjas aiz aizskariem",
	"kamēr es tevi vēroju",
	"daži biti aizmuka, bet mēs viņus noķērām",
	"un pasapņo par ātrāku internetu",
	"aiziet, aizturi elpu",
	"un skaļi padungo, kamēr citi skatās",
	"kamēr mēs pārbaudam tavu pacietību",
	"it kā tev būtu izvēle",
	"tikmēr, vai varu ieintersēt jūs ar jaunu putekļusūcēju?",
	"ĀTRI NEDOMĀ, par rozā ziloņiem!",
	"kamēr pieslēdzamies satalītiem",
	"biti šodien lēni plūst pa tranzistoriem",
	"kamēr mēs nolasam tavu kredītkarti",
	"kamēr mēs nozogam jūsu personas datus",
	"vai esam jau klāt?",
	"lai turpinātu, sakiet skaļi \"Sākt\"",
	"mirklīti, tam ir jābūt kaut kur te pat",
	"kamēr ielādēju strīmu... April April",
	"un dievadēļ neskaties kas tev ir aizmuguras",
	"kamēr daru kaut ko svarīgu",
	"vai esi gatavs?",
	"KLUSUMU! Es mēģinu šeit domāt...",
	"Jūsu laiks mums ir svarīgs",
	"kamēr ceļojat laikā ik pa sekundei",
	"kamēr sazinos ar pirātisma apkarošanas dienastu"
]

# Create a class for our UI
class MyAddon(pyxbmct.AddonDialogWindow):

	def __init__(self, title='', now_playing = '', program_today = [], program_tomorrow = [], program_aftertomorrow = [], program_afteraftertomorrow = []):
		"""Class constructor"""
		# Call the base class' constructor.
		super(MyAddon, self).__init__(title)
		
		# save programs
		self.now_playing = now_playing
		self.program_today = program_today
		self.program_tomorrow = program_tomorrow
		self.program_aftertomorrow = program_aftertomorrow
		self.program_afteraftertomorrow = program_afteraftertomorrow
		
		# Set width, height and the grid parameters
		self.setGeometry(800, 600, 11, 4)
		# Call set controls method
		self.set_controls()
		# Call set navigation method.
		self.set_navigation()
		# Connect Backspace button to close our addon.
		self.connect(pyxbmct.ACTION_NAV_BACK, self.close)

	def set_controls(self):
		"""Set up UI controls"""
		# Image control
		# image = pyxbmct.Image('https://peach.blender.org/wp-content/uploads/poster_rodents_small.jpg?3016dc')
		# self.placeControl(image, 0, 0, rowspan=3, columnspan=2)
		
		# Today button
		self.today_button = pyxbmct.Button('Šodien')
		self.placeControl(self.today_button, 0, 0)
		self.connect(self.today_button, self.set_guide_today)
		# Today button
		self.tomorrow_button = pyxbmct.Button('Rīt')
		self.placeControl(self.tomorrow_button, 0, 1)
		self.connect(self.tomorrow_button, self.set_guide_tomorrow)
		# Today button
		self.aftertomorrow_button = pyxbmct.Button('Parīt')
		self.placeControl(self.aftertomorrow_button, 0, 2)
		self.connect(self.aftertomorrow_button, self.set_guide_aftertomorrow)
		# Today button
		self.afteraftertomorrow_button = pyxbmct.Button('Aizparīt')
		self.placeControl(self.afteraftertomorrow_button, 0, 3)
		self.connect(self.afteraftertomorrow_button, self.set_guide_afteraftertomorrow)
		
		# Now Label
		self.program_name_label = pyxbmct.Label('Šodienas Programma')
		self.placeControl(self.program_name_label, 1, 0, 1,4)		
		
		self.now_label = pyxbmct.FadeLabel()
		self.placeControl(self.now_label, 2, 0, 1,4)
		self.now_label.addLabel('Šobrīd rāda:   ' + self.now_playing )
		
		
		# List
		self.list = pyxbmct.List()
		self.placeControl(self.list, 3, 0, rowspan=7, columnspan=4)
		# Add items to the list
		# items = ['Item {0}'.format(i) for i in range(1, 8)]
		
		
			
		# print self.program_today
		
		self.list.addItems(self.program_today )
		
		# Text label
		# label = pyxbmct.Label('Your name:')
		# self.placeControl(label, 8, 0)
		
		# Close button
		self.close_button = pyxbmct.Button('Aizvērt')
		self.placeControl(self.close_button, 10, 0)
		# Connect close button
		self.connect(self.close_button, self.close)
		
		# Connect Hello button.
		# self.connect(self.hello_buton, lambda:
			# xbmc.executebuiltin('Notification(Hello {0}!, Welcome to PyXBMCt.)'.format(
				# self.name_field.getText())))
	def set_guide_today(self):
		self.set_guide(0)
		
	def set_guide_tomorrow(self):
		self.set_guide(1)
		
	def set_guide_aftertomorrow(self):
		self.set_guide(2)
	
	def set_guide_afteraftertomorrow(self):
		self.set_guide(3)
		
	def set_guide(self, day):
		self.list.reset()
		if day == 1:
			program_items = self.program_tomorrow
			
			self.today_button.setLabel('Šodien', 'font14', '0xFFFFFFFF', '0xFFFF3300')
			self.tomorrow_button.setLabel('Rīt', 'font14', '0xFF7CFC00', '0xFFFF3300')
			self.aftertomorrow_button.setLabel('Parīt', 'font14', '0xFFFFFFFF', '0xFFFF3300')
			self.afteraftertomorrow_button.setLabel('Aizparīt', 'font14', '0xFFFFFFFF', '0xFFFF3300')
			
			self.program_name_label.setLabel('Rītdienas Programma')
		elif day == 2:
			program_items = self.program_aftertomorrow
			
			self.today_button.setLabel('Šodien', 'font14', '0xFFFFFFFF', '0xFFFF3300')
			self.tomorrow_button.setLabel('Rīt', 'font14', '0xFFFFFFFF', '0xFFFF3300')
			self.aftertomorrow_button.setLabel('Parīt', 'font14', '0xFF7CFC00', '0xFFFF3300')
			self.afteraftertomorrow_button.setLabel('Aizparīt', 'font14', '0xFFFFFFFF', '0xFFFF3300')
			
			self.program_name_label.setLabel('Parītdienas Programma')
		elif day == 3:
			program_items = self.program_afteraftertomorrow
			
			self.today_button.setLabel('Šodien', 'font14', '0xFFFFFFFF', '0xFFFF3300')
			self.tomorrow_button.setLabel('Rīt', 'font14', '0xFFFFFFFF', '0xFFFF3300')
			self.aftertomorrow_button.setLabel('Parīt', 'font14', '0xFFFFFFFF', '0xFFFF3300')
			self.afteraftertomorrow_button.setLabel('Aizparīt', 'font14', '0xFF7CFC00', '0xFFFF3300')
			
			self.program_name_label.setLabel('Aizparītdienas Programma')
		else:
			program_items = self.program_today
			
			self.today_button.setLabel('Šodien', 'font14', '0xFF7CFC00', '0xFFFF3300')
			self.tomorrow_button.setLabel('Rīt', 'font14', '0xFFFFFFFF', '0xFFFF3300')
			self.aftertomorrow_button.setLabel('Parīt', 'font14', '0xFFFFFFFF', '0xFFFF3300')
			self.afteraftertomorrow_button.setLabel('Aizparīt', 'font14', '0xFFFFFFFF', '0xFFFF3300')
			
			self.program_name_label.setLabel('Šodienas Programma')
			
		self.list.addItems( program_items )
			

	def set_navigation(self):
		"""Set up keyboard/remote navigation between controls."""
		# self.name_field.controlUp(self.hello_buton)
		# self.name_field.controlDown(self.hello_buton)
		# self.close_button.controlLeft(self.hello_buton)
		# self.close_button.controlRight(self.hello_buton)
		# self.hello_buton.setNavigation(self.name_field, self.name_field, self.close_button, self.close_button)
		# Set initial focus.
		# self.setFocus(self.name_field)
		self.today_button.setNavigation(self.close_button, self.list, self.afteraftertomorrow_button, self.tomorrow_button)
		self.tomorrow_button.setNavigation(self.close_button, self.list, self.today_button, self.aftertomorrow_button)
		self.aftertomorrow_button.setNavigation(self.close_button, self.list, self.tomorrow_button, self.afteraftertomorrow_button)
		self.afteraftertomorrow_button.setNavigation(self.close_button, self.list, self.aftertomorrow_button, self.today_button)
		self.list.controlUp( self.today_button )
		self.list.controlDown( self.close_button )
		self.close_button.controlUp(self.list)
		self.close_button.controlDown(self.today_button)
		self.setFocus(self.today_button)
		
		self.today_button.setLabel('Šodien', 'font14', '0xFF7CFC00', '0xFFFF3300', '0xFF000000')
		# self.today_button.setEnabled(False)


class GuideData(object):
	def __init__(self, playing_now, program_today, program_tomorrow, program_aftertomorrow, program_afteraftertomorrow):
		self.playing_now = playing_now
		self.program_today = program_today
		self.program_tomorrow = program_tomorrow
		self.program_aftertomorrow = program_aftertomorrow
		self.program_afteraftertomorrow = program_afteraftertomorrow
		
def parse_lattelecom_guide(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('Lejupielādēju tv programmu', 'Lūdzu uzgaidi...', random.choice(loadingMessages))
	
	def parseDay(url):
		print "GUIDE URL: ", url
		html = network.getHTML( url )		
		
		program_list_ul = common.parseDOM(html, "ul", attrs = { "id": "program-list-view" })
		
		program_entry = common.parseDOM(program_list_ul, "li")
		program_items = []
		for pEntry in program_entry:
			time = common.parseDOM(pEntry, "b")[0]
			title = common.parseDOM(pEntry, "a")[0]
			program_items.append( time + " - " + title )
		return program_items
			
			
	html = network.getHTML( url )
	# print "GUIDE HTML: ", html
	
	program_list_ul = common.parseDOM(html, "ul", attrs = { "id": "program-list-view" })
	program_entry_now = common.parseDOM(program_list_ul, "li", attrs = { "class": "entry current expandable with-description"} )
	playing_now = ''
	if len(program_entry_now) == 0:
		program_entry_now = common.parseDOM(program_list_ul, "li", attrs = { "class": "entry current expandable without-description"} )
	
	if len(program_entry_now) > 0:
		time = common.parseDOM(program_entry_now, "b")[0].encode('utf-8')
		title = common.parseDOM(program_entry_now, "a")[0].encode('utf-8')
		playing_now = time + " - " + title		
	print "now playing: ", playing_now
	
	today = date.today()	
	pDialog.update( 25 )
	program_today = parseDay(url+today.strftime('%d.%m.%Y'))
	pDialog.update( 50 )
	program_tomorrow = parseDay(url+ (today + datetime.timedelta(days=1)).strftime('%d.%m.%Y')) 
	pDialog.update( 75 )
	program_aftertomorrow = parseDay(url+ (today + datetime.timedelta(days=2)).strftime('%d.%m.%Y')) 
	pDialog.update( 100 )
	program_afteraftertomorrow = parseDay(url+ (today + datetime.timedelta(days=3)).strftime('%d.%m.%Y')) 
	
	
	return GuideData(playing_now, program_today, program_tomorrow, program_aftertomorrow, program_afteraftertomorrow)
	
def parse_seetv_guide(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('Lejupielādēju tv programmu', 'Lūdzu uzgaidi...', random.choice(loadingMessages))
	
	html = network.getHTML( url )
	
	teleprogrammaDiv = common.parseDOM(html, "div", attrs = { "class": "teleprograma " })
	print "Teleprogramma div", teleprogrammaDiv
	
	program_entry_now = common.parseDOM(teleprogrammaDiv, "div", attrs = {"class": "row hover_teleprograma bold_tv"} )
	playing_now = ''
	if len(program_entry_now) == 0:
		program_entry_now = common.parseDOM(program_list_ul, "li", attrs = { "class": "entry current expandable without-description"} )
		
	if len(program_entry_now) > 0:
		spanEntry = common.parseDOM( program_entry_now[0], "span" )
		time = common.parseDOM( spanEntry, "span" )[0]
		title = network.cleanHTML( spanEntry[0] ).strip().replace("\n","").replace("\r", "").replace(time+" ", "")		
		playing_now = time + " - " + title	
		playing_now = playing_now.encode('utf-8')
	print "now playing: ", playing_now
	
	def parseDay(teleprogrammaDiv, day):		
		
		print "Downloading day: ", day
		
		program_list_div = common.parseDOM(teleprogrammaDiv, "div", attrs = { "rel": str(day) })
		
		# program_entry = common.parseDOM(program_list_div, "div", attrs = {"class": "row hover_teleprograma "} )
		program_entry_cols = common.parseDOM(program_list_div, "div", attrs = {"class": "col-lg-6 col-md-6 col-sm-12 col-xs-12 col-uxs-12 col-u2xs-12"} )
		program_entry = common.parseDOM(program_entry_cols, "div")
		program_items = []
		for pEntry in program_entry:
			spanEntry = common.parseDOM( pEntry, "span" )
			# print "spanEntrie: ", len(spanEntry), common.parseDOM( spanEntry, "span" )
			time = common.parseDOM( spanEntry, "span" )[0]
			title = network.cleanHTML( spanEntry[0] ).strip().replace("\n","").replace("\r", "").replace(time+" ", "")			
			program_items.append( time + " - " + title )
		return program_items
	
	today = date.today()	
	pDialog.update( 25 )
	program_today = parseDay(teleprogrammaDiv, today.weekday()+1 )
	pDialog.update( 50 )
	# print (today + datetime.timedelta(days=1)).weekday()+1
	program_tomorrow = parseDay(teleprogrammaDiv, (today + datetime.timedelta(days=1)).weekday()+1 )
	pDialog.update( 75 )
	program_aftertomorrow = parseDay(teleprogrammaDiv, (today + datetime.timedelta(days=2)).weekday()+1 )
	pDialog.update( 100 )
	program_afteraftertomorrow = parseDay(teleprogrammaDiv, (today + datetime.timedelta(days=3)).weekday()+1 )
	
	return GuideData(playing_now, program_today, program_tomorrow, program_aftertomorrow, program_afteraftertomorrow)
	
def parse_tivix_guide(url):
	pDialog = xbmcgui.DialogProgress()
	pDialog.create('Lejupielādēju tv programmu', 'Lūdzu uzgaidi...', random.choice(loadingMessages))
	
	html = network.getHTML( url )
	html = html.replace("tabs__content active", "tabs__content")
	
	
	tabsContent = common.parseDOM(html, "div", attrs = { "class": "tabs__content" })
	print "tabsContent div", tabsContent, len(tabsContent)
	
	# program_entry_now = common.parseDOM(html, "div", attrs = {"class": "tabs__content active"} )	
	# playing_now = ''
	# if len(program_entry_now) > 0:
		# spanEntry = common.parseDOM( program_entry_now[0], "span" )
		# time = common.parseDOM( spanEntry, "span" )[0]
		# title = network.cleanHTML( spanEntry[0] ).strip().replace("\n","").replace("\r", "").replace(time+" ", "")		
		# playing_now = time + " - " + title	
		# playing_now = playing_now.encode('utf-8')
	# print "now playing: ", playing_now
	
	def parseDay(tabsContent, day):		
		
		print "Parsing day: ", day
		
		program_list_div = common.parseDOM(tabsContent[day], "div")
		print "program_list_div", program_list_div
		# program_entry = common.parseDOM(program_list_div, "div", attrs = {"class": "row hover_teleprograma "} )
		program_items = []
		time = None
		title = None
		for pEntry in program_list_div:
			if len(pEntry) == 0:
				continue
				
			if time == None:				
				time = pEntry
				continue
			elif title == None:				
				title = network.html_decode( network.cleanHTML( pEntry ) )
				program_items.append( time + " - " + title )
				time = None
				title = None
		return program_items
	
	today = date.today()	
	pDialog.update( 25 )
	program_today = parseDay(tabsContent, today.weekday() )
	playing_now = ''
	# currTime =  time.strftime('%H:%M')
	currTime = network.getHTML( "http://dev.morf.lv/timezone.php" ) #shitty python doesn't have timezone library by default
	for row in program_today:
		pTime = row[:5]
		print pTime + " <= " + currTime
		if pTime <= currTime:			
			playing_now = row.encode('utf-8')
		else:
			break		
	
	pDialog.update( 50 )
	program_tomorrow = parseDay(tabsContent, (today + datetime.timedelta(days=1)).weekday() )
	pDialog.update( 75 )
	program_aftertomorrow = parseDay(tabsContent, (today + datetime.timedelta(days=2)).weekday() )
	pDialog.update( 100 )
	program_afteraftertomorrow = parseDay(tabsContent, (today + datetime.timedelta(days=3)).weekday() )
	
	return GuideData(playing_now, program_today, program_tomorrow, program_aftertomorrow, program_afteraftertomorrow)

if __name__ == '__main__':
	print 'Number of arguments:', len(sys.argv), 'arguments.'
	print 'Argument List:', str(sys.argv)
	
	guideData = None
	
	url = sys.argv[2]
	if url.startswith("https://tv.lattelecom.lv"):
		guideData = parse_lattelecom_guide( url )
	elif url.startswith("http://seetv.tv"):
		guideData = parse_seetv_guide( url )
	elif url.startswith("http://tivix.co"):
		guideData = parse_tivix_guide( url )
	else:
		xbmcgui.Dialog().ok( "Kļūda", "Tika padota tv programma no nezināma avota", "Neēsmu nekāds burvjumākslinieks" )
	
	if guideData != None:
		myaddon = MyAddon(sys.argv[1] + ' - TV Programma', guideData.playing_now, guideData.program_today, guideData.program_tomorrow, guideData.program_aftertomorrow, guideData.program_afteraftertomorrow )
		myaddon.doModal()
		del myaddon