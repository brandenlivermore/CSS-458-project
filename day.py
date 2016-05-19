class Day(object):

    def __init__(self, day_in, rain_in, sun_in, temp_in):
        '''

        :param day_in: #day of the year 365 day calender
        :param rain_in: #daily precipitation inches
        :param sun_in:  #hours of sun in the day
        :param temp_in: #daily average temperature
        '''
        self.day = day_in
        self.rain = rain_in
        self.sun = sun_in
        self.temp = temp_in