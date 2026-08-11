import win32evtlog

def detect_unauthorized_access():
    alerts = []

    try:
        logtype = 'Security'
        hand = win32evtlog.OpenEventLog(None, logtype)

        flags = win32evtlog.EVENTLOG_BACKWARDS_READ | win32evtlog.EVENTLOG_SEQUENTIAL_READ
        events = win32evtlog.ReadEventLog(hand, flags, 0)

        for event in events:
            if event.EventID == 4625:
                alerts.append("Failed Login Attempt Detected")

    except:
        print("Run as Administrator to read Security logs")

    return alerts