import re

dateRegex = re.compile(r"(?P<day>\d\d?) (?P<month>[a-zśćź]*) (?P<year>202[01]) (?P<hour>\d\d?:\d\d)", re.MULTILINE)
linkRegex = re.compile(r"https://pwr-edu\.zoom\.us/j/.*", re.MULTILINE)


class String_Handler:
    def month_string_to_number(self, string):
        m = {
            'stycznia': 1,
            'lutego': 2,
            'marca': 3,
            'kwietnia': 4,
            'maja': 5,
            'czerwca': 6,
            'lipca': 7,
            'sierpnia': 8,
            'września': 9,
            'października': 10,
            'listopada': 11,
            'grudnia': 12
            }

        try:
            out = m[string]
            return out
        except:
            print("[ERROR] couldn't convert month", string, "to number")

    def get_dates(self, mails):
        data = []
        for mail in mails:
            found = linkRegex.findall(mail)
            if found is not None and len(found) > 0:
                link = found[0]
                print(link)
                found = dateRegex.search(mail)
                try:
                    string = found.group("year") + "-"

                    month = str(self.month_string_to_number(found.group("month")))
                    if len(month) == 1:
                        month = "0" + month

                    string += month + "-"

                    day = found.group("day")
                    if len(day) == 1:
                        day = "0" + day

                    string += day

                    string += "T"
                    hour = found.group("hour")
                    hour = hour[:1] + str(int(hour[1]) - 1) + hour[1 + 1:]

                    string += hour

                    '''
                    sometimes zoom meting is scheduled to start one minute
                    earlier or later than the actual date,
                    so I'm creating three different strings to check:
                    time - 1, time, time + 1 (minute)
                    '''

                    num = str(int(string[len(string) - 1]) - 1)
                    string2 = string[:len(string) - 1] + str(num)

                    num = str(int(string[len(string) - 1]) + 1)
                    string3 = string[:len(string) - 1] + str(num)

                    print(string)
                    print(string2)

                    data.append((string, string2, string3, link))
                except AttributeError:
                    print("NoneType")
                    #print(mail)
                    #print("\n\n")
        return data
