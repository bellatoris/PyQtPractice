# Closing a window

```python
qbtn.clicked.connect(QtCore.QcoreApplication.instance().quit)
```

PyQt5 의 event processing system 은 signal & slot mechanism 으로 만들어져있다. 
Button 을 click 하면, `clicked` signal 이  보내진다. Slot 은 Qt slot 혹은 아무런 
Python callable 이 될 수 있다. `QtCore.QCoreApplication` 은 event main loop 를 들고 있고, 
모든 event 를 처리하고 전달한다. 예제에서는 `quit` method 를 binding 해서, button 을 click 
하면 application 이 꺼지게 하였다.
