import json

from kivymd.app import MDApp
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.dialog import MDDialog
from kivymd.theming import ThemeManager

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen


class MainMenuScreen(Screen):
    pass


class CalendarMenuScreen(Screen):
    pass


class WorkoutMenuScreen(Screen):
    pass


class AddWorkoutScreen(Screen):
    pass


class WaterMenuScreen(Screen):
    pass


class FoodMenuScreen(Screen):
    pass


class GoalsMenuScreen(Screen):
    pass


class SettingMenuScreen(Screen):
    pass


class ColorSettingScreen(Screen):
    pass


class WorkoutApp(MDApp):
    theme_cls = ThemeManager()

    def build(self):
        global settings
        global workouts
        settings = self.get_settings()
        workouts = self.get_workouts()
        self.theme_cls.theme_style = settings["color_scheme"]["theme_style"]
        self.theme_cls.primary_palette = settings["color_scheme"]["primary_palette"]
        self.theme_cls.primary_hue = settings["color_scheme"]["primary_hue"]

    def get_settings(self):
        with open("settings.json", 'r') as f:
            settings = json.load(f)
        f.close()
        return settings

    def change_color(self, primary):
        settings["color_scheme"]["primary_palette"] = primary
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)
        f.close()
        self.build()

    def get_workouts(self):
        with open('workouts.json', 'r') as f:
            workouts = json.load(f)
        f.close()
        return workouts

    def create_new_workout(self):
        new_workout = {}
        for i in range(int(self.root.ids.add_workout.ids.number_exercises.text)):
            new_exercise, info = self.add_exercise(i)
            new_workout[new_exercise] = info
        self.add_workout(
            self.root.ids.add_workout.ids.workout_name.text, new_workout)

    def add_exercise(self, x):
        print(str(x) + "in add_exercise")
        name = str(x)
        stuff = {"timer": 0.0,
                 "counterr": 0}
        # change to new popup, ask for the name of the exercise, ask if timer or counter,
        # get timer (float) or counter (int), submit button that adds to json file under the workout
        # *MAYBE USE MDDIALOG???*
        return name, stuff

    def add_workout(self, name, exercises):
        workouts[name] = exercises
        with open("workouts.json", "w") as f:
            json.dump(workouts, f, indent=4)
        f.close()

    '''
    def show_alert_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="test",
                text="Second Line",
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                    MDFlatButton(
                        text="DISCARD",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                    ),
                ],
            )
        self.dialog.open()

    def show_dateppicker(self):
        picker = MDDatePicker(callback=self.got_date)
        picker.open()

    def got_date(self, the_date):
        print(the_date)
        print(the_date.year)
        print(the_date.month)
        print(the_date.day)
    '''


if __name__ == '__main__':
    WorkoutApp().run()
