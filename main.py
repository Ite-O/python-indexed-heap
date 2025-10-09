class IndexedHeap:
    """
    A min-heap that tracks item indices for O(log n) updates.

    Requirements for custom objects:
    - Must implement __lt__ and __eq__ for ordering and equality.
    - Must be hashable (i.e. define __hash__), since internal
      structures (index map, frequency map) depend on hashing.

    Ordering is determined by __lt__.
    Hash-based equivalence (used for frequency and index tracking)
    depends on __hash__.
    """
    def __init__(self):
        """
        self.item_map is a dictionary, containing a mapping from heap items to a tuple containing the index (in self.heap) and frequency of the item.
        e.g. {item: (index, frequency)}
        """
        self.item_map = {}
        """
        self.heap is a list based representation of the heap. 
        For any given item with index i, its left child will be at index 2*i+1 and its right child at index 2*i+2.
        """
        self.heap = []
        """
        self._item_type identifies the type of items in the heap. 
        isInstance is used to check that new items inserted into the heap are of the same class as existing items in the heap. 
        It also works for subclasses.
        If the heap is empty and an item is added, then the self._item_type is also updated.
        """
        self._item_type = None

    def peek(self):
        if self.heap:
            return self.heap[0]
        else:
            return None

    def insert(self, item, count = 1):
        if len(self.heap) == 0:
            self._item_type = type(item)
        elif not isinstance(item, self._item_type):
            raise TypeError(f"Type difference between new item and current items in heap {self._item_type}")
        
        if item in self.item_map:
            self.item_map[item] = (self.item_map[item][0], self.item_map[item][1] + count)
        else:
            self.heap.append(item)
            self.item_map[item] = (len(self.heap) - 1, count)
            self._sift_up()
        

    def pop(self):
        n = len(self.heap)
        if n == 0:
            raise ValueError("The heap is empty, you cannot pop any item")
        if n > 1:
            root = self.heap[0]
            root_frequency = self.item_map[root][1]
            if root_frequency > 1:
                self.item_map[root] = (self.item_map[root][0], self.item_map[root][1] - 1)
                return root
            else:
                self.heap[0], self.heap[n-1] = self.heap[n-1], self.heap[0]
                self.item_map[self.heap[0]] = (0, self.item_map[self.heap[0]][1])
                res = self.heap.pop()
                del self.item_map[res]
                self._sift_down()
                return res

    def _sift_up(self, idx = None):
        if len(self.heap) > 1:
            curr_idx = len(self.heap) - 1
            if idx:
                if 0 <= idx < len(self.heap):
                    curr_idx = idx
                else:
                    raise ValueError("Provided idx is not within the bounds of the heap")                
            parent_idx = (curr_idx - 1)//2
            while 0 <= parent_idx and self.heap[curr_idx] < self.heap[parent_idx]:
                curr = self.heap[curr_idx]
                parent = self.heap[parent_idx]
                self.heap[curr_idx], self.heap[parent_idx] = self.heap[parent_idx], self.heap[curr_idx]
                self.item_map[curr] = (parent_idx, self.item_map[curr][1])
                self.item_map[parent] = (curr_idx, self.item_map[parent][1])
                curr_idx = parent_idx
                parent_idx = (curr_idx - 1)//2
            return curr_idx
        return -1

    def _sift_down(self, idx = 0):
        if len(self.heap) > 1:
            if 0 <= idx < len(self.heap) - 1:
                curr_idx = idx
            else:
                raise ValueError("Provided idx is not within the bounds of the heap") 
            child_1_idx = 2 * curr_idx + 1
            child_2_idx = 2 * curr_idx + 2
            while child_1_idx < len(self.heap) and \
                ((self.heap[child_1_idx] < self.heap[curr_idx]) or \
                (child_2_idx < len(self.heap) and self.heap[child_2_idx] < self.heap[curr_idx])):
                if child_2_idx < len(self.heap) and self.heap[child_2_idx] < self.heap[child_1_idx]:
                    child_idx = child_2_idx
                    child = self.heap[child_2_idx]
                else:
                    child_idx = child_1_idx
                    child = self.heap[child_1_idx]
                
                curr = self.heap[curr_idx]
                self.heap[curr_idx], self.heap[child_idx] = self.heap[child_idx], self.heap[curr_idx]
                self.item_map[child] = (curr_idx, self.item_map[child][1])
                self.item_map[curr] = (child_idx, self.item_map[curr][1])
                curr_idx = child_idx
                child_1_idx = 2 * curr_idx + 1
                child_2_idx = 2 * curr_idx + 2
            return curr_idx
        return -1
        
    def update(self, curr_item, new_item, count = "ALL"):
        if not isinstance(new_item, self._item_type):
            raise TypeError(f"Type difference between new item and current items in heap {self._item_type}")
        
        if curr_item not in self.item_map:
            raise ValueError("The provided curr_item is not in the heap")

        curr_idx, curr_freq = self.item_map[curr_item]
        if count == "ALL":
            count = curr_freq
        if type(count) != int:
            raise ValueError("Count should either be an integer or 'ALL'")
        if count < 1 or count > curr_freq:
            raise ValueError(f"Count should be between 1 and the currently frequncy of {curr_item} in the heap ({self.item_map[curr_item][1]})")
        
        if count == curr_freq:
            self.heap[curr_idx] = new_item
            del self.item_map[curr_item]
            self.item_map[new_item] = (curr_idx, curr_freq)
            new_idx = self._sift_down(curr_idx)
            if new_idx != -1:
                self._sift_up(new_idx)
        else:
            self.item_map[curr_item] = (curr_idx, curr_freq - count)
            self.insert(new_item, count)

    def to_list(self):
        return self.heap
    
    def get_item_map(self):
        return self.item_map
