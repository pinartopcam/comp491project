import Tkinter as tk                # python 3
import tkFont as tkfont  # python 2

import matplotlib
matplotlib.use("TkAgg")
import Assignment_noDB as a
import PIL.Image as w
import PIL.ImageTk as q
import xlsxwriter
import os

global_result3=[]
global_courses=[]

assignee_spreadsheet = []
authority_spreadsheet = []

class UserInterface(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.resizable(self, 0, 0)
        tk.Tk.geometry(self, "750x750")

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold")

        container = tk.Frame(self , width = 500, height= 500 )
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, WelcomePage, Instructions, ViewPreferences, Link):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class WelcomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent , width = 500, height= 500 )
        self.controller = controller
        label = tk.Label(self, text="Welcome To Optimal Source Assignment Interface", font=controller.title_font)
        label.pack(side="top", fill="x", pady=30)
        image = q.PhotoImage(w.open("Untitled.gif"))
        label3 = tk.Label(self, image=image)
        label3.image = image
        label3.pack()


        label3 = tk.Label(self, font=('Helvetica', 14, "bold") , text="To Start the Assignment, Please Click Continue.")
        label3.pack(side="top", fill="x", padx=100, pady=50)


        button1 = tk.Button(self, text="Continue",
                            command=lambda: controller.show_frame("Instructions"))

        button1.pack(padx=100, pady=50)

        label2 = tk.Label(self, font=('Helvetica', 14, "bold") , text="Created by Gokberk Ozsoy and Pinar Topcam")
        label2.pack(side="top", fill="x", padx=100, pady=50)

class Instructions(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent , width = 500, height= 500 )
        self.controller = controller


        label = tk.Label(self, font=controller.title_font , text="Instructions")
        label.pack(side="top", fill="x", padx=20, pady=50)

        label = tk.Label(self, font=('Helvetica', 14, "bold"), text="1. Please Create two Google Forms to collect preferences.")
        label.pack(side="top", fill="x", padx=20, pady=10)

        button1 = tk.Button(self, text="Click To See The Form and Spreadsheet Instructions Guide",
                            command=lambda: controller.show_frame("Link"))
        button1.pack()

        label = tk.Label(self, font=('Helvetica', 14, "bold"), text="2. Send These Forms to Authorities and Resources.\n\n3. After Preferences Are Collected, Convert the Responses to a Google Spreadsheet.\n\n4. Then Provide Links of Google Spreadsheets In Next Page.")
        label.pack(side="top", fill="x", padx=20, pady=10)


        button1 = tk.Button(self, text="Click to Continue",
                            command=lambda: controller.show_frame("StartPage"))

        button1.pack()
        label2 = tk.Label(self, text="To Return to Start Page, Please Click.", font=('Helvetica', 14, "bold") )
        label2.pack(side="top", fill="x", pady=30)
        button2 = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("WelcomePage"))
        button2.pack()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent , width = 500, height= 500 )
        self.controller = controller
        frames = {}
        flag = False


        label = tk.Label(self, font=('Helvetica', 14, "bold") , text="To continue, please provide the link of Google Spreadsheets.")
        label.pack(side="top", fill="x", padx=20, pady=50)


        label = tk.Label(self, font=('Helvetica', 14, "bold") , text="High Authority Spreadsheet: ")
        label.pack(side="top", fill="x", padx=20, pady=20)

        a = tk.Label(self, text="Link")
        e = tk.Entry(self)

        e.pack()

        label = tk.Label(self, font=('Helvetica', 14, "bold") , text="Assignee Spreadsheet: ")
        label.pack(side="top", fill="x", padx=20, pady=20)

        a = tk.Label(self, text="Link")
        e2 = tk.Entry(self)

        e2.pack()

        assignee_spreadsheet = e.get()
        authority_spreadsheet = e2.get()

        button1 = tk.Button(self, text="Submit the Link",
                            command=lambda: self.createAssignmentPage(frames, parent, controller, e2.get(), e.get(), flag))

        button1.pack(pady=50)
        label2 = tk.Label(self, text="To return to start page, please click.", font=('Helvetica', 14, "bold") )
        label2.pack(side="top", fill="x", pady=30)
        button2 = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("WelcomePage"))
        button2.pack()

    def createAssignmentPage(self, frames,parent, controller, assignee_spreadsheet, authority_spreadsheet, flag):
        flag = True
        if flag:

            splitli_link = assignee_spreadsheet.split('/')

            splitli_link = splitli_link[5]

            splitli_link2 = authority_spreadsheet.split('/')

            splitli_link2 = splitli_link2[5]

            frame = Assignment(parent, controller, splitli_link, splitli_link2)

            frame.grid(row=0, column=0, sticky="nsew")
            frames['Assignment'] = frame
            controller.frames['Assignment'] = frame
            controller.show_frame("Assignment")




class Assignment(tk.Frame):

    def __init__(self, parent, controller, assignee_spreadsheet, authority_spreadsheet):
        frames = {}
        runMain_object = None
        tk.Frame.__init__(self, parent , width = 500, height= 500 )
        self.controller = controller
        flag = False
        label = tk.Label(self, text="                                            ", font=controller.title_font)

        label.grid(row=0, column=1)
        label = tk.Label(self, text="To start the assignment process, \nplease click.", font=controller.title_font)

        label.grid(row=1, column=2)
        label = tk.Label(self, text="    ", font=('Helvetica', 14) )

        label.grid(row=2, column=2)
        label = tk.Label(self, text="Please note that this process may last \nbetween half an hour and an hour.", font=('Helvetica', 14) )

        label.grid(row=3, column=2)
        button = tk.Button(self, text="Start Assignment",
                           command=lambda: self.setTrue(frames, parent, controller, flag, assignee_spreadsheet, authority_spreadsheet, runMain_object))

        button.grid(row=4, column=2)
        label = tk.Label(self, text="    ", font=('Helvetica', 14) )

        label.grid(row=5, column=2)
        label = tk.Label(self, text="    ", font=('Helvetica', 14) )

        label.grid(row=6, column=2)

        label2 = tk.Label(self, text="To return to start page, please click.", font=('Helvetica', 14, "bold") )

        label2.grid(row=7, column=2)
        button2 = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("WelcomePage"))

        button2.grid(row=8, column=2)


    def setTrue(self, frames,parent, controller, flag, assignee_spreadsheet, authority_spreadsheet, runMain_object):
        flag = True

        if flag:
            courses, ta_list, instructors,  taStat, instructorStat,tot_ta_need_per,tot_ta_pref_per, result2, dictionary = a.runMain().run(assignee_spreadsheet, authority_spreadsheet)

            result2 = result2[1:len(result2)-2]

            result3 = result2.split('|')
            index = 0
            global_result3 = result3
            global_courses = courses
            frame = Result(parent, controller, global_result3, global_courses, ta_list, instructors,  taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per,dictionary, runMain_object)

            frame.grid(row=0, column=0, sticky="nsew")
            frames['Result'] = frame
            controller.frames['Result'] = frame
            controller.show_frame("Result")



class Result(tk.Frame):

    def __init__(self, parent, controller, result, courses, ta_list, instructors,  taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per,dictionary, runMain_object):
        tk.Frame.__init__(self, parent , width = 500, height= 500 )
        self.controller = controller
        frames = {}
        flag = False

        label = tk.Label(self, text="Please find the assignment below.", font=controller.title_font)

        label.pack(padx = 20, pady = 20)

        label2 = tk.Label(self, text="To change the assignment manually, \nplease click Manual Change.", font=('Helvetica', 14, "bold"))


        label2.pack(padx = 20, pady = 20)



        index = 0

        new_txt = ''
        for c in courses:
            new_txt = new_txt + c[0] + ' -> '
            for d in dictionary:
                if c[0] in d['course_id']:
                    new_txt = new_txt + d['ta_id'] + ' '

            new_txt = new_txt + '\n\n'
            index = index + 1


        label3 = tk.Label(self, text= new_txt, font=('Helvetica', 10))
        label3.pack(padx = 20, pady = 20)


        button3 = tk.Button(self, text="Extract Results To Excel",
                           command=lambda: self.extractToExcel(flag, courses, ta_list, instructors,  taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per, dictionary))
        button3.pack(padx = 20, pady = 0)
        button2 = tk.Button(self, text="View Statistics",
                           command=lambda: self.showStatistics(frames, parent, controller, result, courses, ta_list, instructors,  taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per, new_txt, dictionary, runMain_object))
        button2.pack(padx = 20, pady = 0)
        index = index + 1

        button1 = tk.Button(self, text="Manual Change",
                           command=lambda: self.createManual(frames, parent, self.controller, flag, result, courses, ta_list, instructors,  taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per,new_txt, dictionary,runMain_object))
        button1.pack(padx = 20, pady = 0)
        index = index + 1
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("WelcomePage"))
        button.pack(padx = 20, pady = 0)


    def createManual(self, frames,parent, controller, flag, result, courses, ta_list, instructors,  taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per,txt, dictionary, runMain_object):
        flag = True

        if flag:

            frame = ManualChange(parent, controller, result, courses, ta_list, instructors, taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per,txt, dictionary, runMain_object)

            frame.grid(row=0, column=0, sticky="nsew")
            frames['ManualChange'] = frame
            controller.frames['ManualChange'] = frame
            controller.show_frame("ManualChange")

    def showStatistics(self, frames, parent, controller, result, courses, ta_list, instructors,  taStat, instructorStat,tot_ta_need_per,tot_ta_pref_per, txt, dictionary, runMain_object):
        flag = True

        if flag:

            frame = ViewStatistics(parent, controller, result, courses, ta_list,instructors,  taStat, instructorStat,tot_ta_need_per,tot_ta_pref_per, txt, dictionary, runMain_object)

            frame.grid(row=0, column=0, sticky="nsew")
            frames['ViewStatistics'] = frame
            controller.frames['ViewStatistics'] = frame
            controller.show_frame("ViewStatistics")

    def extractToExcel(self, flag, courses, ta_list, instructors,  taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per, dictionary):

        flag = True
        if flag:
            desktop = os.path.expanduser("~/Desktop")
            workbook = xlsxwriter.Workbook(desktop+'/ResourceAssignment.xlsx')
            worksheet = workbook.add_worksheet('Assignment')



            bold = workbook.add_format({'bold': True})
            border = workbook.add_format({'border': 1})
            header = workbook.add_format({'border': 1, 'bold': True})
            worksheet.write(0, 0, 'Assignment', bold)

            row = 1
            col = 0

            for c in courses:
                worksheet.write(row, col, c[0], header)
                col = col + 1
                for d in dictionary:
                    if c[0] in d['course_id']:
                        worksheet.write(row, col, d['ta_id'], border)
                        col = col + 1
                col = 0
                row = row + 1

            workbook.close()



class ManualChange(tk.Frame):

    def __init__(self, parent, controller,result, courses, ta_list, instructors, taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per,new_txt, dictionary, runMain_object):
        print('sdfghjkli')
        tk.Frame.__init__(self, parent , width = 500, height= 500 )
        self.parent = parent
        self.controller = controller
        frames = {}


        label = tk.Label(self, text="Assign or Change Manually",  font=('Helvetica', 14, "bold"))
        label.pack(padx=30, pady=30)


        label2 = tk.Label(self,  font=('Helvetica', 14), text="Current Assignment:")
        label2.pack(padx=20, pady=10)


        index = 0
        label3 = tk.Label(self,  font=('Helvetica', 10 ), text=new_txt)
        label3.pack(padx=20, pady=10)



        label4 = tk.Label(self,  font=('Helvetica', 14), text="Select The Course To Change")
        label4.pack(padx = 20, pady = 0)


        course_list = []
        for cou in courses:
            course_list.append(cou[0])

        variable1 = tk.StringVar(self)
        variable1.set(course_list[0])
        y = tk.OptionMenu(self, variable1, *course_list)
        y.pack(padx = 20, pady = 0)

        label5 = tk.Label(self,  font=('Helvetica', 14), text="Select The Teaching Assistant & Delete From Course")
        label5.pack(padx = 20, pady = 0)


        tas = []
        for ta in ta_list:
            tas.append(ta.id)

        variable2 = tk.StringVar(self)
        variable2.set(tas[0])
        y2 = tk.OptionMenu(self, variable2, *tas)
        y2.pack(padx = 20, pady = 0)


        label6 = tk.Label(self,  font=('Helvetica', 14), text="Select The Teaching Assistant & Add To Course")
        label6.pack(padx = 20, pady = 0)

        variable3 = tk.StringVar(self)
        variable3.set(tas[0])
        y3 = tk.OptionMenu(self, variable3, *tas)
        y3.pack(padx = 20, pady = 0)

        flag = False

        c = tk.Button(self, text='Change', command=lambda: self.change(flag, frames, self.parent, self.controller, courses, result, ta_list, instructors,  taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per,variable1, variable2, variable3, dictionary, runMain_object))

        c.pack(padx = 20, pady = 0)
        button3 = tk.Button(self, text="Extract Results To Excel",
                           command=lambda: self.extractToExcel(flag, courses, ta_list, instructors,  taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per, dictionary))
        button3.pack(padx = 20, pady = 0)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack(padx = 20, pady = 0)

    def change(self, flag, frames, parent, controller, courses, result, ta_list,instructors,  taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per,variable1, variable2, variable3, dictionary, runMain_object):
        flag = True
        if flag:
            print 'hey'
            changed_course = variable1.get()
            changed = variable2.get()
            added = variable3.get()

            index = 0

            for d in dictionary:
                if changed_course in d['course_id'] or d['course_id'] in changed_course:
                    if d['ta_id'] in changed or changed in d['ta_id']:
                        d['ta_id'] = added

            new_txt = ''
            index = 0
            print result
            for c in courses:
                new_txt = new_txt + c[0] + ' -> '
                for d in dictionary:
                    if c[0] in d['course_id']:
                        new_txt = new_txt + d['ta_id'] + ' '

                new_txt = new_txt + '\n\n'

                index = index + 1

            frame = ManualChange(parent, controller, result, courses, ta_list, instructors,  taStat, instructorStat,tot_ta_need_per,tot_ta_pref_per, new_txt, dictionary, runMain_object)

            frame.grid(row=0, column=0, sticky="nsew")
            frames['AfterManualChange'] = frame
            controller.frames['AfterManualChange'] = frame
            controller.show_frame("AfterManualChange")

    def extractToExcel(self, flag, courses, ta_list, instructors,  taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per, dictionary):

        flag = True
        if flag:
            desktop = os.path.expanduser("~/Desktop")
            workbook = xlsxwriter.Workbook(desktop+'/ManualChangeResourceAssignment.xlsx')
            worksheet = workbook.add_worksheet('Assignment')



            bold = workbook.add_format({'bold': True})
            border = workbook.add_format({'border': 1})
            header = workbook.add_format({'border': 1, 'bold': True})
            worksheet.write(0, 0, 'Assignment', bold)

            row = 1
            col = 0

            for c in courses:

                worksheet.write(row, col, c[0], header)
                col = col + 1
                for d in dictionary:
                    if c[0] in d['course_id']:
                        #new_txt = new_txt + d['ta_id'] + ' '
                        worksheet.write(row, col, d['ta_id'], border)
                        col = col + 1
                col = 0
                row = row + 1

            workbook.close()



class ViewPreferences(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent , width = 500, height= 500 )
        self.controller = controller
        label = tk.Label(self, text="This is page 1", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("WelcomePage"))
        button.pack()

class ViewStatistics(tk.Frame):

    def __init__(self, parent, controller, result, courses, ta_list, instructor_list ,  taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per,txt, dictionary, runMain_object):
        tk.Frame.__init__(self, parent, width=500, height=500)
        self.controller = controller
        label = tk.Label(self, text=" ", font=('Helvetica', 7, "bold"))
        label.grid(row = 1,column = 1, pady= 20, padx = 5)
        label = tk.Label(self, text=" ", font=('Helvetica', 7, "bold"))
        label.grid(row = 1,column = 2, pady= 20)
        label = tk.Label(self, text=" ", font=('Helvetica', 7, "bold"))
        label.grid(row = 1,column = 3, pady= 20)
        label = tk.Label(self, text="Statistics About This Assignment", font=('Helvetica', 14, "bold"))
        label.grid(row = 1,column = 4, pady= 20)
        label = tk.Label(self, text=" ", font=('Helvetica', 7, "bold"))
        label.grid(row = 2,column = 1, pady= 20)
        label = tk.Label(self, text=" ", font=('Helvetica', 7, "bold"))
        label.grid(row = 2,column = 2, pady= 20)
        label = tk.Label(self, text=" ", font=('Helvetica', 7, "bold"))
        label.grid(row = 2,column = 3, pady= 20)
        button = tk.Button(self, text="Go to Results Page",
                           command=lambda: controller.show_frame("Result"))
        button.grid(row = 2,column = 4)
        button = tk.Button(self, text="Go to Start Page",
                           command=lambda: controller.show_frame("Result"))
        button.grid(row = 3,column = 4)

        print(taStat)
        print(instructorStat)

        txt = ' '
        label = tk.Label(self, text=" ", font=('Helvetica', 7, "bold"))
        label.grid(row = 4,column = 1, pady= 20)
        label = tk.Label(self, text=" ", font=('Helvetica', 7, "bold"))
        label.grid(row = 4,column = 2, pady= 20)
        label = tk.Label(self, text=" ", font=('Helvetica', 7, "bold"))
        label.grid(row = 4,column = 3, pady= 20)
        label = tk.Label(self, text="Authority Statistics", font=('Helvetica', 10, "bold"))
        label.grid(row = 4,column = 4, pady= 20)

        b = tk.Label(self, text=txt, font=('Helvetica', 7))
        b.grid(row = 5,column = 1, pady= 5)
        txt = 'Task Number'
        b = tk.Label(self, text=txt, font=('Helvetica', 7))
        b.grid(row = 5,column = 2, pady= 5 )
        txt = 'Nr. of Resource Need'
        b = tk.Label(self, text=txt, font=('Helvetica', 7))
        b.grid(row = 5,column = 3, pady= 5,  padx = 20)
        txt = 'Nr. of Assigned Resource out of \nResource Requirement Number '
        b = tk.Label(self, text=txt, font=('Helvetica', 7))
        b.grid(row = 5,column = 4, pady= 5,  padx = 20)
        txt = 'Nr. of Authority Preferences'
        b = tk.Label(self, text=txt, font=('Helvetica', 7))
        b.grid(row = 5,column = 5, pady= 5,  padx = 20)
        txt = 'Nr. of Assigned Resources from \nAuthority Preferences'
        b = tk.Label(self, text=txt, font=('Helvetica', 7))
        b.grid(row = 5,column = 6, pady= 5, padx = 20)

        txt = ''
        row = 6
        column = 2
        txt = ' '


        for i in range(len(instructorStat)):  # Rows
            b = tk.Label(self, text=' ', font=('Helvetica', 7))
            b.grid(row = row , column=1, pady=3)
            temp_stat= instructorStat[i]
            temp_txt = ' '
            for jk in range(len(temp_stat)):
                temp_txt = temp_txt + '                                                                             ' + str(temp_stat[jk])
                txt = str(temp_stat[jk])
                b = tk.Label(self, text=txt, font=('Helvetica', 7))

                b.grid(row = row,column = column, pady= 3, padx = 20)
                column = column + 1
            row = row + 1
            column = 2


        label = tk.Label(self, text=" ", font=('Helvetica', 7, "bold"))
        label.grid(row = row+1,column = 1, pady= 20)
        label = tk.Label(self, text=" ", font=('Helvetica', 7, "bold"))
        label.grid(row = row+1,column = 2, pady= 20)
        label = tk.Label(self, text=" ", font=('Helvetica', 7, "bold"))
        label.grid(row = row+1,column = 3, pady= 20)
        label = tk.Label(self, text="Resource Statistics", font=('Helvetica', 10, "bold"))
        label.grid(row = row+1,column = 4, pady= 20)

        row = row + 2

        txt = ''
        b = tk.Label(self, text=txt, font=('Helvetica', 7))
        b.grid(row = row,column = 1, pady= 5)
        txt = 'Number of Resources'
        b = tk.Label(self, text=txt, font=('Helvetica', 7))
        b.grid(row = row,column = 2, pady= 5 )
        txt = 'Nr. of Resource Preferences'
        b = tk.Label(self, text=txt, font=('Helvetica', 7))
        b.grid(row = row,column = 3, pady= 5,  padx = 20)
        txt = 'Nr. of Resources Assigned to \nTheir First Preferences '
        b = tk.Label(self, text=txt, font=('Helvetica', 7))
        b.grid(row = row,column = 4, pady= 5,  padx = 20)
        txt = 'Nr. of Resources Assigned to \nTheir Second Preferences '
        b = tk.Label(self, text=txt, font=('Helvetica', 7))
        b.grid(row = row,column = 5, pady= 5,  padx = 20)
        txt = 'Nr. of Resources Assigned to \nTheir Third Preferences '
        b = tk.Label(self, text=txt, font=('Helvetica', 7))
        b.grid(row = row,column = 6, pady= 5, padx = 20)
        #
        row = row + 1
        column = 2
        txt = ' '

        b = tk.Label(self, text=' ', font=('Helvetica', 7))
        b.grid(row=row, column=1, pady=3)

        b = tk.Label(self, text=len(ta_list), font=('Helvetica', 7))

        b.grid(row=row, column=column, pady=3, padx=20)
        column = column + 1
        b = tk.Label(self, text=3, font=('Helvetica', 7))

        b.grid(row=row, column=column, pady=3, padx=20)
        column = column + 1

        for i in range(len(taStat)):

            txt= taStat[i]
            b = tk.Label(self, text=txt, font=('Helvetica', 7))

            b.grid(row = row,column = column, pady= 3, padx = 20)
            column = column + 1



class AfterManualAssignment(tk.Frame):

    def __init__(self, frames,parent, controller, flag, result, courses, ta_list, instructors, txt, runMain_object):
        tk.Frame.__init__(self, parent , width = 500, height= 500 )
        self.controller = controller


        label = tk.Label(self, font=('Helvetica', 14, "bold"), text="The assignment is changed manually. \n The result is provided below.")
        label.pack(side="top", fill="x", padx=20, pady=50)

        label = tk.Label(self, font=('Helvetica', 14, "bold"), text=txt)
        label.pack(side="top", fill="x", padx=20, pady=50)

        label = tk.Label(self, font=('Helvetica', 14, "bold"), text="To continue changing manually, please click Continue button.")
        label.pack(side="top", fill="x", padx=20, pady=50)


        button1 = tk.Button(self, text="Continue",
                            command=lambda: self.createManual(frames,parent, controller, flag, result, courses, ta_list, instructors, txt, runMain_object))

        button1.pack()
        label2 = tk.Label(self, text="To Return to Start Page, Please Click.", font=('Helvetica', 14, "bold") )
        label2.pack(side="top", fill="x", pady=30)
        button2 = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("WelcomePage"))
        button2.pack()


    def createManual(self, frames,parent, controller, flag, result, courses, ta_list, instructors, txt, runMain_object):
        flag = True

        if flag:

            frame = ManualChange(parent, controller, result, courses, ta_list, txt, runMain_object)

            frame.grid(row=0, column=0, sticky="nsew")
            frames['ManualChange'] = frame
            controller.frames['ManualChange'] = frame
            controller.show_frame("ManualChange")


class Link(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent , width = 500, height= 500 )
        self.controller = controller


        label = tk.Label(self, font=('Helvetica', 14, "bold"), text="Instructions Video Link")
        label.pack(side="top", fill="x", padx=20, pady=50)
        label = tk.Text(self, height=1)
        label.tag_configure("center", justify='center')
        label.insert(1.0, "https://youtu.be/P9zLqdYM0qQ")
        label.tag_add("center", "1.0", "end")

        label.pack(anchor="center", ipadx= 100, fill="x", padx=50, pady=50)


        label2 = tk.Label(self, text="To Return to Instructions Page, Please Click.", font=('Helvetica', 14, "bold") )
        label2.pack(side="top", fill="x", pady=30)
        button2 = tk.Button(self, text="Go to instructions page",
                           command=lambda: controller.show_frame("Instructions"))
        button2.pack()




class Course:

    def __init__(self, id, name, ta_need):
        self.id = id
        self.name = name
        self.ta_need = ta_need

if __name__ == "__main__":
    app = UserInterface()
    app.mainloop()

