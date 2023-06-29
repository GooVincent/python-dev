import unittest
from dataclasses import dataclass
import json


@dataclass
class TaskInfo:
    taskId: int
    userId: int
    host: str = ""


def get_class_members(class_type) -> list:
    """get_class_members
        get all members' name in a class. im my test python3.8 works
    """
    import inspect

    members = inspect.getmembers(class_type, lambda a:not(inspect.isroutine(a)))
    for k, v in members:
        if "__annotations__" in k:
            return list(v.keys())

    return []


def construct_obj_from_dict(d:dict, class_type) -> any:
    """construct_obj_from_dict
        constrcut class object from json

        construct object from dict even d.keys are not matched with class
    """
    if not isinstance(d, dict):
        return None

    members = get_class_members(class_type)
    dict_matched_class = dict()
    for member in members:
        dict_matched_class[member] = d.get(member, None)

    return class_type(**dict_matched_class)


class TestParseJson2Class(unittest.TestCase):

    def test_mathched(self):
        json_str = '{"userId": 11, "taskId": 22, "host": "test.url"}'
        test_input = json.loads(json_str)
        task_info = construct_obj_from_dict(test_input, TaskInfo)
        self.assertTrue(task_info.userId == 11)
        self.assertTrue(task_info.taskId == 22)
        self.assertTrue(task_info.host == "test.url")

    def test_more(self):
        json_str = '{"userId": 11, "taskId": 22, "host": "test.url", "more": "extra"}'
        test_input = json.loads(json_str)
        task_info = construct_obj_from_dict(test_input, TaskInfo)
        self.assertTrue(task_info.userId == 11)
        self.assertTrue(task_info.taskId == 22)
        self.assertTrue(task_info.host == "test.url")

    def test_less(self):
        json_str = '{"userId": 11, "taskId": 22}'
        test_input = json.loads(json_str)
        task_info = construct_obj_from_dict(test_input, TaskInfo)
        self.assertTrue(task_info.userId == 11)
        self.assertTrue(task_info.taskId == 22)
        self.assertTrue(task_info.host == None)


if __name__ == '__main__':
    unittest.main()