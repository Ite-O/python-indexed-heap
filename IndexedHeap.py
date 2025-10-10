from abc import ABC, abstractmethod

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
    
class iheap(ABC):
    def __init__(self, arr = None):
        if arr == None:
            arr = []
        
        if not isinstance(arr, list):
            raise TypeError("arr must be a list")
        
        self.heap = []
        self.item_to_index = {}
        if len(arr) > 0:
            first_item = arr[0]
            for item in arr:
                is_comparable, type1, type2 = self._is_comparable(item, first_item)
            
                if not is_comparable:
                    raise TypeError(f"All items in the heap must be comparable. {type1} and {type2} are not comparable.")
                heap_item = HeapItem(item)
                if heap_item in self.item_to_index:
                    idx = self.item_to_index[heap_item]
                    self.heap[idx].frequency +=1
                else:
                    self.heap.append(heap_item)
                    self.item_to_index[heap_item] = len(self.heap) - 1

        for i in range((len(self.heap)//2)-1, -1, -1):
            self._sift_down(i)

    @abstractmethod
    def _comes_before(self, a, b):
        pass

    @classmethod
    def heapify(cls, arr = None):
        if cls is iheap:
            raise TypeError("Cannot call heapify() on abstract base class iheap directly")
        if arr == None:
            arr = []
        if not isinstance(arr, list):
            raise TypeError("arr should be a list or None")
        return cls(arr)
        
    def _sift_up(self, idx = None):
        n = len(self.heap)
        if idx == None:
            idx = n-1
        if idx < 0 or idx >= n:
            raise ValueError(f"idx out of range, idx: {idx}, heap size: {len(self.heap)}")
        while idx > 0:
            parent_idx = (idx - 1) // 2
            parent_value = self.heap[parent_idx]
            value = self.heap[idx]
            if self._comes_before(value, parent_value):
                self.heap[idx], self.heap[parent_idx] = self.heap[parent_idx], self.heap[idx]
                self.item_to_index[value] = parent_idx
                self.item_to_index[parent_value] = idx
                idx = parent_idx
            else:
                break
        return idx
    
    def _sift_down(self, idx = None):
        n = len(self.heap)
        if idx == None:
            idx = 0
        if idx < 0 or idx >= n:
            raise ValueError(f"idx out of range, idx: {idx}, heap size: {len(self.heap)}")
        child1_idx, child2_idx = (2 * idx + 1), (2 * idx + 2)    
        while child1_idx < n and \
            (self._comes_before(self.heap[child1_idx], self.heap[idx]) \
            or (child2_idx < n and self._comes_before(self.heap[child2_idx], self.heap[idx]))    
            ):
            child_idx = child1_idx
            child_value = self.heap[child1_idx]
            if child2_idx < n and self._comes_before(self.heap[child2_idx], child_value):
                child_idx = child2_idx
                child_value = self.heap[child2_idx]
            value = self.heap[idx]
            self.heap[idx], self.heap[child_idx] = self.heap[child_idx], self.heap[idx]
            self.item_to_index[child_value] = idx
            self.item_to_index[value] = child_idx
            idx = child_idx
            child1_idx, child2_idx = (2 * idx + 1), (2 * idx + 2)
        return idx
    
    def peek(self):
        if self.heap:
            return self.heap[0].item
        else:
            return None
        
    def insert(self, item, count = 1):
        if len(self.heap) > 0:
            is_comparable, type1, type2 = self._is_comparable(item, self.heap[0].item)
            if not is_comparable:
                raise TypeError(f"All items in the heap must be comparable. {type1} and {type2} are not comparable.")
        heap_item = HeapItem(item, count)
        if heap_item in self.item_to_index:
            idx = self.item_to_index[heap_item]
            self.heap[idx].frequency += count
        else:
            self.heap.append(heap_item)
            self.item_to_index[heap_item] = len(self.heap) - 1
            self._sift_up()

    def pop(self):
        n = len(self.heap)
        if n == 0:
            raise IndexError("Pop from empty heap")
        if n > 1:
            root: HeapItem = self.heap[0]
            if root.frequency > 1:
                root.frequency -= 1
                return root.item
            else:
                last_item = self.heap[n-1]
                self.heap[0], self.heap[n-1] = self.heap[n-1], self.heap[0]
                self.item_to_index[last_item] = 0
        res = self.heap.pop()
        del self.item_to_index[res]
        if len(self.heap) > 1:
            self._sift_down()
        return res.item
    
    def _validate_item_in_heap(self, item):
        heap_item = HeapItem(item)
        if heap_item not in self.item_to_index:
            raise ValueError(f"The provided item ({item}) is not in the heap")
        return (heap_item, self.item_to_index[heap_item])
    
    def update(self, item, count):
        heap_item, idx = self._validate_item_in_heap(item)
        if count == "ALL":
            count = heap_item.frequency
        if not isinstance(count, int):
            raise ValueError("The count must be an integer or 'ALL'")
        if count < 0:
            raise ValueError("Count must be greater than or equal to 0")
        if count > 0:
            heap_item.frequency = count
        else:
            last_idx = len(self.heap) -1
            if idx != last_idx:
                last_item = self.heap[last_item]
                self.heap[idx], self.heap[last_idx] = self.heap[last_idx], self.heap[idx]
                self.item_to_index[last_item] = idx
            self.heap.pop()
            del self.item_to_index[heap_item]
            if idx != last_idx:
                new_idx = self._sift_down(idx)
                self._sift_up(new_idx)
            
    def remove(self, item):
        self.update(item, "ALL")

    def replace(self, curr_item, new_item, count = "ALL"):
        curr_heap_item, curr_idx = self._validate_item_in_heap(curr_item)
        is_comparable, type1, type2 = self._is_comparable(new_item, curr_item)
        if not is_comparable:
            raise TypeError(f"All items in the heap must be comparable. {type1} and {type2} are not comparable.")
        new_heap_item = HeapItem(new_item)
        if curr_heap_item == new_heap_item:
            raise ValueError("curr_item cannot be equivalent to the new_item, consider using the update or remove methods")

        if count == "ALL":
            count = curr_heap_item.frequency
        if type(count) != int:
            raise ValueError("Count should either be an integer or 'ALL'")
        if count < 1 or count > curr_heap_item.frequency:
            raise ValueError(f"Count should be between 1 and the frequncy of {curr_item} in the heap ({curr_heap_item.frequency})")
        
        if count == curr_heap_item.frequency:
            new_heap_item.frequency = curr_heap_item.frequency
            self.heap[curr_idx] = new_heap_item
            del self.item_to_index[curr_heap_item]
            self.item_to_index[new_heap_item] = curr_idx
            new_idx = self._sift_down(curr_idx)
            self._sift_up(new_idx)
        else:
            curr_heap_item.frequency -= count
            self.insert(new_item, count)

    def __len__(self):
        return len(self.heap)
    
    def __bool__(self):
        return bool(self.heap)
    
    def to_list(self, showFreq = False):
        res = []
        if showFreq:
            for heap_item in self.heap:
                res.append((heap_item.item, heap_item.frequency))
        else:
            for heap_item in self.heap:
                res.append(heap_item.item)
        return res
    
    @abstractmethod
    def _is_class(self, other):
        pass
    
    def __eq__(self, other):
        if not self._is_class(other):
            return False
        elif len(self.heap) != len(other.heap):
            return False
        for i in range(len(self.heap)):
            if self.heap[i] != other.heap[i]:
                return False
            try:
                if self.item_to_index[self.heap[i]] != other.item_to_index[other.heap[i]]:
                    return False
            except KeyError:
                return False
            
            if self.heap[i].frequency != other.heap[i].frequency:
                return False
        return True
    
    @abstractmethod
    def _is_comparable(self, a, b):
        pass
    
class min_iheap(iheap):
    def _comes_before(self, a, b):
        return a < b
    
    def _is_comparable(self, a, b):
        try:
            a < b
            b < a
            return (True, type(a), type(b))
        except TypeError:
            return (False, type(a), type(b))
    
    def _is_class(self, other):
        if isinstance(other, min_iheap):
            return True
        else:
            return False

class max_iheap(iheap):
    def _comes_before(self, a, b):
        return a > b
    
    def _is_comparable(self, a, b):
        try:
            a > b
            b > a
            return (True, type(a), type(b))
        except TypeError:
            return (False, type(a), type(b))
    
    def _is_class(self, other):
        if isinstance(other, max_iheap):
            return True
        else:
            return False