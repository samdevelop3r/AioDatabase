# AioDatabase
Wrapper for fast working with asynchronous mysql

# Edit dbconfig.json for working

```json
{
  "hostname": "Your hostname",
  "port": 3306,
  "user": "Username",
  "password": "User's password",
  "db": "Database's name"
}
```

# Examples for working

Creating a table


```py
database = aiodatabase.AioDatabase()
await database.create_table(
    name="users",
    primary_key="id int", username="str",
    balance="int", mutes="int"
)
```

Insert a column to table

```py
database = aiodatabase.AioDatabase()
await database.table("users").insert_value(
    username="sam", balance=0, mutes=2
)
```

Update a values from tables

```py
database = aiodatabase.AioDatabase()
await database.table("users").update_value(
    values=[{"username": "Greatest Sam"}, {"balance": 999}]
    username="sam"  # value that determine where existing thats column
)
```

Deleting the columns

```py
database = aiodatabase.AioDatabase()
await database.table("users").delete_value(username="Sam")
```

Selecting a values from columns

```py
database = aiodatabase.AioDatabase()
await database.table("users").select_values(
    values="all",  # or values=["username", "balance"]
    balance=200
)
```
