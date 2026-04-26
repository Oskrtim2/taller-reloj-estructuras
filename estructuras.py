class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class ListState:
    def append(self, dll, data): pass
    def prepend(self, dll, data): pass
    def remove(self, dll, data): pass
    def forward(self, dll): pass
    def backward(self, dll): pass


class EmptyListState(ListState):
    def append(self, dll, data):
        node = Node(data)
        dll.head = node
        dll.tail = node
        dll.current = node
        dll._size += 1
        dll._state = SingleListState()

    def prepend(self, dll, data):
        self.append(dll, data)

    def remove(self, dll, data):
        return False

    def forward(self, dll):
        return None

    def backward(self, dll):
        return None


class SingleListState(ListState):
    def append(self, dll, data):
        node = Node(data)
        node.prev = dll.tail
        dll.tail.next = node
        dll.tail = node
        dll._size += 1
        dll._state = MultiListState()

    def prepend(self, dll, data):
        node = Node(data)
        node.next = dll.head
        dll.head.prev = node
        dll.head = node
        dll._size += 1
        dll._state = MultiListState()

    def remove(self, dll, data):
        if dll.head.data == data:
            dll.head = None
            dll.tail = None
            dll.current = None
            dll._size = 0
            dll._state = EmptyListState()
            return True
        return False

    def forward(self, dll):
        return dll.current.data if dll.current else None

    def backward(self, dll):
        return dll.current.data if dll.current else None


class MultiListState(ListState):
    def append(self, dll, data):
        node = Node(data)
        node.prev = dll.tail
        dll.tail.next = node
        dll.tail = node
        dll._size += 1

    def prepend(self, dll, data):
        node = Node(data)
        node.next = dll.head
        dll.head.prev = node
        dll.head = node
        dll._size += 1

    def remove(self, dll, data):
        node = dll.head
        while node:
            if node.data == data:
                if dll.current == node:
                    dll.current = node.next or node.prev
                if node.prev:
                    node.prev.next = node.next
                else:
                    dll.head = node.next
                if node.next:
                    node.next.prev = node.prev
                else:
                    dll.tail = node.prev
                dll._size -= 1
                if dll._size == 1:
                    dll._state = SingleListState()
                elif dll._size == 0:
                    dll._state = EmptyListState()
                return True
            node = node.next
        return False

    def forward(self, dll):
        if dll.current.next:
            dll.current = dll.current.next
        else:
            dll.current = dll.head
        return dll.current.data

    def backward(self, dll):
        if dll.current.prev:
            dll.current = dll.current.prev
        else:
            dll.current = dll.tail
        return dll.current.data


class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None
        self._size = 0
        self._state = EmptyListState()

    def append(self, data):
        self._state.append(self, data)

    def prepend(self, data):
        self._state.prepend(self, data)

    def remove(self, data):
        return self._state.remove(self, data)

    def forward(self):
        return self._state.forward(self)

    def backward(self):
        return self._state.backward(self)

    def get_current(self):
        return self.current.data if self.current else None

    def go_to_start(self):
        self.current = self.head
        return self.current.data if self.current else None

    def to_list(self):
        result = []
        node = self.head
        while node:
            result.append(node.data)
            node = node.next
        return result

    def is_empty(self):
        return self._size == 0

    @property
    def size(self):
        return self._size

    def __len__(self):
        return self._size

    def __iter__(self):
        node = self.head
        while node:
            yield node.data
            node = node.next


class StackState:
    def push(self, stack, data): pass
    def pop(self, stack): pass
    def peek(self, stack): pass


class EmptyStackState(StackState):
    def push(self, stack, data):
        stack._items.append(data)
        stack._state = NonEmptyStackState()

    def pop(self, stack):
        return None

    def peek(self, stack):
        return None


class NonEmptyStackState(StackState):
    def push(self, stack, data):
        stack._items.append(data)

    def pop(self, stack):
        item = stack._items.pop()
        if len(stack._items) == 0:
            stack._state = EmptyStackState()
        return item

    def peek(self, stack):
        return stack._items[-1]


class Stack:
    def __init__(self):
        self._items = []
        self._state = EmptyStackState()

    def push(self, data):
        self._state.push(self, data)

    def pop(self):
        return self._state.pop(self)

    def peek(self):
        return self._state.peek(self)

    def is_empty(self):
        return len(self._items) == 0

    @property
    def size(self):
        return len(self._items)

    def to_list(self):
        return list(reversed(self._items))

    def clear(self):
        self._items.clear()
        self._state = EmptyStackState()

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return reversed(self._items)


class QueueState:
    def enqueue(self, queue, data): pass
    def dequeue(self, queue): pass
    def front(self, queue): pass


class EmptyQueueState(QueueState):
    def enqueue(self, queue, data):
        queue._items.append(data)
        queue._state = NonEmptyQueueState()

    def dequeue(self, queue):
        return None

    def front(self, queue):
        return None


class NonEmptyQueueState(QueueState):
    def enqueue(self, queue, data):
        queue._items.append(data)

    def dequeue(self, queue):
        item = queue._items.pop(0)
        if len(queue._items) == 0:
            queue._state = EmptyQueueState()
        return item

    def front(self, queue):
        return queue._items[0]


class Queue:
    def __init__(self):
        self._items = []
        self._state = EmptyQueueState()

    def enqueue(self, data):
        self._state.enqueue(self, data)

    def dequeue(self):
        return self._state.dequeue(self)

    def front(self):
        return self._state.front(self)

    def is_empty(self):
        return len(self._items) == 0

    @property
    def size(self):
        return len(self._items)

    def to_list(self):
        return list(self._items)

    def clear(self):
        self._items.clear()
        self._state = EmptyQueueState()

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)
