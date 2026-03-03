import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene
from mainwindow import Ui_MainWindow
from node import BaseNode

plugin_path = os.path.join(os.path.dirname(__file__), "venv", "Lib", "site-packages", "PyQt5", "Qt5", "plugins", "platforms")
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

class FlowPyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("FlowPy - Sürükle Bırak Testi")
        
        # 1. Tuvali ve Sahneyi Oluştur
        self.scene = QGraphicsScene()
        self.ui.graphicsView.setScene(self.scene)
        self.scene.setSceneRect(-500, -500, 1000, 1000)

        # 2. Tuvalin dışarıdan gelen sürüklemeleri kabul etmesini sağla
        self.ui.graphicsView.setAcceptDrops(True)

        # 3. Sürüklenen nesne tuvalin üzerine geldiğinde tetiklenen fonksiyon
        def dragEnterEvent(event):
            # Eğer sürüklenen şey bir metin (text) içeriyorsa kabul et
            if event.mimeData().hasText():
                event.accept()
            else:
                event.ignore()

        # 4. Nesne fare tuşu bırakıldığında (Drop) tetiklenen fonksiyon
        def dropEvent(event):
            # Panelden sürüklenen yazıyı alıyoruz (Örn: "İşlem Düğümü")
            node_text = event.mimeData().text()
            
            # Farenin bırakıldığı ekran koordinatını, sahne koordinatına çeviriyoruz
            view_pos = event.pos()
            scene_pos = self.ui.graphicsView.mapToScene(view_pos)
            
            # Seçilen yazıya göre yeni bir düğüm üretip sahneye ekliyoruz
            yeni_dugum = BaseNode(node_text)
            yeni_dugum.setPos(scene_pos)
            self.scene.addItem(yeni_dugum)
            
            event.accept()

        # 5. Yazdığımız bu fonksiyonları senin QGraphicsView'a bağlıyoruz
        self.ui.graphicsView.dragEnterEvent = dragEnterEvent
        self.ui.graphicsView.dragMoveEvent = dragEnterEvent
        self.ui.graphicsView.dropEvent = dropEvent

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FlowPyApp()
    window.show()
    sys.exit(app.exec_())