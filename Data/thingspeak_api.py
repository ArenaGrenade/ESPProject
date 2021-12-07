import sys
import requests
import json

# clear the channel feed
req = requests.delete('https://api.thingspeak.com/channels/1567627/feeds.json?api_key=6VPR0L04PHIOJGCH')

# get the channel feed
# count = 100
# req = requests.get('https://api.thingspeak.com/channels/1567627/feeds.json?api_key=DVPEY4N0W239YFXN&results={}'.format(count))
# data = req.json()['feeds']
# with open('p6.json', 'w') as f:
# 	json.dump(data, f, indent=4)
# print(data)