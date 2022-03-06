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


def get_variable_values():
    res = dict()
    for x in c.execute("SELECT * from meta_values"):
        res[x[0]] = x[1]
    return res


class Database:
    @staticmethod
    def insert_meta_value(variable, entry):
        with conn:
            c.execute("INSERT INTO meta_values VALUES (:variable, :entry)", {'variable': variable,
                                                                             'entry': entry})

    @staticmethod
    def update_meta_value(variable, entry):
        with conn:
            c.execute("""UPDATE meta_values SET Entries = :entry
                    WHERE Variables = :variable""",
                      {'variable': variable, 'entry': entry})

    @staticmethod
    def remove_meta_values(variable):
        with conn:
            c.execute("DELETE from meta_values WHERE Variables = :variable", {'variable': variable})


# Database.insert_meta_value('bg_color', '#c0c0c0')
# Database.insert_meta_value('fg_color', '#000000')
# Database.insert_meta_value('button_bg_color', '#808080')
# Database.insert_meta_value('font', 'Cambria')
# Database.insert_meta_value('output_dir', os.path.join(os.path.expanduser('~'), 'Pictures', 'ScreenShotJoin'))
