import os
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
from itertools import islice
from bs4 import BeautifulSoup
import os
# from flask import Flask, render_template, request
import pandas as pd

import datetime
from dateutil.relativedelta import *

def main():
    # Can change the directories and presidents to what user wants
    path_for_PROCESSED = "/Data/ScrapedData"
    path_for_weblinks = "/Data/Weblinks.txt"
    presidents = ["Biden", "Trump", "Obama", "W Bush", "Clinton", "Bush"]

    # Creates a WebLinkReader object to store the location of the Weblinks file
    # Gets an array of the weblinks that are in the Weblinks text file
    # Creates objects from the FileScraper and WriteData classes
    web_link = WebLinkReader(path_for_weblinks)
    webArray: list[str] = web_link.read_web_links()
    web_scraper_p = FileScraper()
    writer = WriteData()

    # Loops however many weblinks there are
    # Calls the write_data method, sending in the FileScraper object and the
    #   index to append to the end of the file name
    ###########################################################################################################
    for i, link in enumerate(webArray):
        paragraphs: str = web_scraper_p.scrape_data(i, link)
        writer.write_data(paragraphs, i, path_for_PROCESSED, presidents[i])
    ###########################################################################################################

    file_names = str(os.path.dirname(__file__)) + path_for_PROCESSED + "_"
    RemoveEmptyLines(presidents, file_names)
    data = {"Biden": [], "Trump": [], "Obama": [], "W Bush": [], "Clinton": [], "Bush": []}

    data_length_list = {"Biden": 38, "Trump": 142, "Obama": 445, "W Bush": 283, "Clinton": 216, "Bush": 113}
    #  data_length_list = {"Biden": 38, "Trump": 142, "Obama": 445, "W Bush": 283, "Clinton": 216, "Bush": 113}

    # Loop through one file at a time, taking the data from it and storing it in an array
    for pres in presidents:
        with open(file_names + pres, 'r') as infile:
            for i in range(data_length_list[pres]):
                data[pres].append([])
                for j in range(5):
                    new_line = infile.readline()
                    data[pres][i].append(new_line[:-1])

        frame = pd.DataFrame(data[pres][1:], columns=[data[pres][0]])
        data[pres] = frame

    fields = ['Name', 'Disastes', 'Begin Date', 'End Date', 'Total CPI-Adjusted Cost (Millions of Dollars)', 'Deaths']
    data_csv = pd.read_csv(str(os.getcwd()) + '/events-US-1980-2023.csv', sep=',', names=fields)
    data_csv = data_csv[2:]

    # Drop useless cols
    data_csv = data_csv.drop(columns=['Name', 'Disastes', 'Deaths', 'Begin Date'])
    # print(data_csv)

    # Makes the dates into dateTime in the data_csv dataframe
    for i, j in enumerate(data_csv['End Date']):
        data_csv['End Date'].iloc[i] = (
                    str(data_csv['End Date'].iloc[i][:-4]) + '-' + str(data_csv['End Date'].iloc[i][-4:-2]))
    # data_csv['End Date'] = pd.to_datetime(data_csv['End Date']).dt.to_period('M')
    data_csv['End Date'] = pd.to_datetime(data_csv['End Date'])

    # data_csv['End Date'] = pd.Timestamp(data_csv['End Date'])+pd.DateOffset(months=1)
    data_csv['End Date'] = data_csv['End Date'] + pd.DateOffset(months=0)
    data_csv['End Date'] = pd.to_datetime(data_csv['End Date']).dt.to_period('M')


    data_csv['Total CPI-Adjusted Cost (Millions of Dollars)'] = data_csv['Total CPI-Adjusted Cost (Millions of Dollars)'].astype(float)
    # data_csv = data_csv.groupby(['End Date']).sum()
    # print(data_csv)
    data_csv = data_csv.groupby(['End Date'], as_index=False)['Total CPI-Adjusted Cost (Millions of Dollars)'].sum()
    # data_csv['Total CPI-Adjusted Cost (Millions of Dollars)'] = data_csv['Total CPI-Adjusted Cost (Millions of Dollars)'].astype(str)
    # print(data_csv)

    for pres in presidents:
        # Call the CombineData fucntion that formats the data and pres data then combines them on the shared field of date
        # Find the correlation value between the president's approval rating and the cost of severe wather data
        # Plot the data
        CombinedDate = CombineData(data, pres, data_csv)

        # MCombinedData = CombinedDate.groupby(['End Date'])
        # print(MCombinedData)
# .agg("mean")

        p = CombinedDate['Total CPI-Adjusted Cost (Millions of Dollars)'].corr(CombinedDate['Approving'])
        print(f"{pres}: {p}")
        print(CombinedDate)
        plot_data(CombinedDate)

    # plt.show()

    #######################################################################################
    # Next Steps:
    #   1) Create Graphs with pres approval rating and another with cost
    #   2) Create the website using Flask
    #######################################################################################

def plot_data(CombinedDate):
    CombinedDate['Approving'] = CombinedDate['Approving'].astype(int)
    CombinedDate['Total CPI-Adjusted Cost (Millions of Dollars)'] = CombinedDate[
        'Total CPI-Adjusted Cost (Millions of Dollars)'].astype(float)
    CombinedDate.plot(x='End Date', y=['Total CPI-Adjusted Cost (Millions of Dollars)'])
    CombinedDate.plot(x='End Date', y=['Approving'])
    print("=========================================================================")

# Function for combining the cost and approval data
def CombineData(data, pres, data_csv):

    # data[pres] = data[pres].groupby(['End Date']).mean()
    # data[pres] = frame

    MonthArray = np.array(data[pres]["End Date"])
    ApprovalArray = np.array(data[pres]["Approving"])
    Stats = pd.DataFrame({'End Date': MonthArray.flatten(), 'Approving': ApprovalArray.flatten()})
    # Stats = Stats.groupby(['End Date']).mean()
    # Stats['End Date'] = pd.to_datetime(Stats['End Date'])
    # se_date = use_date+relativedelta(months=+1)

    #####################################################################################################
    # # Stats['End Date'] = pd.Timestamp(Stats['End Date'])+pd.DateOffset(months=1)
    # Stats['End Date'] = Stats['End Date'] + pd.DateOffset(months=1)
    Stats['End Date'] = pd.to_datetime(Stats['End Date']).dt.to_period('M')




    #####################################################################################################

    # print(Stats['End Date'])
    Stats['Approving'] = Stats['Approving'].astype(int)
    Stats = Stats.groupby(['End Date'], as_index=False)['Approving'].mean()

    CombinedDate = pd.merge(Stats, data_csv, on="End Date")
    return CombinedDate


# Function for removing white space from the text files with Pres Data
def RemoveEmptyLines(presidents, file_names):
    for i in range(3):
        for pres in presidents:
            result = ""
            with open(file_names + pres, 'r+') as the_file:
                for line in the_file:
                    if not line.isspace():
                        result += line
                the_file.seek(0)
                the_file.write(result)

# Class for getting the web links in a txt file and storing them in an array
class WebLinkReader:
    # Initializes a WebLinkReader object with a var link that stores the path to the Weblinks.txt file
    def __init__(self, paths: str) -> None:
        self.link = str(os.path.dirname(__file__)) + "/" + paths

    # Removes the last index that has nothing in it
    def read_web_links(self):
        file = open(self.link, "r")
        webArray: list[str] = (file.read()).split(",")
        webArray.pop()
        return webArray


# Class for refining the data that was obtained in the get_data
class FileScraper:
    # Method that reads the raw html in the rawArticle[i] file and uses BeautifulSoup to grab only the paragraphs of the webpage
    # It goes into a div and accesses the information in the id where it equals "article-body" and stores that data in the paragraphs string
    def scrape_data(self, i: int, link: str) -> str:
        webpage = requests.get(link)
        soup = BeautifulSoup(webpage.text, "html.parser")
        paragraphs: str = soup.findAll('div', attrs={"class": "field-body"})
        return paragraphs


class WriteData:
    # Method that writes the refined data(gives as paragraphs variable) to the specified file
    def write_data(self, paragraphs: str, i: int, path_pro: str, president) -> None:
        file_to_read_pro: str = str(os.path.dirname(__file__)) + path_pro + "_" + president
        file1 = open(file_to_read_pro, "w")
        for paragraph in paragraphs:
            file1.write(str(paragraph.text))
        file1.close()


if __name__ == "__main__":
    # app.run()
    main()
