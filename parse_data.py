import time


def parse_data_by_day(filename):

    with open(filename, encoding='utf8') as datafile:

        print("Reading in data...")

        line = datafile.readline()

        start = time.perf_counter()

        current_date = []

        day_data = []

        new_filename = ""

        counter = 1
        file_line = 1
        while line:

            if convert_to_bcd(line[0:10]) != False:

                if "Mon " in line[0:4] or "Tue " in line[0:4] or "Wed " in line[0:4] or "Thu " in line[0:4] or \
                        "Fri " in line[0:4] or "Sat " in line[0:4] or "Sun " in line[0:4]:

                    # This sets the current_date to the first line in the file
                    if counter == 1:

                        if len(day_data) > 0:

                            file = open(new_filename, "a", encoding='utf8')
                            file.write(''.join( x for x in day_data ))
                            file.close()

                            day_data.clear()

                        print("Current file line is", file_line)

                        #current_date.append(convert_to_bcd(line[0:28]))\
                        current_date = convert_to_bcd(line[0:10])
                        #current_date.pop(3)
                        #current_date.pop(3)

                        new_filename = convert_from_bcd(current_date)
                        new_filename = new_filename.replace(' ', '_') + '.txt'

                        print("Writing in file {}".format(new_filename))

                    if current_date == convert_to_bcd(line[0:10]):

                        # Write to new file for that date

                        day_data.append(line)

                        counter += 1

                    else:

                        print("Resetting counter, date is", convert_to_bcd(line[0:10]), "line is", line)

                        counter = 1

            file_line += 1

            line = datafile.readline()


def convert_to_bcd(date_string):

    temp_bcd_list = date_string.split()

    # print(temp_bcd_list)

    bcd_days = {'Sun': '0000 0001', 'Mon': '0000 0010', 'Tue': '0000 0011', 'Wed': '0000 0100', 'Thu': '0000 0101',
                'Fri': '0000 0110', 'Sat': '0000 0111'}

    bcd_months = {'Jan': '0000 0001', 'Feb': '0000 0010', 'Mar': '0000 0011', 'Apr': '0000 0100', 'May': '0000 0100',
                  'Jun': '0000 0110', 'Jul': '0000 0111', 'Aug': '0000 1000', 'Sep': '0000 1001', 'Oct': '0001 0000',
                  'Nov': '0001 0001', 'Dec': '0001 0010'}

    bcd_num = {'0': '0000', '1': '0001', '2': '0010', '3': '0011', '4': '0100', '5': '0101', '6': '0110', '7': '0111',
               '8': '1000', '9': '1001'}

    bcd = []

    try:

        if len(date_string) == 27:

            # Appends the day to BCD
            bcd.append(bcd_days[temp_bcd_list[0]])

            # Appends the month to BCD
            bcd.append(bcd_months[temp_bcd_list[1]])

            # Appends the date to BCD
            bcd.append(str(bcd_num[temp_bcd_list[2][0]] + ' ' + bcd_num[temp_bcd_list[2][1]]))

            # Appends the time to BCD
            bcd.append(str(bcd_num[temp_bcd_list[3][0]] + ' ' + bcd_num[temp_bcd_list[3][1]] + ' ' +
                           bcd_num[temp_bcd_list[3][3]] + ' ' + bcd_num[temp_bcd_list[3][4]] + ' ' +
                           bcd_num[temp_bcd_list[3][6]] + ' ' + bcd_num[temp_bcd_list[3][7]]))

            # Appends the year to BCD
            bcd.append(str(bcd_num[temp_bcd_list[5][0]] + ' ' + bcd_num[temp_bcd_list[5][1]] + ' ' +
                           bcd_num[temp_bcd_list[5][2]] + ' ' + bcd_num[temp_bcd_list[5][3]]))

        else:

            # Appends the day to BCD
            bcd.append(bcd_days[temp_bcd_list[0]])

            # Appends the month to BCD
            bcd.append(bcd_months[temp_bcd_list[1]])

            # Appends the date to BCD
            bcd.append(str(bcd_num[temp_bcd_list[2][0]] + ' ' + bcd_num[temp_bcd_list[2][1]]))

    except:

        # print("Error adding line", temp_bcd_list)
        return False

    #print(bcd)

    return bcd


def convert_from_bcd(bcd_data):

    bcd_days = {'0000 0001': 'Sun', '0000 0010': 'Mon', '0000 0011': 'Tue', '0000 0100': 'Wed', '0000 0101': 'Thu',
                '0000 0110': 'Fri', '0000 0111': 'Sat'}

    bcd_months = {'0000 0001': 'Jan', '0000 0010': 'Feb', '0000 0011': 'Mar', '0000 0100': 'Apr', '0000 0101': 'May',
                  '0000 0110': 'Jun', '0000 0111': 'Jul', '0000 1000': 'Aug', '0000 1001': 'Sep', '0001 0000': 'Oct',
                  '0001 0001': 'Nov', '0001 0010': 'Dec'}

    bcd_num = {'0000': '0', '0001': '1', '0010': '2', '0011': '3', '0100': '4', '0101': '5', '0110': '6', '0111': '7',
               '1000': '8', '1001': '9'}

    if len(bcd_data) == 4:

    # print(bcd_data)
        bcd_date = bcd_data[2].split()
        bcd_time = bcd_data[3].split()
        bcd_year = bcd_data[4].split()

        bcd_string = bcd_days[bcd_data[0]] + ' ' + \
                     bcd_months[bcd_data[1]] + ' ' + \
                     bcd_num[bcd_date[0]] + bcd_num[bcd_date[1]] + ' ' + \
                     bcd_num[bcd_time[0]] + bcd_num[bcd_time[1]] + ':' + bcd_num[bcd_time[2]] + bcd_num[bcd_time[3]] + ':' \
                     + bcd_num[bcd_time[4]] + bcd_num[bcd_time[5]] + ' ' \
                     + bcd_num[bcd_year[0]] + bcd_num[bcd_year[1]] + bcd_num[bcd_year[2]] + bcd_num[bcd_year[3]]

    else:

        bcd_date = bcd_data[2].split()

        bcd_string = bcd_days[bcd_data[0]] + ' ' + \
                     bcd_months[bcd_data[1]] + ' ' + \
                     bcd_num[bcd_date[0]] + bcd_num[bcd_date[1]]

    return bcd_string


#convert_from_bcd( convert_to_bcd("Mon Feb 28 11:12:11 EST 2020") )

parse_data_by_day("G:/Downloads/twitter-data-timpestamped (2).txt")
