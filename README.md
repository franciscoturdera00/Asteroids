
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

## About Asteroids

`Player`: Can thrust forward, rotate left, rotate right, and shoot lasers

![Player](https://github.com/franciscoturdera00/Asteroids/blob/main/Images/player.png?raw=true)

`Asteroid`: A moving obstacle of varying sizes. Watch out, asteroid trajectory is slightly are affected by the gravitational pull of the player!

![Asteroid](https://github.com/franciscoturdera00/Asteroids/blob/main/Images/asteroid.png?raw=true)

`Alien`: A smart opponent that will move towards your position at various speeds and intervals.

![Alien](https://github.com/franciscoturdera00/Asteroids/blob/main/Images/alien.png?raw=true)

### Items

`Bullet`: An extra bullet added to the player's arsenal

![Bullet](https://github.com/franciscoturdera00/Asteroids/blob/main/Images/shot.png?raw=true)

`Black Hole`: A growing black hole that destroys everything it touches

![Nuke](https://github.com/franciscoturdera00/Asteroids/blob/main/Images/nuke.png?raw=true)


