import os


MTA_KEY = os.environ["MTA_API_KEY"] #obtain one at http://web.mta.info/developers/developer-data-terms.html
NUM_TRAINS = 3  #the number of trains to display for each station/direction combination
STOP_IDS = ['230N', '419N', '230S']  #an array of stations/directions that you would like displayed. Find these in the stations file in staticdata
