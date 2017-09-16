# -*- coding: utf-8 -*-

import sys
import urllib, urllib2, ssl, re
import requests
import httplib
import urlparse
import re

UA = 'Mozilla/6.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.5) Gecko/2008092417 Firefox/3.0.3'

def cleanHTML(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

def unshorten_url(url):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    else:
        return url

def exists(url):
	r = requests.head(url)
	return r.status_code == requests.codes.ok

def postHTML(url, post_fields):

	if sys.hexversion >= 0x02070BF0:
		r = requests.post(url, data=post_fields)
		print(r.status_code, r.reason)
		html = r.text.encode('utf-8')
	else:
		print "Crap we have the old version"
		
		# hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		# 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		# 'Accept-Encoding': 'none',
		# 'Accept-Language': 'pl-PL,pl;q=0.8',
		# 'Connection': 'keep-alive'}
		
		# http://dev.morf.lv/mirror.php?url=https://cinemalive.tv/scripts/search.php&post=
		postParam = ""
		for key, value in post_fields.iteritems():
			postParam+=key+":"+value
			
		# req = urllib2.Request("http://dev.morf.lv/mirror.php?url="+url+"&post="+postParam, headers=hdr)
		
		# try:
			# page = urllib2.urlopen(req)
		# except urllib2.HTTPError, e:
			# print e.fp.read()
		
		# html = page.read()
		# print html
		
		r = requests.get("http://dev.morf.lv/mirror.php?url="+url+"&post="+postParam)
		print(r.status_code, r.reason)
		html = r.text.encode('utf-8')
		
	
	#Let's just itterate through stupid encoding/decodings
	try:
		html = html.decode('utf-8').encode('utf-8')
	except:		
		html = html.decode('latin-1').encode('utf-8')
		
	# test = html.encode('latin1').decode('utf8')
	# print test
	
	return html
	
def getHTML(url, data = False, limit = False):	   
	print "Downloading URL... [network.py]"
	
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'pl-PL,pl;q=0.8',
		'Connection': 'keep-alive'}
		

	if url.startswith("https://"):
		if sys.hexversion >= 0x02070BF0:
			print "Cool, we have TLSv1 Support"
			
			context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
			context.verify_mode = ssl.CERT_NONE
			context.check_hostname = False
		
			req = urllib2.Request(url, headers=hdr)

			try:
				page = urllib2.urlopen(req,context=context, timeout=5)
			except urllib2.HTTPError, e:
				print "ERROR while downloading: " + e.fp.read()

			# size = int(page.info().getheaders("Content-Length")[0])
			# print "PAGE SIZE: " + str(size)
			
			html = ""
			if limit != False:
				for x in range(limit):
					html += page.readline()
			else:
				html = page.read()
		else:
			print "Crap we have the old version"
			
			req = urllib2.Request("http://dev.morf.lv/mirror.php?url="+url, headers=hdr)
			
			try:
				page = urllib2.urlopen(req, timeout=5)
			except urllib2.HTTPError, e:
				print e.fp.read()

			# size = int(page.info().getheaders("Content-Length")[0])
			# print "PAGE SIZE: " + str(size)
			
			html = ""
			if limit != False:
				for x in range(limit):
					html += page.readline()
			else:
				html = page.read()
	else:
		print "Normal http download..."
		
		req = urllib2.Request(url, headers=hdr)

		
		try:
			page = urllib2.urlopen(req, timeout=5)
		except urllib2.HTTPError, e:
			print "ERROR while downloading: " + e.fp.read()
			return
		except urllib2.URLError, e:
			print "Couldn't resolve url: " + e.fp.read()
			return
		except:
			print "Misc error occured"
			return		
		# size = int(page.info().getheaders("Content-Length")[0])
		# print "PAGE SIZE: " + str(size)
		
		html = ""
		if limit != False:
			for x in range(limit):
				html += page.readline()
		else:
			html = page.read()
		# print "dickidy: " + url
		
	print "Length of the string: ", len(html)
	
	#Let's just itterate through stupid encoding/decodings
	try:
		html = html.decode('utf-8').encode('utf-8')
	except:		
		html = html.decode('latin-1').encode('utf-8')
	
	print "URL Downloaded"
	return html
	
def request(url, headers={}):
    print('request: %s' % url)
    req = urllib2.Request(url, headers=headers)
    req.add_header('User-Agent', UA)
    try:
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
    except urllib2.HTTPError, error:
        data=error.read() 
        error.close()
    print('len(data) %s' % len(data))
    return data


def post(url, data, headers={}):
    postdata = urllib.urlencode(data)
    req = urllib2.Request(url, postdata, headers)
    req.add_header('User-Agent', UA)
    try:
        response = urllib2.urlopen(req)
        data = response.read()
        response.close()
    except urllib2.HTTPError, error:
        data=error.read() 
        error.close()
    return data
	
def html_decode(s):
	"""
	Returns the ASCII decoded version of the given HTML string. This does
	NOT remove normal HTML tags like <p>.
	"""
	htmlCodes = (
			("'", '&#39;'),
			('"', '&quot;'),
			('>', '&gt;'),
			('<', '&lt;'),
			('&', '&amp;'),
			(' ', '&nbsp;')
		)
	for code in htmlCodes:
		s = s.replace(code[1], code[0])
	return s