import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def initialize_driver():
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver

def start_game(driver):
    driver.get("https://arithmetic.zetamac.com/")
    start_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//input[@value='Start']"))
    )
    start_button.click()

def solve_equation(equation):
    parts = equation.split()
    
    if len(parts) != 3:
        raise ValueError("Equation must consist of two numbers and an operator.")
    
    number1, operator, number2 = parts
    
    try:
        number1 = int(number1)
        number2 = int(number2)
    except ValueError:
        raise ValueError("The first and third parts of the equation must be numbers.")
    
    if operator == '+':
        return number1 + number2
    elif operator == '–':
        return number1 - number2
    elif operator == '×':
        return number1 * number2
    elif operator == '÷':
        if number2 == 0:
            raise ValueError("Division by zero is not allowed.")
        return number1 / number2

def submit_answer(driver, answer):
    answer_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "answer"))
    )
    answer_input.clear()
    answer_input.send_keys(str(answer))

def play_game(driver):
    time_v = float('inf')
    while time_v > 0:
        time_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "left"))
        )
        time_v = int(time_element.text.split(': ')[1].strip())
        print(time_element.text)

        problem_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "problem"))
        )
        print(problem_element.text)
        answer = solve_equation(problem_element.text)
        print(answer)

        submit_answer(driver, answer)

def main():
    driver = initialize_driver()
    try:
        start_game(driver)
        play_game(driver)
    finally:
        time.sleep(120)
        driver.quit()

if __name__ == "__main__":
    main()
