# Proposal

## What will (likely) be the title of your project?

Python Expense Tracker

## In just a sentence or two, summarize your project. (E.g., "A website that lets you buy and sell stocks.")

A dashboard that allows me to view my monthly expenses to give a better overview of how I spend my money. It will accept monthly reports from money transactions, including credit card reports, bank accounts, Venmo transactions, etc.

## In a paragraph or more, detail your project. What will your software do? What features will it have? How will it be executed?

I'm using the code from this article: https://towardsdatascience.com/manage-your-money-with-python-707579202203 as a jumping off point. Basically, the software will read a csv file that comes from my bank account, credit card, Venmo, and any other payment method I have to find read all of my transactions and income. It will then sort the expenses into categories (groceries, eating out, rent, utilities, etc) so that I can better understand where my money goes and what I can cut back on. Then it will output a monthly report that has charts that visually show how I spend my money using plotly. I would also like for it to track my cashback rewards on my credit card that change month to month. It will also track how much money I should move to my savings account each month, and in this way will also track my 'net worth'. It will take all of this information and create a user dashboard that runs locally on my laptop that lets me compare month to month spending. The dashboard will be created with jupyter_dash, dash_core_component, and dash_html_components.

## If planning to combine 1051's final project with another course's final project, with which other course? And which aspect(s) of your proposed project would relate to 1051, and which aspect(s) would relate to the other course?

N/A

## If planning to collaborate with 1 or 2 classmates for the final project, list their names, email addresses, and the names of their assigned TAs below.

N/A

## In the world of software, most everything takes longer to implement than you expect. And so it's not uncommon to accomplish less in a fixed amount of time than you hope.

### In a sentence (or list of features), define a GOOD outcome for your final project. I.e., what WILL you accomplish no matter what?

I will definitely be able to accomplish the reading of my csv files, categorization of the different expenses, and the ceation of the charts. 

### In a sentence (or list of features), define a BETTER outcome for your final project. I.e., what do you THINK you can accomplish before the final project's deadline?

I think I can also incorporate the cashback rewards and the tracking of my expenses month to month. 

### In a sentence (or list of features), define a BEST outcome for your final project. I.e., what do you HOPE to accomplish before the final project's deadline?

I would like to set up a way to automate the retrieval of the csv file from my various accounts so that all I have to do each month is run the code.

## In a paragraph or more, outline your next steps. What new skills will you need to acquire? What topics will you need to research? If working with one of two classmates, who will do what?

My next steps are going to be figuring out how to get the csv files from my different accounts or finding an existing app that will allow me to import all of my various accounts into one place that will export one csv file. I will also need to research pandas and numpy data analysis tools to better understand their capabilities and how to use them effectively. I will also look more into jupyter_dash to determine how I can make a more aestetically pleasing dashboard than the one that the article creates. 
