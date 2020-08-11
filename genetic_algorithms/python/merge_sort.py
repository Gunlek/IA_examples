def merge(A, B):
    if A == []:
        return B
    elif B == []:
        return A
    elif A[0] <= B[0]:
        return [A[0]] + merge(A[1::], B)
    else:
        return [B[0]] + merge(A, B[1::])

def merge_sort(A):
    if len(A) <= 1:
        return A
    else:
        return merge(merge_sort(A[:len(A)//2]), merge_sort(A[len(A)//2:]))