import Instructor as i
import Course as co
import TeachingAssistant as ta
from random import shuffle
import random
import numpy as np
import excel_read as e


class Assignment_noDB:
    def __init__(self, preference_list, ta_list, course_list, instructor_list):
        self.preference_list = preference_list
        self.ta_list = ta_list
        self.course_list = course_list
        self.instructor_list = instructor_list


    # check preference data of both high authorities and resources. If there is no information in any slot that
    # should have been full, this function fills this slot randomly. Of course, this function only fills the preference
    # data for high authorities and resources. Other information such as number of resource need of a task is must be
    # filled during the form filling step. However, if the resource or high authority made some of her choices but left
    # some of them empty, we run this function before assignment to fill all empty preferences.
    def check_preferences(self, courses):
        from random import randint

        for instructor in self.instructor_list:
            for course in instructor.courses:
                #get the number of preferences for each specific course

                course_preferences = []
                final_list = []
                final_ids = []
                available_ranks = []
                for cou in courses:
                    if course.id == cou.id:
                        ta_need = int(cou.ta_need)

                numberOfPref = 0
                if ta_need == 1:
                    numberOfPref = 3
                elif ta_need == 2:
                    numberOfPref = 5
                else:
                    numberOfPref = ta_need * 2

                for pref in instructor.preferences:
                    if pref.course_id == course.id:
                        course_preferences.append(pref)
                        # to remove the duplicate preferences
                        if pref.ta_id not in final_ids:
                            final_list.append(pref)
                            final_ids.append(pref.ta_id)
                            available_ranks.append(pref.rank)
                        else:
                            index = instructor.preferences.index(pref)
                            instructor.preferences.pop(index)

                course_preferences = final_list
                preference_per_course = len(course_preferences)

                if preference_per_course == numberOfPref:
                    continue
                else:
                    nr_of_preferences = preference_per_course

                    if nr_of_preferences > numberOfPref:
                        #if there are more than required preferences
                        index = nr_of_preferences
                        while index != nr_of_preferences:
                            instructor.preferences.pop(index-1)
                            index = index - 1
                    else:
                        #if there are less than required preferences
                        required_pref = numberOfPref - nr_of_preferences

                        not_available_ranks = []
                        count = 1
                        while count < numberOfPref+1:
                            if count not in available_ranks:
                                not_available_ranks.append(count)
                            count = count + 1
                        not_available_ranks.reverse()

                        while required_pref != 0:

                            random_number = randint(0, len(self.ta_list)-1)
                            valid_preference = True

                            for pref in instructor.preferences:
                                if pref.ta_id == self.ta_list[random_number].id and course.id == pref.course_id:
                                    #if this ta is already in preference list
                                    valid_preference = False
                                    break

                            if valid_preference:
                                instructor.createPreference(instructor.id,self.ta_list[random_number].id, course.id, not_available_ranks.pop())
                                nr_of_preferences = nr_of_preferences + 1
                                required_pref = required_pref - 1


        for ta in self.ta_list:

            ta_preferences = ta.preferences
            numberOfPref = 3

            final_list = []
            final_ids = []
            available_ranks = []

            # to remove the duplicate preferences
            for pref in ta.preferences:
                if pref.course_id not in final_ids:
                    final_list.append(pref)
                    final_ids.append(pref.course_id)
                    available_ranks.append(pref.rank)
                else:
                    index = ta.preferences.index(pref)
                    ta.preferences.pop(index)

            ta_preferences = final_list

            if len(ta_preferences) == numberOfPref:
                continue
            else:
                nr_of_preferences = len(ta_preferences)

                not_available_ranks = []
                count = 1
                while count < numberOfPref+1:
                    if count not in available_ranks:
                        not_available_ranks.append(count)
                    count = count + 1
                not_available_ranks.reverse()

                if nr_of_preferences > numberOfPref:
                    #if there are more than 10 preferences
                    index = nr_of_preferences
                    while index != nr_of_preferences:
                        ta_preferences.pop(index-1)
                        index = index - 1
                else:
                    #if there are less than 10 preferences
                    required_pref = numberOfPref - nr_of_preferences

                    while required_pref != 0:

                        random_number = randint(0, len(self.course_list)-1)
                        valid_preference = True

                        for pref in ta.preferences:
                            if pref.course_id == self.course_list[random_number].id:
                                #if this ta is already in preference list
                                valid_preference = False
                                break

                        if valid_preference:
                            ta.createPreference(ta.id, self.course_list[random_number].id, None, not_available_ranks.pop())
                            required_pref = required_pref - 1


    # this is the score function of our project. it is implemented as declared in the report and it scores the
    # fitness of the given chromosome.
    def score(self, chromosome, courselist, instructorlist, empFactor, wi, wta):

        courseSatisfaction=[]

        for c in range(len(courselist)):
            assignedTAs = chromosome[c]
            numberOfTaPref=3

            if len(assignedTAs)==1:
                numberofInsPref=3
            elif len(assignedTAs)==2:
                numberofInsPref=5
            else:
                numberofInsPref=2*len(assignedTAs)

            instructor=None
            for i in range(len(instructorlist)):
                if instructorlist[i].id==courselist[c].instructor:
                    instructor=instructorlist[i]

            taneed = int(courselist[c].ta_need)
            instructor_satisfaction=0
            overall_ta_satisfaction=0


            # instructor satisfaction for c

            for x in range(len(assignedTAs)):
                if assignedTAs[x] is not None:  # new addition for coping with assignments None
                    for p in range(len(instructor.preferences)):

                        if instructor.preferences[p].ta_id == assignedTAs[x].id and instructor.preferences[p].course_id==courselist[c].id:
                            instructor_satisfaction +=  (float (numberofInsPref+1-instructor.preferences[p].rank))*empFactor

            base_case = 0

            for x in range(len(assignedTAs)):
                base_case += (float (numberofInsPref-x))*empFactor

            instructor_satisfaction=int ((instructor_satisfaction/base_case)*100)

            # ta satisfaction for c

            for k in range(len(assignedTAs)):
                if assignedTAs[k] is not None:  # new addition for coping with assignments None
                    for p in range(len(assignedTAs[k].preferences)):

                        if assignedTAs[k].preferences[p].course_id== courselist[c].id:
                            overall_ta_satisfaction += int( ( (float ((numberOfTaPref+1-assignedTAs[k].preferences[p].rank)*empFactor)) / (float (numberOfTaPref*empFactor))) *100)

            overall_ta_satisfaction= overall_ta_satisfaction/taneed

            # satisfaction for c

            satisfaction=(wi*instructor_satisfaction + wta*overall_ta_satisfaction)/(wi+wta)
            courseSatisfaction.append(satisfaction)


        tot = 0
        for cs in range(len(courseSatisfaction)):
           tot += courseSatisfaction[cs]
        return tot/(len(courseSatisfaction))


    # this method does a lot of job. it first scores the given population, saves the noteworthy chromosomes and
    # creates the next generation by applying crossover and mutation operations to the current population.
    def assign(self, initialPopulation, numberOfIter, cloningPercentage, crossoverPercantage, mutationPercentage, empFactor, wi, wta, maxNoOfCollision, tas, courses, instructors, domain):

        pop = initialPopulation
        iterations = numberOfIter


        popSize = len(pop)
        NoOfclonedChros = int(cloningPercentage * popSize)
        NoOfcrossedChros = int(crossoverPercantage * popSize)
        NoOfmutatedChros = int(mutationPercentage * popSize)

        bestScoreChoromosomeList = [[0,0] for y in xrange(maxNoOfCollision+1)]  # first -> chromosome, second -> score

        for l in range(iterations):


            # calculate the score of each chromosome in population
            for p in range(popSize):
                temp_ch = pop[p]
                s = self.score(temp_ch, courses, instructors, empFactor, wi, wta)
                temp_collision = self.countCollisions(temp_ch, tas)

                if temp_collision <= maxNoOfCollision:

                    if s > bestScoreChoromosomeList[temp_collision][1]:

                        yy = []  # holds only the assignments
                        for jk in range(len(temp_ch)):
                            temp_tr=[]
                            for jh in range(len(temp_ch[jk])):
                                temp_tr.append(temp_ch[jk][jh])
                            yy.append(temp_tr)

                        bestScoreChoromosomeList[temp_collision][1] = s
                        bestScoreChoromosomeList[temp_collision][0] = yy

            # produce next generation from the current generation
            clonedChros = []
            crossedChros = []
            mutatedChros = []
            permutedIndices = np.random.permutation(popSize)
            currentIndex = 0

            for clo in range(NoOfclonedChros):
                clonedChros.append(pop[permutedIndices[currentIndex]])
                currentIndex += 1

            for cros in range(NoOfcrossedChros):
                crossedChros.append(pop[permutedIndices[currentIndex]])
                currentIndex += 1

            for mut in range(NoOfmutatedChros):
                mutatedChros.append(pop[permutedIndices[currentIndex]])
                currentIndex += 1

            childsOfCrossChros = []
            crossoverIndex = 0
            for j in range(NoOfcrossedChros / 2):
                parent1 = crossedChros[crossoverIndex]
                crossoverIndex += 1
                parent2 = crossedChros[crossoverIndex]
                crossoverIndex += 1
                ch1, ch2 = self.crossover(parent1, parent2, tas, maxNoOfCollision,0)
                childsOfCrossChros.append(ch1)
                childsOfCrossChros.append(ch2)

            mutants = []
            mutationIndex = 0
            for mj in range(NoOfmutatedChros):
                mutants.append(self.mutation(mutatedChros[mutationIndex], domain, tas, maxNoOfCollision))

            popIndex = 0
            for clo in range(NoOfclonedChros):
                pop[popIndex] = clonedChros[clo]
                popIndex += 1

            for cros in range(NoOfcrossedChros):
                pop[popIndex] = childsOfCrossChros[cros]
                popIndex += 1

            for mut in range(NoOfmutatedChros):
                pop[popIndex] = mutatedChros[mut]
                popIndex += 1

        return bestScoreChoromosomeList


    # initializes the population given the domain information of each task. this is the starting point of iterations.
    # first generation is created by the result of this function.
    def initialize(self,populationSize,courses,domain,tas,maxNoOfCollision):

        population = []
        n = 0

        while n < populationSize: #for each chromosome
            chromosome = []

            for cl in range(len(courses)):  #for each course

                temp_ta_need=int(courses[cl].ta_need)
                temp_domain=domain[cl] #returns the candidate ta list for this course
                shuffle(temp_domain)
                temp_assigned_tas=[]

                for j in range(temp_ta_need):
                    if j < len(temp_domain):
                        temp_assigned_tas.append(temp_domain[j])
                    else:
                        temp_assigned_tas.append(None)

                chromosome.append(temp_assigned_tas)

            if self.countCollisions(chromosome,tas) <= maxNoOfCollision:
                n = n+1
                population.append(chromosome)

        return population


    # counts the numbers of collisions in the given chromosome.
    def countCollisions(self,chromosome,tas):

        numberOfCollisions = 0

        for ta_index in range(len(tas)):
            temp_ta = tas[ta_index]
            occurrence = 0

            for c_index in range(len(chromosome)):  # for each course
                temp_ta_list = chromosome[c_index]

                for tr in range(len(temp_ta_list)):
                    if temp_ta_list[tr] is not None:
                        if temp_ta.id == temp_ta_list[tr].id:
                            occurrence += 1

            if occurrence == 2:
                numberOfCollisions += 1

            elif occurrence == 3:
                numberOfCollisions += 2

        return numberOfCollisions


    # given two chromosomes, this function applies crossover by randomly selecting the gene which will be swapped.
    def crossover(self,chromosome1,chromosome2,tas,maxNoOfCollision,it):

        crossedCourseIndex=random.randint(0,len(chromosome1)-1)
        safe1=chromosome1[crossedCourseIndex]
        safe2=chromosome2[crossedCourseIndex]
        maxIteration=100

        sourceTaList=chromosome1[crossedCourseIndex]
        chromosome1[crossedCourseIndex]=chromosome2[crossedCourseIndex]
        chromosome2[crossedCourseIndex]=sourceTaList

        if it < maxIteration:
            if self.countCollisions(chromosome1,tas) > maxNoOfCollision or self.countCollisions(chromosome2,tas) > maxNoOfCollision:
                chromosome1[crossedCourseIndex]=safe1
                chromosome2[crossedCourseIndex]=safe2
                self.crossover(chromosome1,chromosome2,tas,maxNoOfCollision,it+1)

        return chromosome1,chromosome2


    # given one chromosome, this function applies the mutation operation to that chromosome in collaboration with the
    # domain information of the task
    def mutation(self,chromosome1,domain,tas,maxNoOfCollision):

        mutatedCourseIndex =random.randint(0,len(chromosome1)-1)

        courseDom=domain[mutatedCourseIndex]
        assignedDom=chromosome1[mutatedCourseIndex]

        temp_taneed=len(chromosome1[mutatedCourseIndex])
        mutationTaIndex_source=random.randint(0,temp_taneed-1)
        temp_ta=chromosome1[mutatedCourseIndex][mutationTaIndex_source]

        possibleDomain=(list(set(courseDom) - set(assignedDom)) + list(set(assignedDom) - set(courseDom)))

        if len(possibleDomain) != 0:
            mutationTaIndex_destination=random.randint(0,len(possibleDomain)-1)
            chromosome1[mutatedCourseIndex][mutationTaIndex_source]= possibleDomain[mutationTaIndex_destination]

            if self.countCollisions(chromosome1,tas) > maxNoOfCollision:
                chromosome1[mutatedCourseIndex][mutationTaIndex_source]=temp_ta
                self.mutation(chromosome1,domain,tas,maxNoOfCollision)

        else:
            self.mutation(chromosome1,domain,tas,maxNoOfCollision)

        return chromosome1

    # this function is for showing statistics about the final assignment. it is binded with the UI and all of its
    # outputs feed the UI.
    def showStats(self,chromosome,courses,instructor_list,tas):
         result = ""
         result2 = ""
         final_assignment_courses = []
         final_assignment_ids=[]
         dictionary=[]
         #calculation of statistics
         numberOfTaPref = 3
         taStat = [0 for m in xrange(numberOfTaPref)]
         instructorStat=[]

         instructorStat1=[0 for s1 in xrange(3)]
         instructorStat.append(instructorStat1)
         instructorStat2=[0 for s2 in xrange(5)]
         instructorStat.append(instructorStat2)
         instructorStat3=[0 for s3 in xrange(6)]
         instructorStat.append(instructorStat3)
         instructorStat4 = [0 for s4 in xrange(8)]
         instructorStat.append(instructorStat4)
         instructorStat5 = [0 for s5 in xrange(10)]
         instructorStat.append(instructorStat5)
         instructorStat6 = [0 for s5 in xrange(12)]
         instructorStat.append(instructorStat6)


         for c in range(len(courses)): #for each course

             temp_ins_id=courses[c].instructor
             temp_ins=None
             for ins in range(len(instructor_list)):
                 if temp_ins_id == instructor_list[ins].id:
                     temp_ins=instructor_list[ins]


             for i in range(int(courses[c].ta_need)): #for each ta of a particular course

                temp_ta=chromosome[c][i]
                index_for_insStat=int(courses[c].ta_need)-1

                stat=-1
                if temp_ta is not None:  # for instructor statistics
                    for inspref in range(len(temp_ins.preferences)):
                        if temp_ins.preferences[inspref].ta_id == temp_ta.id and temp_ins.preferences[inspref].course_id == courses[c].id:
                            stat=temp_ins.preferences[inspref].rank

                if stat != -1:
                    instructorStat[index_for_insStat][stat-1] += 1

                stat =-1
                if temp_ta is not None:  # for ta statistics
                    for tapref in range(len(temp_ta.preferences)):
                        if temp_ta.preferences[tapref].course_id == courses[c].id:
                            stat = temp_ta.preferences[tapref].rank

                if stat != -1:
                    taStat[stat-1] += 1

         # this part is for the calculation of data that will be used in UI

         instructor_five_col_data = []  # first-> taneed, second -> how many in taneed, three -> how many in no of pref
         total_course_ta_need_per = []
         total_course_pref_per= []

         for cx in range(len(courses)):  # for each course

            temp_course_id = courses[cx].id
            temp_ins_id = courses[cx].instructor

            temp_ta_need = int(courses[cx].ta_need)

            howmanyintaneed = 0
            howmanyinpreferences = 0

            if temp_ta_need == 1:
                temp_no_of_pref = 3
            elif temp_ta_need == 2:
                temp_no_of_pref = 5
            else:
                temp_no_of_pref = 2 * temp_ta_need

            temp_ins = None
            for ins in range(len(instructor_list)):
                if temp_ins_id == instructor_list[ins].id:
                    temp_ins = instructor_list[ins]

            temp_assigned_tas = chromosome[cx]

            for ix in range(len(temp_assigned_tas)):  # for each ta of a particular course

                temp_tax = temp_assigned_tas[ix]

                if temp_tax is not None:
                    for insprefx in range(len(temp_ins.preferences)):
                        if temp_ins.preferences[insprefx].ta_id == temp_tax.id and temp_ins.preferences[
                            insprefx].course_id == courses[cx].id:

                            temp_rank = temp_ins.preferences[insprefx].rank

                            if temp_rank <= temp_ta_need:
                                howmanyintaneed = howmanyintaneed + 1
                            if temp_rank <= temp_no_of_pref:
                                howmanyinpreferences = howmanyinpreferences + 1

            instructor_five_col_data.append([temp_course_id, temp_ta_need,howmanyintaneed, temp_no_of_pref, howmanyinpreferences])

            ta_need_per=  (float(howmanyintaneed) / float(temp_ta_need)) * 100
            total_course_ta_need_per.append(ta_need_per)
            ta_pref_per= (float(howmanyinpreferences) / float(temp_ta_need)) * 100
            total_course_pref_per.append(ta_pref_per)


         tot_ta_need_per= int (sum(total_course_ta_need_per) / float(len(total_course_ta_need_per)) )
         tot_ta_pref_per= int (sum(total_course_pref_per) / float(len(total_course_pref_per)) )



         for kk in range(len(courses)):
             result = result + "|"

             for ck in range(int(courses[kk].ta_need)):
                 result = result + " " + str(courses[kk].id) + " "
                 final_assignment_courses.append(courses[kk].id)




         for ix in range(len(chromosome)):
             result2 = result2 + "|"

             for ik in range(len(chromosome[ix])):
                 if chromosome[ix][ik] is None:
                     final_assignment_ids.append(None)
                 else:
                    result2 = result2 + chromosome[ix][ik].id + ' '
                    final_assignment_ids.append(chromosome[ix][ik].id)


         for jkh in range(len(final_assignment_courses)):
             if final_assignment_ids[jkh] is not None:
                 dictionary.append({'course_id': final_assignment_courses[jkh], 'ta_id': final_assignment_ids[jkh]})
             else:
                 dictionary.append({'course_id': final_assignment_courses[jkh], 'ta_id': 'None'})

         return result2, dictionary,taStat,instructor_five_col_data, tot_ta_need_per,tot_ta_pref_per


    # this function creates domains for each task by intersecting the high authority and resource preferences.
    def createDomain(self, tas, courses, instructors):
        domain = [[] for y in xrange(len(courses))]

        for t in range(len(tas)):
            for pr in range(len(tas[t].preferences)):

                temp_ta_id = tas[t].id
                temp_id = tas[t].preferences[pr].course_id
                temp_index = -1
                for ct in range(len(courses)):
                    if courses[ct].id == temp_id:
                        temp_index = ct

                temp_course=courses[temp_index]
                temp_ins_id= temp_course.instructor


                temp_instructor = None
                for i in range(len(instructors)):
                    if instructors[i].id == temp_ins_id:
                        temp_instructor = instructors[i]

                flag = False
                for pi in range(len(temp_instructor.preferences)):
                    if temp_ta_id == temp_instructor.preferences[pi].ta_id:
                        flag = True
                if flag:
                    domain[temp_index].append(tas[t])
        return domain


    # this function detects the unassigned resources by comparing the assignment results and the resource pool.
    def detectUnassignedTas(self,chromosome,tas):  # gives the unassigned TAs as list

        soFarAssigned=[]

        for cours in range(len(chromosome)):
            for ts in range(len(chromosome[cours])):
                if chromosome[cours][ts] is not None:

                    flag=False
                    for sfa in range(len(soFarAssigned)):
                        if soFarAssigned[sfa] == chromosome[cours][ts]:
                            flag=True

                    if not flag:
                        soFarAssigned.append(chromosome[cours][ts])

        unassignedList = (list(set(tas) - set(soFarAssigned)) + list(set(soFarAssigned) - set(tas)))

        return unassignedList

    # this function detects the multiply assigned resources in a given chromosome and returns them.
    def getmultipleassignedtas(self,chromosome,tas):  # helper for collision handle function: first step

        multipleAssignedTas = []
        classifiedMultipleAssignedList = []

        for searchTaIndex in range(len(tas)):
            searchTa = tas[searchTaIndex]
            multipleFlag = 0

            for cour in range(len(chromosome)):  # for each course
                for ta_index in range(len(chromosome[cour])):  # for each ta in that course
                    if chromosome[cour][ta_index] is not None and chromosome[cour][ta_index].id == searchTa.id:
                        multipleFlag += 1

            if multipleFlag > 1:
                for cour in range(len(chromosome)):  # for each course
                    for ta_index in range(len(chromosome[cour])):  # for each ta in that course
                        if chromosome[cour][ta_index] is not None and chromosome[cour][ta_index].id == searchTa.id:
                            multipleAssignedTas.append([searchTa, [cour, ta_index]])


        while multipleAssignedTas!=[]:

            temp_collided_ta_list=[]
            temp_collided_ta_list.append(multipleAssignedTas[0])

            temp_id=multipleAssignedTas[0][0].id
            multipleAssignedTas.pop(0)
            if multipleAssignedTas == []:
                break

            while multipleAssignedTas[0][0].id == temp_id:
                temp_collided_ta_list.append(multipleAssignedTas[0])
                multipleAssignedTas.pop(0)
                if multipleAssignedTas == []:
                    break

            classifiedMultipleAssignedList.append(temp_collided_ta_list)

        return classifiedMultipleAssignedList


    # this function is helper to collisionHandler function and it decides which of the multiple assigned resource
    # copies should remain in the assignment so that the overall score becomes the largest.
    def decidewhichtoremain(self,temp_collided_ta_list,chromosome,courses,instructors,tas,empFactor,wi,wta):

        scores = []

        for tctl_index in range(len(temp_collided_ta_list)):  # for each multiple assigned ta

            templateChro = []  # holds only the assignments
            for jk in range(len(chromosome)):
                temp_tr = []
                for jh in range(len(chromosome[jk])):
                    temp_tr.append(chromosome[jk][jh])
                templateChro.append(temp_tr)

            iter = 0
            while iter < len(temp_collided_ta_list):
                if tctl_index != iter:
                    location = temp_collided_ta_list[iter][1]
                    iter = iter + 1
                    templateChro[location[0]][location[1]] = None
                else:
                    iter = iter + 1

            scores.append(self.score(templateChro, courses, instructors, empFactor, wi, wta))

        return scores

    # this function is helper to the collisionHandler function and it is basically eleminates all the copies of the multiple assigned
    # resources expect the ones which are decided in the decidewhichtoremain() function. Thus as output of this function,
    # we end up with a collision free chromosome.
    def rearrangeChromosome(self,chromosome,allScores,classifiedMultipleAssignedList):

        for c_index in range(len(classifiedMultipleAssignedList)):
            temp_score_list=allScores[c_index]
            remainingIndex=temp_score_list.index(max(temp_score_list))

            temp_collided_ta_list=classifiedMultipleAssignedList[c_index]


            for iter2 in range(len(temp_collided_ta_list)):
                 if remainingIndex != iter2:
                     location = temp_collided_ta_list[iter2][1]
                     chromosome[location[0]][location[1]] = None

        return chromosome

    # this function is helper to the collisionHandler function and it returns the empty locations in the given chromosome.
    def giveNoneLocations(self,chromosome):  # if there is any None in the assignment, returns true and gives the locations of Nones
                                             #  might be little unnecessary

        locations=[]

        for cours in range(len(chromosome)):
            for ts in range(len(chromosome[cours])):
                if chromosome[cours][ts] is None:
                    locations.append([cours,ts])

        return locations

    # this function is helper to the collisionHandler function. Given a list of unassigned resources, this function puts each
    # unassigned resource to each empty slots in the chromosome. For each put, the resulting score is calculated.
    # the resulting score of each try is decided by looking at if the resource is in the list of the manager of the corresponding task
    # if the resource has preferred that task in its preference list or both. Then at the end of the day, we get the information
    # for each unassigned resource about where to assign them.
    def getCandidatesforNoneSlots(self,chromosome,unassignedTas,courses,instructors,wi,wta):

        noneLocations=self.giveNoneLocations(chromosome)
        candidates = []

        for nl in range(len(noneLocations)):  # for each None slot
            none_course=courses[noneLocations[nl][0]]
            none_course_id=none_course.id
            none_course_instructor_id=none_course.instructor
            none_course_instructor=None

            for ins in range(len(instructors)):
                if none_course_instructor_id == instructors[ins].id:
                    none_course_instructor = instructors[ins]


            temp_candidates = []

            for uata_index in range(len(unassignedTas)):  # for each unassigned Ta check for particular None slot if she is good match
                temp_ta=unassignedTas[uata_index]

                passFlag=True

                for inspref in range(len(none_course_instructor.preferences)):  # iterate on instructor preferences
                    for tapref in range(len(temp_ta.preferences)):  # iterate on ta preferences

                        if none_course_instructor.preferences[inspref].ta_id == temp_ta.id and none_course_instructor.preferences[inspref].course_id==none_course_id and temp_ta.preferences[tapref].course_id == none_course_id:
                            ipreflen=len(none_course_instructor.preferences)
                            tapreflen=len(temp_ta.preferences)
                            priority= wi*(ipreflen-none_course_instructor.preferences[inspref].rank) + wta*(tapreflen-temp_ta.preferences[tapref].rank)
                            temp_candidates.append([temp_ta,priority]) # if 0 no priority, if 1 instructor wants, if 2 both wants
                            passFlag=False

                if passFlag:
                    for inspref in range(len(none_course_instructor.preferences)):  # iterate on instructor preferences
                        if none_course_instructor.preferences[inspref].ta_id == temp_ta.id and none_course_instructor.preferences[inspref].course_id==none_course_id:
                            ipreflen = len(none_course_instructor.preferences)
                            priority = wi*(ipreflen-none_course_instructor.preferences[inspref].rank)
                            temp_candidates.append([temp_ta, priority])  # if 0 no priority, if 1 instructor wants, if 2 both wants
                            passFlag = False

                if passFlag:
                    for tapref in range(len(temp_ta.preferences)):  # iterate on ta preferences
                        if temp_ta.preferences[tapref].course_id == none_course_id:
                            tapreflen = len(temp_ta.preferences)
                            priority = wta*(tapreflen-temp_ta.preferences[tapref].rank)
                            temp_candidates.append([temp_ta, priority])

            candidates.append(temp_candidates)

        return noneLocations,candidates


    # this function is also the helper for collisionHandler function and given the unassigned resources score information
    # for each empty location in the chromosome, we fill the empty slots by comparing the scores of each resource for each empty slot.
    # for example, if an unassigned resource has the maximum score for a particular tas that is calculated in getCandidatesforNoneSlots() function
    # compared to the others, then it will be assigned to that task. this function recursively assigns the maximum scores to the
    # empty spots until every unassigned resource is assigned to a task.
    def fillChromosome(self,chromosome,candidates,noneLocations,tas,courses,instructors,wi,wta): # helper for collision handle function: fourth step

        #finds the best match for each none location by looking at the maximum score.
        maxCandidates=[]
        for can in range(len(candidates)): # iterate over each None slot
            max = -1
            index = -1
            for i in range(len(candidates[can])):
                if candidates[can][i][1] > max:
                    max=candidates[can][i][1]
                    index=i
            if len(candidates[can])>0:
                maxCandidates.append([can,candidates[can][index]])


        for maxC in range(len(maxCandidates)):
            presentFlag=False

            for othermaxC in range(len(maxCandidates)):
                if maxC != othermaxC:
                    if maxCandidates[maxC][1][0] == maxCandidates[othermaxC][1][0]:
                        presentFlag=True


            if not presentFlag:
                none_index=maxCandidates[maxC][0]
                none_location=noneLocations[none_index]
                chromosome[none_location[0]][none_location[1]]= maxCandidates[maxC][1][0]

        unas=self.detectUnassignedTas(chromosome,tas)
        while unas != []:
            lastNoneSlots,lastCandidates= self.getCandidatesforNoneSlots(chromosome,unas,courses,instructors,wi,wta)
            if len(lastCandidates[0])==0:
                break
            LastmaxCandidate = []
            lmax = -1
            lindex = -1
            lcani= -1
            for lcan in range(len(lastCandidates)):  # iterate over each last None slot
                for li in range(len(lastCandidates[lcan])):
                    if lastCandidates[lcan][li][1] > lmax:
                        lmax = lastCandidates[lcan][li][1]
                        lindex = li
                        lcani= lcan
            LastmaxCandidate.append([lcani, lastCandidates[lcani][lindex]])

            none_index = LastmaxCandidate[0][0]
            none_location = lastNoneSlots[none_index]
            chromosome[none_location[0]][none_location[1]] = LastmaxCandidate[0][1][0]
            unas = self.detectUnassignedTas(chromosome, tas)


        # after every option, just assign randomly
        final_unas=self.detectUnassignedTas(chromosome,tas)
        final_noneLocations=self.giveNoneLocations(chromosome)

        shuffle(final_unas)
        shuffle(final_noneLocations)

        for jkl in range(len(final_unas)):
            fnl_none_location=final_noneLocations[jkl]
            chromosome[fnl_none_location[0]][fnl_none_location[1]]=final_unas[jkl]

        return chromosome


    # this function is kind of the accumulation of multiple different functions into same body. the main aim of this function
    # is to detect multiple assigned resources, calculate which replica of each multiple assigned resource will remain in the chromosome,
    # eleminate the other ones so that the chromosome becomes collision free, and finally match the unassigned resources with the empty slots
    # in the chromosome.
    def collisionHandler(self,chromosome,tas,courses,instructors,empFactor,wi,wta):
        #  this will be applied at the very end.
        #  during mid-steps, any chromosome might have None as assignment.

        #first -> detect multiple assigned tas.
        classifiedMultipleAssignedList=self.getmultipleassignedtas(chromosome,tas)

        #second -> for each multiple assigned ta, convert each replica one by one into None and calculate score.
        allScores=[]
        for c_index in range(len(classifiedMultipleAssignedList)):
            allScores.append(self.decidewhichtoremain(classifiedMultipleAssignedList[c_index],chromosome,courses,instructors,tas,empFactor,wi,wta))


        # third -> get the best score for each multiple assigned tas separately, so you decide which replica of the multiple assigned ta will be left.
        rearrangedChromosome=self.rearrangeChromosome(chromosome,allScores,classifiedMultipleAssignedList)


        #fourth -> by trying all the possibilities of unassigned Tas, calculate the best score and return it as the assignment results.
        unassignedTas=self.detectUnassignedTas(rearrangedChromosome,tas)
        if len(unassignedTas)==0 :
            return rearrangedChromosome
        else:
            noneLocations,candidates=self.getCandidatesforNoneSlots(rearrangedChromosome,unassignedTas,courses,instructors,wi,wta)
            finalChromosome=self.fillChromosome(rearrangedChromosome,candidates,noneLocations,tas,courses,instructors,wi,wta)

            return finalChromosome

    # during the algorithm run, as stated in the report, we save each best score for each number of collisions.
    # at the end of the run, we select the minimum two number of collision chromosomes, make them collision free
    # compare their final score and return the one with the biggest score as the final assignment result.
    def giveLastDecision(self,be,tas,courses,instructors,empFactor,wi,wta):

        minNoOfCollision=-1

        for ber in range(len(be)):
            if be[ber][0] != 0:
                minNoOfCollision=ber
                break


        if minNoOfCollision==0:
            testChromosome1=be[minNoOfCollision][0]
        else:
            testChromosome1=self.collisionHandler(be[minNoOfCollision][0],tas,courses,instructors,empFactor,wi,wta)


        testChromosome2=self.collisionHandler(be[minNoOfCollision+1][0],tas,courses,instructors,empFactor,wi,wta)

        score1=self.score(testChromosome1,courses,instructors,empFactor,wi,wta)
        score2 = self.score(testChromosome2, courses, instructors, empFactor, wi, wta)

        if score1 >= score2:
            return testChromosome1
        else:
            return testChromosome2


# this is the class which will be working when the gui_noDB.py is clicked.
class runMain():

    def __init__(self):
        print('ok')


    def run(self, assignee_spreadsheet, authority_spreadsheet):

        instructor_id_list = []
        advisor_list = []
        ta_list = []
        teaches = []
        course_list = []


        tas = []
        instructors = []
        courses = []
        course_ids = []


        for t in ta_list:
            advisor = None

            for a in advisor_list:
                if a[1] == t[0]:
                    advisor = a[0]

            teaching_assistant = ta.TeachingAssistant(t[0], '', advisor, t[1])
            tas.append(teaching_assistant)


        for ins in instructor_id_list:
            advisee = []
            course_of_ins = []

            for a in advisor_list:
                if a[0] == ins[0]:
                    advisee.append(a[1])

            for course in teaches:
                for cou in course_list:
                    if course[0] == ins[0]:
                        if cou[0] == course[1]:
                            if course[1] not in course_ids:
                                new_course = co.Course(course[1], '', cou[1], course[0], cou[2])
                                courses.append(new_course)
                                course_ids.append(course[1])
                                course_of_ins.append(new_course)


            instructor = i.Instructor(ins[0], '', course_of_ins, advisee, ins[1])
            instructors.append(instructor)


        instructor_preferences, instructors, courses, course_list= e.main(authority_spreadsheet, 'High Authority')
        ta_preferences, tas = e.main(assignee_spreadsheet, 'Assignee')


        for ins_pref_insert in range(len(instructor_preferences)):

            temp_ins_id=instructor_preferences[ins_pref_insert].teacher_id

            for ins_iter in range(len(instructors)):
                if temp_ins_id == instructors[ins_iter].id :
                    instructors[ins_iter].preferences.append(instructor_preferences[ins_pref_insert])


        for ta_pref_insert in range(len(ta_preferences)):

            temp_ta_id=ta_preferences[ta_pref_insert].ta_id

            for tas_iter in range(len(tas)):
                if temp_ta_id == tas[tas_iter].id :
                    tas[tas_iter].preferences.append(ta_preferences[ta_pref_insert])


        # parameter initialization
        import Assignment_noDB as a
        populationSize = 200
        empFactor = 3
        wi = 1.7
        wta = 1.2
        numberOfIter = 10000
        cloningPercentage = 0.1
        crossoverPercantage = 0.8
        mutationPercentage = 0.1
        maxNoOfCollision = len(tas)/3

        # create an assignment object
        assignment = a.Assignment_noDB([], tas, courses, instructors)

        # check preferences before starting assignment
        assignment.check_preferences(courses)

        # create domains for each task
        domain = assignment.createDomain(assignment.ta_list, assignment.course_list, assignment.instructor_list)

        # initialize the population
        initialPopulation = assignment.initialize(populationSize, assignment.course_list, domain, assignment.ta_list,maxNoOfCollision)

        # start the assignment process with the initialized population
        be = assignment.assign(initialPopulation, numberOfIter, cloningPercentage, crossoverPercantage,mutationPercentage, empFactor, wi, wta, maxNoOfCollision, assignment.ta_list,assignment.course_list, assignment.instructor_list, domain)

        # given two chromosomes with the minimum collisions, convert them into zero collision version and return the highest score one as the result
        finalAssignmentChromosome = assignment.giveLastDecision(be, assignment.ta_list, assignment.course_list,assignment.instructor_list, empFactor, wi, wta)

        # pass the results of the final assignment chromosome to the user interface
        result2, dictionary, taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per = assignment.showStats(finalAssignmentChromosome,courses,instructors,tas)
        course_list = []
        for c in courses:
            course_list.append([c.id, c.ta_need])

        return course_list, tas, instructors, taStat, instructorStat, tot_ta_need_per,tot_ta_pref_per, result2, dictionary




def main():

    r = runMain()
    result, result2 = r.run()
    print(result)
    print(result2)

if __name__ == '__main__':
	main()





