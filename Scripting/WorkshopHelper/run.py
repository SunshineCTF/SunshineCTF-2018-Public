import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

DOMAIN = "http://localhost:"
PORT = "50001"

driver = webdriver.Chrome()
driver.get(DOMAIN + PORT)

# First start the game
start_button = driver.find_element_by_tag_name("button")
start_button.send_keys(" ")

# Loop until we get to the flag
while True:
    # Wait a second in order for the page to load fully
    time.sleep(1)
    # Find the question
    try:
        question = driver.find_element_by_id("question").text.split(" ")
    except Exception as e:
        # If we do not find a question, perhaps we are at the end,
        # so just exit then
        print(e)
        break
    feature_type, feature_name = question[8:11:2]
    print(feature_type, feature_name)

    # Then find the corresponding gear
    correct_gear = driver.find_element_by_xpath(
        "//div[@{}='{}']".format(feature_type, feature_name)
    )

    # Go down an extra level
    correct_gear = correct_gear.find_element_by_tag_name("div")

    # Get the gear's question and get the solution to it (as an int)
    gear_question = correct_gear.find_element_by_tag_name("h3").text
    gear_answer = str(int(eval(gear_question)))

    # Figure out if the gear is a multiple choice solution or text input
    sub_divs = correct_gear.find_elements_by_tag_name("div")
    if len(sub_divs) == 1:
        # If the gear is a text input, write in the solution
        text_input = correct_gear.find_element_by_tag_name("input")
        text_input.send_keys(gear_answer)
    else:
        # If the geaer is a multiple choice input, find and select the answer
        options = correct_gear.find_elements_by_tag_name("div")
        for option in options:
            if gear_answer == option.text:
                option.find_element_by_tag_name("input").click()
                break

    # Then submit the answer
    correct_gear.find_element_by_tag_name("button").send_keys(Keys.RETURN)

# driver.close()
