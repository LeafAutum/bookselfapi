import requests

def client():
   
    data = {"username": "test2", 
            "email" : "test2@gmail.com",
            "password1":"chaeunlee",
            "password2":"chaeunlee",
            }

    response= requests.post("http://127.0.0.1:8000/api/rest-auth/registration/", data =data)
    Token_auth ='Token e0dd21eb98cb565f49812a09ca4fa58f7e0980b3'

    # headers = {"Authorization": Token_auth }
    # response =  requests.get("http://127.0.0.1:8000/api/Profileslist/", headers=headers)
    print("response status",response.status_code)
    response_data =response.json()
    print(response_data)


if __name__== "__main__":    
     client()
    