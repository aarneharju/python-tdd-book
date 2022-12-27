from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException
import time

MAX_WAIT = 3


class NewVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):

        # The user has heard about a new online todo list and goes to check out its homepage
        self.browser.get(self.live_server_url)

        # The user notices the page title and header mention todo list
        self.assertIn('Todo', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('todo', header_text)
        # self.fail('Finish the test!')

        # The user is invited to enter a todo item straight away
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a todo item'
        )

        # The user types "Fill up the dish machine" into a text box
        inputbox.send_keys('Fill up the dish machine')

        # When the user hits enter, the page updates, and now the page lists "1: Fill up the dish machine" as an item in a todo list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Fill up the dish machine')

        # self.assertTrue(
        #     any(row.text == '1: Fill up the dish machine' for row in rows),
        #     f'New todo item did not appear in table. Contents were: \n{table.text}'
        # )

        # There is still a text box inviting the user to add another item. The user enters "Cook dinner"
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Cook dinner')
        inputbox.send_keys(Keys.ENTER)

        # The page updates again and shows both items on the list
        self.wait_for_row_in_list_table('2: Cook dinner')
        self.wait_for_row_in_list_table('1: Fill up the dish machine')


    # The user wonders whether the site will remember her list. Then the user sees that the site has generated a unique URL -- there is some explanatory text to that effect
    def test_multiple_users_can_start_lists_at_different_urls(self):

        # The user starts a new todo list
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy nuts')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy nuts')

        # The user notices that the list has a unique URL
        user1_list_url = self.browser.current_url
        self.assertRegex(user1_list_url,  '/lists/.+')

        # A new user comes along to the site

        # We use a new browser session to make sure that no information of user1 is coming through from cookies etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # User2 visits the home page. There is no sign of user1's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('dish', page_text)
        self.assertNotIn('dinner', page_text)

        # User2 starts a new list by entering new item. He is less interesting than user1
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # User2 gets his own unique URL
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user2_list_url, user1_list_url)

        # Again, there is no trace of user1's list
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('dish', page_text)
        self.assertIn('Buy milk', page_text)
