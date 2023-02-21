"""从模型的docker logs中获得日志，并且将日志中的task提取出来用来本地测试验证。
    如：
    docker logs --since 2023-02-15T00:00:00Z --until 2023-02-16T00:00:00Z txt2img_pipeline_vx.x.x >  13-2023-02-15.log
"""
import os


class LogExactTask(object):

    logfile_path = f'./logs-prod/'
    csvfile_path = f'./'

    def __init__(self, log_file):
        self.log_file_with_path = f"{self.logfile_path}{log_file}"
        file_name = os.path.splitext(log_file)[0]
        tasks_file_name = f'./{file_name}_2tasks.log'
        print(f'{tasks_file_name}')
        self.save_file_fd = open(tasks_file_name, 'w')

    def read_log_file(self):
        with open(self.log_file_with_path, 'r') as log_fd:
            lines = log_fd.readlines()

        return lines
    
    def run(self):
        lines = self.read_log_file()
        for line in lines:
            if '=============task server get a message' in line:
                start = line.find('{')
                end = line.rfind('}')
                # print(f'{line[start:end+1]}')
                assert(self.save_file_fd is not None)
                self.save_file_fd.write(f'{str(line[start:end+1])}\n')

    def __del__(self):
        if self.save_file_fd:
            self.save_file_fd.close()


if __name__ == '__main__':
    test_log = LogExactTask('13-2023-02-15.log')
    test_log.run()
