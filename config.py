import os


VERSION = '0.1.0'
if os.path.exists('VERSION'):
    with open('VERSION', 'r') as f:
        VERSION = f.read().strip()
COMMAND_LIST = [
    {
        'command': 'devices',
        'list': ['list', 'power_on', 'power_off', 'reboot']
    },
    {
        'command': 'timer',
        'list': ['list', 'create', 'update', 'delete', 'update_timers']
    }
]

BASE_URL = 'http://127.0.0.1:9033'
DEVICES_LIST_URL = '%s/device/devices' % BASE_URL
DEVICE_STATUS_URL = DEVICES_LIST_URL + '/'
DEVICES_SET_POWER_URL = '%s/device/devices/set_power' % BASE_URL
ROBOT_SHUTDOWN_URL = '%s/device/robot/shutdown' % BASE_URL

TIMERS_URL = '%s/timer/timers' % BASE_URL
TIMERS_UPDATE_URL = '%s/timer/timers/update_timers' % BASE_URL
TIMER_TYPE = ['daily', 'weekly', 'monthly']
TIMER_ID_MIN = 1
TIMER_ID_MAX = 255


TIMER_COMMANDS = [
    {
        "command_id": 1,
        "command": "set_power",
        "args": ["off", "on"]
    },
    {
        "command_id": 2,
        "command": "360_switch",
        "args": ["interaction", "PC"]
    }
]
