from PIL import Image, ImageFont, ImageDraw
from google.transit import gtfs_realtime_pb2
import nyct_subway_pb2
import urllib
import datetime
import math
import os
from config import *
import traceback

departure_times = []
train_times = ''

while True:

	try:
		mtafeed = gtfs_realtime_pb2.FeedMessage()
		response = urllib.urlopen('http://datamine.mta.info/mta_esi.php?key=' + MTA_KEY + '&feed_id=21')
		test = mtafeed.ParseFromString(response.read())
		current_time = datetime.datetime.now()
		for stop in STOP_IDS:
			for entity in mtafeed.entity:
				if entity.trip_update:
					for update in entity.trip_update.stop_time_update:
						if update.stop_id == stop:
							departure_time = update.departure.time
							departure_time = datetime.datetime.fromtimestamp(departure_time)
							departure_time = math.trunc(((departure_time - current_time).total_seconds()) / 60)
							departure_times.append("%s min" % departure_time)
			departure_times.sort()
			for time in departure_times:
				if time < 0:
					departure_times.remove(time)
			for time in departure_times[:NUM_TRAINS]:
				train_times+=str(time)
				train_times+=str(',')
			train_times = train_times[:-1]

			# staticimg = Image.open('staticimages/' + stop[0] + stop[3] + '.ppm')
			staticimg = Image.open('staticimages/F+G-train-w-background-black.ppm')
			draw = ImageDraw.Draw(staticimg)
			title_font = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf', 9)
			time_font = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf', 9)
			min_text_font = ImageFont.truetype('/usr/share/fonts/truetype/noto/NotoMono-Regular.ttf', 4)

			# font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 10)

			# F train
			# name of direction
			draw.text((20, 4), "Manhattan", fill=(255,255,255), font=title_font)
			# next train time
			draw.text((50, 4), train_times, fill=(255,255,255), font=time_font)
			# min
			draw.text((120, 4), "min", fill=(255,255,255), font=min_text_font)

			# G train
			# name of direction
			draw.text((20, 19), "Williamsburg", fill=(255,255,255), font=title_font)
			# next train time
			draw.text((50, 19), train_times, fill=(255,255,255), font=time_font)
			# min
			draw.text((120, 19), "min", fill=(255,255,255), font=min_text_font)

			staticimg.save('dynamicimages/dynamictime.ppm')
			departure_times = []
			train_times = ''

			os.system('sudo ./rpi-rgb-led-matrix/examples-api-use/demo --led-chain=4 -D 1 -m 99999999 dynamicimages/dynamictime.ppm --led-no-hardware-pulse --led-gpio-mapping=adafruit-hat')
	except Exception:
		print traceback.format_exc()
