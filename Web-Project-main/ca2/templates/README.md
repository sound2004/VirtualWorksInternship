The improvements made to the html pages include the following below:

- Adding CSRF protection for each page ```( <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">)```
- Each User's home page personalized to reflect the full name of the user ```(<h1 align="center">Your Notes!</h1> | <h1 class="mb-4">Welcome, {{ user.first_name | escape }} {{ user.surname | escape }}!</h1>)```
- Adding the csrf token to the javascript in the deletion of the already added notes.      ```('Content-Type': 'application/json' 'X-CSRF-Token': '{{ csrf_token() }}')```
