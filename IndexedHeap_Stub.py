from IndexedHeap import HeapItem, min_iheap, max_iheap

class _HeapStubMixin:
    def __init__(self, heap, item_to_index):
        self.heap = [HeapItem(item) for item in heap]
        self.item_to_index = item_to_index

class max_iheap_stub(_HeapStubMixin, max_iheap):
    pass


class min_iheap_stub(_HeapStubMixin, min_iheap):
    pass
