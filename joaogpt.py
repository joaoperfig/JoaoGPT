# Import the required modules
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from IPython import embed
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

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

def get_gpt(driver, chatgpt):
    driver.switch_to.window(chatgpt)
    conversation = driver.find_element(By.XPATH, '//*[@id="__next"]/div[1]/div[1]/main/div[1]/div/div/div')
    elements = conversation.find_elements(By.XPATH, "*")
    reply = elements[-2].text
    return reply

def send_messenger(message, driver, messenger):
    driver.switch_to.window(messenger)
    input_box = driver.find_element(By.XPATH, "//div[@class='xzsf02u x1a2a7pz x1n2onr6 x14wi4xw x1iyjqo2 x1gh3ibb xisnujt xeuugli x1odjw0f notranslate']")
    input_box.send_keys(message)
    input_box.send_keys(Keys.RETURN)
    return

def get_messenger(driver, messenger):
    driver.switch_to.window(messenger)
    conversation = driver.find_element(By.XPATH, "//div[@aria-label='Mensagens na conversa com o nome Danilo PIPO']")
    #conversation = driver.find_element(By.XPATH, "//div[@aria-label='Mensagens na conversa com o nome Server Minecraft']")
    #conversation = driver.find_element(By.XPATH, "//div[@aria-label='Mensagens na conversa com João e Pedro']")
    #conversations = driver.find_elements(By.XPATH, "//div[@class='x1h91t0o xkh2ocl x78zum5 xdt5ytf x13a6bvl x193iq5w x1c4vz4f xcrg951']")
    #conversation = conversations[-1]
    elements = conversation.find_elements(By.XPATH, "*")
    messages = []
    #embed()
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

def make_message_input(messages):
    string = ""
    for message in messages:
        name = message[0]
        content = message[1]
        if content == "Enter":
            s = "[IMAGE FROM "+name+"]"
        else:
            s = "[MESSAGE FROM "+name+"]: "+content
        string += s + "\n"
    return string



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
        else:
            chatgpt = tab


    print("Giving chatgpt identity...")

    with open("identity.txt", "r") as f:
        identity = f.read()

    send_gpt(identity, driver, chatgpt)
    time.sleep(10)

    print("Entering cycle")

    chatlog = []

    while True:
        print("Checking messenger.")
        messages = get_messenger(driver, messenger)
        new_messages, chatlog = get_new_messages(chatlog, messages)
        if len(new_messages) > 0:
            print("Found new messages.")
            input = make_message_input(new_messages[-10:])
            print(input)
            time.sleep(0.5)
            print("Sending to GPT")
            send_gpt(input, driver, chatgpt)
            time.sleep(15)
            response = get_gpt(driver, chatgpt)
            print("Got response:")
            print(response)
            if "REPLY" in response:
                print("Sending to messenger")
                send_messenger(response[9:], driver, messenger)


        time.sleep(10)





    #send_messenger("message", driver, messenger)
    get_messenger(driver, messenger)

    #embed()
