

# Documentation on the app 

## Overview 
This is a little app that takes your input of meeting time ranges and simply checks against the google support holidays in your provided country and returns all non clashing provided time slots.


## Running the app 

This app is built yet locally and made as container images with docker compose, and it has hence abstracts environments’ conflicts. 

Ensure docker is installed Simply run 

	docker-compose up --build

To spin up the container, and boom!!, your app is running on port http://127.0.0.1:8000/api/schedules on  your local machine.

It takes a json format of the form:

	{
	"from": "2021-12-24T00:00:00Z",
	"to": "2021-12-26T00:00:00Z",
	"CC":"NG"} 

For the post request.
Kindly note the double quotes:

### Navigation

the API at endpoint http://127.0.0.1:8000/api/schedules supports both GET and POST via HTTP request or through the django in-browser API ui as described but for ease of third party usage i have a integrated a nice easy to play with swagger-UI at the endpoint http://127.0.0.1:8000/swagger-ui/ or http://127.0.0.1:8000/redoc for redoc documentation as well. do GET request of availabe holidays country at  http://127.0.0.1:8000/api/schedules/?cc=us , where cc is your country code

If you have many requests kindly wrapp in square brackets [] with comma separated. I have told this little boy to catch several types of inputs you throw at it and give you a nice response. Find fun in playing with this simple API. 

### The test suite

I did unittest on the app with several test cases. I created a small json file of a few time slots as payloads for the post requests To check against needed outputs. 

The “docker-compose up” earlier will spin up both the web and and the test but to run only the testing unit, kindly run :


	docker-compose up test 


And see how the test was evaluated on your console. And at anypoint you can run 

	docker-compose logs test 

	docker-compose logs web 

for the web process


### the data folder	

check the inputs.json in the data folder in the root directory to play around with these inputs. Alongside is holidays.json both for unittesting make sure these files are not edited in this folder so unit test cases will not assert wrong. You can copy them out though. The dumpdata.json inside is the dummy data from the api holidays saved for reference purpose as it can use for deletion retrieving 

## Implementation choice:

Efficiency and speed is always our topic in api building. The google url provided doesn’t provide an API endpoint for json response of the holidays so i have to webscrape the contents and this information are wrapped inside html containers which might change anytime so i have to save these items in our database as we won’t as well want to web scrape a third party url on every user request. So I choose saving to database to enhance speed, then rather work on database request efficiency instead of a third party endpoint we have no opinion on.

Most requests from a single country will be almost the same as people from a country will share the same holidays hence this app is a good candidate for db caching of which i’ll use django memcache or redis in the future.

And also while i was implementing the view request logic i took into consideration the speed of our algorithm, i query the holiday table by filter on the given time slot to return false if exist and hence render such slot as invalid. I also checked against weekends if not clashing or otherwise rendered invalid

The web rapping is in the root directory i used beautiful soup to achieve this task

### BONUS (GET REQUEST):
The api support GET requests kindly provide a query parameter cc: as your country code to view all available holidays corresponding to specific country. E.g cc:us is for the United states while cc:ng is for Nigeria ect.. i.e http://127.0.0.1:8000/api/schedules/?cc=us  .

### -
incase of any complaints of further upgrade, contact the developer @mallamsiddiq@gmail.com


thanks .

#### akinyemi sodiq



