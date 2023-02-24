from bson import ObjectId
from datetime import datetime

import pymongo

import config

mongo_cli = pymongo.MongoClient(config.MONGODB_URI)


class BaseCollection(object):
    database = ''
    name = ''

    @classmethod
    def json_format(cls, item):
        """
        是否需要深度遍历呢？
        :param item:
        :return:
        """
        if not item:
            return {}

        for k, v in item.items():
            if isinstance(v, ObjectId):
                item[k] = str(v)

            elif isinstance(v, datetime):
                # item[k] = v.isoformat()
                item[k] = int(v.timestamp())

        return item

    @classmethod
    def date_column2timestamp(cls, item):
        """把字典中值为 datetime 的转为 iso 标准日期字符串"""
        for k in item:
            if isinstance(item[k], datetime):
                item[k] = item[k].isoformat()
        return item

    @classmethod
    def insert_one(cls, item, remove_id=True):
        # 添加创建时间
        if isinstance(item, dict) and "update_time" not in item:
            item["update_time"] = datetime.utcnow()

        mongo_cli[cls.database][cls.name].insert_one(item)
        item['_id'] = str(item['_id'])
        if remove_id:
            item['_id'] = None
            item.pop('_id')

        return {"code": 1, "data": item}

    @classmethod
    def insert_many(cls, items):
        res = mongo_cli[cls.database][cls.name].insert_many(items)
        return {
            "code": 1,
            "data": {
                'data': [str(inserted_id) for inserted_id in res.inserted_ids],
                'total': len(res.inserted_ids)
            }
        }

    @classmethod
    def delete_one(cls, query):
        res = mongo_cli[cls.database][cls.name].delete_one(query)
        return {
            "code": 1,
            "data": {
                'total': res.deleted_count
            }
        }

    @classmethod
    def delete_many(cls, query):
        res = mongo_cli[cls.database][cls.name].delete_many(query)
        return {
            "code": 1,
            "data": {
                'total': res.deleted_count
            }
        }

    @classmethod
    def update_one(cls, query, values):
        # 添加修改时间
        if isinstance(values, dict) and "$set" in values \
                and isinstance(values["$set"], dict) \
                and "update_time" not in values["$set"]:
            values["$set"]["update_time"] = datetime.utcnow()

        if "_id" in query:
            query["_id"] = ObjectId(query["_id"])

        res = mongo_cli[cls.database][cls.name].update_one(query, values)
        return {
            "code": 1,
            "data": {
                'total': res.modified_count
            }
        }

    @classmethod
    def update_many(cls, query, values):
        if "_id" in query:
            query["_id"] = ObjectId(query["_id"])

        res = mongo_cli[cls.database][cls.name].update_many(query, values)
        return {
            "code": 1,
            "data": {
                'total': res.modified_count
            }
        }

    @classmethod
    def find_one(cls, query, columns=None, json_format=True):
        res = mongo_cli[cls.database][cls.name].find_one(query, columns)
        if json_format:
            res = cls.json_format(res)

        return {
            "code": 1,
            "data": res
        }

    @classmethod
    def pre_find_one(cls, query, columns=None):
        res = mongo_cli[cls.database].find_one(query, columns)
        return res

    @classmethod
    def pre_find(cls, query, columns={'_id': 0}, sort=None):
        res = mongo_cli[cls.database][cls.name].find(query, columns)
        if sort:
            if isinstance(sort, str):
                res = res.sort(sort)

            elif isinstance(sort, dict) and (len(sort) == 1):
                for key, value in sort.items():
                    res = res.sort(key, value)
                    break

            elif isinstance(sort, (tuple, list)) and (len(sort) == 2):
                res = res.sort(*sort)

        return res

    @classmethod
    def find(cls, query, columns={'_id': 0}, sort=None, page_no=1, page_size=20, json_format=True):
        """
        查询明细
        :param query:
        :param columns:
        :param sort:
        :param page_no:
        :param page_size:
        :param json_format: 是否对数据中json不支持的格式的字段进行转换
        :return:
        """
        try:
            page_no = int(page_no)
            if page_no < 1:
                page_no = 1

        except Exception as e:
            page_no = 1

        try:
            page_size = int(page_size)
            if page_size < 1 or page_size > config.MAX_EXPORT_LINES:
                page_size = 20

        except Exception as e:
            page_size = 20

        limit = page_size
        offset = page_size * (page_no - 1)
        res = cls.pre_find(query, columns, sort=sort)
        count = res.count()

        res = res.limit(limit).skip(offset)
        data = []
        for item in res:
            if json_format:
                item = cls.json_format(item)

            data.append(item)

        return {
            "code": 1,
            "data": {
                'data': data,
                'total': count
            }
        }

    @classmethod
    def aggregate(cls, pipeline: list):
        res = mongo_cli[cls.database][cls.name].aggregate(pipeline)
        data = []
        for item in res:
            if ('_id' in item) and isinstance(item['_id'], ObjectId):
                item['_id'] = str(item['_id'])
            item = cls.date_column2timestamp(item or {})
            data.append(item)
        return {
            "code": 1,
            "data": data
        }
