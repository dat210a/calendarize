# calendarize

### DAT210 Group A Project
#### Yearly calendar
An interactive timeline for keeping track of yearly recurring events.  
[TODO list](app/README.md)

#### Resources
More will be added as they become relevant
* HTML/CSS/JS
    * [Material Design guidelines](https://material.io/guidelines/)
    * [Materialize CSS framework](http://materializecss.com)
* Python/Flask/SQL
    * [Flask documentation](http://flask.pocoo.org/)  
    * [Jinja2 documentation](http://jinja.pocoo.org/)  
    * [Python documentation](https://docs.python.org/3/)  
* Local documentation
    * [cfg readme](app/cfg/README.md)
    * [funcs readme](app/funcs/README.md)
    * [db readme](app/db/README.md)
    
#### Guidelines
The python code for this project loosely follows [PEP 8 style guidelines](https://www.python.org/dev/peps/pep-0008/).  
Some IDEs/editors come with PEP8 linting by default, but there should be linting packages for most of the common editors.  

It is not crucial to follow every rule to the letter; i.e. the "shadows from outer scope" guideline is often worth breaking to make code more readable.  
Whether or not breaking this makes your code more or less readable is up to personal judgement, however.

Refactoring code to conform with the guidelines after the fact is easy (and will be done once the code is deemed complete), so not following them isn't going to ruin things, but it's recommended that you try and follow the guidelines from the beginning.

**Note:**  
It's not good practice to have frameworks such as the materialize.css framework we're using in the repo itself.  
This should be something users of the repo would have to download and setup themselves, but we've decided to have it in the repo to make it easier for people to run the app.  


**WARNING: This is likely to change in the future; the materialize.css files will probably be removed from the repo, at which point each user is responsible for making sure they have the framework installed correctly.**
