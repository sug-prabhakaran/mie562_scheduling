# **Coding Assignment 2 - Solve Job Shop Problem (JSP) with Mixed Integer Programming (MIP)**

## **Formulation**

### **1. Parameters**

* $j \in J$: operation $j$ in set of all operations $J$
* $k \in K$: machine/resource $k$ in set of all resources $K$
* $J_{k}$: Set of all operations to be completed by resource $k$
* $\varepsilon$: Set of all operation pairs $(j,i)$ s.t i is constrained to be after j
* $n$: number of jobs
* $m$: number of machines
* $p_{j}$: processing time of operation j
* $M$: a very large constant

### **2. Objective Function:**

* $min C_{max}$

### **2. Decision Variables**

* $S_{j}$: Integer start time of operation $j$
* $z_{ji}$: Binary variable denoting 1 if j precedes *

### **3. Constraints**

(1) Makespan Constraints