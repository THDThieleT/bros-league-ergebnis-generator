import os
import re
import csv
import datetime
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET

#Setup Variables

width, height = 1920, 1080
y_offset = 62
first_name = 302 #310 unterseite erste Zeile
position_text = 556
left_allignment = 620
name_size = 20

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
winner_team_size = 55
winner_name_pos = (288, 770)
winner_name_size = 42

# Load a font (optional: use default if you don't have one)
race_titel = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=34)
race_classification = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=56)
regular = ImageFont.truetype("./fonts/Formula1-Regular_web.ttf", size=name_size)
position_font = ImageFont.truetype("./fonts/Formula1-Regular_web.ttf", size=24)
winner_team_font = ImageFont.truetype("./fonts/Formula1-Wide_web.ttf", size=winner_team_size)
winner_name_font = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=winner_name_size)
bold = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=lastname_size)
pos_bold = ImageFont.truetype("./fonts/Formula1-Bold_web.ttf", size=position_size)




def create_rennergebnis_page_1(data, race_time, filename="rennergebnisse_seite1.png"):
    # Create a transparent base image (RGBA mode)  
    final_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # Fully transparent

    # Example: Load images to add (ensure these support transparency or convert them)
    background = Image.open("./images/Rennergebnis_Hintergrund.png").convert("RGBA")

    # Paste images onto the final image at specified positions
    final_image.paste(background, (0, 0), background)  # The third argument is the mask for transparency

    # Add text
    draw = ImageDraw.Draw(final_image)

    # Draw text with semi-transparency
    draw.text((557, 134), "FORMULA 1 BROS LEAGUE rF2 EIFEL GRAND PRIX 2024", font=race_titel, fill=(255, 255, 255, 255), anchor="lt")
    draw.text((557, 193), "RACE CLASSIFICATION", font=race_classification, fill=(167, 169, 171, 255), anchor="lt")

    #Draw race winner
    winner_filename = data[0][1].replace(" ", "_").upper() + ".png"
    winner_overall = Image.open("./overalls/" + winner_filename).convert("RGBA")
    winner_overall = winner_overall.resize((680, 680))
    final_image.paste(winner_overall, overall_position, winner_overall)

    overall_fade = Image.open("./images/Winner_Vordergrund.png").convert("RGBA")
    final_image.paste(overall_fade, (0,0), overall_fade)
    
    #Winner rotated team text
    winner_team = data[0][2].split(" ")[0].upper()
    team_box = draw.textbbox((-100, -100), winner_team, font=winner_team_font)
    temp_img = Image.new("RGBA", (team_box[2] - team_box[0], team_box[3] - team_box[1]), (0, 0, 0, 0))  # Big enough for horizontal text
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((0, 0), winner_team, font=winner_team_font, fill=(255, 255, 255, 76), anchor="lt")

    # Rotate the temporary image 90 degrees counter-clockwise
    rotated_text = temp_img.rotate(90, expand=True)
    final_image.paste(rotated_text, winner_team_position, rotated_text)
    
    ### Winner Name
    draw.text(winner_name_pos, data[0][1].upper(), font=winner_name_font, fill=(255, 255, 255, 255), anchor="mm")
    
    ### Fill Positions
    position = 0
    winner_final_time = race_time[0]
    for name, lastname, number, team, flag, overall, stammpilot in data:
        #Text zu CAPS
        lastname = lastname.upper()
        team = team.upper()
        
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
            draw.text((team_name_allignment , first_name + (position * y_offset)), team, font=regular, fill=(0, 0, 0, 255), anchor="lb")
            #Zeit
            td = datetime.timedelta(seconds=winner_final_time)
            # Format as mm:ss.SSS
            minutes, sec = divmod(td.total_seconds(), 60)
            formatted = f"{int(minutes):02}:{sec:06.3f}"
            draw.text((race_time_allignment , first_name + (position * y_offset)), formatted, font=regular, fill=(0, 0, 0, 255), anchor="rm")
            #Points
            draw.text((points_pos_x, first_name + (position * y_offset)), gained_points, font=pos_bold, fill=(0, 0, 0, 255), anchor="rm")
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
            draw.text((team_name_allignment , first_name + (position * y_offset)), team, font=regular, fill=(255, 255, 255, 255), anchor="lb")
            #Zeit
            if(race_time[position] == 0.0):
                draw.text((race_time_allignment , first_name + (position * y_offset)), "DNS", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            else:
                draw.text((race_time_allignment , first_name + (position * y_offset)), f"+{(race_time[position] - winner_final_time):.3f}", font=regular, fill=(255, 255, 255, 255), anchor="rm")
            #Points
            draw.text((points_pos_x, first_name + (position * y_offset)), gained_points, font=pos_bold, fill=(255, 255, 255, 255), anchor="rm")

        # Update position for the next name
        position += 1

    

    # Save the final image
    final_image.save(filename, format="PNG")
    print("Image saved as "+ filename)

def create_rennergebnis_page_2(winner, data, filename="rennergebnisse_seite2.png"):
    # Create a transparent base image (RGBA mode)
    
    
    
    final_image = Image.new("RGBA", (width, height), (0, 0, 0, 0))  # Fully transparent

    # Example: Load images to add (ensure these support transparency or convert them)
    background = Image.open("./images/Rennergebnis_Hintergrund_2.png").convert("RGBA")

    # Paste images onto the final image at specified positions
    final_image.paste(background, (0, 0), background)  # The third argument is the mask for transparency

    # Add text
    draw = ImageDraw.Draw(final_image)

    # Draw text with semi-transparency
    draw.text((557, 134), "FORMULA 1 BROS LEAGUE rF2 EIFEL GRAND PRIX 2024", font=race_titel, fill=(255, 255, 255, 255), anchor="lt")
    draw.text((557, 193), "RACE CLASSIFICATION", font=race_classification, fill=(167, 169, 171, 255), anchor="lt")

    #Draw race winner
    winner_filename = winner[1].replace(" ", "_").upper() + ".png"
    winner_overall = Image.open("./overalls/" + winner_filename).convert("RGBA")
    winner_overall = winner_overall.resize((680, 680))
    final_image.paste(winner_overall, overall_position, winner_overall)

    overall_fade = Image.open("./images/Winner_Vordergrund.png").convert("RGBA")
    final_image.paste(overall_fade, (0,0), overall_fade)
    
    #Winner rotated team text
    winner_team = winner[2].split(" ")[0].upper()
    team_box = draw.textbbox((-100, -100), winner_team, font=winner_team_font)
    temp_img = Image.new("RGBA", (team_box[2] - team_box[0], team_box[3] - team_box[1]), (0, 0, 0, 0))  # Big enough for horizontal text
    temp_draw = ImageDraw.Draw(temp_img)
    temp_draw.text((0, 0), winner_team, font=winner_team_font, fill=(255, 255, 255, 76), anchor="lt")

    # Rotate the temporary image 90 degrees counter-clockwise
    rotated_text = temp_img.rotate(90, expand=True)
    final_image.paste(rotated_text, winner_team_position, rotated_text)
    
    ### Winner Name
    draw.text(winner_name_pos, winner[1].upper(), font=winner_name_font, fill=(255, 255, 255, 255), anchor="mm")
    
    ### Fill Positions
    position = 0
    
    #Draw Winner row
    #Text zu CAPS
    name = winner[0]
    lastname = winner[1].upper()
    team = winner[2].upper()
    time = winner[3]
    flag = winner[4]
    
    
    #Draw Position
    draw.text((position_text, first_name + (position * y_offset)), "1", font=position_font, fill=(0, 0, 0, 255), anchor="lb")
    
    #Draw Flag
    flag_image = Image.open("./flags/" + flag + ".png").convert("RGBA")
    flag_image = flag_image.resize((flag_width, flag_height))
    final_image.paste(flag_image, (left_allignment, first_name + (position * y_offset) - flag_y_offset), flag_image)
    
    
    # Draw the rest of row     
    bbox = draw.textbbox((-100, -100), name, font=regular)
    name_length = bbox[2] - bbox[0]
    
    #Vorname
    draw.text((left_allignment + flag_width + spacer, first_name + (position * y_offset)), name, font=regular, fill=(0, 0, 0, 255), anchor="lb")
    #Nachname
    draw.text((left_allignment  + flag_width + spacer + name_length + spacer, first_name + (position * y_offset)), lastname, font=bold, fill=(0, 0, 0, 255), anchor="lb")
    #Teamname
    draw.text((team_name_allignment , first_name + (position * y_offset)), team, font=regular, fill=(0, 0, 0, 255), anchor="lb")
    #Zeit
    draw.text((race_time_allignment , first_name + (position * y_offset)), time, font=regular, fill=(0, 0, 0, 255), anchor="rm")
    #Points
    draw.text((points_pos_x, first_name + (position * y_offset)), "+25", font=pos_bold, fill=(0, 0, 0, 255), anchor="rm")
            
    position += 1
    
    for name, lastname, team, time, flag in data:
        #Text zu CAPS
        lastname = lastname.upper()
        team = team.upper()
        
        # Draw the rest of row     
        bbox = draw.textbbox((-100, -100), name, font=regular)
        name_length = bbox[2] - bbox[0]

        #Draw Position
        draw.text((position_text, first_name + (position * y_offset)), str(position + 10), font=position_font, fill=(255, 255, 255, 255), anchor="lb")            
        #Draw Flag
        flag_image = Image.open("./flags/" + flag + ".png").convert("RGBA")
        flag_image = flag_image.resize((flag_width, flag_height))
        final_image.paste(flag_image, (left_allignment, first_name + (position * y_offset) - flag_y_offset), flag_image)
        #Vorname
        draw.text((left_allignment + flag_width + spacer, first_name + (position * y_offset)), name, font=regular, fill=(255, 255, 255, 255), anchor="lb")
        #Nachname
        draw.text((left_allignment  + flag_width + spacer + name_length + spacer, first_name + (position * y_offset)), lastname, font=bold, fill=(255, 255, 255, 255), anchor="lb")
        #Teamname
        draw.text((team_name_allignment , first_name + (position * y_offset)), team, font=regular, fill=(255, 255, 255, 255), anchor="lb")
        #Zeit
        draw.text((race_time_allignment , first_name + (position * y_offset)), time, font=regular, fill=(255, 255, 255, 255), anchor="rm")
        #Points
        draw.text((points_pos_x, first_name + (position * y_offset)), "+0", font=pos_bold, fill=(255, 255, 255, 255), anchor="rm")

        # Update position for the next name
        position += 1

    

    # Save the final image
    final_image.save(filename, format="PNG")
    print("Image saved as "+ filename)

if __name__ == "__main__":

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
        # ...weitere Verarbeitung...
    else:
        print("Keine passenden XML-Dateien gefunden.")

    ### Extract Drivers from XML ###
    xml_export = []
    for driver in root.findall('.//Driver'):
        name_elem = driver.find('Name')
        position = driver.find('Position')
        category_elem = driver.find('Category')
        racetime = driver.find('FinishTime')
        if category_elem is not None and "F1S13" in category_elem.text:                        
            if name_elem is not None and name_elem.text:
                if racetime is None:
                    racetime = "0.0"
                    xml_export.append((name_elem.text, position.text, racetime))
                else:
                    xml_export.append((name_elem.text, position.text, racetime.text))
    xml_export.sort(key=lambda x: int(x[1]))  # Sort by position

    ### get Driver config ###
    driver_config = []    
    # read driver_config.csv
    with open("driver_config.csv", encoding="utf-8") as csvfile:
        csvreader = csv.reader(csvfile, delimiter=";")

        # skip header1
        next(csvreader)

        for row in csvreader:
            if row == []:
                continue            
            driver_config.append(row)

    ### get sorted Race Result with config file ###
    rennergebnis = []    
    race_time = []
    for entry in xml_export:
        found = False
        for config in driver_config:
            if (config[0] + " " + config[1]).upper() == entry[0].upper():                
                rennergebnis.append(config)                
                race_time.append(float(entry[2]))
                driver_config.remove(config)
                found = True                                
                break
        if not found:
            print("Kein Eintrag für " + entry[0] + " gefunden!")            


    

    # create badges for betreuer
    fahrer_seite1 = rennergebnis[:10]  # First 10 entries for page 1
    fahrer_seite2 = rennergebnis[10:20]  # Next 10 entries for page 2
    create_rennergebnis_page_1(fahrer_seite1, race_time[:10])
    #create_rennergebnis_page_2(rennergebnis[0], fahrer_seite2)
    
