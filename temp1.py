

# def test_var_kwargs(farg, **kwargs):
#     print "formal arg:", farg
#     for key in kwargs:
#         print "another keyword arg: %s: %s, type = %s" % (key, kwargs[key], type(kwargs[key]))

# test_var_kwargs(farg=1, myarg2="two", myarg3=3)




def f(x):
    return {
        'a': 1,
        'b': 2,
    }.get(x, 9) 

print f('m')

# from PySide.QtGui import *
# import sys

# class testWidget(QGraphicsView):
#     def __init__(self):
#         QGraphicsView.__init__(self)

#         floorSpinBox = QSpinBox()
#         floorSpinBox.setGeometry(0,0,50,25)

#         proxyWidget = QGraphicsProxyWidget() 
#         proxyWidget.setWidget(floorSpinBox)

#         scene = QGraphicsScene(self)
#         scene.addItem(proxyWidget)
#         self.setScene(scene)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     widget = testWidget()
#     widget.show()
#     app.exec_()