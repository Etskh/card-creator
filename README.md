# card-creator



## MILESTONE 1
### Basic Type Editing:
✓ can edit a card type
✓ fields can be selected
- fields can be dragged to move around
- can modify width
- can modify alignment
- add fields to the card type
- remove fields from the card type


MILESTONE 2
Basic Card Editing:
- a bar up top to show all the card types
  [             -dk. grey-                      ]
- in the bar, list all card types as buttons
  [ {#card types}                               ]
- these buttons will show the cardtype below as a list of card data
  [ {#card types}                               ]
- second bar will switch between the different card-type views
  [ view | layout     -light green-             ]
- a table of existing cards
  [ view | layout | data   -light green-        ]
- create a new card creates a new row in the table
- changing fields in the text edit view popup
- each card has a number beside it denoting how many in the deck (4x)


MILESTONE 3
Automatic Deployment:
- add secret_key env to heroku account
- add secret_key env to pycharm environment
- add travis build key to heroku account
- spruce up the page
  \<link href="https://fonts.googleapis.com/css?family=Oswald" rel="stylesheet">
  body { font-family: 'Oswald', sans-serif; }


MILESTONE 4
Advanced Card Editing:
- remove style from model
- add italic boolean to field
- add bold boolean to field
- add font-family selectbox to field
    \<link href="https://fonts.googleapis.com/css?family=Amatic+SC:700|Open+Sans+Condensed:300" rel="stylesheet">
    font-family: 'Open Sans Condensed', sans-serif;
    font-family: 'Amatic SC', cursive;
- add text-size boolean to field
- create side bar for cardtype editing
- change name of cardtype
- change background of cardtype


MILESTONE 5
Project:
- [                  -black-                    ]
 bar at top of screen to show current project
- [ Project Name     -black-                    ]
 Project name is the name of the active project
- [ Project Name     -black-             {gear} ]
 {gear} is the project settings page!
- project settings page has editable name
- project settings page has delete option
- \[ Project Name     -black-             {gear} ][ {+} ] <- dk. green
 {+} is the button to create a new project
- new project page has text-box for project name and save!
- \[ Project Name     -black-             {gear} ][ {list} {+} ]
 {list} show a list of all projects that user owns
- if user has no projects, {list} doesn't show up
- project list page has names of all projects to go to their page


MILESTONE 6
Field Templates:
- you can create a template for a field at the cardtype level
- this will provide a value for the field data doesn't exist for that card
- by default, the field data will be grayed out in the view
- you can use [field-name] in the fields to print out other fields
- it makes sure that you don't have any circular dependencies


MILESTONE 7
Users:
- if not logged in, show log-in screen to log-in
- upon login, go to project list
- add button to bar at top for user page
- \[ Project Name            {gear} ][ {list} {+} {user} ]
 {user} will go to user settings
- user settings has a name field for the user


MILESTONE 8
Rules:
- each card has a collection of rules
- rules are text with a decimal weight of benefit or detriment
- rules can be put into a field with the `{rules}` string


MILESTONE 9
Art on Card:
- As an extra piece of data for each card: have unique art
- this can be uploaded from the card data entry area
- there are checks for size to make sure it's not too big, or small
- {art} puts the image in the field with pos:abs, w/h:100%


MILESTONE 10
Data:
- create integer values for each card, like fields
- these numbers cannot be null
- fields can reference data in the cards with [#data-name]


MILESTONE 11
Symbols:
- create a symbol group and several icons for use in the fields
- symbols can be referenced in fields with [@symbol-name]
- card-data can be null, and if a card-data is null, it it replaced by a symbol
- along with symbols, projects have enumerations which are like select box items
- enumerations can be added like tags to cards


MILESTONE 12
Maff n' Graff
- every card has the curve computed from:
   data (nominator or denominator) * their scale
   rule benefit or detriment * situational
- the jedi value is visible in the data table
- it is also graphable
- with the data and rules, we can compute a graph
- to show all the cards in the project
- we can go from one cardtype to the graph show the jedi curve
