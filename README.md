# BoschGLM50C

This is the laser distance measuring device. We are connecting to the PC using Bluetooth and getting the values to python script to display.

Here are the basic requirements for the setup:
1. A bluetooth Activated Bosch GLM 50 C device
2. Windows OS
3. Python 3.7 (which we tried)
4. PyBluez 0.22 for python 3.7 (Download the specific version(.whl) manually and install using the path as below)
  pip install "C:\Users\(username)\Downloads\PyBluez-0.22-cp37-cp37m-win_amd64.whl"
  pip install requests
5.install Microsoft visual studio c++ 2015/2017 Build tools using this link(http://go.microsoft.com/fwlink/?LinkId=691126&fixForIE=.exe.) - Need some patience, it will take an hour or two.

if you want to create a new environment install anaconda 3 and work with conda prompt (instead of command prompt)
  1.Download and install Anaconda for python
  2. create a environment(this command will create a new environment with python3.7 version installed)
    conda create --name py37 python=3.7
    conda activate py37
    pip install "C:\Users\(username)\Downloads\PyBluez-0.22-cp37-cp37m-win_amd64.whl"
    pip install requests
    
once setup is done, execute the file (test_bluetooth_bosch_glm50c.py)

attached the screenshot for the output.
