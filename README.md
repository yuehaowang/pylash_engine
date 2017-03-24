# Pylash Engine
---------------

**Latest Version: 1.5.0**

`Pylash` is a game engine for `python`. We develop `pylash` in `python3` and the GUI engine of `pylash` is `PyQt4`. With `pylash`, you could create games in a simple way.


## License: MIT License

We use [MIT License](http://en.wikipedia.org/wiki/MIT_License), which is a kind of free and friendly license. Also of note, you should follow the license of `PyQt4` as well, because `pylash` is based on it.


## Why Pylash

`Pylash` is intended for creating games in a simple way. Some leading benefits making `pylash` outstand are listed below:

1. Cross-platform. No matter which computer OS you choose, if `python3` and `PyQt4` are both available on it, `pylash` is available as well.
2. Powerful. `Pylash` provides plenty of useful classes which almost come from `ActionScript 3`, a script language for `flash`. As we all know, `flash` is a good tool for creating games and animations. Therefore, `Pylash` takes in some of its advantages aiming to make creating game in `pylash` as easy as `flash`.
3. Easy-to-get-started. It's really easy to get started with `pylash` because you don't need to follow many complex steps if you want to install it. Just install `python3` and `PyQt4` in advance and all preparations are done. Without any configurations but only to download source files and copy them into your project directory, it's already available to use `pylash` in your project. (P.S. You may have trouble installing and configuring `PyQt4`. However, don't be worried, for there are many tutorials on the Internet to tell you how to get it done.)

With every plus there must be a minus, `pylash` remains improved and enhanced. `Pylash` is not designed for creating commercial products because it is not run by a team or a company. But `pylash` will be a good helper for those who are freshmen in developing game and who dream of creating their own games.


## Get Pylash

**With Git:**

Input this command in `Git Bash` to clone `pylash`:

```
git clone git@github.com:yuehaowang/pylash_engine.git
```

**Without Git:**

The url to download the engine is here: 

[https://github.com/yuehaowang/pylash_engine/archive/master.zip](https://github.com/yuehaowang/pylash_engine/archive/master.zip)


## Before Using Pylash

For `pylash` is based on `Python3` and `PyQt4`, you need to install them in advance.

**Python3 will be found here:**

[https://www.python.org/](https://www.python.org/)

**PyQt4 will be found here:**

[https://riverbankcomputing.com/software/pyqt/intro](https://riverbankcomputing.com/software/pyqt/intro)


## Support

If you find that certain bugs exist in `pylash` or that you have any questions or advice, please let us know:

> **My email:** wangyuehao1999@gmail.com
> 
> **My twitter:** [https://twitter.com/yuehaowang](https://twitter.com/yuehaowang)

Bugs can be submitted into [Github Issues](https://github.com/yuehaowang/pylash_engine/issues) as well.


## Demo Screenshots

- **Find Character**

![Demo 1](http://images.cnblogs.com/cnblogs_com/yorhom/731449/o_3.png)

- **Get Fruits**

![Demo 2](http://images.cnblogs.com/cnblogs_com/yorhom/731449/o_2.png)

- **Tower Defense**

![Demo 3](http://images.cnblogs.com/cnblogs_com/yorhom/731449/o_5.png)


## Get Started

- [Overview of Pylash](https://github.com/yuehaowang/pylash_engine/wiki/Overview-of-Pylash)
- [A Simple Program: Hello World](https://github.com/yuehaowang/pylash_engine/wiki/A-Simple-Program:-Hello-World)
- [Load and Display An Image](https://github.com/yuehaowang/pylash_engine/wiki/Load-and-Display-An-Image)
- [Sprite and Mouse Event](https://github.com/yuehaowang/pylash_engine/wiki/Sprite-and-Mouse-Event)
- [Create Vector Graphics](https://github.com/yuehaowang/pylash_engine/wiki/Create-Vector-Graphics)


## Documentation

Documentation comes soon...

## Changelog for 1.5.0

1. Added `Sprite.hitTestObject` method to test collision with other objects.
2. Added `Sprite.addShape` method to add a shape to `Sprite` objects for testing collision.
3. Added 'run.py', which is tool to run demo and examples. Try command `python run.py examples.example_name` to run an example while try command `python run.py demo.demo_name` to run a demo.
4. Added more demo. Check them in 'demo/' directory.