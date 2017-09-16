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



def GetCategoryImage( str ):
	str = str.lower()
	
	str = str.replace(u'ē', 'e')
	str = str.replace(u'ŗ', 'r')
	str = str.replace(u'ū', 'u')
	str = str.replace(u'ī', 'i')
	str = str.replace(u'ō', 'o')
	str = str.replace(u'ā', 'a')
	str = str.replace(u'š', 's')
	str = str.replace(u'ģ', 'g')
	str = str.replace(u'ķ', 'k')
	str = str.replace(u'ļ', 'l')
	str = str.replace(u'ž', 'z')
	str = str.replace(u'č', 'c')
	str = str.replace(u'ņ', 'n')
	
	if str == 'animacija' or str == 'bernu filmas un multfilmas' or str == 'animacijas' or str == 'berniem':
		return '%s/categories/Animation.png'% iconpath
	elif str == 'asa sizeta' or str == 'spriedzes, asa sizeta filmas':
		return '%s/categories/Action.png'% iconpath
	elif str == 'biografija':
		return '%s/categories/Biography.png'% iconpath
	elif str == 'dokumentala' or str == 'dokumentalas filmas' or str == 'dokumentalas':
		return '%s/categories/Documentary.png'% iconpath
	elif str == 'drama' or str == 'dramas un biografiskas filmas' or str == 'dramas':
		return '%s/categories/Drama.png'% iconpath
	elif str == 'fantazija':
		return '%s/categories/Fantasy.png'% iconpath
	elif str == 'gimenes':
		return '%s/categories/Family.png'% iconpath
	elif str == 'komedija' or str == 'komedijas':
		return '%s/categories/Comedy.png'% iconpath
	elif str == 'muzikls' or str == 'muzikli':
		return '%s/categories/Musical.png'% iconpath
	elif str == 'piedzivojumu' or str == 'piedzivojumu un gimenes filmas':
		return '%s/categories/Adventure.png'% iconpath
	elif str == 'romantika' or str == 'romantiskas filmas' or str == 'romantiskas':
		return '%s/categories/Romance.png'% iconpath
	elif str == 'sausmu' or str == 'sausmu un mistikas filmas' or str == 'sausmenes':
		return '%s/categories/Horror.png'% iconpath
	elif str == 'trilleris' or str == 'trilleri':
		return '%s/categories/Thriller.png'% iconpath
	elif str == 'fantastika' or str == 'zinatniska fantastika' or str == 'fantastikas':
		return '%s/categories/Sci-fi.png'% iconpath
	elif str == 'sporta':
		return '%s/categories/Sport.png'% iconpath
	elif str == 'kara':
		return '%s/categories/War.png'% iconpath
	elif str == 'vesturiska' or str == 'vesturiskas':
		return '%s/categories/History.png'% iconpath
	elif str == 'westerns' or str == 'vesterns':
		return '%s/categories/Western.png'% iconpath
	elif str == 'jaunakas':
		return '%s/new.png'% iconpath
	elif str == 'vertetakas':
		return '%s/star.png'% iconpath
	elif str == 'skatitakas':
		return '%s/movie-2.png'% iconpath
	elif str == 'mistika' or str == 'misterija':
		return '%s/categories/Mystery.png'% iconpath
	elif str == 'filmas krievu valoda' or str == 'krieviski':
		return '%s/categories/russian.png'% iconpath
	elif str == 'latviesu filmas':
		return '%s/categories/latvia.png'% iconpath
	elif str == 'detektivs':
		return '%s/categories/detective.png'% iconpath
	elif str == 'ziemassvetku':
		return '%s/categories/christmas.png'% iconpath
	
	
	return '%s/categories/Others.png'% iconpath

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
    if "?" not in needle:
        return False
        
    needle = needle.split("?")[0]
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
	
def MakeSearchableString(str):
	str = str.lower()
	
	str = str.replace(u'ē', 'e')
	str = str.replace(u'ŗ', 'r')
	str = str.replace(u'ū', 'u')
	str = str.replace(u'ī', 'i')
	str = str.replace(u'ō', 'o')
	str = str.replace(u'ā', 'a')
	str = str.replace(u'š', 's')
	str = str.replace(u'ģ', 'g')
	str = str.replace(u'ķ', 'k')
	str = str.replace(u'ļ', 'l')
	str = str.replace(u'ž', 'z')
	str = str.replace(u'č', 'c')
	str = str.replace(u'ņ', 'n')
	
	# print str
	return str