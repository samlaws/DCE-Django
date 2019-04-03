  # DCE

  The Defect classification engine is a website created using the Django package of python, the primary app of the site uses a pre-trained multilayer perceptron to classify defects from various sources.

  The site also supports user account creation and basic authentication.

  ## Requirements

  * Python Environment with:
    * Django
    * Django Crispy Forms
    * Django Tables 2
    * Dill
    * Sklearn


   ## TO DO

   * Reproduce Michael's search bar functionality for searching body
   * Figure out how to improve the pagination buttons at the bottom of the table
   * Make the table a fixed size
   * Add a Requirements.txt to the repository
   * Rework reclassification (Sorry Kieran)
      * Add the reclassifaction form to the detail view?
      * Hide the column in the table and change it so that the column stores the old value and the classification column stores the new
   * Possibly add tests (shhh)
