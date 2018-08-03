These code is for COMP9334 Project, UNSW, author: Xiaowei Zhou, z5108173
===================================
To test few data:
Ready all configuration files and run ./wrapper.py
Note. Same configuration at different test (e.g. It is first test or second test) will have different result as the test index affect random seed (for random simulation only)
===================================
For large amount testing (e.g. same configuration for 30 times):
Edit buildFile.py to determine a specific delayedoff value for specific times of tests.
Then by using ./run.sh, buildFile.py will construct configure files for tests, and then tests will run automatically. After simulation finish, MRT and 95% CI is calculated automatically.
./Tdistribution.py is used to get average of n tests and 95% CI.
./expDistribution.py is used for supporting random number generation correctness.
./clear.sh is used to REMOVE all configure files and output files for tests.
===================================
directory reproducibility contains configurations and outputs for reproducibility check
===================================
directory results contains MRT,std dev,CI result for different delayedoff time to support report
===================================
randomSimulation function in sim.py is NOT used since it is replace by buildTrace and traceSimulation
