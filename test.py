import numpy as np
import pandas as pd
import sys
import time
from julia.api import Julia
from quicksort import quickSort
from utils import df_to_arrowbytes, arrowbytes_to_df


def random_data(N, random_state=0):
    np.random.seed(random_state)

    df = pd.DataFrame({
        "index": np.random.randint(10*N, size=N),
        "value": np.random.randn(N),
    })
    df.loc[N-1, "index"] = -2
    df.loc[N-2, "index"] = -1

    return df


def quickSortJL(df, sort_col, low, high):
    jl = Julia(compiled_modules=False)
    jl.eval('include("quicksort.jl")')
    from julia.Main import quickSort as quicksort_jl

    # Convert to Julia 1-based indexing
    low, high = low+1, high+1

    arrowbytes = df_to_arrowbytes(df)
    result_bytes = quicksort_jl(arrowbytes, sort_col, low, high)
    result_df = arrowbytes_to_df(result_bytes)

    return result_df

def test_quicksort(N=50, sort_fcn=quickSort, random_state=0):
    # Generate random data
    df = random_data(N, random_state)

    # Save initial and final results
    comparison_df = df.copy().rename(columns=lambda c: "init_"+c)

    # Sort the DataFrame and get runtime
    start = time.time()
    result = sort_fcn(df, "index", 0, len(df)-1)
    end = time.time()-start
    print("\nRuntime (N={}): {:.2f}s".format(N, end))

    for c in result.columns:
        comparison_df["final_"+c] = result[c]

    # Print truncated result comparison
    print(comparison_df.head(), end="\n...\n")
    tail_string = comparison_df.tail().to_string()
    print(tail_string[tail_string.find("\n")+1:])


if __name__ == "__main__":
    N = 50 if len(sys.argv)==1 else int(sys.argv[1])
    test_quicksort(N, sort_fcn=quickSort)
    test_quicksort(N, sort_fcn=quickSortJL)
    test_quicksort(N, sort_fcn=quickSortJL)
