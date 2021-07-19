## Requirements

Install the requirements.

```
pip install -r requirementstxt 
```
## Tests

Make sure the tests pass:
```
pytest test.py
```

## Start Service
```
run app.py
```

## Remarks
```
For the advanced requirements, I only implemented find nearby user function.
The api route and the function is:

@app.route('/api/v0.0/nearby/<string:user_name>',methods=['GET'])
def get_nearby(user_name):

Sorry for not sufficient time for implementing the rest.
```