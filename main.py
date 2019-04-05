import pytesseract
import cv2


def image_read():

    # reads in an image from src and converts to greyscale
    img = cv2.imread("nhl.png")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # region of interest for the full scoreboard
    scoreboard = img[75:125, 125:850]

    # region of interest for the first team
    team_one = scoreboard[:, 55:220]

    # region of interest for the second team
    team_two = scoreboard[:, 300:475]

    # region of interest for the period/time
    time_clock = scoreboard[:, 500:710]

    # scales the screenshot larger for better accuracy
    team_one = cv2.resize(team_one, None, fx=3, fy=3, interpolation= cv2.INTER_LINEAR)
    team_two = cv2.resize(team_two, None, fx=3, fy=3, interpolation= cv2.INTER_LINEAR)

    # binarizes the team ROIs for increased accuracy
    ret, t1_thresh = cv2.threshold(team_one, 175, 255, cv2.THRESH_BINARY)
    ret, t2_thresh = cv2.threshold(team_two, 175, 255, cv2.THRESH_BINARY)

    # creates an array [TEAM NAME, SCORE] for the teams
    # and              [PERIOD, TIME LEFT] for the game time
    # this part is kind of gooky because it sometimes reads 0 as Q
    # so I want to eventually train tesseract on the game font
    team_one_score = pytesseract.image_to_string(t1_thresh).replace('Q', 'O').split()
    team_two_score = pytesseract.image_to_string(t2_thresh).replace('Q', 'O').split()
    game_time = pytesseract.image_to_string(time_clock).split()


    # below this line is useless, just testing shit to visualize whats going on
    print(team_one_score)
    print(team_two_score)
    print(game_time)

    cv2.imshow('hl', t1_thresh)
    cv2.imshow('h2', t2_thresh)
    cv2.imshow('team one', team_one)
    cv2.imshow('team two', team_two)
    cv2.imshow('time clock', time_clock)
    cv2.imshow('scoreboard', scoreboard)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


image_read()
