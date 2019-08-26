import requests
from bs4 import BeautifulSoup

headers = requests.utils.default_headers()

headers.update( {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'})
url = 'https://www.redfin.com/city/29470/IL/Chicago/recently-sold'
#url can change based on user's input, for now this code is parsing through all the avaliable homes in Chicago

counter = 1;
#Counter and while loop is in place if user wants to scrap the remaining pages 
#of the recently sold homes, this code only scraps the first page's house data
while True:
	link = requests.get(url, headers=headers)
	soup = BeautifulSoup(link.content, "lxml")

	for match in soup.find_all('a', class_='bottom link-override'):
		
		#Relevant details I think are essential is address, price, city, zip code,
		#state, number of beds, baths, and total square feet
		type_house = match.find('div', class_='HomeStats font-size-smaller')
		price = match.find('span', class_='homecardPrice font-size-small font-weight-bold').text
		address = match.find('div', class_='addressDisplay font-size-smaller')
		street_name = address.find('span').text
		zip_city = address.find('span', class_='cityStateZip')

		#Code below strips any unnecessary characters to make output more
		#presentable
		city = ''
		state = ''
		zip_code = ''
		comma = True
		space = 0
		for word in zip_city.text:
			if comma == True:
				if word != ',':
					city += word
				else:
					comma = False
			else:
				if word != ' ' and space == 1:
					state += word
				elif word != ' ' and space == 2:
					zip_code += word
				elif word == ' ':
					space+= 1

		print("Address: " + street_name)
		print(" Price: " + price)
		print(" City: " + city)
		print(" State: " + state)
		print(" Zip Code: " + zip_code)

		#Parses to find the number of beds, baths, and square feet for output
		type_house_counter = 0
		for values in type_house.find_all('div', class_='value'):
			if type_house_counter == 0:
				print(" Beds: " + values.text),
				
			elif type_house_counter == 1:
				print(" Baths: " + values.text),
				
			elif type_house_counter == 2:
				print(" Square Feet: " + values.text),
			type_house_counter+=1

		print('\n')

	
	page = soup.find('link', rel="next")
	page_next = (page.get('href'))

	for tag in soup.find_all('meta'):
		if tag.get("name", None) == "HOME_URL":
			start_page = tag.get("content", None)

	max_counter = 0
	for max_num in soup.find_all('a', class_= "clickable goToPage"):
		if int(max_num.get_text()) > max_counter:
			max_counter = int(max_num.get_text())

	#start_page and page_next is made just in case user wants to continue
	#scrapping the rest of the pages.  For example, recently sold homes in 
	#Chicago has a total of 18 pages, this code only parses through one.  
	#This code now contains the url for the second page, and has the total
	#number of pages, which is 18.  If a user wants to parse through all of 
	#the pages, I would change the while loop condition to stop after 
	#18 iterations, and replace the url with the next page's url
	url = start_page + page_next
	break