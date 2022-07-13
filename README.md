# User Scheduling in 5G

<p align="center">
  <img src="https://marceaucoupechoux.wp.imt.fr/files/2019/09/scheduler.png" alt="5G Antenna" />
</p>


## Brief Overview

In 5G, an antenna transmits data packets to smartphones (or users) through a wireless medium, which is divided into a set of frequency channels. The higher the power dedicated to a user, the higher the data rate it can experience. The exact dependence between power and data rate is however user and channel specific. With the same transmit power, a user close to the antenna will enjoy for example a higher data rate than a user far away. A wireless packet scheduler is thus responsible to allocated channels to users and to divide the total power budget of the antenna among the available channels. The goal of this project is to design optimal packet schedulers in this context.

Please find explanations on this project in the `subject.pdf` and `report.pdf` files.

## Test & results

1. This shell supports most linux shell functionalities including semicolon separated commands, piping, redirection, all basic linux commands etc. 
2. Foreground and Background processes can also be executed.

The following functions allow one to test each step of the project with any of the test file ('test1', 'test2', 'test3', 'test4' or 'test5'):

* Preprocessing

  * ``` bash
    testPreprocessing('test1')
    ```
* Greedy algorithm 

  * ``` bash
    testGreedy('test1')
    ```
    
* LP solver

  * ``` bash 
    testLP_solver('test1')
    ```
* Dynamic programming algorithm 

  * ``` bash
    testDP('test1')
    ```
  * ``` bash 
    testDP2('test1')
    ```
    
* Online stochastic algorithm

  * ``` bash 
    testOnline()
    ```
