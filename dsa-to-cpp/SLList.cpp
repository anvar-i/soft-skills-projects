#include <iostream>
using namespace std;

/*
Simple analog of Single Linked List
*/

template <typename T>

class Node {
public:
    T value;
    Node<T>* next;

    Node(const T& newValue) : value(newValue), next(nullptr) {}
};


class SingleLinkedList {
public:
    Node<T>* first;
    Node<T>* last;

    SingleLinkedList() {
        first = nullptr;
        last = nullptr;
    }

    ~SingleLinkedList() {
        Node<T>* current = first;

        while (current != nullptr) {
            Node<T>* nextNode = current->next;
            delete current;
            current = nextNode;
        }
    }

    // Add a value to the end of the list.
    void add(const T& value) {
        Node<T>* newNode = new Node<T>(value);

        if (first == nullptr) {
            first = newNode;
            last = newNode;
        } else {
            last->next = newNode;
            last = newNode;
        }
    }

    // Insert a value before index. Index 0 means the beginning.
    // Returns false when the index is invalid.
    bool insert(int index, const T& value) {
        if (index < 0) {
            return false;
        }

        if (index == 0) {
            Node<T>* newNode = new Node<T>(value);
            newNode->next = first;
            first = newNode;

            if (last == nullptr) {
                last = newNode;
            }
            return true;
        }

        Node<T>* previous = first;
        int currentIndex = 0;

        while (previous != nullptr && currentIndex < index - 1) {
            previous = previous->next;
            ++currentIndex;
        }

        if (previous == nullptr) {
            return false;
        }

        Node<T>* newNode = new Node<T>(value);
        newNode->next = previous->next;
        previous->next = newNode;

        if (newNode->next == nullptr) {
            last = newNode;
        }
        return true;
    }

    // Remove the value at index. Returns false when the index is invalid.
    // The method is called remove because delete is a C++ keyword.
    bool remove(int index) {
        if (index < 0 || first == nullptr) {
            return false;
        }

        Node<T>* removedNode;

        if (index == 0) {
            removedNode = first;
            first = first->next;

            if (first == nullptr) {
                last = nullptr;
            }
        } else {
            Node<T>* previous = first;
            int currentIndex = 0;

            while (previous != nullptr && currentIndex < index - 1) {
                previous = previous->next;
                ++currentIndex;
            }

            if (previous == nullptr || previous->next == nullptr) {
                return false;
            }

            removedNode = previous->next;
            previous->next = removedNode->next;

            if (removedNode == last) {
                last = previous;
            }
        }

        delete removedNode;
        return true;
    }

    // Return the first matching index, or -1 when the value is not found.
    int search(const T& value) const {
        Node<T>* current = first;
        int index = 0;

        while (current != nullptr) {
            if (current->value == value) {
                return index;
            }

            current = current->next;
            ++index;
        }

        return -1;
    }

    // Return the total number of nodes in the list.
    int count() const {
        int total = 0;
        Node<T>* current = first;

        while (current != nullptr) {
            ++total;
            current = current->next;
        }

        return total;
    }

    // Sort values in ascending order using selection sort.
    void sort() {
        for (Node<T>* current = first; current != nullptr; current = current->next) {
            Node<T>* smallest = current;

            for (Node<T>* scan = current->next; scan != nullptr; scan = scan->next) {
                if (scan->value < smallest->value) {
                    smallest = scan;
                }
            }

            if (smallest != current) {
                T temporary = current->value;
                current->value = smallest->value;
                smallest->value = temporary;
            }
        }
    }

    // Print all values from first to last.
    void display() const {
        Node<T>* current = first;

        while (current != nullptr) {
            cout << current->value << " ";
            current = current->next;
        }
        cout << endl;
    }

    // Reverse the links so the last node becomes the first node.
    void reverse() {
        Node<T>* previous = nullptr;
        Node<T>* current = first;
        last = first;

        while (current != nullptr) {
            Node<T>* nextNode = current->next;
            current->next = previous;
            previous = current;
            current = nextNode;
        }

        first = previous;
    }
};
