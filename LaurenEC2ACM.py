import pandas
import datetime
#Adatped from old copy found on git.
xmlString = ""
authors = ""
menuinput = ""
def welcomeMenu() :
    print("***********************************************")
    print("Welcome To Aithaea's EasyChair to ACM Converter\n***********************************************\n\nTo use this convertor you will need the following:\n*The CSV file containing ONLY accepted submissions\n*The CSV file containing author information\n*Your proceedings number from ACM\n*The date that you held your committee meeting to accept/reject papers")
    print("\nPlease ensure the two CSV files are stored in the same directory you are running this code from, and name them as follows:")
    print("*The author info csv file should be named authors.csv\nThe accepted paper csv file should be named accepted.csv")
    print("\nFailure to do this will result in the program being unable to run.")
    print("\n\nTime to begin!")

def endingOptions () :
    print("*******************************************************")
    print("Thank you for using Aithaea's Easychair to ACM Coverter")
    print("*******************************************************")
    menuinput = input("Would you like to (a) output your XML to console, or (b) save it to an XML file?")
    canprogress = False

    if menuinput.upper() == "A" or menuinput.upper() == "(A)":
        print(xmlString)
        canprogress = True
    elif menuinput.upper() == "B" or menuinput.upper() == "(B)":
        file = open("paperLoadDraft.xml", "w")
        n = file.write(xmlString)
        file.close()
        canprogress = True
    else:
        canprogress = False
    while canprogress == False:
        menuinput = input("Please enter (a) or (b)")
        if menuinput.upper() == "A" or menuinput.upper() == "(A)":
            print(xmlString)
            canprogress = True
        elif menuinput.upper() == "B" or menuinput.upper() == "(B)":
            file = open("paperLoadDraft.xml", "w")
            n = file.write(xmlString)
            file.close()
            canprogress = True
        else:
            canprogress = False

def splitAuthors(authorString):
    global authors
    subauthors = authorString.replace(' and ', ', ')
    subauthors = subauthors.split(', ')
    return subauthors


def generateAuthorData(name, authors, number, subnumber):
    global xmlString
    #splitName = name.split(" ")

    for row in authors.iterrows():
        fname = row[1][1]
        sname = row[1][2]
        #print("subnumber =" + str(subnumber) + " " + str(row[1][0]) )
        if name.startswith(fname) and name.endswith(sname) and subnumber == row[1][0]:
            xmlString += "\n\t\t\t<author>\n\t\t\t\t<prefix/>\n\t\t\t\t<first_name>" + row[1][1] + "</first_name>"
            xmlString += "\n\t\t\t\t<middle_name/>"
            xmlString += "\n\t\t\t\t<last_name>" + row[1][2] + "</last_name>"
            xmlString += "\n\t\t\t\t<suffix />\n\t\t\t\t<affiliations>"
            #getting affiliations
            if ";" in row[1][5] :
                splitInstitutions = row[1][5].split(";")
                affiliationCount = 0
                amount = len(splitInstitutions)
                while affiliationCount < amount:

                    xmlString += "\n\t\t\t\t\t<affiliation>"
                    xmlString += "\n\t\t\t\t\t\t<department/>"
                    xmlString += "\n\t\t\t\t\t\t<institution>"+splitInstitutions[affiliationCount].strip()+"</institution>"
                    xmlString += "\n\t\t\t\t\t\t<city/>"
                    xmlString += "\n\t\t\t\t\t\t<state_province/>"
                    xmlString += "\n\t\t\t\t\t\t<country>"+row[1][4]+"</country>"
                    affiliationCount += 1
                    xmlString += "\n\t\t\t\t\t\t<sequence_no>" + str(affiliationCount) + "</sequence_no>"
                    xmlString += "\n\t\t\t\t\t</affiliation>"
            else:
                xmlString += "\n\t\t\t\t\t<affiliation>"
                xmlString += "\n\t\t\t\t\t\t<department/>"
                xmlString += "\n\t\t\t\t\t\t<institution>" + row[1][5] + "</institution>"
                xmlString += "\n\t\t\t\t\t\t<city/>"
                xmlString += "\n\t\t\t\t\t\t<state_province/>"
                xmlString += "\n\t\t\t\t\t\t<country>" + row[1][4] + "</country>"
                xmlString += "\n\t\t\t\t\t\t<sequence_no>1</sequence_no>"
                xmlString += "\n\t\t\t\t\t</affiliation>"



            xmlString += "\n\t\t\t\t</affiliations>"
            xmlString += "\n\t\t\t\t<email_address>" + row[1][3] + "</email_address>"
            xmlString += "\n\t\t\t\t<sequence_no>" + str(number) + "</sequence_no>"
            if row[1][8] == "yes":
                xmlString += "\n\t\t\t\t<contact_author>Y</contact_author>"
            else :
                xmlString += "\n\t\t\t\t<contact_author>N</contact_author>"
            xmlString += "\n\t\t\t\t<ACM_profile_id/>\n\t\t\t\t<ACM_client_no/>\n\t\t\t\t<ORCID/>\n\t\t\t</author>"



def improveDateTime(date):
    stringToSplit = date.split(" ")
    splitDate = stringToSplit[0].split("-")
    format_datetime = datetime.datetime(int(splitDate[0]), int(splitDate[1]), int(splitDate[2]))
    return format_datetime.strftime("%d-%b-%Y").upper()
welcomeMenu()
xmlString = "<?xml version=\"1.0\"?>\n<erights_record>\n\t<parent_data>\n"

proceedingNumber = input("What is your proceeding number? (e.g. 2018-1234.1234)")

xmlString += "\t\t<proceeding>"+proceedingNumber+"</proceeding>\n\t\t<volume/>\n\t\t<issue/>\n\t\t<issue_date/>\n\t\t<source>self-generated</source>\n\t</parent_data>"
accepted = pandas.read_csv('accepted.csv')
authors = pandas.read_csv('authors.csv')

acceptedDate = input("On what date were the acceptance decisions made? (DD-MMM-YYYY) e.g 10-JAN-2001: ")

accepted = accepted.applymap(lambda x: x.strip() if type(x)==str else x)
accepted['decision'] = accepted['decision'].apply(lambda x: x.replace('accept as ', '') if type(x)==str else x)
accepted['decision'] = accepted['decision'].apply(lambda x: x.replace('poster', 'abstract') if type(x)==str else x)
accepted = accepted[accepted['decision']!='reject']

accepted = accepted.sort_values('decision', ascending=False)
i = 0
for submission in accepted.iterrows():
    xmlString += "\n\t<paper>\n\t\t<paper_type>Full Paper</paper_type>\n\t\t<art_submission_date>" + improveDateTime(submission[1][5]) + "</art_submission_date>"
    xmlString += "\n\t\t<art_approval_date>" + acceptedDate + "</art_approval_date>"
    xmlString += "\n\t\t<paper_title>" + submission[1][3] +"</paper_title>"
    i += 1
    xmlString += "\n\t\t<event_tracking_number>Sub" + str(i) + "</event_tracking_number>"
    xmlString += "\n\t\t<published_article_number/>\n\t\t<start_page/>\n\t\t<end_page/>"
    authors2Split = submission[1][4]
    stringAuthors = splitAuthors(authors2Split)
    count = 0
    for author in stringAuthors:
        count += 1
        #print(author)
        generateAuthorData(author, authors, count, submission[1][0])
        #findAuthor(author)

    #subauthors = submission[1][4]
    #print(subauthors)
    xmlString += "\n\t\t<section>Full Papers</section>"
    xmlString += "\n\t\t<sequence_no>" + str(i) + "</sequence_no>"
    xmlString += "\n\t</paper>"
xmlString += "\n</erights_record>"
#print(xmlString)
endingOptions()
