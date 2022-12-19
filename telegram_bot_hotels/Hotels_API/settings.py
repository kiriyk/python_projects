url_loc = "https://hotels4.p.rapidapi.com/locations/v2/search"
url_hotels = 'https://hotels4.p.rapidapi.com/properties/list'
url_photo = 'https://hotels4.p.rapidapi.com/properties/get-hotel-photos'

QUERYSTRING = {"query": "new york", "locale": "ru_RU", "currency": "RUB"}

HEADERS = {
	"X-RapidAPI-Host": "hotels4.p.rapidapi.com",
	"X-RapidAPI-Key": "key"
}

BASE_REQUEST = {
	"destinationId": "1506246",
	"pageNumber": "1",
	"pageSize": "5",
	"adults1": "1",
	"sortOrder": "PRICE",
	"locale": "en_US",
	"currency": "RUB"
}

_MAX_PHOTO_NUMBER = 10
_MAX_HOTELS_NUMBER = 7
