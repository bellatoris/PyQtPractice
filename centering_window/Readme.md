# Centering window on the screen

`qr = self.frameGeometry` 를 통해서 widget 의 geometry 를 가진 rectangle 을 얻는다. 
`qr` 을 화면 중앙으로 옮긴후 `self.move(qr.topLeft)` 를 통해서 widget 을 중앙으로 이동시킨다. 
`cp = QDesktopWidget().availableGeometry().center()` monitor 의 screen resolution 을 알아내고, 
이 resolution 을 통해 center point 를 얻는다. 그 후 `qr.moveCenter(cp)` 를 통해서 rectangle 을 
중앙에 이동 시킨후 `self.move(qr.topLeft)` 를 이용해 widget 을 중앙에 이동 시킨다.
