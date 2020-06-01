import json
import requests


class Comm:
    def __init__(self, bot_number):
        self.cmd = {'botNo': bot_number}
        self.reset_cmd

    def status(self):
        ip, port = 'localhost', '8080'
        url = f'http://{ip}:{port}/status'
        connected = False
        raw = None
        while not connected:
            try:
                raw = requests.get(url, json=self.cmd)
                connected = True
            except requests.exceptions.ConnectionError:
                print('Connection refused')

        return json.loads(raw.text)

    def send(self):
        ip, port = 'localhost', '8080'
        url = f'http://{ip}:{port}/cmd'

        connected = False
        while not connected:
            try:
                raw = requests.post(url, json=self.cmd)
                connected = True
            except requests.exceptions.ConnectionError:
                print('Connection refused')

        status = json.loads(raw.text)
        self.reset_cmd()

        return status

    def rotate(self, angle):
        if angle < 0.:
            angle = -1
        if angle > 0.:
            angle = 1
        self.cmd['rotation'] = angle

    def move(self, dx, dy):
        if dx < 0.:
            dx = -1
        if dx > 0.:
            dx = 1
        self.cmd['dx'] = dx

        if dy < 0.:
            dy = -1
        if dy > 0.:
            dy = 1
        self.cmd['dy'] = dy

    def shoot(self, val):
        val = True if val else False
        self.cmd['shoot'] = val

    def reset_cmd(self):
        self.cmd['dx'] = 0
        self.cmd['dy'] = 0
        self.cmd['rotation'] = 0
        self.cmd['shoot'] = False
