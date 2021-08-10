"""
Created by James Lawson and Beth Ann Townsend
Project name: project11
File name: library.py

This program holds the books contained in a library, where a user can input a
text file of commands for the program to read and process.
"""

#the class that holds the information about a book, later used in the larger library
class Book(object):

    #this will be increased and used later to calculate the total
    CHECKED_OUT_OVER_TIME = 0

    #the initialization of the Book class, setting up the required variables for each book
    def __init__(self, title, author, year, available = True, timesCheckedOut = 0):
        self.title = title
        self.author = author
        self.year = year
        self.available = True
        self.timesCheckedOut = timesCheckedOut

    #displays the book information
    def __str__(self):
        return self.title + " by " + self.author + ", " + self.year + "\n" + "Times checked out: " + str(self.timesCheckedOut) + "\n"

    #by setting equality, it will be easier to compare down the road, using ==
    def __eq__(self, other):
        if self is other: return True
        if type(other) != type(self):
            return False
        return self.title == other.title and self.author == other.author and self.year == other.year
    
    #method "checking out" a book from a library. It will be removed and the count for books checked out will increase by one
    def checkOut(self):
        if self.available == True:
            self.available = False
            self.timesCheckedOut += 1
            Book.CHECKED_OUT_OVER_TIME += 1
            return True
        else:
            return False

    #if a book has been checked out, this method will return it to the library, making it available again
    def checkIn(self):
        if self.available == False:
            self.available = True
            return True
        else:
            return False

#this library class takes information from the book class to generate the overarching class and the methods pertaining specifically to a library
class Library(Book):

    #initialization, setting books to an empty list and the total of checked out books to 0, as nothing has happened yet
    def __init__(self):
        self.books = []
        self.totalCheckedOut = 0

    #visual display that will return information about the library in text
    def __str__(self):
        string = "Total books held by library: " + str(len(self.books)) + "\n" + " Total books currently checked out: " + str(self.totalCheckedOut) + "\n"
        
        for x in self.books:
            if x.available == True:
                string += (" Available books: " + str(x) + "\n")
            if x.available == False:
                string += (" Checked out books: " + str(x) + "\n")
        return string

    #again, setting equality    
    def __eq__(self, other):
        if self is other: return True
        if type(other) != Library: return False
        if len(Library) != len(other):
            return False
        else:
            sort(Library)
            sort(other)
            if Library == other:
                return True

    #allows user to add a new book to the library with the append feature, dictated by the title, author, and year used everywhere else for a book
    def addBook(self, title, author, year):
        book = Book(title, author, year)
        self.books.append(book)

    #locates a book by matching the input from the user to a book in the library and returning that
    def findBook(self, title, author, year):
        for book in self.books:
            if title == book.title and author == book.author and year == book.year:
                return book
            else:
                return None 

    #the opposite of add; allows user to delete a book
    def removeBook(self, title, author, year):
        for book in self.books:
            if title == book.title and author == book.author and year == book.year:
                self.books.remove(book)
                break

    #lets user "check out" a book, essentially noting that the book is not currently accessible by the user in the library but still storing it for later when it will be returned (hopefully. Otherwise they'll get fined and the librarians will be mad)
    def checkOut(self, title, author, year):
        for book in self.books:
            if title == book.title and author == book.author and year == book.year and book.available:
                book.checkOut()
                self.totalCheckedOut += 1
            else:
                print("Book is already out", "\n")

    #opposite of "check out"; returns the book to be available once more for check out
    def checkIn(self, title, author, year):
        for book in self.books:
            if title == book.title and author == book.author and year == book.year and not book.available:
                book.checkIn()
            else:
                print("Book is already in", "\n")

    #uses Python's sort to arrange the books accordingly
    def sort(self, sortKey=lambda n: n.title):
        return self.books.sort(key = sortKey)

    #arranged by author
    def sortByAuthor(self):
        return self.sort(lambda n: n.author)

    #by year
    def sortByYear(self):
        return self.sort(lambda n: n.year)

    #by title
    def sortByTitle(self):
        return self.sort()

#the main function that controls everything and interprets the commands from the user's text file
def main():
    filename = input("Please enter the name of the file: ")
    #opens the file that the user inputs
    f = open(filename, "r")
    #interprets the contents
    line = f.read()
    #splits the words apart for a list
    command = line.split("\n")
    command = list(filter(lambda x: x != "", command))
    #sets libraries variable to an empty dictionary
    libraries = {}
    #initializes x at 0
    x = 0
    
    while x < len(command):
        text = command[x].split(" ")

        #accounts for the key word "create" in the text file
        if text[0] == "create":
            #allows user to make their own library, found at index 1
            libraries[text[1]] = Library()
            x += 1

        #this counts the total of books checked out, using the original from Book
        elif text[0] == "total":
            print("Total:"  + str(Book.CHECKED_OUT_OVER_TIME), "\n")
            x += 1

        #all of these use methods already worked out above
        if len(text) > 1:
            #sees key word "add" and reads the next three lines to take in the title, author, and year, gathering the info needed for a book to be added to the library
            if text[1] == "add":
                title = command[x+1]
                author = command[x+2]
                year = command[x+3]
                x += 4
                libraries[text[0]].addBook(title, author, year)

            #takes in "display" and prints the __str__
            elif text[1] == "display":
                print(str(libraries[text[0]]), "\n")
                x += 1

            #responds to "remove" and reads the next three lines to know what book to remove
            elif text[1] == "remove":
                title = command[x+1]
                author = command[x+2]
                year = command[x+3]
                x += 4
                libraries[text[0]].removeBook(title, author, year)

            #reads "checkout" and looks to the next three lines for what book to check out   
            elif text[1] == "checkout":
                title = command[x+1]
                author = command[x+2]
                year = command[x+3]
                x += 4
                libraries[text[0]].checkOut(title, author, year)

            #opposite of "checkout"; checks in the book from the title, author, year given
            elif text[1] == "checkin":
                title = command[x+1]
                author = command[x+2]
                year = command[x+3]
                x += 4
                libraries[text[0]].checkIn(title, author, year)

            #this will sort, depending on what command the user employs
            elif text[1] == "sort":
                #sorts by title
                if text[2] == "title":
                    title = command[x+1]
                    libraries[text[0]].sortByTitle()
                #by author
                elif text[2] == "author":
                    author = command[x+2]
                    libraries[text[0]].sortByAuthor()
                #by year
                elif text[2] == "year":
                    year = command[x+3]
                    libraries[text[0]].sortByYear()
                x += 1
   
if __name__ == "__main__":
    main()
