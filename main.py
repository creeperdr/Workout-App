from datetime import datetime
import json

from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton, MDRectangleFlatButton, MDIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.list import TwoLineRightIconListItem
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.textfield import MDTextField
from kivymd.theming import ThemeManager

from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen


class MainMenuScreen(Screen):
    pass


class CalendarMenuScreen(Screen):
    pass


class WorkoutMenuScreen(Screen):
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
    water_dialog = None
    food_dialog = None

    def build(self):
        global settings
        settings = self.get_settings()
        global workouts
        workouts = self.get_workouts()
        global water
        water = self.get_water()
        global foods
        foods = self.get_foods()

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
            for i in range(len(water)):
                self.root.ids.water_menu.ids['water_container'].add_widget(WaterListItem(
                    text='[b]' + str(list(water.keys())[i]) + '[/b]', secondary_text=str(list(water.values())[i]) + ' gallons'))
            self.starting = False
            for i in range(len(foods)):
                self.root.ids.food_menu.ids['food_container'].add_widget(FoodListItem(
                    text='[b]' + str(list(foods.keys())[i]) + '[/b]', secondary_text=str(list(foods.values())[i]) + ' calories'))
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

    def get_water(self):
        with open('water.json', 'r') as f:
            water = json.load(f)
        f.close()
        return water

    def get_foods(self):
        with open('foods.json', 'r') as f:
            foods = json.load(f)
        f.close()
        return foods

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
                content_cls=WorkoutDialogContent())

        self.add_workout_dialog.open()

    def close_workout_dialog(self):
        self.add_workout_dialog.dismiss()
        self.add_workout_dialog = None

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

#    def add_exercise_field(self, checkbox, value):
#        if value:
#            print('timer')
#            self.add_exercise_dialog.add_widget(ExerciseListItem())
#            self.add_exercise_dialog.add_widget(ExerciseListItem())
#        else:
#            print('reps')
        # add_widget reps text field

    def close_exercise_dialog(self, *args):
        self.add_exercise_dialog.dismiss()

    def add_exercise(self, x):
        name = str(x+1)
        stuff = {"timer": 0.0,
                 "counter": 0}
        # self.show_exercise_dialog()
        # change to new popup, ask for the name of the exercise, ask if timer or counter,
        # get timer (float) or counter (int), submit button that adds to json file under the workout
        return name, stuff

    def add_workout(self, name, exercises):
        workouts[name] = exercises
        self.root.ids.workout_menu.ids['workout_container'].add_widget(WorkoutListItem(
            text='[b]' + name + '[/b]', secondary_text=str(len(exercises.keys())) + ' exercises'))
        with open("workouts.json", "w") as f:
            json.dump(workouts, f, indent=4)
        f.close()

    def show_water_dialog(self):
        if not self.water_dialog:
            self.water_dialog = MDDialog(
                title="Add water to log",
                type="custom",
                content_cls=WaterDialogContent())

        self.water_dialog.open()

    def add_water(self, date, gallons_consumed):
        water[str(date)] = int(gallons_consumed)
        with open("water.json", "w") as f:
            json.dump(water, f, indent=4)
        f.close()
        self.root.ids.water_menu.ids['water_container'].add_widget(WaterListItem(
            text='[b]' + date + '[/b]', secondary_text=gallons_consumed + ' gallon'))

    def close_water_dialog(self):
        self.water_dialog.dismiss()
        self.water_dialog = None

    def show_food_dialog(self):
        if not self.food_dialog:
            self.food_dialog = MDDialog(
                title="Add calories to log",
                type="custom",
                content_cls=FoodDialogContent())

        self.food_dialog.open()

    def add_food(self, date, calories_consumed):
        foods[str(date)] = int(calories_consumed)
        with open("foods.json", "w") as f:
            json.dump(foods, f, indent=4)
        f.close()
        self.root.ids.food_menu.ids['food_container'].add_widget(FoodListItem(
            text='[b]' + date + '[/b]', secondary_text=calories_consumed + ' calories'))

    def close_food_dialog(self):
        self.food_dialog.dismiss()
        self.food_dialog = None

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


class WaterDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set the date_text label to today's date when useer first opens dialog box
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))

    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        """This functions gets the date from the date picker and converts its it a
        more friendly form then changes the date label on the dialog to that"""

        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)


class FoodDialogContent(MDBoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # set the date_text label to today's date when useer first opens dialog box
        self.ids.date_text.text = str(datetime.now().strftime('%A %d %B %Y'))

    def show_date_picker(self):
        """Opens the date picker"""
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        """This functions gets the date from the date picker and converts its it a
        more friendly form then changes the date label on the dialog to that"""

        date = value.strftime('%A %d %B %Y')
        self.ids.date_text.text = str(date)


class ExerciseListItem(MDTextField):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def delete_item(self, exercise_list_item):
        self.parent.remove_widget(exercise_list_item)


class WorkoutListItem(TwoLineRightIconListItem):
    # confirm_delete_dialog = None

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def delete_item(self, workout_list_item):
        left = workout_list_item.text.split('[')
        right = left[1].split(']')
        x = workouts.pop(right[1])
        with open("workouts.json", "w") as f:
            json.dump(workouts, f, indent=4)
        f.close()
        self.parent.remove_widget(workout_list_item)


        # add confirm dialog
'''
    def confirm_delete(self, workout_list_item):
        if not self.confirm_delete_dialog:
            self.confirm_delete_dialog = MDDialog(
                title="Confirm Workout Deletion",
                type="custom",
                content_cls=Content(),
                text='This will delte your workout forever, arre you sure you want to continue?',
                buttons=[
                    MDFlatButton(
                        text="CANCEL",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=self.close()
                    ),
                    MDFlatButton(
                        text="DELETE",
                        theme_text_color="Custom",
                        ext_color=self.theme_cls.primary_color,
                        on_release=self.delete_item(workout_list_item)
                    ),
                ]
            )
        self.confirm_delete_dialog.open()

    def close(self):
        print("close")
        # self.confirm_delete_dialog.dismiss()
'''


class WaterListItem(TwoLineRightIconListItem):

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def delete_item(self, water_list_item):
        left = water_list_item.text.split('[')
        right = left[1].split(']')
        x = water.pop(right[1])
        with open("water.json", "w") as f:
            json.dump(water, f, indent=4)
        f.close()
        self.parent.remove_widget(water_list_item)
        # add confirm dialog


class FoodListItem(TwoLineRightIconListItem):

    def __init__(self, pk=None, **kwargs):
        super().__init__(**kwargs)
        self.pk = pk

    def delete_item(self, food_list_item):
        left = food_list_item.text.split('[')
        right = left[1].split(']')
        x = foods.pop(right[1])
        with open("foods.json", "w") as f:
            json.dump(foods, f, indent=4)
        f.close()
        self.parent.remove_widget(food_list_item)
        # add confirm dialog


if __name__ == '__main__':
    WorkoutApp().run()
