# Introduction
This program is to calculate the nematic orientation of liquid crystal particles around periodic meta atoms. The unit cells in this project are cylinders immersed in liquid crystal. I applied different voltages on the liquid crystal and run the openQmin software to simulate the orientation angle of a series of nanostructures with specific gap range and radius range. The [open-Qmin](https://github.com/sussmanLab/open-Qmin) Software is developed by the research groups of [Daniel Sussman](https://www.dmsussman.org/) and [Daniel Beller](https://bellerphysics.gitlab.io/).

In this project, we use the openQmin.out which is compiled from the open-Qmin project to conduct the simulation and create the boundary files according to the instructions from the open-Qmin project. To see more details about the compilation of the openQmin please refer to [this website](https://sussmanlab.github.io/open-Qmin/). 

To simplfy the process of running a set of simulations, I streamlined a series process into the bash code to run it on a HPC, including creating boundary files, simulation of the LC, integrate the simulation result and create the correspondant files for Lumerical FDTD to imput the LC directions.
# The whole process
1. create the boundary files
2. run the LdG simulations for LC orientations by running the qmin.sh. The qmin.sh includes following steps:
   - run openQmin.out adopting correspondant boundary files for different parameters
   - run merge.sh to concatenate the simulation files from the openQmin.out, typically in the name of "[0,50,100,150] V _ gap [gap length] _ radius [radius length] _ x[0-2] y[0-2] z[0-2].txt", into a big file without particular order
   - run analysis.py to transform the output .txt file into .csv file that can be import into Lumerical FDTD, to see more details please refer to [Lumerical FDTD database](https://optics.ansys.com/hc/en-us/articles/360034902033-Import-liquid-crystal-orientation-from-CSV-Simulation-object).
3. run the .lsf in Lumerical FDTD to import .csv files
# Basic use
## To create the virtual environment
```
conda create -n qmin python=3.12
conda activate qmin
pip install numpy 
```
## To create the boundary file
`bash boundaryfile.sh`
## To conduct the simulation of LC
`sbatch qmin.sh`

This bash file utlizes different number of CPU cores to run different boundary files (27 cores for boundary files divisible by 3, 8 cores for files divisible by 2, else 1 core).
Or run `sbatch fix.sh` which could run an array of parameters using one core. 
## Attention
I used a v100 GPU on an HPC for the simulation, please pay attention to the compilation steps if you use a different GPU.