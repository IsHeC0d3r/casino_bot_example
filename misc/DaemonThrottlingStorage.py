from time import time, sleep

class DaemonThrottlingStorage():
    def __init__(self, ex: int = None, max: int = None):
        """
        Init DaemonThrottlingStorage

        :By @IsHeCoder:
        :param ex - expiration_time:
        :param max - maximum messages count at this time:
        :return:
        """

        self.storage = {}
        self.ex = ex
        self.max = max

    def set(self, key: str | int) -> None:
        """
        Adding values to RAM in key:value format

        :By @IsHeCoder:
        :param key:
        :param value:
        :param ex = None:
        :return:
        """

        # print('[DEBUG]: SET')

        if key not in self.storage:
            self.storage[key] = [{'status': 0, 'ex': 0}]
        
        self.storage[key].append(
                {
                    'ex': time() + self.ex
                }
        )
    
    def get(self, key: str | int) -> dict | int:
        """
        Getting values from RAM

        :By @IsHeCoder:
        :param key:
        :return:
        """

        # print('[DEBUG]: GET')

        self.storage.setdefault(key, [{'status': 0, 'ex': 0}])

        if time() < self.storage[key][0]['ex']:
            return 1

        #self.storage[key] = [self.storage[key][0]] + [data for data in self.storage[key][1:] if time() > data['ex']]

        # for data in self.storage[key][1:]:
        #     if time() > data['ex']:
        #         self.storage[key].remove(data)

        # if len(self.storage[key]) > 2:
        #     print(len(self.storage[key]))
        #     self.storage[key].remove(data for data in self.storage[key][1:] if time() > data['ex'])

        self.storage[key] = [self.storage[key][0]] + [data for data in self.storage[key][1:] if time() < data['ex']]

        # print(self.storage[key])

        if len(self.storage[key]) - 2 == self.max:
            self.set_status(key, 1)
            return 1
        else:
            return 0
        return -1
        # if key in self.storage:
        #     if time() < self.storage[key][0]['ex']:
        #         return 1
        #     for data in self.storage[key]:
        #         if 'status' not in data:
        #             if time() > data['ex']:
        #                 self.storage[key].remove(data)
        #     if len(self.storage[key]) - 1 == self.max:
        #         self.set_status(key, 1)
        #         return 1
        #     else:
        #         return 0
        return -1
    
    def set_status(self, key: str | int, status: int) -> None:
        self.storage.setdefault(key, [{'status': 0, 'ex': 0}])
        self.storage[key][0]['status'], self.storage[key][0]['ex'] = status, time() + self.ex
    
    def get_status(self, key: str | int, status: int) -> None:
        return self.storage.setdefault(key, [{'status': 0, 'ex': 0}])[0]['status']