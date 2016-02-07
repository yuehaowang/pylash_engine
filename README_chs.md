# Pylash引擎
---------------

[**English**](https://github.com/yuehaowang/pylash_engine/blob/master/README.md)
|
[**中文**](https://github.com/yuehaowang/pylash_engine/blob/master/README_chs.md)

**最新版本：1.4.0**

`Pylash`是一个`python`游戏引擎，它模仿了一些`flash`中的类和功能。我们使用`Python3`和GUI引擎`PyQt4`开发`pylash`。许多来自`flash`的类，例如：`Sprite`，`BitmapData`，`Bitmap`，`TextField`，`Loader`，`Graphics`都可以在`pylash`中被找到。


## 开源协议：MIT License

我们使用[MIT License](http://en.wikipedia.org/wiki/MIT_License)，它是一个免费、友好的协议。除此之外，你也必须遵守`PyQt4`的协议，因为`pylash`是基于它开发而来。


## 获取Pylash

**使用Git:**

在`Git Bash`输入以下命令来对`pylash`进行clone:

```
git clone git@github.com:yuehaowang/pylash_engine.git
```

**不使用Git:**

以下是下载该引擎的地址： 

[https://github.com/yuehaowang/pylash_engine/archive/master.zip](https://github.com/yuehaowang/pylash_engine/archive/master.zip)


## 在使用Pylash之前

由于`pylash`是基于`Python3`和`PyQt4`的，所以你需要首先安装它们。

**Python3可以在这里被找到：**

[https://www.python.org/](https://www.python.org/)

**PyQt4可以在这里被找到：**

[https://riverbankcomputing.com/software/pyqt/intro](https://riverbankcomputing.com/software/pyqt/intro)


## 支持

如果你发现库件存在bug，或者你有任何问题或者意见，请让我们知道。

> **我的邮箱：** wangyuehao1999@gmail.com
> 
> **我的微博：** [http://weibo.com/yorhomwang](http://weibo.com/yorhomwang)

你也可以到[Github Issues](https://github.com/yuehaowang/pylash_engine/issues)提交bug。


## 示例截图

- **找汉字**

![Demo 1](http://images.cnblogs.com/cnblogs_com/yorhom/731449/o_pylash_demo1.png)

- **接水果**

![Demo 2](http://images.cnblogs.com/cnblogs_com/yorhom/731449/o_pylash_demo2.png)

- **塔防**

![Demo 3](http://images.cnblogs.com/cnblogs_com/yorhom/731449/o_pylash_demo3.png)


## 入门教程

- [Overview of Pylash](https://github.com/yuehaowang/pylash_engine/wiki/Overview-of-Pylash)
- [A Simple Program: Hello World](https://github.com/yuehaowang/pylash_engine/wiki/A-Simple-Program:-Hello-World)
- [Load and Display An Image](https://github.com/yuehaowang/pylash_engine/wiki/Load-and-Display-An-Image)
- [Sprite and Mouse Event](https://github.com/yuehaowang/pylash_engine/wiki/Sprite-and-Mouse-Event)
- [Create Vector Graphics](https://github.com/yuehaowang/pylash_engine/wiki/Create-Vector-Graphics)


## 文档

即将发布……


## 更新日志

### 版本 1.4.0

*发布日期：2/7/2016*

1. 【强化】你可以设置`DisplayObject`的`width`&`height`属性来限制显示对象的显示尺寸。
2. 在`media`模块中加入了`Sound`类用于播放音频。
3. 【强化】你可以使用`LoadManage.load`来加载音频。
4. 【改进】`LoadManage`以前使用`threading.thread`来创建新线程，目前使用`QThread`。

### 版本 1.3.3

*发布日期：1/10/2016*

1. 在`ui`模块中加入了`LineEdit`类，用于创建单行输入框。
2. 在`system`模块中加入了`RankingSystem`，它用于连接服务器并发送新增/获取排名的请求。
3. 在`net`模块中加入了`RankingServer`，它是一个配合`RankingSystem`使用的`socket`服务器。
4. 【Bug修复】在`TweenLite`中无法使用`onComplete`&`onStart`&`onUpdate`属性。

### 版本 1.3.2

*发布日期：12/26/2015*

1. 在`ui`模块中加入了`ButtonSample`，用来创建一个简单的按钮。一般而言，它用于测试。
2. 在`media`模块中加入了`StageWebView`，用来在窗口中显示网页。

### 版本 1.3.1

*发布日期：11/21/2015*

1. 在`BitmapData`中加入`draw`方法，用于在`BitmapData`对象中绘制显示对象。
2. 【改进】将绘制`QImage`对象更改为绘制`QPixmap`对象，以提高渲染效率。
3. 在`BitmapData`中加入了`setPixel`，`getPixel`，`setPixels`，`getPixels`方法，用于像素处理。
4. 为一次性进行更快的多次像素处理，在`BitmapData`中加入了`lock`，`unlock`方法。
5. 加入了`Rectangle`类和`Point`类。
6. 【Bug修复】当使用了`moveTo`方法或者`lineTo`方法，获取`Graphics`宽度高度不正确。
7. 【强化】在设置颜色值时，支持hex值。

### 版本 1.3.0

*发布日期：11/8/2015*

1. 【Bug修复】当你把`LinearGradientColor`/`RadialGradientColor`/`ConicalGradientColor`对象作为第二个参数传入`Graphics`的`lineStyle`方法时，会报错。
2. 加入了`TweenLite`静态类和`TweenLiteChild`类，用于创建缓动动画。
3. 加入了`Easing`静态类，用以为`TweenLite`类提供缓动方法。
4. 【改进】更详细的内部报错机制。
5. 【Bug修复】无法使用`Button.removeState`。

#### 版本 1.2.1

*发布日期：11/1/2015*

1. 加入了`Shape`类，用于创建矢量图形。当你创建矢量图形时，它比`Sprite`更高效。
2. 【强化】鼠标事件的效率。

#### 版本 1.2.0

*发布日期：10/7/2015*

1. 加入了几款加载界面的示例进度条。
2. 加入了`Button`类，用于创建简单的按钮。
3. 加入了`LinearGradientColor`，`RadialGradientColor`，`ConicalGradientColor`类，用于创建渐变色。 
4. 在`LoadManage`类中加入`delay`属性，通过这个属性，你可以设置加载资源与加载下一个资源的时间间隔，通常用于显示加载界面。
5. 在`stage`中加入`useAntialiasing`属性，用于打开/关闭反走样。
6. 【Bug修复】`LoadManage`中，`onComplete`回调函数会在用于加载资源的线程中被调用。
7. 【Bug修复】`PyQt`会报错，如果`TextField`的`text`属性被设置为一个不是`str`类型的值。
8. 在`DisplayObjectContainer`中加入了`mouseShelter`属性，用于设置是否停止对被其他对象遮住的显示对系那个传递鼠标事件。
9. 【Bug修复】鼠标事件的`selfY`出错。
10. 【强化】给入`Animation`类的'bitmapData'参数的`x`，`y`属性会作为动画的起始位置。 
11. 加入了`AnimationSet`类来控制一组动画。
12. 加入了`MOUSE_OVER`和`MOUSE_OUT`事件。

#### 版本 1.1.0

*发布日期：9/20/2015*

1. 【改进】更改和新增了`Graphics`中的方法。
2. 在`Graphics`中加入了对`join style`，`cap style`的设置。

#### 版本 1.0.0 

*发布日期：9/12/2015*

创建`pylash`，涵盖了`display`，`text`，`system`，`utils`以及`events`模块。其中有`Sprite`，`Bitmap`，`Graphics`，`Loader`，`Stage`以及更多的功能强大的类。