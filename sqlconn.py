import pyodbc

server = 'comp491server.database.windows.net'
database = 'comp491project'
username = 'comp491user'
password = 'comp491servercomp491serveR'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()



def main():
    course_array = []
    ta_array = []
    ta_pref_array = []
    pref_array = []
    instructors= []
    with open("courses2.txt", "r") as ins:
        array = []
        count = 0
        for line in ins:
            if count > 0:
                x = line.split()
                course_array.append({'course': x[0], 'ta_need': x[1], 'instructor': x[2]})
                if x[2] not in instructors:
                    instructors.append(x[2])
            count = count + 1


    with open("talist2.txt", "r") as ins:
        array = []
        count = 0
        for line in ins:
            if count > 0:
                x = line.split()
                ta_array.append({'id': x[0], 'advisor': x[1]})
            count = count + 1


    with open("tapref2.txt", "r") as ins:
        array = []
        count = 0
        for line in ins:
            if count > 0:
                x = line.split()
                index = line.index("\t")
                prefs = line[index + 1: len(line)]
                ta_pref_array.append({'id': x[0], 'prefs': prefs})
            count = count + 1

    with open("pref2.txt", "r") as ins:
        array = []
        count = 0
        for line in ins:
            if count > 0:
                x = line.split()
                index = line.index("\t")
                code = line[0: index]
                index2 = line.index("\t", index+1)
                course = line[index+1: index2]
                prefs =line[index2+1 : len(line)].strip()
                pref_array.append({'id': code, 'course': course, 'prefs': prefs})
            count = count + 1


#COURSE TABLE:
    for c in course_array:

        values = (c['course'], 'COMP', c['ta_need'])
        print(values)
        cursor = cnxn.cursor()
        cursor.execute("insert into Course(CourseID, CourseDepartment, TeachingAssistantNeed) values (?, ?, ?)", values)
        cnxn.commit()


# INSTRUCTOR TABLE:
    for ins in instructors:

         values = (ins, 'COMP')
         cursor = cnxn.cursor()
         cursor.execute("insert into Instructor(InstructorID, InstructorDepartment) values (?, ?)", values)
         cnxn.commit()

#TEACHES TABLE:
    for c in course_array:

        values = (c['instructor'], c['course'])
        cursor = cnxn.cursor()
        cursor.execute("insert into Teaches(InstructorID, CourseID) values (?, ?)", values)
        cnxn.commit()

# #TA TABLE:
    for t in ta_array:

        values = (t['id'], 'COMP')
        cursor = cnxn.cursor()
        cursor.execute("insert into TeachingAssistant(TeachingAssistantID, TeachingAssistantDepartment) values (?, ?)", values)
        cnxn.commit()



#ADVISOR TABLE:
    for t in ta_array:

        values = (t['advisor'], t['id'])
        cursor = cnxn.cursor()
        cursor.execute("insert into Advisor(InstructorID, TeachingAssistantID) values (?, ?)", values)
        cnxn.commit()



# REQUESTS TABLE:

    for ta in ta_pref_array:
         index3 = -1
         rank = 0
         prev_index = -1
         prefs = ta['prefs']

         print(len(prefs))
         while index3 < len(prefs):
             try:
                 index3 = prefs.index("\t", index3 + 1)

                 rank = rank + 1
                 if len(prefs[prev_index + 1:index3]) > 1:
                     values = (ta['id'], prefs[prev_index + 1:index3], rank)
                     print(values)
                     cursor = cnxn.cursor()
                     cursor.execute("insert into Requests(TeachingAssistantID, CourseID, ChoiceRank) values (?, ?, ?)", values)
                     cnxn.commit()
                 prev_index = index3
                 print prev_index
             except:
                 rank = rank + 1
                 if len(prefs[prev_index + 1:len(prefs)]) > 1:
                     print('burda')
                     values = (ta['id'], prefs[prev_index + 1:len(prefs)].split()[0], rank)
                     cursor = cnxn.cursor()
                     cursor.execute("insert into Requests(TeachingAssistantID, CourseID, ChoiceRank) values (?, ?, ?)", values)
                     cnxn.commit()
                     print(values)
                     index3 = len(prefs)
                 break


# #PREFERS TABLE:
    for i in pref_array:
         index3 = -1
         rank = 0
         prev_index = -1
         prefs = i['prefs']
         while index3 < len(prefs):
             try:
                 index3 = prefs.index("\t", index3 + 1)

                 rank = rank + 1
                 if len(prefs[prev_index + 1:index3]) > 1:
                     values = (i['id'], prefs[prev_index + 1:index3],i['course'],  rank)
                     cursor = cnxn.cursor()
                     cursor.execute("insert into Prefers(InstructorID, TeachingAssistantID, CourseID, ChoiceRank) values (?, ?, ?, ?)", values)
                     cnxn.commit()
                 prev_index = index3
                 print prev_index
             except:
                 rank = rank + 1
                 if len(prefs[prev_index + 1:len(prefs)]) > 1:
                     values = (i['id'], prefs[prev_index + 1:len(prefs)].split()[0], i['course'], rank)
                     cursor = cnxn.cursor()
                     cursor.execute("insert into Prefers(InstructorID, TeachingAssistantID, CourseID, ChoiceRank) values (?, ?, ?, ?)", values)
                     cnxn.commit()
                     index3 = len(prefs)
                 break


#CONNECT TO DATABASE AND RUN THE QUERY TO INSERT VALUES INTO THE DATABASE


# cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
# cursor = cnxn.cursor()
# #cursor.execute("SELECT TOP 20 pc.Name as CategoryName, p.name as ProductName FROM [SalesLT].[ProductCategory] pc JOIN [SalesLT].[Product] p ON pc.productcategoryid = p.productcategoryid")
# cursor.execute("insert into products(id, name) values (?, ?)", values)
# row = cursor.fetchone()
# while row:
#     print (str(row[0]) + " " + str(row[1]))
#     row = cursor.fetchone()


if __name__ == '__main__':
	main()