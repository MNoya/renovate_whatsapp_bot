import csv
import os
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By


class Bot:
    link = "http://peluqueriaamiga.uy/instructivo"
    breakline = Keys.SHIFT + Keys.ENTER + Keys.SHIFT  # Keys.ENTER to give a new line effect in your Message
    MESSAGE = f"L’Oréal te presenta PeluqueriaAmiga, ¡tu oportunidad para estar en la web!{breakline}{breakline}" \
              f"Los consumidores podrán encontrar tu salón, y las promociones que quieras ofrecer.{breakline}{breakline}" \
              f"Registrarte es súper fácil y no tiene costo para el salón🔥.{breakline}{breakline}" \
              f"Sumate ahora en www.peluqueriaamiga.uy o descárgate el instructivo aquí: {breakline}{breakline}{link}"

    def __init__(self):
        self.contacts = self.read_contacts("contacts.csv")
        self.driver = webdriver.Chrome(self.get_chromedriver_path())
        self.wait = WebDriverWait(self.driver, 5)
        self.wait_longer = WebDriverWait(self.driver, 10)

    def run(self):
        self.driver.get("https://web.whatsapp.com/")
        input("Scan the QR code and then press Enter")

        for contact in self.contacts:
            self.send_message(contact)

        self.driver.quit()

    @staticmethod
    def read_contacts(filename):
        print(f"Reading {filename}")
        contacts = []
        with open(filename, mode='r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                print(f'\t{row["name"]}: {row["phone"]}')
                contacts.append(row)
        print(f'Processed {len(contacts)} contacts.')
        return contacts

    @staticmethod
    def get_chromedriver_path():
        return os.path.dirname(os.path.realpath(__file__)) + '/chromedriver'

    def send_message(self, contact):
        try:
            contact_box = self.get_contact_box(contact['name'])
            contact_box.click()
            self.write_message()
            print(f"Successfully sent message to {contact['name']}")
            time.sleep(0.5)

        except Exception as e:
            # If target Not found Add it to the failed List
            print(f"Problem sending message to {contact}: {e}")

    def write_message(self):
        message_input_xpath = "(//div[@contenteditable='true'])[2]"
        input_box = self.wait.until(EC.presence_of_element_located((By.XPATH, message_input_xpath)))
        input_box.clear()
        input_box.send_keys(self.MESSAGE)
        input_box.send_keys(Keys.ENTER)

    def get_contact_box(self, contact_name):
        x_arg = f"//span[contains(@title,'{contact_name}')]"

        spans = self.driver.find_elements_by_xpath(x_arg)
        for span in spans:
            if span.text == contact_name:
                return span
        else:
            self.search_contact_by_string(contact_name)
            spans = self.driver.find_elements_by_xpath(x_arg)
            for span in spans:
                if span.text == contact_name:
                    return span
            else:
                raise ValueError(f"Cant get contact box for {contact_name}")

    def click_on_element(self, x_arg):
        self.driver.find_element_by_xpath(x_arg).click()

    def search_contact_by_string(self, str):
        print(f"Searching {str}")
        inp_xpath = "//div[@contenteditable='true']"
        input_box = self.wait.until(EC.presence_of_element_located((By.XPATH, inp_xpath)))
        input_box.clear()
        input_box.send_keys(str)
        time.sleep(1)


if __name__ == "__main__":
    Bot().run()
