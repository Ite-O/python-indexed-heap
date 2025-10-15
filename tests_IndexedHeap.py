import unittest
import Indexed_Heap
import math
import IndexedHeap_Stub

class Test_IndexedHeap(unittest.TestCase):    
    def test_heapify(self):
        arr_1 = [500, 300, -1000, -1.5, math.pi]
        arr_2 = ["ababacc", "brown", "yellow", "abc", "aaaaaaa"]
        arr_3 = [-1000,-1.5,500, 300, math.pi]

        max_heaps =[Indexed_Heap.MaxHeap(arr_1),
                    Indexed_Heap.MaxHeap(arr_2),
                    Indexed_Heap.MaxHeap(arr_3)
                    ]
        min_heaps = [Indexed_Heap.MinHeap(arr_1),
                    Indexed_Heap.MinHeap(arr_2),
                    Indexed_Heap.MinHeap(arr_3)
                    ]
        
        min_heaps_stubs = [
                    IndexedHeap_Stub.min_heap_stub(
                        heap = [-1000,-1.5,500, 300, math.pi], 
                        item_to_index = {Indexed_Heap.HeapItem(-1000): 0, 
                                        Indexed_Heap.HeapItem(-1.5): 1,
                                        Indexed_Heap.HeapItem(500): 2,
                                        Indexed_Heap.HeapItem(300): 3,
                                        Indexed_Heap.HeapItem(math.pi): 4
                                        }             
                    ),
                    IndexedHeap_Stub.min_heap_stub(
                        heap = ["aaaaaaa", "ababacc", "yellow", "abc", "brown"], 
                        item_to_index = {Indexed_Heap.HeapItem("aaaaaaa"): 0, 
                                        Indexed_Heap.HeapItem("ababacc"): 1,
                                        Indexed_Heap.HeapItem("yellow"): 2,
                                        Indexed_Heap.HeapItem("abc"): 3,
                                        Indexed_Heap.HeapItem("brown"): 4
                                        } 
                    ),
                    IndexedHeap_Stub.min_heap_stub(
                        heap = [-1000,-1.5,500, 300, math.pi], 
                        item_to_index = {Indexed_Heap.HeapItem(-1000): 0, 
                                        Indexed_Heap.HeapItem(-1.5): 1,
                                        Indexed_Heap.HeapItem(500): 2,
                                        Indexed_Heap.HeapItem(300): 3,
                                        Indexed_Heap.HeapItem(math.pi): 4
                                        }             
                    )                 
        ]
        max_heaps_stubs = [
                    IndexedHeap_Stub.max_heap_stub(
                        heap = [500, 300, -1000, -1.5, math.pi], 
                        item_to_index = {Indexed_Heap.HeapItem(500): 0, 
                                        Indexed_Heap.HeapItem(300): 1,
                                        Indexed_Heap.HeapItem(-1000): 2,
                                        Indexed_Heap.HeapItem(-1.5): 3,
                                        Indexed_Heap.HeapItem(math.pi): 4
                                        }             
                    ),
                    IndexedHeap_Stub.max_heap_stub(
                        heap = ["yellow", "brown", "ababacc", "abc", "aaaaaaa"], 
                        item_to_index = {Indexed_Heap.HeapItem("yellow"): 0, 
                                        Indexed_Heap.HeapItem("brown"): 1,
                                        Indexed_Heap.HeapItem("ababacc"): 2,
                                        Indexed_Heap.HeapItem("abc"): 3,
                                        Indexed_Heap.HeapItem("aaaaaaa"): 4
                                        } 
                    ),
                    IndexedHeap_Stub.max_heap_stub(
                        heap = [500,300,-1000, -1.5, math.pi] , 
                        item_to_index = {Indexed_Heap.HeapItem(500): 0, 
                                        Indexed_Heap.HeapItem(300): 1,
                                        Indexed_Heap.HeapItem(-1000): 2,
                                        Indexed_Heap.HeapItem(-1.5): 3,
                                        Indexed_Heap.HeapItem(math.pi): 4
                                        } 
                    )
                                     
        ]
        for i in range(len(min_heaps)):
            self.assertEqual(min_heaps[i], min_heaps_stubs[i])
        
        for i in range(len(max_heaps)):
            self.assertEqual(max_heaps[i], max_heaps_stubs[i])

    def test_insert_peak_pop_with_duplicates(self):
        def test_min():
            min_heap = Indexed_Heap.MinHeap()
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
            max_heap = Indexed_Heap.MaxHeap()
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
            min_heap = Indexed_Heap.MinHeap()
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
            min_heap.remove(5, strict=False)
            self.assertEqual(len(min_heap), 9)
            min_heap.remove(1, 100, strict=False)
            self.assertEqual(len(min_heap), 8)
            ordered_list = list(min_heap)
            self.assertEqual(len(ordered_list), 8)

        def test_max():
            max_heap = Indexed_Heap.MaxHeap()
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
            max_heap.remove(5, strict=False)
            self.assertEqual(len(max_heap), 9)
            max_heap.remove(1, 100, strict=False)
            self.assertEqual(len(max_heap), 8)
            max_heap.insert(10, 3)
            ordered_list = list(max_heap)
            self.assertEqual(len(ordered_list), 11)
            
            a = Indexed_Heap.MaxHeap()
            b = Indexed_Heap.MaxHeap()
            print(a == b)

        test_min()
        test_max()


if __name__ == "__main__":
    unittest.main()