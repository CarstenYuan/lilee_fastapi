## This is a Python web server demonstration using FastAPI and MySQL.
### Functionalities
#### APIs
- User Management
    - Create User: add a new user
    - Delete User: Remove a user by id
    - Read Single User: Retrieve details of a specific user by id.
    - Read All Users: List all users with optional filtering by partial name match.
- Groups Management
    - Create Group: Add a new group.
    - Delete Group: Remove a group by id. Prevent deletion if the group has at least one user and provide an appropriate error message.
    - Read Single Group: Retrieve details of a specific group by id.
    - Read All Groups: List all groups.
---
### Database Design
#### Users Table
| id | name | group_id |
|--------|--------------------|---------|
| 1      | Olive Smith        | Null    |
| 2      | Noah Johnson       | 17      |
| 3      | Emma Williams      | 9       |

#### Groups Table
| id | name |
|--------|--------------|
| 1      | Basketball   |
| 2      | Math         |
| 3      | Literature   |

- Relationship: A user can belong to zero or one group; a group can have zero or many users.
---
### Launch services
#### Docker
- #### Prerequisites:
    - Have Docker installed and running
    - Port 3308 isn't occupied yet, otherwise, you'll need to change the port for 'mysqlDB' inside the docker-compose.yml file
```
# git clone this repository
> git clone https://github.com/CarstenYuan/lilee_fastapi.git
> cd lilee_fastapi

# run docker-compose.yml
> docker-compose up -d
```
#### Locally (for easier debugging or testing) ==> Future Work
---
### Testing
```
Visit the swagger web page: 127.0.0.1:9000/swagger
```
### Users APIs
#### Read All Users: List all users with optional filtering by partial name match.

- Execute **without** any name filter

> You should see 90 users in the response body (if you haven't created or deleted any users.)`

- Execute **with** a name filter

> Input 'Ja' in the name filter for example, and you will see the response body as below:
```
[
  {
    "group_id": 13,
    "id": 19,
    "name": "Avery Jackson"
  },
  {
    "group_id": 10,
    "id": 77,
    "name": "Kinsley James"
  },
  {
    "group_id": null,
    "id": 86,
    "name": "Jasmine Roberts"
  }
]
```
##### ------------------------------------------------------------
#### Create User: add a new user

- Input a name and an optional group_id, then click execute. **(Note: group_id has to exist)**
> You will see the response body as below:
```
{
  "item_type": "User",
  "name": "Haw Yuan",
  "id": 91,
  "group_id": null
}

> With group_id:
{
  "item_type": "User",
  "name": "Carsten Yuan",
  "id": 92,
  "group_id": 5
}
```

#### Use **Read Single User** to verify: input the id from the user you just created.
- If the user exists in the table:
```
{
  "item_type": "User",
  "name": "Carsten Yuan",
  "id": 92,
  "group_id": 5
}
```
- If the user doesn't exist:
```
{
  "detail": "User with id 95 does not exist."
}
```
##### ------------------------------------------------------------
#### Delete User: Remove a user by id

- Input a valid id
> The response body will show who was deleted
```
{
  "item_type": "User",
  "name": "Carsten Yuan",
  "id": 92,
  "group_id": 5
}
```
- If id doesn't exist
```
{
  "detail": "User with id 95 does not exist."
}
```
#### Use **Read Single User** to verify
```
{
  "detail": "User with id 92 does not exist."
}
```
##### ----------------------------------------------------------------------------------------------------
### Groups APIs
- Mostly the same as the above APIs, but several differences need to be clarified
    1. No name filter for 'GetAllGroups' API
    2. Cannot delete a group that has at least 1 member inside it
```
{
  "detail": "Group cannot be deleted because it has members."
}
```
