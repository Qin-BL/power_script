import json
import urllib
import requests
from config import *


# devices
def handle_devices_list(command, command_child):
    option = input('device id or press Enter to list all: ')

    if not option:
        res = requests.get(DEVICES_LIST_URL)
        print(json.loads(res.content)["ret"])
        return
    if not option.isdigit():
        print('input error')
        return
    res = requests.get(urllib.parse.urljoin(DEVICE_STATUS_URL, option))
    print(json.loads(res.content)["ret"])


def handle_devices_set_power(op):
    option = input('device ids[1,2,3...]: ').strip()
    try:
        device_ids = [int(i) for i in option.split(',') if i]
    except:
        print('input error')
        return
    body = {
        'op': op,
        'devices': device_ids
    }
    res = requests.post(DEVICES_SET_POWER_URL, json=body)
    print(res.content)


def handle_devices_power_on(command, command_child):
    handle_devices_set_power(command_child)


def handle_devices_power_off(command, command_child):
    handle_devices_set_power(command_child)


def handle_devices_reboot(command, command_child):
    handle_devices_set_power(command_child)


def handle_robot_shutdown(command, command_child):
    res = requests.get(ROBOT_SHUTDOWN_URL)
    print(res.content)


# timer
def handle_timer_list(command, command_child):
    option = input('device id or press Enter to list all: ')

    if not option:
        res = requests.get(TIMERS_URL)
        print(json.loads(res.content)["ret"])
        return
    if not option.isdigit():
        print('input error')
        return
    res = requests.get(urllib.parse.urljoin(TIMERS_URL+'/', option))
    print(json.loads(res.content)["ret"])


def get_timer_id():
    res = requests.get(TIMERS_URL)
    timers = json.loads(res.content)["ret"]
    if not timers:
        return TIMER_ID_MIN
    tmp = TIMER_ID_MIN
    for i in timers:
        if (i['id'] - tmp) > 1:
            return i["id"] - 1
        else:
            tmp = i["id"]
    timer_id = tmp + 1
    if timer_id > 255:
        print("timer queue full !")
    return timer_id


def handle_timer_create(command, command_child):
    timer_id = get_timer_id()
    try:
        command_id = int(input('command id[%s]: ' % ';'.join(
            ['%s:%s' % (i["command_id"], i["command"]) for i in TIMER_COMMANDS])).strip())
        args = []
        for i in TIMER_COMMANDS:
            if i["command_id"] == command_id:
                args = i["args"]
        command_arg = int(input('command arg[%s]: ' % ';'.join(['%s:%s' % i for i in enumerate(args)])).strip())
        device_ids = [int(i) for i in input('device ids[1,2,3...]: ').strip().split(',') if i]
        minute = int(input('minute: ').strip())
        hour = int(input('hour: ').strip())
        timer_type = input('timer type%s: ' % json.dumps(TIMER_TYPE)).strip()
        if timer_type not in TIMER_TYPE:
            print('input error')
            return
        days_of_month = [int(i) for i in input('days_of_month[1,2,3...]: ').strip().split(',')
                         if 0 < int(i) < 32]
        days_of_week = [int(i) for i in input('days_of_week[0:Sunday,1:Monday...]: ').strip().split(',')
                        if 0 < int(i) < 8]
    except:
        print('input error')
        return
    res = requests.post(TIMERS_URL, json={
        "id": timer_id,
        "command": command_id,
        "arg": command_arg,
        "devices": device_ids,
        "minute": minute,
        "hour": hour,
        "day_type": timer_type,
        "days_of_month": days_of_month,
        "days_of_week": days_of_week
    })
    print(res.content)


def handle_timer_update(command, command_child):
    res = requests.get(TIMERS_URL)
    timers = json.loads(res.content)["ret"]
    print(timers)
    if not timers:
        print("no timers")
        return
    timer_ids = [i['id'] for i in timers]
    try:
        timer_id = int(input('update timer id: ').strip())
        if timer_id not in timer_ids:
            print("has not this timer")
            return
        command_id = int(input('command id[%s]: ' % ';'.join(
            ['%s:%s' % (i["command_id"], i["command"]) for i in TIMER_COMMANDS])).strip())
        args = []
        for i in TIMER_COMMANDS:
            if i["command_id"] == command_id:
                args = i["args"]
        command_arg = int(input('command arg[%s]: ' % ';'.join(['%s:%s' % i for i in enumerate(args)])).strip())
        device_ids = [int(i) for i in input('device ids[1,2,3...]: ').strip().split(',') if i]
        minute = int(input('minute: ').strip())
        hour = int(input('hour: ').strip())
        timer_type = input('timer type%s: ' % json.dumps(TIMER_TYPE)).strip()
        if timer_type not in TIMER_TYPE:
            print('input error')
            return
        days_of_month = [int(i) for i in input('days_of_month[1,5,7...]:').strip().split(',')
                         if 0 < int(i) < 32]
        days_of_week = [int(i) for i in input('days_of_week[1,3,5...]:').strip().split(',')
                        if 0 < int(i) < 8]
    except:
        print('input error')
        return
    res = requests.put(urllib.parse.urljoin(TIMERS_URL+'/', str(timer_id)), data=json.dumps({
        "id": timer_id,
        "command": command_id,
        "arg": command_arg,
        "devices": device_ids,
        "minute": minute,
        "hour": hour,
        "day_type": timer_type,
        "days_of_month": days_of_month,
        "days_of_week": days_of_week
    }))
    print(res.content)


def handle_timer_delete(command, command_child):
    res = requests.get(TIMERS_URL)
    print(json.loads(res.content)["ret"])
    try:
        timer_id = int(input('delete timer id: ').strip())
    except:
        print('input error')
        return
    res = requests.delete(urllib.parse.urljoin(TIMERS_URL+'/', str(timer_id)))
    print(json.loads(res.content)["ret"])


def handle_timer_update_timers(command, command_child):
    try:
        timer_list = json.loads(input('enter update timers list: ').strip())
        print(type(timer_list))
    except:
        print('input error')
        return
    fail_list = []
    for timer in timer_list:
        try:
            res = requests.put(urllib.parse.urljoin(TIMERS_URL+'/', str(timer["id"])), data=json.dumps(timer))
        except:
            fail_list.append(timer)
    if fail_list:
        print("update fail timers")
        print(fail_list)
