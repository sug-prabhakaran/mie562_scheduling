# **Coding Assignment 2 - Solve Job Shop Problem (JSP) with Mixed Integer Programming (MIP)**

## **References and Resources Used**

1. [01 Knapsack Problem in Python and Gurobi (Youtube) - Decision Making 101](https://www.youtube.com/watch?v=t6_Dpq7L3YQ&list=PLjiMsqjDUvBj0Oz3hpzKEOsMScSi3Mp_u&index=1&pbjreload=101)  This tutorial was great introduction of creating models in Gurobi using Python and walking through an easier example: the knapsack problem.

2. [Gurobi and Python. Capacitated Vehicle Routing Problem - Hernan Caceras](https://www.youtube.com/watch?v=7_-Xuq2xKdc&pbjreload=101)  Another tutorial of building a model in Gurobi using Python with a more complex example.  This has good information using different data structures for creating variables.

3. [JSP Problem Instances with Solutions - tammy0612](https://github.com/tamy0612/JSPLIB).  This GitHub page has various problem instances in the standard JSP problem instance format that can be used to test the model.  I copied several smaller (less than 10 x 10) problem instances into the quercus_instances folder to validate this model and program.

## **Problem Introduction**

The standard job shop scheduling problem (JSP) is a known NP-hard problem that requires more advanced techniques to solve due to their exponentially increasing complexity with respect to instance size.  One technique is the Mixed Integer Linear Programming (MIP) formulation, which relies on branch and bounding, relaxation into a linear programming and inferences to reduce the search size.  Gurobi is one of the best industrial solvers that applies these algorithms.

In the formulation below, you will see the general model for a JSP that was built into the Gurobi program.  Test instances in the standard JSP problem instance format are in the instances folder.  The program will take an input test instance and solve the JSP using the model and output the results in the following format:

  * (makespan, {job_0:\[operation_0: start_time_00, operation_1: start_time_01, ..., operation_j_0: start_time_0j], ... job_n:\[operation_0: start_time_n0, ..., operation j_n: star_time_nj]})

## **Formulation**

### **1. Parameters**


* <a href="https://www.codecogs.com/eqnedit.php?latex=j&space;\in&space;J" target="_blank"><img src="https://latex.codecogs.com/gif.latex?j&space;\in&space;J" title="j \in J" /></a>: operation ***j*** in set of all operations ***J***
* <a href="https://www.codecogs.com/eqnedit.php?latex=k&space;\in&space;K" target="_blank"><img src="https://latex.codecogs.com/gif.latex?k&space;\in&space;K" title="k \in K" /></a>: machine/resource ***k*** in set of all resources ***K***
* <a href="https://www.codecogs.com/eqnedit.php?latex=j&space;\in&space;J_{k}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?j&space;\in&space;J_{k}" title="j \in J_{k}" /></a>: Set of all operations ***j*** to be completed by resource ***k***
* <a href="https://www.codecogs.com/eqnedit.php?latex=\varepsilon" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\varepsilon" title="\varepsilon" /></a>: Set of all operation pairs ***(j,i)*** s.t ***i*** is constrained to be after ***j***
* <a href="https://www.codecogs.com/eqnedit.php?latex=n" target="_blank"><img src="https://latex.codecogs.com/gif.latex?n" title="n" /></a>: number of jobs
* <a href="https://www.codecogs.com/eqnedit.php?latex=m" target="_blank"><img src="https://latex.codecogs.com/gif.latex?m" title="m" /></a>: number of machines
* <a href="https://www.codecogs.com/eqnedit.php?latex=p_j" target="_blank"><img src="https://latex.codecogs.com/gif.latex?p_j" title="p_j" /></a>: processing time of operation ***j***
*<a href="https://www.codecogs.com/eqnedit.php?latex=M" target="_blank"><img src="https://latex.codecogs.com/gif.latex?M" title="M" /></a>: a very large constant

### **2. Objective Function:**

* <a href="https://www.codecogs.com/eqnedit.php?latex=\min&space;C_{max}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\min&space;C_{max}" title="\min C_{max}" /></a>

### **2. Decision Variables**

* <a href="https://www.codecogs.com/eqnedit.php?latex=S_j" target="_blank"><img src="https://latex.codecogs.com/gif.latex?S_j" title="S_j" /></a>: Integer start time of operation ***j***
* <a href="https://www.codecogs.com/eqnedit.php?latex=z_{ji}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?z_{ji}" title="z_{ji}" /></a>: Binary variable denoting if ***j** precedes ***i***
* <a href="https://www.codecogs.com/eqnedit.php?latex=C_{max}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?C_{max}" title="C_{max}" /></a>: makespan, which is the latest finishing time of all operations

### **3. Constraints**

**1. Makespan Constraints**

**2. Precedence Constraints**

**3. Resource Constraints**

**4. Starting Time >= 0**
