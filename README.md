# [Discovering Polarized Communities in Signed Networks](http://edoardogalimberti.altervista.org/documents/papers/***.pdf)

## Folders
* datasets: datasets listed in Table 1
* polarized_communities: code

## Code
To use the code, first run 'python setup.py build_ext --inplace' from the folder 'polarized_communities/'.
This command builds the .c files created by Cython.
Alternatively, without running the mentioned command, it is possible to directly execute the Python code.

## Execution
Run the following command from the folder 'polarized_communities/':
  'python main.py [-h] [-b B] d a'

#### Positional arguments:
  * d           dataset
    * highlandtribes
    * cloister
    * congress
    * bitcoin
    * wikielections
    * twitterreferendum
    * slashdot
    * wikiconflict
    * epinions
    * wikipolitics
    
  * a           algorithm
    * eigensign       (Algorithm 1)
    * random_eigensign        (Algorithm 2)
    * greedy_signed_degree        (Greedy)
    * bansal        (Bansal)
    * random_local        (LocalSearch)

#### Optional arguments:
  * -h, --help  show the help message and exit

  * -b       multiplicative factor for random_eigensign ('l1' or float, 'l1' default)
  	
#### Example:
  'python main.py cloister random_eigensign -b 1.7'
