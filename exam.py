""" Exam has attributes:
    Variables: COURSES,
    variable domain values: days
    constraints: no students has a two or more exams on the same day """

import csv
import random

class Course():
    student_courses = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    exam_days = []
    def __init__(self):
        self.each_student_courses = [['A','B','C'], ['B','D','E'], ['C','E','F'], ['E','F','G']]
        self.exam_days = ['Sun', 'Mon', 'Tue']


    def days(self):
        return self.exam_days

    def courses(self):
        return self.student_courses



    #def read_student_courses(self):
        # Open the CSV file for reading
        #with open(self.each_student_courses, mode='r', newline='') as file:
            # Use the csv reader to parse the file
            #csv_reader = csv.reader(file)

            # Read each row in the file and store it in the list
            #for row in csv_reader:
                # First element is the list of courses
                #courses = row[0].split(',')  # Splitting courses if comma-separated
                #self.student_courses.append(courses)

        #return self.student_courses

    #def read_days(self):

        # Open the CSV file for reading
        #with open(self.days, mode='r', newline='') as file:
            # Use the csv reader to parse the file
            #csv_reader = csv.reader(file)

            # Read each row in the file and store it in the list
            #for row in csv_reader:

                #days = row[0].split(',')  # Splitting courses if comma-separated
                #self.exam_days.append(days)
            #flattened_days = [each_day for each_day in self.exam_days for each_day in each_day]
            #return flattened_days

    # make a list of adjacent courses to check the adjacency
    def adjacency(self):
        self.adjacent = dict()
        for each_student_course in self.each_student_courses:
            for course_1 in each_student_course:
                for course_2 in each_student_course:
                    if course_1 == course_2:
                        continue
                    self.adjacent[(course_1, course_2)] = 1 # forms an edge
                    self.adjacent[(course_2, course_1)] = 1
        return self.adjacent

    def neighbors(self, course):
        """
        Given a course, return the set of adjacent courses (those that cannot be scheduled on the same day).
        """
        neighbors = []
        for (course_1, course_2) in self.adjacent:
            if course_1 == course:
                neighbors.append(course_2)
        return neighbors















