import os
import re
import csv
import datetime
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET


class Winner:
    def __init__(self, winner_data=[], finish_time=""):
        if not (winner_data == []):
            self.Vorname = winner_data[0]
            self.Nachname = winner_data[1]
            self.Nummer = winner_data[2]
            self.Team = winner_data[3]
            self.winning_team = self.get_team_short()
            self.Nation = winner_data[4]
            self.Overall = winner_data[5]
            self.Stammfahrer = winner_data[6]
            self.finish_time = finish_time

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

fastest_lap_position = (556, 1006)
lastname_size = 30
flag_width = 40
flag_height = 26
flag_y_offset = 22
spacer = 10
team_logo_alignment = 1070
team_name_allignment = 1165
race_time_allignment = 1700
overall_position = (-50, 130)

points_pos_x = 1811
position_size = 24

winner_team_position = (86, 132)
winner_number_position = (450, 132)
winner_team_size = 55
winner_name_pos = (288, 770)
winner_name_size = 42
winner = Winner([])
fastest_lap_driver = fastest_lap()

name_rennen = "Name des Rennens"

# Load a font (optional: use default if you don't have one)
race_titel = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=34)
race_classification = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=56)
regular = ImageFont.truetype("./fonts/Formula1-Regular_web.ttf", size=name_size)
position_font = ImageFont.truetype("./fonts/Formula1-Regular_web.ttf", size=24)
winner_team_font = ImageFont.truetype("./fonts/Formula1-Wide_web.ttf", size=winner_team_size)
winner_name_font = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=winner_name_size)
bold = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=lastname_size)
pos_bold = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=position_size)

### Arrays
xml_export = []
driver_config = []
rennergebnis = []
fastest_laps = []



def create_rennergebnis_page_1(data, filename="rennergebnisse_seite1.png"):
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
    temp_draw.text((0, 0), winner.winning_team, font=winner_team_font, fill=(255, 255, 255, 76), anchor="lt")

    # Rotate the temporary image 90 degrees counter-clockwise
    rotated_text = temp_img.rotate(90, expand=True)
    final_image.paste(rotated_text, winner_team_position, rotated_text)

    #Winner rotated number text
    team_box = draw.textbbox((-100, -100), winner.Nummer, font=winner_team_font)
    temp_img = Image.new("RGBA", (team_box[2] - team_box[0], team_box[3] - team_box[1]), (0, 0, 0, 0))  # Big enough for horizontal text
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((0, 0), winner.Nummer, font=winner_team_font, fill=(255, 255, 255, 76), anchor="lt")

    # Rotate the temporary image 90 degrees counter-clockwise
    rotated_text = temp_img.rotate(90, expand=True)
    final_image.paste(rotated_text, winner_number_position, rotated_text)
    
    ### Winner Name
    draw.text(winner_name_pos, winner.Nachname.upper(), font=winner_name_font, fill=(255, 255, 255, 255), anchor="mm")
    
    ### Fill Positions
    position = 0
    for entry in data:
        #Text zu CAPS
        name = entry[0][0]            
        lastname = entry[0][1].upper()
        team = entry[0][3].upper()
        flag = entry[0][4]        
        driver_time = entry[1]
        
        # Draw the rest of row     
        bbox = draw.textbbox((-100, -100), name, font=regular)
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
            flag_image = Image.open("./flags/" + flag + ".png").convert("RGBA")
            flag_image = flag_image.resize((flag_width, flag_height))
            final_image.paste(flag_image, (left_allignment, first_name + (position * y_offset) - flag_y_offset), flag_image)
            #Vorname
            draw.text((left_allignment + flag_width + spacer, first_name + (position * y_offset)), name, font=regular, fill=(0, 0, 0, 255), anchor="lb")
            #Nachname
            draw.text((left_allignment  + flag_width + spacer + name_length + spacer, first_name + (position * y_offset)), lastname, font=bold, fill=(0, 0, 0, 255), anchor="lb")
            #Teamname
            draw.text((team_name_allignment , first_team_and_points + (position * y_offset)), team, font=regular, fill=(0, 0, 0, 255), anchor="lm")
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
            flag_image = Image.open("./flags/" + flag + ".png").convert("RGBA")
            flag_image = flag_image.resize((flag_width, flag_height))
            final_image.paste(flag_image, (left_allignment, first_name + (position * y_offset) - flag_y_offset), flag_image)
            #Vorname
            draw.text((left_allignment + flag_width + spacer, first_name + (position * y_offset)), name, font=regular, fill=(255, 255, 255, 255), anchor="lb")
            #Nachname
            draw.text((left_allignment  + flag_width + spacer + name_length + spacer, first_name + (position * y_offset)), lastname, font=bold, fill=(255, 255, 255, 255), anchor="lb")
            #Teamname
            draw.text((team_name_allignment , first_team_and_points + (position * y_offset)), team, font=regular, fill=(255, 255, 255, 255), anchor="lm")
            #Zeit
            if (driver_time == "DNS"):
                draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), "DNS", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            elif (driver_time == "DNF"):
                draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), "DNF", font=regular, fill=(255, 255, 255, 255), anchor="rm")            
            elif ("Lap" in driver_time):
                draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), driver_time, font=regular, fill=(255, 255, 255, 255), anchor="rm")
            else:
                time_behind_leader = float(driver_time) - float(winner.finish_time)
                if(time_behind_leader < 10):
                    draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), f"+0{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
                else:
                    draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), f"+{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            #Points
            draw.text((points_pos_x, first_team_and_points + (position * y_offset)), gained_points, font=pos_bold, fill=(255, 255, 255, 255), anchor="rm")

        # Update position for the next name
        position += 1

    ### Draw fsatess Lap
    bbox = draw.textbbox((-100, -100), "FASTEST LAP", font=regular)
    name_length = bbox[2] - bbox[0]
    draw.text(fastest_lap_position, "FASTEST LAP", font=regular, fill=(255, 0, 255, 255), anchor="lm")
    draw.text((fastest_lap_position[0] + name_length + spacer + 5, fastest_lap_position[1]), f"{fastest_lap_driver.Nachname}     {fastest_lap_driver.Team}     {fastest_lap_driver.get_laptime_formatted()}     (+1 Point)", font=regular, fill=(255, 255, 255, 255), anchor="lm")

    # Save the final image
    final_image.save(filename, format="PNG")
    print("Image saved as "+ filename)

def create_rennergebnis_page_2(data, filename="rennergebnisse_seite2.png"):
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
    temp_draw.text((0, 0), winner.winning_team, font=winner_team_font, fill=(255, 255, 255, 76), anchor="lt")

    # Rotate the temporary image 90 degrees counter-clockwise
    rotated_text = temp_img.rotate(90, expand=True)
    final_image.paste(rotated_text, winner_team_position, rotated_text)

    #Winner rotated number text
    team_box = draw.textbbox((-100, -100), winner.Nummer, font=winner_team_font)
    temp_img = Image.new("RGBA", (team_box[2] - team_box[0], team_box[3] - team_box[1]), (0, 0, 0, 0))  # Big enough for horizontal text
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((0, 0), winner.Nummer, font=winner_team_font, fill=(255, 255, 255, 76), anchor="lt")

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
    #Zeit
    td = datetime.timedelta(seconds=float(winner.finish_time))
    # Format as mm:ss.SSS
    minutes, sec = divmod(td.total_seconds(), 60)
    formatted = f"{int(minutes):02}:{sec:06.3f}"
    draw.text((race_time_allignment , first_name + (position * y_offset)), formatted, font=regular, fill=(0, 0, 0, 255), anchor="rb")
    #Points
    draw.text((points_pos_x, first_name + (position * y_offset)), "+25", font=pos_bold, fill=(0, 0, 0, 255), anchor="rb")


    ### Fill Positions
    position = 1
    for entry in data:
        #Text zu CAPS
        name = entry[0][0]            
        lastname = entry[0][1].upper()
        team = entry[0][3].upper()
        flag = entry[0][4]        
        driver_time = entry[1]
        
        # Draw the rest of row     
        bbox = draw.textbbox((-100, -100), name, font=regular)
        name_length = bbox[2] - bbox[0]
                
        gained_points = "+0"
        
        #Draw Position
        draw.text((position_text, first_name + (position * y_offset)), str(position + 12), font=position_font, fill=(255, 255, 255, 255), anchor="lb")            
        #Draw Flag
        flag_image = Image.open("./flags/" + flag + ".png").convert("RGBA")
        flag_image = flag_image.resize((flag_width, flag_height))
        final_image.paste(flag_image, (left_allignment, first_name + (position * y_offset) - flag_y_offset), flag_image)
        #Vorname
        draw.text((left_allignment + flag_width + spacer, first_name + (position * y_offset)), name, font=regular, fill=(255, 255, 255, 255), anchor="lb")
        #Nachname
        draw.text((left_allignment  + flag_width + spacer + name_length + spacer, first_name + (position * y_offset)), lastname, font=bold, fill=(255, 255, 255, 255), anchor="lb")
        #Teamname
        draw.text((team_name_allignment , first_team_and_points + (position * y_offset)), team, font=regular, fill=(255, 255, 255, 255), anchor="lm")
        #Zeit
        if (driver_time == "DNS"):
            draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), "DNS", font=regular, fill=(255, 255, 255, 255), anchor="rm")
        elif (driver_time == "DNF"):
            draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), "DNF", font=regular, fill=(255, 255, 255, 255), anchor="rm")            
        elif ("Lap" in driver_time):
            draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), driver_time, font=regular, fill=(255, 255, 255, 255), anchor="rm")
        else:
            time_behind_leader = float(driver_time) - float(winner.finish_time)
            if(time_behind_leader < 10):
                draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), f"+0{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            else:
                draw.text((race_time_allignment , first_team_and_points + (position * y_offset)), f"+{(time_behind_leader):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
        #Points
        draw.text((points_pos_x, first_team_and_points + (position * y_offset)), gained_points, font=pos_bold, fill=(255, 255, 255, 255), anchor="rm")

        # Update position for the next name
        position += 1

    ### Draw fsatess Lap
    bbox = draw.textbbox((-100, -100), "FASTEST LAP", font=regular)
    name_length = bbox[2] - bbox[0]
    draw.text(fastest_lap_position, "FASTEST LAP", font=regular, fill=(255, 0, 255, 255), anchor="lm")
    draw.text((fastest_lap_position[0] + name_length + spacer + 5, fastest_lap_position[1]), f"{fastest_lap_driver.Nachname}     {fastest_lap_driver.Team}     {fastest_lap_driver.get_laptime_formatted()}     (+1 Point)", font=regular, fill=(255, 255, 255, 255), anchor="lm")


    

    # Save the final image
    final_image.save(filename, format="PNG")
    print("Image saved as "+ filename)

def read_raceresult_xml():
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

        if (category_elem is None) or not ("F1S13" in category_elem.text):                        
            continue

        if (finished is None):
            print("finished ist None")
            continue
        
        if fastes_lap is None:
            fastes_lap = "1000"
        else:
            fastes_lap = fastes_lap.text

        if finished.text == "None":
            xml_export.append((name_elem.text, position.text, "DNS", fastes_lap))
            continue

        if finished.text == "DNF":
            xml_export.append((name_elem.text, position.text, "DNF", fastes_lap))
            continue

        if int(finished_laps.text) < int(race_laps.text):
            if (int(race_laps.text) - int(finished_laps.text) == 1):
                xml_export.append((name_elem.text, position.text, "+1 Lap", fastes_lap))
            else:
                xml_export.append((name_elem.text, position.text, f"+ {int(race_laps.text) - int(finished_laps.text)} Laps", fastes_lap))
            continue

        if finished.text == "Finished Normally":
            xml_export.append((name_elem.text, position.text, racetime.text, fastes_lap))
            continue    
    ### Sortiere nach Position
    xml_export.sort(key=lambda x: int(x[1]))  # Sort by position

def read_driver_config():       
    # read driver_config.csv
    with open("driver_config.csv", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=";")
        # skip header1
        next(csvreader)

        for row in csvreader:
            if row == []:
                continue            
            driver_config.append(row)    

def result_preprocessing():
    ### get sorted Race Result with config file ###   
    fastest = fastest_lap()
    for entry in xml_export:
        found = False
        for config in driver_config:
            if (config[0] + " " + config[1]).upper() == entry[0].upper():                
                rennergebnis.append([config, entry[2]])                                            
                driver_config.remove(config)
                found = True         
                if(float(entry[3]) < float(fastest.lap_time)):
                    fastest = fastest_lap(config[0], config[1], config[3], entry[3])
                break
        if not found:
            print("Kein Eintrag für " + entry[0] + " gefunden!")   
    
    print("Fertig mit der Ergebnisverarbeitung.")
    return Winner(rennergebnis[0][0], rennergebnis[0][1]), fastest

if __name__ == "__main__":

    read_raceresult_xml()
    read_driver_config()
    winner, fastest_lap_driver = result_preprocessing() 
    name_rennen = "FORMULA 1 BROS LEAGUE rF2 EIFEL GRAND PRIX 2024"
    
    # create badges for betreuer
    fahrer_seite1 = rennergebnis[:12]  # First 11 entries for page 1
    fahrer_seite2 = rennergebnis[12:]  # Next 11 entries for page 2    
    create_rennergebnis_page_1(fahrer_seite1)
    create_rennergebnis_page_2(fahrer_seite2)
    
