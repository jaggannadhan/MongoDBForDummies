# MongoDB For Dummies - 101
Easy to learn MongoDB setup and guide with Python for beginners. Explore the code, run the examples, and start building your own APIs! Contributions and feedback are welcome.

# What is MongoDB?
MongoDB is a NoSQL database that stores data in a flexible, JSON-like format called BSON (Binary JSON). It is designed to handle large volumes of unstructured or semi-structured data. Unlike traditional relational databases (like MySQL or PostgreSQL), MongoDB doesn't rely on tables, rows, and columns. Instead, it uses collections  and documents (tables and rows in SQL).

## MongoDB Data Model
MongoDB organizes data into **databases**, **collections**, and **documents**.

1. Database: A database is a container for collections. You can think of it as similar to a schema in relational databases. <br/>
2. Collection: A collection is a group of documents. It’s analogous to a table in relational databases, but unlike tables, collections don’t enforce a strict schema.<br/>
3. Document: A document is a single record in MongoDB. It is stored in BSON (Binary JSON) format, which is a binary representation of JSON-like objects. Documents are similar to rows in relational databases, but they can have nested structures.<br/>

## What is a Document?
```
{
  "_id": ObjectId("60a7c3f8e4b0f2a3b4c5d6e7"),
  "user_id": "user123",
  "date": "2023-10-01",
  "workout_type": "Running",
  "duration_minutes": 30,
  "calories_burned": 300,
  "notes": "Felt great today!"
}
```
*_id*: Every document in MongoDB has a unique _id field, which acts as the primary key. If you don't specify one, MongoDB will automatically generate an ObjectId for it.

## What is BSON?
BSON (Binary JSON) : BSON is a binary-encoded serialization of JSON-like documents. MongoDB uses BSON internally to store data. BSON extends JSON by supporting additional data types like *Date*, *Binary*, and *ObjectId*.


## Setting Up MongoDB Locally (MacOS)
### 1. Installing MongoDB
```
brew tap mongodb/brew
brew install mongodb-community@8.0
```

### 2. Running MongoDB Locally
```
mongod
```

### 3. Connecting to MongoDB Using Python (PyMongo)
```
pip install pymongo
```
PyMongo is the official MongoDB driver for Python and is **synchronous**.
This means that each database operation blocks the execution of your program until it completes.

**Motor** is an *asynchronous* driver for MongoDB, built on top of PyMongo and designed to leverage Python's asyncio library.
```
pip install motor
```


### Basic Motor commands
| Operation          | Command                         | Description                                                    |        
|--------------------|---------------------------------|----------------------------------------------------------------|
| Insert One         | `insert_one(document)`          | Inserts a single document.                                     |
| Insert Many        | `insert_many(documents)`        | Inserts multiple documents.                                    |
| Find All           | `find(query)`                   | Retrieves all documents matching the query.                    |
| Find One           | `find_one(query)`               | Retrieves a single document matching the query.                |
| Update One         | `update_one(query, update)`     | Updates a single document.                                     |
| Update Many        | `update_many(query, update)`    | Updates multiple documents.                                    |
| Delete One         | `delete_one(query)`             | Deletes a single document.                                     |
| Delete Many        | `delete_many(query)`            | Deletes multiple documents.                                    |
| Count Documents    | `count_documents(query)`        | Counts documents matching the query.                           |
| Aggregate          | `aggregate(pipeline)`           | Performs aggregation operations.                               |
| Sort               | `sort(field, direction)`        | Sorts results by a field (1 for ascending, -1 for descending). |
| Limit              | `limit(n)`                      | Limits the number of results returned.                         |


### What Is the Aggregation Framework?
The aggregation framework processes data in stages, where each stage performs a specific operation (e.g., filtering, grouping, sorting). The output of one stage becomes the input for the next stage, forming a pipeline.

#### Key Stages in the Aggregation Pipeline (Most commonly used)
1. `$match`   : Filters documents to pass only those that match the specified condition(s). <br/>
2. `$group`   : Groups documents by a specified key and applies aggregations (e.g., sum, average). <br/>
3. `$sort`    : Sorts documents based on a field. <br/>
4. `$project` : Reshapes documents (e.g., include/exclude fields, rename fields). <br/>
5. `$limit`   : Limits the number of documents passed to the next stage. <br/>
6. `$lookup`  : Performs a left outer join to another collection. <br/>
7. `$unwind`  : Flatten the joined array of nutrition entries. <br/>

#### Example
Let's say we have two collections, `Workouts`, 

```
[
    {
        "_id": "1",
        "user_id": "user123",
        "calories_burned": 300
    },
    {
        "_id": "2",
        "user_id": "user456",
        "calories_burned": 400
    }
]
```
and `Nutrition`
```
[
    {
        "_id": "a",
        "user_id": "user123",
        "calories": 500
    },
    {
        "_id": "b",
        "user_id": "user123",
        "calories": 600
    },
    {
        "_id": "c",
        "user_id": "user456",
        "calories": 700
    }
]
```
Let's performing a `$lookup` between the **Workouts** and **Nutrition** collections, 

```
pipeline = [{
    "$lookup": {
        "from": "nutrition",  # Join with the Nutrition collection
        "localField": "user_id",
        "foreignField": "user_id",
        "as": "nutrition_data"  # Store joined data in this field
    }
}]
results = await workout_collection.aggregate(pipeline).to_list(None)
return results
```

After the `$lookup` result might look like this:
```
[
    {
        "_id": "1",
        "user_id": "user123",
        "calories_burned": 300,
        "nutrition_data": [
            {"_id": "a", "user_id": "user123", "calories": 500},
            {"_id": "b", "user_id": "user123", "calories": 600}
        ]
    },
    {
        "_id": "2",
        "user_id": "user456",
        "calories_burned": 400,
        "nutrition_data": [
            {"_id": "c", "user_id": "user456", "calories": 700}
        ]
    }
]
```

Let's apply `$unwind`
```
pipeline = [
  {
      "$lookup": {
          "from": "nutrition",  # Join with the Nutrition collection
          "localField": "user_id",
          "foreignField": "user_id",
          "as": "nutrition_data"  # Store joined data in this field
      }
  },
  {
  "$unwind": "$nutrition_data"  # Flatten the nutrition_data array
  }
]
```
After applying `$unwind` to the nutrition_data field, the result will look like this:
```
[
    {
        "_id": "1",
        "user_id": "user123",
        "calories_burned": 300,
        "nutrition_data": {"_id": "a", "user_id": "user123", "calories": 500}
    },
    {
        "_id": "1",
        "user_id": "user123",
        "calories_burned": 300,
        "nutrition_data": {"_id": "b", "user_id": "user123", "calories": 600}
    },
    {
        "_id": "2",
        "user_id": "user456",
        "calories_burned": 400,
        "nutrition_data": {"_id": "c", "user_id": "user456", "calories": 700}
    }
]
```
#### Key Points About `$unwind`
Handles Empty Arrays: If the array field is empty, `$unwind` will exclude the document from the output unless you use the preserveNullAndEmptyArrays option.

```
{
    "$unwind": {
        "path": "$nutrition_data",
        "preserveNullAndEmptyArrays": true
    }
}
```