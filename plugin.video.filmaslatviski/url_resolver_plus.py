# -*- coding: utf-8 -*-
import network
import sys
import xbmc
import xbmcgui
import xbmcplugin
import urlresolver
import CommonFunctions
import kodi_func
import js2py
import re

common = CommonFunctions
common.plugin = "Filmas-Latviski-1.0.0"

def resolve(url):
	link = urlresolver.resolve(url)
	if link == False or link == "":
		if url.startswith("https://cloudsany.com"):
			print "CloudsAny detected..."
			html = network.getHTML(url)
			playerCode = common.parseDOM(html, "div", attrs = {"id": "player_code"})
			scripts = common.parseDOM(playerCode, "script")
			js = scripts[-1]
			
			js = js.replace("eval", "fnRes=")
			print "return" in js
			js = str(js2py.eval_js(js))
			print "Decoded js", js
			
			searchObj = re.search("file:\"[\'\w\d:\/.?=]*\"", js)
			if searchObj:
				resolvedUrl = searchObj.group().replace("file:\"", "")
				resolvedUrl = resolvedUrl[:-1]
				print "Decoded URL", resolvedUrl
				return resolvedUrl
			else:
				return False
			
			
	return link