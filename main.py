#!/usr/bin/env python3
from argparse import ArgumentParser
from pathlib import Path
import abc
import subprocess

from bottle import route, run, request, SimpleTemplate

SERVER_PATH = Path(__file__).parent
DEFAULT_ENCODING = 'utf-8'
DEFAULT_HOST = '0.0.0.0'
DEFAULT_PORT = 8000


clipboard_html = SimpleTemplate(
    open(SERVER_PATH / 'clipboard.html.jinja').read(),
    data='',
)


def cli():
    p = ArgumentParser()
    p.add_argument('host', nargs='?', default=DEFAULT_HOST)
    p.add_argument('port', nargs='?', type=int, default=DEFAULT_PORT)
    return p


class ClipboardBackend(abc.ABC):

    @abc.abstractmethod
    def copy(self, data):
        """Write data to the clipboard"""
        raise NotImplemented

    @abc.abstractmethod
    def paste(self, ):
        """Ouput the contents of the clipboarrd"""
        raise NotImplemented


class TmuxBuffer(ClipboardBackend):
    def copy(self, data, encoding=DEFAULT_ENCODING):
        if not isinstance(data, bytes):
            data = str(data).encode(encoding)

        process = subprocess.Popen(['tmux', 'load', '-'],
                                   stdout=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
        process.stdin.write(data)
        process.stdin.close()
        retcode = process.wait(5)
        if retcode != 0:
            raise Exception('Error copying data')

    def paste(self):
        process = subprocess.run(['tmux', 'save', '-'], check=True,
                                 capture_output=True)
        if process.returncode != 0:
            raise Exception('Error getting clipboard data')

        return process.stdout


backend = TmuxBuffer()


@route('/clipboard', method='GET')
def read_clipboard():
    return backend.paste()


@route('/clipboard', method='POST')
def write_clipboard():
    backend.copy(request.body())


@route('/', method='GET')
def clipboard_form():
    return clipboard_html.render(data=backend.paste())


@route('/', method='POST')
def clipboard_form_target():
    data = request.POST.get('data')
    backend.copy(data)
    return clipboard_html.render(data=data)


if __name__ == '__main__':
    args = cli().parse_args()
    run(host=args.host, port=args.port)
