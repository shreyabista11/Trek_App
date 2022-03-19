# trek_app
##This app contains REST API.
REST APIs have functionalities to add trek destination,get trek destinations,update trek destination and delete trek destination.

1) POST a trek destination:This adds a trek destination:</br>
  -URL:</br>
    http://127.0.0.1:5000/rest/treks</br>
  -URL endpoint:</br>
    /rest/treks </br>
  -Method:</br>
    POST </br>
  -Parameters: </br>
    title:required:text:title of trek destination </br>
    days:required:number:days required to complete trek destination </br>
    difficulty:required:text:difficulty level of trek destination </br>
    total_cost:required:number:total cost of trek destination </br>
    token:required:text: token of logged in user </br>
    
   -Payload{ </br>
    "title":"sikles trek", </br>
    "days":5, </br>
    "difficulty":"level 1", </br>
    "total_cost":20000, </br>
    "token":"6e13ac4a-eafd-4d55-8d21-0efba897be2e" </br>
      } </br>
    -Response: </br>
      message:a message after adding of trek destination is attempted </br>
      E.g. -on successful response 200 OK </br>
      if adding of trek destination is successful: </br>
     {
        "message": "Trek has been added Successfully" 
      } </br>
      OR. </br>
      if entered token is invalid/user is not authenticated: </br>
      { </br>
        "message": "Please enter a valid token" </br>
      } </br>
   
      
    
      
2)GET all treks-this gets all treks from database </br>
  -URL: </br>
    http://127.0.0.1:5000/rest/treks </br>
  -URL endpoint: </br>
    /rest/treks </br>
  -Method: </br>
    GET </br>
  -Parameters: </br>
    No parameteres required as input. </br>
    
  
  -Response: </br>
      logged_in_user:this returns if the request is sent by a logged in user or not ,returns NULL if user is not a logged in user. </br>
      treks:This returns treks list which contains trekId, title of trek,days of trek, difficulty level of trek,total cost of trek,upvotes of trek and fullname of user who added              trek </br>
      
   -E.g. -on successful response 200 OK </br>
      Payload </br>
      { </br>
        "logged_in_user": null, </br>
        "treks": [ </br>
            [
                3,
                "Phoksundo Trek",
                11,
                "level 4",
                24000,
                23,
                "Jyoti Adhikari"
            ],
            [
                4,
                "Khaptad trip",
                20,
                "level 4",
                20000,
                23,
                "Bigyan Rijal"
            ]</br>

  ]</br>
}</br>

3)UPDATE - to update a trek destination </br>
  -URL: </br>
    http://127.0.0.1:5000/rest/treks </br>
  -URL endpoint:</br>
    /rest/treks </br>
  -Method: </br>
    PUT </br>
  -Parameters: </br>
    trekId:required:number:id of trek destination </br>
    title:required:text:title of trek destination </br>
    days:required:number:days required to complete trek destination </br>
    difficulty:required:text:difficulty level of trek destination </br>
    total_cost:required:number:total cost of trek destination </br>
    token:required:text: token of logged in user </br>
    
   -Payload </br>
    { </br>
    "trekId":12,
    "title":"tilicho lake trek",
    "days":5,
    "difficulty":"level 1",
    "total_cost":15000,
    "token":"6e13ac4a-eafd-4d55-8d21-0efba897be2e"
    } </br>
    -Response: </br>
      message:a message after updating of trek destination is attempted </br>
     e.g: </br>
     >if updating of trek destination is successful: </br>
     {
        "message": "Trek has been updated Successfully" </br>
      } </br>
      OR. </br>
      >if entered token is invalid/user is not authenticated: </br>
      { </br>
        "message": "Please enter a valid token" </br>
      } </br>
      OR. </br>
      ->if user tries to update trek destination using someone else's token </br>
      { </br>
         "message": "you cannot update someone else's trek" </br>
      } </br>
      
4)DELETE - to delete a trek destination </br>
  -URL: </br>
    http://127.0.0.1:5000/rest/treks </br>
  -URL endpoint: </br>
    /rest/treks </br>
  -Method: </br>
    DELETE </br>
  -Parameters: </br>
    trekId:required:number:id of trek destination </br>
    token:required:text: token of logged in user </br>
    
   -Payload </br>
    { </br>
    "trekId":12, </br>
    "token":"6e13ac4a-eafd-4d55-8d21-0efba897be2e" </br>
    } </br>
    -Response: </br>
      message:a message after deleting of a trek destination is attempted </br>
     e.g: </br>
     >if updating of trek destination is successful: </br>
     { </br>
        "message": "Trek has been deleted Successfully" </br>
      } </br>
      OR. </br>
      >if entered token is invalid/user is not authenticated: </br>
      { </br>
        "message": "Please enter a valid token" </br>
      } </br>
      OR. </br>
      ->if user tries to delete trek destination using someone else's token </br>
      { </br>
         "message": "you cannot delete someone else's trek" </br>
      } </br>

      
    
  
    
