from iheap import HeapItem, miniheap, maxiheap

class _HeapStubMixin:
    def __init__(self, heap, item_to_index):
        self.heap = [HeapItem(item) for item in heap]
        self.item_to_index = item_to_index

class max_iheap_stub(_HeapStubMixin, maxiheap):
    pass


class min_iheap_stub(_HeapStubMixin, miniheap):
    pass
