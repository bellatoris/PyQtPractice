# Hello Qt

모든 PyQt5 application 은 application object 를 생성해야 한다. 

```python
from PyQt5.QtWidgets import QApplication

app = QApplication(sys.argv)
```

`QWidget` 는 모든 user interface objects 의 base class 이다. `QWidget` 의 
default constructor 는 parent 가 없으며, parent 가 없는 widget 은 window 라고 
불린다.

```python
from PyQt5.QtWidgets import QWidget

w = QWidget()
```

```python
w.resize(250, 150)  # resize the widget, 250px wide 150px height.
w.move(300, 300)  # move the widget, x=300, y=300 coordinate.
w.show()  # display the widget on the screen. 
```

`sys.exit(app.exec_())` Application 의 main loop 으로 들어왔고, 
이제부터 event handling 이 시작된다. 


