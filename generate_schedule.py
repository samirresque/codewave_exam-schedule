from new_exam import *
import sys
import random

class Schedule_Generate():
    #all_courses = ['A','B','C', 'D', 'E', 'F', 'G']
    #days = ['Sun', 'Mon', 'Tue']
    exam_days = []
    all_courses = []
    adjacency = dict()
    domains = dict()
    def __init__(self, exam):
        self.exam = exam
        self.adjacency = self.exam.adjacency()
        self.all_courses = self.exam.courses()
        self.exam_days = self.exam.days()

        for each_course in self.all_courses:
            self.domains[each_course] = set(self.exam_days)

    def solve(self):
        """
        Solve the CSP using arc consistency and backtracking.
        """
        if not self.arc_consistency():
            return None
        return self.backtrack(dict())

    def revise(self, course_1, course_2):
        """
        Make course_1 arc-consistent with course_2.
        Remove values from `self.domains[course_1]` if they are not consistent
        with any value in `self.domains[course_2]`.
        """
        revised = False
        if (course_1, course_2) in self.adjacency and self.adjacency[(course_1, course_2)] == 1:
            for day_1 in self.domains[course_1].copy():
                conflict = True  # Assume there's no valid assignment initially
                for day_2 in self.domains[course_2]:
                    if day_1 != day_2:  # Courses can be scheduled on different days
                        conflict = False
                        break
                if conflict:
                    self.domains[course_1].remove(day_1)
                    revised = True
        return revised

    def arc_consistency(self, arcs=None):
        """
        Enforce arc consistency for all arcs.
        """
        queue = []
        if arcs is None:
            for course in self.domains:
                neighbors = self.exam.neighbors(course)
                for n in neighbors:
                    queue.append((course, n))
        else:
            queue = arcs

        while queue:
            (course_1, course_2) = queue.pop(0)
            if self.revise(course_1, course_2):
                if len(self.domains[course_1]) == 0:
                    return False  # Inconsistent, no solution
                neighbors = self.exam.neighbors(course_1)
                for neighbor in neighbors:
                    if neighbor != course_2:
                        queue.append((neighbor, course_1))
        return True

    def assignment_complete(self, assignment):
        """
        Check if the assignment is complete (all courses are assigned a day).
        """
        return all(course in assignment for course in self.all_courses)

    def consistent(self, assignment):
        """
        Return True if the assignment does not violate any constraints:
        no adjacent courses should be scheduled on the same day.
        """
        for course_1 in assignment:
            for course_2 in self.exam.neighbors(course_1):
                # Check if both courses are scheduled on the same day
                if course_2 in assignment and assignment[course_1] == assignment[course_2]:
                    return False  # Conflict found
        return True  # No conflicts found


    def select_unassigned_variable(self, assignment):
        """
        Select an unassigned variable using the Minimum Remaining Values (MRV) heuristic.
        """
        unassigned_courses = [course for course in self.all_courses if course not in assignment]

        # Apply MRV Minimum Remaining Value heuristic: choose the course with the fewest possible values in its domain
        return min(unassigned_courses, key=lambda course: len(self.domains[course]))

    def order_domain_values(self, course, assignment):
        """
        Return the domain values ordered by Least Constraining Value (LCV) heuristic.
        """
        if course not in self.domains:
            return []

        def count_constraints(value):
            # Count how many values this value would rule out for neighboring courses
            return sum(
                value in self.domains[neighbor]
                for neighbor in self.exam.neighbors(course)
                if neighbor not in assignment
            )

        return sorted(self.domains[course], key=count_constraints)

    def backtrack(self, assignment):
        # Check if the assignment is complete
        if self.assignment_complete(assignment):
            return assignment

        # Select an unassigned variable
        unassigned_courses = self.select_unassigned_variable(assignment)
        course = random.choice(unassigned_courses)

        for day in self.domains[course]:
            new_assignment = assignment.copy()
            new_assignment[course] = day

            # Only proceed if the new assignment is consistent
            if self.consistent(new_assignment):
                result = self.backtrack(new_assignment)
                if result:
                    return result

        return None  # No valid assignment found

def main():
    #if len(sys.argv) != 3:  # Expecting 2 arguments + script name
        #sys.exit("Usage: python exam.py <courses_file> <days_file>")

    #courses_file = sys.argv[1]
    #days_file = sys.argv[2]

    exam = Course()
    node = Schedule_Generate(exam)
    assignment = node.solve()
    # result output
    if assignment is None:
        print("No solution.")
    else:
        # Create a dictionary to group courses by values
        grouped_courses = {}

        # Populate the new dictionary
        for course, value in assignment.items():
            if value not in grouped_courses:
                grouped_courses[value] = []
            grouped_courses[value].append(course)

        # Print the grouped courses
        for value, courses in grouped_courses.items():
            print(f"Value: {value}, Courses: {courses}")

if __name__ == "__main__":
    main()

