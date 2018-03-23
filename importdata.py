from PIL import Image, ImageFont, ImageDraw
from google.transit import gtfs_realtime_pb2
import nyct_subway_pb2
import urllib
import datetime
import math
import os
from config import *
import traceback
import time
# use the import below for debugging this code
import code
# put this line anywhere you want to interact with your code via termainal:
# code.interact(local=dict(globals(), **locals()))

def get_train_times(feed_id, stop_id):
	departure_times = []
	train_times = []
	mtafeed = gtfs_realtime_pb2.FeedMessage()
	f_train_response = urllib.urlopen("http://datamine.mta.info/mta_esi.php?key=" + MTA_KEY + "&feed_id=" + feed_id)
	mtafeed.ParseFromString(f_train_response.read())
	current_time = datetime.datetime.now()

	for entity in mtafeed.entity:
		if entity.trip_update:
			for update in entity.trip_update.stop_time_update:
				if update.stop_id == stop_id:
					departure_time = update.departure.time
					departure_time = datetime.datetime.fromtimestamp(departure_time)
					departure_time = math.trunc(((departure_time - current_time).total_seconds()) / 60)
					departure_times.append(departure_time)
	departure_times.sort()
	for departure_time in departure_times:
		if departure_time < 0:
			departure_times.remove(departure_time)
	for departure_time in departure_times[:NUM_TRAINS]:
		train_times.append(departure_time)
	return train_times

def draw_sign(f_train_times, g_train_times, fontPath):
	# grab base image as base
	staticimg = Image.open("staticimages/F+G-train-w-background-black.ppm")
	draw = ImageDraw.Draw(staticimg)
	# create fonts
	title_font = ImageFont.truetype(fontPath, 9)
	time_font = ImageFont.truetype(fontPath, 9)
	second_train_font = ImageFont.truetype(fontPath, 7)
	# Write train time text
	# F train
	# ==========================
	# name of direction
	draw.text((20, 4), "Manhattan", fill=(255,255,255), font=title_font)
	# next train time
	draw.text((87, 4), str(f_train_times[0]), fill=(255,255,255), font=time_font)
	draw.text((99, 4), "min", fill=(255,255,255), font=time_font)
	# second train time
	draw.text((118, 2), str(f_train_times[1]), fill=(255,255,255), font=second_train_font)
	# G train
	# ==========================
	# name of direction
	draw.text((20, 19), "Williamsburg", fill=(255,255,255), font=title_font)
	# next train time
	draw.text((87, 19), str(g_train_times[0]), fill=(255,255,255), font=time_font)
	draw.text((99, 19), "min", fill=(255,255,255), font=time_font)
	# second train time
	draw.text((118, 17), str(g_train_times[1]), fill=(255,255,255), font=second_train_font)
	# create new image to display
	staticimg.save("dynamicimages/dynamictime.ppm")

while True:

	try:
		f_train_feed_id = "21"
		g_train_feed_id = "31"
		f_stop_id = "F24N"
		g_stop_id = "F24N"

		f_train_times = get_train_times(f_train_feed_id, f_stop_id)
		g_train_times = get_train_times(g_train_feed_id, g_stop_id)

		# use if on Mac
		# draw_sign(f_train_times, g_train_times, "/Library/Fonts/Arial.ttf")
		draw_sign(f_train_times, g_train_times, "/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf")

		os.system("sudo ./rpi-rgb-led-matrix/examples-api-use/demo --led-chain=4 -D 1 -t 1 -m 99999999 dynamicimages/dynamictime.ppm --led-no-hardware-pulse --led-gpio-mapping=adafruit-hat")
		time.sleep(30)

	except Exception:
		print traceback.format_exc()
