# All Testing has been done using the swagger docs once running the fastapi server

# User

## Route: /api/v1/user/register

Body: {
"email": "yourGmailToGiveAccessTo@gmail.com",
"password": "123"
}

Response: A google auth redirect uri

## Route: /api/v1/user/auth/google/callback

Body: {
authCode: automatically called & created when using register
}

Response: {
"message": "OAuth signup successful!",
"access_token": "ya29.0206",
"refresh_token": "1//01fZwj5OG3HYcCgYIARAAEJ-2fL2-RdAC34qvZX1fNm-TDx1Xg",
"expiry": "2025-10-31T00:03:46",
"email": "aronsanchez038@gmail.com"
}

## Route: /api/v1/user/login

Body: urlformEncoded - userName:'signedupEmail@gmail.com' Password:'pass'

Response: {
"access_token": FHaA",
"token_type": "bearer"
}

## Route: /api/v1/user/me

Body: Recieves JWT Token in header

Response: {
"email": "gmail@gmail.com",
"id": 2
}

## Route: /api/v1/user/token

Body: Recieves JWT Token in header

Response: {
"access_token": "ya29.Dx1Xg",
"expiry": "2025-10-31T00:03:46"
}

# Course

## Route: /api/v1/courses/

Body: JWT Token in header

Response: {
[
{
"name": "cs-450",
"id": 1
}
] or []
}

## Route:
