### CS 121 Assignment 3 README

Prior to running the code, make sure the hierarchy of the directory structures as following:

cs121SE:
    .git/
    developer/DEV/*folders of subdomains (<= extract this from the zip file) 
    src/*.py
    __main__.py
    .gitignore
    cli.py
    InvertToFiles.py
    preprocess.py
    README.md
    TEST.md


## Instructions on setup/running code:

Make sure to have python 3.9 or later, we used Python 3.10.4 to code.
Make sure to install the following dependencies:
    - tqdm
    - tkinter
    - json
    - BeautifulSoup 4
    - pathlib

=========================================================


# 1. To create the inverted index:

Make sure to be on the root directory of this project such that you can access "python preprocess.py"

Run `python preprocess.py` This will roughly take 1:30 ~ 2 hours. There will be files created in the developer/DEV folder. The inverted index is in there.

Run `python InvertToFiles.py` This will roughly take 2 hours. This will convert the single file Inverted Index to multi-files located in developer/DEV/word_index_holder




# 2. To run the search engine:

Make sure to be on the root directory.

Run `python __main__.py` for the GUI interface. The interface will take roughly 2 ~ 5 seconds to load up. Entering in the search query and click search.

Run `python cli.py` for the command line interface. If you are on OpenLab then this is probably the only way to test. Type the search query in command line and press enter for search.























