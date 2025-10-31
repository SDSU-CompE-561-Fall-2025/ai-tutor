# All Testing has been done using the swagger docs once running the fastapi server

# User

## POST Route: /api/v1/user/register

Body: {
"email": "yourGmailToGiveAccessTo@gmail.com",
"password": "123"
}

Response: A google auth redirect uri

## GET Route: /api/v1/user/auth/google/callback

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

## POST Route: /api/v1/user/login

Body: urlformEncoded - userName:'signedupEmail@gmail.com' Password:'pass'

Response: {
"access_token": FHaA",
"token_type": "bearer"
}

## GET Route: /api/v1/user/me

Body: Recieves JWT Token in header

Response: {
"email": "gmail@gmail.com",
"id": 2
}

## GET Route: /api/v1/user/token

Body: Recieves JWT Token in header

Response: {
"access_token": "ya29.Dx1Xg",
"expiry": "2025-10-31T00:03:46"
}

# Course

## POST Route: /api/v1/courses/

Request Body: {
  "name": "math101"
}

Response: {
  "name": "math101",
  "id": 1
}

## GET Route: /api/v1/courses/ 

Response: [
  {
    "name": "math101",
    "id": 1
  }
]

## GET Route: /api/v1/courses/1 

Parameters: course_id 

Response: {
  "name": "math101",
  "id": 1
}

## PUT Route: /api/v1/courses/1 

Parameters: course_id 

Body: {
  "name": "physics102"
}

Response: {
  "name": "physics102",
  "id": 1
}

## GET Route: /api/v1/courses/1/tutor-sessions 

Parameters: course_id 

Response: [
  {
    "title": "session1",
    "id": 1,
    "course_name": "physics102",
    "chat_messages": [
      {
        "role": "user",
        "message": "test",
        "id": 1,
        "tutor_session_title": "session1",
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
  "name": "test",
  "google_drive_id": "2",
  "course_id": 1
}

Response: {
  "id": 2,
  "name": "test",
  "google_drive_id": "2",
  "course_name": "physics102",
  "created_at": "2025-10-31T03:05:03"
}

## GET Route: /api/v1/files/ 

Response: [
  {
    "id": 1,
    "name": "test",
    "google_drive_id": "2",
    "course_name": "physics102",
    "created_at": "2025-10-31T03:49:27"
  }
]

## PUT Route: /api/v1/files/{file_id}

Body: {
  "name": "test",
  "google_drive_id": "2",
  "course_id": 1
}

Response: {
  "id": 2,
  "name": "test",
  "google_drive_id": "2",
  "course_name": "physics102",
  "created_at": "2025-10-31T03:05:03"
}

## DELETE Route: /api/v1/files/{file_id}

Body: {
  "file_id": 2
}

Response: null

## GET Route: /api/v1/files/{file_id}

Body: {
  "file_id": 2
}

Response: {
  "id": 2,
  "name": "test",
  "google_drive_id": "2",
  "course_name": "physics102",
  "created_at": "2025-10-31T03:05:03"
}

## GET Route: /api/v1/files/course/{course_id}

Body: {
  "course_id": 2
}

Response: [
  {
    "id": 2,
    "name": "test",
    "google_drive_id": "2",
    "course_name": "physics102",
    "created_at": "2025-10-31T03:51:51.659Z"
  }
]

# Tutor Session

## POST Route: /api/v1/tutor-session/chat

Body: {
  "title": session1,
  "course_id": 1
}

Response: {
  "title": "session1",
  "id": 1,
  "course_name": "physics101",
  "chat_messages": [
    {
      "role": "user",
      "message": "Hello World!",
      "id": 2,
      "tutor_session_title": "session1",
      "created_at": "2025-10-31T03:57:02.329Z"
    }
  ],
  "created_at": "2025-10-31T03:57:02.329Z"
}

## GET Route: /api/v1/tutor-session/{tutor_session_id}

Body: {
  "tutor_session_id" = 2
}

Response: {
  "title": "session1",
  "id": 2,
  "course_name": "physics101",
  "chat_messages": [
    {
      "role": "user",
      "message": "Hello World!",
      "id": 2,
      "tutor_session_title": "session1",
      "created_at": "2025-10-31T03:57:02.329Z"
    }
  ],
  "created_at": "2025-10-31T03:57:02.329Z"
}

## PUT Route: /api/v1/tutor-session/chat

Body: {
  "tutor_session_id": 1,
  "title": session1
}

Response: {
  "title": "session1",
  "id": 1,
  "course_name": "physics101",
  "chat_messages": [
    {
      "role": "user",
      "message": "Hello World!",
      "id": 2,
      "tutor_session_title": "session1",
      "created_at": "2025-10-31T03:57:02.329Z"
    }
  ],
  "created_at": "2025-10-31T03:57:02.329Z"
}

## DELETE Route: /api/v1/tutor-session/chat

Body: {
  "tutor_session_id": 2
}

Response: null

## GET Route: /api/v1/tutor-session/{tutor_session_id}/messages

Body: {
  "tutor_session_id": 3
}

Response: {
  "title": "session2",
  "id": 3,
  "course_name": "math201",
  "chat_messages": [
    {
      "role": "user",
      "message": "Bye World!",
      "id": 5,
      "tutor_session_title": "session2",
      "created_at": "2025-10-31T03:57:02.329Z"
    }
  ],
  "created_at": "2025-10-31T03:57:02.329Z"
}
