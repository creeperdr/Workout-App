import json

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineRightIconListItem
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
    starting = True
    theme_cls = ThemeManager()
    add_workout_dialog = None
    add_exercise_dialog = None

    def build(self):
        global settings
        global workouts
        settings = self.get_settings()
        workouts = self.get_workouts()
        self.theme_cls.theme_style = settings["color_scheme"]["theme_style"]
        self.theme_cls.primary_palette = settings["color_scheme"]["primary_palette"]
        self.theme_cls.primary_hue = settings["color_scheme"]["primary_hue"]
        self.after_start()

    def after_start(self):
        if self.starting:
            for i in range(len(workouts)):
                self.root.ids.workout_menu.ids['workout_container'].add_widget(WorkoutListItem(
                    text='[b]' + str(list(workouts.keys())[i]) + '[/b]', secondary_text=str(len(dict(list(workouts.values())[i]).keys())) + ' exercises'))
            self.starting = False
        else:
            pass

    def get_settings(self):
        with open("settings.json", 'r') as f:
            settings = json.load(f)
        f.close()
        return settings

    def get_workouts(self):
        with open('workouts.json', 'r') as f:
            workouts = json.load(f)
        f.close()
        return workouts

    def change_color(self, primary):
        settings["color_scheme"]["primary_palette"] = primary
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)
        f.close()
        self.build()

    def show_workout_dialog(self):
        if not self.add_workout_dialog:
            self.add_workout_dialog = MDDialog(
                type="custom",
                content_cls=WorkoutDialogContent(),
            )

        self.add_workout_dialog.open()

    def close_workout_dialog(self, *args):
        self.add_workout_dialog.dismiss()

    def create_new_workout(self, workout_name, number_exercises):
        new_workout = {}
        for i in range(int(number_exercises)):
            new_exercise, info = self.add_exercise(i)
            new_workout[new_exercise] = info
        self.add_workout(workout_name, new_workout)

    def show_exercise_dialog(self):
        if not self.add_exercise_dialog:
            self.add_exercise_dialog = MDDialog(
                type="custom",
                content_cls=ExerciseDialogContent(),
            )

        self.add_exercise_dialog.open()

    def add_exercise_field(self, checkbox, value):
        if value:
            print('timer')
            # add_widget timer text field
        else:
            print('reps')
            # add_widget reps text field

    def close_exercise_dialog(self, *args):
        self.add_exercise_dialog.dismiss()

    def add_exercise(self, x):
        name = str(x+1)
        stuff = {"timer": 0.0,
                 "counter": 0}
        self.show_exercise_dialog()
        # change to new popup, ask for the name of the exercise, ask if timer or counter,
        # get timer (float) or counter (int), submit button that adds to json file under the workout
        # *MAYBE USE MDDIALOG???*
        return name, stuff

    def add_workout(self, name, exercises):
        workouts[name] = exercises
        self.root.ids.workout_menu.ids['workout_container'].add_widget(WorkoutListItem(
            text='[b]' + name + '[/b]', secondary_text=str(len(exercises.keys())) + ' exercises'))
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


class WorkoutDialogContent(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class ExerciseDialogContent(MDBoxLayout):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class WorkoutListItem(TwoLineRightIconListItem):

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def delete_item(self, the_list_item):
        self.parent.remove_widget(the_list_item)
        # add delete from dictionary


if __name__ == '__main__':
    WorkoutApp().run()
