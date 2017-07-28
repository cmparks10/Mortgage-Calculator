'''
Corey Parks
4/23/2016
Final Project

a GUI Mortage Calculator that uses web scraping to get most of it's information.
It also opens a web page based off the users input



The first thing we will do is import all of
the libraries that we will use!'''


from tkinter import *
from tkinter import ttk
import urllib.request
from bs4 import BeautifulSoup
import webbrowser
#Let's initialize!
class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        #After the program has been initialized, define the main functions:
        self.title("Corey's Mortgage Solutions")
        self.loanAmt()
        self.repayPeriod()
        self.Counties()
        self.Output()
        self.Searcher()

    def loanAmt(self):
        '''
        This function has a label and an Entry Box prompting the user
        for input of the amount of the loan
        '''
        Label (self, text = "Amount of Loan (nearest dollar)").grid(row=1, column = 0)
        self.txtLoan = Entry(self)
        self.txtLoan.grid(row = 1, column = 1)
        
    def repayPeriod(self):
        '''
        Next we set up the Radio Buttons that will correspond to the
        length of the fixed rate mortgage. Later, we will determine
        what information to scrape for depending on what button was selected.
        '''
        self.radVar = IntVar()
        Label (self, text = "Repayment Period").grid(row = 2, rowspan = 2)
        Label (self, text = "").grid(row = 3, rowspan = 2)
        self.rb15 = Radiobutton(self, text = "15 year", variable = self.radVar, value = 1)
        self.rb30 = Radiobutton(self, text = "30 year", variable = self.radVar, value = 2)
        self.rb15.grid(row = 2, column = 1)
        self.rb30.grid(row = 3, column = 1)
        self.ScrapedRate = StringVar()
        self.ScrapedRateLabel = Label(textvariable = self.ScrapedRate)
        self.ScrapedRateLabel.grid(row = 5, column = 1)
        self.SRLabel = Label(text = 'Current Fixed Rate: ')
        self.SRLabel.grid(row =5, column = 0)

    def Counties(self):
        '''Alright boys and girls! Let's start scrapin'!'''
        #First, put in the url that you want to scrape from
        url =  'http://www.stats.indiana.edu/dms4/propertytaxes.asp'
        #Let the program know that you want it to open it to get the information
        page = urllib.request.urlopen(url)
        #Creating a variable to use that is the Beautiful Soup function - this is what actually reads the web page!
        soup = BeautifulSoup(page.read(), "html.parser")

        #This is where the soup gets beautiful. Below, we tell where in the HTML we will be looking for the info we want. 
        counties = soup.find('select',{'name':'geo'})
        #Once that has been established, get rid of that messy HTML formatting - we want the meat of the web page!
        counties = (counties.get_text())
        #Create the combobox:
        Label(self, text = "County of Residence").grid(row = 6, column = 0)
        self.boxValue = StringVar()
        self.box = ttk.Combobox(self, textvariable = self.boxValue,
                                state='readonly')
        #Assign what will be in the box to the scraped information from above.
        self.box['values'] = (counties)
        #Start the combobox on the first(0th element - cause computers!) element from the scraped data
        self.box.current(0)
        self.box.grid(row = 6, column = 1)

        
        #Create a place to the counties average property tax to display once the program performs it calculations
        self.SCRLabel = Label(text ='Current Average Property Tax: ')
        self.SCRLabel.grid(row = 7, column = 0)
        self.ScrapedCountyRate = StringVar()
        self.ScrapedCountyRateLabel = Label (textvariable = self.ScrapedCountyRate)
        self.ScrapedCountyRateLabel.grid(row = 7, column = 1)

    def Output(self):
        '''
        Now we create a button to do most of the fun stuff!
        '''
        self.btnCalc = Button(self, text = "Calculate Loan")
        self.btnCalc.grid(row = 8, column = 1)
        #call the calculate function!
        self.btnCalc["command"] = self.calculate


    def calculate(self):
        '''
        Here is where the fun stuff happens!. There will be alot going on - so stay with me!
        '''
        #First, check to see if the user has even put any values in the Entry box for the loan
        if len(self.txtLoan.get()) <= 0:
            self.newWindow = Toplevel(self)
            #If they haven't, let them know with a new Window!
            Label(self.newWindow, text = "Please enter a loan amount to the nearest dollar").grid()
            self.newWindow.grid()
            
        
        #Now, we take a look at the selected Radio Button and do some web scraping:

        #If Button 1 is selected:    
        if self.radVar.get()== 1:
            #BeautifulSoup!!!!!!
            url =  'http://www.bankrate.com/indiana/mortgage-rates.aspx'
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page.read(), "html.parser")

            rate = soup.find_all("td",{'class':'exptbl-rates-data'})[3]
            Rate = (rate.get_text())
            #Here, we strip the % from the returned value from the web page. This ensures things don't get
            #Messy later when we do some math.
            percent = '%'
            for i in range(0, len(percent)):
                self.Rate = Rate.replace(percent[i],"")
                self.ScrapedRate.set(self.Rate)
        #If Button 2 is selected - you know the drill!    
        elif self.radVar.get()==2:
            url =  'http://www.bankrate.com/indiana/mortgage-rates.aspx'
            page = urllib.request.urlopen(url)
            soup = BeautifulSoup(page.read(), "html.parser")

            rate = soup.find_all("td",{'class':'exptbl-rates-data'})[0]
            Rate = (rate.get_text())
            percent = '%'
            for i in range(0, len(percent)):
                self.Rate = Rate.replace(percent[i],"")
                self.ScrapedRate.set(self.Rate)
                
        #If neither button is selected, let them know with a New Window!
        elif self.radVar.get() == 0:
            self.newWindow = Toplevel(self)
            Label(self.newWindow, text = "Please choose a Repayment Period").grid()
            self.newWindow.grid()
            
    
        #Time for more soup! This time let's get some average property tax values!!!!
        url = 'https://smartasset.com/taxes/indiana-property-tax-calculator'
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page.read(), "html.parser")
        
        self.PropTax = (self.boxValue.get())

        searchWord = re.compile(self.PropTax)
        
        #I had a heck of a time figuring out how to select a certain sibling in HTML, so I decided to do it
        #with brute force and go one by one until things made sense!
        cat = soup.find("td", text = searchWord).find_next_sibling("td")
        cat = cat.find_next_sibling("td")
        cat = cat.find_next_sibling("td").text
        percent = '%'
        for i in range (0, len(percent)):
            self.cat = cat.replace(percent[i],"")
        
        self.ScrapedCountyRate.set(self.cat)
        
        #Do the math!!!!
        #get the amount of the loan
        self.loan = int(self.txtLoan.get())
        #Get the Fixed Interest Rate
        self.IntRate = float(self.ScrapedRate.get())
        #Get the average property tax:
        self.PropRate = float(self.ScrapedCountyRate.get())
        
        Label(self, text = "Monthly Payments").grid(row = 10, column =0)
        self.MonthlyPayments = StringVar()
        self.MonthlyPaymentsLabel = Label(textvariable = self.MonthlyPayments)
        self.MonthlyPaymentsLabel.grid(row = 10, column = 1)
        #Calculate the plain monthly payments without interest
        self.output = int(self.radVar.get())
        '''
        Look at those radio buttons again! This time we decide what the montly payments will be
        based off the length of the loan. 15 years * 12 months in a year is 180 months, etc
        '''
        if self.radVar.get()== 1:
            self.plain = self.loan/180
            
        elif self.radVar.get()==2:
            self.plain = self.loan/360
        
        #Find what interest would be
        self.math = self.plain * self.IntRate
        self.IntRate = self.IntRate/100
        self.IntRate = (1+self.IntRate**(1/12)-1)



        '''
        This is where the math gets screwy. See the documentation.
        I just decided to hack at it until the numbers came out close, and then implement that into the program
        If anything the monthly payments will be slightly higher, so that will be a pleasant surprise for the
        homeowner when he/she gets thier first payment!
        '''
        self.IntRate = self.plain*self.IntRate
        self.IntRate = self.plain-self.IntRate
        self.PropRate = self.PropRate/100
        self.PropRate = (1+self.PropRate**(1/12)-1)#Formula to calculate fixed interest rate

        self.PropRate = self.plain*self.PropRate
        self.PropRate = self.plain-self.PropRate
        #self.PropRate = self.plain+self.PropRate

        self.math = (self.plain+self.IntRate+self.PropRate)
        #Round it off to two cents
        self.x = round(self.math, 2)
        
        self.MonthlyPayments.set(self.x)
        '''
        #Property taxes are paid twice per year. For simplicity's sake,
        we are going to include them into the monthly payments of the program
        '''
        
    def Searcher(self):
        #Now we search for your house! More Labels and Entry Boxes here
        Label (self, text = "Enter Zip Code").grid(row=12, column = 0)
        self.zip = Entry(self)
        self.zip.grid(row = 12, column = 1)
        
        #A button with a command just like before
        Label(self, text = "").grid(row = 11, column =1)
        self.btnSearch = Button(self, text = "Search for Homes")
        self.btnSearch.grid(row = 13, column = 1)
        self.btnSearch["command"] = self.Search
        
    def Search(self):
        #Get that value and search the Web!
        self.Zip = int(self.zip.get())
        webbrowser.open('http://www.zillow.com/homes/for_sale/{}_rb/?fromHomePage=true&shouldFireSellPageImplicitClaimGA=false&fromHomePageTab=buy'.format(self.Zip))
               
def main ():        
    app = App()

if __name__=='__main__':
    main()
