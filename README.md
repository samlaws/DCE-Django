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

   * Figure out how to improve the pagination buttons at the bottom of the table
   * Add tests
   * Project maintenance - Eg. decluttering by removing template files we no longer use and eventually changing the newspaper theme to something that makes sense
   * Make delete view a pop up
