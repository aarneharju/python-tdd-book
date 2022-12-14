from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # The user has heard about a new online todo list and goes to check out its homepage
        self.browser.get('http://localhost:8000')

        # The user notices the page title and header mention todo list
        self.assertIn('Todo', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('todo', header_text)
        # self.fail('Finish the test!')

        # The user is invited to enter a todo item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute(
            'placeholder'), 'Enter a todo item')

        # The user types "Fill up the dish machine" into a text box
        inputbox.send_keys('Fill up the dish machine')

        # When the user hits enter, the page updates, and now the page lists "1: Fill up the dish machine" as an item in a todo list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertTrue(
            any(row.text == '1: Fill up the dish machine' for row in rows),
            'New todo item did not appear in table'
        )

        # There is still a text box inviting the user to add another item. The user enters "Cook dinner"
        # inputbox.send_keys('Cook dinner')
        self.fail('Finish the test!')

        # The page updates again and shows both items on the list

        # The user wonders whether the site will remember her list. Then the user sees that the site has generated a unique URL -- there is some explanatory text to that effect

        # The user visits that URL - the todo list is still there


if __name__ == '__main__':
    unittest.main()

# browser.quit()
