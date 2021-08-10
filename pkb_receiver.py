import pkb_server as pkbs

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

def handle_message(msg):
    if 'key_press' in msg.keys():
        keyList = msg['key_press']
        report = ''
        for key in keyList: report += chr(key)
        write_report(report)

s = pkbs.PKBServer(5560, handle_message)