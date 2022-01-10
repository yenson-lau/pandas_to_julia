# Inplace Quicksort for Pandas DataFrames
#   Based on code by Mohit Kumra and Anush Krishna V


# Swap two rows in a DataFrame

def swap_rows(df, i, j):
    df.iloc[i], df.iloc[j] = df.iloc[j], df.iloc[i].copy()


# This function takes last element as pivot, places
# the pivot element at its correct position in sorted
# array, and places all smaller (smaller than pivot)
# to left of pivot and all greater elements to right
# of pivot

def partition(df, sort_col, low, high):
    i = (low-1)             # index of smaller element
    arr = df[sort_col]      # col to be sorted

    pivot = arr.iloc[high]  # pivot

    for j in range(low, high):

        # If current element is smaller than or
        # equal to pivot
        if arr.iloc[j] <= pivot:

            # increment index of smaller element
            i = i+1
            swap_rows(df, i, j)

    swap_rows(df, i+1, high)
    return (i+1)


# The main function that implements QuickSort
# arr[] --> Array to be sorted,
# low  --> Starting index,
# high  --> Ending index

def quickSort(df, sort_col, low, high):
    if len(df) == 1:
        return df

    if low < high:
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(df, sort_col, low, high)

        # Separately sort elements before
        # partition and after partition
        quickSort(df, sort_col, low, pi-1)
        quickSort(df, sort_col, pi+1, high)

    return df
