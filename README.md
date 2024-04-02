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
### Database Design
#### Users Table
| id | name | group_id |
|--------|--------------------|---------|
| 1      | Olive Smith        | Null    |
| 2      | Noah Johnson       | 17      |
| 3      | Emma Williams      | 9       |

#### Groups Table
| id | name |
|--------|---------|
| 1      | Basketball   |
| 2      | Math         |
| 3      | Literature   |

- Relationship: A user can belong to zero or one group; a group can have zero or many users.

### Launch services
#### Locally
- ##### Prerequisites:
    - Have local MySQL DB installed and running, with username 'root' and password '1qaz2wsx'
```
# git clone this repository
> git clone https://github.com/CarstenYuan/lilee_fastapi.git
> cd lilee_fastapi

# install python dependencies
> pip install -r requirements.txt

# db initial migration
> alembic upgrade head

# run FastAPI app
> python ./app.py
```
#### Docker
- ##### Prerequisites:
    - Have Docker installed and running
    - Port 3308 isn't occupied yet, otherwise, you'll need to change the port for mysqlDB inside the docker-compose.yml file
```
# git clone this repository
> git clone https://github.com/CarstenYuan/lilee_fastapi.git
> cd lilee_fastapi

# run docker-compose.yml
> docker-compose up -d
```

### Testing
```
Visit website: 127.0.0.1:9000/
```
#### Users APIs
- Read All Users: List all users with optional filtering by partial name match.
```
1. Click execute directly without any name filter
> You should see 90 users in the response body if you haven't created or deleted any users.

2. With a name filter
> Input 'Ja' in the name filter, and you will see the response body like this:
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

- Create User: add a new user
```
1. Input a name and an optional group_id, then click execute. (Note: group_id has to exist)
> You will see 200 and the response body like this:
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

2. Use 'Read Single User' to verify
> Input the id from the user you just created.
> If the user exists in the table:
{
  "item_type": "User",
  "name": "Carsten Yuan",
  "id": 92,
  "group_id": 5
}

> If not
{
  "detail": "User with id 95 does not exist."
}
```

- Delete User: Remove a user by id
```
1.
> Input a valid id, and the response body will show who was deleted
{
  "item_type": "User",
  "name": "Carsten Yuan",
  "id": 92,
  "group_id": 5
}

> If id doesn't exist
{
  "detail": "User with id 95 does not exist."
}

2. Use 'Read Single User' to verify
{
  "detail": "User with id 92 does not exist."
}
```

#### Groups APIs
- Mostly the same as the above APIs, but 2 differences need to be clarified
    - No name filter for 'GetAllGroups' API
    - Cannot delete a group that has at least 1 member inside it
```
{
  "detail": "Group cannot be deleted because it has members."
}
```
