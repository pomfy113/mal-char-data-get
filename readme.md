# Basic Usage:
1. OPTIONAL: Run season-get.py to grab all seasonal anime IDs, or create your own.
    - To run, use ```python season-get.py [year] [season, lowercase]```
    - Format for each file is newline separated numbers similar to:
    ```
        1
        2
        3
    ```
    - Heavily suggested that you clean the IDs yourself; it does not have a filter as of now
2. Run create-csv.py to grab everything in the txt file you created
    - To run, use ```python create-csv.py [name of input] [name of output]```
    - It will grab the file from input, and save a new one at output
    - As said above, heavily suggested that you pick and choose the IDs yourself
    - You can customize the .txt file it draws from; see above
    - Format is:
    ```
        title,charLastName, charFirstName,role,seiyuuLastName, seiyuuFirstName
        OR
        title,charName,role,seiyuuLastName, seiyuuFirstName
    ```
