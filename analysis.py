# import pandas as pd
import csv

import itertools

from openpyxl import Workbook

def main():
    # create the lists and the dictionaries
    names = []
    dates = []
    date_num = {}
    date_topic_num = {}
    student_date_time = {}

    # add relevant data to the lists and dictionaries

    fill_lists_and_dicts(names, dates, date_num, date_topic_num, student_date_time)

    # analyze the movement of students

    analyze_movement(student_date_time, dates)

    # print(date_topic_num)

    get_averges(date_topic_num, dates)


def fill_lists_and_dicts(names, dates, date_num, date_topic_num, student_date_time):
    # fills with names, dates, and other data
    first_file = open('attendance_fully_updated.csv')
    next(first_file)
    for line in first_file:
        line = line.strip()
        parts = line.split(',')
        topic = parts[0]
        if 'Office Hours' not in topic:

            date = parts[2]
            if date not in dates:
                dates.append(date)
                current_dates_attendees = []

            time = parts[4]

            num_par = len(parts[6::])

            names_par = parts[6::]
            for name in names_par:
                name = remove_quotation(name.strip())
                name = remove_pronouns(name)
                name_par = (no_capitalized(name))
                if name != 'notstudent':
                    if name_par not in names:
                        names.append(name_par)
                    if name_par not in current_dates_attendees:
                        current_dates_attendees.append(name)

                        if name_par not in student_date_time:
                            smol_dict = {}
                            smol_dict[date] = time
                            student_date_time[name_par] = [smol_dict]
                        else:
                            if date not in student_date_time[name_par][-1]:
                                smol_dict = {}
                                smol_dict[date] = time
                                student_date_time[name_par].append(smol_dict)

                    else:
                        num_par -= 1

                else:
                    num_par -= 1

            if date not in date_num:
                date_num[date] = num_par
            else:
                date_num[date] += num_par

            if date not in date_topic_num:
                date_topic_num[date] = [num_par]
            else:
                date_topic_num[date].append(num_par)

    up_to_week_3 = ['09/14/2020', '09/16/2020', '09/18/2020', '09/21/2020', '09/23/2020', '09/25/2020', '09/28/2020',
                    '09/30/2020', '10/02/2020']
    percent_of_non_synchronous_viewers = 0.5
    second_file = open('UniqueViewsPanopto.csv')
    next(second_file)
    for line in second_file:
        line = line.strip()
        parts = line.split(',')
        date = parts[0]
        views = round(int(parts[1]) * percent_of_non_synchronous_viewers)

        if date in up_to_week_3:
            class_size = 422
        else:
            class_size = 414

        if len(date_topic_num[date]) == 3:
            date_topic_num[date].append(views)
        else:
            date_topic_num[date][-1] += views
            if date_num[date] + date_topic_num[date][-1] > class_size:
                date_topic_num[date][-1] = class_size - date_num[date]

    for date in date_topic_num:
        if date in up_to_week_3:
            class_size = 422
        else:
            class_size = 414
        attended = date_num[date] + date_topic_num[date][3]
        if attended >= class_size:
            date_topic_num[date].append(0)
        else:
            date_topic_num[date].append(class_size - attended)
    # print(date_topic_num)


def analyze_movement(student_date_time, dates):
    average_movement = {'8:30-8:30': 0, '8:30-11:30': 0, '8:30-2:30': 0, '8:30-PN': 0,
                        '11:30-8:30': 0, '11:30-11:30': 0, '11:30-2:30': 0, '11:30-PN': 0,
                        '2:30-8:30': 0, '2:30-11:30': 0, '2:30-2:30': 0, '2:30-PN': 0,
                        'PN-8:30': 0, 'PN-11:30': 0, 'PN-2:30': 0, 'PN-PN': 0}
    up_to_week_3 = ['09/14/2020', '09/16/2020', '09/18/2020', '09/21/2020', '09/23/2020', '09/25/2020', '09/28/2020',
                    '09/30/2020', '10/02/2020']

    for date in dates:
        # if date != '09/14/2020':
        if date not in up_to_week_3:
            # if date in up_to_week_3:
            #     movement = {'8:30-8:30': 0, '8:30-11:30': 0, '8:30-2:30': 0, '8:30-PN': 0,
            #                 '11:30-8:30': 0, '11:30-11:30': 0, '11:30-2:30': 0, '11:30-PN': 0,
            #                 '2:30-8:30': 0, '2:30-11:30': 0, '2:30-2:30': 0, '2:30-PN': 0,
            #                 'PN-8:30': 0, 'PN-11:30': 0, 'PN-2:30': 0, 'PN-PN': 0}
            #     total_students = 414
            # else:
            #     movement = {'8:30-8:30': 0, '8:30-11:30': 0, '8:30-2:30': 0, '8:30-PN': 0,
            #                 '11:30-8:30': 0, '11:30-11:30': 0, '11:30-2:30': 0, '11:30-PN': 0,
            #                 '2:30-8:30': 0, '2:30-11:30': 0, '2:30-2:30': 0, '2:30-PN': 0,
            #                 'PN-8:30': 0, 'PN-11:30': 0, 'PN-2:30': 0, 'PN-PN': 8}
            #     total_students = 422

            movement = {'8:30-8:30': 0, '8:30-11:30': 0, '8:30-2:30': 0, '8:30-PN': 0,
                        '11:30-8:30': 0, '11:30-11:30': 0, '11:30-2:30': 0, '11:30-PN': 0,
                        '2:30-8:30': 0, '2:30-11:30': 0, '2:30-2:30': 0, '2:30-PN': 0,
                        'PN-8:30': 0, 'PN-11:30': 0, 'PN-2:30': 0, 'PN-PN': 8}
            total_students = 414

            current_date_index = dates.index(date)
            # current_date = date
            past_date = dates[current_date_index - 1]

            for student in student_date_time:
                student_dates = []
                for day in student_date_time[student]:
                    day = day.keys()
                    for key in day:
                        student_dates.append(key)

                if date in student_dates:
                    student_current_index = student_dates.index(date)
                    current_class = student_date_time[student][student_current_index][date]
                else:
                    current_class = 'PN'
                if past_date in student_dates:
                    past_class = student_date_time[student][student_dates.index(past_date)][past_date]
                else:
                    past_class = 'PN'

                if past_class == '8:30':
                    if current_class == '8:30':
                        movement['8:30-8:30'] += 1
                    elif current_class == '11:30':
                        movement['8:30-11:30'] += 1
                    elif current_class == '2:30':
                        movement['8:30-2:30'] += 1
                    elif current_class == 'PN':
                        movement['8:30-PN'] += 1
                elif past_class == '11:30':
                    if current_class == '8:30':
                        movement['11:30-8:30'] += 1
                    elif current_class == '11:30':
                        movement['11:30-11:30'] += 1
                    elif current_class == '2:30':
                        movement['11:30-2:30'] += 1
                    elif current_class == 'PN':
                        movement['11:30-PN'] += 1
                elif past_class == '2:30':
                    if current_class == '8:30':
                        movement['2:30-8:30'] += 1
                    elif current_class == '11:30':
                        movement['2:30-11:30'] += 1
                    elif current_class == '2:30':
                        movement['2:30-2:30'] += 1
                    elif current_class == 'PN':
                        movement['2:30-PN'] += 1
                elif past_class == 'PN':
                    if current_class == '8:30':
                        movement['PN-8:30'] += 1
                    elif current_class == '11:30':
                        movement['PN-11:30'] += 1
                    elif current_class == '2:30':
                        movement['PN-2:30'] += 1
                    elif current_class == 'PN':
                        movement['PN-PN'] += 1
                # if date == '10/30/2020':
                #     print(movement)
            daily_averaged = {'8:30-8:30': movement['8:30-8:30'] / total_students,
                              '8:30-11:30': movement['8:30-11:30'] / total_students,
                              '8:30-2:30': movement['8:30-2:30'] / total_students,
                              '8:30-PN': movement['8:30-PN'] / total_students,
                              '11:30-8:30': movement['11:30-8:30'] / total_students,
                              '11:30-11:30': movement['11:30-11:30'] / total_students,
                              '11:30-2:30': movement['11:30-2:30'] / total_students,
                              '11:30-PN': movement['11:30-PN'] / total_students,
                              '2:30-8:30': movement['2:30-8:30'] / total_students,
                              '2:30-11:30': movement['2:30-11:30'] / total_students,
                              '2:30-2:30': movement['2:30-2:30'] / total_students,
                              '2:30-PN': movement['2:30-PN'] / total_students,
                              'PN-8:30': movement['PN-8:30'] / total_students,
                              'PN-11:30': movement['PN-11:30'] / total_students,
                              'PN-2:30': movement['PN-2:30'] / total_students,
                              'PN-PN': movement['PN-PN'] / total_students}
            total_class_transitions = 20
            average_movement['8:30-8:30'] += daily_averaged['8:30-8:30'] / total_class_transitions
            average_movement['8:30-11:30'] += daily_averaged['8:30-11:30'] / total_class_transitions
            average_movement['8:30-2:30'] += daily_averaged['8:30-2:30'] / total_class_transitions
            average_movement['8:30-PN'] += daily_averaged['8:30-PN'] / total_class_transitions
            average_movement['11:30-8:30'] += daily_averaged['11:30-8:30'] / total_class_transitions
            average_movement['11:30-11:30'] += daily_averaged['11:30-11:30'] / total_class_transitions
            average_movement['11:30-2:30'] += daily_averaged['11:30-2:30'] / total_class_transitions
            average_movement['11:30-PN'] += daily_averaged['11:30-PN'] / total_class_transitions
            average_movement['2:30-8:30'] += daily_averaged['2:30-8:30'] / total_class_transitions
            average_movement['2:30-11:30'] += daily_averaged['2:30-11:30'] / total_class_transitions
            average_movement['2:30-2:30'] += daily_averaged['2:30-2:30'] / total_class_transitions
            average_movement['2:30-PN'] += daily_averaged['2:30-PN'] / total_class_transitions
            average_movement['PN-8:30'] += daily_averaged['PN-8:30'] / total_class_transitions
            average_movement['PN-11:30'] += daily_averaged['PN-11:30'] / total_class_transitions
            average_movement['PN-2:30'] += daily_averaged['PN-2:30'] / total_class_transitions
            average_movement['PN-PN'] += daily_averaged['PN-PN'] / total_class_transitions
    # print(average_movement)

    col_1 = [average_movement['8:30-8:30'], average_movement['11:30-8:30'], average_movement['2:30-8:30'],
             average_movement['PN-8:30']]
    col_2 = [average_movement['8:30-11:30'], average_movement['11:30-11:30'], average_movement['2:30-11:30'],
             average_movement['PN-11:30']]
    col_3 = [average_movement['8:30-2:30'], average_movement['11:30-2:30'], average_movement['2:30-2:30'],
             average_movement['PN-2:30']]
    col_4 = [average_movement['8:30-PN'], average_movement['11:30-PN'], average_movement['2:30-PN'],
             average_movement['PN-PN']]
    normalized_col_1 = normalize_col(col_1, get_col_sum(col_1))
    normalized_col_2 = normalize_col(col_2, get_col_sum(col_2))
    normalized_col_3 = normalize_col(col_3, get_col_sum(col_3))
    normalized_col_4 = normalize_col(col_4, get_col_sum(col_4))
    # print(normalized_col_1[0], normalized_col_2[0], normalized_col_3[0], normalized_col_4[0])
    # print(normalized_col_1[1], normalized_col_2[1], normalized_col_3[1], normalized_col_4[1])
    # print(normalized_col_1[2], normalized_col_2[2], normalized_col_3[2], normalized_col_4[2])
    # print(normalized_col_1[3], normalized_col_2[3], normalized_col_3[3], normalized_col_4[3])
    print(student_date_time['benjamen gao'])



    # df = pd.DataFrame(data=student_date_time, index=[0])
    #
    # df = (df.T)
    #
    # print(df)
    #
    # df.to_excel('dict1.xlsx')

    # with open('output.csv', 'wb') as output:
    #     writer = csv.writer(output)
    #     for key, value in student_date_time.iteritems():
    #         writer.writerow([key, value])

    # testname = open('Book1.xlsx')
    # write_xls(testname, student_date_time)

def write_xls(filename, data):
    wb = Workbook(write_only=True)
    ws = wb.create_sheet()

    headers = list(set(itertools.chain.from_iterable(data)))
    ws.append(headers)

    for elements in data:
        ws.append([elements.get(h) for h in headers])

    wb.save(filename)


def remove_quotation(name):
    if name[0] == '"':
        name = name[1:]
    if name[-1] == '"':
        name = name[:-1]
    return name


def remove_pronouns(name):
    if '(' in name:
        first_index = name.index('(')
        if ')' in name:
            name = name[:first_index]
            return name.strip()
        return name
    return name


def no_capitalized(name):
    no_cap = name.lower()
    return no_cap


def get_col_sum(col):
    sum = 0
    for elem in col:
        sum += elem
    return sum


def normalize_col(col, sum):
    normalized_col = []
    for elem in col:
        normalized_col.append(elem / sum)
    return normalized_col


def get_averges(date_topic_num, dates):
    a_average = 0
    b_average = 0
    c_average = 0
    a_per = 0
    b_per = 0
    c_per = 0
    for b in range(3):
        for i in range(1, len(dates)):
            curr_date = dates[i]
            past_date = dates[i - 1]
            curr_class_att = date_topic_num[curr_date][b]
            past_class_att = date_topic_num[past_date][b]
            if b == 0:
                a_average += (curr_class_att - past_class_att) / 28
                a_per += ((curr_class_att - past_class_att) / 28) / past_class_att
            elif b == 1:
                b_average += (curr_class_att - past_class_att) / 28
                b_per += ((curr_class_att - past_class_att) / 28) / past_class_att
            elif b == 2:
                c_average += (curr_class_att - past_class_att) / 28
                c_per += ((curr_class_att - past_class_att) / 28) / past_class_att
    # print(a_average)
    # print(b_average)
    # print(c_average)
    # print(a_per * 100)
    # print(b_per * 100)
    # print(c_per * 100)

    # print(date_topic_num)


if __name__ == '__main__':
    main()