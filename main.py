import platform

if platform.system() == "Linux":
    try:
        from jnius import autoclass
        def android_toast(message):
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            Toast = autoclass('android.widget.Toast')
            context = PythonActivity.mActivity
            Toast.makeText(context, str(message), Toast.LENGTH_SHORT).show()
    except Exception as e:
        def android_toast(message):
            print("[AndroidToast] (Ошибка)", message)
else:
    def android_toast(message):
        print("[AndroidToast]", message)

import random
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import ListProperty, NumericProperty, StringProperty, BooleanProperty
from kivymd.app import MDApp
from kivymd.toast import android_toast
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

skins_data = {
    "Common": [
        {"name": "Iron Branch", "image": "🌿", "price": 50},
        {"name": "Tango", "image": "🥭", "price": 75},
        {"name": "Clarity", "image": "💧", "price": 60},
        {"name": "Healing Salve", "image": "🧪", "price": 80},
        {"name": "Smoke of Deceit", "image": "💨", "price": 90},
        {"name": "Observer Ward", "image": "👁", "price": 70},
        {"name": "Sentry Ward", "image": "🔍", "price": 85},
        {"name": "Dust of Appearance", "image": "✨", "price": 65},
    ],
    "Uncommon": [
        {"name": "Magic Stick", "image": "🪄", "price": 150},
        {"name": "Boots of Speed", "image": "👢", "price": 200},
        {"name": "Ring of Protection", "image": "💍", "price": 180},
        {"name": "Gauntlets of Strength", "image": "🥊", "price": 170},
        {"name": "Mantle of Intelligence", "image": "🧠", "price": 190},
        {"name": "Slippers of Agility", "image": "👟", "price": 160},
    ],
    "Rare": [
        {"name": "Arcane Boots", "image": "🥾", "price": 400},
        {"name": "Magic Wand", "image": "🪄✨", "price": 450},
        {"name": "Blade of Alacrity", "image": "⚔️", "price": 500},
        {"name": "Staff of Wizardry", "image": "🧙", "price": 480},
        {"name": "Ogre Axe", "image": "🪓", "price": 420},
        {"name": "Mithril Hammer", "image": "🔨", "price": 470},
    ],
    "Mythical": [
        {"name": "Black King Bar", "image": "👑", "price": 1000},
        {"name": "Force Staff", "image": "📿", "price": 1200},
        {"name": "Eul's Scepter", "image": "🌪️", "price": 1100},
        {"name": "Mekansm", "image": "⚕️", "price": 1150},
        {"name": "Pipe of Insight", "image": "🎺", "price": 1050},
    ],
    "Legendary": [
        {"name": "Butterfly", "image": "🦋", "price": 2500},
        {"name": "Divine Rapier", "image": "⚡", "price": 3000},
        {"name": "Daedalus", "image": "🗡️", "price": 2800},
        {"name": "Monkey King Bar", "image": "🐒", "price": 2600},
        {"name": "Scythe of Vyse", "image": "🪃", "price": 2700},
    ],
    "Immortal": [
        {"name": "Aegis of Immortal", "image": "🛡", "price": 5000},
        {"name": "Refresher Orb", "image": "🔮", "price": 5500},
        {"name": "Octarine Core", "image": "💜", "price": 6000},
        {"name": "Radiance", "image": "☀️", "price": 5800},
    ]
}
RARITIES = list(skins_data.keys())

class MainScreen(Screen):
    inventory = ListProperty([])
    balance = NumericProperty(1000)
    ad_cooldown = NumericProperty(0)
    currently_opening = BooleanProperty(False)
    won_item = StringProperty("")

    def on_pre_enter(self, *args):
        self.update_inventory_grid()

    def open_case(self):
        if self.currently_opening: return
        self.currently_opening = True
        self.ids['case_btn'].disabled = True
        self.ids['loot_text'].text = "Прокрутка кейса..."
        Clock.schedule_once(self.show_case_result, 1.7)

    def show_case_result(self, dt):
        rarity = random.choices(RARITIES, weights=[40,30,15,8,5,2])[0]
        item_info = random.choice(skins_data[rarity])
        item = {
            "name": item_info["name"],
            "rarity": rarity,
            "image": item_info["image"],
            "price": item_info["price"],
        }
        self.inventory.append(item)
        self.won_item = f"{item['image']} {item['name']} ({item['rarity']})"
        self.ids['loot_text'].text = f"Вы выбили {self.won_item}!"
        android_toast(text=f"Добавлено в инвентарь: {self.won_item}").open()
        self.currently_opening = False
        self.ids['case_btn'].disabled = False
        self.update_inventory_grid()

    def update_inventory_grid(self):
        grid = self.ids.inventory_grid
        grid.clear_widgets()
        for idx, item in enumerate(self.inventory):
            btn = MDFlatButton(
                text=f"{item['image']}\n{item['name']}\n[{item['rarity']}]",
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                on_release=lambda btn, i=idx: self.sell_item(i),
                font_size="16sp"
            )
            grid.add_widget(btn)

    def sort_inventory(self):
        self.inventory = sorted(self.inventory, key=lambda x: RARITIES.index(x['rarity']))
        self.update_inventory_grid()

    def sell_item(self, idx):
        if idx < 0 or idx >= len(self.inventory): return
        sold = self.inventory.pop(idx)
        self.balance += sold['price']
        android_toast(text=f"Продан: {sold['name']} (+{sold['price']} монет)").open()
        self.update_inventory_grid()

    def ad_money(self):
        if self.ad_cooldown > 0: return
        self.show_ad_dialog()

    def show_ad_dialog(self):
        self.ad_dialog = MDDialog(text="А ЗДЕСЬ МОГЛА БЫТЬ ВАША РЕКЛАМА\n\n10 сек.", buttons=[])
        self.ad_dialog.open()
        self.ad_timer = 10
        Clock.schedule_interval(self.ad_tick, 1)

    def ad_tick(self, dt):
        self.ad_timer -= 1
        self.ad_dialog.text = f"А ЗДЕСЬ МОГЛА БЫТЬ ВАША РЕКЛАМА\n\n{self.ad_timer} сек."
        if self.ad_timer <= 0:
            self.ad_dialog.dismiss()
            self.balance += 500
            self.ids['loot_text'].text = "Реклама просмотрена, +500 монет!"
            android_toast(text="Получено +500 монет за рекламу!").open()
            self.ad_cooldown = 10  # Кулдаун 10 сек
            Clock.schedule_interval(self.decrement_ad_cooldown, 1)
            return False

    def decrement_ad_cooldown(self, dt):
        self.ad_cooldown -= 1
        if self.ad_cooldown <= 0:
            self.ids['loot_text'].text = "Открой кейс и выиграй скин Dota 2!"
            return False

class DotaInventoryApp(MDApp):
    def build(self):
        Builder.load_file("mykv.kv")
        sm = ScreenManager()
        sm.add_widget(MainScreen(name='main'))
        return sm

if __name__ == '__main__':
    DotaInventoryApp().run()
