# Package binparse 
This code provide functionality of parsing binary file and searching patterns.

## Using
- Open file main.py
- In main function create object of class BinaryParse with arg file_path to binary file
- Execute function from public interface of class
- Return result of any functions
- In root directory will create results file with JSON output

## Unit tests
To run JSON test of binparse package execute from root directory:  
`python -m unittest binparse/tests/tests.py`

## Measure performance
To measure time of script working use Linux utility `time`:  
`time python main.py`
