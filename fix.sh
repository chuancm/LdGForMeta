#!/bin/bash
#SBATCH --mem=4Gb
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=48:00:00
#SBATCH --gres=gpu:v100:1
#SBATCH --job-name=fix
#SBATCH --output /gpfs/home/mc10709/code/logfiles/fix%j.out 
#SBATCH --mail-type=END,FAIL      # Mail events (NONE, BEGIN, END, FAIL, ALL)
#SBATCH --mail-user=muchuanchen8@gmail.com     # Where to send mail 

module load anaconda3/gpu/new
conda activate qmin
module unload gcc
module load openmpi/3.1.4_cuda
module load cuda
module load gcc12/12.2.0
# conda activate qmin
# !!!!!!!!!!!!!!!!!!!!!!!!!!!ATTENTION!!!!!!!!!!!!!!!!!!!!!!!!!!!
# the Lx Ly Lz in the parameter is not equal to the size of the physical model
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

# e=0.03587 # for 150V e = 0.03587 100V e = 0.02391 50V e = 0.01196
volt_array=()
gap_array=(90 150 80 80 50 30 120 130 150 110 30 20)
radius_array=(85 65 150 120 85 145 100 75 125 145 65 60)
size=${#gap_array[@]}
for ((i=0;i<size;i+=1));do
	volt=0V
	gap=${gap_array[i]}
	radius=${radius_array[i]}
	if [[ "$volt" == "150V" ]];then
		e=0.03587
		echo 150V
	elif [[ "$volt" == "100V" ]];then
		e=0.02391
		echo 100V
	elif [[ "$volt" == "50V" ]];then
		e=0.01196
		echo 50V
	elif [[ "$volt" == "0V" ]];then
		e=0
		echo 0V
	else
		echo input error
	fi
	# gap=100
	# radius=130		
	g=$((gap/10)) # the properties in mes
	r=$(echo "scale=1;$radius/10" | bc)
	p=$(echo "$g+2*$r" | bc)
	Lx=$(((gap+radius*2)/10))
	Ly=$Lx
	Lz=150
	p_int=$(printf "%.0f" $p)
	echo "g=${g}" "r=${r}" "Lx= ${Lx}"	
	/gpfs/home/mc10709/open-Qmin/build/openQmin.out -z 2  --GPU -1 --phaseConstantA -1 --phaseConstantB -12.3 --phaseConstantC 10.1 --deltaT 0.0002 --fTarget 1e-10 --iterations 150000 --randomSeed -1 --L1 0.349 --L2 0.0 --L3 0.0 --L4 0.0 --L6 0.0 --Lx "$((Lx))" --Ly "$((Ly))" --Lz "$((Lz))" --boundaryFile /gpfs/home/mc10709/ldg/boundryfiles/gap"${g}"_radius"${r}".txt --saveFile /gpfs/home/mc10709/ldg/result/"${volt}"gap"${g}"_radius"${r}" --linearSpacedSaving -1 --logSpacedSaving -1 --stride 1 --hFieldX 0 --hFieldY 0 --hFieldZ 0 --hFieldMu0 1 --hFieldChi 1 --hFieldDeltaChi 0.5 --eFieldX 0 --eFieldY "${e}" --eFieldZ 0 --eFieldEpsilon0 1  --eFieldEpsilon 2.34 --eFieldDeltaEpsilon 0.6867
	echo current structure is finished. Analyzing... 
	mv /gpfs/home/mc10709/ldg/result/"${volt}"gap"${g}"_radius"${r}"_x0y0z0.txt /gpfs/home/mc10709/ldg/result/"${volt}"gap"${g}"_radius"${r}".txt
	python /gpfs/home/mc10709/code/analysis.py "${p}" /gpfs/home/mc10709/ldg/result/"${volt}"gap"${g}"_radius"${r}".txt /gpfs/home/mc10709/ldg/result_csv/"${volt}"gap"${g}"_radius"${r}".csv
done
echo All simulations are completed!
