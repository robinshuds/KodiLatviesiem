# -*- coding: utf-8 -*-

import sys
import os
import re
import js2py
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
# import urlresolver
import urllib, urllib2, ssl, re
import CommonFunctions
import requests
import json
from urlparse import urlparse
import hashlib
import random
import pyxbmct
import network

channelList = {'Latvijas Kanāli': {
									'icon': '%s/Latvia.png',
									'channels':	[{'name': 'LTV1',
												'thumb': '%s/ltv1.png',
												'guide': 'https://tv.lattelecom.lv/lv/programma/interaktiva/list/ltv1/',
												'sources': [
															#{'name':'LTV1 - Tiešraide 1 [COLOR yellow][Ārzemes Neies][/COLOR][COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'resolve_ltv1_source1'},
															#{'name':'LTV1 - Tiešraide 2 [COLOR yellow][Ārzemes Neies][/COLOR][COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://dvb.gpsystems.lv:4242/bynumber/1?by_HasBahCa'},
															#{'name':'LTV1 - Tiešraide 3 [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://80.70.22.46/LTV1/playlist.m3u8', 'key': 0},
															#{'name':'LTV1 - Tiešraide 4 [COLOR yellow][Iet Tikai Ārzemēs][/COLOR]', 'url': 'http://89.201.43.188/play.php?freq=140.25', 'key': 2},
															#{'name':'LTV1 - Tiešraide 5 ', 'url': 'http://ts.liubimoe.tv/0c985436-bd42-4d69-8c43-0f231489370f/lv-ltv1/index.m3u8'},
															#{'name':'LTV1 - Tiešraide 6 ', 'url': 'http://83.166.48.35:8888/udp/235.35.1.20:1234'}
															{'name':'LTV1 - Tiešraide 1 ', 'url': 'http://80.70.22.46:80/LTV1&ff/video.m3u8'}
															]
												},
												{'name': 'LTV7',
												'thumb': '%s/ltv7.png',
												'guide': 'https://tv.lattelecom.lv/lv/programma/interaktiva/list/ltv7/',
												'sources': [
															#{'name': 'LTV7 - Tiešraide 1 [COLOR yellow][Ārzemes Neies][/COLOR][COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'resolve_ltv7_source1'},
															#{'name': 'LTV7 - Tiešraide 2 [COLOR yellow][Ārzemes Neies][/COLOR][COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://dvb.gpsystems.lv:4242/bynumber/3'},
															#{'name': 'LTV7 - Tiešraide 3 [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://80.70.22.46/LTV7/playlist.m3u8', 'key': 0},
															#{'name': 'LTV7 - Tiešraide 4 [COLOR yellow][Iet Tikai Ārzemēs][/COLOR]', 'url': 'http://89.201.43.188/play.php?freq=168.25', 'key': 2},
															#{'name': 'LTV7 - Tiešraide 5', 'url': 'http://ts.liubimoe.tv/0c985436-bd42-4d69-8c43-0f231489370f/lv-ltv7/index.m3u8'}
															{'name': 'LTV7 - Tiešraide 1', 'url': 'http://80.70.22.46:80/LTV7&ff/video.m3u8'}
															]
												},
												{'name': 'TV3 Latvija',
												'thumb': '%s/tv3.png',
												'guide': 'https://tv.lattelecom.lv/lv/programma/interaktiva/list/tv3/',
												'sources': [
															#{'name': 'TV3 Latvija - High [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream2_high.stream/chunklist.m3u8'},
															#{'name': 'TV3 Latvija - Medium [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream2_medium.stream/chunklist.m3u8'},
															#{'name': 'TV3 Latvija - Low [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream2_low.stream/chunklist.m3u8'},
															#{'name': 'TV3 Latvija - Tiešraide 4 [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://80.70.22.46/TV3/playlist.m3u8', 'key': 0},
															#{'name': 'TV3 Latvija - Tiešraide 5 [COLOR red][Iet Tikai Ārzemēs][/COLOR]', 'url': 'http://89.201.43.188/play.php?freq=161.25', 'key': 2},
															#{'name': 'TV3 Latvija - Tiešraide 6', 'url': 'http://ts.liubimoe.tv/0c985436-bd42-4d69-8c43-0f231489370f/lv-tv3/index.m3u8'},
															#{'name': 'TV3 Latvija - Tiešraide 7', 'url': 'http://83.166.48.35:8888/udp/235.35.1.22:1234'}
															{'name': 'TV3 Latvija - Tiešraide 1', 'url': 'https://mtglv1010.cloudycdn.services/tvplay/_definst_/mtgstream2.smil/chunklist_b1863680.m3u8'}
															]
												},
												{'name': 'LNT',
												'thumb': '%s/lnt.png',
												'guide': 'https://tv.lattelecom.lv/lv/programma/interaktiva/list/lnt/',
												'sources': [
															#{'name': 'LNT - High [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream1_high.stream/playlist.m3u8'},
															#{'name': 'LNT - Medium [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream1_medium.stream/playlist.m3u8'},
															#{'name': 'LNT - Low [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream1_low.stream/playlist.m3u8'},
															#{'name': 'LNT - Tiešraide 4 [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://80.70.22.46/LNT/playlist.m3u8', 'key': 0},
															#{'name': 'LNT - Tiešraide 5 [COLOR yellow][Iet Tikai Ārzemēs][/COLOR]', 'url': 'http://89.201.43.188/play.php?freq=154.25', 'key': 2},
															#{'name': 'LNT - Tiešraide 6', 'url': 'http://ts.liubimoe.tv/0c985436-bd42-4d69-8c43-0f231489370f/lv-lnt/index.m3u8'},
															#{'name': 'LNT - Tiešraide 7', 'url': 'http://83.166.48.35:8888/udp/235.35.1.19:1234'}
															{'name': 'LNT - Tiešraide 1', 'url': 'https://mtglv1010.cloudycdn.services/tvplay/_definst_/mtgstream1.smil/chunklist_b1863680.m3u8'}
															]
												},
												{'name': 'TV6 Latvija',
												'thumb': '%s/tv6.png',
												'guide': 'https://tv.lattelecom.lv/lv/programma/interaktiva/list/tv6/',
												'sources': [
															#{'name': 'TV6 Latvija - High [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream4_high.stream/playlist.m3u8'},
															#{'name': 'TV6 Latvija - Medium [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream4_medium.stream/playlist.m3u8'},
															#{'name': 'TV6 Latvija - Low [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream4_low.stream/playlist.m3u8'},
															#{'name': 'TV6 Latvija - Tiešraide 4 [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://80.70.22.46/TV6/playlist.m3u8', 'key': 0},
															#{'name': 'TV6 Latvija - Tiešraide 5 [COLOR red][Iet Tikai Ārzemēs][/COLOR]', 'url': 'http://89.201.43.188/play.php?freq=189.25', 'key': 2},
															#{'name': 'TV6 Latvija - Tiešraide 6', 'url': 'http://ts.liubimoe.tv/0c985436-bd42-4d69-8c43-0f231489370f/lv-tv6/index.m3u8'},
															#{'name': 'TV6 Latvija - Tiešraide 7', 'url': 'http://83.166.48.35:8888/udp/235.35.1.25:1234'}
															{'name': 'TV6 Latvija - Tiešraide 1', 'url': 'https://mtglv1010.cloudycdn.services/tvplay/_definst_/mtgstream4.smil/chunklist_b1863680.m3u8'}
															]
												},
												{'name': 'Kanāls 2',
												'thumb': '%s/kanals2.png',
												'guide': 'https://tv.lattelecom.lv/lv/programma/interaktiva/list/kanals_2/',
												'sources': [
															#{'name': 'Kanāls 2 - High [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream3_high.stream/playlist.m3u8'},
															#{'name': 'Kanāls 2 - Medium [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream3_medium.stream/playlist.m3u8'},
															#{'name': 'Kanāls 2 - Low [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'http://wpc.11eb4.teliasoneracdn.net/8011EB4/origin1/tvplay/mtgstream3_low.stream/playlist.m3u8'},
															#{'name': 'Kanāls 2 - Tiešraide 4 [COLOR red][Iet Tikai Ārzemēs][/COLOR]', 'url': 'http://89.201.43.188/play.php?freq=503.25', 'key': 2},
															#{'name': 'Kanāls 2 - Tiešraide 5', 'url': 'http://ts.liubimoe.tv/0c985436-bd42-4d69-8c43-0f231489370f/lv-kanals2/index.m3u8'},
															#{'name': 'Kanāls 2 - Tiešraide 6', 'url': 'http://83.166.48.35:8888/udp/235.35.1.18:1234'}
															{'name': 'Kanāls 2 - Tiešraide 1', 'url': 'https://mtglv1010.cloudycdn.services/tvplay/_definst_/mtgstream3.smil/chunklist_b1863680.m3u8'}
															]
												},
												{'name': 'PBMK',
												'thumb': '%s/pbmk.png',
												'guide': None,
												'sources': [{'name': 'Первый Балтийский Музыкальный - Tiešraide 1', 'url': 'https://streamer4.tvdom.tv/PBMK/tracks-v1a1/index.m3u8?token=token1'},
															{'name': 'Первый Балтийский Музыкальный - Tiešraide 2', 'url': 'http://ts.liubimoe.tv/0c985436-bd42-4d69-8c43-0f231489370f/ru-perv-muz-kanal/index.m3u8'}]
												}]
								  },
			  'Populārzinātniskie Kanāli': {
									'icon': '%s/science.png',
									'channels':	[{'name': 'Discovery Channel',
												'thumb': '%s/discoverychannel.png',
												'guide': 'https://tv.lattelecom.lv/lv/programma/interaktiva/list/discovery_channel/',
												'sources': [{'name':'Discovery Channel - [English]', 'url': 'resolve_discoverychannel_source1'},
															{'name':'SeeTV|Discovery Channel - [Russian]', 'url': "resolve_seetv_stream('http://seetv.tv/vse-tv-online/discovery-channel-tv')"}]
												},
												{'name': 'Discovery Science',
												'thumb': '%s/discoveryscience.png',
												'guide': 'https://tv.lattelecom.lv/lv/programma/interaktiva/list/discovery_science/',
												'sources': [{'name':'Discovery Science - [English] [COLOR red][Iespējams Bojāts][/COLOR]', 'url': 'resolve_discoverychannelhd_source1'},
															{'name':'SeeTV|Discovery Science - [Russian]', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/discovery-science' )"}]
												},
												{'name': 'Animal Planet',
												'thumb': '%s/AnimalPlanet.png',
												'guide': 'http://seetv.tv/vse-tv-online/animalplanet',
												'sources': [{'name':'Animal Planet- [Russian]', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/animalplanet' )"}]
												},
												{'name': 'NASA TV',
												'thumb': '%s/nasatv.png',
												'guide': None,
												'sources': [{'name':'NASA TV - [English]', 'url': 'http://nasatv-lh.akamaihd.net/i/NASA_101@319270/master.m3u8'}]
												},												
												{'name': 'Viasat Explorer',
												'thumb': '%s/viasatexplorer.png',
												'guide': 'http://tivix.co/tvprog/getprog.php?wmode=transparent&chnum=152',
												'sources': [{'name':'tvid.us|Viasat Explorer - [Russian]', 'url': 'http://178.124.183.19/hls/CH_VIASATEXPLORER/variant.m3u8?'},
															{'name':'TIVIX|Viasat Explorer - [Russian]', 'url': 'resolve_tivix_stream("http://tivix.co/119-viasat-explorer.html")'}]
												},
												{'name': 'Viasat History',
												'thumb': '%s/viasathistory.png',
												'guide': 'http://tivix.co/tvprog/getprog.php?wmode=transparent&chnum=175',
												'sources': [{'name':'SeeTV|Viasat History - [Russian]', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/viasathistory' )"},
															{'name':'TIVIX|Viasat History - [Russian]', 'url': 'resolve_tivix_stream("http://tivix.co/116-viasat-history.html")'},
															{'name':'TVLT|Viasat History - [Russian]', 'url': 'http://83.166.48.35:8888/udp/235.35.1.8:1234'}]
												},
												{'name': 'Viasat Nature',
												'thumb': '%s/viasatnature.png',
												'guide': 'http://tivix.co/tvprog/getprog.php?wmode=transparent&chnum=652',
												'sources': [{'name':'SeeTV|Viasat Nature - [Russian]', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/viasatnature' )"},
															{'name':'TIVIX|Viasat Nature - [Russian]', 'url': 'resolve_tivix_stream("http://tivix.co/180-viasat-nature.html")'},
															{'name':'TVLT|Viasat Nature - [Russian]', 'url': 'http://83.166.48.35:8888/udp/235.35.1.7:1234'}]
												},
												{'name': 'National Geographic Channel',
												'thumb': '%s/nationalgeographic.png',
												'guide': 'http://seetv.tv/vse-tv-online/national-geographic-channel',
												'sources': [{'name':'SeeTV|National Geographic Channel - [Russian]', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/national-geographic-channel' )"}]
												},
												{'name': 'Nat Geo Wild',
												'thumb': '%s/natgeowild.png',
												'guide': 'http://seetv.tv/vse-tv-online/natgeowild',
												'sources': [{'name':'SeeTV|Nat Geo Wild - [Russian]', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/natgeowild' )"},
															{'name':'TIVIX|Nat Geo Wild - [Russian]', 'url': 'resolve_tivix_stream("http://tivix.co/347-nat-geo-wild.html")'}]
												}]
								  },
			  'русские каналы': {
									'icon': '%s/Russia.png',
									'channels':	[{'name': 'СТБ',
												'thumb': '%s/stb.png',
												'guide': 'http://seetv.tv/vse-tv-online/stb-ch-ua',
												'sources': [{'name':'SeeTV|СТБ', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/stb-ch-ua' )"}]
												},
												{'name': 'ТНТ',
												'thumb': '%s/tnt.png',
												'guide': 'http://tivix.co/tvprog/getprog.php?wmode=transparent&chnum=14',
												'sources': [{'name':'SeeTV|ТНТ', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/tnt-tv-202' )"},
															{'name':'TIVIX|ТНТ', 'url': 'resolve_tivix_stream("http://tivix.co/10-tnt.html")'}]
												},
												{'name': 'ТНТ4 (Comedy TV)',
												'thumb': '%s/tnt4.png',
												'guide': 'http://seetv.tv/vse-tv-online/tnt-comedy',
												'sources': [{'name':'SeeTV|ТНТ4 (Comedy TV)', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/tnt-comedy' )"},
															{'name':'TIVIX|ТНТ4 (Comedy TV)', 'url': 'resolve_tivix_stream("http://tivix.co/29-kamedi-tv.html")'}]
												},												
												{'name': 'Кинохит',
												'thumb': '%s/kinohit.png',
												'guide': 'http://seetv.tv/vse-tv-online/kinohit',
												'sources': [{'name':'SeeTV|Кинохит', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/kinohit' )"},
															{'name':'TIVIX|Кинохит', 'url': 'resolve_tivix_stream("http://tivix.co/328-kinohit.html")'}]
												},
												{'name': 'Рен ТВ',
												'thumb': '%s/rentv.png',
												'guide': 'https://tv.lattelecom.lv/lv/programma/interaktiva/list/ren_baltija/',
												'sources': [{'name':'SeeTV|Рен ТВ', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/peh-tb' )"},
															{'name':'TIVIX|Рен ТВ', 'url': 'resolve_tivix_stream("http://tivix.co/8-ren-tv.html")'}]
												},
												{'name': 'СТС',
												'thumb': '%s/sts.png',
												'guide': 'http://seetv.tv/vse-tv-online/ctc',
												'sources': [{'name':'SeeTV|СТС', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/ctc' )"},
															{'name':'TIVIX|СТС', 'url': 'resolve_tivix_stream("http://tivix.co/11-sts.html")'}]
												},
												{'name': 'Первый канал',
												'thumb': '%s/1kanal.png',
												'guide': 'http://tivix.co/tvprog/getprog.php?wmode=transparent&chnum=8',
												'sources': [{'name':'SeeTV|Первый канал', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/perviy-kanal' )"},
															{'name':'TIVIX|Первый канал', 'url': 'resolve_tivix_stream("http://tivix.co/336-pervyy-kanal.html")'}]
												},
												{'name': 'Кинопремьера',
												'thumb': '%s/hdkino.png',
												'guide': 'http://tivix.co/tvprog/getprog.php?wmode=transparent&chnum=34',
												'sources': [{'name':'TIVIX|Кинопремьера', 'url': 'resolve_tivix_stream("http://tivix.co/251-kino-tv.html")'}]
												},
												{'name': 'Дом кино',
												'thumb': '%s/domkino.png',
												'guide': 'http://tivix.co/tvprog/getprog.php?wmode=transparent&chnum=302',
												'sources': [{'name':'TIVIX|Дом кино', 'url': 'resolve_tivix_stream("http://tivix.co/115-telekanal-dom-kino.html")'}]
												},
												{'name': 'Наше кино',
												'thumb': '%s/nashekino.png',
												'guide': 'http://tivix.co/tvprog/getprog.php?wmode=transparent&chnum=312',
												'sources': [{'name':'TIVIX|Наше кино', 'url': 'resolve_tivix_stream("http://tivix.co/319-nashe-kino.html")'}]
												},
												{'name': 'TV 1000 Megahit HD',
												'thumb': '%s/tv1000megahit.png',
												'guide': 'http://seetv.tv/vse-tv-online/tv1000-megahit-hd',
												'sources': [{'name':'TIVIX|TV 1000 Megahit HD', 'url': 'resolve_tivix_stream("http://tivix.co/270-tv1000-megahit-hd.html")'},
															{'name':'SeeTV|TV 1000 Megahit HD', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/tv1000-megahit-hd' )"}]
												},
												{'name': 'TV 1000 Premium HD',
												'thumb': '%s/tv1000premium.png',
												'guide': 'http://seetv.tv/vse-tv-online/tv1000-premium-hd',
												'sources': [{'name':'TIVIX|TV 1000 Premium HD', 'url': 'resolve_tivix_stream("http://tivix.co/271-tv-1000-premium-hd.html")'},
															{'name':'SeeTV|TV 1000 Premium HD', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/tv1000-premium-hd' )"}]
												},
												{'name': 'ТВ 1000 Русское кино',
												'thumb': '%s/tv1000ruskoekino.png',
												'guide': 'http://seetv.tv/vse-tv-online/tv1000rus',
												'sources': [{'name':'TIVIX|ТВ 1000 Русское кино', 'url': 'resolve_tivix_stream("http://tivix.co/187-tv-1000-russkoe-kino.html")'},
															{'name':'SeeTV|ТВ 1000 Русское кино', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/tv1000rus' )"}]
												},
												{'name': 'ТV 1000 Action',
												'thumb': '%s/tv1000action.png',
												'guide': 'http://seetv.tv/vse-tv-online/tv1000',
												'sources': [{'name':'TIVIX|ТV 1000 Action', 'url': 'resolve_tivix_stream("http://tivix.co/67-tv1000-action.html")'},
															{'name':'SeeTV|ТV 1000 Action', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/tv1000' )"}]
												},
												{'name': 'ТV 1000',
												'thumb': '%s/tv1000.png',
												'guide': 'http://seetv.tv/vse-tv-online/tv1000east',
												'sources': [{'name':'TIVIX|ТV 1000', 'url': 'resolve_tivix_stream("http://tivix.co/188-tv-1000.html")'},
															{'name':'SeeTV|ТV 1000', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/tv1000east' )"}]
												},
												{'name': 'ТV 1000 Comedy HD',
												'thumb': '%s/tv1000comedy.png',
												'guide': 'http://seetv.tv/vse-tv-online/tv1000-comedy-hd',
												'sources': [{'name':'TIVIX|ТV 1000 Comedy HD', 'url': 'resolve_tivix_stream("http://tivix.co/276-tv-1000-comedy-hd.html")'},
															{'name':'SeeTV|ТV 1000 Comedy HD', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/tv1000-comedy-hd' )"}]
												},
												{'name': 'Охота и рыбалка',
												'thumb': '%s/ohota-i-rybalka.png',
												'guide': 'http://tivix.co/tvprog/getprog.php?wmode=transparent&chnum=243',
												'sources': [{'name':'TIVIX|Охота и рыбалка', 'url': 'resolve_tivix_stream("http://tivix.co/175-ohota-i-rybalka.html")'},
															{'name':'SeeTV|Охота и рыбалка', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/ohota-i-rybalka' )"}]
												},
												{'name': 'Россия 24',
												'thumb': '%s/rossija24.png',
												'guide': 'http://tivix.co/tvprog/getprog.php?wmode=transparent&chnum=328',
												'sources': [{'name':'TIVIX|Россия 24', 'url': 'resolve_tivix_stream("http://tivix.co/62-rossiya-24.html")'},
															{'name':'Vesti.ru|Россия 24', 'url': 'resolve_vestiru_stream("https://player.vgtrk.com/iframe/live/id/21/showZoomBtn/false/isPlay/true/")'}]
												},
												{'name': 'Россия 1',
												'thumb': '%s/russia1.png',
												'guide': 'http://tivix.co/tvprog/getprog.php?wmode=transparent&chnum=9',
												'sources': [{'name':'TIVIX|Россия 1', 'url': 'resolve_tivix_stream("http://tivix.co/61-rossiya-1.html")'},
															{'name':'Vesti.ru|Россия 1', 'url': "resolve_vestiru_stream('https://player.vgtrk.com/iframe/live/id/2961/showZoomBtn/false/isPlay/true/')"}]
												}]
								  },
				'Mūzikas Kanāli': {
									'icon': '%s/music2.png',
									'channels':	[{'name': '1HD Music Television',
												'thumb': '%s/1HD.png',
												'guide': None,
												'sources': [{'name': '1HD Music Television', 'url': 'http://80.250.191.10:1935/live/hlsstream343/playlist.m3u8'}]
												},
												{'name': '365 Music TV',
												'thumb': '%s/365music.png',
												'guide': None,
												'sources': [{'name': '365 Music TV', 'url': 'https://str4.365music.ru/365music_hls/tracks-v1a1/index.m3u8'}]
												},
												{'name': 'MTV Hits',
												'thumb': '%s/mtvhits.png',
												'guide': None,
												'sources': [{'name': 'TIVIX|MTV Hits', 'url': 'resolve_tivix_stream("http://tivix.co/159-mtv-hits.html")'}]
												},
												{'name': 'MTV Dance',
												'thumb': '%s/mtvdance.png',
												'guide': None,
												'sources': [{'name': 'TIVIX|MTV Dance', 'url': 'resolve_tivix_stream("http://tivix.co/161-mtv-dance.html")'}]
												},
												{'name': 'Music Box UA',
												'thumb': '%s/musicboxua.png',
												'guide': None,
												'sources': [{'name': 'TIVIX|Music Box UA', 'url': 'resolve_tivix_stream("http://tivix.co/158-music-box-ua.html")'},
															{'name': 'SEETV|Music Box UA', 'url': 'resolve_seetv_stream("http://seetv.tv/vse-tv-online/music-box-ua")'}]
												},
												{'name': 'VH1',
												'thumb': '%s/vh1.png',
												'guide': None,
												'sources': [{'name': 'TIVIX|VH1', 'url': 'resolve_tivix_stream("http://tivix.co/265-vh1-europe.html")'}]
												},
												{'name': 'VH1 Classic',
												'thumb': '%s/vh1classic.png',
												'guide': None,
												'sources': [{'name': 'TIVIX|VH1 Classic', 'url': 'resolve_tivix_stream("http://tivix.co/264-vh1-classik.html")'}]
												},
												{'name': 'M1',
												'thumb': '%s/m1.png',
												'guide': None,
												'sources': [{'name': 'TIVIX|M1', 'url': 'resolve_tivix_stream("http://tivix.co/348-m1.html")'}]
												},
												{'name': 'Rock HD',
												'thumb': '%s/rockhd.png',
												'guide': None,
												'sources': [{'name': 'Rock HD', 'url': 'rtmp://91.201.78.3:1935/live/rockhd'}]
												},
												{'name': 'Heavy Metal Television',
												'thumb': '%s/heavymetaltv.png',
												'guide': None,
												'sources': [{'name': 'Heavy Metal Television', 'url': 'http://70.166.98.130:1935/hmtv/myStream/playlist.m3u8'}]
												}]
								  },
				'Sporta Kanāli': {
									'icon': '%s/sport.png',
									'channels':	[{'name': 'Viasat Sport Baltic',
												'thumb': '%s/viasatsportbaltic.png',
												'guide': 'https://tv.lattelecom.lv/lv/programma/interaktiva/list/viasat_sport_baltic/',
												'sources': [{'name': 'SVO|Viasat Sport Baltic [COLOR red][Ārzemes Neies][/COLOR]', 'url': "resolve_sportsvideoonline3( 'http://sportsvideoline3.pw/player?channel=sportbaltic&player=clappr' )"},
															{'name': 'HVZ|Viasat Sport Baltic', 'url': "http://ts.liubimoe.tv/0c985436-bd42-4d69-8c43-0f231489370f/lv-vs-sport-balt/index.m3u8"},
															{'name': 'TVLT|Viasat Sport Baltic', 'url': "http://83.166.48.35:8888/udp/235.35.1.6:1234"},
															{'name': 'onlysport.tv|Viasat Sport Baltic', 'url': "resolve_onlysport_tv_stream('http://onlysport.tv/player?channel=vbaltic&player=clappr')"}]
												},
												{'name': 'Viasat Sport',
												'thumb': '%s/viasatsport.png',
												'guide': None,
												'sources': [{'name': 'SVO|Viasat Sport [COLOR red][Ārzemes Neies][/COLOR]', 'url': "resolve_sportsvideoonline3( 'http://sportsvideoline3.pw/player?channel=viasatsporteast&player=clappr' )"},
															{'name': 'TIVIX|Viasat Sport', 'url': "resolve_tivix_stream( 'http://tivix.co/117-viasat-sport.html' )"}]
												},
												{'name': 'Eurosport 1',
												'thumb': '%s/eurosport1.png',
												'guide': 'https://tv.lattelecom.lv/lv/programma/interaktiva/list/eurosport_1/',
												'sources': [{'name': 'SVO|Eurosport 1 [COLOR red][Ārzemes Neies][/COLOR]', 'url': "resolve_sportsvideoonline3( 'http://sportsvideoline3.pw/player?channel=eurosport&player=clappr' )"},
															{'name': 'SEETV|Eurosport 1', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/eurosport' )"}]
												},
												{'name': 'Eurosport 2',
												'thumb': '%s/eurosport2.png',
												'guide': 'http://seetv.tv/vse-tv-online/eurosport-2-online',
												'sources': [{'name': 'SVO|Eurosport 2 [COLOR red][Ārzemes Neies][/COLOR]', 'url': "resolve_sportsvideoonline3( 'http://sportsvideoline3.pw/player?channel=eurosport2&player=clappr' )"},
															{'name': 'SEETV|Eurosport 2', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/eurosport-2-online' )"}]
												},
												{'name': 'КХЛ',
												'thumb': '%s/khl.png',
												'guide': 'https://tv.lattelecom.lv/lv/programma/interaktiva/list/khl/',
												'sources': [{'name': 'SVO|КХЛ [COLOR red][Ārzemes Neies][/COLOR]', 'url': "resolve_sportsvideoonline3( 'http://sportsvideoline3.pw/player?channel=khl&player=clappr' )"},
															{'name': 'SEETV|КХЛ', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/khl-tv' )"},
															{'name': 'TIVIX|КХЛ', 'url': "resolve_tivix_stream( 'http://tivix.co/53-khl-tv.html' )"}]
												},
												{'name': 'КХЛ HD',
												'thumb': '%s/khlhd.png',
												'guide': None,
												'sources': [{'name': 'SVO|КХЛ HD [COLOR red][Ārzemes Neies][/COLOR]', 'url': "resolve_sportsvideoonline3( 'http://sportsvideoline3.pw/player?channel=khlhd&player=clappr' )"},
															{'name': 'SEETV|КХЛ HD', 'url': "resolve_seetv_stream( 'http://seetv.tv/vse-tv-online/khl-hd' )"}]
												},
												{'name': 'СПОРТ 1',
												'thumb': '%s/sport1.png',
												'guide': None,
												'sources': [{'name': 'SVO|СПОРТ 1 [COLOR red][Ārzemes Neies][/COLOR]', 'url': "resolve_sportsvideoonline3( 'http://sportsvideoline3.pw/player?channel=sport1ru&player=clappr' )"}]
												},
												{'name': 'СПОРТ',
												'thumb': '%s/sportrussia.png',
												'guide': None,
												'sources': [{'name': 'SVO|СПОРТ [COLOR red][Ārzemes Neies][/COLOR]', 'url': "resolve_sportsvideoonline3( 'http://sportsvideoline3.pw/player?channel=sportrussia&player=clappr' )"}]
												},
												{'name': 'ФУТБОЛ 1 УКРАИНА',
												'thumb': '%s/futbol1ua.png',
												'guide': None,
												'sources': [{'name': 'SVO|ФУТБОЛ 1 УКРАИНА [COLOR red][Ārzemes Neies][/COLOR]', 'url': "resolve_sportsvideoonline3( 'http://sportsvideoline3.pw/player?channel=football1ua&player=clappr' )"}]
												},
												{'name': 'ФУТБОЛ 2 УКРАИНА',
												'thumb': '%s/futbol2ua.png',
												'guide': None,
												'sources': [{'name': 'SVO|ФУТБОЛ 2 УКРАИНА [COLOR red][Ārzemes Neies][/COLOR]', 'url': "resolve_sportsvideoonline3( 'http://sportsvideoline3.pw/player?channel=football2ua&player=clappr' )"}]
												}
												]
								  }
			  }
					
channelKeys = [
	'3f09dffb6f9b05782ce5fe94eff7156d14238ce35b2f39bf0bd2d69ca976c45e',
	'0678966dbb59ed47c43162874ae5a4a5038720ee1c228e1944d2a95117f9584c', #devtools
	'dfcc5460ce3f865b76cd0f8040c673d176d3b193e7c63c0c95ec0a9c8a8f7ff0', #kaspiejodairsis
]		

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

mysettings = xbmcaddon.Addon(id = 'plugin.video.dzivaistv')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
getSetting = xbmcaddon.Addon().getSetting
iconpath = xbmc.translatePath(os.path.join(home, 'resources/icons/'))

skin_used = xbmc.getSkinDir()


def showkeyboard(txtMessage="",txtHeader="",passwordField=False):
    if txtMessage=='None': txtMessage=''
    keyboard = xbmc.Keyboard(txtMessage, txtHeader, passwordField)#("text to show","header text", True="password field"/False="show text")
    keyboard.doModal()
    if keyboard.isConfirmed():
        return keyboard.getText()
    else:
        return False # return ''
		
		
def postHTML(url, post_fields):

	if sys.hexversion >= 0x02070BF0:
		r = requests.post(url, data=post_fields)
		print(r.status_code, r.reason)
		html = r.text.encode('utf-8')
	else:
		print "Crap we have the old version"
	
		
		# http://dev.morf.lv/mirror.php?url=https://cinemalive.tv/scripts/search.php&post=
		postParam = ""
		for key, value in post_fields.iteritems():
			postParam+=key+":"+value
		
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
	
def getHTML(url, data = False):	   
	print "Downloading URL... " + url
	
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'pl-PL,pl;q=0.8',
		'Connection': 'keep-alive'}
		

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
			return None

		html = page.read()
	else:
		print "Crap we have the old version"
		
		req = urllib2.Request("http://dev.morf.lv/mirror.php?url="+url, headers=hdr)
		
		try:
			page = urllib2.urlopen(req,timeout=5)
		except urllib2.HTTPError, e:
			print e.fp.read()
			return None

		html = page.read()
		
	print "Length of the string: ", len(html)
	
	#Let's just itterate through stupid encoding/decodings
	try:
		html = html.decode('utf-8').encode('utf-8')
	except:		
		html = html.decode('latin-1').encode('utf-8')
	
	print "URL Downloaded"
	return html
	
	
def resolve_ltv1_source1():

	try:
		html = getHTML('http://embed.ls.lv/ltv1g/index.php?utm_medium=ltv1')
	except:
		return False
	
	if html == None or len(html) < 1:
		return False
	
	searchObj = re.search('file: ".*"', html)
	if searchObj:
		resolvedUrl = searchObj.group().replace('file: "', '')
		resolvedUrl = resolvedUrl[:-1]
		return resolvedUrl
	else:
	   return False
	
def resolve_ltv7_source1():
	try:
		html = getHTML('http://embed.ls.lv/ltv2g/index.php?utm_medium=ltv2')
	except:
		return False
		
	if html == None or len(html) < 1:
		return False
		
	searchObj = re.search('file: ".*"', html)
	if searchObj:
		resolvedUrl = searchObj.group().replace('file: "', '')
		resolvedUrl = resolvedUrl[:-1]
		return resolvedUrl
	else:
	   return False
	  

def resolve_discoverychannelhd_source1():
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'pl-PL,pl;q=0.8',
		'Connection': 'keep-alive'}
		
	req = urllib2.Request('http://www.tikilive.com/embed?scheme=embedChannel&channelId=41598&autoplay=yes&showChat=no', headers=hdr)

	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print "ERROR while downloading: " + e.fp.read()
		return

	html = page.read()
	# html = getHTML()
	print html
	#resolve channelId
	searchObj = re.search("hlsCdnMoChannelId: '\d*'", html)
	if searchObj:
		channelId = searchObj.group().replace("hlsCdnMoChannelId: '", '')
		channelId = channelId[:-1]		
	else:
	   return False
	   
	#resolve start time
	searchObj = re.search("hlsCdnMoStime: '\d*'", html)
	if searchObj:
		hlsCdnMoStime = searchObj.group().replace("hlsCdnMoStime: '", '')
		hlsCdnMoStime = hlsCdnMoStime[:-1]		
	else:
	   return False
	   
	   
	#resolve end time
	searchObj = re.search("hlsCdnMoEtime: '\d*'", html)
	if searchObj:
		hlsCdnMoEtime = searchObj.group().replace("hlsCdnMoEtime: '", '')
		hlsCdnMoEtime = hlsCdnMoEtime[:-1]		
	else:
	   return False
	   
	#resolve token id
	searchObj = re.search("hlsCdnMoToken: '[\d\w]*'", html)
	if searchObj:
		hlsCdnMoToken = searchObj.group().replace("hlsCdnMoToken: '", '')
		hlsCdnMoToken = hlsCdnMoToken[:-1]		
	else:
	   return False
   
	return "http://tv-tikilive-live.hls.adaptive.level3.net/show_demotiki/405/amlst:mainstream/playlist.m3u8?op_id=19&userId=0&channelId="+channelId+"&stime="+hlsCdnMoStime+"&etime="+hlsCdnMoEtime+"&token="+hlsCdnMoToken
	
def resolve_discoverychannel_source1():
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'pl-PL,pl;q=0.8',
		'Connection': 'keep-alive'}
		
	req = urllib2.Request('http://www.tikilive.com/embed?scheme=embedChannel&channelId=40686&autoplay=yes&showChat=no', headers=hdr)

	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print "ERROR while downloading: " + e.fp.read()
		return

	html = page.read()
	# html = getHTML()
	print html
	#resolve channelId
	searchObj = re.search("hlsCdnMoChannelId: '\d*'", html)
	if searchObj:
		channelId = searchObj.group().replace("hlsCdnMoChannelId: '", '')
		channelId = channelId[:-1]		
	else:
	   return False
	   
	#resolve start time
	searchObj = re.search("hlsCdnMoStime: '\d*'", html)
	if searchObj:
		hlsCdnMoStime = searchObj.group().replace("hlsCdnMoStime: '", '')
		hlsCdnMoStime = hlsCdnMoStime[:-1]		
	else:
	   return False
	   
	   
	#resolve end time
	searchObj = re.search("hlsCdnMoEtime: '\d*'", html)
	if searchObj:
		hlsCdnMoEtime = searchObj.group().replace("hlsCdnMoEtime: '", '')
		hlsCdnMoEtime = hlsCdnMoEtime[:-1]		
	else:
	   return False
	   
	#resolve token id
	searchObj = re.search("hlsCdnMoToken: '[\d\w]*'", html)
	if searchObj:
		hlsCdnMoToken = searchObj.group().replace("hlsCdnMoToken: '", '')
		hlsCdnMoToken = hlsCdnMoToken[:-1]		
	else:
	   return False
   
	return "http://tv-tikilive-live.hls.adaptive.level3.net/show_demotiki/11/amlst:mainstream/playlist.m3u8?op_id=19&userId=0&channelId="+channelId+"&stime="+hlsCdnMoStime+"&etime="+hlsCdnMoEtime+"&token="+hlsCdnMoToken
	
def resolve_onlysport_tv_stream(url):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'pl-PL,pl;q=0.8',
		'Connection': 'keep-alive'}
		
	req = urllib2.Request(url, headers=hdr)

	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print "ERROR while downloading 1st attempt: " + e.fp.read()
		try:
			req = urllib2.Request("http://dev.morf.lv/mirror.php?url="+url, headers=hdr)
			page = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print "ERROR while downloading final attempt: " + e.fp.read()
			return

	html = page.read()
	# html = getHTML()
	print "DOWNLOADED HTML: ", html
	
	searchObj = re.search("(source|file): '.+'", html)
	if searchObj:
		resolvedLink = searchObj.group().split("'", 1)[1][:-1]
		# resolvedLink = searchObj.group().replace("source: '", '')
		# resolvedLink = resolvedLink[:-1]
	else:
	   return False
	   
	print "RESOLVED URL: ", resolvedLink
	return resolvedLink+"|Referer="+urllib.quote_plus(url)+"&Host="+urllib.quote_plus("cdn.videosofsport1.pw")
	
def resolve_seetv_stream(url):

	session = requests.Session()
	session.cookies.get_dict()
	response = session.get(url)
	html = response.content
	cookies = session.cookies.get_dict()
	print cookies
	# html = getHTML(url)
	
	searchObj = re.search('var linkTv = \d*;', html)
	if searchObj:
		resolvedLinkTv = searchObj.group().replace('var linkTv = ', '')
		resolvedLinkTv = resolvedLinkTv[:-1]
	else:
	   return False

	user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
	headers = { 
			'User-Agent' : user_agent,
			'Accept' : 'application/json, text/javascript, */*; q=0.01',
			'Accept-Language' : 'en-US,en;q=0.8,lv;q=0.6,en-GB;q=0.4',
			'Cache-Control' : 'no-cache',
			'Connection' : 'keep-alive',
			# 'Cookie' : '__cfduid=d1c6864852f2a1d64b53f2a0d92e7a6ed1481207982; uppodhtml5_volume=0.8; _ga=GA1.2.1188885436.1481207985; seetv_session_new=f63d8254c650c97898efa5a37f507cc96986279b',
			'Cookie' : '__cfduid='+cookies['__cfduid']+'; seetv_session_new='+cookies['seetv_session_new'],
			'Host' : 'seetv.tv',
			'Pragma' : 'no-cache',
			'Referer' : url,
			'X-Requested-With' : 'XMLHttpRequest'
		}
	req = urllib2.Request('http://seetv.tv/get/player/'+str(resolvedLinkTv), None, headers)
	response = urllib2.urlopen(req)

	result = json.loads(response.read())

	if result['status'] == True:
		# file = result['file'].replace("%3F", "?")
		file = result['file'].replace("%3F", "?")+"|Cookie="+urllib.quote_plus( headers['Cookie'] )+"&HttpProxy="+urllib.quote_plus("http://stream3.seetv.tv:8081")+"&Referer="+urllib.quote_plus(url)
		print (file)
		return file
	else:
		print False

	response.close()

def resolve_sportsvideoonline3(url):
	hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
		'Accept-Encoding': 'none',
		'Accept-Language': 'pl-PL,pl;q=0.8',
		'Connection': 'keep-alive'}
		
	req = urllib2.Request(url, headers=hdr)

	try:
		page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print "ERROR while downloading 1st attempt: " + e.fp.read()
		try:
			req = urllib2.Request("http://dev.morf.lv/mirror.php?url="+url, headers=hdr)
			page = urllib2.urlopen(req)
		except urllib2.HTTPError, e:
			print "ERROR while downloading final attempt: " + e.fp.read()
			return

	html = page.read()
	# html = getHTML()
	print "DOWNLOADED HTML: ", html
	
	searchObj = re.search("(source|file): '.+'", html)
	if searchObj:
		resolvedLink = searchObj.group().split("'", 1)[1][:-1]
		# resolvedLink = searchObj.group().replace("source: '", '')
		# resolvedLink = resolvedLink[:-1]
	else:
	   return False
	   
	print "RESOLVED URL: ", resolvedLink
	return resolvedLink+"|Referer="+urllib.quote_plus(url)+"&Host="+urllib.quote_plus("cdn.smotrimult.com")

def getURLFromObfJs(js):
	progress_dialog = xbmcgui.DialogProgress()
	progress_dialog.create("Dekodējam strīmu")
	js = js.replace(";eval", "fnRes=")
	print "return" in js
	#evalFn = js.split("'));")
	#print len(evalFn)
	#print evalFn

	count = 0
	maxTries = 4
	while "var value={" not in js or count == maxTries:
		progress = int(float((float(count)/maxTries)*100))
		print "Evaluating: " + str(count)
		progress_dialog.update( progress , "Lūdzu uzgaidi...", "Rūķīši cenšas dekodēt TIVIX strīmu", "Atlicis: " + str(maxTries - count) )
		if (progress_dialog.iscanceled()): return
		js = str(js2py.eval_js(js))
		js = js.replace(";eval", "fnRes=")
		count += 1

	#print js

	searchObj = re.search("'value':'[\'\w\d:\/.?=]*}", js)
	if searchObj:
		resolvedUrl = searchObj.group().replace("'value':'", "")
		resolvedUrl = resolvedUrl[:-2]
		return resolvedUrl
	else:
		return False
		

def fastTIVIXdeobfuscator(js):
	def decode1( w, i, s, e ):
		lIll = 0
		ll1I = 0
		Il1l = 0
		ll1l = []
		l1lI = []
		
		while True:
			if (lIll < 5): 
				l1lI.append(w[lIll])
			elif(lIll < len(w)):
				ll1l.append(w[lIll])
			lIll += 1
			if (ll1I < 5):
				l1lI.append(i[ll1I])
			elif (ll1I < len(i)):
				ll1l.append(i[ll1I])
			ll1I += 1
			if (Il1l < 5):
				l1lI.append(s[Il1l])
			elif (Il1l < len(s)):
				ll1l.append(s[Il1l])
			Il1l += 1
			if (len(w) + len(i) + len(s) + len(e) == len(ll1l) + len(l1lI) + len(e)):
				break
			
		
		lI1l = ''.join(ll1l)
		I1lI = ''.join(l1lI)
		
		# print lIll, ll1I, Il1l, lI1l, I1lI
		
		l1ll = []
		ll1I = 0;
		for lIll in xrange(0,len(ll1l),2):
			ll11 = -1		
			if (ord(I1lI[ll1I]) % 2):
				ll11 = 1
			l1ll.append(unichr(int(lI1l[lIll:lIll+2], 36) - ll11))
			ll1I += 1
			if (ll1I >= len(l1lI)):
				ll1I = 0
		return ''.join(l1ll)

	count = 0
	while "var value={" not in js or count == 10:
		print "Evaluating: " + str(count) + "\n"
		js = js.split("}(")[-1][:-3]
		decodeArg = js.replace("'", "").split( "," )
		# print "Decode arg: ", decodeArg
		js = decode1(decodeArg[0], decodeArg[1], decodeArg[2], decodeArg[3])
		count += 1
		
	searchObj = re.search("'value':'[\'\w\d:\/.?=]*}", js)
	if searchObj:
		resolvedUrl = searchObj.group().replace("'value':'", "")
		resolvedUrl = resolvedUrl[:-2]
		return resolvedUrl
	else:
		return False
		
def resolve_tivix_stream(url):

	session = requests.Session()
	session.cookies.get_dict()
	response = session.get(url)
	html = response.content
	cookies = session.cookies.get_dict()
	print cookies
	# html = getHTML(url)
	
	searchObj = re.search("<div id=\"advm_video\"><\/div>[ \\n\\r]*<script>[\\w\\d;\\n\\r\\t (),{}=\\[\\]<>\\.\\+\\'\\-\\%]*<\\/script>", html)
	if searchObj:
		resolvedJS = searchObj.group().replace("</script>","").split("<script>")[1].strip()
		# print resolvedLinkTv
		# resolvedLinkTv = resolvedLinkTv[:-1]
	else:
	   return False
	   
	header_m3u8 = {
			'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
			'Accept' : '*/*',
			'Accept-Encoding' : 'gzip, deflate, sdch',
			'X-Requested-With' : 'ShockwaveFlash/24.0.0.175',
			'Cookie' : 'PHPSESSID='+cookies['PHPSESSID'],
			# 'Host' : 'stream3.seetv.tv:8081',
			# 'HttpProxy' : 'http://stream3.seetv.tv:8081',
			'Pragma' : 'no-cache',
			'Cache-Control' : 'no-cache',
			'Connection' : 'keep-alive',
			'Referer' : url
	}
	
	streamUrl = fastTIVIXdeobfuscator( resolvedJS )
	if streamUrl == False:
		streamUrl = getURLFromObfJs(resolvedJS)
	resolvedStreamURL = streamUrl+"|"+urllib.urlencode(header_m3u8)
	print "TIVIX stream URL: " + resolvedStreamURL
	return 	resolvedStreamURL
		
	
def resolve_vestiru_stream(url):
	session = requests.Session()
	session.cookies.get_dict()
	response = session.get(url)
	html = response.content
	cookies = session.cookies.get_dict()
	print html, cookies
	# html = getHTML(url)
	
	searchObj = re.search(':"(https:|http:)\\/\\/[\\w\\d. \\/:?=&%-_]*"', html)
	if searchObj:
		resolvedUrl = searchObj.group().replace(':"', '')
		resolvedUrl = resolvedUrl[:-1]
	else:
	   return False
	   
	query = urlparse(str(resolvedUrl)).query.replace("&", "; ")
	print query
	
	header_m3u8 = {
			'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
			'Accept' : '*/*',
			'Accept-Encoding' : 'gzip, deflate, sdch',
			'X-Requested-With' : 'ShockwaveFlash/24.0.0.175',
			# 'Cookie' : 'ngx_uid='+cookies['ngx_uid'],
			'Cookie' : query,
			# 'Host' : 'stream3.seetv.tv:8081',
			# 'HttpProxy' : 'http://stream3.seetv.tv:8081',
			'Pragma' : 'no-cache',
			'Cache-Control' : 'no-cache',
			'Connection' : 'keep-alive',
			'Referer' : url
	}
	response = session.get(resolvedUrl)
	print "m3u8 file test download: "
	print response.content, response.headers
	
	
	
	resolvedStreamURL = resolvedUrl+"|"+urllib.urlencode(header_m3u8)
	print "vesti.ru stream URL: " + resolvedStreamURL
	
	return resolvedStreamURL
	

	

def get_categories():
         """
         Get's the list of channel categories: Latvian, Russian, Sport etc.
         """
         return channelList.keys()
		 
def get_sources(category, channel):
	channels = channelList[category]['channels']
	
	for ch in channels:
		if ch['name'] == channel:
			return ch['sources']
			
	return
	
def get_guide(category, channel):
	channels = channelList[category]['channels']
	
	for ch in channels:
		if ch['name'] == channel:
			return ch['guide']
			
	return None
	
def get_channel_icon(category, channel):
	channels = channelList[category]['channels']
	
	for ch in channels:
		if ch['name'] == channel:
			return ch['thumb']
			
	return
	
def isURL(url):
	if url.startswith("rtmp://") or url.startswith("http://") or url.startswith("https://"):
		return True
		
	
	try:
		f = urllib2.urlopen(url)
		print "Return code: " + str(f.getcode())
		return True
	except ValueError:  # invalid URL
		return False
	except:
		return False
		
def getKeys():
	keys = []
	dirname = xbmc.translatePath('special://profile/addon_data/plugin.video.dzivaistv/')
	if os.path.exists(dirname):
		localFile = dirname + 'dzivaistv.key'
		temp = open( localFile, mode='r')
		for line in temp:
			keyHash =  hashlib.sha256(line.rstrip('\n')).hexdigest()
			if keyHash not in keys:
				keys.append( keyHash )
		temp.close()
		
	return keys

def TestStreams():
	testItems = []
	keys = getKeys()
	
	categories = get_categories()
	for cat in categories:
		for ch in channelList[cat]['channels']:
			for source in ch['sources']:
				if 'key' in source.keys():
					channelKey = channelKeys[source['key']]
					if channelKey not in keys:
						continue
				testItems.append( {"path": cat+"/"+ch['name']+"/"+source['name'], "url": source['url'], "status": False, "icon":get_channel_icon(cat, ch['name']) } )
	
	pDialog = xbmcgui.DialogProgress()
	randomText = random.choice(loadingMessages)
	pDialog.create('Pārbaudam strīmus', 'Lūdzu uzgaidi...', randomText)
	print "Items to test: ", testItems
	
	for i in range(0, len(testItems)):
		progress = int(float((float(i)/len(testItems))*100))
		pDialog.update( progress , "Lūdzu uzgaidi...", randomText, "Atlicis: " + str(len(testItems) - i) )
		# pDialog.update( progress )
		if (pDialog.iscanceled()): break
		url = testItems[i]['url']
		
		testIfURL = isURL(url)
		# print "Is it URL? " + str(testIfURL)
		
		if testIfURL == False:
			funcArgStr = url.partition('(')[-1].rpartition(')')[0]
			funcArg = funcArgStr.split(',')
			funcArg = [x.replace("'","").replace('"','').replace(' ', '') for x in funcArg if x]
			
			functionName = url.split("(")[0]
			print "Function Name + Arguments: ", functionName, funcArg
			resolvedUrl = globals()[functionName](*funcArg)
			# resolvedUrl = eval( url )
			if resolvedUrl == False:
				testItems[i]['status'] = False
				continue
			else:
				resolvedUrl = resolvedUrl.split("|")[0]
		else:
			resolvedUrl = url.split("|")[0]
			
		print "Test resolved URL: " + resolvedUrl
		
		try:
			file = network.getHTML( resolvedUrl, limit = 100 )
			if file != None and "not found" not in file:
				# print "TESTED HTML: ", file
				testItems[i]['status'] = True
			else:
				testItems[i]['status'] = False
		except:
			print "Exception occured while downloading"
			testItems[i]['status'] = False
			
				
	badStreams = 0
	for result in testItems:
		if result['status'] == True:
			statusText = "[COLOR green][  OK  ][/COLOR] "
		else:
			statusText = "[COLOR red][Kļūda][/COLOR] "
			badStreams += 1
			
		addSysLink( statusText + result['path'], result['url'], 'status_play_stream', result['icon']% iconpath)
		
	pDialog.close()
	
	goodStreams = len(testItems)-badStreams
	appQuality = int(float((float(goodStreams)/len(testItems))*100))
	line1 = "Ejoši strīmi: " + str(goodStreams) + " no " + str(len(testItems))
	line2 = "Bojāti strīmi: " + str(badStreams) + " no " + str(len(testItems))
	line3 = "Aplikācijas kvalitāte: " + str(appQuality) + "%"
	xbmcgui.Dialog().ok( "Rezultāti: ", line1, line2, line3  )
	
def OpenTvGuide(url):
	 xbmc.executebuiltin(url)
	
def HomeNavigation():	
	categories = get_categories()
	for category in categories:
		addDir(category, category, 'state_channels', channelList[category]['icon']% iconpath)
		
	addSysLink( "Atslēga", "atslega", "state_enter_key",  "%s/unlock.png"% iconpath )
	keys = getKeys()
	if channelKeys[1] in keys:
		addDir( "Pārbaudīt strīmu statusus", "stream_status", "state_stream_status", "%s/signals.png"% iconpath )

	
def Channels(category):
	channels = channelList[category]['channels']
	# xbmc.executebuiltin('RunAddon(plugin.video.youtube)')
	for channel in channels:
		commands = None
		if channel['guide'] != None:
			commands = []
			commands.append(( 'Skatīt TV programmu', 'RunScript(special://home/addons/plugin.video.dzivaistv/programma.py, '+channel['name']+', '+channel['guide']+')', ))
			
		addDir(channel['name'], category+":"+channel['name'], 'state_sources', channel['thumb']% iconpath, None, commands)
		
def Sources(url):
	splitParam = url.split(":")
	
	category = splitParam[0]
	channel = splitParam[1]
	print category, channel
	sources = get_sources(category, channel)
	
	keys = getKeys()
	
	for i in range(0, len(sources)):
		if 'key' in sources[i].keys():
			channelKey = channelKeys[sources[i]['key']]
			if channelKey not in keys:
				continue
		addSysLink(sources[i]['name'], sources[i]['url'], 'status_play_stream', get_channel_icon(category, channel)% iconpath)
	
	guide = get_guide(category, channel)
	if guide != None:
		# commands = []
		# commands.append(( 'Skatīt TV programmu', 'RunScript(special://home/addons/plugin.video.dzivaistv/programma.py, '+channel['name']+', '+channel['guide']+')', ))
		addSysLink("[COLOR green]Skatīt TV Programmu[/COLOR]", 'RunScript(special://home/addons/plugin.video.dzivaistv/programma.py, '+channel+', '+guide+')', 'status_tv_guide', '%s/tvguide.png'% iconpath)
		
		#print isURL(sources[i]['url']), sources[i]
		#if isURL(sources[i]['url']) == False:
			#resolvedUrl = globals()[sources[i]['url']]()
			#if resolvedUrl != False:
				#addLink(sources[i]['name'], resolvedUrl, get_channel_icon(category, channel)% iconpath)
		#else:
			#addLink(sources[i]['name'], sources[i]['url'], get_channel_icon(category, channel)% iconpath)
			
	
def UnlockChannels():
	key = showkeyboard('', u'Ievadi Atslēgu')
	
	if not key:
		return
		
	keyHash =  hashlib.sha256(key).hexdigest()
	
	for knownKey in channelKeys:
		if keyHash == knownKey:
			print "Found a valid key"			
			dirname = xbmc.translatePath('special://profile/addon_data/plugin.video.dzivaistv/')
			if not os.path.exists(dirname):
				os.mkdir(dirname)
			
			localFile = dirname + 'dzivaistv.key'
			temp = open( localFile, mode='a')
			temp.write( key  + "\n" )
			temp.close()
			
			xbmcgui.Dialog().ok("Kods pieņemts", "Kods tika pieņemts", "Jums tagad ir pieejami papildus kanāli")
			# print localFile
			break
			
	print key, keyHash

def addDir(title, url, mode, picture, page=None, commands=None):
	sys_url = sys.argv[0] + '?title=' + urllib.quote_plus(title) + '&url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode))
	if  picture == None:
		item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage='')
	else:
		item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png' , thumbnailImage=picture)    
		sys_url += '&picture=' + urllib.quote_plus(str(picture))
	if page != None:
		sys_url += '&page=' + urllib.quote_plus(str(page))
	
	if commands != None:
		# print "MAN IR KOMMANDAS!"
		item.addContextMenuItems( commands )
		
	item.setInfo(type='Video', infoLabels={'Title': title})

	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys_url, listitem=item, isFolder=True)
	
def addLink(title, url, picture):
	if  picture == None:
		item = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage='')
	else:
		item = xbmcgui.ListItem(title, iconImage='DefaultVideo.png', thumbnailImage=picture)
	item.setInfo( type='Video', infoLabels={'Title': title} )	
	xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=url, listitem=item)
    
    
def addSysLink(title, url, mode, picture):
    if picture == None:
        item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage='')
    else:
        item = xbmcgui.ListItem(title, iconImage='DefaultFolder.png', thumbnailImage=picture)

    sys_url = sys.argv[0] + '?title=' + urllib.quote_plus(title) + '&url=' + urllib.quote_plus(url) + '&mode=' + urllib.quote_plus(str(mode)) + '&picture=' + urllib.quote_plus(str(picture))
    
    item.setInfo( type='Video', infoLabels={'Title': title} )

    xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=sys_url, listitem=item)
	
def play_stream(url):
	media_url = url
	print "MEDIA URL " + media_url
	item = xbmcgui.ListItem('TV3 Latvia', path = media_url)
	# xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
	# xbmcplugin.setResolvedUrl( handle=int( sys.argv[1]), succeeded=False, listitem=item )
	listItem = xbmcgui.ListItem("Tesfilm", path=media_url)
	xbmc.Player().play(item=media_url, listitem=listItem)
	return
	
def SetThumbnailView():
	if skin_used == 'skin.confluence':
		xbmc.executebuiltin('Container.SetViewMode(500)') # "Thumbnail" view
		
def PlayStream(url, title, picture):

	pDialog = xbmcgui.DialogProgress()
	pDialog.create('Dekodējam strīmu', 'Lūdzu uzgaidi...', random.choice(loadingMessages))
	
	resolvedUrl = None
	
	testIfURL = isURL(url)
	print "Is it URL? " + str(testIfURL)
	
	if testIfURL == False:
		funcArgStr = url.partition('(')[-1].rpartition(')')[0]
		funcArg = funcArgStr.split(',')
		funcArg = [x.replace("'","").replace('"','').replace(' ', '') for x in funcArg if x]
		
		functionName = url.split("(")[0]
		print "Function Name + Arguments: ", functionName, funcArg
		resolvedUrl = globals()[functionName](*funcArg)
		# resolvedUrl = eval( url )
		if resolvedUrl == False:
			d = xbmcgui.Dialog()
			d.ok('Radās Kļūda', 'Nevarēja dekodēt strīmu, mēģiniet vēlreiz vai mēginiet citu avotu.')
			return
	else:
		resolvedUrl = url
		
	listitem = xbmcgui.ListItem(title, path=url)
	listitem.setInfo(type='video', infoLabels={'title': title})
	listitem.setThumbnailImage(picture)
	
	print "Channel Thumbnail: ", picture
		
	xbmc.Player().play(resolvedUrl, listitem)
		
def get_params():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
        params=sys.argv[2]
        cleanedparams=params.replace('?','')
        if (params[len(params)-1]=='/'):
            params=params[0:len(params)-2]
        pairsofparams=cleanedparams.split('&')
        param={}
        for i in range(len(pairsofparams)):
            splitparams={}
            splitparams=pairsofparams[i].split('=')
            if (len(splitparams))==2:
                param[splitparams[0]]=splitparams[1]
                            
    return param

common = CommonFunctions
common.plugin = "Filmas-Latviski-0.0.1"

params = get_params()
url = None
title = None
mode = None
picture = None
page = 1

try:
    title = urllib.unquote_plus(params['title'])
except:
    pass
try:
    url = urllib.unquote_plus(params['url'])
except:
    pass
try:
    mode = urllib.unquote_plus(params['mode'])
except:
    pass
try:
    picture = urllib.unquote_plus(params['picture'])
except:
    pass
try:
    page = int(params['page'])
except:
    pass

if mode == None:
	HomeNavigation()
	SetThumbnailView()
elif mode == 'state_channels':
	Channels(url)
	SetThumbnailView()
elif mode =='state_sources':
	Sources(url)
elif mode == 'status_play_stream':
	PlayStream(url, title, picture)
elif mode == 'state_enter_key':
	print "ENTER THE KEY"
	UnlockChannels()
elif mode == 'state_stream_status':
	TestStreams()
elif mode == 'status_tv_guide':
	OpenTvGuide(url)

		

# print(requests.get("https://cinemalive.tv/filmaslatviski", verify=False))

	
xbmcplugin.endOfDirectory(int(sys.argv[1]))


# content = getHTML("https://cinemalive.tv/filmaslatviski");
# print content
	




# addon_handle = int(sys.argv[1])

# xbmcplugin.setContent(addon_handle, 'movies')

# url = urlresolver.resolve('https://openload.co/embed/eCLBpX3iByw/') 

# li = xbmcgui.ListItem('Sapinusies', iconImage='DefaultVideo.png')
# xbmcplugin.addDirectoryItem(handle=addon_handle, url=url, listitem=li)

# xbmcplugin.endOfDirectory(addon_handle)


