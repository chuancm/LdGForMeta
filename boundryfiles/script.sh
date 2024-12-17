#!/bin/bash
#SBATCH -o job.%j.out
#SBATCH --mem=32Gb
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1 
#SBATCH --ntasks=27
#SBATCH --time=3:30:00
#SBATCH --gres=gpu:v100:1
#SBATCH --job-name=qmin
module unload gcc
module load openmpi/3.1.4_cuda 
module load cuda
module load gcc12/12.2.0 

mpirun -n 27 /gpfs/home/mc10709/open-Qmin/build/openQmin.out -z 2  --GPU -1 --phaseConstantA -1 --phaseConstantB -12.3 --phaseConstantC 10.1 --deltaT 0.0002 --fTarget 1e-18 --iterations 500000 --randomSeed -1 --L1 0.349 --L2 0.0 --L3 0.0 --L4 0.0 --L6 0.0 --Lx 12 --Ly 12 --Lz 50 --boundaryFile /gpfs/home/mc10709/ldg/boundryfiles/nanodisk_10.txt --saveFile /gpfs/home/mc10709/ldg/result/z0interval10 --linearSpacedSaving -1 --logSpacedSaving -1 --stride 1 --hFieldX 0 --hFieldY 0 --hFieldZ 0 --hFieldMu0 1 --hFieldChi 1 --hFieldDeltaChi 0.5 --eFieldX 0 --eFieldY 0.03587 --eFieldZ 0 --eFieldEpsilon0 1  --eFieldEpsilon 2.34 --eFieldDeltaEpsilon 0.6867

tar -cf ./ldg/result/test8_z2_150V.tar ./ldg/result/z0interval10* 
