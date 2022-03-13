from time import perf_counter


class Timer:
    def __init__(self):
        self.t_start = None
        self.t_end = None
        self.start()

    def start(self):
        self.t_start = perf_counter()

    def stop(self):
        self.t_end = perf_counter()

    def get_time(self):
        if self.t_end is not None:
            return self.t_end - self.t_start
        return perf_counter() - self.t_start

    def print_time(self, text=''):
        print(self.return_time_text(text))

    def return_time_text(self, text=''):
        return f'\t| {text}{self.get_time():0.4f}s'
