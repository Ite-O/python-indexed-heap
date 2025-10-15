from Indexed_Heap import HeapItem, MinHeap, MaxHeap

class _HeapStubMixin:
    def __init__(self, heap, item_to_index):
        self.heap = [HeapItem(item) for item in heap]
        self.item_to_index = item_to_index

class max_heap_stub(_HeapStubMixin, MaxHeap):
    pass


class min_heap_stub(_HeapStubMixin, MinHeap):
    pass
