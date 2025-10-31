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

# Chat_Messages

## /api/v1/chat-messages/

Body: Bearer Token in header

Response: [
{
"id": 1,
"tutor_session_id": 1,
"role": "user",
"message": "I am the goat",
"user_id": 1,
"created_at": "2025-10-29T22:45:49"
},
{
"id": 2,
"tutor_session_id": 1,
"role": "user",
"message": "I am dariel",
"user_id": 1,
"created_at": "2025-10-29T22:46:20"
},
{
"id": 3,
"tutor_session_id": 1,
"role": "user",
"message": "hello whats inthe chat history",
"user_id": 1,
"created_at": "2025-10-30T02:36:44"
},]

## Post: /api/v1/chat-messages/

Body: {
"role": "user",
"message": "hello tell me about my documents",
"tutor_session_id": 1
}

Response: {
"role": "assistant",
"message": "Hello Dariel!\n\nYour primary document is **A3 Written Assignment 3**, which is a practical exercise centered around **Constraint Satisfaction Problems (CSPs)** in Artificial Intelligence.\n\nHere's a breakdown of its content:\n\n* **Defining CSPs:** The assignment begins by asking you to define the fundamental components of a CSP—**Variables**, **Domains**, and **Constraints**—using a children's crossword puzzle as an example. This involves identifying word slots, possible English words, and rules like shared letters and unique word usage.\n\n* **Oz Map Coloring Problem:** This is the main part, applying CSP concepts to a 3-color map of Frank Baum's fictional land of Oz.\n _ You'll be asked to draw a **constraint hypergraph** to visually represent which regions touch each other.\n _ A significant portion involves simulating the **AC3 algorithm** step-by-step. You'll demonstrate how it enforces arc consistency by reducing variable domains and updating a queue, given initial assignments (Q=Green, W=Purple).\n \* Finally, you'll show how **Forward Checking** uses these same initial assignments to immediately prune the domains of neighboring variables, simplifying the problem early on.\n\nIn essence, the document guides you through understanding how to model problems as CSPs and then apply powerful algorithms like AC3 and Forward Checking to solve or simplify them.\n\nThe file ID for this material is: `1DxZBJqKNaAdjdmDKAq_bkb3BE62k1oFYIHtqYqs51ho`",
"id": 38,
"tutor_session_title": "test",
"created_at": "2025-10-31T04:14:19"
}

## Get: /api/v1/chat-messages/{message_id}

Parameter: message_id

Response: {
"role": "user",
"message": "I am dariel",
"id": 2,
"tutor_session_title": null,
"created_at": "2025-10-29T22:46:20"
}

## Patch: /api/v1/chat-messages/{message_id}

Parameter: message_id

Body: {
"role": "user",
"message": "no no no",
"tutor_session_id": 1
}

Response: {
"role": "user",
"message": "no no no",
"id": 2,
"tutor_session_title": null,
"created_at": "2025-10-29T22:46:20"
}

## Delete: /api/v1/chat-messages/{message_id}

Parameter: message_id

Response: null
