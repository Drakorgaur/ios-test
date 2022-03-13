# ios-test
**Python tests created to check ios project 1.**
## Disclaimer 

### Please read it

**This test is not shows your real project correctness.**  
It just helps you to correct your global mistakes. 

Project could be written in different ways. I tried to remove
chance that test will fail if subsequence differ.  
That means I had to use sort() function that will sort all lines 
in my file and your output. Be careful.


## Usage
```
Usage: test.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  directory  Shows all available directories for test
  run        run tests for corona.sh.
```
To check run options:
>./test.py run --help

PS _corona.sh have to be in the same directory with test.py or look  
write `./test.py run -f/--file <path/to/file.sh>`_


## Possible problems
1) If script not running without `sudo` please do
>sudo chmod -R +x test.py
2) If You are using Windows test will print `Test running currently on linux only`
 
## At the end I want to say

Feel free to modify test for your use.  

Also, I would be very happy if you contribute with help and send PRs  
to improve test.

Thank You for using this test.  
Best regards,  
Mark
