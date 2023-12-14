"""从模型的docker logs中获得日志，并且将日志中的task请求数据转化为csv。
    如：
    docker logs --since 2023-02-15T00:00:00Z --until 2023-02-16T00:00:00Z txt2img_pipeline_vx.x.x >  13-2023-02-15.log
"""
import csv
import os
import ast
from collections import namedtuple
from typing import List

NT_CSV_ElE = namedtuple('NtCsvEle', ['taskId', 'inputText'])

class LogToCsv(object):

    logfile_path = f'./'
    csvfile_path = f'./'
    csv_fd = None
    col_num = 0
    # element_i_care = ['userId', 'taskId', 'inputText', 'negativePrompt', 'seeds', 'outputCnt', 'width', 'height']
    element_i_care = ['taskId', 'inputText']

    def __init__(self, file_name):
        self.log_file_with_path = f"{self.logfile_path}{file_name}"
        self.csv_file_with_path = f"{self.logfile_path}{file_name}.csv"
        print(f"{self.logfile_path}, {file_name}, {self.log_file_with_path},{self.csv_file_with_path}")
        self.create_csv_file()

    def read_log_file(self):
        with open(self.log_file_with_path, 'r') as log_fd:
            lines = log_fd.readlines()

        return lines

    def create_csv_file(self):
        self.csv_field_name = []

        for col_name in self.element_i_care:
            self.csv_field_name.append(col_name)
            self.col_num += 1
       
        self.csv_fd = open(self.csv_file_with_path, mode='w')
        self.writer = csv.DictWriter(self.csv_fd, fieldnames=self.csv_field_name)
        self.writer.writeheader()
   
    def write_csv_row(self, row:NT_CSV_ElE):
        row_value = dict()
        args_num = 0
        for i, value in enumerate(row):
            if i >= self.col_num:
                break
            row_value[self.csv_field_name[i]] = value
            args_num += 1

        if args_num != self.col_num:
            raise ValueError(f'Data num is not match with column num.')
       
        self.writer.writerow(row_value)
   
    def run(self):
        lines = self.read_log_file()
        for line in lines:
            task_msg_dict = ast.literal_eval(line) 
            csv_row_value = NT_CSV_ElE(task_msg_dict['taskId'], task_msg_dict['settings']['inputText'])
            #print(f"{csv_row_value}")
            self.write_csv_row(csv_row_value)

    def __del__(self):
        if self.csv_fd:
            self.csv_fd.close()


if __name__ == '__main__':
    test_log = LogToCsv('tasks.log')
    test_log.run()
