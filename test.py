print("Claude")
print("Claude1")


def bubblesort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def test_sorted():
    assert bubblesort([3, 1, 2]) == [1, 2, 3]

def test_already_sorted():
    assert bubblesort([1, 2, 3]) == [1, 2, 3]

def test_empty():
    assert bubblesort([]) == []

def test_single():
    assert bubblesort([42]) == [42]

def test_duplicates():
    assert bubblesort([3, 1, 2, 1]) == [1, 1, 2, 3]
