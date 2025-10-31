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

# Files 

## POST Route: /api/v1/files/ 

Body: {
  "name": "string",
  "google_drive_id": "string",
  "course_id": 1
}

Response: {
  "id": 2,
  "name": "string",
  "google_drive_id": "string",
  "course_name": "string",
  "created_at": "2025-10-31T03:05:03"
}

# Google Drive 

## Search with Query 
  {
    "id": "1JXdqDzmalhX0zNM0-5asrAQyoDOrVdwS",
    "name": "11/23/2021",
    "mime_type": "application/vnd.google-apps.folder",
    "web_view_link": "https://drive.google.com/drive/folders/1JXdqDzmalhX0zNM0-5asrAQyoDOrVdwS"
  },

  {
    "id": "1-76wbyhUyVIC4XCbk9y-YK3SzTmfLQs1",
    "name": "01/21/2022",
    "mime_type": "application/vnd.google-apps.folder",
    "web_view_link": "https://drive.google.com/drive/folders/1-76wbyhUyVIC4XCbk9y-YK3SzTmfLQs1"
  }

# Search User Files 
{
    "id": "1IQAdv1nQSyrIeboHicLiLlMmAH14WxZ0",
    "name": "HTML learning Footage",
    "mime_type": "application/vnd.google-apps.folder",
    "web_view_link": "https://drive.google.com/drive/folders/1IQAdv1nQSyrIeboHicLiLlMmAH14WxZ0"
  }

# Read By File ID

Body: 
{
  "fileid": "12vDv5EQ9cKl1ceBbYxEZN7rJAGFJ9J4zA9TNBo07v14"
}

Reponse body: 

{
  "content": "﻿World War II was a global conflict that lasted from 1939 to 1945, involving most of the world’s major nations. It began when Germany, led by Adolf Hitler, invaded Poland, prompting Britain and France to declare war. The war soon spread across Europe, Africa, and Asia, with the Axis powers—Germany, Italy, and Japan—fighting against the Allies, including the United States, the Soviet Union, and the United Kingdom. It was the deadliest conflict in history, marked by the Holocaust and the use of atomic bombs on Hiroshima and Nagasaki. The war ended with the defeat of the Axis powers and reshaped global politics, leading to the rise of the United States and the Soviet Union as superpowers."
}