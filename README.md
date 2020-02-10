# Pylash Engine
---------------

**Latest Version: 2.0.0**

*Pylash* is a modern and cross-platform 2D game engine written in *Python*. With modern and practical interfaces provided by *pylash*, you can create games in an easy and relaxed way.


## License

[MIT License](http://en.wikipedia.org/wiki/MIT_License)


## Why Pylash

1. Cross-platform. Leveraging compatibility of the underlying engine *PySide2*, *pylash* supports many mainstream platforms including Ubuntu, macOS and Windows.
2. Easy-to-use APIs. *Pylash* adopts ActionScript-like interface designs to raise the efficiency of game developing.
3. Lightweight. *Pylash* does not come with piles of third-party tools and frameworks.
4. Comprehensiveness. *Pylash* is a universal framework and provides various object-oriented interfaces including display of images, text and vector graphics, collision detection, tween animation, multimedia, etc.


## Get Started with *Pylash*

### Installation

```bash
$ pip install pylash-engine
```

### Hello World Program

Create a *Python* file and open it with your favorite text editor. Type in the code below:

```python
from pylash.core import init, addChild
from pylash.display import TextField

def main():
    txt = TextField()
    txt.text = "Hello World"
    txt.size = 40
    txt.x = txt.y = 100
    addChild(txt)

init(30, "Hello World", 400, 300, main)
```

Run the *Python* file and you will get a window with a "Hello World" text.


## Contributing

This project is hosted [on Github](https://github.com/yuehaowang/pylash_engine). Issue reports and pull requests are welcome. In addition, you can drop me an email if you have any question or suggestion.

- My email: wangyuehao1999@gmail.com


## Example Screenshots

- **Find Character**

![Find Character](https://github.com/yuehaowang/pylash_engine/raw/master/doc/images/find_character.png)

- **Get Fruits**

![Get Fruits](https://github.com/yuehaowang/pylash_engine/raw/master/doc/images/get_fruits.png)

- **Tower Defense**

![Tower Defense](https://github.com/yuehaowang/pylash_engine/raw/master/doc/images/tower_defense.png)


<!-- ## Get Started

- [Overview of Pylash](https://github.com/yuehaowang/pylash_engine/wiki/Overview-of-Pylash)
- [A Simple Program: Hello World](https://github.com/yuehaowang/pylash_engine/wiki/A-Simple-Program:-Hello-World)
- [Load and Display An Image](https://github.com/yuehaowang/pylash_engine/wiki/Load-and-Display-An-Image)
- [Sprite and Mouse Event](https://github.com/yuehaowang/pylash_engine/wiki/Sprite-and-Mouse-Event)
- [Create Vector Graphics](https://github.com/yuehaowang/pylash_engine/wiki/Create-Vector-Graphics)


## Documentation

Documentation comes soon... -->

## Changelog for 2.0.0

1. Port base engine from *PyQt4* to *PySide2*.
2. Removed modules: `text`, `system`, `net`.
3. Renamed modules: `utils` => `core`.
4. Added `loaders` module, providing various loaders for different resource types.
5. Moved `TextField` class and related classes to `display` module.
6. Enhanced `LineEdit` class: added focus-in event and focus-out event.
7. Substitute *Phonon* with *QtMultimedia* as multimedia engine.
8. Added `Video` class in `media` module for displaying videos.
9. Improved event system. Listener will not receive an event dispatcher as the parameter anymore.
10. Added more demo.
11. Added docstring for `core` module.

<!-- ## Changelog for 1.5.0 -->

<!-- 1. Added `Sprite.hitTestObject` method to test collision with other objects.
2. Added `Sprite.addShape` method to add a shape to `Sprite` objects for testing collision.
3. Added 'run.py', which is tool to run demo and examples. Try command `python run.py examples.example_name` to run an example while try command `python run.py demo.demo_name` to run a demo.
4. Added more demo. Check them in 'demo/' directory. -->