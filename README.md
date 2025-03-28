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


# MongoDB Concepts
## 1. Data Modeling in MongoDB
Data modeling is a critical aspect of designing efficient and scalable MongoDB schemas. Unlike relational databases, MongoDB uses a flexible schema , which means you have more freedom in how you structure your data. However, this flexibility also requires careful planning to ensure optimal performance.

#### Key Concepts
a. **Embedded Data**: Store related data in a single document (e.g., embedding nutrition entries within a user document). <br/>
b. **Referenced Data**: Store related data in separate collections and reference them using IDs (e.g., linking workouts and nutrition via user_id).<br/>
c. **Denormalization**: Duplicate data to reduce the need for joins (useful for read-heavy workloads).<br/>
d. **Normalization**: Avoid duplication by splitting data into multiple collections (useful for write-heavy workloads).<br/>

#### Best Practices for Data Modeling
a. **Understand Your Queries**:<br/>
Design your schema based on the queries your application will perform most frequently.<br/>
Optimize for reads if your application is read-heavy, and for writes if it’s write-heavy.<br/>
b. **Limit Document Size**:<br/>
Keep documents under 16 MB to avoid hitting MongoDB’s size limit.<br/>
Use references for large or frequently updated data.<br/>
c. **Avoid Deep Nesting**:<br/>
While MongoDB supports nested objects and arrays, deeply nested structures can make queries more complex.<br/>
Flatten your data where possible.<br/>
d. **Use Arrays for One-to-Many Relationships**:<br/>
For relationships where one entity has multiple related items (e.g., a workout with multiple nutrition entries), use arrays.<br/>
Be cautious about array size to avoid exceeding document limits.<br/>
e. **Index Strategically**:<br/>
Create indexes on fields used in filters, sorts, and groupings.<br/>
Avoid over-indexing, as it increases storage costs and slows down writes.<br/>


## 2. Indexing Optimization
Indexes are crucial for improving query performance, but they come with trade-offs. Let’s explore how to optimize indexes for large datasets and complex queries.

#### Key Topics
**Index Types:**<br/>
a. Single-field indexes (e.g., user_id).<br/>
b. Compound indexes (e.g., user_id + date).<br/>
c. Text indexes for full-text search.<br/>
d. Geospatial indexes for location-based queries.<br/>
**Index Creation Strategies:**<br/>
a. Create indexes on fields used in filters ($match), sorts ($sort), and groupings ($group).<br/>
b. Avoid over-indexing, as it increases storage costs and slows down writes.<br/>
**Explain Plans:**<br/>
Use MongoDB’s explain() method to analyze query performance and verify index usage.<br/>

#### Examples:
1. Create a single-field index on `user_id`.
```
await db["workouts"].create_index("user_id")
```
2. Create a compound index on `user_id` and `date`.
```
# Filter by user_id and Sort by date 
await db["workouts"].create_index([("user_id", 1), ("date", -1)])
```
3. Text Index 
```
await db["workouts"].create_index([("notes", "text")])
```
4. Geospatial Index 
```
await db["locations"].create_index([("location", "2dsphere")])
```
5. Testing Index Performance
Use the explain() method to verify that queries use the indexes:
```
result = await db["workouts"].find({"user_id": "user123"}).sort("date", -1).explain()
print(result)
```
6. Monitor Index Usage and identify unused indexes:
```
stats = await db["workouts"].aggregate([{"$indexStats": {}}]).to_list(None)
print(stats)
```
7. Drop Unused Indexes:
```
await db["workouts"].drop_index("user_id_1")
```
8. TTL Index:
TTL (Time-To-Live) indexes automatically remove documents after a specified period. This is useful for managing temporary data like logs or sessions.
```
await db["logs"].create_index("createdAt", expireAfterSeconds=30 * 24 * 60 * 60)
```
9. Partial Indexes:
Partial indexes only index documents that match a filter. This reduces index size and improves performance for specific queries.
```
# Index only workouts with calories_burned > 500:
await db["workouts"].create_index(
    [("calories_burned", 1)],
    partialFilterExpression={"calories_burned": {"$gt": 500}}
)
```
10. Wildcard Indexes:
Wildcard indexes allow you to index all fields in a document or a subset of fields. This is useful for dynamic schemas.
```
await db["workouts"].create_index({"$**": 1})
```
**Key Metrics to Look For:** <br/>
a. `stage`: `IXSCAN`: Indicates that the query used an index.<br/>
b. `totalDocsExamined`: The number of documents scanned ( much smaller than the total number of documents in the collection if an index is used).<br/>
c. `executionTimeMillis`: The time taken to execute the query.<br/>


## 3. Scaling MongoDB
As your application grows, you may need to scale MongoDB to handle increased traffic and data volume. <br/>
a. **Sharding**: Distribute data across multiple servers to improve performance and storage capacity.<br/>
b. **Replication**: Maintain multiple copies of your data for high availability and fault tolerance.<br/>
c. **Capped Collections**: Use fixed-size collections for high-throughput logging or analytics.<br/>

### Sharding
Sharding is MongoDB’s solution for horizontal scaling. It involves distributing data across multiple servers (shards) to improve performance and storage capacity.

#### How Sharding Works?
**Shard Key**:<br/>
A shard key determines how data is distributed across shards.<br/>
Example: Use `user_id` as the shard key to distribute data by user.<br/>
**Chunks**:<br/>
Data is divided into chunks based on the shard key.<br/>
Each chunk contains a range of shard key values.<br/>
**Mongos Router**:<br/>
The `mongos` process routes queries to the appropriate shard(s).<br/>
**Config Servers**:<br/>
Store metadata about the cluster (e.g., which shard contains which chunks).<br/>

#### Best Practices for Sharding
a. Choose a high-cardinality shard key (e.g., `user_id`) to ensure even data distribution.<br/>
b. Avoid using monotonically increasing keys (e.g., timestamps) as the shard key, as they can lead to hotspots.<br/>
c. Monitor shard distribution using the `sh.status()` command.<br/>

###  Replication
Replication ensures high availability by maintaining multiple copies of your data. MongoDB uses a replica set, which consists of:<br/>
**Primary Node**: Handles all write operations.<br/>
**Secondary Nodes**: Replicate data from the primary and can serve read operations.<br/>
**Arbiter (Optional)**: Helps elect a new primary if the current primary fails.<br/>

#### How Replication Works?
a. Write operations are applied to the primary node.<br/>
b. The primary logs changes in the `oplog` (operations log).<br/>
c. Secondary nodes replicate changes from the oplog.<br/>

### Capped Collections
Capped collections are fixed-size collections that automatically overwrite old data when the size limit is reached. They’re useful for high-throughput logging or analytics.
```
await db.create_collection(
    "logs",
    capped=True,
    size=100000,  # Maximum size in bytes
    max=1000      # Maximum number of documents
)
```

