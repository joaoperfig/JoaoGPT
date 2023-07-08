# Import the required modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from IPython import embed
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import random
import openai

with open("secrets.txt", "r") as f:
    key = f.read().strip()
openai.api_key = key

def send_safe_keys(target, text):
    lines = text.split("\n")
    for line in lines:
        target.send_keys(line)
        target.send_keys(Keys.SHIFT + Keys.ENTER)

def send_gpt(message, driver, chatgpt):
    driver.switch_to.window(chatgpt)
    time.sleep(0.5)
    input_box = driver.find_element(By.CSS_SELECTOR, "textarea")
    #input_box.send_keys(message)
    send_safe_keys(input_box, message)
    time.sleep(0.5)
    submit_button = driver.find_element(By.CSS_SELECTOR, "button.absolute")
    submit_button.click()
    time.sleep(0.5)
    return

def send_gpt(gpt_chatlog):
    print("Sending log to gpt")
    completion = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=gpt_chatlog
    )
    print("Got gpt response.")
    summary = completion["choices"][0]["message"]["content"]
    return summary

def send_messenger(message, driver, messenger):
    driver.switch_to.window(messenger)
    input_box = driver.find_element(By.XPATH, "//div[@class='xzsf02u x1a2a7pz x1n2onr6 x14wi4xw x1iyjqo2 x1gh3ibb xisnujt xeuugli x1odjw0f notranslate']")
    input_box.send_keys(message)
    input_box.send_keys(Keys.RETURN)
    return

def send_gif(descriprion, driver, messenger):
    driver.switch_to.window(messenger)
    gif_button = driver.find_element(By.XPATH, "//div[@aria-label='Escolher um GIF']")
    gif_button.click()
    time.sleep(0.5)
    input_box = driver.switch_to.active_element
    input_box.send_keys(descriprion)
    time.sleep(4)
    scroll_box = driver.find_element(By.XPATH, "//div[@class='xb57i2i x1q594ok x5lxg6s x78zum5 xdt5ytf x6ikm8r x1ja2u2z x1pq812k x1rohswg xfk6m8 x1yqm8si xjx87ck xx8ngbg xwo3gff x1n2onr6 x1oyok0e x1odjw0f x1e4zzel x2b8uid xh8yej3']")
    gifs = scroll_box.find_elements(By.XPATH, "*")
    gifs[0].click()
    time.sleep(0.5)
    return

def get_messenger(driver, messenger):
    driver.switch_to.window(messenger)
    #conversation = driver.find_element(By.XPATH, "//div[@aria-label='Mensagens na conversa com o nome TestGPT']")
    #conversation = driver.find_element(By.XPATH, "//div[@aria-label='Mensagens na conversa com o nome E sobre Bob, Marley']")
    #conversation = driver.find_element(By.XPATH, "//div[@aria-label='Mensagens na conversa com o nome Server Minecraft']")
    #conversation = driver.find_element(By.XPATH, "//div[@aria-label='Mensagens na conversa com João e Pedro']")
    conversations = driver.find_elements(By.XPATH, "//div[@class='x1n2onr6']")
    #conversation = conversations[-1]
    elements = conversations[1].find_elements(By.XPATH, "*")
    messages = []
    for element in elements:
        parsed = parse_element(element)
        if parsed != None:
            messages += [parsed]
    return messages

def parse_element(element):
    try:
        text = element.text
    except:
        return None
    if not ("Enter" in text):
        return None
    lines = text.split("\n")
    name = lines[0]
    content = lines[1]
    if len(content) <= 1:
        return None
    if name == "Enviaste":
        return None
    if "Mensagem original" in content:
        content = lines[3]
    return (name, content)

def get_new_messages(chatlog, messages):
    new_messages = []
    for i, message in enumerate(messages):
        if not (message in chatlog):
            new_messages += [message]
            chatlog += [message]
    #chatlog = chatlog[-500:]
    return new_messages, chatlog

def make_message_input(message):
    name = message[0]
    content = message[1]
    if content == "Enter":
        return "[IMAGE FROM "+name+"]"
    else:
        return "[MESSAGE FROM "+name+"]: "+content


# Main Function
if __name__ == '__main__':

    print("Finding chrome window...")

    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    #Change chrome driver path accordingly
    chrome_driver = "C:/chromedriver/chromedriver.exe"
    driver = webdriver.Chrome(chrome_driver, chrome_options=chrome_options)

    print("Successfully linked to Chrome window.")

    #get first child window
    tabs = driver.window_handles

    for tab in tabs:
        #switch focus to child window
        driver.switch_to.window(tab)
        time.sleep(0.9)
        print("Tab title: " + driver.title)
        if "Messenger" in driver.title:
            messenger = tab


    print("Giving chatgpt identity...")

    with open("identity.txt", "r") as f:
        identity = f.read()

    gpt_chatlog = [{"role": "system", "content": identity}]
    #send_messenger("*som de boot do Windows XP", driver, messenger)

    print("Entering cycle")


    chatlog = []

    while True:
        print("Checking messenger.")
        messages = get_messenger(driver, messenger)
        new_messages, chatlog = get_new_messages(chatlog, messages)
        if len(new_messages) > 0:
            print("Found new messages.")
            for new_message in new_messages[-10:]:
                formatted = make_message_input(new_message)
                gpt_chatlog += [{"role": "user", "content": formatted}]
                print(formatted)
            response = send_gpt(gpt_chatlog)
            gpt_chatlog += [{"role": "assistant", "content": response}]
            print("Got response:")
            print(response)
            if "REPLY" in response:
                print("Sending to messenger")
                send_messenger(response[9:], driver, messenger)
            elif "IMAGE" in response:
                print("Sending image")
                send_gif(response[10:].split("]")[0], driver, messenger)
            elif "GIF" in response:
                print("Sending gif")
                send_gif(response[8:].split("]")[0], driver, messenger)


        time.sleep(5)
