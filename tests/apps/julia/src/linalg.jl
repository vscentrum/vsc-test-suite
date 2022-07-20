using Pkg
Pkg.update()
Pkg.add("BenchmarkTools")

using LinearAlgebra: similar
using LinearAlgebra
using BenchmarkTools

function main(args)
    BLAS.set_num_threads(parse(Int, args[1]))
    println("Julia version: ", VERSION)
    println("BLAS num threads: ", args[1])

    sz = 4096
    A = rand(sz, sz)
    B = rand(sz, sz)
    C = similar(A)
    F = A*A'

    time = @belapsed mul!($C, $A, $B)
    println("Dotted two $sz x $sz matrices in $time s.")

    time = @belapsed cholesky($F)
    println("Cholesky decomposition of a $sz x $sz matrix in $time s.")

    time = @belapsed lu($A)
    println("LU decomposition of a $sz x $sz matrix in $time s.")
end

println(ARGS)
main(ARGS)