from bs4 import BeautifulSoup
import pandas as pd

class Courses():
    def __init__(self, course_page):
        self.soup = BeautifulSoup(course_page, 'html.parser')
        self.course_df = pd.DataFrame(data={
            'title': [],
            'id': [],
            'name': [],
            'cred': [],
            'offered': [],
            'prereq': [],
            'coreq': [],
            'antireq': [],
            'descr': []
        })
        self.course_df = self.course_df.set_index('title')
        self.course_iter()

    def course_iter(self):
        for center in self.soup.find_all('center'):
            table = center.table
            cur_row = table.tr

            # get the course title
            self.cur_course = cur_row.td.b.a['name']

            # this is so we only get courses available to cs students
            if (self.cur_course[3] == '0'):
                continue
            if (self.cur_course[3] in "123" and self.cur_course[2] != '1'):
                continue

            # # code for getting the course cred:
            # cred_strings = cur_row.td.b.strings
            # for string in cred_strings:
            #     cred = str(string)
            #     cred = cred[-4:]
            #     self.course_df.loc[self.cur_course,'cred'] = cred
            # since all courses should be 0.5 creds, it's kind of redundant...
            self.course_df.loc[self.cur_course,'cred']='0.50'

            # fill course id
            course_id = cur_row.td.next_sibling.string
            course_id = str(course_id)[-6:]
            self.course_df.loc[self.cur_course, 'id'] = course_id


            # fill course name
            cur_row = cur_row.next_sibling
            self.course_df.loc[self.cur_course, 'name'] = str(cur_row.td.string)

            # fill course description
            cur_row = cur_row.next_sibling
            descr_string = str(cur_row.td.string)
            if (descr_string[-1] == ']'):
                # if the offerings are listed with the description,
                # this parses the description for the offerings
                offering = ''
                while (descr_string[-1] != ':'):
                    if (descr_string[-1] in 'FWS'):
                        offering = descr_string[-1] + offering
                    descr_string = descr_string[:-1]
                while (descr_string[-1] != '['):
                    descr_string = descr_string[:-1]
                descr_string = descr_string[:-1]
                self.course_df.loc[self.cur_course, 'offered'] = offering
            self.course_df.loc[self.cur_course, 'descr'] = descr_string

            # the rest of the rows are misc notes, parsed by parse_notes
            for row in cur_row.next_siblings:
                self.notes_string = str(row.string)
                self.parse_notes()

    def parse_notes(self):
        if (not self.notes_string):
            return

        if (self.notes_string == 'None'):
            return

        first_char = self.notes_string[0]

        if (first_char == ' '):
            # skips white space in the beginning
            self.notes_string = self.notes_string[1:]
            self.parse_notes()

        elif (first_char == '['):
            # "[Notes: ... Offered: ...]"
            offering = ''
            note = self.notes_string
            while (note[-1] != ':'):
                if (note[-1] in 'FWS'):
                    offering = note[-1] + offering
                note = note[:-1]
            self.course_df.loc[self.cur_course, 'offered'] = offering
        
        elif (first_char == 'P'):
            # "Prereq: ..."
            self.course_df.loc[self.cur_course, 'prereq'] = self.notes_string[8:]

        elif (first_char == 'C'):
            # "Coreq: ..."
            self.course_df.loc[self.cur_course, 'coreq'] = self.notes_string[7:]
        
        elif (first_char == 'A'):
            # "Anitreq: ..."
            self.course_df.loc[self.cur_course, 'antireq'] = self.notes_string[9:]


        # PARSING OPTIONS SKIPPED:

        # elif (first_char == '(' and self.notes_string[1] == 'C'):
        #     # "(Cross-listed with ...)"
        #     
        
        # elif (first_char == 'D'):
        #     # "Department consent required"
        #     

        # elif (first_char == 'O'):
        #     # "Only offered online"
        #

        else:
            print("Parsing skipped: " + self.notes_string)


    def get_df(self):
        return self.course_df

    def save_to(self, save_path):
        self.course_df.to_csv(save_path)

    





