#!/bin/bash -l

ntasks=$1

commit=1d4577f92644d2de308bf6568c6f153989ecf3dc
case=HPC_motorbike
size=Large
version=v8

# Prepare environment
source $FOAM_BASH

# Prepare a job-specific work directory in $VSC_SCRATCH
if [ ! -z ${SLURM_JOB_ID+x} ]
then
    workdir=${VSC_SCRATCH}/reframe_${SLURM_JOB_ID}
elif [ ! -z ${PBS_JOBID+x} ]
then
    workdir=${VSC_SCRATCH}/reframe_${PBS_JOBID}
else
    echo "Failed to create work directory"
fi
origdir=$(pwd)
echo $workdir
mkdir -p ${workdir}
cd ${workdir}

# Download input files
git clone https://develop.openfoam.com/committees/hpc.git
cd hpc
git checkout ${commit}
cd ${case}/${size}/${version}

# Prepare mesh
sed -i "s/numberOfSubdomains.*/numberOfSubdomains ${ntasks};/" system/decomposeParDict
mesh_script=Allmesh${size:0:1}
chmod u+x ${mesh_script}
./${mesh_script}

# Check mesh
. $WM_PROJECT_DIR/bin/tools/RunFunctions
runParallel checkMesh

# Run case
chmod u+x Allclean
chmod u+x Allrun
./Allrun

# Copy back files
cp log.simpleFoam log.checkMesh ${origdir}
