import os
import re
import csv
import datetime
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET
import math

class Winner:
    def __init__(self, winner_driver):
        if not (winner_driver is None):
            self.Vorname = winner_driver.Vorname
            self.Nachname = winner_driver.Nachname
            self.Nummer = winner_driver.Nummer
            self.Team = winner_driver.Team
            self.winning_team = self.get_team_short()
            self.Nation = winner_driver.Nation
            self.Overall = winner_driver.Overall
            self.Stammfahrer = winner_driver.Stammfahrer
            self.finish_time = winner_driver.finish_time

    def get_team_short(self):
        if(self.Team == "Toyota F1 Team"):
            return "TOYOTA"
        if(self.Team == "Hugo Bros BMW Williams"):
            return "WILLIAMS"
        if(self.Team == "Scuderia Toro Rosso"):
            return "TORO ROSSO"
        if(self.Team == "Alpine F1 Team"):
            return "ALPINE"
        if(self.Team == "Mercedes AMG"):
            return "MERCEDES"
        if(self.Team == "Scuderia Ferrari"):
            return "FERRARI"
        if(self.Team == "McLaren F1 Team"):
            return "MCLAREN"
        if(self.Team == "LUNZiT Red Bull Racing"):
            return "RED BULL"
        if(self.Team == "Jordan Grand Prix"):
            return "JORDAN"
        if(self.Team == "Cadillac F1 Team"):
            return "CADILLAC"
        if(self.Team == "Audi F1 Team"):
            return "AUDI"
        if(self.Team == "Reserve"):
            return "ERSATZ"

class Driver:
    def __init__(self, driver_data=[]):
        if not (driver_data == []):
            self.Vorname = driver_data[0]
            self.Nachname = driver_data[1]
            self.Nummer = driver_data[2]
            self.Team = driver_data[3]            
            self.Nation = driver_data[4]
            self.Overall = driver_data[5]
            self.Stammfahrer = driver_data[6]
            self.finish_time = ""
            self.fastest_lap = ""
            self.penalty = None

    def get_driver_name(self):
        return self.Vorname + " " + self.Nachname

    def get_team_short(self):
        if(self.Team == "Toyota F1 Team"):
            return "TOYOTA"
        if(self.Team == "Hugo Bros BMW Williams"):
            return "WILLIAMS"
        if(self.Team == "Scuderia Toro Rosso"):
            return "TORO ROSSO"
        if(self.Team == "Alpine F1 Team"):
            return "ALPINE"
        if(self.Team == "Mercedes AMG"):
            return "MERCEDES"
        if(self.Team == "Scuderia Ferrari"):
            return "FERRARI"
        if(self.Team == "McLaren F1 Team"):
            return "MCLAREN"
        if(self.Team == "LUNZiT Red Bull Racing"):
            return "RED BULL"
        if(self.Team == "Jordan Grand Prix"):
            return "JORDAN"
        if(self.Team == "Cadillac F1 Team"):
            return "CADILLAC"
        if(self.Team == "Audi F1 Team"):
            return "AUDI"
        if(self.Team == "Reserve"):
            return "ERSATZ"

class fastest_lap:
    def __init__(self, Vorname="Vorname", Nachname="Nachname", Team="Test Team", lap_time="1000.0"):
        self.Vorname = Vorname
        self.Nachname = Nachname
        self.Team = Team
        self.lap_time = lap_time
        
    def get_laptime_formatted(self):
        td = datetime.timedelta(seconds=float(self.lap_time))
        # Format as mm:ss.SSS
        minutes, sec = divmod(td.total_seconds(), 60)
        return f"{int(minutes):02}:{sec:06.3f}"

#Setup Variables

width, height = 1920, 1080
y_offset = 65
first_name = 243 #310 unterseite erste Zeile
first_team_and_points = 232
position_text = 556
left_allignment = 620
name_size = 20
name_size_insta = 16
row_height = 42

fastest_lap_position = (556, 1006)
lastname_size = 30
flag_width = 40
flag_height = 26
flag_y_offset = 22
spacer = 10
team_logo_alignment = (1085,212)
team_logo_scaled = (40,40)
team_name_allignment = 1165
race_time_allignment = 1700
quali_time_allignment = 1820
overall_position = (-50, 100)

points_pos_x = 1811
position_size = 24

penalty_pos_x = 1590
quali_penalty_x = 1700
penalty_text_size = 15

winner_team_position = (86, 80)
winner_number_position = (450, 80)
winner_team_size = 55
winner_name_pos = (288, 815)
winner_name_size = 42

#winner = Winner([])
fastest_lap_driver = fastest_lap()

arrow_scale = (25,25)
driver_wm_arrow_x = 1592
team_wm_arrow_x = 1594

###### Drivers Championship
driver_wm_race_titel_position = (330, 130)
driver_wm_offset_x = 96
driver_wm_left_allignment_x = 312 + driver_wm_offset_x
driver_wm_first_row_lower = 286
driver_wm_first_name_y = driver_wm_first_row_lower - 10
driver_wm_position_x = 353
driver_wm_team_x = 950
driver_wm_team_y = (int) (driver_wm_first_row_lower - (row_height / 2))
driver_wm_team_logo = (driver_wm_team_x - 75, driver_wm_team_y - 20)
driver_wm_points_pos = (1575, (int) (driver_wm_first_row_lower - (row_height / 2)))
driver_wm_info_text_position = (350, 974)

###### Constructor Championship
team_wm_race_titel_position = (330, 85)
team_wm_offset_x = 75
team_wm_left_allignment_x = 312 + team_wm_offset_x
team_wm_first_row_lower = 247
team_wm_first_name_y = team_wm_first_row_lower - 10
team_wm_position_x = 340
team_wm_team_x = 1050
team_wm_team_y = (int) (team_wm_first_row_lower - (row_height / 2))
team_wm_team_logo = (team_wm_team_x - 75, team_wm_team_y - 20)
team_wm_points_pos = (1575, (int) (team_wm_first_row_lower - (row_height / 2)))
team_wm_info_text_position = (350, 1005)
team_wm_team_logo_scaled = (40,40)

# Load a font (optional: use default if you don't have one)
race_titel = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=34)
race_titel_insta = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=28)
race_classification = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=56)
regular = ImageFont.truetype("./fonts/Formula1-Regular_web.ttf", size=name_size)
insta = ImageFont.truetype("./fonts/Formula1-Regular_web.ttf", size=name_size_insta)
penalty_font = ImageFont.truetype("./fonts/Formula1-Regular_web.ttf", size=penalty_text_size)
position_font = ImageFont.truetype("./fonts/Formula1-Regular_web.ttf", size=24)
winner_team_font = ImageFont.truetype("./fonts/Formula1-Wide_web.ttf", size=winner_team_size)
winner_name_font = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=winner_name_size)
bold = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=lastname_size)
pos_bold = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=position_size)

#Insta format
insta_height = 1080
insta_width = 1080
insta_row_height = 45
insta_row_gap = 25
insta_position_text = 45
insta_y_offset = (insta_row_height + insta_row_gap)
insta_left_allignment = 100
insta_first_name = 218
insta_race_titel_pos =(30, 70)
insta_team_alignment = (520,int(230 - (insta_row_height / 2)))
team_logo_alignment = (1085,207)
insta_team_name_allignment = 540
insta_quali_time_allignment = 1040
insta_points_allignment = 1017
insta_quali_penalty_x = insta_width - (insta_width -  insta_quali_time_allignment) - 110
insta_racetime_alignment = 950
insta_race_penalty_pos = insta_racetime_alignment - 120
insta_fastest_lap_position = (insta_position_text, 1045)
insta_race_info_pos = 1060

### Arrays
xml_export = []
driver_config = []
team_config = []
rennergebnis = []
qualiergebnis = []
starting_grid = []
fastest_laps = []

name_rennen = "Name des Rennens"
current_race_number = 0

def create_rennergebnis_page_1(data, filename="output/rennergebnisse_seite1.png"):
    # Create a transparent base image (RGBA mode)  
    final_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # Fully transparent
    classment_transparent = Image.open("./images/Classement_background.png").convert("RGBA")
    background = Image.open("./images/Rennergebnis_Hintergrund.png").convert("RGBA")

    # Paste images onto the final image at specified positions
    mask = Image.new('L', classment_transparent.size, 200)  # 50% transparency
    final_image.paste(classment_transparent, (0, 0), mask)  # The third argument is the mask for transparency
    final_image.paste(background, (0, 0), background)  # The third argument is the mask for transparency
    draw = ImageDraw.Draw(final_image)

    # Draw Racetitel with semi-transparency
    draw.text((557, 100), name_rennen, font=race_titel, fill=(255, 255, 255, 255), anchor="lt")

    #Draw race winner
    winner_overall = Image.open("./overalls/" + winner.Overall).convert("RGBA")
    winner_overall = winner_overall.resize((680, 680))
    final_image.paste(winner_overall, overall_position, winner_overall)
    overall_fade = Image.open("./images/Winner_Vordergrund.png").convert("RGBA")
    final_image.paste(overall_fade, (0,0), overall_fade)
    
    #Winner rotated team text
    team_box = draw.textbbox((-100, -100), winner.winning_team, font=winner_team_font)
    temp_img = Image.new("RGBA", (team_box[2] - team_box[0], team_box[3] - team_box[1]), (0, 0, 0, 0))  # Big enough for horizontal text
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((0, 0), winner.winning_team, font=winner_team_font, fill=(255, 255, 255, 100), anchor="lt")

    # Rotate the temporary image 90 degrees counter-clockwise
    rotated_text = temp_img.rotate(90, expand=True)
    final_image.paste(rotated_text, winner_team_position, rotated_text)

    #Winner rotated number text
    team_box = draw.textbbox((-100, -100), winner.Nummer, font=winner_team_font)
    temp_img = Image.new("RGBA", (team_box[2] - team_box[0], team_box[3] - team_box[1]), (0, 0, 0, 0))  # Big enough for horizontal text
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((0, 0), winner.Nummer, font=winner_team_font, fill=(255, 255, 255, 100), anchor="lt")

    # Rotate the temporary image 90 degrees counter-clockwise
    rotated_text = temp_img.rotate(90, expand=True)
    final_image.paste(rotated_text, winner_number_position, rotated_text)
    
    ### Winner Name
    draw.text(winner_name_pos, winner.Nachname.upper(), font=winner_name_font, fill=(255, 255, 255, 255), anchor="mm")
    
    ### Fill Positions
    position = 0
    for driver in data:
        #Text zu CAPS

        
        # Draw the rest of row     
        bbox = draw.textbbox((-100, -100), driver.Vorname, font=regular)
        name_length = bbox[2] - bbox[0]
        
        if(position == 0):
            gained_points = "+25"
        elif(position == 1):
            gained_points = "+18"
        elif(position == 2):
            gained_points = "+15"
        elif(position == 3):
            gained_points = "+12"
        elif(position == 4):
            gained_points = "+10"
        elif(position == 5):
            gained_points = "+8"
        elif(position == 6):
            gained_points = "+6"
        elif(position == 7):
            gained_points = "+4"
        elif(position == 8):
            gained_points = "+2"
        elif(position == 9):
            gained_points = "+1"
        else:
            gained_points = "+0"

        
        if(position == 0):
            #Draw Position
            draw.text((position_text, first_name + (position * y_offset)), str(position + 1), font=position_font, fill=(0, 0, 0, 255), anchor="lb")            
            #Draw Flag
            flag_image = Image.open("./flags/" + driver.Nation + ".png").convert("RGBA")
            flag_image = flag_image.resize((flag_width, flag_height))
            final_image.paste(flag_image, (left_allignment, first_name + (position * y_offset) - flag_y_offset), flag_image)
            #Vorname
            draw.text((left_allignment + flag_width + spacer, first_name + (position * y_offset)), driver.Vorname, font=regular, fill=(0, 0, 0, 255), anchor="lb")
            #Nachname
            draw.text((left_allignment  + flag_width + spacer + name_length + spacer, first_name + (position * y_offset)), driver.Nachname.upper(), font=bold, fill=(0, 0, 0, 255), anchor="lb")
            #Teamname
            draw.text((team_name_allignment , first_team_and_points + (position * y_offset)), driver.Team.upper(), font=regular, fill=(0, 0, 0, 255), anchor="lm")
            #Team Logo
            logo = Image.open("./team_logos/" + get_team_logo(driver.Team)).convert("RGBA")
            logo = logo.resize(team_logo_scaled)
            # Paste images onto the final image at specified positions
            final_image.paste(logo, (team_logo_alignment[0], team_logo_alignment[1] + (position * y_offset)), logo)
            draw = ImageDraw.Draw(final_image)
            #Zeit
            td = datetime.timedelta(seconds=float(winner.finish_time))
            # Format as mm:ss.SSS
            minutes, sec = divmod(td.total_seconds(), 60)
            formatted = f"{int(minutes):02}:{sec:06.3f}"
            draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), formatted, font=regular, fill=(0, 0, 0, 255), anchor="rm")
            #Points
            draw.text((points_pos_x, first_team_and_points + (position * y_offset)), gained_points, font=pos_bold, fill=(0, 0, 0, 255), anchor="rm")
        else:
            #Draw Position
            draw.text((position_text, first_name + (position * y_offset)), str(position + 1), font=position_font, fill=(255, 255, 255, 255), anchor="lb")            
            #Draw Flag
            flag_image = Image.open("./flags/" + driver.Nation + ".png").convert("RGBA")
            flag_image = flag_image.resize((flag_width, flag_height))
            final_image.paste(flag_image, (left_allignment, first_name + (position * y_offset) - flag_y_offset), flag_image)
            #Vorname
            draw.text((left_allignment + flag_width + spacer, first_name + (position * y_offset)), driver.Vorname, font=regular, fill=(255, 255, 255, 255), anchor="lb")
            #Nachname
            draw.text((left_allignment  + flag_width + spacer + name_length + spacer, first_name + (position * y_offset)), driver.Nachname.upper(), font=bold, fill=(255, 255, 255, 255), anchor="lb")
            #Teamname
            draw.text((team_name_allignment , first_team_and_points + (position * y_offset)), driver.Team.upper(), font=regular, fill=(255, 255, 255, 255), anchor="lm")
            #Team Logo
            logo = Image.open("./team_logos/" + get_team_logo(driver.Team)).convert("RGBA")
            logo = logo.resize(team_logo_scaled)
            # Paste images onto the final image at specified positions
            final_image.paste(logo, (team_logo_alignment[0], team_logo_alignment[1] + (position * y_offset)), logo)
            draw = ImageDraw.Draw(final_image)
            #Zeit
            if (driver.finish_time == "DNS"):
                draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), "DNS", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            elif (driver.finish_time == "DNF"):
                draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), "DNF", font=regular, fill=(255, 255, 255, 255), anchor="rm")            
            elif ("Lap" in driver.finish_time):
                draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), driver.finish_time, font=regular, fill=(255, 255, 255, 255), anchor="rm")
            else:
                time_behind_leader = float(driver.finish_time) - float(winner.finish_time)
                if(time_behind_leader < 10):
                    draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), f"+0{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
                else:
                    draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), f"+{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            #Points
            draw.text((points_pos_x, first_team_and_points + (position * y_offset)), gained_points, font=pos_bold, fill=(255, 255, 255, 255), anchor="rm")
            #Penatly
            if (driver.penalty is not None):
                draw.text((penalty_pos_x , first_team_and_points + (position * y_offset)), ("+" + str(driver.penalty) + " sek") , font=penalty_font, fill=(255, 0, 0, 255), anchor="rm")


        # Update position for the next name
        position += 1

    ### Draw fastest Lap
    bbox = draw.textbbox((-100, -100), "FASTEST LAP", font=regular)
    name_length = bbox[2] - bbox[0]
    draw.text(fastest_lap_position, "FASTEST LAP", font=regular, fill=(255, 0, 255, 255), anchor="lm")
    draw.text((fastest_lap_position[0] + name_length + spacer + 5, fastest_lap_position[1]), f"{fastest_lap_driver.Nachname}     {fastest_lap_driver.Team}     {fastest_lap_driver.get_laptime_formatted()}", font=regular, fill=(255, 255, 255, 255), anchor="lm")

    # Save the final image
    final_image.save(filename, format="PNG")
    print("Image saved as "+ filename)

def create_rennergebnis_page_2(data, filename="output/rennergebnisse_seite2.png"):
    # Create a transparent base image (RGBA mode)  
    final_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # Fully transparent
    classment_transparent = Image.open("./images/Classement_background.png").convert("RGBA")
    background = Image.open("./images/Rennergebnis_Hintergrund_2.png").convert("RGBA")

    # Paste images onto the final image at specified positions
    mask = Image.new('L', classment_transparent.size, 200)  # 50% transparency
    final_image.paste(classment_transparent, (0, 0), mask)  # The third argument is the mask for transparency
    final_image.paste(background, (0, 0), background)  # The third argument is the mask for transparency
    draw = ImageDraw.Draw(final_image)

    # Draw Racetitel with semi-transparency
    draw.text((557, 100), name_rennen, font=race_titel, fill=(255, 255, 255, 255), anchor="lt")

    #Draw race winner
    winner_overall = Image.open("./overalls/" + winner.Overall).convert("RGBA")
    winner_overall = winner_overall.resize((680, 680))
    final_image.paste(winner_overall, overall_position, winner_overall)
    overall_fade = Image.open("./images/Winner_Vordergrund.png").convert("RGBA")
    final_image.paste(overall_fade, (0,0), overall_fade)
    
    #Winner rotated team text
    team_box = draw.textbbox((-100, -100), winner.winning_team, font=winner_team_font)
    temp_img = Image.new("RGBA", (team_box[2] - team_box[0], team_box[3] - team_box[1]), (0, 0, 0, 0))  # Big enough for horizontal text
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((0, 0), winner.winning_team, font=winner_team_font, fill=(255, 255, 255, 100), anchor="lt")

    # Rotate the temporary image 90 degrees counter-clockwise
    rotated_text = temp_img.rotate(90, expand=True)
    final_image.paste(rotated_text, winner_team_position, rotated_text)

    #Winner rotated number text
    team_box = draw.textbbox((-100, -100), winner.Nummer, font=winner_team_font)
    temp_img = Image.new("RGBA", (team_box[2] - team_box[0], team_box[3] - team_box[1]), (0, 0, 0, 0))  # Big enough for horizontal text
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((0, 0), winner.Nummer, font=winner_team_font, fill=(255, 255, 255, 100), anchor="lt")

    # Rotate the temporary image 90 degrees counter-clockwise
    rotated_text = temp_img.rotate(90, expand=True)
    final_image.paste(rotated_text, winner_number_position, rotated_text)
    
    ### Winner Name
    draw.text(winner_name_pos, winner.Nachname.upper(), font=winner_name_font, fill=(255, 255, 255, 255), anchor="mm")
    

    #Draw Winner in Tableau
    position = 0
    draw.text((position_text, first_name + (position * y_offset)), str(position + 1), font=position_font, fill=(0, 0, 0, 255), anchor="lb")            
    #Draw Flag
    flag_image = Image.open("./flags/" + winner.Nation + ".png").convert("RGBA")
    flag_image = flag_image.resize((flag_width, flag_height))
    final_image.paste(flag_image, (left_allignment, first_name + (position * y_offset) - flag_y_offset), flag_image)

    # Draw the rest of row     
    bbox = draw.textbbox((-100, -100), winner.Vorname, font=regular)
    name_length = bbox[2] - bbox[0]

    #Vorname
    draw.text((left_allignment + flag_width + spacer, first_name + (position * y_offset)), winner.Vorname, font=regular, fill=(0, 0, 0, 255), anchor="lb")    
    #Nachname
    draw.text((left_allignment  + flag_width + spacer + name_length + spacer, first_name + (position * y_offset)), winner.Nachname, font=bold, fill=(0, 0, 0, 255), anchor="lb")
    #Teamname
    draw.text((team_name_allignment , first_name + (position * y_offset)), winner.Team, font=regular, fill=(0, 0, 0, 255), anchor="lb")
    #Team Logo
    team_filename = get_team_logo(winner.Team)
    logo = Image.open("./team_logos/" + team_filename).convert("RGBA")
    logo = logo.resize(team_logo_scaled)
    # Paste images onto the final image at specified positions
    final_image.paste(logo, (team_logo_alignment[0], team_logo_alignment[1] + (position * y_offset)), logo)
    draw = ImageDraw.Draw(final_image)
    #Zeit
    td = datetime.timedelta(seconds=float(winner.finish_time))
    # Format as mm:ss.SSS
    minutes, sec = divmod(td.total_seconds(), 60)
    formatted = f"{int(minutes):02}:{sec:06.3f}"
    draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), formatted, font=regular, fill=(0, 0, 0, 255), anchor="rm")
    #Points
    draw.text((points_pos_x, first_team_and_points + (position * y_offset)), "+25", font=pos_bold, fill=(0, 0, 0, 255), anchor="rm")


    ### Fill Positions
    position = 1
    for driver in data:
        #Text zu CAPS

        
        # Draw the rest of row     
        bbox = draw.textbbox((-100, -100), driver.Vorname, font=regular)
        name_length = bbox[2] - bbox[0]
                
        gained_points = "+0"
        
        #Draw Position
        draw.text((position_text, first_name + (position * y_offset)), str(position + 12), font=position_font, fill=(255, 255, 255, 255), anchor="lb")            
        #Draw Flag
        flag_image = Image.open("./flags/" + driver.Nation + ".png").convert("RGBA")
        flag_image = flag_image.resize((flag_width, flag_height))
        final_image.paste(flag_image, (left_allignment, first_name + (position * y_offset) - flag_y_offset), flag_image)
        #Vorname
        draw.text((left_allignment + flag_width + spacer, first_name + (position * y_offset)), driver.Vorname, font=regular, fill=(255, 255, 255, 255), anchor="lb")
        #Nachname
        draw.text((left_allignment  + flag_width + spacer + name_length + spacer, first_name + (position * y_offset)), driver.Nachname.upper(), font=bold, fill=(255, 255, 255, 255), anchor="lb")
        #Teamname
        draw.text((team_name_allignment , first_team_and_points + (position * y_offset)), driver.Team, font=regular, fill=(255, 255, 255, 255), anchor="lm")
        #Team Logo
        logo = Image.open("./team_logos/" + get_team_logo(driver.Team)).convert("RGBA")
        logo = logo.resize(team_logo_scaled)
        # Paste images onto the final image at specified positions
        final_image.paste(logo, (team_logo_alignment[0], team_logo_alignment[1] + (position * y_offset)), logo)
        draw = ImageDraw.Draw(final_image)
        #Zeit
        if (driver.finish_time == "DNS"):
            draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), "DNS", font=regular, fill=(255, 255, 255, 255), anchor="rm")
        elif (driver.finish_time == "DNF"):
            draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), "DNF", font=regular, fill=(255, 255, 255, 255), anchor="rm")            
        elif ("Lap" in driver.finish_time):
            draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), driver.finish_time, font=regular, fill=(255, 255, 255, 255), anchor="rm")
        else:
            time_behind_leader = float(driver.finish_time) - float(winner.finish_time)
            if(time_behind_leader < 10):
                draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), f"+0{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            else:
                draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), f"+{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
        #Points
        draw.text((points_pos_x, first_team_and_points + (position * y_offset)), gained_points, font=pos_bold, fill=(255, 255, 255, 255), anchor="rm")
        #Penalty
        if (driver.penalty is not None):
            draw.text((penalty_pos_x , first_team_and_points + (position * y_offset)), ("+" + str(driver.penalty) + " sek") , font=penalty_font, fill=(255, 0, 0, 255), anchor="rm")
        # Update position for the next name
        position += 1

    ### Draw fastest Lap
    bbox = draw.textbbox((-100, -100), "FASTEST LAP", font=regular)
    name_length = bbox[2] - bbox[0]
    draw.text(fastest_lap_position, "FASTEST LAP", font=regular, fill=(255, 0, 255, 255), anchor="lm")
    draw.text((fastest_lap_position[0] + name_length + spacer + 5, fastest_lap_position[1]), f"{fastest_lap_driver.Nachname}     {fastest_lap_driver.Team}     {fastest_lap_driver.get_laptime_formatted()}", font=regular, fill=(255, 255, 255, 255), anchor="lm")


    

    # Save the final image
    final_image.save(filename, format="PNG")
    print("Image saved as "+ filename)

def create_insta_rennergebnis_page_1(data, filename="insta/insta_rennergebnisse_seite1.png"):
    # Create a transparent base image (RGBA mode)  
    final_image = Image.new("RGBA", (insta_width, insta_height), (0, 0, 0, 0))  # Fully transparent
    background = Image.open("./images/Raceresult_Insta_1.png").convert("RGBA")

    # Paste images onto the final image at specified positions
    final_image.paste(background, (0, 0), background)  # The third argument is the mask for transparency
    draw = ImageDraw.Draw(final_image)

    # Draw Racetitel with semi-transparency
    draw.text((insta_race_titel_pos[0], insta_race_titel_pos[1]), name_rennen, font=race_titel_insta, fill=(255, 255, 255, 255), anchor="lm")

    ### Fill Positions
    position = 0
    for driver in data:
        # Draw the rest of row     
        bbox = draw.textbbox((-100, -100), driver.Vorname, font=regular)
        name_length = bbox[2] - bbox[0]
        
        if(position == 0):
            gained_points = "+25"
        elif(position == 1):
            gained_points = "+18"
        elif(position == 2):
            gained_points = "+15"
        elif(position == 3):
            gained_points = "+12"
        elif(position == 4):
            gained_points = "+10"
        elif(position == 5):
            gained_points = "+8"
        elif(position == 6):
            gained_points = "+6"
        elif(position == 7):
            gained_points = "+4"
        elif(position == 8):
            gained_points = "+2"
        elif(position == 9):
            gained_points = "+1"
        else:
            gained_points = "+0"

        
        if(position == 0):
            #Draw Position
            draw.text((insta_position_text, insta_first_name + (position * insta_y_offset)), str(position + 1), font=position_font, fill=(0, 0, 0, 255), anchor="lb")            
            #Draw Flag
            flag_image = Image.open("./flags/" + driver.Nation + ".png").convert("RGBA")
            flag_image = flag_image.resize((flag_width, flag_height))
            final_image.paste(flag_image, (insta_left_allignment, insta_first_name + (position * insta_y_offset) - flag_y_offset), flag_image)
            #Vorname
            draw.text((insta_left_allignment + flag_width + spacer, insta_first_name + (position * insta_y_offset)), driver.Vorname, font=regular, fill=(0, 0, 0, 255), anchor="lb")
            #Nachname
            draw.text((insta_left_allignment  + flag_width + spacer + name_length + spacer, insta_first_name + (position * insta_y_offset)), driver.Nachname.upper(), font=bold, fill=(0, 0, 0, 255), anchor="lb")
            #Teamname
            #draw.text((insta_team_alignment[0] , insta_team_alignment[1] + (position * insta_y_offset)), driver.Team.upper(), font=insta, fill=(0, 0, 0, 255), anchor="lm")
            #Team Logo
            logo = Image.open("./team_logos/" + get_team_logo(driver.Team)).convert("RGBA")
            logo = logo.resize(team_logo_scaled)
            # Paste images onto the final image at specified positions
            final_image.paste(logo, (insta_team_alignment[0] + 2*flag_width, insta_team_alignment[1] + (position * insta_y_offset) - flag_y_offset), logo)
            draw = ImageDraw.Draw(final_image)
            #Zeit
            td = datetime.timedelta(seconds=float(winner.finish_time))
            # Format as mm:ss.SSS
            minutes, sec = divmod(td.total_seconds(), 60)
            formatted = f"{int(minutes):02}:{sec:06.3f}"
            draw.text((insta_racetime_alignment , insta_team_alignment[1] + (position * insta_y_offset)), formatted, font=regular, fill=(0, 0, 0, 255), anchor="rm")
            #Points
            draw.text((insta_points_allignment, insta_team_alignment[1] + (position * insta_y_offset)), gained_points, font=pos_bold, fill=(0, 0, 0, 255), anchor="mm")
        else:
            #Draw Position
            draw.text((insta_position_text, insta_first_name + (position * insta_y_offset)), str(position + 1), font=position_font, fill=(255,255,255, 255), anchor="lb")            
            #Draw Flag
            flag_image = Image.open("./flags/" + driver.Nation + ".png").convert("RGBA")
            flag_image = flag_image.resize((flag_width, flag_height))
            final_image.paste(flag_image, (insta_left_allignment, insta_first_name + (position * insta_y_offset) - flag_y_offset), flag_image)
            #Vorname
            draw.text((insta_left_allignment + flag_width + spacer, insta_first_name + (position * insta_y_offset)), driver.Vorname, font=regular, fill=(255, 255, 255, 255), anchor="lb")
            #Nachname
            draw.text((insta_left_allignment  + flag_width + spacer + name_length + spacer, insta_first_name + (position * insta_y_offset)), driver.Nachname.upper(), font=bold, fill=(255, 255, 255, 255), anchor="lb")
            #Teamname
           #draw.text((insta_team_alignment[0] , insta_team_alignment[1] + (position * insta_y_offset)), driver.Team.upper(), font=insta, fill=(255, 255, 255, 255), anchor="lm")
            #Team Logo
            logo = Image.open("./team_logos/" + get_team_logo(driver.Team)).convert("RGBA")
            logo = logo.resize(team_logo_scaled)
            # Paste images onto the final image at specified positions
            final_image.paste(logo, (insta_team_alignment[0] + 2*flag_width, insta_team_alignment[1] + (position * insta_y_offset) - flag_y_offset), logo)
            draw = ImageDraw.Draw(final_image)
            #Zeit
            if (driver.finish_time == "DNS"):
                draw.text((insta_racetime_alignment , insta_team_alignment[1] + (position * insta_y_offset)), "DNS", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            elif (driver.finish_time == "DNF"):
                draw.text((insta_racetime_alignment , insta_team_alignment[1] + (position * insta_y_offset)), "DNF", font=regular, fill=(255, 255, 255, 255), anchor="rm")            
            elif ("Lap" in driver.finish_time):
                draw.text((insta_racetime_alignment , insta_team_alignment[1] + (position * insta_y_offset)), driver.finish_time, font=regular, fill=(255, 255, 255, 255), anchor="rm")
            else:
                time_behind_leader = float(driver.finish_time) - float(winner.finish_time)
                if(time_behind_leader < 10):
                    draw.text((insta_racetime_alignment , insta_team_alignment[1] + (position * insta_y_offset)), f"+0{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
                else:
                    draw.text((insta_racetime_alignment , insta_team_alignment[1] + (position * insta_y_offset)), f"+{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            #Points
            draw.text((insta_points_allignment, insta_team_alignment[1] + (position * insta_y_offset)), gained_points, font=pos_bold, fill=(255, 255, 255, 255), anchor="mm")
            #Penatly
            if (driver.penalty is not None):
                draw.text((insta_race_penalty_pos , insta_team_alignment[1] + (position * insta_y_offset)), ("+" + str(driver.penalty) + " sek") , font=penalty_font, fill=(255, 0, 0, 255), anchor="rm")


        # Update position for the next name
        position += 1

    ### Draw fastest Lap
    bbox = draw.textbbox((-100, -100), "FASTEST LAP", font=regular)
    name_length = bbox[2] - bbox[0]
    draw.text(insta_fastest_lap_position, "FASTEST LAP", font=regular, fill=(255, 0, 255, 255), anchor="lm")
    draw.text((insta_fastest_lap_position[0] + name_length + spacer + 5, insta_fastest_lap_position[1]), f"{fastest_lap_driver.Nachname}     {fastest_lap_driver.Team}     {fastest_lap_driver.get_laptime_formatted()}", font=regular, fill=(255, 255, 255, 255), anchor="lm")

    # Save the final image
    final_image.save(filename, format="PNG")
    print("Image saved as "+ filename)

def create_insta_rennergebnis_page_2(data, filename="insta/insta_rennergebnisse_seite2.png"):
    # Create a transparent base image (RGBA mode)  
    final_image = Image.new("RGBA", (insta_width, insta_height), (0, 0, 0, 0))  # Fully transparent
    background = Image.open("./images/Raceresult_Insta_2.png").convert("RGBA")

    # Paste images onto the final image at specified positions
    final_image.paste(background, (0, 0), background)  # The third argument is the mask for transparency
    draw = ImageDraw.Draw(final_image)

    # Draw Racetitel with semi-transparency
    draw.text((insta_race_titel_pos[0], insta_race_titel_pos[1]), name_rennen, font=race_titel_insta, fill=(255, 255, 255, 255), anchor="lm")

    ### Winner ###
    position = 0
    bbox = draw.textbbox((-100, -100), winner.Vorname, font=regular)
    name_length = bbox[2] - bbox[0]
    #Draw Position
    draw.text((insta_position_text, insta_first_name + (position * insta_y_offset)), str(position + 1), font=position_font, fill=(0, 0, 0, 255), anchor="lb")            
    #Draw Flag
    flag_image = Image.open("./flags/" + winner.Nation + ".png").convert("RGBA")
    flag_image = flag_image.resize((flag_width, flag_height))
    final_image.paste(flag_image, (insta_left_allignment, insta_first_name + (position * insta_y_offset) - flag_y_offset), flag_image)
    #Vorname
    draw.text((insta_left_allignment + flag_width + spacer, insta_first_name + (position * insta_y_offset)), winner.Vorname, font=regular, fill=(0, 0, 0, 255), anchor="lb")
    #Nachname
    draw.text((insta_left_allignment  + flag_width + spacer + name_length + spacer, insta_first_name + (position * insta_y_offset)), winner.Nachname.upper(), font=bold, fill=(0, 0, 0, 255), anchor="lb")
    #Teamname
    #draw.text((insta_team_alignment[0] , insta_team_alignment[1] + (position * insta_y_offset)), driver.Team.upper(), font=insta, fill=(0, 0, 0, 255), anchor="lm")
    #Team Logo
    logo = Image.open("./team_logos/" + get_team_logo(winner.Team)).convert("RGBA")
    logo = logo.resize(team_logo_scaled)
    # Paste images onto the final image at specified positions
    final_image.paste(logo, (insta_team_alignment[0] + 2*flag_width, insta_team_alignment[1] + (position * insta_y_offset) - flag_y_offset), logo)
    draw = ImageDraw.Draw(final_image)
    #Zeit
    td = datetime.timedelta(seconds=float(winner.finish_time))
    # Format as mm:ss.SSS
    minutes, sec = divmod(td.total_seconds(), 60)
    formatted = f"{int(minutes):02}:{sec:06.3f}"
    draw.text((insta_racetime_alignment , insta_team_alignment[1] + (position * insta_y_offset)), formatted, font=regular, fill=(0, 0, 0, 255), anchor="rm")
    #Points
    draw.text((insta_points_allignment, insta_team_alignment[1] + (position * insta_y_offset)), "+25", font=pos_bold, fill=(0, 0, 0, 255), anchor="mm")

    ### Fill Positions
    position = 1
    for driver in data:
        # Draw the rest of row     
        bbox = draw.textbbox((-100, -100), driver.Vorname, font=regular)
        name_length = bbox[2] - bbox[0]
        
        gained_points = "+0"    

        #Draw Position
        draw.text((insta_position_text, insta_first_name + (position * insta_y_offset)), str(position + 12), font=position_font, fill=(255,255,255, 255), anchor="lb")            
        #Draw Flag
        flag_image = Image.open("./flags/" + driver.Nation + ".png").convert("RGBA")
        flag_image = flag_image.resize((flag_width, flag_height))
        final_image.paste(flag_image, (insta_left_allignment, insta_first_name + (position * insta_y_offset) - flag_y_offset), flag_image)
        #Vorname
        draw.text((insta_left_allignment + flag_width + spacer, insta_first_name + (position * insta_y_offset)), driver.Vorname, font=regular, fill=(255, 255, 255, 255), anchor="lb")
        #Nachname
        draw.text((insta_left_allignment  + flag_width + spacer + name_length + spacer, insta_first_name + (position * insta_y_offset)), driver.Nachname.upper(), font=bold, fill=(255, 255, 255, 255), anchor="lb")
        #Teamname
        #draw.text((insta_team_alignment[0] , insta_team_alignment[1] + (position * insta_y_offset)), driver.Team.upper(), font=insta, fill=(255, 255, 255, 255), anchor="lm")
        #Team Logo
        logo = Image.open("./team_logos/" + get_team_logo(driver.Team)).convert("RGBA")
        logo = logo.resize(team_logo_scaled)
        # Paste images onto the final image at specified positions
        final_image.paste(logo, (insta_team_alignment[0] + 2*flag_width, insta_team_alignment[1] + (position * insta_y_offset) - flag_y_offset), logo)
        draw = ImageDraw.Draw(final_image)
        #Zeit
        if (driver.finish_time == "DNS"):
            draw.text((insta_racetime_alignment , insta_team_alignment[1] + (position * insta_y_offset)), "DNS", font=regular, fill=(255, 255, 255, 255), anchor="rm")
        elif (driver.finish_time == "DNF"):
            draw.text((insta_racetime_alignment , insta_team_alignment[1] + (position * insta_y_offset)), "DNF", font=regular, fill=(255, 255, 255, 255), anchor="rm")            
        elif ("Lap" in driver.finish_time):
            draw.text((insta_racetime_alignment , insta_team_alignment[1] + (position * insta_y_offset)), driver.finish_time, font=regular, fill=(255, 255, 255, 255), anchor="rm")
        else:
            time_behind_leader = float(driver.finish_time) - float(winner.finish_time)
            if(time_behind_leader < 10):
                draw.text((insta_racetime_alignment , insta_team_alignment[1] + (position * insta_y_offset)), f"+0{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            else:
                draw.text((insta_racetime_alignment , insta_team_alignment[1] + (position * insta_y_offset)), f"+{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
        #Points
        draw.text((insta_points_allignment, insta_team_alignment[1] + (position * insta_y_offset)), gained_points, font=pos_bold, fill=(255, 255, 255, 255), anchor="mm")
        #Penatly
        if (driver.penalty is not None):
            draw.text((insta_race_penalty_pos , insta_team_alignment[1] + (position * insta_y_offset)), ("+" + str(driver.penalty) + " sek") , font=penalty_font, fill=(255, 0, 0, 255), anchor="rm")


        # Update position for the next name
        position += 1

    ### Draw fastest Lap
    bbox = draw.textbbox((-100, -100), "FASTEST LAP", font=regular)
    name_length = bbox[2] - bbox[0]
    draw.text(insta_fastest_lap_position, "FASTEST LAP", font=regular, fill=(255, 0, 255, 255), anchor="lm")
    draw.text((insta_fastest_lap_position[0] + name_length + spacer + 5, insta_fastest_lap_position[1]), f"{fastest_lap_driver.Nachname}     {fastest_lap_driver.Team}     {fastest_lap_driver.get_laptime_formatted()}", font=regular, fill=(255, 255, 255, 255), anchor="lm")

    # Save the final image
    final_image.save(filename, format="PNG")
    print("Image saved as "+ filename)


def create_quali_page_1(data, filename="output/qualifikation_seite1.png"):
    # Create a transparent base image (RGBA mode)  
    final_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # Fully transparent
    classment_transparent = Image.open("./images/Classement_background.png").convert("RGBA")
    background = Image.open("./images/Quali_Hintergrund1.png").convert("RGBA")

    # Paste images onto the final image at specified positions
    mask = Image.new('L', classment_transparent.size, 200)  # 50% transparency
    final_image.paste(classment_transparent, (0, 0), mask)  # The third argument is the mask for transparency
    final_image.paste(background, (0, 0), background)  # The third argument is the mask for transparency
    draw = ImageDraw.Draw(final_image)

    # Draw Racetitel with semi-transparency
    draw.text((557, 100), name_rennen, font=race_titel, fill=(255, 255, 255, 255), anchor="lt")

    winner = data[0]

    #Draw race winner
    winner_overall = Image.open("./overalls/" + winner.Overall).convert("RGBA")
    winner_overall = winner_overall.resize((680, 680))
    final_image.paste(winner_overall, overall_position, winner_overall)
    overall_fade = Image.open("./images/Winner_Vordergrund.png").convert("RGBA")
    final_image.paste(overall_fade, (0,0), overall_fade)
    
    #Winner rotated team text
    team_box = draw.textbbox((-100, -100), winner.get_team_short(), font=winner_team_font)
    temp_img = Image.new("RGBA", (team_box[2] - team_box[0], team_box[3] - team_box[1]), (0, 0, 0, 0))  # Big enough for horizontal text
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((0, 0), winner.get_team_short(), font=winner_team_font, fill=(255, 255, 255, 100), anchor="lt")

    # Rotate the temporary image 90 degrees counter-clockwise
    rotated_text = temp_img.rotate(90, expand=True)
    final_image.paste(rotated_text, winner_team_position, rotated_text)

    #Winner rotated number text
    team_box = draw.textbbox((-100, -100), winner.Nummer, font=winner_team_font)
    temp_img = Image.new("RGBA", (team_box[2] - team_box[0], team_box[3] - team_box[1]), (0, 0, 0, 0))  # Big enough for horizontal text
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((0, 0), winner.Nummer, font=winner_team_font, fill=(255, 255, 255, 100), anchor="lt")

    # Rotate the temporary image 90 degrees counter-clockwise
    rotated_text = temp_img.rotate(90, expand=True)
    final_image.paste(rotated_text, winner_number_position, rotated_text)
    
    ### Winner Name
    draw.text(winner_name_pos, winner.Nachname.upper(), font=winner_name_font, fill=(255, 255, 255, 255), anchor="mm")
    
    ### Fill Positions
    position = 0
    for driver in data:
        #Text zu CAPS

        
        # Draw the rest of row     
        bbox = draw.textbbox((-100, -100), driver.Vorname, font=regular)
        name_length = bbox[2] - bbox[0]
        
        if(position == 0):
            #Draw Position
            draw.text((position_text, first_name + (position * y_offset)), str(position + 1), font=position_font, fill=(0, 0, 0, 255), anchor="lb")            
            #Draw Flag
            flag_image = Image.open("./flags/" + driver.Nation + ".png").convert("RGBA")
            flag_image = flag_image.resize((flag_width, flag_height))
            final_image.paste(flag_image, (left_allignment, first_name + (position * y_offset) - flag_y_offset), flag_image)
            #Vorname
            draw.text((left_allignment + flag_width + spacer, first_name + (position * y_offset)), driver.Vorname, font=regular, fill=(0, 0, 0, 255), anchor="lb")
            #Nachname
            draw.text((left_allignment  + flag_width + spacer + name_length + spacer, first_name + (position * y_offset)), driver.Nachname.upper(), font=bold, fill=(0, 0, 0, 255), anchor="lb")
            #Teamname
            draw.text((team_name_allignment , first_team_and_points + (position * y_offset)), driver.Team.upper(), font=regular, fill=(0, 0, 0, 255), anchor="lm")
            #Team Logo
            logo = Image.open("./team_logos/" + get_team_logo(driver.Team)).convert("RGBA")
            logo = logo.resize(team_logo_scaled)
            # Paste images onto the final image at specified positions
            final_image.paste(logo, (team_logo_alignment[0], team_logo_alignment[1] + (position * y_offset)), logo)
            draw = ImageDraw.Draw(final_image)
            #Zeit
            if winner.finish_time != "No Time":
                td = datetime.timedelta(seconds=float(winner.finish_time))
                # Format as mm:ss.SSS
                minutes, sec = divmod(td.total_seconds(), 60)
                formatted = f"{int(minutes):01}:{sec:06.3f}"
                draw.text((quali_time_allignment , first_team_and_points + (position * y_offset)), formatted, font=regular, fill=(0, 0, 0, 255), anchor="rm")
            else:
                draw.text((quali_time_allignment , first_team_and_points + (position * y_offset)), "No Time", font=regular, fill=(0, 0, 0, 255), anchor="rm")
            #Penatly
            if (driver.penalty is not None):
                draw.text((quali_penalty_x , first_team_and_points + (position * y_offset)), driver.penalty, font=penalty_font, fill=(255, 0, 0, 255), anchor="rm")
        else:
            #Draw Position
            draw.text((position_text, first_name + (position * y_offset)), str(position + 1), font=position_font, fill=(255, 255, 255, 255), anchor="lb")            
            #Draw Flag
            flag_image = Image.open("./flags/" + driver.Nation + ".png").convert("RGBA")
            flag_image = flag_image.resize((flag_width, flag_height))
            final_image.paste(flag_image, (left_allignment, first_name + (position * y_offset) - flag_y_offset), flag_image)
            #Vorname
            draw.text((left_allignment + flag_width + spacer, first_name + (position * y_offset)), driver.Vorname, font=regular, fill=(255, 255, 255, 255), anchor="lb")
            #Nachname
            draw.text((left_allignment  + flag_width + spacer + name_length + spacer, first_name + (position * y_offset)), driver.Nachname.upper(), font=bold, fill=(255, 255, 255, 255), anchor="lb")
            #Teamname
            draw.text((team_name_allignment , first_team_and_points + (position * y_offset)), driver.Team.upper(), font=regular, fill=(255, 255, 255, 255), anchor="lm")
            #Team Logo
            logo = Image.open("./team_logos/" + get_team_logo(driver.Team)).convert("RGBA")
            logo = logo.resize(team_logo_scaled)
            # Paste images onto the final image at specified positions
            final_image.paste(logo, (team_logo_alignment[0], team_logo_alignment[1] + (position * y_offset)), logo)
            draw = ImageDraw.Draw(final_image)
            #Zeit
            if (driver.finish_time == "No Time"):
                draw.text((quali_time_allignment , first_team_and_points + (position * y_offset)), "No Time", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            else:
                time_behind_leader = float(driver.finish_time) - float(winner.finish_time)
                draw.text((quali_time_allignment , first_team_and_points + (position * y_offset)), f"+{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            #Penatly
            if (driver.penalty is not None):
                draw.text((quali_penalty_x , first_team_and_points + (position * y_offset)), driver.penalty, font=penalty_font, fill=(255, 0, 0, 255), anchor="rm")


        # Update position for the next name
        position += 1

    # Save the final image
    final_image.save(filename, format="PNG")
    print("Image saved as "+ filename)

def create_quali_page_2(data, filename="output/qualifikation_seite2.png"):
    # Create a transparent base image (RGBA mode)  
    final_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # Fully transparent
    classment_transparent = Image.open("./images/Classement_background.png").convert("RGBA")
    background = Image.open("./images/Quali_Hintergrund2.png").convert("RGBA")

    # Paste images onto the final image at specified positions
    mask = Image.new('L', classment_transparent.size, 200)  # 50% transparency
    final_image.paste(classment_transparent, (0, 0), mask)  # The third argument is the mask for transparency
    final_image.paste(background, (0, 0), background)  # The third argument is the mask for transparency
    draw = ImageDraw.Draw(final_image)

    # Draw Racetitel with semi-transparency
    draw.text((557, 100), name_rennen, font=race_titel, fill=(255, 255, 255, 255), anchor="lt")
    
    winner = qualiergebnis[0]
    #Draw race winner
    winner_overall = Image.open("./overalls/" + winner.Overall).convert("RGBA")
    winner_overall = winner_overall.resize((680, 680))
    final_image.paste(winner_overall, overall_position, winner_overall)
    overall_fade = Image.open("./images/Winner_Vordergrund.png").convert("RGBA")
    final_image.paste(overall_fade, (0,0), overall_fade)
    
    #Winner rotated team text
    team_box = draw.textbbox((-100, -100), winner.get_team_short(), font=winner_team_font)
    temp_img = Image.new("RGBA", (team_box[2] - team_box[0], team_box[3] - team_box[1]), (0, 0, 0, 0))  # Big enough for horizontal text
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((0, 0), winner.get_team_short(), font=winner_team_font, fill=(255, 255, 255, 100), anchor="lt")

    # Rotate the temporary image 90 degrees counter-clockwise
    rotated_text = temp_img.rotate(90, expand=True)
    final_image.paste(rotated_text, winner_team_position, rotated_text)

    #Winner rotated number text
    team_box = draw.textbbox((-100, -100), winner.Nummer, font=winner_team_font)
    temp_img = Image.new("RGBA", (team_box[2] - team_box[0], team_box[3] - team_box[1]), (0, 0, 0, 0))  # Big enough for horizontal text
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((0, 0), winner.Nummer, font=winner_team_font, fill=(255, 255, 255, 100), anchor="lt")

    # Rotate the temporary image 90 degrees counter-clockwise
    rotated_text = temp_img.rotate(90, expand=True)
    final_image.paste(rotated_text, winner_number_position, rotated_text)
    
    ### Winner Name
    draw.text(winner_name_pos, winner.Nachname.upper(), font=winner_name_font, fill=(255, 255, 255, 255), anchor="mm")
    

    #Draw Winner in Tableau
    position = 0
    draw.text((position_text, first_name + (position * y_offset)), str(position + 1), font=position_font, fill=(0, 0, 0, 255), anchor="lb")            
    #Draw Flag
    flag_image = Image.open("./flags/" + winner.Nation + ".png").convert("RGBA")
    flag_image = flag_image.resize((flag_width, flag_height))
    final_image.paste(flag_image, (left_allignment, first_name + (position * y_offset) - flag_y_offset), flag_image)

    # Draw the rest of row     
    bbox = draw.textbbox((-100, -100), winner.Vorname, font=regular)
    name_length = bbox[2] - bbox[0]

    #Vorname
    draw.text((left_allignment + flag_width + spacer, first_name + (position * y_offset)), winner.Vorname, font=regular, fill=(0, 0, 0, 255), anchor="lb")    
    #Nachname
    draw.text((left_allignment  + flag_width + spacer + name_length + spacer, first_name + (position * y_offset)), winner.Nachname, font=bold, fill=(0, 0, 0, 255), anchor="lb")
    #Teamname
    draw.text((team_name_allignment , first_name + (position * y_offset)), winner.Team, font=regular, fill=(0, 0, 0, 255), anchor="lb")
    #Team Logo
    team_filename = get_team_logo(winner.Team)
    logo = Image.open("./team_logos/" + team_filename).convert("RGBA")
    logo = logo.resize(team_logo_scaled)
    # Paste images onto the final image at specified positions
    final_image.paste(logo, (team_logo_alignment[0], team_logo_alignment[1] + (position * y_offset)), logo)
    draw = ImageDraw.Draw(final_image)
    #Zeit
    td = datetime.timedelta(seconds=float(winner.finish_time))
    # Format as mm:ss.SSS
    minutes, sec = divmod(td.total_seconds(), 60)
    formatted = f"{int(minutes):01}:{sec:06.3f}"
    draw.text((quali_time_allignment , first_team_and_points + (position * y_offset)), formatted, font=regular, fill=(0, 0, 0, 255), anchor="rm")
    


    ### Fill Positions
    position = 1
    for driver in data:
        #Text zu CAPS

        # Draw the rest of row     
        bbox = draw.textbbox((-100, -100), driver.Vorname, font=regular)
        name_length = bbox[2] - bbox[0]
        
        #Draw Position
        draw.text((position_text, first_name + (position * y_offset)), str(position + 12), font=position_font, fill=(255, 255, 255, 255), anchor="lb")            
        #Draw Flag
        flag_image = Image.open("./flags/" + driver.Nation + ".png").convert("RGBA")
        flag_image = flag_image.resize((flag_width, flag_height))
        final_image.paste(flag_image, (left_allignment, first_name + (position * y_offset) - flag_y_offset), flag_image)
        #Vorname
        draw.text((left_allignment + flag_width + spacer, first_name + (position * y_offset)), driver.Vorname, font=regular, fill=(255, 255, 255, 255), anchor="lb")
        #Nachname
        draw.text((left_allignment  + flag_width + spacer + name_length + spacer, first_name + (position * y_offset)), driver.Nachname.upper(), font=bold, fill=(255, 255, 255, 255), anchor="lb")
        #Teamname
        draw.text((team_name_allignment , first_team_and_points + (position * y_offset)), driver.Team.upper(), font=regular, fill=(255, 255, 255, 255), anchor="lm")
        #Team Logo
        logo = Image.open("./team_logos/" + get_team_logo(driver.Team)).convert("RGBA")
        logo = logo.resize(team_logo_scaled)
        # Paste images onto the final image at specified positions
        final_image.paste(logo, (team_logo_alignment[0], team_logo_alignment[1] + (position * y_offset)), logo)
        draw = ImageDraw.Draw(final_image)
        #Zeit
        if (driver.finish_time == "No Time"):
            draw.text((quali_time_allignment , first_team_and_points + (position * y_offset)), "No Time", font=regular, fill=(255, 255, 255, 255), anchor="rm")
        else:
            time_behind_leader = float(driver.finish_time) - float(winner.finish_time)
            draw.text((quali_time_allignment , first_team_and_points + (position * y_offset)), f"+{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
        #Penalty
        if (driver.penalty is not None):
            draw.text((quali_penalty_x , first_team_and_points + (position * y_offset)), driver.penalty, font=penalty_font, fill=(255, 0, 0, 255), anchor="rm")
        # Update position for the next name
        position += 1

    
    

    # Save the final image
    final_image.save(filename, format="PNG")
    print("Image saved as "+ filename)

def create_insta_quali_page_1(data, filename="insta/insta_quali_seite1.png"):
    # Create a transparent base image (RGBA mode)  
    final_image = Image.new("RGBA", (insta_width, insta_height), (0, 0, 0, 0))  # Fully transparent
    background = Image.open("./images/Quali_Insta_1.png").convert("RGBA")

    final_image.paste(background, (0, 0), background)  # The third argument is the mask for transparency
    draw = ImageDraw.Draw(final_image)

    # Draw Racetitel with semi-transparency
    draw.text((insta_race_titel_pos[0], insta_race_titel_pos[1]), name_rennen, font=race_titel_insta, fill=(255, 255, 255, 255), anchor="lm")

    winner = data[0]

    ### Fill Positions
    position = 0
    for driver in data:        
        # Draw the rest of row     
        bbox = draw.textbbox((-100, -100), driver.Vorname, font=regular)
        name_length = bbox[2] - bbox[0]
        
        if(position == 0):
            #Draw Position
            draw.text((insta_position_text, insta_first_name + (position * insta_y_offset)), str(position + 1), font=position_font, fill=(0, 0, 0, 255), anchor="lb")            
            #Draw Flag
            flag_image = Image.open("./flags/" + driver.Nation + ".png").convert("RGBA")
            flag_image = flag_image.resize((flag_width, flag_height))
            final_image.paste(flag_image, (insta_left_allignment, insta_first_name + (position * insta_y_offset) - flag_y_offset), flag_image)
            #Vorname
            draw.text((insta_left_allignment + flag_width + spacer, insta_first_name + (position * insta_y_offset)), driver.Vorname, font=regular, fill=(0, 0, 0, 255), anchor="lb")
            #Nachname
            draw.text((insta_left_allignment  + flag_width + spacer + name_length + spacer, insta_first_name + (position * insta_y_offset)), driver.Nachname.upper(), font=bold, fill=(0, 0, 0, 255), anchor="lb")
            #Teamname
            draw.text((insta_team_alignment[0] , insta_team_alignment[1] + (position * insta_y_offset)), winner.Team, font=regular, fill=(0, 0, 0, 255), anchor="lm")
            #Zeit
            if winner.finish_time != "No Time":
                td = datetime.timedelta(seconds=float(winner.finish_time))
                # Format as mm:ss.SSS
                minutes, sec = divmod(td.total_seconds(), 60)
                formatted = f"{int(minutes):01}:{sec:06.3f}"
                draw.text((insta_quali_time_allignment , insta_team_alignment[1] + (position * insta_y_offset)), formatted, font=regular, fill=(0, 0, 0, 255), anchor="rm")
            else:
                draw.text((insta_quali_time_allignment , insta_team_alignment[1] + (position * insta_y_offset)), "No Time", font=regular, fill=(0, 0, 0, 255), anchor="rm")
        else:
            #Draw Position
            draw.text((insta_position_text, insta_first_name + (position * insta_y_offset)), str(position + 1), font=position_font, fill=(255, 255, 255, 255), anchor="lb")            
            #Draw Flag
            flag_image = Image.open("./flags/" + driver.Nation + ".png").convert("RGBA")
            flag_image = flag_image.resize((flag_width, flag_height))
            final_image.paste(flag_image, (insta_left_allignment, insta_first_name + (position * insta_y_offset) - flag_y_offset), flag_image)
            #Vorname
            draw.text((insta_left_allignment + flag_width + spacer, insta_first_name + (position * insta_y_offset)), driver.Vorname, font=regular, fill=(255, 255, 255, 255), anchor="lb")
            #Nachname
            draw.text((insta_left_allignment  + flag_width + spacer + name_length + spacer, insta_first_name + (position * insta_y_offset)), driver.Nachname.upper(), font=bold, fill=(255, 255, 255, 255), anchor="lb")
             #Teamname
            draw.text((insta_team_alignment[0] , insta_team_alignment[1] + (position * insta_y_offset)), driver.Team, font=regular, fill=(255, 255, 255, 255), anchor="lm")
            #Zeit
            if (driver.finish_time == "No Time"):
                draw.text((insta_quali_time_allignment , insta_team_alignment[1] + (position * insta_y_offset)), "No Time", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            else:
                time_behind_leader = float(driver.finish_time) - float(winner.finish_time)
                draw.text((insta_quali_time_allignment , insta_team_alignment[1] + (position * insta_y_offset)), f"+{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            #Penatly
            if (driver.penalty is not None):
                draw.text((insta_quali_penalty_x , insta_team_alignment[1] + (position * insta_y_offset)), driver.penalty, font=penalty_font, fill=(255, 0, 0, 255), anchor="rm")


        # Update position for the next name
        position += 1

    # Save the final image
    final_image.save(filename, format="PNG")
    print("Image saved as "+ filename)

def create_insta_quali_page_2(data, filename="insta/insta_quali_seite2.png"):
    # Create a transparent base image (RGBA mode)  
    final_image = Image.new("RGBA", (insta_width, insta_height), (0, 0, 0, 0))  # Fully transparent
    background = Image.open("./images/Quali_Insta_2.png").convert("RGBA")
    final_image.paste(background, (0, 0), background)  # The third argument is the mask for transparency
    draw = ImageDraw.Draw(final_image)

    # Draw Racetitel with semi-transparency
    draw.text((insta_race_titel_pos[0], insta_race_titel_pos[1]), name_rennen, font=race_titel_insta, fill=(255, 255, 255, 255), anchor="lm")
    
    winner = qualiergebnis[0]

    #Draw Winner in Tableau
    position = 0
    bbox = draw.textbbox((-100, -100), winner.Vorname, font=regular)
    name_length = bbox[2] - bbox[0]
    #Draw Position
    draw.text((insta_position_text, insta_first_name + (position * insta_y_offset)), str(position + 1), font=position_font, fill=(0, 0, 0, 255), anchor="lb")            
    #Draw Flag
    flag_image = Image.open("./flags/" + winner.Nation + ".png").convert("RGBA")
    flag_image = flag_image.resize((flag_width, flag_height))
    final_image.paste(flag_image, (insta_left_allignment, insta_first_name + (position * insta_y_offset) - flag_y_offset), flag_image)
    #Vorname
    draw.text((insta_left_allignment + flag_width + spacer, insta_first_name + (position * insta_y_offset)), winner.Vorname, font=regular, fill=(0, 0, 0, 255), anchor="lb")
    #Nachname
    draw.text((insta_left_allignment  + flag_width + spacer + name_length + spacer, insta_first_name + (position * insta_y_offset)), winner.Nachname.upper(), font=bold, fill=(0, 0, 0, 255), anchor="lb")
    #Teamname
    draw.text((insta_team_name_allignment , insta_team_alignment[1] + (position * insta_y_offset)), winner.Team, font=regular, fill=(0, 0, 0, 255), anchor="lm")
    #Zeit
    if winner.finish_time != "No Time":
        td = datetime.timedelta(seconds=float(winner.finish_time))
        # Format as mm:ss.SSS
        minutes, sec = divmod(td.total_seconds(), 60)
        formatted = f"{int(minutes):01}:{sec:06.3f}"
        draw.text((insta_quali_time_allignment , insta_team_alignment[1] + (position * insta_y_offset)), formatted, font=regular, fill=(0, 0, 0, 255), anchor="rm")
    else:
        draw.text((insta_quali_time_allignment , insta_team_alignment[1] + (position * insta_y_offset)), "No Time", font=regular, fill=(0, 0, 0, 255), anchor="rm")


    ### Fill Positions
    position = 1
    for driver in data:
        bbox = draw.textbbox((-100, -100), driver.Vorname, font=regular)
        name_length = bbox[2] - bbox[0]
        #Draw Position
        draw.text((insta_position_text, insta_first_name + (position * insta_y_offset)), str(position + 12), font=position_font, fill=(255, 255, 255, 255), anchor="lb")            
        #Draw Flag
        flag_image = Image.open("./flags/" + driver.Nation + ".png").convert("RGBA")
        flag_image = flag_image.resize((flag_width, flag_height))
        final_image.paste(flag_image, (insta_left_allignment, insta_first_name + (position * insta_y_offset) - flag_y_offset), flag_image)
        #Vorname
        draw.text((insta_left_allignment + flag_width + spacer, insta_first_name + (position * insta_y_offset)), driver.Vorname, font=regular, fill=(255, 255, 255, 255), anchor="lb")
        #Nachname
        draw.text((insta_left_allignment  + flag_width + spacer + name_length + spacer, insta_first_name + (position * insta_y_offset)), driver.Nachname.upper(), font=bold, fill=(255, 255, 255, 255), anchor="lb")
            #Teamname
        draw.text((insta_team_name_allignment , insta_team_alignment[1] + (position * insta_y_offset)), driver.Team, font=regular, fill=(255, 255, 255, 255), anchor="lm")
        #Zeit
        if (driver.finish_time == "No Time"):
            draw.text((insta_quali_time_allignment , insta_team_alignment[1] + (position * insta_y_offset)), "No Time", font=regular, fill=(255, 255, 255, 255), anchor="rm")
        else:
            time_behind_leader = float(driver.finish_time) - float(winner.finish_time)
            draw.text((insta_quali_time_allignment , insta_team_alignment[1] + (position * insta_y_offset)), f"+{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
        #Penatly
        if (driver.penalty is not None):
            draw.text((insta_quali_penalty_x , insta_team_alignment[1] + (position * insta_y_offset)), driver.penalty, font=penalty_font, fill=(255, 0, 0, 255), anchor="rm")
        position += 1

    
    

    # Save the final image
    final_image.save(filename, format="PNG")
    print("Image saved as "+ filename)

def read_raceresult_xml():
    global current_race_number, xml_export, starting_grid

    xml_export = []
    starting_grid = []

    ### Finde die XML Datei zum letzten Rennen ###
    folder = 'race_results'
    pattern = re.compile(r'Rennen(\d+)\.xml')

    # Find all files matching the pattern
    files = [f for f in os.listdir(folder) if pattern.match(f)]

    # Extract the number and find the file with the highest number
    if files:
        max_file = max(files, key=lambda f: int(pattern.match(f).group(1)))
        print(f"Öffne Datei: {max_file}")
        # Beispiel: XML parsen
        import xml.etree.ElementTree as ET
        tree = ET.parse(os.path.join(folder, max_file))
        root = tree.getroot()
    else:
        print("Keine passenden XML-Dateien gefunden.")
    
    current_race_number = int(str.split(max_file, "Rennen")[1][0:2])

    race_laps = root.find('.//RaceLaps')
    ### Extract Drivers from XML ###    
    for driver in root.findall('.//Driver'):
        name_elem = driver.find('Name')
        position = driver.find('Position')
        category_elem = driver.find('Category')
        racetime = driver.find('FinishTime')
        finished = driver.find('FinishStatus')        
        finished_laps = driver.find('Laps')
        fastes_lap = driver.find('BestLapTime')
        penalty = driver.find('r2la_penalty')
        grid_pos = driver.find('GridPos')

        if (category_elem is None) or not ("F1S13" in category_elem.text):                        
            continue

        if (finished is None):
            print("finished ist None")
            continue
        
        if grid_pos is not None:
            grid_pos = grid_pos.text
            starting_grid.append((name_elem.text, grid_pos))
        
        if penalty is not None:
            penalty = (int) (penalty.text.split(".")[0])  # Nur Sekundenanteil
        else:
            penalty = 0

        if fastes_lap is None:
            fastes_lap = "1000"
        else:
            fastes_lap = fastes_lap.text

        if finished.text == "None":
            xml_export.append((name_elem.text, position.text, "DNS", fastes_lap, penalty))
            continue

        if finished.text == "DNF":
            xml_export.append((name_elem.text, position.text, "DNF", fastes_lap, penalty))
            continue

        if int(finished_laps.text) < int(race_laps.text):
            if (int(race_laps.text) - int(finished_laps.text) == 1):
                xml_export.append((name_elem.text, position.text, "+1 Lap", fastes_lap, penalty))
            else:
                xml_export.append((name_elem.text, position.text, f"+ {int(race_laps.text) - int(finished_laps.text)} Laps", fastes_lap, penalty))
            continue

        if finished.text == "Finished Normally":
            xml_export.append((name_elem.text, position.text, racetime.text, fastes_lap, penalty))
            continue
        
        
    ### Sortiere nach Position
    xml_export.sort(key=lambda x: int(x[1]))  # Sort by position
    starting_grid.sort(key=lambda x: int(x[1]))  # Sort by grid position

def read_quali_xml():
    global qualiergebnis
    quali1 = []
    quali2 = []
    ### Finde die XML Datei zum letzten Rennen ###
    folder = 'quali_result'

### Quali1 Ergegbnis

    # Extract the number and find the file with the highest number
    import xml.etree.ElementTree as ET
    tree = ET.parse(os.path.join(folder, "quali1.xml"))
    root = tree.getroot()

    ### Extract Drivers from XML ###    
    for driver in root.findall('.//Driver'):
        name_elem = driver.find('Name')
        position = driver.find('Position')
        category_elem = driver.find('Category')
        quali_time = driver.find('BestLapTime')
        finished = driver.find('FinishStatus') 
        penalty = driver.find('r2la_penalty')   

        if (category_elem is None) or not ("F1S13" in category_elem.text):                        
            continue

        if (finished is None):
            print("finished ist None")
            continue

        if quali_time is not None:
            quali_time = quali_time.text

        if penalty is not None:
            if penalty.text.isdigit():
                penalty = int(penalty.text)
            else:
                penalty = penalty.text
        else: 
            penalty = 0   
        
        if quali_time is not None:
            quali1.append((name_elem.text, position.text, quali_time, penalty))
        else:
            quali1.append((name_elem.text, position.text, "No Time", penalty))
    ### Sortiere nach Position
    quali1.sort(key=lambda x: int(x[1]))  # Sort by position

#Quali2 Ergebnis
# Extract the number and find the file with the highest number
    import xml.etree.ElementTree as ET
    tree = ET.parse(os.path.join(folder, "quali2.xml"))
    root = tree.getroot()

    ### Extract Drivers from XML ###    
    for driver in root.findall('.//Driver'):
        name_elem = driver.find('Name')
        position = driver.find('Position')
        category_elem = driver.find('Category')
        quali_time = driver.find('BestLapTime')
        finished = driver.find('FinishStatus')
        penalty = driver.find('r2la_penalty')       

        if position is not None:
            if int(position.text) > 10:
                continue

        if (category_elem is None) or not ("F1S13" in category_elem.text):                        
            continue

        if (finished is None):
            print("finished ist None")
            continue

        if quali_time is not None:
            quali_time = quali_time.text

        if penalty is not None:
            if penalty.text.isdigit():
                penalty = int(penalty.text)
            else:
                penalty = penalty.text
        else: 
            penalty = 0         
        
        if quali_time is not None:
            quali2.append((name_elem.text, position.text, quali_time, penalty))
        else:
            quali2.append((name_elem.text, position.text, "No Time", penalty))
    ### Sortiere nach Position
    quali2.sort(key=lambda x: int(x[1]))  # Sort by position

    qualiergebnis = quali2 + quali1[10:]

def read_driver_config():    
    global driver_config
    # read driver_config.csv
    with open("configs/driver_config.csv", encoding="utf-8") as csvfile:
        driver_config.clear()  # Clear existing data
        csvreader = csv.reader(csvfile, delimiter=";")
        # skip header1
        next(csvreader)

        for row in csvreader:
            if row == []:
                continue            
            driver_config.append(Driver(row))    

def read_team_config():
    team_config = []
    # read driver_config.csv
    with open("configs/team_config.csv", encoding="utf-8") as csvfile:        
        csvreader = csv.reader(csvfile, delimiter=";")
        # skip header1
        next(csvreader)

        for row in csvreader:
            if row == []:
                continue            
            team_config.append(row) 
    return team_config

def result_preprocessing():
    ### get sorted Race Result with config file ###   
    fastest = fastest_lap()
    rennergebnis.clear()  # Clear existing results
    for entry in xml_export:        
        found = False
        for driver in driver_config:
            if (driver.get_driver_name().upper() == entry[0].upper()):  
                #print("Gefunden: " + config[0] + " " + config[1] + ". Gesucht: " + entry[0])              
                driver_config.remove(driver)

                if entry[-1] > 0:
                    driver.penalty = entry[-1]
                driver.finish_time = entry[2]

                rennergebnis.append(driver)      
                driver.fastest_lap = entry[3]                                                      
                found = True    
                if not (driver.finish_time == "DNS" or driver.finish_time == "DNF" or "+" in driver.finish_time):                         
                    if(float(driver.fastest_lap) < float(fastest.lap_time)):
                        fastest = fastest_lap(driver.Vorname, driver.Nachname, driver.Team, driver.fastest_lap)
                    break
        if not found:
            print("Kein Eintrag für " + driver.get_driver_name() + " gefunden!")   

    print("Fertig mit der Ergebnisverarbeitung.")
    return (Winner(rennergebnis[0]), fastest)

def result_preprocessing_wm():
    ### get sorted Race Result with config file ###   
    fastest = fastest_lap()
    rennergebnis.clear()  # Clear existing results
    for entry in xml_export:        
        found = False
        for driver in driver_config:
            if (driver.get_driver_name().upper() == entry[0].upper()):  
                #print("Gefunden: " + config[0] + " " + config[1] + ". Gesucht: " + entry[0])              
                driver_config.remove(driver)
                rennergebnis.append(driver)                                                            
                found = True         
        if not found:
            print("Kein Eintrag für " + driver.get_driver_name() + " gefunden!")   

    print("Fertig mit der Ergebnisverarbeitung.")
    return Winner(rennergebnis[0]), fastest

def quali_preprocessing():
    global starting_grid, qualiergebnis
    final_quali_result = []
    for entry in qualiergebnis:
        for driver in driver_config:
            if (driver.get_driver_name().upper() == entry[0].upper()):  
                driver.finish_time = entry[2]
                if(entry[3] != 0):
                    if(entry[3] == "DSQ"):
                        driver.penalty = "DSQ"
                    else:
                        driver.penalty = f"+{entry[3]} Pos"
                final_quali_result.append(driver)
        
    qualiergebnis = final_quali_result.copy()

def get_team_logo(team):
    if(team == "Toyota F1 Team"):
            return "toyota.png"
    if(team == "Hugo Bros BMW Williams"):
        return "bmw.png"
    if(team == "Scuderia Toro Rosso"):
        return "toro_rosso.png"
    if(team == "Alpine F1 Team"):
        return "alpine.png"
    if(team == "Mercedes AMG"):
        return "mercedes.png"
    if(team == "Scuderia Ferrari"):
        return "ferrari.png"
    if(team == "McLaren F1 Team"):
        return "mclaren.png"
    if(team == "LUNZiT Red Bull Racing"):
        return "red_bull.png"
    if(team == "Jordan Grand Prix"):
        return "jordan.png"
    if(team == "Cadillac F1 Team"):
        return "cadillac.png"
    if(team == "Audi F1 Team"):
        return "audi.png"
    if(team == "Reserve"):
        return "reserve.png"

def calculate_wm_rankings():
    global xml_export, driver_config, team_config, rennergebnis
    driver_standings = []
    team_standings = []
    driver_standings_last_race = []
    team_standings_last_race = []
    xml_export.clear()  # Clear existing results

    team_config = read_team_config()
    for team in team_config:
        team.append(0)
        team_standings.append(team)

    print("WM Stand erzeugen")

    ### lese alle XML Datein ###
    folder = 'race_results'
    pattern = re.compile(r'Rennen(\d+)\.xml')

    # Find all files matching the pattern
    files = [f for f in os.listdir(folder) if pattern.match(f)]

    import xml.etree.ElementTree as ET
    race_number = 0
    ### Für jedes Rennen
    for race_file in files:   
        print("\n" + race_file + "\n")        
        tree = ET.parse(os.path.join(folder, race_file))
        root = tree.getroot()
        xml_export.clear()
        race_number += 1

        ### Extract Drivers from XML ###    
        for driver in root.findall('.//Driver'):
            name_elem = driver.find('Name')
            position = driver.find('Position')
            category_elem = driver.find('Category')
            fastes_lap = driver.find('BestLapTime')
            team = driver.find('TeamName')
            
            if (category_elem is None) or not ("F1S13" in category_elem.text):                        
                continue

            if fastes_lap is None:
                fastes_lap = "1000"
            else:
                fastes_lap = fastes_lap.text

            xml_export.append((name_elem.text, position.text, fastes_lap, team.text))

        ### Sortiere nach Position
        xml_export.sort(key=lambda x: int(x[1]))  # Sort by position

        ### Get driver config again    
        read_driver_config()
        _, fastest = result_preprocessing_wm()     
        finish_position = 0
        #print("\nRennergebnis:")
        for driver in rennergebnis:
            finish_position += 1              
            #print(driver[0][0] + " " + driver[0][1], finish_position)
            if(len(driver_standings) == 0):
                print("Driver Standing init")
                driver_standings.append([driver, 25])
                team = "reserve"
                if(driver.Stammfahrer):                    
                    team = driver.Team

                team_index = team_standings.index(next(entry for entry in team_standings if entry[0] == team))
                team_standings[team_index][-1] += 25
                team_standings[team_index][-1] -= (finish_position/10000)
                continue                                

            if any(entry[0].get_driver_name() == driver.get_driver_name() for entry in driver_standings):                
                ### Driver already in standings
                #print(driver)
                #print(driver_standings[0][0][0])
                item = next(entry for entry in driver_standings if entry[0].get_driver_name() == driver.get_driver_name())                  
                team = "reserve"
                if(driver.Stammfahrer):                    
                    team = driver.Team

                if(race_number < 7 and (driver.Nachname == "Rutishauser")):
                    team = driver.Team

                team_index = team_standings.index(next(entry for entry in team_standings if entry[0] == team))

                if(finish_position == 1):
                    item[1] += 25
                    item[1] -= (finish_position/10000)
                    team_standings[team_index][-1] += 25
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 2):
                    item[1] += 18
                    item[1] -= (finish_position/10000)
                    team_standings[team_index][-1] += 18
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 3):
                    item[1] += 15
                    item[1] -= (finish_position/10000)
                    team_standings[team_index][-1] += 15
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 4):
                    item[1] += 12
                    item[1] -= (finish_position/10000)
                    team_standings[team_index][-1] += 12
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 5):
                    item[1] += 10
                    item[1] -= (finish_position/10000)
                    team_standings[team_index][-1] += 10
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 6):
                    item[1] += 8
                    item[1] -= (finish_position/10000)
                    team_standings[team_index][-1] += 8
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 7):
                    item[1] += 6
                    item[1] -= (finish_position/10000)
                    team_standings[team_index][-1] += 6
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 8):
                    item[1] += 4
                    item[1] -= (finish_position/10000)
                    team_standings[team_index][-1] += 4
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 9):
                    item[1] += 2
                    item[1] -= (finish_position/10000)
                    team_standings[team_index][-1] += 2
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 10):
                    item[1] += 1
                    item[1] -= (finish_position/10000)
                    team_standings[team_index][-1] += 1
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position > 10):
                    item[1] += 0.01 
                    item[1] -= (finish_position/10000)
                    continue
            else:        
                print("Fahrer " + driver.get_driver_name() +  " hinzufügen zu Standings")   
                #print(driver)
                #print(driver_standings)
                #print("")
                team = "reserve"
                if(driver.Stammfahrer):
                    team = driver.Team

                team_index = team_standings.index(next(entry for entry in team_standings if entry[0] == team))                                                   
                if(finish_position == 1):
                    driver_standings.append([driver, (25) - (finish_position/10000)])
                    team_standings[team_index][-1] += 25
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 2):
                    driver_standings.append([driver, (18) - (finish_position/10000)])
                    team_standings[team_index][-1] += 18
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 3):
                    driver_standings.append([driver, (15) - (finish_position/10000)])
                    team_standings[team_index][-1] += 15
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 4):
                    driver_standings.append([driver, (12) - (finish_position/10000)])
                    team_standings[team_index][-1] += 12
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 5):
                    driver_standings.append([driver, (10) - (finish_position/10000)])
                    team_standings[team_index][-1] += 10
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 6):
                    driver_standings.append([driver, (8) - (finish_position/10000)])
                    team_standings[team_index][-1] += 8
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 7):
                    driver_standings.append([driver, (6) - (finish_position/10000)])
                    team_standings[team_index][-1] += 6
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 8):
                    driver_standings.append([driver, (4) - (finish_position/10000)])
                    team_standings[team_index][-1] += 4
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 9):
                    driver_standings.append([driver, (2) - (finish_position/10000)])
                    team_standings[team_index][-1] += 2
                    team_standings[team_index][-1] -= (finish_position/10000)
                    continue
                elif(finish_position == 10):
                    driver_standings.append([driver, (1) - (finish_position/10000)])
                    team_standings[team_index][-1] += 1
                    team_standings[team_index][-1] -= (finish_position/10000) 
                    continue
                else:
                    driver_standings.append([driver,  (0.01)  - (finish_position/10000)])
                    continue                        

        ### Sort by points ###
        driver_standings.sort(key=lambda x:x[1], reverse=True)
        team_standings_sorted = (team_standings.copy())[:11]
        team_standings_sorted.sort(key=lambda x: x[-1], reverse=True)
        team_standings_sorted.append(team_standings[-1])        

        if(race_number == len(files) - 1):
            driver_standings_last_race = driver_standings.copy()
            team_standings_last_race = team_standings_sorted.copy()
        
    if(race_number == 1):
        driver_standings_last_race = driver_standings.copy()
        team_standings_last_race = team_standings_sorted.copy()

    #print("\nFahrer WM Stand nach " + race_file + "\n" + "-------------------------------")                                                    
    #for driver in driver_standings:
    #    if(driver[1] % 1) < 0.5:
    #        print(driver[0][0][0] + " " + driver[0][0][1] + " - " + str(math.floor(driver[1])) + " Punkte (" + str(driver[1]) + ")")
    #    else:
    #        print(driver[0][0][0] + " " + driver[0][0][1] + " - " + str(math.ceil(driver[1])) + " Punkte (" + str(driver[1]) + ")")

    #print("\nTeam WM Stand nach " + race_file + "\n" + "-------------------------------")                                                    
    #for constructor in team_standings_sorted:
    #    if(constructor[-1] % 1) < 0.5:
    #        print(constructor[0] + " - " + str(math.floor(constructor[-1])) + " Punkte")
    #    else:
    #        print(constructor[0] + " - " + str(math.ceil(constructor[-1])) + " Punkte")

    generate_drivers_championship(driver_standings_last_race, driver_standings)
    generate_constructor_championship(team_standings_last_race, team_standings_sorted)

def generate_drivers_championship(last_race_standings, driver_standings):
    
    necessary_pages = math.ceil(len(driver_standings) / 11)
    
    for i in range(0, necessary_pages):
        # Create a transparent base image (RGBA mode)          
        final_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # Fully transparent
        background = Image.open("./images/Driver_standing_Background.png").convert("RGBA")
        if(i == 0):
            overlay = Image.open("./images/Driver_standings_1.png").convert("RGBA")
        else:
            overlay = Image.open("./images/Driver_standings_2.png").convert("RGBA")

        # Paste images onto the final image at specified positions
        mask = Image.new('L', background.size, 200)  # 50% transparency
        final_image.paste(background, (0, 0), mask)  # The third argument is the mask for transparency
        final_image.paste(overlay, (0, 0), overlay)  # The third argument is the mask for transparency
        draw = ImageDraw.Draw(final_image)

        # Draw Racetitel with semi-transparency
        draw.text(driver_wm_race_titel_position, name_rennen, font=race_titel, fill=(255, 255, 255, 255), anchor="lt")
        
        draw.text(driver_wm_info_text_position, f"Stand nach {current_race_number}/17 Rennen", font=regular, fill=(255, 255, 255, 255), anchor="lm")
        
        relevant_drivers = driver_standings[i * 11:(i + 1) * 11]

        #Positionspfeile
        arrow_up = Image.open("./images/arrow_up.png").convert("RGBA")
        arrow_down = Image.open("./images/arrow_down.png").convert("RGBA")
        arrow_up= arrow_up.resize(arrow_scale)
        arrow_down= arrow_down.resize(arrow_scale)
        
        ### Fill Positions
        position = 0
        for entry in relevant_drivers:            
            #Text zu CAPS
            driver_selec = entry[0]
            name = driver_selec.Vorname
            lastname = driver_selec.Nachname.upper()

            if(lastname == "RUTISHAUSER"):
                team = "Reserve"
            else:
                team = driver_selec.Team

            flag = driver_selec.Nation
            team_filename = get_team_logo(team)
            
            # Draw the rest of row     
            bbox = draw.textbbox((-100, -100), name, font=regular)
            name_length = bbox[2] - bbox[0]

            try:
                last_race_index = last_race_standings.index(next(standing for standing in last_race_standings if standing[0] == driver_selec))                        
            except StopIteration:
                last_race_index = position + (i * 11)
            if(position == 0 and i == 0):
                #Draw Position
                draw.text((driver_wm_position_x, driver_wm_first_name_y + (position * y_offset)), str(position + 1), font=position_font, fill=(0, 0, 0, 255), anchor="lb")            
                #Draw Flag
                flag_image = Image.open("./flags/" + flag + ".png").convert("RGBA")
                flag_image = flag_image.resize((flag_width, flag_height))
                final_image.paste(flag_image, (driver_wm_left_allignment_x, driver_wm_first_name_y + (position * y_offset) - flag_y_offset), flag_image)
                #Vorname
                draw.text((driver_wm_left_allignment_x + flag_width + spacer, driver_wm_first_name_y + (position * y_offset)), name, font=regular, fill=(0, 0, 0, 255), anchor="lb")
                #Nachname
                draw.text((driver_wm_left_allignment_x  + flag_width + spacer + name_length + spacer, driver_wm_first_name_y + (position * y_offset)), lastname, font=bold, fill=(0, 0, 0, 255), anchor="lb")
                #Teamname
                draw.text((driver_wm_team_x , driver_wm_team_y + (position * y_offset)), team, font=regular, fill=(0, 0, 0, 255), anchor="lm")
                #Team Logo
                logo = Image.open("./team_logos/" + team_filename).convert("RGBA")
                logo = logo.resize(team_logo_scaled)
                # Paste images onto the final image at specified positions
                final_image.paste(logo, (driver_wm_team_logo[0], driver_wm_team_logo[1] + (position * y_offset)), logo)
                draw = ImageDraw.Draw(final_image)
                #Points
                if(entry[1] % 1) < 0.5:
                    draw.text((driver_wm_points_pos[0], driver_wm_points_pos[1] + (position * y_offset)), str(math.floor(entry[1])), font=pos_bold, fill=(0, 0, 0, 255), anchor="rm")
                else:
                    draw.text((driver_wm_points_pos[0], driver_wm_points_pos[1] + (position * y_offset)), str(math.ceil(entry[1])), font=pos_bold, fill=(0, 0, 0, 255), anchor="rm")   

                if (last_race_index > 1):
                    # Paste images onto the final image at specified positions
                    final_image.paste(arrow_up, (driver_wm_arrow_x, driver_wm_first_row_lower - row_height + ((row_height - arrow_scale[1]) % 2) + (position * y_offset) + 7), arrow_up)
                    draw = ImageDraw.Draw(final_image)
                

            else:
                #Draw Position
                draw.text((driver_wm_position_x, driver_wm_first_name_y + (position * y_offset)), str(position + 1 + (i*11)), font=position_font, fill=(255, 255, 255, 255), anchor="lb")            
                #Draw Flag
                flag_image = Image.open("./flags/" + flag + ".png").convert("RGBA")
                flag_image = flag_image.resize((flag_width, flag_height))
                final_image.paste(flag_image, (driver_wm_left_allignment_x, driver_wm_first_name_y + (position * y_offset) - flag_y_offset), flag_image)
                #Vorname
                draw.text((driver_wm_left_allignment_x + flag_width + spacer, driver_wm_first_name_y + (position * y_offset)), name, font=regular, fill=(255, 255, 255, 255), anchor="lb")
                #Nachname
                draw.text((driver_wm_left_allignment_x  + flag_width + spacer + name_length + spacer, driver_wm_first_name_y + (position * y_offset)), lastname, font=bold, fill=(255, 255, 255, 255), anchor="lb")
                #Teamname
                draw.text((driver_wm_team_x , driver_wm_team_y + (position * y_offset)), team, font=regular, fill=(255, 255, 255, 255), anchor="lm")
                #Team Logo
                logo = Image.open("./team_logos/" + team_filename).convert("RGBA")
                logo = logo.resize(team_logo_scaled)
                # Paste images onto the final image at specified positions
                final_image.paste(logo, (driver_wm_team_logo[0], driver_wm_team_logo[1] + (position * y_offset)), logo)
                draw = ImageDraw.Draw(final_image)
                #Points
                if(entry[1] % 1) < 0.5:
                    draw.text((driver_wm_points_pos[0], driver_wm_points_pos[1] + (position * y_offset)), str(math.floor(entry[1])), font=pos_bold, fill=(255, 255, 255, 255), anchor="rm")
                else:
                    draw.text((driver_wm_points_pos[0], driver_wm_points_pos[1] + (position * y_offset)), str(math.ceil(entry[1])), font=pos_bold, fill=(255, 255, 255, 255), anchor="rm")
                #Pos Gained arrow
                if (last_race_index > (position + (i*11))):
                    # Paste images onto the final image at specified positions
                    final_image.paste(arrow_up, (driver_wm_arrow_x, driver_wm_first_row_lower - row_height + ((row_height - arrow_scale[1]) % 2) + (position * y_offset) + 7), arrow_up)
                    draw = ImageDraw.Draw(final_image)
                elif (last_race_index < (position + (i*11))):
                    # Paste images onto the final image at specified positions
                    final_image.paste(arrow_down, (driver_wm_arrow_x, driver_wm_first_row_lower - row_height + ((row_height - arrow_scale[1]) % 2) + (position * y_offset) + 7), arrow_down)
                    draw = ImageDraw.Draw(final_image)
            # Update position for the next name
            position += 1


        filename = "output/Fahrer_WM_Seite_" + str(i + 1) + ".png"
        final_image.save(filename, format="PNG")
        print("Image saved as "+ filename)

def generate_constructor_championship(last_race_standings, team_standings):

    # Create a transparent base image (RGBA mode)          
    final_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # Fully transparent
    background = Image.open("./images/Constructor_Standing_background.png").convert("RGBA")
    overlay = Image.open("./images/Constructor_Standing.png").convert("RGBA")

    # Paste images onto the final image at specified positions
    mask = Image.new('L', background.size, 200)  # 50% transparency
    final_image.paste(background, (0, 0), mask)  # The third argument is the mask for transparency
    final_image.paste(overlay, (0, 0), overlay)  # The third argument is the mask for transparency
    draw = ImageDraw.Draw(final_image)

    # Draw Racetitel with semi-transparency
    draw.text(team_wm_race_titel_position, name_rennen, font=race_titel, fill=(255, 255, 255, 255), anchor="lt")
    
    draw.text(team_wm_info_text_position, f"Stand nach {current_race_number}/17 Rennen", font=regular, fill=(255, 255, 255, 255), anchor="lm")

    #Positionspfeile
    arrow_up = Image.open("./images/arrow_up.png").convert("RGBA")
    arrow_down = Image.open("./images/arrow_down.png").convert("RGBA")
    arrow_up= arrow_up.resize(arrow_scale)
    arrow_down= arrow_down.resize(arrow_scale)


    ### Fill Positions
    position = 0
    for team in team_standings:
        #Text zu CAPS
        name = team[0]            
        drivers = team[1]
        flag = team[2]
        team_filename = get_team_logo(name)
        
        # Draw the rest of row     
        bbox = draw.textbbox((-100, -100), name, font=regular)
        name_length = bbox[2] - bbox[0]
                
        last_race_index = last_race_standings.index(next(entry for entry in last_race_standings if entry[0] == team[0]))   
        if(position == 0):
            #Draw Position
            draw.text((team_wm_position_x, team_wm_first_name_y + (position * y_offset)), str(position + 1), font=position_font, fill=(0, 0, 0, 255), anchor="lb")            
            #Draw Flag
            flag_image = Image.open("./flags/" + flag + ".png").convert("RGBA")
            flag_image = flag_image.resize((flag_width, flag_height))
            final_image.paste(flag_image, (team_wm_left_allignment_x, team_wm_first_name_y + (position * y_offset) - flag_y_offset), flag_image)
            #Team Name
            draw.text((team_wm_left_allignment_x + flag_width + spacer, team_wm_first_name_y + (position * y_offset)), name.upper(), font=bold, fill=(0, 0, 0, 255), anchor="lb")            
            #Fahrer namen
            draw.text((team_wm_team_x , team_wm_team_y + (position * y_offset)), drivers.upper(), font=regular, fill=(0, 0, 0, 255), anchor="lm")
            #Team Logo
            logo = Image.open("./team_logos/" + team_filename).convert("RGBA")
            logo = logo.resize(team_wm_team_logo_scaled)
            # Paste images onto the final image at specified positions
            final_image.paste(logo, (team_wm_team_logo[0], team_wm_team_logo[1] + (position * y_offset)), logo)
            draw = ImageDraw.Draw(final_image)
            #Points
            if(team[-1] % 1) < 0.5:
                draw.text((team_wm_points_pos[0], team_wm_points_pos[1] + (position * y_offset)), str(math.floor(team[-1])), font=pos_bold, fill=(0, 0, 0, 255), anchor="rm")
            else:
                draw.text((team_wm_points_pos[0], team_wm_points_pos[1] + (position * y_offset)), str(math.ceil(team[-1])), font=pos_bold, fill=(0, 0, 0, 255), anchor="rm")

            #Position gained?
            if (last_race_index > 1):
                # Paste images onto the final image at specified positions
                final_image.paste(arrow_up, (team_wm_arrow_x, team_wm_first_row_lower - row_height + ((row_height - arrow_scale[1]) % 2) + (position * y_offset) + 7), arrow_up)
                draw = ImageDraw.Draw(final_image)
        else:
            #Draw Position
            draw.text((team_wm_position_x, team_wm_first_name_y + (position * y_offset)), str(position + 1), font=position_font, fill=(255, 255, 255, 255), anchor="lb")            
            #Draw Flag
            flag_image = Image.open("./flags/" + flag + ".png").convert("RGBA")
            flag_image = flag_image.resize((flag_width, flag_height))
            final_image.paste(flag_image, (team_wm_left_allignment_x, team_wm_first_name_y + (position * y_offset) - flag_y_offset), flag_image)
            #Team Name
            draw.text((team_wm_left_allignment_x + flag_width + spacer, team_wm_first_name_y + (position * y_offset)), name.upper(), font=bold, fill=(255, 255, 255, 255), anchor="lb")            
            #Fahrer namen
            draw.text((team_wm_team_x , team_wm_team_y + (position * y_offset)), drivers.upper(), font=regular, fill=(255, 255, 255, 255), anchor="lm")
            #Team Logo
            logo = Image.open("./team_logos/" + team_filename).convert("RGBA")
            logo = logo.resize(team_wm_team_logo_scaled)
            # Paste images onto the final image at specified positions
            final_image.paste(logo, (team_wm_team_logo[0], team_wm_team_logo[1] + (position * y_offset)), logo)
            draw = ImageDraw.Draw(final_image)
            #Points
            if(team[-1] % 1) < 0.5:
                draw.text((team_wm_points_pos[0], team_wm_points_pos[1] + (position * y_offset)), str(math.floor(team[-1])), font=pos_bold, fill=(255, 255, 255, 255), anchor="rm")
            else:
                draw.text((team_wm_points_pos[0], team_wm_points_pos[1] + (position * y_offset)), str(math.ceil(team[-1])), font=pos_bold, fill=(255, 255, 255, 255), anchor="rm")
            #Pos Gained arrow
                if (last_race_index > position):
                    # Paste images onto the final image at specified positions
                    final_image.paste(arrow_up, (team_wm_arrow_x, team_wm_first_row_lower - row_height + ((row_height - arrow_scale[1]) % 2) + (position * y_offset) + 7), arrow_up)
                    draw = ImageDraw.Draw(final_image)
                elif (last_race_index < position):
                    # Paste images onto the final image at specified positions
                    final_image.paste(arrow_down, (team_wm_arrow_x, team_wm_first_row_lower - row_height + ((row_height - arrow_scale[1]) % 2) + (position * y_offset) + 7), arrow_down)
                    draw = ImageDraw.Draw(final_image)

        # Update position for the next name
        position += 1


    final_image.save("output/Team_WM.png", format="PNG")
    print("Image saved as Team_WM.png")

if __name__ == "__main__":

    read_raceresult_xml()
    read_driver_config()

    with open("configs/Race_Names.csv", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile)        
        race_titels = list(csvreader)
        if(len(race_titels) < current_race_number):
            print("Mehr Rennergebnis.xml als Renntitel in Race_Names.csv")
        else:
            name_rennen = race_titels[current_race_number - 1][0]        

    winner, fastest_lap_driver = result_preprocessing()    
    print(fastest_lap_driver)
    
    # create badges for betreuer
    fahrer_seite1 = rennergebnis[:12]  # First 11 entries for page 1
    fahrer_seite2 = rennergebnis[12:]  # Next 11 entries for page 2    
    create_rennergebnis_page_1(fahrer_seite1)
    create_insta_rennergebnis_page_1(fahrer_seite1)
    create_rennergebnis_page_2(fahrer_seite2)
    create_insta_rennergebnis_page_2(fahrer_seite2)
    calculate_wm_rankings()
    
    read_driver_config()
    read_quali_xml()
    quali_preprocessing()
    create_quali_page_1(qualiergebnis[:12])
    create_insta_quali_page_1(qualiergebnis[:12])
    create_quali_page_2(qualiergebnis[12:])
    create_insta_quali_page_2(qualiergebnis[12:])
