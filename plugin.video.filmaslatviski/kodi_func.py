# -*- coding: utf-8 -*-

import sys
import os
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import urllib

mysettings = xbmcaddon.Addon(id = 'plugin.video.filmaslatviski')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
getSetting = xbmcaddon.Addon().getSetting
iconpath = xbmc.translatePath(os.path.join(home, 'resources/icons/'))


def showkeyboard(txtMessage="",txtHeader="",passwordField=False):
    if txtMessage=='None': txtMessage=''
    keyboard = xbmc.Keyboard(txtMessage, txtHeader, passwordField)#("text to show","header text", True="password field"/False="show text")
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()
    else:
		return False
		
def isLinkUseful(needle):
    haystack = ['/index.php', '#']
    return needle not in haystack
	
def isVideoFormat(needle):
    haystack = ['mp4', 'avi', 'mp4?mime=true', 'm3u8', 'mov']
    return needle in haystack
	
def addDir(title, url, mode, picture, page=None, source_id=None):
    sys_url = sys.argv[0] + '?title=' + urllib.quote_plus(title) + '&url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode)) + '&source_id=' + urllib.quote_plus(str(source_id))
    if  picture == None:
        item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage='')
    else:
        item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png' , thumbnailImage=picture)    
        sys_url += '&picture=' + urllib.quote_plus(str(picture))
    if page != None:
        sys_url += '&page=' + urllib.quote_plus(str(page))
    item.setInfo(type='Video', infoLabels={'Title': title})

    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys_url, listitem=item, isFolder=True)
	
def addLink(title, url, picture):
	# if url.startswith('plugin://') == True:
		# url = 'PlayMedia('+url+')'

	# print url

	if  picture == None:
		item = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage='')
	else:
		item = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage=picture)
	item.setInfo( type='Video', infoLabels={'Title': title} )		
	if url.startswith('plugin://') == True:
		item.setProperty('IsPlayable', 'true')
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=item)