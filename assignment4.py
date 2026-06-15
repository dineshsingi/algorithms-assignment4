"""
Assignment 4: Heap Data Structures - Implementation, Analysis, and Applications
Author: Dinesh Singi
Course: MSCS-532 Algorithms and Data Structures
"""

import time
import random
import heapq


# =============================================================================
# SECTION 1: HEAPSORT
# =============================================================================

def heapify(arr, n, root_index):
    largest = root_index
    left_child  = 2 * root_index + 1
    right_child = 2 * root_index + 2

    if left_child < n and arr[left_child] > arr[largest]:
        largest = left_child

    if right_child < n and arr[right_child] > arr[largest]:
        largest = right_child

    if largest != root_index:
        arr[root_index], arr[largest] = arr[largest], arr[root_index]
        heapify(arr, n, largest)


def heapsort(arr):
    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr


# =============================================================================
# SECTION 2: TASK CLASS AND PRIORITY QUEUE
# =============================================================================

class Task:
    def __init__(self, task_id, name, priority, arrival_time=0, deadline=None):
        self.task_id      = task_id
        self.name         = name
        self.priority     = priority
        self.arrival_time = arrival_time
        self.deadline     = deadline

    def __repr__(self):
        return (f"Task(id={self.task_id}, name='{self.name}', "
                f"priority={self.priority}, arrival={self.arrival_time})")


class MaxHeapPriorityQueue:
    def __init__(self):
        self._heap    = []
        self._index   = {}
        self._counter = 0

    def _swap(self, i, j):
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]
        self._index[self._heap[i][2].task_id] = i
        self._index[self._heap[j][2].task_id] = j

    def _sift_up(self, pos):
        while pos > 0:
            parent = (pos - 1) // 2
            if self._heap[pos][0] > self._heap[parent][0]:
                self._swap(pos, parent)
                pos = parent
            else:
                break

    def _sift_down(self, pos):
        n = len(self._heap)
        while True:
            largest = pos
            left    = 2 * pos + 1
            right   = 2 * pos + 2
            if left  < n and self._heap[left][0]  > self._heap[largest][0]:
                largest = left
            if right < n and self._heap[right][0] > self._heap[largest][0]:
                largest = right
            if largest != pos:
                self._swap(pos, largest)
                pos = largest
            else:
                break

    def insert(self, task):
        entry = (task.priority, self._counter, task)
        self._counter += 1
        self._heap.append(entry)
        pos = len(self._heap) - 1
        self._index[task.task_id] = pos
        self._sift_up(pos)

    def extract_max(self):
        if self.is_empty():
            return None
        self._swap(0, len(self._heap) - 1)
        _, _, top_task = self._heap.pop()
        del self._index[top_task.task_id]
        if self._heap:
            self._sift_down(0)
        return top_task

    def increase_key(self, task_id, new_priority):
        pos = self._index[task_id]
        old_priority, counter, task = self._heap[pos]
        task.priority = new_priority
        self._heap[pos] = (new_priority, counter, task)
        self._sift_up(pos)

    def decrease_key(self, task_id, new_priority):
        pos = self._index[task_id]
        old_priority, counter, task = self._heap[pos]
        task.priority = new_priority
        self._heap[pos] = (new_priority, counter, task)
        self._sift_down(pos)

    def peek(self):
        return self._heap[0][2] if self._heap else None

    def is_empty(self):
        return len(self._heap) == 0

    def size(self):
        return len(self._heap)


# =============================================================================
# SECTION 3: QUICKSORT AND MERGE SORT (for comparison)
# =============================================================================

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot  = arr[random.randint(0, len(arr) - 1)]
    left   = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right  = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)


def mergesort(arr):
    if len(arr) <= 1:
        return arr
    mid   = len(arr) // 2
    left  = mergesort(arr[:mid])
    right = mergesort(arr[mid:])
    return _merge(left, right)


def _merge(left, right):
    result, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


# =============================================================================
# SECTION 4: BENCHMARKS
# =============================================================================

def timed(fn, data):
    start = time.perf_counter()
    fn(data[:])
    return (time.perf_counter() - start) * 1000.0


def run_benchmarks():
    sizes = [500, 1_000, 5_000, 10_000, 20_000]
    distributions = {
        "Random"  : lambda n: random.sample(range(n * 4), n),
        "Sorted"  : lambda n: list(range(n)),
        "Reversed": lambda n: list(range(n - 1, -1, -1)),
    }
    print("\n" + "=" * 72)
    print("EMPIRICAL BENCHMARK: Heapsort vs Quicksort vs Merge Sort (ms)")
    print("=" * 72)
    for dist_name, gen in distributions.items():
        print(f"\n--- {dist_name} Input ---")
        print(f"{'n':>8}  {'Heapsort':>12}  {'Quicksort':>12}  {'Merge Sort':>12}")
        print("-" * 52)
        for n in sizes:
            data = gen(n)
            hs = timed(heapsort, data)
            qs = timed(quicksort, data)
            ms = timed(mergesort, data)
            print(f"{n:>8}  {hs:>12.2f}  {qs:>12.2f}  {ms:>12.2f}")


# =============================================================================
# SECTION 5: SCHEDULER SIMULATION
# =============================================================================

def scheduler_simulation():
    print("\n" + "=" * 72)
    print("TASK SCHEDULER SIMULATION (Max-Heap Priority Queue)")
    print("=" * 72)
    pq = MaxHeapPriorityQueue()
    tasks = [
        Task(1, "System Backup",      priority=3,  arrival_time=0, deadline=10),
        Task(2, "Critical DB Patch",  priority=10, arrival_time=1, deadline=3),
        Task(3, "Send Email Report",  priority=1,  arrival_time=2, deadline=20),
        Task(4, "Security Scan",      priority=7,  arrival_time=3, deadline=8),
        Task(5, "Log Rotation",       priority=2,  arrival_time=4, deadline=15),
        Task(6, "Memory Diagnostics", priority=5,  arrival_time=5, deadline=12),
    ]
    print("\nInserting tasks into the priority queue:")
    for t in tasks:
        pq.insert(t)
        print(f"  Inserted: {t}")
    print(f"\nQueue size: {pq.size()}")
    print(f"Top task (peek): {pq.peek()}")
    print("\nDemonstrating increase_key: Task 3 priority 1 -> 9")
    pq.increase_key(3, 9)
    print("Demonstrating decrease_key: Task 4 priority 7 -> 4")
    pq.decrease_key(4, 4)
    print("\nProcessing tasks in priority order:")
    order = 1
    while not pq.is_empty():
        task = pq.extract_max()
        print(f"  [{order}] Executing: {task}")
        order += 1


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    sample = [64, 25, 12, 22, 11, 90, 3]
    print("Original:", sample)
    print("Heapsorted:", heapsort(sample[:]))
    run_benchmarks()
    scheduler_simulation()