#!/bin/bash
#SBATCH -o job%j.out
#SBATCH --mem=16Gb
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1 
#SBATCH --ntasks=1
#SBATCH --time=01:00:00
#SBATCH --gres=gpu:v100:1
#SBATCH --job-name=boundryfiles
conda activate boundary
for ((gap=20;gap<=200;gap+=10));do
	for ((radius=50;radius<=150;radius+=5));do
		Lx=$((gap + radius * 2))
		Ly=$Lx
		Lz=1500
		echo $Lx $Ly	
		python /gpfs/home/mc10709/code/boundaryCreator.py -x "${Lx}" -y "${Ly}" -z "${Lz}" --gap "${gap}" --radius "${radius}"
	done
done
echo boundary files are created!
