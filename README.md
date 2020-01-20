#### Description
Terms of Services handling mechanism implemented in Django.   

#### Features
* Multiple terms of services allowed(via slug field -> version number).  
* Per user terms of services acceptance.  
* Keeping user profile data state after accepting terms of services.  
* Activate tos in future date.
* Enable/disable tos using status property in admin. 
* Good admin site to manage terms of services.
* Simple decorator to use with DRF ModelViewSet action methods(list, retrieve, create, update, delete). 
If there are any pending tos then it redirects to tos listing page if request is text/html. 
If request is application/json then it redirects to tos listing json api.  
* Api for listing all pending tos. if content-type is text/html then renders html page which list all pending tos 
with a button to accept them, if content-type is application/json then returns list of pending tos. 
* Api for accepting all pending tos.
* Configured well for both content-type of text/html and application/json requests.  
* Enabled redis cache to store user's pending tos which invalidates every 120 seconds.  

#### Screenshot  
![pending tos list](demo.png)


#### requirements.txt
Developed using Python 3.7.5  
* asgiref==3.2.3  
* Django==3.0.2  
* django-environ==0.4.5  
* django-filter==2.2.0  
* django-redis==4.11.0  
* djangorestframework==3.11.0  
* psycopg2-binary==2.8.4  
* pytz==2019.3  
* redis==3.3.11  
* sqlparse==0.3.0  

		
#### Setup  & Run  
* docker-compose -f docker-compose.yml -f docker-compose-dev.yml up  
* docker-compose exec web python manage.py createsuperuser 
      
#### Test  
* Enter to admin site `http://127.0.0.1:8000/api_doc/` and 
create few terms of services with `activation date` less than now and `status` active.
* Hit in browser(text/html) `http://127.0.0.1:8000/tos/v1/terms_of_services/pending_terms/`  -  will show page with 
all pending tos, if you accept then it will redirect you to again pending tos page showing that no more tos to accept.    
* Hit in postman(application/json) `http://127.0.0.1:8000/tos/v1/terms_of_services/pending_terms/`  -  will show json list of all pending tos.  
* Post api for accepting all tos : `http://127.0.0.1:8000/tos/v1/terms_of_services/accept_terms/`  
Post data format :  
```json
{
  "tos-1": 5,
  "tos-2": 8
}
```
##### decorator test  
* I added a ModelViewSet  for testing UserProfile data and used `pending_terms` decorator for retrieve action.
Hit in browser `http://127.0.0.1:8000/api/v1/user_profile/1/` - will redirect you to pending tos page. Hitting api 
with application/json will list json of all pending tos. Redirection to original request yet to implement.  


####  TODO  
* Need to write tests extensively.  
* Write openapi swagger for testing api.  
* If user make json request and has few tos to accept, now it redirects to pending tos api. 
Find better way to distinguish response either it requested response or pending tos list.
* Add redirection to original request after accepting pending tos for text/html request.  
* Now decorator tested with ModelViewSet action methods but need to test with 
regular function based views.
		


