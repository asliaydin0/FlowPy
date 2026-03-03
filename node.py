from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem
from PyQt5.QtCore import QRectF, Qt, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
from PyQt5.QtWidgets import QGraphicsPathItem
from PyQt5.QtGui import QPainterPath
from core import registry

class Port(QGraphicsEllipseItem):
    def __init__(self, parent=None, is_output=False):
        # Dairenin koordinatları ve boyutu (x, y, genişlik, yükseklik)
        super().__init__(-6, -6, 12, 12, parent)
        self.is_output = is_output
        
        # Portların içi dolgulu bir renk olsun
        self.setBrush(QBrush(QColor("#3498db"))) # Mavi renk
        self.setPen(QPen(Qt.black, 1))
        
        # Portun üzerine gelindiğinde farenin işaretçi (cursor) şekli değişsin
        self.setCursor(Qt.CrossCursor)

class BaseNode(QGraphicsItem):
    def __init__(self, title="İşlem Düğümü"):
        super().__init__()
        self.title = title
        
        # Düğümün boyutları
        self.width = 120
        self.height = 60
        
        # Bu bayraklar düğümün fareyle seçilebilmesini ve sürüklenebilmesini sağlar!
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)

        # Bu bayrak, düğüm konum değiştirdiğinde itemChange event'ini tetikler
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        
        # Bu düğüme bağlanan tüm okları (Edge) bu listede tutacağız
        self.edges = []

        # 1. Giriş Portu (Sol orta kısım)
        self.input_port = Port(self, is_output=False)
        self.input_port.setPos(0, self.height / 2) # X: 0, Y: Yüksekliğin yarısı
        
        # 2. Çıkış Portu (Sağ orta kısım)
        self.output_port = Port(self, is_output=True)
        self.output_port.setPos(self.width, self.height / 2) # X: Genişlik kadar, Y: Yüksekliğin yarısı

        self.node_id = registry.register_node(self)

    # 1. ZORUNLU METOT: Düğümün tıklanabilir sınırlarını belirler
    def boundingRect(self):
        return QRectF(0, 0, self.width, self.height)

    # 2. ZORUNLU METOT: Düğümün ekrana nasıl çizileceğini belirler (Senin tuvalin burası)
    def paint(self, painter, option, widget=None):
        # Düğümün arka plan rengi ve kenarlığı
        rect = self.boundingRect()
        
        # Düğüm seçiliyken kenarlığını farklı renkte çizelim (Kullanıcı geri bildirimi)
        if self.isSelected():
            pen = QPen(QColor("#f39c12"), 2) # Turuncu ve kalın kenarlık
        else:
            pen = QPen(QColor("#2c3e50"), 1) # Koyu mavi standart kenarlık
            
        painter.setPen(pen)
        painter.setBrush(QBrush(QColor("#ecf0f1"))) # Açık gri arka plan
        
        # Yuvarlak köşeli dikdörtgen çizimi (Arayüzü yumuşatmak için)
        painter.drawRoundedRect(rect, 10, 10)
        
        # Düğümün başlığını yazdıralım
        painter.setPen(QPen(Qt.black))
        painter.drawText(rect, Qt.AlignCenter, self.title)

        # Düğümün konumu değiştiğinde tetiklenen metot
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            # Düğüm sürüklendiğinde, ona bağlı olan tüm oklara "kendini güncelle" diyoruz
            for edge in self.edges:
                edge.update_positions()
        return super().itemChange(change, value)


class Edge(QGraphicsPathItem):
    def __init__(self, source_port, dest_port):
        super().__init__()
        self.source_port = source_port
        self.dest_port = dest_port
        
        # Çizginin rengi ve kalınlığı
        self.setPen(QPen(QColor("#2980b9"), 3)) 
        
        # Çizgiler (Oklar) her zaman düğümlerin arkasında (altında) kalsın diye Z değerini düşürüyoruz
        self.setZValue(-1) 

        # Oku, başlangıç ve bitiş düğümlerinin listesine ekliyoruz
        self.source_port.parentItem().edges.append(self)
        self.dest_port.parentItem().edges.append(self)
        # -----------------------
        registry.register_edge(self.source_port.parentItem().node_id, self.dest_port.parentItem().node_id)
        
        self.update_positions()

    def update_positions(self):
        # Eğer portlardan biri bile yoksa çizim yapma
        if not self.source_port or not self.dest_port:
            return

        # Portların sahne üzerindeki mutlak koordinatlarını alıyoruz
        # (Çünkü portlar düğümlerin içinde yaşıyor, bize sahnedeki yerleri lazım)
        source_pos = self.source_port.scenePos()
        
        # Çizginin portun tam ortasından çıkması için 6 piksel (yarıçap) kaydırıyoruz
        source_pos.setX(source_pos.x() + 6)
        source_pos.setY(source_pos.y() + 6)
        
        dest_pos = self.dest_port.scenePos()
        dest_pos.setX(dest_pos.x() + 6)
        dest_pos.setY(dest_pos.y() + 6)

        # Bezier eğrisi için 2 adet kontrol noktası (kavis noktası) belirliyoruz
        # Çıkış portundan 50 piksel sağa, Giriş portundan 50 piksel sola kavis veriyoruz
        ctrl_1 = source_pos + QPointF(50, 0)
        ctrl_2 = dest_pos - QPointF(50, 0)

        # Yolu (Path) oluşturup noktaları birleştiriyoruz
        path = QPainterPath(source_pos)
        path.cubicTo(ctrl_1, ctrl_2, dest_pos)
        
        # Çizgiyi sahneye uygula
        self.setPath(path)