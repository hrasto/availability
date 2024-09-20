import itertools 
import argparse
import textwrap

parser = argparse.ArgumentParser(
    prog="python availability.py",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=textwrap.dedent('''\
    FILE FORMAT:
                            
    One line of the .csv file is layed out as follows:
        name,entry_1,entry_2,...,entry_n
    Each person can have a different amount of entries.
    This is an example of an entry: MO10451230
    It means available on Monday between 10:45 and 12:30. 
    The first two letters indicate the weekday (corresponding with the days specified in argument --weekdays).
    Two (optional) times follow:
        if the second one is ommitted (MO1045), it implies available from 10:45 until the end of the day,
        if both of them are omitted (MO), it means available the whole Monday.
    An example file can be found here: https://github.com/hrasto/availability/blob/main/example.csv
    '''))


parser.add_argument('filename', help='path to the .csv file containing availability data')
parser.add_argument('-n', '--num_slots', default=1, type=int, help='how many slots can you afford (takes the union of available people between slots)')
parser.add_argument('-b', '--best_n', default=3, type=int, help='how many slot candidates to print in order from best to worst')
parser.add_argument('-s', '--slot_size', default=6, type=int, help='integer slot size, each unit is 15 minutes, so 6 implies 1h30min slot size')
parser.add_argument('-d', '--weekdays', default=['MO', 'TU', 'WE', 'TH', 'FR'], nargs='+', type=str, help='weekdays to consider; they match the first 2 letters used in the availability entries of the .csv')

args = parser.parse_args()

def decode(short): 
    day = short[:2]

    start = 8.0
    if len(short) > 2: 
        start = float(short[2:4]) + float(short[4:6])/60

    stop = 18.5
    if len(short) == 10:
        stop = float(short[6:8]) + float(short[8:10])/60
    
    times = []
    while start <= stop: 
        times.append(start)
        start += 1/4

    return day, times

availability = {}

with open(args.filename) as f: 
    for line in f:
        entries = line.strip().split(',') 
        name = entries[0]
        avails_short = entries[1:]
        avails = []
        for short in avails_short: 
            day, times = decode(short)
            for time in times: 
                avails.append((day, time))
        availability[name] = set(avails)

all_slots = []
for day in args.weekdays: 
    for hr in range(8, 19): 
        for hrpart in range(4):
            slot_start = (hr + hrpart/4)
            times = set((day, slot_start+i*.25) for i in range(args.slot_size))
            slot_name = day+' '+str(slot_start)
            all_slots.append((slot_name, times))

slot_availabiilty = {}
for slots in itertools.product(all_slots, repeat=args.num_slots):
    desc = tuple(sorted(set(slot_name for slot_name, _ in slots)))
    if len(desc) != args.num_slots or desc in slot_availabiilty: continue

    available_students = set()
    for _, times in slots: 
        available_students = available_students.union(name for name, avails in availability.items() if times<=avails)
    slot_availabiilty[desc] = available_students

def format_slot(slot): 
    day, time = slot.split()
    time = float(time)
    hr = int(time)
    mins = int((time-hr)*60)
    return f"{day} {hr:02d}:{mins:02d}"

print("Best slot(s):")
print()
for i, slot in enumerate(itertools.islice(sorted(slot_availabiilty, key=lambda key: len(slot_availabiilty[key]), reverse=True), args.best_n), start=1):
    students = sorted(slot_availabiilty[slot])
    print(f"{len(students)} available on {' or '.join(map(format_slot, slot))}")
    print(', '.join(students))
    print()