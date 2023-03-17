# Guide for Routes

## Users

- `/users/` - *Token required in header.*
    - GET - gets the info about the user.
    - POST - updates info about the user.

- `/users/login` - *Authorisation username and password in header.*
    - POST - gets the token for the user.

- `/users/register`
    - POST - registers a user. Request body must contain user details.

- `/users/friends` - *Token required in header.*
    - GET - gets info about all friends related to the user given their request token.

- `/users/friends/add` - *Token required in header.*
    - POST - initiates a friend request to the username specified in the request body.

- `/users/friends/accept` - *Token required in header.*
    - POST - accepts the friend request of a user. User-to-accept username must be in the request body.

- `/users/friends/remove` - *Token required in header.*
    - POST - removes the friend given their username.


## Users

| URL | Description | Method | Input Example | Response Example | Response Codes |
| --- | --- | --- | --- | --- | --- |
| `/users/<id>` | Gets the information about the user | GET | `X-Authorization: <Token>` | `{"id": <String>, "username": <String>, "name": <String>, "email": <String>, "created": <Timestamp>}` | 200 - OK<br/>400 - Error: Could not get the user information |
| `/users/<id>` | Updates the information about the user | PUT | Request Header:<br/>`X-Authorization: <Token>`<br/>Request Body:<br/>`{"username": <String>, "password": <String>, "name": <String>, "email": <String>}`<br/>*Note: Parameters can be optional* | 400:<br/>`{"invalid": ["username", "email"]}`<br/>*Note: Invalid array will contain parameter names which already exist in the database (e.g., already in use by another user)* | 200 - OK<br/>400 - Error: Could not update the user information |
| `/users/<id>` | Deletes the user | DELETE | Request Header:<br/>`X-Authorization: <Token>`<br/>Request Body:`{"username": <String>, "password": <String>}` |  | 200 - OK<br/>400 - Error: Could not delete the user |
| `/users/login` | Gets the user access token | POST | Request Body:<br/>`{"username": <String>, "password": <String>}` | 200 |
| `/users/register` | Create the user | POST | Request Body:<br/>`{"username": <String>, "password": <String>, "name": <String>, "email": <String>}` | 400:<br/>`{"invalid": ["username", "email"]}`<br/>*Note: Invalid array will contain parameter names which already exist in the database (e.g., already in use by another user)* | 200 - OK<br/>400 - Error: Could not create the user |

