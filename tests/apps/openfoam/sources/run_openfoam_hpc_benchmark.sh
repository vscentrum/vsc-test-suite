#!/bin/bash -l

ntasks=$1

commit=1d4577f92644d2de308bf6568c6f153989ecf3dc
case=HPC_motorbike
size=Large
version=v8

# Prepare environment
source $FOAM_BASH

# Prepare a job-specific work directory in $REFRAME_SCRATCHDIR
if [ ! -z ${SLURM_JOB_ID+x} ]
then
    workdir=${REFRAME_SCRATCHDIR}/reframe_${SLURM_JOB_ID}
elif [ ! -z ${PBS_JOBID+x} ]
then
    workdir=${REFRAME_SCRATCHDIR}/reframe_${PBS_JOBID}
else
    echo "Failed to create work directory"
fi
origdir=$(pwd)
echo "Original directory: " ${origdir}
echo "Work directory: " $workdir
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

# Check mesh and copy back logfile
. $WM_PROJECT_DIR/bin/tools/RunFunctions
runApplication checkMesh
cp log.checkMesh ${origdir}

# Run case
chmod u+x Allclean
chmod u+x Allrun
./Allrun

# Copy main logfile
cp log.simpleFoam log.checkMesh ${origdir}
