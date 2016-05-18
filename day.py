class Day(object):

    def __init__(self, day_in, rain_in, sun_in, temp_in):
        self.day = day_in #day of the year 365 day calender
        self.rain = rain_in #daily percipitation inches
        self.sun = sun_in #hours of sun in the day
        self.temp = temp_in #daily average temperature