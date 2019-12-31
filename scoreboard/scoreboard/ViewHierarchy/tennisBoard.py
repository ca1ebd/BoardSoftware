from rgbViews import *
import json


class TennisBoard:

    def __init__(self, rootView, defaults=None):
        self.__rootView__ = rootView

        if defaults==None:
            #set default values here
            defaults = {
                "homeScore": "00",
                "awayScore": "00",
                "hs1": "0",
                "hs2": "0",
                "hs3": "0",
                "as1": "0",
                "as2": "0",
                "as3": "0",
            }

        # Views

        # self.awayScore = RGBLabel(self.__rootView__, 0, 12, defaults["awayScore"], TextStyle.IMAGE)

        # self.homeScore = RGBLabel(self.__rootView__, 60, 12, defaults["homeScore"], TextStyle.IMAGE)
        # defAway = defaults["awayColor"]
        # defHome = defaults["homeColor"]
        # self.awayLabel.setColor(graphics.Color(defAway["R"], defAway["G"], defAway["B"]))
        # self.homeLabel.setColor(graphics.Color(defHome["R"], defHome["G"], defHome["B"]))
        # self.clockIndicator = Clock(self.__rootView__, 33, 38, defSeconds=defaults['timeSeconds'])
        # self.s1_indicator = PeriodIndicator(self.__rootView__, 43, 0, 'S', defPeriod=defaults['period'])

        #top labels
        row_margin = 4
        top_row_height = 10
        second_third_row_height = 13

        first_row_y_pos = 0
        second_row_y_pos = top_row_height + row_margin
        third_row_y_pos = second_row_y_pos + second_third_row_height + row_margin

        game_x = 15
        s_width = 16
        s_x = game_x + 33
        self.game_label = RGBLabel(self.__rootView__, game_x, first_row_y_pos, "GAME")
        self.s1_label = RGBLabel(self.__rootView__, s_x, first_row_y_pos, "S1")
        self.s2_label = RGBLabel(self.__rootView__, s_x + s_width, first_row_y_pos, "S2")
        self.s3_label = RGBLabel(self.__rootView__, s_x + 2*s_width, first_row_y_pos, "S3")



        #first col
        self.homeLabel = RGBLabel(self.__rootView__, 2, second_row_y_pos, "H", font_path="../../fonts/10x20.bdf", font_y_offset=13)
        self.awayLabel = RGBLabel(self.__rootView__, 2, third_row_y_pos, "G", font_path="../../fonts/10x20.bdf", font_y_offset=13)

        #home scores
        self.home_game_score = RGBLabel(self.__rootView__, 18, second_row_y_pos, defaults['homeScore'], font_path="../../fonts/10x20.bdf", font_y_offset=13)
        self.home_set1_label = RGBLabel(self.__rootView__, s_x+2, second_row_y_pos, defaults['hs1'], font_path="../../fonts/10x20.bdf", font_y_offset=13)
        self.home_set2_label = RGBLabel(self.__rootView__, s_x + s_width + 2, second_row_y_pos, defaults['hs2'], font_path="../../fonts/10x20.bdf", font_y_offset=13)
        self.home_set3_label = RGBLabel(self.__rootView__, s_x + 2*s_width + 2, second_row_y_pos, defaults['hs3'],
                                        font_path="../../fonts/10x20.bdf", font_y_offset=13)

        #away scores
        self.away_game_score = RGBLabel(self.__rootView__, 18, third_row_y_pos, defaults['awayScore'],
                                        font_path="../../fonts/10x20.bdf", font_y_offset=13)
        self.away_set1_label = RGBLabel(self.__rootView__, s_x + 2, third_row_y_pos, defaults['as1'],
                                        font_path="../../fonts/10x20.bdf", font_y_offset=13)
        self.away_set2_label = RGBLabel(self.__rootView__, s_x + s_width + 2, third_row_y_pos, defaults['as2'],
                                        font_path="../../fonts/10x20.bdf", font_y_offset=13)
        self.away_set3_label = RGBLabel(self.__rootView__, s_x + 2 * s_width + 2, third_row_y_pos, defaults['as3'],
                                        font_path="../../fonts/10x20.bdf", font_y_offset=13)

        self.set_ids = {
            "h1": self.home_set1_label,
            "h2": self.home_set2_label,
            "h3": self.home_set3_label,
            "a1": self.away_set1_label,
            "a2": self.away_set2_label,
            "a3": self.away_set3_label,
        }

        #set colors
        inner = [self.home_game_score, self.home_set1_label, self.home_set2_label, self.home_set3_label, self.away_game_score, self.away_set1_label, self.away_set2_label, self.away_set3_label]
        for label in inner:
            label.setColor(graphics.Color(0, 255, 0))

        top_row = [self.game_label, self.s1_label, self.s2_label, self.s3_label]
        for label in top_row:
            label.setColor(graphics.Color(255, 255, 0))

        self.away_game_score.setColor(graphics.Color(0, 255, 255))
        self.home_game_score.setColor(graphics.Color(0, 255, 255))

        self.homeLabel.setColor(graphics.Color(255, 255, 0))
        self.awayLabel.setColor(graphics.Color(255, 255, 0))

        # self.homeLabel.setFont()

    def setSetScore(self, dataStr):
        data_parse = json.loads(dataStr)
        chosen_label = self.set_ids[data_parse['setID']]
        #make sure that only single digit given
        assert len(data_parse['score']) == 1
        chosen_label.setText(data_parse['score'])

    def setHomeScore(self, dataStr):
        #make sure that we aren't trying to set text too big
        assert len(dataStr) <= 2

        # TODO make app send correct data instead of fixing here
        if len(dataStr) == 1:
            self.home_game_score.setText("0" + dataStr)
        else:
            self.home_game_score.setText(dataStr)

    def setAwayScore(self, dataStr):
        #make sure that we aren't trying to set text too big
        assert len(dataStr) <= 2

        # TODO make app send correct data instead of fixing here
        if len(dataStr) == 1:
            self.away_game_score.setText("0" + dataStr)
        else:
            self.away_game_score.setText(dataStr)

    def setHomeColor(self, dataStr):
        colorObject = json.loads(dataStr)
        red = int(colorObject["R"])
        green = int(colorObject["G"])
        blue = int(colorObject["B"])
        self.homeLabel.setColor(graphics.Color(red, green, blue))

    def setAwayColor(self, dataStr):
        colorObject = json.loads(dataStr)
        red = int(colorObject["R"])
        green = int(colorObject["G"])
        blue = int(colorObject["B"])
        self.awayLabel.setColor(graphics.Color(red, green, blue))

if __name__ == "__main__":
    rootView = RGBBase()
    board = TennisBoard(rootView)
    #test functionality
    # time.sleep(10)
    # board.set_set_score("{\"setID\":\"h1\",\"score\":\"3\"}")
    # board.set_set_score("{\"setID\":\"h2\",\"score\":\"2\"}")
    # board.set_set_score("{\"setID\":\"h3\",\"score\":\"1\"}")
    # board.set_set_score("{\"setID\":\"a1\",\"score\":\"6\"}")
    # board.set_set_score("{\"setID\":\"a2\",\"score\":\"5\"}")
    # board.set_set_score("{\"setID\":\"a3\",\"score\":\"4\"}")
    # board.setHomeScore("15")
    # board.setAwayScore("30")
    while True:
        pass