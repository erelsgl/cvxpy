# cvxcore

## Introduction
Convex optimization modeling tools like CVX, CVXPY, and Convex.Jl translate high-level problem descriptions into low-level, canonical forms that are then passed to an backend solver. cvxcore is a software package that factors out the common operations that all such modeling systems perform into a single library with a simple C++ interface. cvxcore removes the need to reimplement this canonicalization process in new languages and provides significant performance gains over high level language implemententations.


## Usage with CVXPY
If you're using CVXPY update to it 0.3.0 or higher.

One can expect a 3 - 10x  speed-up over the original CVXPY implementation on most other problems.

<!-- ## Installation -->
<!-- cvxcore supports both Python 2 and Python 3. -->

<!-- 1. Install ``numpy`` with ``pip`` from the command-line. -->

<!-- ``` -->
<!-- pip install numpy -->
<!-- ``` -->

<!-- 2. Install ``cvxcore`` with ``pip`` from the command-line. -->

<!-- ``` -->
<!-- pip install cvxcore -->
<!-- ``` -->

<!-- Note: If you're installing cvxcore on Windows, a nonstandard system, or wish to build cvxcore directly from source, you need to install ```swig.``` We are currently working to remove this dependency. -->

<!-- On Linux, -->

<!-- ``` -->
<!-- sudo apt-get install swig -->
<!-- ``` -->

<!-- On Mac OSX, using homebrew, -->

<!-- ``` -->
<!-- brew install swig -->
<!-- ``` -->


## Integration with other CVX.* solvers
To use cvxcore with the CVX solver of your choice one must take the following steps:

1. Represent the problem's objective and constraints each as linear atom trees at some point during the solve process. To convert the linOp trees to a matrix representation, first call the wrapper to convert the high level language linOp tree into a C++ LinOp tree. This involves tree traversal, and some special cases depending on the representation of dense and sparse matrices. You may refer to the ```build_lin_op_tree``` function in **canonInterface.py** to see an example of how this is done.

2. Pass your vector of C++ LinOps into cvxcore's build matrix function. This will return a ```ProblemData``` structure, containing a sparse matrix representation of the problem data. Currently, final problem data is stored in COO representation using ```std::vector```. You should convert this to a data format accessable to the target language. For Python, this unpacking can be done efficiently using cvxcore's get{V/I/J} functions, which converts the representation to NUMPY arrays. For future languages, some work may be needed to do this efficiently.

3. With these two steps implemented, you have essentially recreated **canonInterface.py** in the language of your choice. You now should be able to execute code of the form

```python
V, I, J, b = canonInterface.get_problem_matrix(lin_expr_tree, var_offset_map)
```
where ```V, I, J``` is a COO representation of the problem matrix ```A```. Matrix ```V, I, J``` and vector ```b``` can then be passed to your solver as needed.

## Code Organization
- **/src/** contains the source code for cvxcore
	- **cvxcore.(c/h)pp** implements the matrix building algorithm. This file also provides the main access point into cvxcore's functionality, the ```build_matrix``` function.
	-  **LinOp.hpp** defines the LinOp class, linear atoms which we traverse during construction of the matrix.
	- **LinOpOperations.(c/h)pp** defines functions to get coefficients corresponding to each of the LinOps. This includes 18 special cases, one for each LinOp.
    - **ProblemData.hpp** defines the structure returned by ```build_matrix```, which includes a sparse representation of the problem matrix and the dense constant vector.

- **/src/python** contains code specific to our integration of cvxcore with CVXPY.
	- **canonInterface.py** implements code which calls our SWIG binding of cvxcore, including the function ```get_problem_matrix```. It also defines a function to create a C++ LinOp tree from a Python LinOp tree, handling a variety of special cases related to data representation.
    - **cvxcore.py** the Python binding autmatically generated by SWIG.

 - **cvxcore.i** exposes functions and data types to SWIG, which automatically generate bindings for cvxcore in a variety of common programming languages.

- **/tests/** contains code to test the accuracy and performance of cvxcore. **test_linops.py** tests a variety of problems to ensure that our basic LinOp construction and representation is correct. **huge_testman.py** benchmarks cvxcore on a variety of EE364A problems.



## Contact
If you have comments or concerns, please do not hesitate to contact one of us at  {piq93,jackzhu,millerjp}@stanford.edu.
