from mongo import BaseCollection

import config


class TaskCollection(BaseCollection):
    database = config.MONGODB_DB
    name = config.COLLECTION_TASK

    """struct
    {
        "_id": "",
        "audio": {
            "size": 0,
            "duration": 0,
            "url": "",
            "start_time": "",
            "end_time": ""
        },
        "task_id": "",
        "create_time": "",
        "update_time": "",
        "status": 0,
        "": ""
    }
    """


class ResultCollection(BaseCollection):
    database = config.MONGODB_DB
    name = config.COLLECTION_RESULT

    """struct
    {
        "_id": "",
        "url": "",
        "task_id": "",
        "id": "",
        "start_time": "",
        "end_time": "",
        "text": "",
        "create_time": "",
        "update_time": ""
    }
    """


class MonitorCollection(BaseCollection):
    database = config.MONGODB_DB
    name = config.COLLECTION_MONITOR

    """struct
    {
        "_id": "",
        "cpu": "",
        "memory": "",
        "disk": "",
        "create_time": "",
        "update_time": ""
    }
    """


if __name__ == "__main__":
    # TaskCollection.insert_one({"a": "test", "b": "test"})
    # ResultCollection.insert_one({"a": "test", "b": "test"})
    from bson import ObjectId
    # res = TaskCollection.update_one(
    #     {"_id": ObjectId(ObjectId("63f5f66af14925b223016f8b"))},
    #     {"$set": {"start_download_time": datetime.datetime.now()}}
    # )
    # print(res)
    res = ResultCollection.delete_many({"task_id": "3673cbb2-b2a4-11ed-b1dd-527ffdafd4cf"})
    print(res)
