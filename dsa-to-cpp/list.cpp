#include <cstddef>
#include <iostream>
#include <utility>

// Data_Type must be copyable. Search/count use ==, sort uses <,
// and display uses <<. Only the methods you use need these operators.
template <typename Data_Type>
class Node {
public:
    Data_Type value;
    Node* next;

    explicit Node(const Data_Type& value) : value(value), next(nullptr) {}
};

template <typename Data_Type>
class D_Node {
public:
    Data_Type value;
    D_Node* next;
    D_Node* prev;

    explicit D_Node(const Data_Type& value)
        : value(value), next(nullptr), prev(nullptr) {}
};

// Indexes are zero-based. Invalid insert/remove calls return false.
// A signed index type allows search to return -1 and rejects negative indexes.
template <typename Data_Type>
class list {
private:
    Node<Data_Type>* head = nullptr;
    Node<Data_Type>* tail = nullptr;
    std::ptrdiff_t length = 0;

    void clear() noexcept {
        while (head != nullptr) {
            Node<Data_Type>* old_head = head;
            head = head->next;
            delete old_head;
        }
        tail = nullptr;
        length = 0;
    }

    void swap(list& other) noexcept {
        std::swap(head, other.head);
        std::swap(tail, other.tail);
        std::swap(length, other.length);
    }

public:
    list() = default;

    // Deep copies prevent two lists from owning/deleting the same nodes.
    list(const list& other) {
        try {
            for (const Node<Data_Type>* node = other.head;
                 node != nullptr; node = node->next) {
                add(node->value);
            }
        } catch (...) {
            clear();
            throw;
        }
    }

    list(list&& other) noexcept { swap(other); }

    // Copy-and-swap also handles move assignment and self-assignment.
    list& operator=(list other) noexcept {
        swap(other);
        return *this;
    }

    // Insert BEFORE index; index == length appends. O(index), O(1) at ends.
    bool insert(const Data_Type& value, std::ptrdiff_t index) {
        if (index < 0 || index > length) {
            return false;
        }
        if (index == length) {
            add(value);
            return true;
        }

        Node<Data_Type>* node = new Node<Data_Type>(value);
        if (index == 0) {
            node->next = head;
            head = node;
        } else {
            Node<Data_Type>* previous = head;
            for (std::ptrdiff_t i = 1; i < index; ++i) {
                previous = previous->next;
            }
            node->next = previous->next;
            previous->next = node;
        }
        ++length;
        return true;
    }

    // Append in O(1) time using the tail pointer.
    void add(const Data_Type& value) {
        Node<Data_Type>* node = new Node<Data_Type>(value);
        if (tail == nullptr) {
            head = node;
        } else {
            tail->next = node;
        }
        tail = node;
        ++length;
    }

    // O(n) time: a singly linked list must find the tail's predecessor.
    bool remove() { return remove(length - 1); }

    // O(index) time, O(1) for the head. 'delete' is a C++ keyword.
    bool remove(std::ptrdiff_t index) {
        if (index < 0 || index >= length) {
            return false;
        }

        Node<Data_Type>* removed;
        if (index == 0) {
            removed = head;
            head = head->next;
            if (head == nullptr) {
                tail = nullptr;
            }
        } else {
            Node<Data_Type>* previous = head;
            for (std::ptrdiff_t i = 1; i < index; ++i) {
                previous = previous->next;
            }
            removed = previous->next;
            previous->next = removed->next;
            if (removed == tail) {
                tail = previous;
            }
        }
        delete removed;
        --length;
        return true;
    }

    // O(n) time, O(1) extra space; values are not copied.
    void reverse() noexcept {
        Node<Data_Type>* previous = nullptr;
        Node<Data_Type>* current = head;
        tail = head;
        while (current != nullptr) {
            Node<Data_Type>* next = current->next;
            current->next = previous;
            previous = current;
            current = next;
        }
        head = previous;
    }

    // Return the first matching index, or -1. O(n) worst-case time.
    std::ptrdiff_t search(const Data_Type& value) const {
        std::ptrdiff_t index = 0;
        for (const Node<Data_Type>* node = head;
             node != nullptr; node = node->next, ++index) {
            if (node->value == value) {
                return index;
            }
        }
        return -1;
    }

    // O(n) time, O(1) extra space.
    std::size_t count(const Data_Type& value) const {
        std::size_t occurrences = 0;
        for (const Node<Data_Type>* node = head;
             node != nullptr; node = node->next) {
            if (node->value == value) {
                ++occurrences;
            }
        }
        return occurrences;
    }

    // Example output: [1, 2, 3]. An empty list prints []. O(n) time.
    void display(std::ostream& output = std::cout) const {
        output << '[';
        for (const Node<Data_Type>* node = head;
             node != nullptr; node = node->next) {
            if (node != head) {
                output << ", ";
            }
            output << node->value;
        }
        output << "]\n";
    }

    // Stable ascending insertion sort: O(n^2) worst-case, O(n) when sorted,
    // O(1) extra space. Relink nodes instead of allocating/copying values.
    void sort() {
        if (head == nullptr) {
            return;
        }
        Node<Data_Type>* sorted_tail = head;
        while (sorted_tail->next != nullptr) {
            Node<Data_Type>* current = sorted_tail->next;
            if (!(current->value < sorted_tail->value)) {
                sorted_tail = current;
                continue;
            }

            Node<Data_Type>* previous = nullptr;
            Node<Data_Type>* position = head;
            // Insert after equal values to preserve their original order.
            while (position != current && !(current->value < position->value)) {
                previous = position;
                position = position->next;
            }

            // Compare before detaching so a throwing < leaves nodes owned.
            sorted_tail->next = current->next;
            if (current == tail) {
                tail = sorted_tail;
            }
            current->next = position;
            if (previous == nullptr) {
                head = current;
            } else {
                previous->next = current;
            }
        }
    }

    ~list() { clear(); }
};

template <typename Data_Type>
class D_list {
private:
    D_Node<Data_Type>* head = nullptr;
    D_Node<Data_Type>* tail = nullptr;
    std::ptrdiff_t length = 0;

    // Called only with a valid index. Start at whichever end is closer.
    D_Node<Data_Type>* node_at(std::ptrdiff_t index) const {
        if (index < length / 2) {
            D_Node<Data_Type>* node = head;
            for (std::ptrdiff_t i = 0; i < index; ++i) {
                node = node->next;
            }
            return node;
        }
        D_Node<Data_Type>* node = tail;
        for (std::ptrdiff_t i = length - 1; i > index; --i) {
            node = node->prev;
        }
        return node;
    }

    void clear() noexcept {
        while (head != nullptr) {
            D_Node<Data_Type>* old_head = head;
            head = head->next;
            delete old_head;
        }
        tail = nullptr;
        length = 0;
    }

    void swap(D_list& other) noexcept {
        std::swap(head, other.head);
        std::swap(tail, other.tail);
        std::swap(length, other.length);
    }

public:
    D_list() = default;

    D_list(const D_list& other) {
        try {
            for (const D_Node<Data_Type>* node = other.head;
                 node != nullptr; node = node->next) {
                add(node->value);
            }
        } catch (...) {
            clear();
            throw;
        }
    }

    D_list(D_list&& other) noexcept { swap(other); }

    D_list& operator=(D_list other) noexcept {
        swap(other);
        return *this;
    }

    // Insert BEFORE index; index == length appends.
    // O(1 + min(index, length - index)) time, O(1) at either end.
    bool insert(const Data_Type& value, std::ptrdiff_t index) {
        if (index < 0 || index > length) {
            return false;
        }
        if (index == length) {
            add(value);
            return true;
        }

        D_Node<Data_Type>* next = node_at(index);
        D_Node<Data_Type>* node = new D_Node<Data_Type>(value);
        node->next = next;
        node->prev = next->prev;
        if (next->prev == nullptr) {
            head = node;
        } else {
            next->prev->next = node;
        }
        next->prev = node;
        ++length;
        return true;
    }

    // O(1) time.
    void add(const Data_Type& value) {
        D_Node<Data_Type>* node = new D_Node<Data_Type>(value);
        node->prev = tail;
        if (tail == nullptr) {
            head = node;
        } else {
            tail->next = node;
        }
        tail = node;
        ++length;
    }

    // O(1) time: the tail has a direct pointer to its predecessor.
    bool remove() { return remove(length - 1); }

    // O(1 + min(index, length - 1 - index)) time, O(1) at either end.
    bool remove(std::ptrdiff_t index) {
        if (index < 0 || index >= length) {
            return false;
        }
        D_Node<Data_Type>* removed = node_at(index);
        if (removed->prev == nullptr) {
            head = removed->next;
        } else {
            removed->prev->next = removed->next;
        }
        if (removed->next == nullptr) {
            tail = removed->prev;
        } else {
            removed->next->prev = removed->prev;
        }
        delete removed;
        --length;
        return true;
    }

    // O(n) time, O(1) extra space.
    void reverse() noexcept {
        D_Node<Data_Type>* current = head;
        while (current != nullptr) {
            std::swap(current->next, current->prev);
            current = current->prev; // This was next before the swap.
        }
        std::swap(head, tail);
    }

    // Return the first matching index, or -1. O(n) worst-case time.
    std::ptrdiff_t search(const Data_Type& value) const {
        std::ptrdiff_t index = 0;
        for (const D_Node<Data_Type>* node = head;
             node != nullptr; node = node->next, ++index) {
            if (node->value == value) {
                return index;
            }
        }
        return -1;
    }

    // O(n) time, O(1) extra space.
    std::size_t count(const Data_Type& value) const {
        std::size_t occurrences = 0;
        for (const D_Node<Data_Type>* node = head;
             node != nullptr; node = node->next) {
            if (node->value == value) {
                ++occurrences;
            }
        }
        return occurrences;
    }

    // O(n) time. Accepts an optional stream for file output or testing.
    void display(std::ostream& output = std::cout) const {
        output << '[';
        for (const D_Node<Data_Type>* node = head;
             node != nullptr; node = node->next) {
            if (node != head) {
                output << ", ";
            }
            output << node->value;
        }
        output << "]\n";
    }

    // Stable ascending insertion sort: O(n^2) worst-case, O(n) when sorted,
    // O(1) extra space. Walk backward through the sorted prefix.
    void sort() {
        D_Node<Data_Type>* current = head == nullptr ? nullptr : head->next;
        while (current != nullptr) {
            D_Node<Data_Type>* next = current->next;
            D_Node<Data_Type>* position = current->prev;
            while (position != nullptr && current->value < position->value) {
                position = position->prev;
            }

            if (position != current->prev) {
                // Detach only after all comparisons for this node succeed.
                current->prev->next = current->next;
                if (current->next != nullptr) {
                    current->next->prev = current->prev;
                } else {
                    tail = current->prev;
                }

                current->prev = position;
                if (position == nullptr) {
                    current->next = head;
                    head->prev = current;
                    head = current;
                } else {
                    current->next = position->next;
                    position->next->prev = current;
                    position->next = current;
                }
            }
            current = next;
        }
    }

    ~D_list() { clear(); }
};
