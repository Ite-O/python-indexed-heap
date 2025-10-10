import unittest
import IndexedHeap
import math
import IndexedHeap_Stub

class Test_IndexedHeap(unittest.TestCase):    
    def test_heapify(self):
        arr_1 = [500, 300, -1000, -1.5, math.pi]
        arr_2 = ["ababacc", "brown", "yellow", "abc", "aaaaaaa"]
        arr_3 = [-1000,-1.5,500, 300, math.pi]

        max_heaps =[IndexedHeap.max_iheap.heapify(arr_1),
                    IndexedHeap.max_iheap.heapify(arr_2),
                    IndexedHeap.max_iheap.heapify(arr_3)
                    ]
        min_heaps = [IndexedHeap.min_iheap.heapify(arr_1),
                     IndexedHeap.min_iheap.heapify(arr_2),
                     IndexedHeap.min_iheap.heapify(arr_3)
                     ]
        
        min_heaps_stubs = [
                    IndexedHeap_Stub.min_iheap_stub(
                        heap = [-1000,-1.5,500, 300, math.pi], 
                        item_to_index = {IndexedHeap.HeapItem(-1000): 0, 
                                        IndexedHeap.HeapItem(-1.5): 1,
                                        IndexedHeap.HeapItem(500): 2,
                                        IndexedHeap.HeapItem(300): 3,
                                        IndexedHeap.HeapItem(math.pi): 4
                                        }             
                    ),
                    IndexedHeap_Stub.min_iheap_stub(
                        heap = ["aaaaaaa", "ababacc", "yellow", "abc", "brown"], 
                        item_to_index = {IndexedHeap.HeapItem("aaaaaaa"): 0, 
                                        IndexedHeap.HeapItem("ababacc"): 1,
                                        IndexedHeap.HeapItem("yellow"): 2,
                                        IndexedHeap.HeapItem("abc"): 3,
                                        IndexedHeap.HeapItem("brown"): 4
                                        } 
                    ),
                    IndexedHeap_Stub.min_iheap_stub(
                        heap = [-1000,-1.5,500, 300, math.pi], 
                        item_to_index = {IndexedHeap.HeapItem(-1000): 0, 
                                        IndexedHeap.HeapItem(-1.5): 1,
                                        IndexedHeap.HeapItem(500): 2,
                                        IndexedHeap.HeapItem(300): 3,
                                        IndexedHeap.HeapItem(math.pi): 4
                                        }             
                    )                 
        ]
        max_heaps_stubs = [
                    IndexedHeap_Stub.max_iheap_stub(
                        heap = [500, 300, -1000, -1.5, math.pi], 
                        item_to_index = {IndexedHeap.HeapItem(500): 0, 
                                        IndexedHeap.HeapItem(300): 1,
                                        IndexedHeap.HeapItem(-1000): 2,
                                        IndexedHeap.HeapItem(-1.5): 3,
                                        IndexedHeap.HeapItem(math.pi): 4
                                        }             
                    ),
                    IndexedHeap_Stub.max_iheap_stub(
                        heap = ["yellow", "brown", "ababacc", "abc", "aaaaaaa"], 
                        item_to_index = {IndexedHeap.HeapItem("yellow"): 0, 
                                        IndexedHeap.HeapItem("brown"): 1,
                                        IndexedHeap.HeapItem("ababacc"): 2,
                                        IndexedHeap.HeapItem("abc"): 3,
                                        IndexedHeap.HeapItem("aaaaaaa"): 4
                                        } 
                    ),
                    IndexedHeap_Stub.max_iheap_stub(
                        heap = [500,300,-1000, -1.5, math.pi] , 
                        item_to_index = {IndexedHeap.HeapItem(500): 0, 
                                        IndexedHeap.HeapItem(300): 1,
                                        IndexedHeap.HeapItem(-1000): 2,
                                        IndexedHeap.HeapItem(-1.5): 3,
                                        IndexedHeap.HeapItem(math.pi): 4
                                        } 
                    )
                                     
        ]
        for i in range(len(min_heaps)):
            self.assertEqual(min_heaps[i], min_heaps_stubs[i])
        
        for i in range(len(max_heaps)):
            self.assertEqual(max_heaps[i], max_heaps_stubs[i])

    def test_insert_peak_pop_with_duplicates(self):
        def test_min():
            min_heap = IndexedHeap.min_iheap()
            min_heap.insert(10)
            self.assertEqual(min_heap.peek(), 10)
            min_heap.insert(5)
            self.assertEqual(min_heap.peek(), 5)
            min_heap.insert(-100)
            self.assertEqual(min_heap.peek(), -100)
            min_heap.insert(1000)
            self.assertEqual(min_heap.peek(), -100)
            min_heap.insert(5)
            min_heap.insert(5)

            self.assertEqual(min_heap.pop(), -100)
            self.assertEqual(min_heap.pop(), 5)
            self.assertEqual(min_heap.pop(), 5)
            self.assertEqual(min_heap.pop(), 5)
            self.assertEqual(min_heap.pop(), 10)
            self.assertEqual(min_heap.pop(), 1000)
            with self.assertRaises(IndexError):
                min_heap.pop()
        
        def test_max():
            max_heap = IndexedHeap.max_iheap()
            max_heap.insert(10)
            self.assertEqual(max_heap.peek(), 10)
            max_heap.insert(15)
            self.assertEqual(max_heap.peek(), 15)
            max_heap.insert(-100)
            self.assertEqual(max_heap.peek(), 15)
            max_heap.insert(1000)
            self.assertEqual(max_heap.peek(), 1000)
            max_heap.insert(15)
            max_heap.insert(15)

            self.assertEqual(max_heap.pop(), 1000)
            self.assertEqual(max_heap.pop(), 15)
            self.assertEqual(max_heap.pop(), 15)
            self.assertEqual(max_heap.pop(), 15)
            self.assertEqual(max_heap.pop(), 10)
            self.assertEqual(max_heap.pop(), -100)
            with self.assertRaises(IndexError):
                max_heap.pop()
        
        test_min()
        test_max()

    def test_insert_remove_count(self):
        def test_min():
            min_heap = IndexedHeap.min_iheap()
            for _ in range(5):
                min_heap.insert(5)
            for i in range(10, 0, -1):
                min_heap.insert(i)
            self.assertEqual(min_heap.count(5), 6)
            self.assertEqual(len(min_heap), 15)
            min_heap.remove(5)
            self.assertEqual(min_heap.count(5), 5)
            self.assertEqual(len(min_heap), 14)
            min_heap.remove(5, 5)
            self.assertEqual(min_heap.count(5), 0)
            self.assertEqual(len(min_heap), 9)

        def test_max():
            max_heap = IndexedHeap.max_iheap()
            for _ in range(5):
                max_heap.insert(5)
            for i in range(10, 0, -1):
                max_heap.insert(i)
            self.assertEqual(max_heap.count(5), 6)
            self.assertEqual(len(max_heap), 15)
            max_heap.remove(5)
            self.assertEqual(max_heap.count(5), 5)
            self.assertEqual(len(max_heap), 14)
            max_heap.remove(5, 5)
            self.assertEqual(max_heap.count(5), 0)
            self.assertEqual(len(max_heap), 9)

        test_min()
        test_max()


if __name__ == "__main__":
    unittest.main()