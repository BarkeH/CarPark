import requests

response = requests.post("http://0.0.0.0:5000/api/payment", 
        data = {'cardNumber':12345678,
            'cvv':123,
            'price':10})
print(response.text)
