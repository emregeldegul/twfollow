#!/usr/bin/env python
# -*- coding: utf-8 -*-

#Modules
import mechanize, sqlite3, time, re, os

#Fixed
border_line_one = "-"*30
border_line_two = "-"*50

twitter_login = "https://mobile.twitter.com/login"
twitter_logout = "https://mobile.twitter.com/logout"
twitter_follow = "https://mobile.twitter.com/"
twitter_tweet = "https://mobile.twitter.com/compose/tweet"

twitter_login_check = "https://twitter.com/settings/account"
twitter_follow_check = []

proxy_site = "http://proxy-list.org/english/index.php?p=1"
proxy_lists = []
proxy_data = ['113.255.61.57:80', '108.58.186.227:3128', '60.251.46.23:3128', '222.188.100.203:8086',
'113.215.0.130:82', '125.209.91.190:8080', '202.145.3.242:8080', '179.124.212.139:80', '119.252.174.210:8080',
'218.29.111.106:9999', '191.102.115.66:8080', '128.199.164.105:8888', '177.234.0.110:3130', '117.135.241.80:8080',
'137.116.91.232:3128', '40.113.124.17:3128', '23.101.69.141:3128', '58.253.238.242:80', '123.59.12.25:80',
'104.209.187.151:3128', '60.219.24.125:3128', '177.47.238.18:8080', '58.147.174.167:8080', '104.171.126.86:8089',
'211.72.13.116:3128', '117.135.241.80:8080', '125.39.17.91:3128', '177.234.0.110:3130', '219.142.192.196:42969',
'185.93.54.194:3128', '181.49.221.6:8080', '192.3.90.124:3128', '195.34.238.154:8080', '123.125.114.167:80',
'124.240.187.84:82', '23.101.69.141:3128', '117.136.234.18:81', '218.29.155.198:9999', '83.241.46.175:8080',
'212.78.211.173:80', '219.142.192.196:212', '194.154.128.65:8080', '219.142.192.196:42969', '185.93.54.194:3128',
'181.49.221.6:8080', '192.3.90.124:3128', '195.34.238.154:8080', '123.125.114.167:80', '124.240.187.84:82',
'23.101.69.141:3128', '117.136.234.18:81', '218.29.155.198:9999', '83.241.46.175:8080', '212.78.211.173:80',
'219.142.192.196:212', '194.154.128.65:8080', '219.142.192.196:39475', '92.255.174.88:80', '124.240.187.79:80',
'112.1.185.108:8123', '162.248.240.137:3127', '80.98.162.102:8080', '112.95.190.144:9999', '122.96.59.105:82',
'40.113.124.17:3128', '192.3.90.124:3128', '92.50.188.98:8080', '89.46.233.100:8081', '61.174.10.22:8080', '207.28.38.3:3128']
proxy_list = proxy_lists

bold = "\033[1m"
underline = "\033[4m"
green = "\033[92m"
blue = "\033[94m"
yellow = "\033[93m"
red = "\033[91m"
endcolor = "\033[0m"

#Database Connection
if os.path.exists("wdata.db") == True:
	database = sqlite3.connect("wdata.db")
	cursor = database.cursor()
	print border_line_two
	print bold+blue+"[+] Veritabanı Bağlantısı Sağlandı"+endcolor
	print border_line_two
else:
	print border_line_two
	print bold+red+"[-] Veritabanı Bulunamadı"+endcolor
	print "[*] Veritabanı Oluşturuluyor"
	database = sqlite3.connect("wdata.db")
	cursor = database.cursor()
	print bold+blue+"Veritabanı Oluşturuldu"+endcolor
	print "[*] Tablolar Oluşturuluyor"
	cursor.execute("CREATE TABLE accounts (account_id INTEGER PRIMARY KEY AUTOINCREMENT, account_mail TEXT, account_password TEXT)")
	print bold+blue+"[+] Tablolar Oluşturuldu"+endcolor
	print border_line_two

#Start Of Browser
browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.addheaders = [('User-agent', 'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)')]

#Functions
def help():
	print "~~ TWFollow Twitter Takip Sistemi ~~"
	print bold+"Kullanım // Komutlar"+endcolor
	print yellow+"~ quit "+endcolor+" Çıkış"
	print yellow+"~ help "+endcolor+" Yardım bilgisi"
	print yellow+"~ statistics "+endcolor+" İstatik bilgisi"
	print yellow+"~ account_update filename.txt "+endcolor+" filename.txt dosyasından hesap aktar"
	print yellow+"~ proxy_update "+endcolor+" Proxy adreslerini günceller"
	print yellow+"~ show_accounts full / range 5,9 "+endcolor+" Veri tabanından kullanıcı hesaplarını çeker"
	print yellow+"~ show_proxy "+endcolor+" Mevcut proxy listesini görüntüler"
	print yellow+"~ account_del full / user ID / range 5,20 "+endcolor+" Belirtilen hesapları siler"
	print yellow+"~ follow_bot twitterKullaniciAdi "+endcolor+" Belirtilen kullanıcı hesabına takipçi yollar"
	print yellow+"~ feed_bot tweetlist.txt "+endcolor+" tweetlist.txt adresinde ki tweetleri sırayla yayımlar"
	print ""
	print bold+"Yazılım Hakkında"+endcolor
	print "Yazan: MuReCoder / https://emregeldegul.net"
	print "Sürüm: V2"

def account_update(filename):
	try:
		account_file = open(filename)
		account_line = account_file.readlines()
		for account in account_line:
			account = account.rsplit()
			account = account[0]
			jaggu = account.partition(":")
			email, dot, password = jaggu
			cursor.execute("""INSERT INTO accounts (account_mail, account_password) VALUES ("{}", "{}")""".format(email, password))
	except:
		print bold+red+"Hedef Dosyaya Bağlantı Sağlanamadı"+endcolor
	finally:
		database.commit()

def proxy_update():
	print bold+green+"[*] Proxy Listesi Güncelleniyor. Bu işlem bir kaç dakika sürebilir."+endcolor
	try:
		loop = 0
		while loop < 5:
			source_code = browser.open(proxy_site).read()
			proxy_address = re.findall('<li class="proxy">(.*?)</li>', source_code)
			for proxy in proxy_address:
				if proxy == "Proxy":
					continue
				proxy_list.append(proxy)
			loop += 1
			time.sleep(30)
		print bold+blue+"[+] Proxy listeniz güncellendi. Toplam {} proxy eklendi.".format(len(proxy_list))+endcolor
	except:
		print bold+red+"[-] Proxy listeniz güncellenemedi, bağlantınızı kontrol edin."+endcolor

def show_accounts(option, start=None, finish=None):
	if option == "full":
		comm = """SELECT * FROM accounts"""
	else:
		comm = """SELECT * FROM accounts WHERE account_id BETWEEN {} and {}""".format(start, finish)

	print "+------+----------------------------------------+--------------------+"
	print green+"+ ID   + Kullanıcı Adı & E-Posta                + Şifre              +"+endcolor
	print "+------+----------------------------------------+--------------------+"
	cursor.execute(comm)
	accounts = cursor.fetchall()
	for account in accounts:
		idno, email, password = account
		print "+ "+str(idno).zfill(4)+" + "+email.ljust(38) +" + "+password.ljust(18)+" +"
		print "+------+----------------------------------------+--------------------+"

def show_proxy():
	for proxy in proxy_list:
		print bold+"Proxy: "+endcolor+proxy

def account_del(comm):
	try:
		cursor.execute(comm)
		print "Belirtilen hesaplar silindi"
	except:
		print "Veri Tabanı Hatası!"
	finally:
		database.commit()

def follow_bot(nickname):
	start = int(raw_input("Start ID: "))
	finish = int(raw_input("Finish ID: "))
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	periot = (finish-start)/30
	order = 0
	periot_order = 0
	periot_check = 0
	print bold+"Başlangıç Saati: "+endcolor+time.strftime("%H:%M:%S")
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	cursor.execute("""SELECT * FROM accounts WHERE account_id BETWEEN {} and {}""".format(start, finish))
	accounts = cursor.fetchall()
	for account in accounts:
		order += 1
		idno, mail, password = account
		if mail in twitter_follow_check:
			order -= 1
		else:
			if periot_check == periot:
				periot_order += 1
				periot_check = 1
			browser.set_proxies({"http://":proxy_data[periot_order]})
			browser.open(twitter_login)
			browser.select_form(nr=0)
			browser['session[username_or_email]'] = mail
			browser['session[password]'] = password
			browser.submit()
			source_tw = browser.open(twitter_login_check).read()
			if mail.encode("utf-8") in source_tw:
				browser.open(twitter_follow+nickname)
				browser.select_form(nr=0)
				browser.submit()
				browser.open(twitter_logout)
				browser.select_form(nr=0)
				browser.submit()
				print "Devir Saati: "+time.strftime("%H:%M:%S")+" | Kişi Sıralaması: "+str(order)
			else:
				order -= 1
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print bold+blue+"Toplam Takipçi:"+endcolor+str(order)

def feed_bot():
	start = int(raw_input("Start ID: "))
	finish = int(raw_input("Finish ID: "))
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	cursor.execute("""SELECT * FROM accounts WHERE account_id BETWEEN {} and {}""".format(start, finish))
	accounts = cursor.fetchall()
	for account in accounts:
		order += 1
		idno, mail, password = account
		if mail in twitter_follow_check:
			order -= 1
		else:
			if periot_check == periot:
				periot_order += 1
				periot_check = 1
			browser.set_proxies({"http://":proxy_data[periot_order]})
			browser.open(twitter_login)
			browser.select_form(nr=0)
			browser['session[username_or_email]'] = mail
			browser['session[password]'] = password
			browser.submit()
			source_tw = browser.open(twitter_login_check).read()
			if mail.encode("utf-8") in source_tw:
				browser.open(twitter_follow+nickname)
				browser.select_form(nr=0)
				browser.submit()
				browser.open(twitter_logout)
				browser.select_form(nr=0)
				browser.submit()
				print "Devir Saati: "+time.strftime("%H:%M:%S")+" | Kişi Sıralaması: "+str(order)
			else:
				order -= 1
	print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
	print bold+blue+"Toplam Takipçi:"+endcolor+str(order)

#Can Is Proxy Update
proxy_option = raw_input(bold+green+"Proxy listesi güncellensin mi? (e/h): "+endcolor)
if proxy_option == "e":
	proxy_list = proxy_lists
	proxy_update()
else:
	proxy_list = proxy_data
print border_line_two

#Body Of Software
while True:
	command = raw_input(bold+yellow+"es@coderlab ~$ "+endcolor)
	if command.startswith("quit"):
		break
	elif command.startswith("help"):
		print border_line_one
		help()
		print border_line_one
	elif command.startswith("account_update"):
		print border_line_one
		filename = command[15:]
		account_update(filename)
		print border_line_one
	elif command.startswith("proxy_update"):
		print border_line_one
		proxy_update()
		print border_line_one
	elif command.startswith("show_accounts"):
		if "full" in command:
			show_accounts("full")
		elif "range" in command:
			rang = command[20:]
			rang = rang.partition(",")
			start, dott, finish = rang
			show_accounts("range", start, finish)
		else:
			print "Böyle bir hesap gösterim seçeneği bulunmamaktadır."
	elif command.startswith("show_proxy"):
		print border_line_one
		show_proxy()
		print border_line_one
	elif command.startswith("account_del"):
		if "full" in command:
			account_del("""DELETE FROM accounts""")
		elif "user" in command:
			userid = command[16:]
			account_del("""DELETE FROM accounts WHERE account_id == {}""".format(userid))
		elif "range" in command:
			rang = command[18:]
			rang = rang.partition(",")
			start, dott, finish = rang
			account_del("""DELETE FROM accounts WHERE account_id BETWEEN {} and {}""".format(start, finish))
		else:
			print "Böyle bir hesap silme seçeneği bulunmamaktadır."
	elif command.startswith("follow_bot"):
		nickname = command[11:]
		print border_line_one
		follow_bot(nickname)
		print border_line_one
	else:
		print bold+red+"Böyle bir komut bulunmamakta!"+endcolor+" "+command
