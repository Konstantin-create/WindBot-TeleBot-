# Time imports
import time
from datetime import datetime

# Tables import
from prettytable import PrettyTable
# Selenium imports
from selenium import webdriver
from selenium.webdriver.common.by import By


# Functions
def deg_to_direction(num):
    val = int((num / 22.5) + .5)
    arr = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]
    return arr[(val % 16)]


def get_windy_forecast(x, y, donate):
    # Variables
    x = str(x).strip()
    y = str(y).strip()
    windDeg = []
    output = []
    table = PrettyTable()

    # Initialisation of driver
    driver = webdriver.Chrome()
    print(f"https://www.windy.com/{x}/{y}?{x},{y},11,m:eTYahdm")
    driver.get(f"https://www.windy.com/{x}/{y}?{x},{y},11,m:eTYahdm")
    time.sleep(2)

    # Parse data
    data = driver.find_element(by=By.XPATH, value='//*[@id="detail-data-table"]/tbody/tr[2]').text.split()
    windMiddle = driver.find_element(by=By.XPATH, value='//*[@id="detail-data-table"]/tbody/tr[6]').text.split()
    windMax = driver.find_element(by=By.XPATH, value='//*[@id="detail-data-table"]/tbody/tr[7]').text.split()
    windDegData = driver.find_element(by=By.XPATH, value='//*[@id="detail-data-table"]/tbody/tr[8]').get_attribute(
        'innerHTML').split("<td")
    windDegData.pop(0)
    driver.close()

    # Get wind angel
    for i in range(len(windDegData)):
        windDeg.append(
            windDegData[i][
            windDegData[i].find("transform: "):windDegData[i].find(";", windDegData[i].find("transform: "))])
    date_time = int(str(datetime.date(datetime.now())).split("-")[2])

    # Make output
    for i in range(len(windMax)):
        if int(data[i]) == 0 and i != 0:
            date_time += 1
            if date_time - int(str(datetime.date(datetime.now())).split("-")[2]) >= donate:
                break

        output.append(
            [str(date_time), data[i], windMiddle[i], windMax[i],
             deg_to_direction(int(int(windDeg[i][windDeg[i].find("(") + 1:windDeg[i].find("deg")])))])

    # Create table
    table.field_names = ["Day", "Time", "Middle Wind(kt)", "Max Wind(kt)", "Wind Direction"]
    for i in range(len(output)):
        table.add_row(output[i])
    return table
