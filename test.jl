include("quicksort.jl")


function random_data(N::Int;
    rng::AbstractRNG=MersenneTwister(1234)
    )::DataFrame

    df = DataFrame(Dict(
    "index" => rand(rng, 0:10*N-1, N),
    "value" => randn(rng, N),
    ))
    df[N, "index"] = -2
    df[N-1, "index"] = -1

    return df
end


function test_quicksort(;N::Int=50)::Nothing
    df = random_data(N)

    print("\nInitial DataFrame: ")
    show(df, allrows=false, display_size=(19, 32))
    println("")

    println("\nQuickSort (N=$(N)): ")
    @time quickSort!(df, "index", 1, size(df,1))

    print("\nSorted DataFrame: ")
    show(df, allrows=false, display_size=(19, 32))
    println("")

end


if abspath(PROGRAM_FILE) == @__FILE__
    N = length(ARGS) > 0 ? parse(Int, ARGS[1]) : 50
    test_quicksort(N=N)
end
