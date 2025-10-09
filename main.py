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
    def __init__(self, arr = None):
        if arr == None:
            arr = []

        """
        self.heap is a list based representation of the heap. 
        For any given item with index i, its left child will be at index 2*i+1 and its right child at index 2*i+2.
        """
        if isinstance(arr, list):
            self.heap = arr[:]
        else:
            raise ValueError("arr must be a list")
        
        """
        self._item_type identifies the type of items in the heap. 
        isInstance is used to check that new items inserted into the heap are of the same class as existing items in the heap. 
        It also works for subclasses.
        If the heap is empty and an item is added, then the self._item_type is also updated.
        """
        self._item_type = None
        if len(arr) > 0:
            self._item_type = type(arr[0])

        """
        self.item_map is a dictionary, containing a mapping from heap items to a tuple containing the index (in self.heap) and frequency of the item.
        e.g. {item: (index, frequency)}
        """
        self.item_map = {}
        for i, item in enumerate(arr):
            if not isinstance(item, self._item_type):
                raise TypeError("All items in the heap must satisfy isinstance. Ie. Must be of the same type or a subclass")
            if item in self.item_map:
                self.item_map[item] = (i, self.item_map[item][1] + 1)
            else:
                self.item_map[item] = (i, 1)
        
        """
        Sifting down all non-leaf items to heapify self.heap
        """
        for i in range((len(arr)//2)-1, -1, -1):
            self._sift_down(i)

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
            raise ValueError("The heap is empty, no items to pop")
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
        if len(self.heap) > 1:
            self._sift_down()
        return res

    def _sift_up(self, idx = None):
        if idx == None:
            idx = len(self.heap) - 1
        if idx < 0 or idx >= len(self.heap):
            raise ValueError("Provided idx is not within the bounds of the heap") 
        if len(self.heap) > 1:                               
            parent_idx = max((idx - 1)//2, 0)
            try:
                while idx > 0 and self.heap[idx] < self.heap[parent_idx]:
                    curr = self.heap[idx]
                    parent = self.heap[parent_idx]
                    self.heap[idx], self.heap[parent_idx] = self.heap[parent_idx], self.heap[idx]
                    self.item_map[curr] = (parent_idx, self.item_map[curr][1])
                    self.item_map[parent] = (idx, self.item_map[parent][1])
                    idx = parent_idx
                    parent_idx = max((idx - 1)//2, 0)
            except TypeError:
                raise TypeError("Inconsistent types in heap, items must be mutually comparable with < operator")
        return idx

    def _sift_down(self, idx = 0):
        if idx < 0 or idx >= len(self.heap):
            raise ValueError("Provided idx is not within the bounds of the heap") 
        
        if len(self.heap) > 1: 
            child_1_idx = 2 * idx + 1
            child_2_idx = 2 * idx + 2
            try:
                while child_1_idx < len(self.heap) and \
                    ((self.heap[child_1_idx] < self.heap[idx]) or \
                    (child_2_idx < len(self.heap) and self.heap[child_2_idx] < self.heap[idx])):
                    if child_2_idx < len(self.heap) and self.heap[child_2_idx] < self.heap[child_1_idx]:
                        child_idx = child_2_idx
                        child = self.heap[child_2_idx]
                    else:
                        child_idx = child_1_idx
                        child = self.heap[child_1_idx]
                    
                    curr = self.heap[idx]
                    self.heap[idx], self.heap[child_idx] = self.heap[child_idx], self.heap[idx]
                    self.item_map[child] = (idx, self.item_map[child][1])
                    self.item_map[curr] = (child_idx, self.item_map[curr][1])
                    idx = child_idx
                    child_1_idx = 2 * idx + 1
                    child_2_idx = 2 * idx + 2
            except TypeError:
                raise TypeError("Inconsistent types in heap, items must be mutually comparable with < operator")
        return idx
    
    def _validate_item_in_heap(self, item):
        if item not in self.item_map:
            raise ValueError("The provided curr_item is not in the heap")
        return self.item_map[item]
    
    def update(self, item, count):
        idx, freq = self._validate_item_in_heap(item)
        if count == "ALL":
            count = freq
        if not isinstance(count, int):
            raise ValueError("The count must be an integer or 'ALL'")
        if count < 0:
            raise ValueError("Count must be greater than or equal to 0")
        if count > 0:
            self.item_map[item] = (idx, count)
        else:
            last_idx = len(self.heap) -1
            if idx != last_idx:
                self.heap[idx], self.heap[last_idx] = self.heap[last_idx], self.heap[idx]
                self.item_map[self.heap[idx]] = (idx, self.item_map[self.heap[idx]][1])
            self.heap.pop()
            del self.item_map[item]
            if idx != last_idx:
                new_idx = self._sift_down(idx)
                self._sift_up(new_idx)

    def remove(self, item):
        self.update(item, "ALL")
    
    def replace(self, curr_item, new_item, count = "ALL"):
        if not isinstance(new_item, self._item_type):
            raise TypeError(f"Type difference between new item and current items in heap {self._item_type}")
        
        if curr_item not in self.item_map:
            raise ValueError("The provided curr_item is not in the heap")
        
        if curr_item == new_item:
            raise ValueError("curr_item cannot be equivalent to the new_item, consider using the update or remove methods")

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
            self._sift_up(new_idx)
        else:
            self.item_map[curr_item] = (curr_idx, curr_freq - count)
            self.insert(new_item, count)
    
    def __len__(self):
        return len(self.heap)
    
    def __bool__(self):
        return bool(self.heap)

    @classmethod
    def heapify(cls, arr = None):
        if arr == None:
            arr = []
        if not isinstance(arr, list):
            raise TypeError("arr should be a list or None")
        return cls(arr)

    def to_list(self):
        return self.heap[:]
    
    def get_item_map(self):
        return self.item_map.copy()
