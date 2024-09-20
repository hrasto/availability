# availability.py
Python command line program to help you decide meeting times. 
There is currently no error handling, so you need to follow the instructions.

#### Example 1
```
python availability.py example.csv
```
Output: 
```
Best slot(s):

6 available on MO 10:45
Charlie Evans, David Clark, Ivy Wilson, Jane Smith, John Doe, Leo Martinez

6 available on FR 09:30
Alice Johnson, Bob Brown, David Clark, Eva Green, Grace Lee, Jack Taylor

6 available on FR 09:45
Alice Johnson, Bob Brown, David Clark, Eva Green, Grace Lee, Jack Taylor

```

#### Example 2
```
python availability.py example.csv -f 14
```
Translated as: give me the 3 best timeslots that are no earlier than 14:00. 

Output: 
```
Best slot(s):

6 available on FR 15:00
Alice Johnson, Bob Brown, David Clark, Jack Taylor, Jane Smith, Karen Scott

6 available on FR 15:15
Alice Johnson, Bob Brown, David Clark, Jack Taylor, Jane Smith, Karen Scott

6 available on FR 15:30
Alice Johnson, Bob Brown, David Clark, Jack Taylor, Jane Smith, Karen Scott
```

#### Example 3
```
python availability.py example.csv -n 2 -b 5 -s 8
```
Translated as: give me the 5 best timeslot pairs, where everyone is available on at least one of the timeslots, and the timeslot is 2 hours long (8*15min). 

Output: 
```
Best slot(s):

10 available on FR 08:00 or TU 09:00
Alice Johnson, Bob Brown, David Clark, Frank Harris, Grace Lee, Ivy Wilson, Jack Taylor, Jane Smith, John Doe, Leo Martinez

10 available on FR 08:15 or TU 09:00
Alice Johnson, Bob Brown, David Clark, Frank Harris, Grace Lee, Ivy Wilson, Jack Taylor, Jane Smith, John Doe, Leo Martinez

10 available on FR 08:30 or TU 09:00
Alice Johnson, Bob Brown, David Clark, Frank Harris, Grace Lee, Ivy Wilson, Jack Taylor, Jane Smith, John Doe, Leo Martinez

10 available on FR 08:45 or TU 09:00
Alice Johnson, Bob Brown, David Clark, Frank Harris, Grace Lee, Ivy Wilson, Jack Taylor, Jane Smith, John Doe, Leo Martinez

10 available on FR 09:00 or TU 09:00
Alice Johnson, Bob Brown, David Clark, Frank Harris, Grace Lee, Ivy Wilson, Jack Taylor, Jane Smith, John Doe, Leo Martinez

```

#### Full Usage


```
usage: python availability.py [-h] [-n NUM_SLOTS] [-b BEST_N] [-s SLOT_SIZE]
                              [-d WEEKDAYS [WEEKDAYS ...]] [-f FIRST_HR] [-l LAST_HR]
                              filename

positional arguments:
  filename              path to the .csv file containing availability data

optional arguments:
  -h, --help            show this help message and exit
  -n NUM_SLOTS, --num_slots NUM_SLOTS
                        how many slots can you afford (takes the union of available people
                        between slots)
  -b BEST_N, --best_n BEST_N
                        how many slot candidates to print in order from best to worst
  -s SLOT_SIZE, --slot_size SLOT_SIZE
                        integer slot size, each unit is 15 minutes, so 6 implies 1h30min slot
                        size
  -d WEEKDAYS [WEEKDAYS ...], --weekdays WEEKDAYS [WEEKDAYS ...]
                        weekdays to consider; they match the first 2 letters used in the
                        availability entries of the .csv
  -f FIRST_HR, --first_hr FIRST_HR
                        hour that the day starts
  -l LAST_HR, --last_hr LAST_HR
                        hour that the day ends

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
```
