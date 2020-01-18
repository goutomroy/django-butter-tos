#### Description

* Please do not spend more than 8 hours working on the task. 
* You should implement as much as you can in the given time frame 
while keeping the quality of your work high and production-ready. 
* Please provide all the important info in the Readme file.
* Your task is to implement the backend (and only backend, no frontend) to allow users 
to sign the agreement for the Terms of Services. 
* Store information about when an agreement was signed and what the user data was 
at that point (first_name, last_name, street, post_code).
* If any of the user data changes there should be no changes to the agreement. 
* If the agreement template changes, the agreements already signed should remain unchanged. 
* There should be an API to fetch the agreement for a user (html) 
* When coding think of usage scope for this functionality 1 user per minute so try to optimize disc space taken in long run).


Example agreement template:

```
<div style="font-size: 20px; text-align: center;">
    <p>Some agreement template</p>
    <p style="font-size: 15px;">
        {{first_name}} - {{last_name}}
    </p>
    <p>
        {{street}} - {{post_code}}
    </p>
    <p style="font-size: 15px;">
        Dated: {{date}}
    </p>
</div>
```

The requirements are:
* It should be restful
* Provide git repository
* Add basic docker configuration
* This is part of a bigger (monolith) system
* Implement in django and django rest framework
* Please treat this exercise as if you were writing production-quality code that you’d be proud of.
* Once you are done please push the code into your favourite online repository and share it with us. 
* We recommend that you commit early and often into your repository.
* We would expect the exercise to be completed by Tuesday 21st January.

		
#### Setup  & Run  
* docker-compose up
* docker-compose -f docker-compose.yml -f docker-compose-dev.yml up  
* docker-compose -f docker-compose.yml -f docker-compose-prod.yml up  
* docker-compose exec web python manage.py createsuperuser 
      
#### Api Documentation  
*  I used OpenAPI Specification v2 which tells exactly what each api can do and also can execute the request.  
*  Enter to admin site.  
*  Check `http://127.0.0.1:8000/api_doc/`    

####  TODO  
* Need to write tests extensively.  
		


