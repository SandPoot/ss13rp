import pypresence
import time
import win32gui
import win32process
import psutil
import sys
import util
import requests
import time
from config import *
import webbrowser

if "join" in sys.argv:
	print("joining game...")
	def join(ev):
		ie = webbrowser.get(webbrowser.BackgroundBrowser)
		ie.open('') #py 3.6 breaks this
	rp = pypresence.Client(client_id)
	rp.start()
	print(rp.read())
	rp.register_event("ACTIVITY_JOIN", join)
	rp.loop.run_forever()

else:
	while True:
		try:
			rp = pypresence.Client(client_id)
			rp.start()
			break
		except:
			time.sleep(15)

	def get_hwnds_for_pid (pid):
		def callback (hwnd, hwnds):
			if win32gui.IsWindowVisible (hwnd) and win32gui.IsWindowEnabled (hwnd):
				_, found_pid = win32process.GetWindowThreadProcessId (hwnd)
				if found_pid == pid:
					hwnds.append (hwnd)
			return True
		hwnds = []
		win32gui.EnumWindows (callback, hwnds)
		return hwnds

	def get_server():
		p = [proc for proc in psutil.process_iter() if proc.name() == "dreamseeker.exe"]
		p = p[0]

		windows=get_hwnds_for_pid(p.pid)
		windowtitles = [i for i in [str(win32gui.GetWindowText(item))
						for item in windows] if i != ""]
		for title in windowtitles:
			if not title == "Space Station 13":
				for i in servers.keys():
					if title.startswith(i):
						return servers[i]
			else:
				server = "ss13"
				return servers[server]

	def get_content(entry, else_value = ""):
		if entry in status and status[entry]:
			return status[entry]
		else:
			return else_value if else_value else ""

	while True:
		try:
			server = get_server()
			activity = {"large_text": server[0], "large_image":server[1], "details": server[0]}
			if len(server) >= 5:
				try:
					if server[4] == "fetch":
						status = util.fetch(server[2], server[3], "status")
					elif server[4] == "http":
						status = requests.get(server[2]).json()

					print(status)

					if server[0] in ["Citadel Station", "Transcendent Enemy", "Sandstorm Station 13", "Hyper Station 13", "Nostra-13", "Maconha Station 13", "Shiptest", "T.E. TGMC PvE"]:
						activity["start"] = int(time.time())-int(status["round_duration"])

						map = get_content("map_name", "No Map")
						activity["party_id"] = str(get_content("round_id")) + " " + map #apparently terry has NO revision

						mode = get_content("mode", "dynamic")
						activity["state"] = map + ", " + mode
						activity["buttons"] = [{"label": "Join", "url": "byond://" + server[2] + ":" + str(server[3])}]

						popcap = get_content("popcap", "120")
						popcap = "120" if(int(popcap) <= 0) else popcap
						activity["party_size"] = [int(get_content("players"))] + [int(popcap)]

					#if server[0] in ["Colonial Marines"]:
					#    activity["state"] = status["mode"]
					#    activity["party_size"] = [int(status["players"])]+[300]
					#    activity["start"] = int(time.time())-util.get_sec(*status["stationtime"].split(":"))


					#if server[0] in ["Baystation 12"]:
					#    activity["state"] = status["map"]
					#    activity["party_size"] = [int(status["players"])]+[100]
					#    activity["start"] = int(time.time())-util.get_sec(*status["roundduration"].split(":"))

					#if server[0] in ["Paradise Station"]:
					#    activity["state"] = status["map_name"]
					#    activity["party_size"] = [int(status["players"])]+[250]
					#    activity["start"] = int(time.time())-util.get_sec(*status["roundtime"].split(":"))


					#if server[0].startswith("Goonstation"):
					#    activity["state"] = status["map_name"]#+", "+status["mode"]
					#    activity["party_size"] = [int(status["players"])]+[200]
					#    activity["start"] = int(time.time())-int(status["elapsed"])

				except Exception as E:
					print(E)
					pass

			rp.set_activity(**activity)
			time.sleep(15)

		except Exception as e:
			time.sleep(10)
			try:
				rp.clear_activity()
				time.sleep(5)
			except Exception as e:
				while True:
					try:
						rp = pypresence.Client(client_id)
						rp.start()
						break
					except:
						time.sleep(20)
