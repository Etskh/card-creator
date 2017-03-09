# card-creator


## Russian Demons
- make the portrait card type
- make the ability card type
- make the wealth card type


## Startrek Chthulhu
- make the profession card type
- make the alien card type
- make the character card type
- make the item card type


## Completed
### Milestone 1: Basic Type Editing
- ✓ can edit a card type
- ✓ fields can be selected
- ✓ fields can be dragged to move around
- ✓ can modify name
- ✓ can modify alignment
- ✓ add fields to the card type
- ✓ remove fields from the card type
### Milestone 2: Basic Card Editing
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
### Milestone 3: Field Patterns
- ✓ cards have a template field that is modifyable
- ✓ there is a callback `onkeyup()` that sets a Timeout which will save the field when it is up. If it's called again, it resets the timer
- ✓ if a card doesn't have a FieldData, use the template
- ✓ you can use `{title}` in the fields to print out the title
- ✓ you can use `{count}` in the fields to print out the count
- ✓ each card-type has a set of data that each card must possess
- ✓ each card has a dataset of the data that corresponds with the values and names of the card-type data. Possible implementation: text-field of an array of integers: `[1,2,3,4,5]`
- ✓ can add data type to card type
- ✓ can view data types
- ✓ can rename data type
- ✓ fields can reference data in the cards with `{#data-name}`


## MILESTONE 4
### Advanced Card Editing:
- ✓ remove style from model
- ✓ add italic boolean to field
- ✓ add bold boolean to field
- ✓ create side bar for cardtype editing
- ✓ change name of cardtype
- ✓ add font-family selectbox to field
    font-family: 'Arial', sans-serif;
    font-family: 'Open Sans Condensed', sans-serif;
    font-family: 'Amatic SC', cursive;
- ✓ add text-size number to field
- ✓ text-size changes font-size
- ✓ changing text-side saves in model
- ✓ changing fields in the text edit view popup
- ✓ on save, will save all card data
- ✓ create a new card creates a new row in the table
- ✓ show existing fields on popup
- ✓ save modified fields
- make text size two buttons: once that increments by 10% and one that decreases by 10%


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
  `{list}` show a list of all projects that user owns
- if user has no projects, {list} doesn't show up
- project list page has names of all projects to go to their page
- pressing enter with modal will attempt to save it


## MILESTONE 9
### Symbols, Tags, and Advanced Patterns
- can create symbols at the project level that have an image and a name
- can rename symbols
- can delete symbols
- create a symbol group which serves as a folder for symbols
- symbols can be referenced in fields with `{@symbol-name}`
- `{@symbol-name#height}` will put symbol `symbol-name` in the card `height` times
- along with symbols, projects have enumerations which are like select box items
- `{#height:One,Two}` will show `One` if `height` is == 1 and `Two` if it's 2
- can create tags with a name and value
- can create up to 10 tags per card type
- tags can be deleted
- tags can only be deleted if unused
- tags can be added at will to cards with toggleable buttons
- tags can be seen in the data table
- tags can be put as labels on the card with `{tags}`


## MILESTONE 7
### Art on Card
- allow file uploads as hashed jpgs
- as an extra piece of data for each card: have unique art
- this can be uploaded from the card data entry area
- there are checks for size to make sure it's not too big, or small
- `{art}` puts the image in the field with pos:abs, w/h:100%


## MILESTONE 5
### Code Health
- ✓ add secret_key env to heroku account
- ✓ add secret_key env to pycharm environment
- ✓ add travis build key to heroku account
- ✓ spruce up the page
- cleanup: add minifier and cocatenator to the pipeline
- port css to less
- cleanup: generalise the REST APIs in the views
- cleanup: move the URLs to the cards module
- improvement: write tests for model properties
- cleanup: close the tickets that are open
- improvement: use the PostgreSQL database
- improvement: check data that is being saved on server wtih regexes too
- if there's only one of them, use id not class
- ✓ use Open Sans Condensed for site
- ✓ use Oswald for the cards
- can remove data type
- cleanup: move Font model to its own app


## MILESTONE 8
### Users
- if not logged in, show log-in screen to log-in
- upon login, go to project list
- add button to bar at top for user page
- `[ Project Name            {gear} ][ {list} {+} {user} ]`
  where `{user}` will go to user settings
- user settings has a name field for the user



## MILESTONE 10
### Maff n' Graff
- if a field is overwritten, the user can assign a value
- every card has the curve computed from:
   data (nominator or denominator) * their scale
   field benefit or detriment * situational
- the jedi value is visible in the data table
- it is also graphable
- with the data and rules, we can compute a graph
- to show all the cards in the project
- we can go from one cardtype to the graph show the jedi curve
