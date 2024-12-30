class Node:
    def __init__(self, frame, next_node=None, prev_node=None):
        self.frame = frame
        self.next = next_node  # Pointer to the next node
        self.prev = prev_node  # Pointer to the previous node


class LinkedFrameList:
    def __init__(self):
        self.head = None  # First node (oldest frame)
        self.tail = None  # Last node (latest frame)

    def add_frame(self, frame):
        """Add a new frame to the end of the list."""
        new_node = Node(frame)
        if self.tail:
            self.tail.next = new_node  # Link the current tail to the new node
            new_node.prev = self.tail  # Link the new node back to the current tail
        self.tail = new_node  # Update the tail pointer to the new node
        if not self.head:
            self.head = new_node  # If the list was empty, the new node is also the head

    def get_latest_one(self):
        """Get the latest frame (tail of the list)."""
        return self.tail

    def remove_oldest_frame(self):
        """Remove the oldest frame (head of the list)."""
        if self.head:
            self.head = self.head.next  # Move the head to the next node
            if self.head:
                self.head.prev = None  # Update the new head's prev pointer to None
            else:
                self.tail = None  # If the list is now empty, reset the tail as well

    def display_forward(self):
        """Display the list from oldest to latest frame."""
        current = self.head
        while current:
            print(current.frame, end=" <-> ")
            current = current.next
        print("None")

    def display_backward(self):
        """Display the list from latest to oldest frame."""
        current = self.tail
        while current:
            print(current.frame, end=" <-> ")
            current = current.prev
        print("None")