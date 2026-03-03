# core.py
import uuid

class GraphRegistry:
    def __init__(self):
        # Sahnedeki tüm düğümleri ve aralarındaki okları burada hafızada tutacağız
        self.nodes = {}  # Format: { "uuid": node_nesnesi }
        self.edges = []  # Format: [ ("kaynak_uuid", "hedef_uuid") ]

    def register_node(self, node):
        # Düğüme benzersiz bir ID (UUID) oluştur
        node_id = str(uuid.uuid4())
        self.nodes[node_id] = node
        print(f"Sisteme yeni düğüm eklendi: {node.title} (ID: {node_id[:8]}...)")
        return node_id

    def register_edge(self, source_id, dest_id):
        # İki düğüm birbirine bağlandığında bunu AST motoru için kaydet
        self.edges.append((source_id, dest_id))
        print(f"Arka Planda Bağlantı Kuruldu: {source_id[:8]} -> {dest_id[:8]}")

# Tüm projenin ortak hafızası olacak nesneyi yaratıyoruz
registry = GraphRegistry()