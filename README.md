Simple example for cocotb with cocotb-test

# Installation

## Python environment

### Option 1 (easy): Using miniconda

Install miniconda for your user from here:

https://docs.conda.io/en/latest/miniconda.html#latest-miniconda-installer-links

I recommend to install it to a location such as ~/.python-miniconda and say yes 
to install as a default python distribution (modifies ~/.bashrc)

### Option 2: Using system python

This is also possible when the pthon3 version is reasonably recent (>= 3.7 should work)

try with:
```
python --version
python3 --version
```

If your default python is python2, all following commands need to append the 3, like ```python3```, ```pip3```, ```pytest3/pytest-3```

## Dependencies

Some of that dependencies might be unnecessary for this project, but are very practical for later
```
pip install coloredlogs numpy tqdm PyYAML pyzmq pytest cocotb cocotb-test
sudo yum install python36-pytest
#sudo yum search  pytest    # if package is not available
```

## Digital simulator

One simulator is sufficient, xcelium or icarus/iverilog will work. Personally I use both for different purposes

Do not try the iverilog version from the centos7 repo, this version is too old. You will need v11

iverilog website: http://iverilog.icarus.com/


## Test

To test the setup:
```
cd tests
SIM=xcelium pytest   # for xcelium
SIM=icarus pytest    # for icarus
```

This should show something like:
```
================================= test session starts =================================
platform linux -- Python 3.8.10, pytest-4.6.9, py-1.8.1, pluggy-0.13.0
rootdir: /mnt/Daten/Nosync/Schule/cocotb-test-examples
plugins: forked-1.4.0, xdist-2.5.0, cocotb-test-0.2.1
collected 30 items                                                                    

tests/unit/test_bcid_counter.py ...............                                 [ 50%]
tests/unit/test_bcid_counter_seperated.py ...............                       [100%]

============================= 30 passed in 30.93 seconds ==============================
```
