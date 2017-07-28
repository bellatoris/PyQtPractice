# Showing a tooltip

`QTooltip.setFont` 는 static method 로 tootips 을 render 하는데 사용되는 font 를 정한다. 
`setToolTip` 를 이용해서 tooltip 을 생성한다. 

```python
import PyQt5.QtGui import *

btn.QPushButton("Button", self)
btn.setToolTip("this is a <b>QPushButton</b> widget")
btn.resize(btn.sizeHint())
btn.move(50, 50)
```

`QPushButton` 을 통해 button 을 만들고 `sizeHint()` method 를 사용해서 resize 한다.
