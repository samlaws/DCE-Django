  # DCE

  The Defect classification engine is a website created using the Django package of python, the primary app of the site uses a pre-trained multilayer perceptron to classify defects from various sources.

  The site also supports user account creation and basic authentication.

  ## Requirements

  * Python Environment with:
    * Django
    * Django Crispy Forms
    * Django Tables 2
    * Dill
    * Tablib
    * Sklearn
    
  The quickest way to get these packages is to follow these steps in Anaconda prompt or the Command Line
  
  1. Navigate to the project directory
  2. Create a virtual environment
  3. Install the requirements using pip
  
  ```
  pip install -r requirements.txt
  ```

   ## TO DO

   * ~~Reproduce Michael's search bar functionality for searching body~~ Complete on test branch waiting for merge
   * Figure out how to improve the pagination buttons at the bottom of the table
   * ~~Make the table a fixed size~~ Complete on test branch waiting for merge
   * ~~Add a Requirements.txt to the repository~~
   * Rework reclassification (Sorry Kieran)
      * Add the reclassifaction form to the detail view?
      * Hide the column in the table and change it so that the column stores the old value and the classification column stores the new
   * Possibly add tests (shhh)
   * Project maintenance - Eg. decluttering by removing template files we no longer use and eventually changing the newspaper theme to something that makes sense
