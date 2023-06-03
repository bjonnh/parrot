from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class EventSystem(QObject):
     segment_click = pyqtSignal(float)

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class Canvas(QVBoxLayout):
    def __init__(self):
        super().__init__()
        self.event_system: EventSystem = EventSystem()
        self.canvas = MplCanvas()

        self.canvas.mpl_connect("button_press_event", self.on_click)
        self.toolbar = NavigationToolbar2QT(self.canvas, None)

        self.addWidget(self.toolbar)
        self.addWidget(self.canvas)

    def on_click(self, event):
        if event.xdata is None:
            data = -1
        else:
            data = event.xdata

        self.event_system.segment_click.emit(data)