# Authentication

!!!info
    For API overview and usages, check out [this page](0-overview.md).

## Login

```
POST /api/auth/login
```

__Parameters__

Name     | Description
---------|-------------------------------------
email    | email of the user. 
password | password of the user.

__Request__
```json
{
    "email": "hello@example.com",
    "password": "VerySafePassword0909"
}
```

__Response__
```json

Status: 200 OK
{
    "auth_token": "eyJ0eXAiOiJKV1QiL",
    "email": "ak123@emaple.com",
    "id": "f9dceed1-0f19-49f4-a874-0c2e131abf79",
    "first_name": "",
    "last_name": ""
}
```


## Register

```
POST /api/auth/register
```

__Parameters__

| Name       | Description                                                |
| ---------- | ---------------------------------------------------------- |
| email      | email of the user. Errors out if email already registered. |
| password   | password of the user.                                      |
| first_name | first name of the user.                                    |
| last_name  | last name of the user.                                     |

**Request**

```json
{
  "email": "hello@example.com",
  "password": "VerySafePassword0909",
  "first_name": "S",
  "last_name": "K"
}
```

__Response__

```json

Status: 201 Created
{
    "auth_token": "eyJ0eXAiOiJKV1QiLCJh",
    "email": "test@test.com",
    "id": "f9dceed1-0f19-49f4-a874-0c2e131abf79",
    "first_name": "S",
    "last_name": "K"
}
```

## Change password

```
POST /api/auth/password_change (requires authentication)
```

__Parameters__

Name             | Description
-----------------|-------------------------------------
current_password | Current password of the user.
new_password     | New password of the user.

__Request__
```json
{
    "current_password": "NotSoSafePassword",
    "new_password": "VerySafePassword0909"
}
```

__Response__
```
Status: 204 No-Content
```


## Request password for reset

Send an email to user if the email exist.

```
POST /api/auth/password_reset
```

__Parameters__

Name  | Description
------|-------------------------------------
email | (required) valid email of an existing user.

__Request__
```json
{
    "email": "hello@example.com"
}
```

__Response__
```json

Status: 200 OK
{
    "message": "Further instructions will be sent to the email if it exists"
}
```


## Confirm password reset

Confirm password reset for the user using the token sent in email.

```
POST /api/auth/password_reset_confirm
```

__Parameters__

Name          | Description
--------------|-------------------------------------
new_password  | New password of the user
token         | Token decoded from the url (verification link)


__Request__
```json
{
    "new_password": "new_pass",
    "token" : "IgotTHISfromTHEverificationLINKinEmail"
}
```

__Response__
```
Status: 204 No-Content
```

!!!Note
    The verification link uses the format of key `password-confirm` in `FRONTEND_URLS` dict in settings/common.
