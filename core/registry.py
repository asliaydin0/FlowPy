# core/registry.py
# ──────────────────────────────────────────────────────────────────────
# NodeRegistry: Sahneye eklenen düğümleri UUID'lerine göre bir
# dictionary içinde tutan merkezi kayıt sistemi.
# AST (Abstract Syntax Tree) ve State Machine yapısının veri kaynağı.
# ──────────────────────────────────────────────────────────────────────

import uuid


class NodeRegistry:
    """Sahnedeki tüm düğümleri ve bağlantıları yöneten merkezi kayıt defteri."""

    def __init__(self):
        # { uuid_str: BaseNode nesnesi }
        self.nodes: dict = {}
        # [ (kaynak_uuid, hedef_uuid), ... ]  –  AST kenar listesi
        self.edges: list = []

    # ── Düğüm İşlemleri ──────────────────────────────────────────────

    def add_node(self, node) -> str:
        """Düğümü kayıt defterine ekler ve benzersiz UUID döndürür."""
        node_id = str(uuid.uuid4())
        self.nodes[node_id] = node
        print(f"[Registry] Düğüm eklendi: {getattr(node, 'title', '?')} "
              f"(ID: {node_id[:8]}…)")
        return node_id

    def remove_node(self, node_id: str) -> bool:
        """Verilen UUID'ye sahip düğümü kayıt defterinden siler."""
        if node_id in self.nodes:
            removed = self.nodes.pop(node_id)
            # Bu düğüme ait tüm kenarları da temizle
            self.edges = [
                (s, d) for s, d in self.edges
                if s != node_id and d != node_id
            ]
            print(f"[Registry] Düğüm silindi: {getattr(removed, 'title', '?')} "
                  f"(ID: {node_id[:8]}…)")
            return True
        return False

    def get_node(self, node_id: str):
        """UUID'ye göre düğümü döndürür; yoksa None."""
        return self.nodes.get(node_id, None)

    # ── Kenar (Bağlantı) İşlemleri ───────────────────────────────────

    def add_edge(self, source_id: str, dest_id: str):
        """İki düğüm arasına yönlü bir kenar ekler."""
        self.edges.append((source_id, dest_id))
        print(f"[Registry] Bağlantı eklendi: {source_id[:8]} → {dest_id[:8]}")

    def get_all_nodes(self) -> dict:
        """Tüm kayıtlı düğümleri döndürür."""
        return self.nodes

    def get_all_edges(self) -> list:
        """Tüm kenarların listesini döndürür."""
        return list(self.edges)

    def clear(self):
        """Tüm düğüm ve kenarları temizler."""
        self.nodes.clear()
        self.edges.clear()
        print("[Registry] Tüm kayıtlar temizlendi.")
