import pandas as pd
import csv
import sys

#main
file_path=""
df=""
output_data=[]      #whole data will be stored in JSON format or list of dictionaries


# Function to take the file path as an input
def take_input():
    global file_path
    print("Enter the Input file path(only .csv file):",end="")
    file_path=str(input())
    if(not file_path[-4:]=='.csv'):
        sys.exit(f"Given file is not a '.csv' file\n")




#Read the input .csv file 
def  read_csv(file_path):
    try:
        df=pd.read_csv(file_path)
        return df
    except:
        sys.exit(f" Error occured while reading the file '{file_path}'\n")


# exctracts the columns names from the dataframe
def get_test_columns(df):
    all_columns=df.columns
    test_columns=all_columns[3:]
    test_col=[]
    sub_test_col=[]

    #To get the sub columns like 'score,time,correct,wrong' etc..,
    for i in range(0,6):
        sub_test_col.append(test_columns[i].split('-')[1]) 

    #To get each test names like 'Concept test 1,concept test 2' etc..,
    for test in test_columns[::6]:
        test_col.append(test.split('-')[0])

    return test_col,sub_test_col

# Function to extract data from input file and to create output JSON data
def get_test_data(df,test_name,test_sub_name):
    for index,row in df.iterrows():
        global output_data
        row=list(row)
        total_test_cols=len(row[3:])
        total_test_sub_cols=len(test_sub_name)
        start=3
        end=start+total_test_sub_cols
        count=0
        while(start<total_test_cols):
            output_row_student={}
            output_row_student['Name']=row[0]
            output_row_student['Id']=row[1]
            output_row_student['Chapter Tag']=row[2]
            if(isinstance(row[start],int)==False and isinstance(row[start],float)==False and any(map(str.isdigit, row[start]))==False):
                pass
            else:
                output_row_student.update({'Test Name': test_name[count]})
                count_in=0
                for each_test in row[start:end]:
                    output_row_student.update({test_sub_name[count_in]:each_test})
                    count_in=count_in+1
                output_data.append(output_row_student)

            start=start+total_test_sub_cols
            end=end+total_test_sub_cols
            count=count+1
    return output_data   


# Function to create a output .csv file
def create_csv_file(df):
    data=pd.DataFrame(df)
    try:
        print('By what name I can save the output file?("without file extention"):',end="")
        out_file_name=str(input())+".csv"
        data=data.set_index('Name')
        data.to_csv(out_file_name)
        print("Output file created with the name '{}'".format(out_file_name))
    except:
        print("Error occured while creating .csv file")


# take file path as an input
take_input()

#read the data from the given .csv
df=read_csv(file_path)

#get all the test names and the corresponding details
test_name,test_sub_name=get_test_columns(df)


#extracting data from input file and to create JSON data
output_data=get_test_data(df,test_name,test_sub_name)

#create a output .csv file
create_csv_file(output_data)