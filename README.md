# Pylash Engine
---------------

**Latest Version: 1.2.1**

`Pylash` is a game engine for `python` which imitates some classes and functions in `flash`. We develop `pylash` with `Python3` and the GUI engine of `pylash` is `PyQt4`. Many classes which are almost from `flash` such as `Sprite`, `BitmapData`, `Bitmap`, `TextField`, `Loader` and `Graphics` will be found in `pylash`.


## License: MIT License

We use [MIT License](http://en.wikipedia.org/wiki/MIT_License), which is a free and friendly license. Besides, you must follow the license of `PyQt4` as well, because `pylash` is based on it.


## Get Pylash

**With Git:**

Input this command in `Git Bash` to clone `pylash`:

```
git clone git@github.com:yuehaowang/pylash_engine.git
```

**Without Git:**

The url to download the engine is: 

[https://github.com/yuehaowang/pylash_engine/archive/master.zip](https://github.com/yuehaowang/pylash_engine/archive/master.zip)


## Before Using Pylash

For `pylash` is based on `Python3` and `PyQt4`, you need to install them first.

**Python3 will be found here:**

[https://www.python.org/](https://www.python.org/)

**PyQt4 will be found here:**

[https://riverbankcomputing.com/software/pyqt/intro](https://riverbankcomputing.com/software/pyqt/intro)


## Support

If you find the library has some bugs or that you have any questions or advice, please let me know:

> **My email:** wangyuehao1999@gmail.com
> 
> **My twitter:** [twitter.com/yuehaowang](twitter.com/yuehaowang)

Bugs can be submited into [Github Issues](https://github.com/yuehaowang/pylash_engine/issues) too.


## Demo Screenshots

- **Find Character**

![Demo 1](http://wyh.wjjsoft.com/album/pylash_demo1.png)

- **Get Fruits**

![Demo 2](http://wyh.wjjsoft.com/album/pylash_demo2.png)

- **Tower Defense**

![Demo 2](http://wyh.wjjsoft.com/album/pylash_demo3.png)


## Get Started

- [Overview of Pylash](https://github.com/yuehaowang/pylash_engine/wiki/Overview-of-Pylash)
- [A Simple Program: Hello World](https://github.com/yuehaowang/pylash_engine/wiki/A-Simple-Program:-Hello-World)
- [Load and Display An Image](https://github.com/yuehaowang/pylash_engine/wiki/Load-and-Display-An-Image)
- [Sprite and Mouse Event](https://github.com/yuehaowang/pylash_engine/wiki/Sprite-and-Mouse-Event)


## Documentation

Documentation comes soon...


## Changelog

### version 1.3.0

*Release Date: 11/8/2015*

1. Bugfix: some errors will be thrown when you give a `LinearGradientColor`/`RadialGradientColor`/`ConicalGradientColor` object to `lineStyle` method of `Graphics` class as the second parameter.
2. Added `TweenLite` static class and `TweenLiteChild` class to create some easing animations.
3. Added `Easing` static class to provide many easing methods for `TweenLite` class.
4. Improvement: more detailed internal error hints.
5. Bugfix: cannot use `Button.removeState`.

#### version 1.2.1

*Release Date: 11/1/2015*

1. Added `Shape` class to create vector graphics. It's lighter than `Sprite` when you just want to use vector graphics.
2. Enhancement: efficiency of mouse event.

#### version 1.2.0

*Release Date: 10/7/2015*

1. Added some sample classes about loading page.
2. Added `Button` class to create a simple button.
3. Added `LinearGradientColor`, `RadialGradientColor` and `ConicalGradientColor` class to use gradient color.
4. Added `delay` property in `LoadManage` class to set the delay time between loading a resource and loading the next resource in order to show loading page.
5. Added `useAntialiasing` property in `stage` in order to open/close antialiasing.
6. Bugfix: `onComplete` callback function will be called in the thread used for loading resources in `LoadManage`.
7. Bugfix: `PyQt` will throw errors if `text` property of `TextField` is set to a value whose type is not `str`.
8. Added `mouseShelter` property in `DisplayObjectContainer` to set whether stop propagating mouse events to `DisplayObjectContainer` objects that are sheltered by other objects.
9. Bugfix: `selfY` in mouse event is wrong.
10. Enhancement: the `x` and `y` property in parameter 'bitmapData' given into the constructor of `Animation` class will be the origin position of the animation.
11. Added `AnimationSet` class to control a set of animations.
12. Added `MOUSE_OVER` and `MOUSE_OUT` event.

#### version 1.1.0

*Release Date: 9/20/2015*

1. Improvement: changed and added some methods in `Graphics`.
2. Added settings of `join style`, `cap style` and `miter limit` in `Graphics`.

#### version 1.0.0 

*Release Date: 9/12/2015*

Create `pylash` with `display`, `text`, `system`, `utils` and `events` modules which include `Sprite`, `Bitmap`, `Graphics`, `Loader`, `Stage` and more powerful classes.