#### Description
Terms of Services handling mechanism implemented in Django.   

#### Features
* Multiple terms of services allowed(via slug field -> version number).  
* Per user terms of services acceptance.  
* Keeping user profile data state after accepting terms of services.  
* Activate tos in future date.
* Enable/disable tos using status property in admin. 
* Good admin site to manage terms of services.
* Decorator(`@terms_checker`) to enable terms and services to your site.
* Middleware(`TermsMiddleware`) to enable terms and services to your site.
* Api (`/tos/v1/terms_of_services/`) for listing all pending tos.
* Api for accepting all pending tos.
* Redirection to original request after accepting pending tos.
* Works well for both content-type of text/html and application/json requests.  
* Enabled redis cache to store user's pending tos list which invalidates every `TERMS_CACHE_SECONDS` seconds. 
 

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

#### Settings

* `TERMS_PROTECTED_PATH` - list of path you want to protect from being checked for pending tos. 
It uses python's `startswith` to exclude requested path. `Default` is []. ['/admin/', '/tos/'] will be added implicitly.

* `DEFAULT_TERMS_SLUG` - default slug to use when creating tos in admin. `Default` is `"butter-tos"`.

* `TERMS_CACHE_SECONDS` - number of seconds to to store user's pending tos. `Default` is `60`.

#### Available apis
* Api (`/tos/v1/terms_of_services/`) for listing all pending tos.
* Post api(`/tos/v1/terms_of_services/accept_terms/`) for accepting all tos.
Post data format :  
```json
{
  "tos-1": 5,
  "tos-2": 8
}
```


#### Use of Decorator 

* Use decorator(`@terms_checker`) to any view methods. 
* Decorator(`@terms_checker`) works only for authenticated user. 
* Decorator works with only `safe methods`(get, head, options).
* If there is any pending tos then it sends status code 302, check `location` header for redirection 
url(`/tos/v1/terms_of_services/?next=/requested_url/?param=any`)

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

#### Use of Middleware 

* Middleware(`TermsMiddleware`) works only if `django.contrib.auth.middleware.AuthenticationMiddleware` is 
added in `MIDDLEWARE` 
* Middleware(`TermsMiddleware`) works with only `safe methods`(get, head, options).
* If there is any pending tos then it sends status code 302, check `location` header for redirection 
url(`/tos/v1/terms_of_services/?next=/requested_url/?param=any`)
* To use Middleware add `apps.tos.middleware.TermsMiddleware` to settings MIDDLEWARE list. It should be added after 
`django.contrib.auth.middleware.AuthenticationMiddleware` and before `django.middleware.gzip.GZipMiddleware`.  


#### Visualize that its working  
* Enter to admin site `http://127.0.0.1:8000/admin/` and 
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


####  TODO  
* Need to write tests extensively.  
* Write openapi swagger for testing api.
		


