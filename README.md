
# Asteroids

A recreation of the popular game [Asteroids](https://en.wikipedia.org/wiki/Asteroids_(video_game)) with `pygame`


## Prerequisites:
```
python 3.13.1 or later
```

## On ~/.../Asteroids:

### Recommended
#### Create Virtual Environment:
```
python -m venv .venv
```
Use `.venv/Scripts/python.exe` instead of `python` below.

### Required

#### Install requirements:

```
python -m pip install -r requirements.txt
```

#### Run game:
```
python main.py
```

### Optional 

### Create Local Executable
```
pyinstaller main.py
```
##### Copy `Sounds` and `Fonts` folders into ./dist/main
```
./dist/main/main.exe
```