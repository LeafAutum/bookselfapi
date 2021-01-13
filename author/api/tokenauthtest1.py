import requests

def client():
    Token_auth ='Token e0dd21eb98cb565f49812a09ca4fa58f7e0980b3'
    # credentials = {"username": "cha", "password":"priyanka1"}

    # response= requests.post("http://127.0.0.1:8000/api/rest-auth/login/", data =credentials)

    headers = {"Authorization": Token_auth }
    response =  requests.get("http://127.0.0.1:8000/api/Profileslist/", headers=headers)
    print("response status",response.status_code)
    response_data =response.json()
    print(response_data)


if __name__== "__main__":    
     client()
    