from os import chdir

def changeDate(textFile, time1, time2):
    chdir(r'C:\Users\samlb\Documents\REDDIT_TO_YOUTUBE_PYTHON_SELENIUM\uploadToYoutube')
    with open(textFile) as f:
        myDate = f.read().splitlines()
    myDate = list(map(int, myDate))
    returnValue = myDate
    
    #Calculate next date
    newDate = myDate

    #Is it a leap year
    year = myDate[0]
    leapYear = (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0))

    #Change month and year depending on the day of the month
    if myDate[3] == time2:

        myDate[2] = myDate[2]+1

        #January
        if myDate[1] == 1 and myDate[2] >= 31:
            newDate[1] = 2
            newDate[2] = 1
        
        #February
        if leapYear == True:
            if myDate[1] == 2 and myDate[2] >= 29:
                newDate[1] = 3
                newDate[2] = 1
        else:
            if myDate[1] == 2 and myDate[2] >= 28:
                newDate[1] = 3
                newDate[2] = 1

        #March
        if myDate[1] == 3 and myDate[2] >= 31:
            newDate[1] = 4
            newDate[2] = 1
        
        #April
        if myDate[1] == 4 and myDate[2] >= 30:
            newDate[1] = 5
            newDate[2] = 1
        
        #May
        if myDate[1] == 5 and myDate[2] >= 31:
            newDate[1] = 6
            newDate[2] = 1
        
        #June
        if myDate[1] == 6 and myDate[2] >= 30:
            newDate[1] = 7
            newDate[2] = 1

        #July
        if myDate[1] == 7 and myDate[2] >= 31:
            newDate[1] = 8
            newDate[2] = 1
        
        #August
        if myDate[1] == 8 and myDate[2] >= 31:
            newDate[1] = 9
            newDate[2] = 1
        
        #September
        if myDate[1] == 9 and myDate[2] >= 30:
            newDate[1] = 10
            newDate[2] = 1
        
        #October
        if myDate[1] == 10 and myDate[2] >= 31:
            newDate[1] = 11
            newDate[2] = 1
        
        #November
        if myDate[1] == 11 and myDate[2] >= 30:
            newDate[1] = 12
            newDate[2] = 1
        
        #December
        if myDate[1] == 12 and myDate[2] >= 31:
            newDate[0] = myDate[0]+1
            newDate[1] = 1
            newDate[2] = 1

    #Change time
    if myDate[3] == time1:
        newDate[3] = time2
    else:
        newDate[3] = time1

    myDate = (str(s) for s in myDate)

    with open(textFile, 'w') as f:
        for line in myDate:
            f.write(line)
            f.write('\n')

    return returnValue

changeDate('changeDate.txt', 10, 19)