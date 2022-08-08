def main():
    # create lists and dicts
    data = {}
    names = {}
    dates = []
    date_num = {}
    panopto_viewers = {}
    student_date_time = {}
    date_num_participants = {}
    add_data(data, names, dates, date_num, panopto_viewers, student_date_time, date_num_participants)
    get_averages(data)
    organize_movement(student_date_time, dates, date_num)


def add_data(data, names, dates, date_num, panopto_viewers, student_date_time, date_num_participants):
    # precondition: Empty lists and dictionaries are entered to be filled in.
    # postcondition: The filled lists and dictionaries are returned to be analyzed.
    # creates a list of people that are not students
    non_students = ['Sean Thomas Cotner', "Sara's iPad", 'Sheela Devadas', 'Jimmy He', 'Jonathan Richard Love',
                    'Sarah Isabel McConnell', 'dat nguyen', 'Mark Perlman', 'Arpon Paul Raksit', 'nhi truong vu',
                    'Bogdan Zavyalov', 'Christine Taylor', 'Sara Venkatesh', 'Jonathan Love (he/him)', 'Sarah McConnell (she/her)']
    # start of add_data proper

    first_filename = 'attendance_nums.csv'
    first_file = open(first_filename)   # calculates total Panopto viewers per day
    next(first_file)
    for line in first_file:
        line = line.strip()
        parts = line.split(',')
        date = parts[2]
        views = int(parts[4])
        # if date not in panopto_viewers:
        #     panopto_viewers[date] = views
        # else:
        #     panopto_viewers[date] += views

    filename = 'attendance_full.csv'
    file = open(filename)  # opens and reads the file
    next(file)
    for line in file:
        date_time = {}
        line = line.strip()
        parts = line.split(',')
        topics = parts[0]

        # only adds classes that are not office hours
        if 'Office Hours' not in topics:
            # gets the total number of participants in a given class
            participants = int((parts[5]))
            if 'Math51 8:30 Lectures' in topics:
                participants -= 2  # takes off Professor Taylor and a TA
            elif 'Math51 11:30 Lectures' in topics:
                participants -= 2  # takes off Professor Taylor and a TA
            elif 'Math51 2:30 Lectures' in topics:
                participants -= 3  # takes off Professor Venkatesh, her iPad, and a TA
            if topics not in data:
                data[topics] = [participants]
            else:
                data[topics].append(participants)

            # identifies each student in the given class
            participants_in_curr_class = parts[6::]
            participants_ID = []
            for participant in participants_in_curr_class:
                if participant != '':
                    participant = participant.strip()
                    if '"' in participant:
                        if '"' == participant[0]:
                            participant = participant[1::]
                        else:
                            participant = participant[0:-1]
                    if participant not in names:
                        names[participant] = []
                if participant not in non_students:
                    participants_ID.append(participant)

            # gets all the dates of the classes
            date = parts[2]
            if date not in dates:
                dates.append(date)

            # gets the corresponding time of the class i.e 8:30, 11:30, or 2:30
            time = parts[4]  # what time the classes start

            # gets the date and number of participants in each class
            time_num_attendees = {}
            if date not in date_num_participants:
                time_num_attendees[time] = participants
                date_num_participants[date] = [time_num_attendees]
            else:
                time_num_attendees[time] = participants
                date_num_participants[date].append(time_num_attendees)

            # Identifies which classes a student has attended, but only the first class
            for student in participants_ID:
                date_time[date] = [time]
                if student not in student_date_time:
                    student_date_time[student] = [date_time]
                else:
                    if date in student_date_time[student][-1]:
                        participants -= 1
                        # if time not in student_date_time[student][-1][date]:
                        #     student_date_time[student][-1][date].append(time)
                    else:
                        student_date_time[student].append(date_time)
            if date in date_num:
                date_num[date].append(participants)
                # if len(date_num[date]) == 3:
                #     panopto_views = panopto_viewers[date]
                #     date_num[date].append(panopto_views)
            else:
                date_num[date] = [participants]
    # print(len(student_date_time['benjamen gao']))
    # print(len(date_num))
    # smol_list = []
    # for name in student_date_time:
    #     if len(student_date_time[name]) < 4:
    #         smol_list.append(name)
    # print(smol_list)
    # print(date_num_participants)

    filename = 'UniqueViewsPanopto.csv'
    file = open(filename)
    next(file)
    for line in file:
        line = line.strip()
        parts = line.split(',')
        date = parts[0]
        views = int(parts[1])
        if len(date_num[date]) == 3:
            date_num[date].append(views)
        else:
            date_num[date][3] += views

    for date in date_num:
        attend_total = date_num[date][0] + date_num[date][1] + date_num[date][2] + date_num[date][3]
        if attend_total > 430:
            non_attend = 0
        else:
            non_attend = 430 - attend_total
        date_num[date].append(non_attend)

    print(len(date_num))
    print(len(student_date_time['benjamen gao']))


def get_averages(data):
    # precondition: passed in numeric data about users
    # postcondition: prints the averages, both the difference and percent totals
    difference_totals = {}
    percent_totals = {}
    for topic in data:
        if len(data[topic]) > 21:    # only evaluates lectures
            difference = 0
            percentages = 0
            for i in range(len(data[topic]) - 1):
                difference += (data[topic][i + 1] - data[topic][i])
                print(topic, difference)
                percentages += ((data[topic][i + 1] - data[topic][i]) / data[topic][i])
            average_difference = difference / (len(data[topic]) - 1)
            average_percentage = 100 * percentages / (len(data[topic]) - 1)
            percent_totals[topic] = average_percentage
            difference_totals[topic] = average_difference
    # print("The average difference in participants is: " + str(difference_totals))
    # print("The average percentage difference in participants is: " + str(percent_totals))
    # print(data)
    # print(difference_totals)


def organize_movement(student_date_time, dates, date_num):
    averaged_movement = {'8:30-8:30': 0, '8:30-11:30': 0, '8:30-2:30': 0, '8:30-Panopto': 0, '11:30-8:30': 0,
                         '11:30-11:30': 0, '11:30-2:30': 0, '11:30-Panopto': 0, '2:30-8:30': 0, '2:30-11:30': 0,
                         '2:30-2:30': 0, '2:30-Panopto': 0, 'Panopto-8:30': 0, 'Panopto-11:30': 0, 'Panopto-2:30': 0,
                         'Panopto-Panopto': 0}
    normalized_movement = {'8:30-8:30': 0, '8:30-11:30': 0, '8:30-2:30': 0, '8:30-Panopto': 0, '11:30-8:30': 0,
                           '11:30-11:30': 0, '11:30-2:30': 0, '11:30-Panopto': 0, '2:30-8:30': 0, '2:30-11:30': 0,
                           '2:30-2:30': 0, '2:30-Panopto': 0, 'Panopto-8:30': 0, 'Panopto-11:30': 0, 'Panopto-2:30': 0,
                           'Panopto-Panopto': 0}
    up_to_week_three = ['9/14/2020', '9/16/2020', '9/18/2020', '9/21/2020', '9/23/2020', '9/25/2020', '9/28/2020',
                        '9/30/2020', '10/02/2020']
    for date in dates:
        # eight students dropped after week 3 so this removes those students from the pool
        if date in up_to_week_three:
            movement = {'8:30-8:30': 0, '8:30-11:30': 0, '8:30-2:30': 0, '8:30-Panopto': 0, '11:30-8:30': 0,
                        '11:30-11:30': 0, '11:30-2:30': 0, '11:30-Panopto': 0, '2:30-8:30': 0, '2:30-11:30': 0,
                        '2:30-2:30': 0, '2:30-Panopto': 0, 'Panopto-8:30': 0, 'Panopto-11:30': 0, 'Panopto-2:30': 0,
                        'Panopto-Panopto': 0}
        else:
            movement = {'8:30-8:30': 0, '8:30-11:30': 0, '8:30-2:30': 0, '8:30-Panopto': 0, '11:30-8:30': 0,
                        '11:30-11:30': 0, '11:30-2:30': 0, '11:30-Panopto': 0, '2:30-8:30': 0, '2:30-11:30': 0,
                        '2:30-2:30': 0, '2:30-Panopto': 0, 'Panopto-8:30': 0, 'Panopto-11:30': 0, 'Panopto-2:30': 0,
                        'Panopto-Panopto': 8}
        total_students = 0
        percent_movement = {'8:30-8:30': 0, '8:30-11:30': 0, '8:30-2:30': 0, '8:30-Panopto': 0, '11:30-8:30': 0,
                            '11:30-11:30': 0, '11:30-2:30': 0, '11:30-Panopto': 0, '2:30-8:30': 0, '2:30-11:30': 0,
                            '2:30-2:30': 0, '2:30-Panopto': 0, 'Panopto-8:30': 0, 'Panopto-11:30': 0, 'Panopto-2:30': 0,
                            'Panopto-Panopto': 0}
        curr_date_index = dates.index(date)
        if curr_date_index != 28:
            for student in student_date_time:
                if len(student_date_time[student]) > 3:
                    student_dates = []  # the dates that the student is in class
                    for elem in student_date_time[student]:
                        # print(elem)
                        keys = elem.keys()
                        for key in keys:
                            student_dates.append(key)
                    if date in student_dates:  # if the student is present in class, do this
                        index_curr = student_dates.index(date)
                        curr_class = student_date_time[student][index_curr][date][0]
                    else:  # otherwise, assume they watched Panopto video
                        curr_class = 'Panopto'
                    next_date = dates[curr_date_index + 1]
                    if next_date in student_dates:  # if the student was in class next class:
                        index_next = student_dates.index(next_date)
                        next_class = student_date_time[student][index_next][next_date][0]
                    else:  # otherwise, assume they watched Panopto video
                        next_class = 'Panopto'
                    # print(curr_class, next_class)
                    if curr_class == '8:30':
                        if next_class == '8:30':
                            movement['8:30-8:30'] += 1
                        elif next_class == '11:30':
                            movement['8:30-11:30'] += 1
                        elif next_class == '2:30':
                            movement['8:30-2:30'] += 1
                        elif next_class == 'Panopto':
                            movement['8:30-Panopto'] += 1
                    elif curr_class == '11:30':
                        if next_class == '8:30':
                            movement['11:30-8:30'] += 1
                        elif next_class == '11:30':
                            movement['11:30-11:30'] += 1
                        elif next_class == '2:30':
                            movement['11:30-2:30'] += 1
                        elif next_class == 'Panopto':
                            movement['11:30-Panopto'] += 1
                    elif curr_class == '2:30':
                        if next_class == '8:30':
                            movement['2:30-8:30'] += 1
                        elif next_class == '11:30':
                            movement['2:30-11:30'] += 1
                        elif next_class == '2:30':
                            movement['2:30-2:30'] += 1
                        elif next_class == 'Panopto':
                            movement['2:30-Panopto'] += 1
                    elif curr_class == 'Panopto':
                        if next_class == '8:30':
                            movement['Panopto-8:30'] += 1
                        elif next_class == '11:30':
                            movement['Panopto-11:30'] += 1
                        elif next_class == '2:30':
                            movement['Panopto-2:30'] += 1
                        elif next_class == 'Panopto':
                            movement['Panopto-Panopto'] += 1
                    total_students += 1
            counter = 1
            students_present = 0
            for move in movement:
                if counter in [1, 5, 9, 13]:
                    students_present = date_num[date][0]
                    counter += 1
                elif counter in [2, 6, 10, 14]:
                    students_present = date_num[date][1]
                    counter += 1
                elif counter in [3, 7, 11, 15]:
                    students_present = date_num[date][2]
                    counter += 1
                elif counter in [4, 8, 12, 16]:
                    students_present = date_num[date][3]
                    counter += 1
                percent_movement[move] = ((movement[move]) / students_present)
            for percentage_key in percent_movement:
                averaged_movement[percentage_key] += percent_movement[percentage_key]
    for percent_key in averaged_movement:
        normalized_movement[percent_key] = (averaged_movement[percent_key] / 28)
    row_1 = [normalized_movement['8:30-8:30'], normalized_movement['8:30-11:30'], normalized_movement['8:30-2:30'],
             normalized_movement['8:30-Panopto']]
    row_2 = [normalized_movement['11:30-8:30'], normalized_movement['11:30-11:30'], normalized_movement['11:30-2:30'],
             normalized_movement['11:30-Panopto']]
    row_3 = [normalized_movement['2:30-8:30'], normalized_movement['2:30-11:30'], normalized_movement['2:30-2:30'],
             normalized_movement['2:30-Panopto']]
    row_4 = [normalized_movement['Panopto-8:30'], normalized_movement['Panopto-11:30'],
             normalized_movement['Panopto-2:30'], normalized_movement['Panopto-Panopto']]
    sum_col_1 = row_1[0] + row_2[0] + row_3[0] + row_4[0]
    sum_col_2 = row_1[1] + row_2[1] + row_3[1] + row_4[1]
    sum_col_3 = row_1[2] + row_2[2] + row_3[2] + row_4[2]
    sum_col_4 = row_1[3] + row_2[3] + row_3[3] + row_4[3]
    col_1 = [row_1[0] / sum_col_1, row_2[0] / sum_col_1, row_3[0] / sum_col_1, row_4[0] / sum_col_1]
    col_2 = [row_1[1] / sum_col_2, row_2[1] / sum_col_2, row_3[1] / sum_col_2, row_4[1] / sum_col_2]
    col_3 = [row_1[2] / sum_col_3, row_2[2] / sum_col_3, row_3[2] / sum_col_3, row_4[2] / sum_col_3]
    col_4 = [row_1[3] / sum_col_4, row_2[3] / sum_col_4, row_3[3] / sum_col_4, row_4[3] / sum_col_4]
    normalized_row_1 = [col_1[0], col_2[0], col_3[0], col_4[0]]
    normalized_row_2 = [col_1[1], col_2[1], col_3[1], col_4[1]]
    normalized_row_3 = [col_1[2], col_2[2], col_3[2], col_4[2]]
    normalized_row_4 = [col_1[3], col_2[3], col_3[3], col_4[3]]

    # print('The matrix describing the composition of students in a class is the following:')
    # print(normalized_row_1)
    # print(normalized_row_2)
    # print(normalized_row_3)
    # print(normalized_row_4)

    # print(student_date_time)
    # print(student_date_time['benjamen gao'])


if __name__ == "__main__":
    main()