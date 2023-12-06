from datetime import timedelta, datetime


def sort_list(timetable: list):
    """
    сортировка первоначального расписания в хронологическом порядке по возрастанию

    """
    if not timetable:
        return timetable

    def merging(early_table, later_table):
        new_table = []
        while True:
            element_earl = early_table[0]
            element_late = later_table[0]
            x = element_earl['start']
            y = element_late['start']
            if element_earl['start'] < element_late['start']:

                element = early_table.pop(0)
            else:
                element = later_table.pop(0)
            new_table.append(element)
            if not early_table:
                new_table += later_table
                break
            if not element_late:
                new_table += early_table
                break
        return new_table

    if len(timetable) == 1:
        return timetable

    middle = len(timetable) // 2
    new_earl_timetable = sort_list(timetable[:middle])
    new_late_timetable = sort_list(timetable[middle:])
    return merging(new_earl_timetable, new_late_timetable)


class Appoint:
    def __init__(self, busy_list: list, strt_t, stop_t, interval):
        self.delta = timedelta(minutes=int(interval))
        self.busy = busy_list.copy()
        self.freetime_list = []
        hm = strt_t.split(':')
        hm1 = stop_t.split(':')
        self._start = datetime(2023, 1, 1, 0, 0) \
                      + timedelta(hours=int(hm[0]), minutes=float(hm[1]))
        self._stop = datetime(2023, 1, 1, 0, 0) \
                     + timedelta(hours=int(hm1[0]), minutes=float(hm1[1]))
        self._init_timetable()
        self.run_plan()

    def _init_timetable(self):
        for i in self.busy:
            init = i['start'].split(':')
            finish = i['stop'].split(':')
            i['start'] = datetime(2023, 1, 1, 0, 0) \
                         + timedelta(hours=int(init[0]), minutes=float(init[1]))
            i['stop'] = datetime(2023, 1, 1, 0, 0) \
                        + timedelta(hours=int(finish[0]), minutes=float(finish[1]))

        return self.freetime_list

    def __str__(self):
        str_ = ''
        for i in self.freetime_list:
            str_ += f"'start': {i['start'].strftime('%H:%M')}, 'stop': {i['stop'].strftime('%H:%M')}\n"
        return str_

    def run_plan(self):

        while self._start + self.delta <= self._stop:
            if len(self.busy) > 0:
                element = self.busy.pop(0)
                while self._start < element['start']:
                    if (self._start + self.delta) > (element['start']):
                        self._start = element['stop']
                    else:
                        self.new_record()
                        self._start += self.delta
                        if self._start >= element['start']:
                            self._start = element['stop']

            else:
                break
        if self._start + self.delta <= self._stop:
            self.new_record()
            self._start += self.delta

    def new_record(self):
        new_rec = {}
        new_rec['start'] = self._start
        new_rec['stop'] = self._start + self.delta

        self.freetime_list.append(new_rec)


if __name__ == '__main__':
    busy = [
        {'start': '10:30',
         'stop': '10:50'},
        {'start': '18:40',
         'stop': '18:50'},
        {'start': '14:40',
         'stop': '15:50'},
        {'start': '16:40',
         'stop': '17:20'},
        {'start': '20:05',
         'stop': '20:20'}
        ]
    #  print(sort_list(busy))
    start_time = '9:00'
    stop_time = '21:00'
    interval_ = '30'

    busy = sort_list(busy)

    wind = Appoint(busy, start_time, stop_time, interval_)
    print(wind)
