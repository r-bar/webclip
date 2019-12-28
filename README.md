# WebClip
A simple web UI for interacting with a remote clipboard. Currently supports
using a `tmux` buffer as the clipboard backend.

## Installation (pip)
```
pip install https://github.com/r-bar/webclip/archive/master.zip
```

## Installation (pipx)
```
pipx install --spec https://github.com/r-bar/webclip/archive/master.zip webclip
```

## Running
```
webclip [HOST] [PORT]
```

## Usage
* `GET /`: A web UI for interacting with the clipboard. Displays the current
  clipboard and a form for posting new content.
* `POST /`: The form target for the web UI. Accepts a form encoded body with a
  single attribute, `data`, that contains the new clipboard contents.
* `GET /clipboard`: Get the clipboard content directly as the response body.
  Useful for use with `curl`.
* `POST /clipboard`: Set the clipboard content from the request body. Useful for
  use with `curl`.
