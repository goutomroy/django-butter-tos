#### Description
Terms of Services handling mechanism implemented in Django.   

#### Features
* Multiple terms of services allowed(via slug field -> version number).  
* Per user terms of services acceptance.  
* Keeping user profile data state after accepting terms of services.  
* Activate tos in future date.
* Enable/disable tos using status property in admin. 
* Good admin site to manage terms of services.

* Api (`/tos/v1/terms_of_services/`) for listing all pending tos. 
if content-type is `text/html` then renders html page which lists all pending tos 
with a button to accept them, if content-type is `application/json` then returns list of pending tos. 

* Simple decorator(`@terms_checker`) to use with DRF ModelViewSet action methods(list, retrieve, create, update, delete). 
If there is any pending tos then it sends status code 302, check `location` header for redirection url, 
for this case its `/tos/v1/terms_of_services/`. Automatic redirection will happen if its enabled in client.
In browser and postman its enabled by default. You can switch off to get status code 302, its useful when you are 
requesting from mobile app. Decorator works with only `safe methods`(get, head, options).

* Apis and decorator works only for authenticated user.
* Redirection to original request after accepting pending tos for text/html request.
* Api for accepting all pending tos.
* Configured well for both content-type of text/html and application/json requests.  
* Enabled redis cache to store user's pending tos list which invalidates every 120 seconds.  

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

		
#### Setup & Run  
* Create and paste `app.env` file to project folder as in manage.py. `app.env` format :  

```editorconfig
DEBUG=True
SECRET_KEY=(=fdfs7hp^n=*6jan*%2dfabww1#pud3!9swg&ojq3&uy411
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:pass@postgres/butter_tos
REDIS_URL=rediscache://redis/1
```

* docker-compose -f docker-compose.yml -f docker-compose-dev.yml up  
* docker-compose exec web python manage.py createsuperuser 
      
#### Test  
* Enter to admin site `http://127.0.0.1:8000/api_doc/` and 
create few terms of services with `activation date` less than now and `status` active.
* Hit in browser(text/html) `http://127.0.0.1:8000/tos/v1/terms_of_services/`  -  will show page with 
all pending tos, if you accept then it will redirect you again to pending tos page showing that no more tos to accept.    
* Hit in postman(application/json) `http://127.0.0.1:8000/tos/v1/terms_of_services/pending_terms/`  -  will show 
json list of all pending tos.  
* Post api for accepting all tos : `http://127.0.0.1:8000/tos/v1/terms_of_services/accept_terms/`  
Post data format :  
```json
{
  "tos-1": 5,
  "tos-2": 8
}
```
##### Decorator test  
* I have added a ModelViewSet  for testing UserProfile data and used `pending_terms` decorator for retrieve action.
Hit in browser `http://127.0.0.1:8000/api/v1/user_profile/1/` - will redirect you to pending tos page if there 
is any pending tos for user. Hitting api with `application/json` will give `302` with `location` header if there 
is any pending tos for user.  

##### Decorator use 

```python
class UserProfileViewSet(viewsets.ModelViewSet):

    @terms_checker
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @terms_checker
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @terms_checker
    @action(methods=['get'], detail=False)
    def email_list(self, request):
        ...
```
####  TODO  
* Need to write tests extensively.  
* Write openapi swagger for testing api.
* Now decorator tested with ModelViewSet action methods but need to test with 
regular function based views.
		


