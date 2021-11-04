# Image Stream Push Server

### 简介

​	通过浏览器网页实时查看图像处理结果。

### 环境

​	运行程序需要安装一下python依赖：

- tornado: 用于创建http及websocket服务；
- opencv-contrib-python: 用于图像数据源获取及图像处理。

### 使用

1. 进入到src目录，启动web服务：

```python
python webserver.py
```

2. 打开浏览器，输入http://localhost:8050/；
3. 进入到src目录，启动图像处理demo：

```python
python producer.py
```



### 原理

![](resource/arch.png)