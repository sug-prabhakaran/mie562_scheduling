# **Coding Assignment 2 - Solve Job Shop Problem (JSP) with Mixed Integer Programming (MIP)**

## **References**

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

(1) Makespan Constraints
