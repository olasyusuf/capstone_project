## Design Your Database Schema (ERD)

#### **Social Media API \- Entity Relationship Diagram**

### **![][image1]**


<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

### **Social Media API \- Database Entities Structure**

**Account Entity**

| Field Name | Data Type | Constraints / Indexes | Notes |
| ----- | ----- | ----- | ----- |
| id | UUID | PK, default generated | Primary key |
| username | VARCHAR(150) | UNIQUE, NOT NULL | Indexed for quick lookup |
| email | VARCHAR(255) | UNIQUE, NOT NULL | Indexed for authentication |
| password | VARCHAR(128) | NOT NULL | Hashed password |
| avatar | TextField | NULLABLE | Optional profile image URL |
| bio | TextField | NULLABLE | User bio/description |
| role | VARCHAR(10) | NOT NULL, choices=\[‘admin’, ‘user’\] | Role-based access |
| created\_at | DateTimeField | auto\_now\_add=True | Record creation timestamp |

<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

**Profile Entity (Optional)**

| Field Name | Data Type | Constraints / Indexes | Notes |
| ----- | ----- | ----- | ----- |
| user | OneToOneField | FK \-\> User(id), UNIQUE | Links to User |
| location | VARCHAR(255) | NULLABLE | Optional location |
| website | URLField | NULLABLE | Optional personal website |
| date\_of\_birth | DateField | NULLABLE | Optional DOB |


<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

**Post Entity**

| Field Name | Data Type | Constraints / Indexes | Notes |
| ----- | ----- | ----- | ----- |
| id | UUID | PK, default generated | Primary key |
| author | ForeignKey | FK \-\> User(id), ON DELETE CASCADE | Post author |
| content | TextField | NOT NULL | Post text |
| image | TextField | NULLABLE | Optional image URL |
| created\_at | DateTimeField | auto\_now\_add=True | Timestamp for creation |
| updated\_at | DateTimeField | auto\_now=True | Timestamp for update |


<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

**Like Entity**

| Field Name | Data Type | Constraints / Indexes | Notes |
| ----- | ----- | ----- | ----- |
| id | UUID | PK, default generated | Primary key |
| post | ForeignKey | FK \-\> Post(id), ON DELETE CASCADE | Liked post |
| user | ForeignKey | FK \-\> User(id), ON DELETE CASCADE | User who liked |
| created\_at | DateTimeField | auto\_now\_add=True | Timestamp |


<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

**Comment Entity**

| Field Name | Data Type | Constraints / Indexes | Notes |
| ----- | ----- | ----- | ----- |
| id | UUID | PK, default generated | Primary key |
| post | ForeignKey | FK \-\> Post(id), ON DELETE CASCADE | Related post |
| user | ForeignKey | FK \-\> User(id), ON DELETE SET NULL | Comment author |
| content | TextField | NOT NULL | Comment text |
| created\_at | DateTimeField | auto\_now\_add=True | Timestamp |


<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

**Follow Entity**

| Field Name | Data Type | Constraints / Indexes | Notes |
| ----- | ----- | ----- | ----- |
| id | UUID | PK, default generated | Primary key |
| follower | ForeignKey | FK \-\> User(id), ON DELETE CASCADE | User following |
| following | ForeignKey | FK \-\> User(id), ON DELETE CASCADE | User being followed |
| created\_at | DateTimeField | auto\_now\_add=True | Timestamp |
| UNIQUE(follower, following) | Constraint | Ensures no duplicate follows | Prevent duplicates |

<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

**Notification Entity**

| Field Name | Data Type | Constraints / Indexes | Notes |
| ----- | ----- | ----- | ----- |
| id | UUID | PK, default generated | Primary key |
| user | ForeignKey | FK \-\> User(id), ON DELETE CASCADE | Recipient user |
| type | VARCHAR(20) | NOT NULL | Type of notification (follow, like, comment) |
| message | TextField | NOT NULL | Notification message |
| is\_read | BooleanField | default=False | Read/unread status |
| created\_at | DateTimeField | auto\_now\_add=True | Timestamp |

<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

**Reports Entity (Optional)**

| Field Name | Data Type | Constraints / Indexes | Notes |
| ----- | ----- | ----- | ----- |
| id | UUID | PK, default generated | Primary key |
| reporter | ForeignKey | FK \-\> User(id), ON DELETE CASCADE | Reporter |
| target\_user | ForeignKey | FK \-\> User(id), NULLABLE, ON DELETE SET NULL | Optional reported user |
| target\_post | ForeignKey | FK \-\> Post(id), NULLABLE, ON DELETE SET NULL | Optional reported post |
| reason | TextField | NOT NULL | Reason for report |
| status | VARCHAR(10) | default='pending', choices=\['pending','resolved'\] | Report status |
| created\_at | DateTimeField | auto\_now\_add=True | Timestamp |


<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---
**Relationships Summary**

| Relation | Type | Notes |
| ----- | ----- | ----- |
| User \-\> Post | One-to-Many | A user can create multiple posts |
| User \-\> Comment | One-to-Many | A user can comment on multiple posts |
| User \-\> Like | One-to-Many | A user can like multiple posts |
| User \<-\> User (Follow) | Many-to-Many through Follow | Follower/following relationship |
| User \-\> Notification | One-to-Many | Users receive multiple notifications |
| Post \-\> Comment | One-to-Many | Posts can have multiple comments |
| Post \-\> Like | One-to-Many | Posts can have multiple likes |
| Report \-\> User/Post | Many-to-One (optional) | Reports can reference either users or posts |


<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

## List Your API Endpoints

### Authentication

| Endpoint | Method | Description | Token Required | Notes |
| :---- | :---- | :---- | :---- | :---- |
| /auth/register/ | POST | Register a new user | ❌ | Returns JWT token on success |
| /auth/login/ | POST | Login user and obtain JWT | ❌ | Returns access & refresh tokens |
| /auth/refresh/ | POST | Refresh access token | ✅ | Requires refresh token |

<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

### Users

| Endpoint | Method | Description | Token Required | Notes |
| :---- | :---- | :---- | :---- | :---- |
| /users/ | GET | List all users | ✅ (Admin) | Admin-only; paginated recommended |
| /users/\<username\>/ | GET | Retrieve user profile | ✅ | Accessible by admin or owner |
| /users/profile/ | PATCH | Update logged-in user profile | ✅ | Only owner can edit |
| /users/\<id\>/ | DELETE | Delete a user | ✅ (Admin) | Admin-only |

<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

### Posts

| Endpoint | Method | Description | Token Required | Notes |
| :---- | :---- | :---- | :---- | :---- |
| /posts/ | GET | List all posts | ✅ | Includes author, likes, comments |
| /posts/ | POST | Create a new post | ✅ | Accepts text \+ optional image |
| /posts/\<id\>/ | GET | Get post details | ✅ | Includes likes & comments |
| /posts/\<id\>/ | PATCH | Update a post | ✅ | Only owner or admin |
| /posts/\<id\>/ | DELETE | Delete a post | ✅ | Only owner or admin |
|  |  |  |  |  |


<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

### Social Interactions (Likes & Comments)

| Endpoint | Method | Description | Token Required | Notes |
| :---- | :---- | :---- | :---- | :---- |
| /posts/\<id\>/like/ | POST | Like a post | ✅ | Prevents duplicate likes |
| /posts/\<id\>/like/ | DELETE | Unlike a post | ✅ | Deletes Like object |
| /posts/\<id\>/comment/ | POST | Add comment | ✅ | User can comment on any post |
| /posts/\<id\>/comments/ | GET | List comments | ✅ | Pagination optional |

<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

### Follow System

| Endpoint | Method | Description | Token Required | Notes |
| :---- | :---- | :---- | :---- | :---- |
| /users/\<username\>/follow/ | POST | Follow a user | ✅ | Cannot follow self |
| /users/\<username\>/unfollow/ | DELETE | Unfollow a user | ✅ | Only works if following |
| /users/\<username\>/followers/ | GET | List followers | ✅ | Public if profile not private |
| /users/\<username\>/following/ | GET | List following | ✅ | Public if profile not private |

<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

### Feed

| Endpoint | Method | Description | Token Required | Notes |
| :---- | :---- | :---- | :---- | :---- |
| /feed/ | GET | Retrieve logged-in user feed | ✅ | Posts from followed users, newest first, paginated |

<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

### Notifications

| Endpoint | Method | Description | Token Required | Notes |
| :---- | :---- | :---- | :---- | :---- |
| /notifications/ | GET | Retrieve all notifications | ✅ | Only for logged-in user |
| /notifications/\<id\>/read/ | PATCH | Mark notification as read | ✅ | Only owner can mark read |

<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

### Reports (Optional)

| Endpoint | Method | Description | Token Required | Notes |
| :---- | :---- | :---- | :---- | :---- |
| /reports/ | POST | Report a post or user | ✅ | Admin reviews reports |
| /reports/ | GET | List all reports | ✅ (Admin) | Admin-only; can filter by status |


<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---

**General Notes:**

* All modifying endpoints (POST, PUT/PATCH, DELETE) require JWT token.

* Admin endpoints require token \+ role verification.

* Public endpoints: register & login.

* Optional: pagination, filtering, search on GET endpoints.

* Rate-limiting recommended for login/register/post creation.


<br />

<div align="right">

  [ [↑ to top ↑](#table-of-contents) ]
</div>

---


[image1]: <data:image/png;base64,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>