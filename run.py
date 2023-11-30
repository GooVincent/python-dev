import requests
from typing import List
import random
import time
import json


URI = "http://localhost:60000/api/v1/generate"


class CsvUtils(object):

    def __init__(self, csv_title: List[str], file_name: str):
        self.col_num = 0
        self.file_name = file_name
        self.csv_title = csv_title      # csv_title = ['task_id', 'model_input']
        self.create_csv_file()

    def create_csv_file(self):
        import csv

        self.csv_field_name = []

        for col_name in self.csv_title:
            self.csv_field_name.append(col_name)
            self.col_num += 1

        self.csv_fd = open(self.file_name, mode='w')
        self.writer = csv.DictWriter(self.csv_fd, fieldnames=self.csv_field_name)
        self.writer.writeheader()

    def write_csv_row(self, field: list):
        row_value = dict()
        args_num = 0
        for i, value in enumerate(field):
            if i >= self.col_num:
                break
            row_value[self.csv_field_name[i]] = value
            args_num += 1

        if args_num != self.col_num:
            raise ValueError(f'Data num is not match with column num.')

        self.writer.writerow(row_value)

    def __del__(self):
        if self.csv_fd is not None:
            self.csv_fd.close()


def read_csv(csv_file: str) -> List[dict]:
    import csv

    result = []
    with open(csv_file, 'r') as input_f:
        lines = csv.DictReader(input_f)
        result = list(lines)
    return result


def run(prompt, seed) -> str:
    request = {
        'batch_id': "This is testing batch_id:666",
        'prompt': prompt,
        'seed': seed
    }

    response = requests.post(URI, json=request)

    assert response.status_code == 200, f"rsp_code={response.status_code}"
    result = response.json()['results'][0]['text']
    # result = result.replace('\n', '\\n')
    print(f"--{result}")
    return result


def batch_run_by_specific_file(round: int):
    test_cases_filename = 'tests/batch_chat/chat_test_simple.csv'
    test_result_filename = 'tests/batch_chat/test_result.csv'
    data = read_csv(test_cases_filename)

    title = ['id', 'reply', 'seed', 'input_context']
    generate_fd = CsvUtils(title, test_result_filename)
    for i, line in enumerate(data):
        for j in range(round):
            seed = random.randint(1, 2**32-1)
            reply = run(line['input_context'], seed)
            generate_fd.write_csv_row([i+1, reply, seed, line['input_context']])

            print(f'Done conv[{i}] round[{j}]')


def batch_run_by_fix_context(round: int, input_context: str):
    import concurrent.futures

    title = ['id', 'reply', 'seed', 'input_context']
    input_context = input_context.replace('\\r\\n', '\n')
    input_context = input_context.replace('\r\n', '\n')

    tp = concurrent.futures.ThreadPoolExecutor(max_workers=50)
    futures = []

    for j in range(round):
        seed = random.randint(1, 2**32-1)
        # reply = run(input_context, seed)
        futures.append(tp.submit(run, input_context, seed))

    for i, future in enumerate(concurrent.futures.as_completed(futures)):
        yield {title[0]:i, title[1]:future.result(), title[2]:seed, title[3]:input_context}


if __name__ == '__main__':
    import sys

    round = int(sys.argv[1])
    batch_run_by_specific_file(round)
