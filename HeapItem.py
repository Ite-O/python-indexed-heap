class HeapItem:
    def __init__(self, item, frequency = 1):
        self.item = item
        self.frequency = frequency

    def __eq__(self, other):
        return self.item == other.item
    
    def __lt__(self, other):
        return self.item < other.item
    
    def __gt__(self, other):
        return self.item > other.item
    
    def __hash__(self):
        return hash(self.item)