ver

sz = 4096;

A = rand(sz, sz);
B = rand(sz, sz);
F = A*A';

time = [];

for i = 1:10
    tic;

    C = A*B;

    time(i) = toc;
end
fprintf('Dot product: %f s.\n', mean(time));

for i = 1:10
    tic;

    chol(F);

    time(i) = toc;
end
fprintf('Cholesky factorisation: %f s.\n', mean(time));

for i = 1:10
    tic;

    lu(A);

    time(i) = toc;
end
fprintf('LU factorisation: %f s.\n', mean(time));

