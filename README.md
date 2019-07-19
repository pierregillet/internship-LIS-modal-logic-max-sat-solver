Max SAT solver for Modal Logic
==============================

Dependencies
------------
The Python version must be `3.7.3` or above.

The dependencies are :
* `PLY >= 3.11`
* `Pytest >= 5.0.1`
    
Installation
------------
### Pipenv (recommended) ###
To install the dependencies, run the following command at the root of the repository:

    $ pipenv install

and then, to activate the virtual environment (must be done every time we run a new shell session): 

    $ pipenv shell

### System-wide (discouraged) ###
Install the dependencies with:

    $ pip3 install <dependency>

or, depending on the OS or Linux distribution:    
     
    $ pip install <dependency>
    
### Other methods ###
Other methods do exist (such as bare virtual environments, etc.) but I won't cover them here.
The only requirement is that dependencies listed above do exist in the PYTHONPATH at runtime.

Testing
-------
The project can be tested with:

    $ pytest tests

Usage
-----
### Setup ###
The clauses must be written one per line 

### Execution ###
The project can be run with:

    $ python3 <file_to_run>

or, depending on the OS or Linux distribution:

    $ python <file_to_run>

Input syntax
------------
The solver does not support parenthesis nor the implication for now.

There must be one clause per line, in its conjunctive normal form (clausal normal form).

The symbols are as follows:

|Input   | Meaning|
|--------|--------|
| -      | ¬      |
| []     | ☐      |
| <>     | ◇      |
| &      | ∧      |
| &#124; | ∨      |
| ->     | →      |
