import itertools 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('filename')
parser.add_argument('-n', '--num_slots', default=1, type=int)
parser.add_argument('-b', '--best_n', default=3, type=int)
parser.add_argument('-s', '--slot_size', default=6, type=int)
parser.add_argument('-d', '--weekdays', default=['MO', 'TU', 'WE', 'TH', 'FR'], nargs='+', type=str)

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

print("Best slot(s):")
print()
for i, slot in enumerate(itertools.islice(sorted(slot_availabiilty, key=lambda key: len(slot_availabiilty[key]), reverse=True), args.best_n), start=1):
    students = sorted(slot_availabiilty[slot])
    print(f"{len(students)} available on {', '.join(slot)}")
    print(', '.join(students))
    print()