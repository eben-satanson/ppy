#!/bin/bash

sudo rmmod lp
sudo modprobe ppdev

sudo chmod 666 /dev/parport0

cd badanie
source ${HOME}/anaconda3/etc/profile.d/conda.sh
conda activate psychopy8
${HOME}/anaconda3/envs/psychopy8/bin/python3 ${HOME}/badanie/badanie.py
