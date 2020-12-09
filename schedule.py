from datetime import datetime
import time
from discord_notify import notify
from main import run, time_wait


schedule = {
    0: [
        [
            "BTN 457 | Adv. Virology",
            11,
            12
        ]
    ],
    1: [
        [
            "Biomolecular NMR",
            10,
            11
        ]
    ],
    
    2: [
        [
            "Biomolecular NMR",
            11,
            12
        ]
    ],
    
    3: [
        [
            "BTN 457 | Adv. Virology",
            10,
            11
        ]
    ],
    
    4: [
        [
            "Biomolecular NMR",
            10,
            11
        ],
        [
            "BTN 457 | Adv. Virology",
            11,
            12
        ]
    ],
    
    5: [],
    
    6: [],
    
    'test':[
            [
                "Azad", 
                11, 
                12
            ],
            [
                "Biomolecular NMR", 
                13, 
                15
            ]
    ]           }


def scheduler():
    day = datetime.now().weekday()
    
    #testcase
    #day = 'test'
    
    if day in range(5):
        schedule_today = schedule[day]
        start = schedule_today[0][1]
        if start > datetime.now().hour:
            txt = f"Waiting for the first class to start at {start}"
            notify(txt)
            print(txt)
            time.sleep(time_wait(start))
            run(schedule_today)
        else:
            txt = "Start time already passed for the first class"
            notify(txt)
            print(txt)
    else:
        txt = 'No classes scheduled for today!'
        # notify on discord
        notify(txt)
        print(txt)
        return


scheduler()


    

