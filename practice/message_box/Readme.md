# Message Box

`QWidget` 을 닫으려고 하면 `QCloseEvent` 가 생성 된다. `closeEvent()` 를 override 해서
reimplement 하면, widget 의 behaviour 를 변경할 수 있다.


```python
reply = QMessageBox.question(self, 'Message',
    "Are you sure to quit?", QtGui.QMessageBox.Yes | 
    QtGui.QMessageBox.No, QtGui.QMessageBox.No)
```

`QMessageBox.question` 의 세번째 parameter 는 dialog 에 나타날 button 들이고, 마지막 parameter 
는 default button 이다. `reply` 에 사용자가 선택한 button 이 저장된다.
