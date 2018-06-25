from csv import reader


# makes a 2d list out of a csv file
def csv2table(file, **kwargs):

    # opeing csv file
    with open(file, newline='') as csvfile:

        # reading csv file
        opened_file = reader(csvfile, **kwargs)

        # something to store the data
        table = []
        
        # iterating over fors in csv
        for row in opened_file:
            
            # break up row by spaces            
            table.append(row)


        return table
