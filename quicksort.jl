using Arrow, DataFrames
using PyCall

function swap_rows!(df::DataFrame, i::Int, j::Int)::Nothing
    df[i,:], df[j,:] = df[j,:], copy(df[i,:])
    return nothing
end

function partition(df::DataFrame,
                   sort_col::String,
                   low::Int,
                   high::Int
                   )::Int

    i = low
    arr = df[!, sort_col]
    pivot = arr[high]

    for j in low:high-1
        if arr[j] <= pivot
            swap_rows!(df, i, j)
            i += 1
        end
    end

    swap_rows!(df, i, high)
    return i
end

function quickSort!(df::DataFrame,
                    sort_col::String,
                    low::Int,
                    high::Int
                    )::DataFrame
    if size(df, 1) == 1
        return df
    end

    if low < high
        pi = partition(df, sort_col, low, high)

        quickSort!(df, sort_col, low, pi-1)
        quickSort!(df, sort_col, pi+1, high)
    end
    return df
end

function quickSort(bytes::Vector{UInt8},
                   sort_col::String,
                   low::Int,
                   high::Int
                   )::PyObject

    df = DataFrame(Arrow.Table(bytes))

    result = quickSort!(df, sort_col, low, high)

    io = IOBuffer()
    Arrow.write(io, result)
    seekstart(io)

    result_bytes = take!(io)
    return PyCall.pybytes(result_bytes)
end
