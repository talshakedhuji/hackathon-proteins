##!bin/bash
##Creating the vertial environment
#mkdir project4
#cd project4
#virtualenv -p /usr/bin/python3 newenv
#source newenv/bin/activate.csh
#
#pip install tensorflow~=2.0.0b1
#pip install numpy~=1.16.6
#pip install bio~=0.5.0
#pip install matplotlib~=3.4.2
#pip install pymolPy3~=0.1.2
#pip install logomaker~=0.8
#pip install pandas~=1.2.5
#pip tqdm~=4.61.1
#module load bioinfo
#moudle load pymol

#!bin/bash
#Creating the vertial environment
mkdir project4
cd project4
virtualenv -p /usr/bin/python3.7 newenv
source newenv/bin/activate.csh

#pip install tensorflow~=2.0.0b1
#pip install numpy~=1.16.6
#pip install bio~=0.5.0
#pip install matplotlib~=3.4.2
#pip install pymolPy3~=0.1.2
#pip install logomaker~=0.8
#pip install pandas~=1.2.5
#pip tqdm~=4.61.1
#module load bioinfo
#moudle load pymol

virtualenv -p /usr/bin/python3.7 newenv
source newenv/bin/activate.csh
module load bioinfo
module load pymol
cd project4/newenv/hackathon-proteins/
pip install -r requirements.txt
python3 main.py
