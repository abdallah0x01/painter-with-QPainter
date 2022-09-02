import sys

from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QColorDialog, QVBoxLayout, QPushButton, QToolTip, \
    QListWidget, QAction, QMenu, QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QColor, QFont, QPolygon, QCursor


# Canvas class inherits from QLabel
class Canvas(QLabel):
    class Shapes:
        def __init__(self, shape_type: str, start_x: int, start_y: int, end_x: int, end_y: int):
            painter = QPainter()
            painter.setPen(Qt.red)

            self.start_x = start_x
            self.start_y = start_y
            self.end_x = end_x
            self.end_y = end_y

            if shape_type == 'line':
                self.type = 'line'
                painter.drawLine(start_x, start_y, end_x,
                                 end_y)
            elif shape_type == 'rect':
                self.type = 'rect'
                rect = QRect(start_x, start_y, end_x, end_y)
                painter.drawRect(rect.normalized())

    def __init__(self):
        super().__init__()
        self.width, self.height = 1000, 800
        self.setFixedSize(self.width, self.height)
        self.setMinimumSize(700, 600)
        self.setWindowTitle('painter')
        ###############################
        self.background_color = '#242423'
        self.pix = QPixmap(self.width, self.height)
        self.pix.fill(QColor(self.background_color))
        self.setPixmap(self.pix)
        ##############################
        self.mouse_track_label = QLabel()
        # track mouse if it moves
        self.setMouseTracking(True)
        ###############################

        self.drawing = False
        ##############################
        self.start = QPoint()
        self.end = QPoint()
        ##############################
        self.pen_color = Qt.red
        self.pen_width = 3
        ##########################
        self.polygon_points = []
        self.shapes = []
        ######################
        self.list_widget = QListWidget()
        self.list_widget.addItems(('shape', 'path'))
        ######################
        self.shapes_list = []
        self.no_shapes = 0

    def contextMenuEvent(self, event):
        self.menu = QMenu(self)
        add_shape = QAction('Add Shape', self)
        clear = QAction('Clear', self)

        # add shape
        add_shape.triggered.connect(self.draw)
        self.menu.addAction(add_shape)
        # clear
        clear.triggered.connect(self.clear)
        self.menu.addAction(clear)

        # add other required actions
        self.menu.popup(QCursor.pos())

    def draw(self):
        self.drawing = True

    def clear(self):
        self.pix.fill(QColor(self.background_color))
        self.shapes_list.clear()
        self.no_shapes = 0
        self.update()

    def paintEvent(self, event):
        """ paintEvent track what you are drawing and show it instantaneously, but it is not who paint """
        # This is to prevent the chance of the painting being lost if the user changes windows
        painter = QPainter(self)
        painter.setPen(self.pen_color)
        painter.drawPixmap(QPoint(), self.pix)
        # shape = ''
        if self.drawing & Qt.LeftButton:

            # show rectangle while drawing
            if not self.start.isNull() and not self.end.isNull():
                # if height and width is less than 20 draw line else draw rect
                if self.start.x() == self.end.x() and self.start.y() == self.end.y():
                    pass
                elif abs(self.end.x() - self.start.x()) < 20 or abs(self.end.y() - self.start.y()) < 20:
                    # draw vertical line
                    if abs(self.end.y() - self.start.y()) < 20:
                        painter.drawLine(self.start.x(), self.start.y(), self.end.x(),
                                         self.start.y())


                    else:
                        # draw horizontal line
                        painter.drawLine(self.start.x(), self.start.y(), self.start.x() - self.end.x() + self.end.x(),
                                         self.end.y())

                else:
                    # draw rect
                    rect = QRect(self.start, self.end)
                    painter.drawRect(rect.normalized())

    def mousePressEvent(self, event):
        if self.drawing:
            if event.button() == Qt.LeftButton:
                self.start = event.pos()
                self.end = event.pos()

    def mouseMoveEvent(self, event):
        if self.drawing:
            if event.buttons() & Qt.LeftButton:
                self.end = event.pos()
                self.update()

        self.showMousePosition(event)

    def mouseReleaseEvent(self, event):
        if self.drawing:

            if event.button() == Qt.LeftButton:

                painter = QPainter(self.pix)
                painter.setPen(self.pen_color)

                if self.start.x() == self.end.x() and self.start.y() == self.end.y():
                    pass
                # if height and width is less than 20 draw line else draw rect
                elif abs(self.end.x() - self.start.x()) < 20 or abs(self.end.y() - self.start.y()) < 20:
                    # draw vertical line

                    if abs(self.end.y() - self.start.y()) < 20:
                        painter.drawLine(self.start.x(), self.start.y(), self.end.x(),
                                         self.start.y())
                        shape = self.Shapes('line', self.start.x(), self.start.y(), self.end.x(),
                                            self.start.y())

                    else:
                        # draw horizontal line
                        painter.drawLine(self.start.x(), self.start.y(), self.start.x() - self.end.x() + self.end.x(),
                                         self.end.y())
                        shape = self.Shapes('line', self.start.x(), self.start.y(),
                                            self.start.x() - self.end.x() + self.end.x(),
                                            self.end.y())



                else:
                    rect = QRect(self.start, self.end)
                    painter.drawRect(rect.normalized())
                    shape = self.Shapes('rect', self.start.x(), self.start.y(),
                                        self.end.x(),
                                        self.end.y())
                self.shapes.append(shape)
                self.no_shapes += 1

                self.shapes_details(event)

                #
                # when you call update paintEvent is called and save the drawing to pixmap
                self.update()
                self.drawing = False
                print(self.shapes[-1].type)

        

    def showMousePosition(self, event):

        mouse_position = event.pos()
        global_position = self.mapToGlobal(mouse_position)
        QToolTip.showText(global_position, f'({mouse_position.x()},{mouse_position.y()}')

    def shapes_details(self, event):
        if event.button() == Qt.LeftButton:
            if abs(self.end.y() - self.start.y()) < 20:
                self.shapes_list.append(
                    {f'shape {self.no_shapes} => H_line': (
                        (self.start.x(), self.start.y()), (self.end.x(), self.start.y()))})
            elif abs(self.end.x() - self.start.x()) < 20:
                self.shapes_list.append(
                    {f'shape {self.no_shapes} => V_line': (
                        (self.start.x(), self.start.y()), (self.end.x(), self.end.y()))})

            else:
                self.shapes_list.append(
                    {f'shape {self.no_shapes} => Polygon': (
                        (self.start.x(), self.start.y()), (self.end.x(), self.end.y()))})

            print(self.shapes_list[-1])

    

# Run program
if __name__ == '__main__':
    # QApplication class manages the application’s main event loop, flow, initialization, and finalization,
    # as well as session management. Create application object
    app = QApplication([])
   
    # Create window object
    window = Canvas()
    # add cross cursor
    cursor = QCursor()
    cursor.setShape(Qt.CrossCursor)
    window.setCursor(cursor)

    window.show()
    sys.exit(app.exec())
