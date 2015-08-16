import requests, json
import urllib, cStringIO
from PIL import Image

API_KEY = 'dc6zaTOxFJmzC'
API_ENDPOINT = 'http://api.giphy.com/v1/gifs/search'

def gif_search(search_text):
	try:
		mod = search_text.split()
		query = ''

		for block in mod:
			query += block
			query += '+'

		params = dict(
			q = query[:-1],
			api_key = API_KEY
		)

		res = requests.get(url=API_ENDPOINT, params=params)

		data = json.loads(res.text)
		#print data['data'][0]['images']['original']['url']
		return data
	except:
		print 'error in image factory'

def query_concatenate(a, b):
	return a + '&' + b

def main():
	while True:
		try:
			query = raw_input('type!')

			result = gif_search(query)
			print result

			file = cStringIO.StringIO(urllib.urlopen(result).read())
			img = Image.open(file)
			img.show()
		except:
			pass
			#print 'fuck you'

if __name__ == '__main__':
	main()



	# http://api.giphy.com/v1/gifs/search?q=funny+cat&api_key=dc6zaTOxFJmzC