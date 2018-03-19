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
			staticimg = Image.open('staticimages/1N.ppm')
			draw = ImageDraw.Draw(staticimg)
			font = ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf', 12)
			# font = ImageFont.truetype('/Library/Fonts/Arial.ttf', 10)
			draw.text((16, 1), train_times, fill=(255,255,255), font=font)
			staticimg.save('dynamicimages/dynamictime.ppm')
			departure_times = []
			train_times = ''

			os.system('sudo ./rpi-rgb-led-matrix/examples-api-use/demo --led-chain=4 -D 1 -m 5000 dynamicimages/dynamictime.ppm --led-no-hardware-pulse --led-gpio-mapping=adafruit-hat')
	except Exception:
		print traceback.format_exc()








