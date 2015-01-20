landing-gear
============

Landing gear system in Scade (B6-1 ENSTA ParisTech course)

## Getting the project

You can both get the project as a .zip file at the following url :

http://github.com/wrousseau/landing-gear/archive/master.zip

or by cloning the project (git is required)

    git clone https://github.com/wrousseau/landing-gear

## Opening the Project

Just open the LandingGear Studio Workspace file with Scade Suite.

## Running the tests

Running the tests requires Python.

Scade simulation output files (.csv format) are to be placed in the `Tests/Raw` and are to be named Rxx.csv (where Rxx is the label of the requirement corresponding to the simulation).

Requirement files are json files and are to be placed in the `Tests/Requirements` folder. They are to be named Rxx.req (where Rxx is the label of the requirement). An example of such a file is given below. The package prefix must be given if the tested operator is within a package. Then an array of rules is given, where we test at a given simulation `step` whether or not a `variable` (output of the operator) has an `expectedValue`.

    {
       "packagePrefix":"ControlPackage::CommandLine/",
	"rules":
	[
		{
			"step": 149,
			"variable": "gears_locked_down",
			"expectedValue": true
		},
		{
			"step": 149,
			"variable": "doors_closed",
			"expectedValue": true
		}
	]
    }

To run the tests, the following commands much be ran :

    cd Tests
    python tester.py --requirement Rxx

Running the following command will run all files named Rxx in the `Tests/Requirements` folder

    python tester.py

The test results are outputted both on the standard output and in the `Tests/Results` directory as .txt files.
