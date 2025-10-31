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

## POST Route: /api/v1/courses/

Request Body: {
  "name": "string"
}

Response: {
  "name": "string",
  "id": 1
}

## GET Route: /api/v1/courses/ 

Response: [
  {
    "name": "string",
    "id": 1
  }
]

## GET Route: /api/v1/courses/1 

Parameters: course_id 

Response: {
  "name": "string",
  "id": 1
}

## PUT Route: /api/v1/courses/1 

Parameters: course_id 

Body: {
  "name": "updated_string"
}

Response: {
  "name": "updated_string",
  "id": 1
}

## GET Route: /api/v1/courses/1/tutor-sessions 

Parameters: course_id 

Response: [
  {
    "title": "string",
    "id": 0,
    "course_name": "string",
    "chat_messages": [
      {
        "role": "user",
        "message": "string",
        "id": 0,
        "tutor_session_title": "string",
        "created_at": "2025-10-31T02:59:49.339Z"
      }
    ],
    "created_at": "2025-10-31T02:59:49.339Z"
  }
]

## DELETE Route: /api/v1/courses/1

Parameters: course_id 

Response: null 
