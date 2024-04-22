import os
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pandas import Series, DataFrame
from itertools import islice
from bs4 import BeautifulSoup


def main():

    # Make code cleaner like Trevor's

    # Can change the directories and presidents to what user wants
    path_for_PROCESSED = "/Data/ScrapedData"
    path_for_weblinks = "/Data/Weblinks.txt"
    # presidents = ["Biden", "Trump", "Obama", "W Bush", "Clinton", "Bush", "Reagan", "Carter", "Ford", "Nixon", "Johnson", "Kennedy", "Eisenhower", "Truman"]
    presidents = ["Biden", "Trump", "Obama", "W Bush", "Clinton", "Bush"]


    # Creates a WebLinkReader object to store the location of the Weblinks file
    web_link = WebLinkReader(path_for_weblinks)

    # Gets an array of the weblinks that are in the Weblinks text file
    # https: // www.presidency.ucsb.edu / statistics / data / ronald - reagan - public - approval, https: // www.presidency.ucsb.edu / statistics / data / jimmy - carter - public - approval, https: // www.presidency.ucsb.edu / statistics / data / gerald - r - ford - public - approval, https: // www.presidency.ucsb.edu / statistics / data / richard - m - nixon - public - approval, https: // www.presidency.ucsb.edu / statistics / data / lyndon - b - johnson - public - approval, https: // www.presidency.ucsb.edu / statistics / data / john - f - kennedy - public - approval, https: // www.presidency.ucsb.edu / statistics / data / dwight - d - eisenhower - public - approval, https: // www.presidency.ucsb.edu / statistics / data / harry - s - truman - public - approval, https: // www.presidency.ucsb.edu / statistics / data / franklin - d - roosevelt - public - approval
    webArray: list[str] = web_link.read_web_links()

    # Creates objects from the FileScraper and WriteData classes
    web_scraper_p = FileScraper()
    writer = WriteData()

    # Loops however many weblinks there are
    for i, link in enumerate(webArray):
         paragraphs: str = web_scraper_p.scrape_data(i, link)
         #  Calls the write_data method, sending in the FileScraper object and the
         # index to append to the end of the file name
         writer.write_data(paragraphs, i, path_for_PROCESSED, presidents[i])
    #
    file_names = str(os.path.dirname(__file__)) + path_for_PROCESSED + "_"
    #
    # #Remove white space at beginning of file
    RemoveEmptyLines(presidents, file_names)


    # data = {"Biden": [], "Trump": [], "Obama": [], "W Bush": [], "Clinton": [], "Bush": [], "Reagan": [], "Carter": [], "Ford": [], "Nixon": [], "Johnson": [], "Kennedy": [], "Eisenhower": [], "Truman": []}
    data = {"Biden": [], "Trump": [], "Obama": [], "W Bush": [], "Clinton": [], "Bush": []}


    # Loop through one file at a time, taking the data from it and storing it in an array
    for pres in presidents:
        with open(file_names + pres, 'r') as infile:

            for i in range(30):
                data[pres].append([])
                for j in range(5):
                    new_line = infile.readline()
                    data[pres][i].append(new_line[:-1])

        frame = pd.DataFrame(data[pres][1:], columns=[data[pres][0]])
        data[pres] = frame




    #################################################################################
    # Insert Cost to Pres Data based on the Date var
        # 1) Read the cost csv file and grab the end date and cost
        # 2) Format the dates to the same as the pres data
        # 3) Add the cost data to the pres data where the dates match

    fields = ['Name', 'Disastes', 'Begin Date', 'End Date', 'Total CPI-Adjusted Cost (Millions of Dollars)', 'Deaths']
    data_csv = pd.read_csv(str(os.getcwd()) + '/events-US-1980-2023.csv', sep=',', names=fields)
    data_csv = data_csv[2:]

    # Drop useless cols
    data_csv = data_csv.drop(columns=['Name', 'Disastes', 'Deaths', 'Begin Date'])

    # Makes the dates into dateTime in the data_csv dataframe
    for i, j in enumerate(data_csv['End Date']):
        data_csv['End Date'].iloc[i] = (str(data_csv['End Date'].iloc[i][:-4]) + '-' + str(data_csv['End Date'].iloc[i][-4:-2]))

    data_csv['End Date'] = pd.to_datetime(data_csv['End Date']).dt.to_period('M')
    # print(data_csv['End Date'])

    #################################################################################


    for pres in presidents:

        # Call the CombineData fucntion that formats the data and pres data then combines them on the shared field of date
        CombinedDate = CombineData(data, pres, data_csv)
        print(CombinedDate)

        p = CombinedDate['Total CPI-Adjusted Cost (Millions of Dollars)'].corr(CombinedDate['Approving'])
        print(f"{pres}: {p}")

        CombinedDate['Approving'] = CombinedDate['Approving'].astype(float)
        CombinedDate['Total CPI-Adjusted Cost (Millions of Dollars)'] = CombinedDate['Total CPI-Adjusted Cost (Millions of Dollars)'].astype(float)
        CombinedDate.plot(x='End Date', y=['Approving', 'Total CPI-Adjusted Cost (Millions of Dollars)'])
        CombinedDate.plot(x='End Date', y=['Approving'])


        # plt.matshow(CombinedDate['Total CPI-Adjusted Cost (Millions of Dollars)'].corr(CombinedDate['Approving']))
        # pd.scatter_matrix(CombinedDate)
        print("=========================================================================")

    plt.show()
    # Next Steps:
    #   1) Create Graphs with pres approval rating against cost
    #   2) Create the website using Flask










# Function for combining the cost and approval data
def CombineData(data, pres, data_csv):
    MonthArray = np.array(data[pres]["End Date"])
    ApprovalArray = np.array(data[pres]["Approving"])

    Stats = pd.DataFrame({'End Date': MonthArray.flatten(), 'Approving': ApprovalArray.flatten()})
    Stats['End Date'] = pd.to_datetime(Stats['End Date']).dt.to_period('M')

    # CombinedDate = pd.merge(Stats, data_csv, on="End Date", how='left')
    CombinedDate = pd.merge(Stats, data_csv, on="End Date")
    return CombinedDate



# Function for removing white space from the text files with Pres Data
def RemoveEmptyLines(presidents, file_names):
    for pres in presidents:
        result = ""
        with open(file_names + pres, 'r+') as the_file:
            for line in the_file:
                if not line.isspace():
                    result += line
            the_file.seek(0)
            the_file.write(result)

    for pres in presidents:
        result = ""
        with open(file_names + pres, 'r+') as the_file:
            for line in the_file:
                if not line.isspace():
                    result += line
            the_file.seek(0)
            the_file.write(result)

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

    # Reads the links in the text file from self.link, and returns them in a string
    def read_web_links(self):
        # Opens the file for reading to read the weblinks
        file = open(self.link, "r")
        # Creates an array that reads the file and splits the data where there are commas
        webArray: list[str] = (file.read()).split(",")
        # Removes the last index that has nothing in it
        webArray.pop()
        return webArray


# Class for refining the data that was obtained in the get_data
class FileScraper:
    # Method that reads the raw html in the rawArticle[i] file and uses BeautifulSoup to grab only the paragraphs of the webpage
    def scrape_data(self, i: int, link: str) -> str:
        # Get requests for the html in the webpage
        webpage = requests.get(link)
        # Utilizing beautiful soup, we create an html parser 
        soup = BeautifulSoup(webpage.text, "html.parser")
        # It goes into a div and accesses the information in the id where it equals "article-body" and stores that data in the paragraphs string
        paragraphs: str = soup.findAll('div', attrs={"class":"field-body"})
        # Returns a string will all the paragraph in
        return paragraphs
    
    
# Class for writing the refined data to a specified file
class WriteData:
    # Method that writes the refined data(gives as paragraphs variable) to the specified file
    def write_data(self, paragraphs: str, i: int, path_pro: str, president) -> None:
        # Finds the path for the specified file
        file_to_read_pro: str = str(os.path.dirname(__file__)) + path_pro + "_" + president
        # Opens the file to be written to
        file1 = open(file_to_read_pro, "w")
        # Loops through the paragraphs in the paragraphs variable and writes them to the file
        for paragraph in paragraphs:
            file1.write(str(paragraph.text))
        # Closes the file
        file1.close()




if __name__ == "__main__":
    main()



    # Biden2D = [[0][0]]

    # for i in data["Biden"]:
    #     j = 0
    #     Biden2D.append([])
    #     Biden2D[i][j] = data["Biden"]["End Date"][i]
    #     Biden2D[i][j+1] = data["Biden"]["Approving"][i]

    # print(Biden2D)

    # print(frame)
    # data['Biden'] = frame

    # df.col = pd.to_datetime(df.col).dt.to_period('m')

    # print(data['Biden'])
    # print()


    # print(data["Trump"])
    # print()
    # print(data["Obama"])
    # print()
    # print(data["Clinton"])
    # print()


    # fram.resample('M').sum()
    # print(fram)
    # print()
    # print(cost_frame)
    # test_dataframe = pd.DataFrame(data["Biden"], columns=["Date", "Approving"])
    # fram.corrwith(cost_frame, axis=0, drop=False, method='pearson', numeric_only=False)
    # x = pd.Series((data["Biden"]).iloc[:,1])

    # xx = pd.Series([66, 63, 63,    57, 60,  60, 58, 57.5, 57, 59, 60, 63, 61, 62, 56, 58, 59])
    # yy = pd.Series([0, 0, 9094.9, 1584, 0, 1924.4, 0, 0, 0, 0, 1235.1, 0, 1284.9, 0, 0, 0, 11878.5])

    # print(x)
    # print()
    # print(y)

    # print()
    # print(f"p: {p}")

    # data_csv = pd.read_csv(str(os.getcwd()) + '/WebsiteScraper/events-US-1980-2023.csv')
    # # print(data_csv)
    #
    # series1 = data_csv.iloc[1]
    # print(series1)

    # cost_frame.insert(1, "Cost", cost)
    # BidenStats['Date'].apply(lambda date: date))
    # BidenStats['Date'].to_datetime(df.col).dt.to_period('m')


    # time = ["December 2023", "November 2023", "October 2023", "September 2023", "August 2023", "July 2023", "June 2023", "May 2023", "April 2023", "March 2023", "February 2023", "January 2023", "November 2022", "October 2022", "September 2022", "August 2022", "July 2022", "June 2022", "May 2022", "April 2022", "March 2022", "February 2022", "January 2022", "December 2021", "November 2021", "October 2021"]
    # cost = [1276,                       0,              0,              16162,          12486,    7472.6,      13174.9,    11552.8,        15437,      13499.7,        1786.1,            0,           4285,           0,                   188880.4,       0,          2917.2,     5310.3,     8906.8,     4337.4,         1344.1,         1088.6,         0,                 188880,       0,                  0]
    #
    # fram = pd.DataFrame(time, columns=["Date"])
    # cost_frame = pd.DataFrame(time, columns=["Date"])
    #
    # # fram.rename(columns={"Start Date": "Date"}, inplace=True)
    # fram.insert(1, "Approving", data["Biden"]['Approving'])
    # cost_frame.insert(1, "Cost", cost)
    #
    #
    # x = pd.Series([40, 38, 41, 39, 37, 37, 41, 42, 40, 43, 39, 37, 40, 42, 41, 40, 40, 42, 44, 38, 41, 41, 41, 42, 41, 40])
    # y = pd.Series(cost)
    # p = x.corr(y)
    # print()
    # print(f"p: {p}")
    # print("Completed")


    # frame = pd.DataFrame(data["Biden"][1:], columns=[data["Biden"][0]])
    # BidenMonthArray = np.array(data["Biden"]["End Date"])
    # BidenApprovalArray = np.array(data["Biden"]["Approving"])
    # # print(BidenMonthArray)
    # # print(BidenApprovalArray)
    #
    #
    #
    #
    #
    #
    #
    #
    #
    # BidenStats = pd.DataFrame({'End Date': BidenMonthArray.flatten(), 'Approving': BidenApprovalArray.flatten()})
    # # pd.to_datetime(BidenStats['Date']).dt.to_period('m')
    #
    # BidenStats['End Date'] = pd.to_datetime(BidenStats['End Date']).dt.to_period('M')
    # print(BidenStats)