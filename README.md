# PBEST-Docker 

This repository contains a Docker image of [PBEST](https://github.com/NoamShental/PBEST), 
used to screen COVID-19 samples via group testing, 
as described in the manuscript 
["Efficient high throughput SARS-CoV-2 testing to detect asymptomatic carriers"](https://www.medrxiv.org/content/10.1101/2020.04.14.20064618v1), by Shental et al.

The PBEST protocol allows screening 384 samples using 48 pools, 
where each sample appears in six pools 
according to a Reed-Solomon error-correcting code.

PBEST-Docker allows you to analyze experimental results and detect positive carriers.

Please visit the links above for more details about PBEST and how make the pooling

## Requirements

You need [docker-engine](https://docs.docker.com/engine/installation/) 

See [docker docs](https://docs.docker.com/engine/)


## Quickstart

The first execution could require several minutes, from the second one will be faster.

Clone the repository:  
```commandline
$ git clone https://github.com/next-crs4/PBEST-Docker
```

Cd into the docker directory:  
```commandline
$ cd PBEST-Docker
```

### Using the Makefile

Print the help message
```commandline
$ make help

Please use `make <target>` where <target> is one of
  build                   build the pbest image
  clean                   remove the pbest image from your computer
```

Build the PBEST image
```commandline
$ make build
```
If successfully built:
```commandline
Successfully built 5ae8a1ad8216 
Successfully tagged pbest:Dockerfile

Ready to start. Try:
        pbest --help
        pbest-test --help
```

List all the locally stored Docker images
```commandline
$ docker images

REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
pbest               Dockerfile          5ae8a1ad8216        24 minutes ago      1.88GB
python              3                   7f5b6ccd03e9        13 days ago         934MB
```
## PBEST script
Starting from experimental results, **pbest** script detect positive carriers.

Print the help message
```commandline
$ pbest --help

usage: pbest [-h] --input-file FILE --output-file FILE [--output-format STR]
             [--force] [--logfile PATH]

Run PBEST algorithm to identify COVID-19 positive carriers

optional arguments:
  -h, --help            show this help message and exit
  --input-file FILE, -i FILE
                        input file (experimental results)
  --output-file FILE, -o FILE
                        output file (detected samples)
  --output-format STR, -t STR
                        Output file format: [tsv,csv,xlsx]
  --force, -f           force to overwrite output file
  --logfile PATH        log file (default=stderr)
```
An example of input-file .xlsx can be found 
[here](https://github.com/next-crs4/PBEST-Docker/blob/master/examples/ExpTwoCarriersResults.xlsx).
Each row represents a pool: the first column identifies the pool, the second is a flag equals to '1' if the pool contains an unknown positive
In this example, there are 12 pool set to '1': 6,8,15,20,21,27,31,32,34,39,41,46

Put this file in a local folder: ```/path/to/local/data/ExpTwoCarriersResults.xlsx```
Now, run the **pbest** script
```bash
$ pbest -i /path/to/local/data/ExpTwoCarriersResults.xlsx -o /path/to/local/data/DetectedSamples.xlsx
```
In this examples, the detected samples are `[72, 142]`.  The related output-file .xlsx can be found 
[here](https://github.com/next-crs4/PBEST-Docker/blob/master/examples/DetectedSamples.xlsx).

Use `-f` option to overwrite output file and `-t` to choose an other format (.csv or .tsv)

## PBEST-TEST script
It tests the robustness and reliability of the **pbest** script, creating a dummy input-file with know positive carriers.

Print the help message
```commandline
$ pbest-test --help

usage: pbest-test [-h] {random,select} ...

create dummy .xlsx files and test it

positional arguments:
  {random,select}

optional arguments:
  -h, --help       show this help message and exit
```
### Random
```commandline
$ pbest-test random --help

usage: pbest-test random [-h] --number INTEGER --output-file FILE [--force]
                         [--run] [--logfile PATH]

optional arguments:
  -h, --help            show this help message and exit
  --number INTEGER, -n INTEGER
                        number of asymptomatic carriers to be created
  --output-file FILE, -o FILE
                        output xlsx file
  --force, -f           force to overwrite output file
  --run, -r             run pbest script
  --logfile PATH        log file (default=stderr
```

Example: create a dummy file with 3 positive carrier (random)
```commandline
$ pbest-test random -n 3 -o /path/to/local/data/Random3Carriers.xlsx -r

....
2020-06-23 15:32:13|INFO    |pBestTest |Carriers: [192, 218, 311]
2020-06-23 15:32:13|INFO    |pBestTest |Detected Samples: [192, 218, 311]
2020-06-23 15:32:13|INFO    |pBestTest |Testing successful!!!
```

### Select
```commandline
$ pbest-test select --help

usage: pbest-test select [-h] --carriers INT [INT ...] --output-file FILE
                         [--force] [--run] [--logfile PATH]

optional arguments:
  -h, --help            show this help message and exit
  --carriers INT [INT ...], -c INT [INT ...]
                        list of asymptomatic carriers to be created
  --output-file FILE, -o FILE
                        output xlsx file
  --force, -f           force to overwrite output file
  --run, -r             run pbest script
  --logfile PATH        log file (default=stderr)
```

Example: create a dummy file with 3 positive carrier on you choose
```commandline
$  pbest-test select -c 35 187 261 -o /path/to/local/data/Selected3Carriers.xlsx  -r

....
2020-06-23 15:46:08|INFO    |pBestTest |Carriers: [35, 187, 261]
2020-06-23 15:46:08|INFO    |pBestTest |Detected Samples: [35, 187, 261]
2020-06-23 15:46:08|INFO    |pBestTest |Testing successful!!!
```

## Finishing
Remove PBEST images from local computer
```bash
$ make clean
```


