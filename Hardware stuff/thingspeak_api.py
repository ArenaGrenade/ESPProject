import sys
import requests

# clear the channel feed
req = requests.delete('https://api.thingspeak.com/channels/1567627/feeds.json?api_key=6VPR0L04PHIOJGCH')

# get the channel feed
# count = 20
# req = requests.get('https://api.thingspeak.com/channels/1501117/feeds.json?api_key=AN6HKHWJNLPWQFDG&results={}'.format(count))

# # printing the channel feed
# data = req.json()['feeds']
# for i in range(len(data)):
# 	print("ID:", data[i]['entry_id'], " Temperature:",data[i]['field1'], " Humidity:", data[i]['field2'], " Heat Index:", data[i]['field3'])