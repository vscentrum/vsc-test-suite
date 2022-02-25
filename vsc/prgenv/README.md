# How to run the tests

## MPI Hello World test

The following has been tested on genius, hortense, and hydra

```shell
module load ReFrame
cd vsc/progenv
reframe --verbose --run --checkpath mpi_hello_world.py -C ../config_vsc.py
```

On Hortense, you first need to specify a credit account to which you have access

```shell
# specify Slurm account to use (credits)
export SBATCH_ACCOUNT='gadminforever'
```
