import sys
import signal
import argparse
import readline

from config import *
import handlers


def exit(signal_num, sign):
    sys.exit(signal_num)


signal.signal(signal.SIGINT, exit)
signal.signal(signal.SIGTERM, exit)


def handler(command, command_child):
    getattr(handlers, 'handle_%s_%s' % (command, command_child))(command, command_child)


def main():
    parser = argparse.ArgumentParser(description='Power Control ClI.')
    parser.add_argument('-v', '--version', help="version of Power Control ClI.",
                        action='version', version=VERSION)
    parser.add_argument("--command", type=str, required=False)
    parser.add_argument("--child", type=str, required=False)
    args = parser.parse_args()
    if args.command:
        handler(args[1], args[2])
        return
    command_str = ', '.join(['%s:%s' % (COMMAND_LIST.index(i), i['command'])
                             for i in COMMAND_LIST])
    while True:
        option = input('%s\n' % command_str).strip()
        command = ''
        cms = []
        if option.isdigit():
            try:
                command = COMMAND_LIST[int(option)]['command']
                cms = COMMAND_LIST[int(option)]['list']
            except:
                print('input error')
                continue
        else:
            if option == 'exit':
                break
            for i in COMMAND_LIST:
                if i['command'] == option:
                    command = i['command']
                    cms = i['list']
        if not command:
            print('input error')
            continue

        cms_str = ', '.join(['%s:%s' % (cms.index(i), i) for i in cms])
        option = input('%s\n' % cms_str).strip()
        command_child = ''
        if option.isdigit():
            command_child = cms[int(option)]
        else:
            if command_child not in cms:
                print('input error')
                continue
            command_child = option
        handler(command, command_child)


if __name__ == '__main__':
    main()
