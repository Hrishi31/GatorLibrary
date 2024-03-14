class MinHeap:
    def __init__(self):
        # Initialize the heap with a dummy element at index 0 for easier index calculations.
        self.heap = [None]

    def insert(self, reservation):
        # Add the new reservation to the end of the heap.
        self.heap.append(reservation)
        # Restore the heap property by moving the new reservation up as necessary.
        self._bubble_up(len(self.heap) - 1)

    def _bubble_up(self, idx):
        # Base case: if we're at the root of the heap, do nothing.
        if idx <= 1:
            return
        # Calculate the parent's index.
        parent_idx = idx // 2
        if self.heap[parent_idx] is not None:
            # Compare the priorities of the current node and its parent.
            parent_priority = self.heap[parent_idx][1]
            current_priority = self.heap[idx][1]
            # Swap with the parent if the current node has a higher priority.
            if current_priority < parent_priority or (
                    current_priority == parent_priority and self.heap[idx][2] < self.heap[parent_idx][2]):
                self.heap[parent_idx], self.heap[idx] = self.heap[idx], self.heap[parent_idx]
                # Continue bubbling up.
                self._bubble_up(parent_idx)

    def extract_min(self):
        # If the heap is empty, return None.
        if len(self.heap) <= 1:
            return None
        # The smallest element is at the root of the heap.
        min_reservation = self.heap[1]
        # Replace the root with the last element in the heap.
        self.heap[1] = self.heap[-1]
        self.heap.pop()
        # Restore the heap property by moving the new root down as necessary.
        self._bubble_down(1)
        return min_reservation

    def _bubble_down(self, idx):
        smallest = idx
        left_idx = 2 * idx  # Index of left child
        right_idx = 2 * idx + 1  # Index of right child

        # Check if the left child exists and has higher priority than the current node.
        if left_idx < len(self.heap) and self.heap[left_idx]:
            if self.heap[left_idx][1] < self.heap[smallest][1] or (
                    self.heap[left_idx][1] == self.heap[smallest][1] and self.heap[left_idx][2] < self.heap[smallest][
                2]):
                smallest = left_idx

        # Check if the right child exists and has higher priority than the current node.
        if right_idx < len(self.heap) and self.heap[right_idx]:
            if self.heap[right_idx][1] < self.heap[smallest][1] or (
                    self.heap[right_idx][1] == self.heap[smallest][1] and self.heap[right_idx][2] < self.heap[smallest][
                2]):
                smallest = right_idx

        # If either child has higher priority, swap with that child and continue down the heap.
        if smallest != idx:
            self.heap[idx], self.heap[smallest] = self.heap[smallest], self.heap[idx]
            self._bubble_down(smallest)

    def is_empty(self):
        # The heap is empty if it only contains the dummy element.
        return len(self.heap) == 1
