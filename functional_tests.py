from selenium import webdriver

browser = webdriver.Firefox()

# The user has heard about a new online todo list and goes to check out its homepage
browser.get('http://localhost:8000')

# The user notices the page title and header mention todo list
assert 'Todo' in browser.title

# The user is invited to enter a todo item straight away

# The user types "Fill up the dish machine" into a text box

# When the user hits enter, the page updates, and now the page lists "1 - Fill up the dish machine" as an item in a todo list

# There is still a text box inviting the user to add another item. The user enters "Cook dinner"

# The page updates again and shows both items on the list

# The user wonders whether the site will remember her list. Then the user sees that the site has generated a unique URL -- there is some explanatory text to that effect

# The user visits that URL - the todo list is still there

browser.quit()
