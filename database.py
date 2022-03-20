import sqlite3
import os
import shutil


app_data_location = os.path.join(os.getenv('APPDATA'), 'MkReman', 'ScreenShotJoin')
if not os.path.exists(os.path.join(app_data_location, 'DataBase.db')):
    os.makedirs(app_data_location)
    shutil.copy('./DataBase.db', os.path.join(app_data_location, 'DataBase.db'))

conn = sqlite3.connect(os.path.join(app_data_location, 'DataBase.db'))

c = conn.cursor()
# c.execute("""CREATE TABLE meta_values (
#             Variables text,
#             Entries text
#             )""")
# c.execute("""CREATE TABLE LightTheme (
#             Variables text,
#             Entries text
#             )""")
# c.execute("""CREATE TABLE DarkTheme (
#             Variables text,
#             Entries text
#             )""")


def get_variable_values():
    return {x[0]: x[1] for x in c.execute("SELECT * from meta_values")}


def get_theme_values(theme):
    return {x[0]: x[1] for x in c.execute(f"SELECT * from {theme}")}


class Database:
    font_list = sorted(['Arial', 'Cambria', 'Segoe UI', 'Segoe Script', 'Sitka Text', 'Times New Roman',
                        'Imprint MT Shadow'])

    @staticmethod
    def insert_meta_value(variable, entry):
        with conn:
            c.execute("INSERT INTO meta_values VALUES (:variable, :entry)", {'variable': variable,
                                                                             'entry': entry})

    @staticmethod
    def update_meta_value(variable, entry):
        with conn:
            c.execute(f"UPDATE meta_values SET Entries = '{entry}' WHERE Variables = '{variable}'")

    @staticmethod
    def remove_meta_values(variable):
        with conn:
            c.execute("DELETE from meta_values WHERE Variables = :variable", {'variable': variable})

    @staticmethod
    def insert_theme_value(theme, variable, entry):
        with conn:
            command = f"INSERT INTO {theme} VALUES (:variable, :entry)"
            c.execute(command, {'variable': variable, 'entry': entry})

    @staticmethod
    def update_theme_value(theme, variable, entry):
        with conn:
            command = f"UPDATE {theme} SET entries = :entry WHERE Variables = :variable"
            c.execute(command, {'variable': variable, 'entry': entry})

    @staticmethod
    def remove_theme_value(theme, variable):
        with conn:
            command = f"DELETE from {theme} WHERE Variables = :variable"
            c.execute(command, {'variable': variable})


# Database.insert_meta_value('theme', 'LightTheme')
# Database.insert_meta_value('output_dir', os.path.join(os.path.expanduser('~'), 'Pictures', 'ScreenShotJoin'))

# Database.insert_theme_value('LightTheme', 'fg_color', '#000000')
# Database.insert_theme_value('LightTheme', 'entry_bg_color', '#f2f2f2')
# Database.insert_theme_value('LightTheme', 'bg_color', '#c0c0c0')
# Database.insert_theme_value('LightTheme', 'font', 'Cambria')
# Database.insert_theme_value('LightTheme', 'button_size', '12')
# Database.insert_theme_value('LightTheme', 'font_size', '14')
#
# Database.insert_theme_value('DarkTheme', 'fg_color', '#ffffff')
# Database.insert_theme_value('DarkTheme', 'entry_bg_color', '#525252')
# Database.insert_theme_value('DarkTheme', 'bg_color', '#404040')
# Database.insert_theme_value('DarkTheme', 'font', 'Cambria')
# Database.insert_theme_value('DarkTheme', 'button_size', '12')
# Database.insert_theme_value('DarkTheme', 'font_size', '14')
