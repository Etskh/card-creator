# card-creator



## MILESTONE 1
### Basic Type Editing
- ✓ can edit a card type
- ✓ fields can be selected
- ✓ fields can be dragged to move around
- ✓ can modify name
- ✓ can modify alignment
- ✓ add fields to the card type
- ✓ remove fields from the card type


## MILESTONE 2
### Basic Card Editing
- ✓ a bar up top to show all the card types
  `[             -dk. grey-                      ]`
- ✓ in the bar, list all card types as buttons
  `[ {#card types}                               ]`
- ✓ these buttons will show the cardtype below as a list of card data
  `[ {#card types}                               ]`
- ✓ second bar will switch between the different card-type views
  `[ view | layout     -light green-             ]`
- ✓ a table of existing cards
  `[ view | layout | data   -light green-        ]`
- ✓ each card has a number beside it denoting how many in the deck (4x)


## MILESTONE 3
### Field Patterns
- you can create a template for a field at the cardtype level
  this will provide a value for the field data doesn't exist for that card
- by default, the field data will be grayed out in the view
- you can use `{title}` in the fields to print out the title
- each card has a collection of rules
- rules are text with a decimal weight of benefit or detriment
- rules can be put into a field with the `{rules}` string
- create integer values for each card, like fields
- these numbers cannot be null
- fields can reference data in the cards with `{#data-name}`


## MILESTONE 4
### Advanced Card Editing:
- create a new card creates a new row in the table
- changing fields in the text edit view popup
- remove style from model
- add italic boolean to field
- add bold boolean to field
- add font-family selectbox to field
    <link href="https://fonts.googleapis.com/css?family=Amatic+SC:700|Open+Sans+Condensed:300" rel="stylesheet">
    font-family: 'Open Sans Condensed', sans-serif;
    font-family: 'Amatic SC', cursive;
- add text-size boolean to field
- create side bar for cardtype editing
- change name of cardtype
- change background of cardtype


## MILESTONE 5
### Automatic Deployment
- add secret_key env to heroku account
- add secret_key env to pycharm environment
- add travis build key to heroku account
- ✓ spruce up the page
  <link href="https://fonts.googleapis.com/css?family=Oswald" rel="stylesheet">
  body { font-family: 'Oswald', sans-serif; }


## MILESTONE 6
### Project
- `[                  -black-                    ]`
  bar at top of screen to show current project
- `[ Project Name     -black-                    ]`
  Project name is the name of the active project
- `[ Project Name     -black-             {gear} ]`
  where `{gear}` is the project settings page!
- project settings page has editable name
- project settings page has delete option
- `[ Project Name     -black-             {gear} ][ {+} ]` <- dk. green
  {+} is the button to create a new project
- new project page has text-box for project name and save!
- `[ Project Name     -black-             {gear} ][ {list} {+} ]`
  `{list} show a list of all projects that user owns
- if user has no projects, {list} doesn't show up
- project list page has names of all projects to go to their page


## MILESTONE 8
### Art on Card
- allow file uploads as hashed jpgs
- as an extra piece of data for each card: have unique art
- this can be uploaded from the card data entry area
- there are checks for size to make sure it's not too big, or small
- `{art}` puts the image in the field with pos:abs, w/h:100%


## MILESTONE 7
### Users
- if not logged in, show log-in screen to log-in
- upon login, go to project list
- add button to bar at top for user page
- `[ Project Name            {gear} ][ {list} {+} {user} ]`
  where `{user}` will go to user settings
- user settings has a name field for the user


## MILESTONE 9
### Symbols
- create a symbol group and several icons for use in the fields
- symbols can be referenced in fields with [@symbol-name]
- card-data can be null, and if a card-data is null, it it replaced by a symbol
- along with symbols, projects have enumerations which are like select box items
- enumerations can be added like tags to cards


## MILESTONE 12
### Maff n' Graff
- every card has the curve computed from:
   data (nominator or denominator) * their scale
   rule benefit or detriment * situational
- the jedi value is visible in the data table
- it is also graphable
- with the data and rules, we can compute a graph
- to show all the cards in the project
- we can go from one cardtype to the graph show the jedi curve



- cards have a template field that is modifyable
- there is a callback `onkeyup()` that sets a Timeout which will save the field when it is up. If it's called again, it resets the timer


- create a `CardView` class in `view.py`, which takes a card-type
- you can create a template for a field at the cardtype level this will provide a value for the field data doesn't exist for that card
- by default, the field data will be grayed out in the view
- you can use {title} in the fields to print out the title
- you can use {count} in the fields to print out the count
- each card has a collection of rules
- rules are text with a decimal weight of benefit or detriment
- rules can be put into a field with the {rules} string
- create integer values for each card, like fields
- these numbers cannot be null
- fields can reference data in the cards with {#data-name}


## Features

### MVP
- each card has a set of rules that are { text, weight }
- each card-type has a set of data that each card must possess
- each card has a dataset of the data that corresponds with the values and names of the card-type data. Possible implementation: text-field of an array of integers: `[1,2,3,4,5]`
- the follow fields are accessible with vanilla braces: `{title}`, `{count}`, `{rules}`. Possible implementations: `get_fields()` function on a card- this will return a full array of the Fields, complete with text. Other implementation: having a `CardView` object which has `get_fields()` function and 
  - `{title}`: the title of the card
  - `{count}`: the number of this type of card
  - `{rules}`: a list of the rules of the card
- card-data can be referenced with braces and a hash proceeding the name. For example: {#attack}, {#defence}, {#cost}

### Eventually
- project symbols can be printed out with an "at" symbol proceeding the name for example: {@red-mana}, {@blue-mana}...
- symbols can be repeated with card-data, so if the user wants {@heart} to appear three times on the card to represent the number of #wounds, they can add {@heart|#wounds}
- each card has unique art, which is placed 
