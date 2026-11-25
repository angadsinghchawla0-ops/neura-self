#!/usr/bin/env python3
"""
ROOTMEOW KivyMD Application
Native Android UI for the ROOTMEOW bot
"""

import sys
import os
import asyncio
import threading
import json
import time
from pathlib import Path

# Kivy setup
os.environ['KIVY_NO_ARGS'] = '1'
os.environ['KIVY_NO_CONFIG'] = '1'

from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.core.window import Window
from kivy.metrics import dp, sp
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, NoTransition

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.card import MDCard
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem, ThreeLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.icon import MDIcon
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.menu import MDDropdownMenu

# Import the bot logic
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.bot import NeuraBot
from core import state
from utils import proxy_manager
from neura_engines.setup_engine import NeuraSetupEngine

# Load KV definitions
Builder.load_file(os.path.join(os.path.dirname(__file__), 'rootmeow_kv.kv'))


class StatCard(MDCard):
    """Stat display card for dashboard"""
    icon_text = StringProperty("💰")
    value = StringProperty("0")
    label = StringProperty("Balance")
    icon_color = ListProperty([1, 1, 1, 1])


class AccountCard(MDCard):
    """Account list card"""
    account_id = StringProperty("")
    account_name = StringProperty("Unknown")
    account_discriminator = StringProperty("")
    status = StringProperty("offline")
    avatar_icon = StringProperty("account-circle")
    status_color = ListProperty([0.5, 0.5, 0.5, 1])


class SettingItem(MDBoxLayout):
    """Settings item with label and control"""
    setting_label = StringProperty("Setting")
    control_widget = None


class RootMeowApp(MDApp):
    """Main ROOTMEOW KivyMD Application"""

    title = "ROOTMEOW"
    icon = "dashboard/static/assets/neura.ico"
    theme_cls = None

    # Bot state
    bots = ListProperty([])
    current_bot_index = NumericProperty(-1)
    bot_running = BooleanProperty(False)
    dashboard_data = {}

    # Dialogs
    _account_dialog = None
    _settings_dialog = None

    def build(self):
        """Build the application"""
        self.theme_cls = self.theme_cls
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.accent_palette = "Cyan"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.material_style = "M3"

        # Set window size for desktop testing
        if not self.is_android():
            Window.size = (400, 700)

        return Builder.load_file(os.path.join(os.path.dirname(__file__), 'rootmeow_kv.kv'))

    def is_android(self):
        """Check if running on Android"""
        return 'ANDROID_ARGUMENT' in os.environ or 'ANDROID_PRIVATE' in os.environ

    def on_start(self):
        """Called when app starts"""
        # Initialize bot in background
        threading.Thread(target=self.init_bot_background, daemon=True).start()

        # Start dashboard update timer
        Clock.schedule_interval(self.update_dashboard, 2.0)

        # Request permissions on Android
        if self.is_android():
            self.request_android_permissions()

    def request_android_permissions(self):
        """Request Android runtime permissions"""
        try:
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.INTERNET,
                Permission.ACCESS_NETWORK_STATE,
                Permission.ACCESS_WIFI_STATE,
                Permission.WAKE_LOCK,
                Permission.VIBRATE,
                Permission.POST_NOTIFICATIONS,
                Permission.FOREGROUND_SERVICE,
            ])
        except ImportError:
            pass  # Not on Android

    def init_bot_background(self):
        """Initialize bot in background thread"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(self.async_init_bot())
        except Exception as e:
            print(f"Bot init error: {e}")

    async def async_init_bot(self):
        """Async bot initialization"""
        try:
            # Load accounts
            config_dir = state.CONFIG_DIR
            accounts_path = os.path.join(config_dir, 'accounts.json')

            if not os.path.exists(accounts_path):
                return

            with open(accounts_path, 'r') as f:
                acc_data = json.load(f)
                accounts = [a for a in acc_data.get('accounts', []) if a.get('enabled', True)]

            if not accounts:
                return

            # Load stats
            state.load_account_stats()

            # Start first account
            for i, acc in enumerate(accounts):
                token = acc.get('token')
                channels = acc.get('channels', [])
                if not token or "YOUR_TOKEN_HERE" in token or "PLACEHOLDER" in token:
                    continue

                valid_channels = [ch for ch in channels if ch and "YOUR_CHANNEL_ID_HERE" not in str(ch)]

                proxy_url, proxy_auth, proxy_label = proxy_manager.resolve_account_proxy(acc)

                bot = NeuraBot(
                    token=token,
                    channels=valid_channels,
                    proxy_url=proxy_url,
                    proxy_auth=proxy_auth,
                    proxy_label=proxy_label,
                )

                state.bot_instances.append(bot)
                self.bots.append({
                    'bot': bot,
                    'name': acc.get('name', f'Account {i+1}'),
                    'token': token,
                    'channels': valid_channels,
                    'proxy_label': proxy_label,
                })

                # Start bot
                asyncio.create_task(bot.run_bot())

                # Only run first account on mobile to save resources
                if self.is_android() and i == 0:
                    break

            self.bot_running = True
            self.current_bot_index = 0 if self.bots else -1

        except Exception as e:
            print(f"Async bot init error: {e}")

    @mainthread
    def update_dashboard(self, dt):
        """Update dashboard UI with bot data"""
        if not self.bot_running or self.current_bot_index < 0:
            return

        try:
            bot_data = self.bots[self.current_bot_index]
            bot = bot_data['bot']

            if not bot.is_ready or not bot.user:
                return

            uid = str(bot.user.id)
            st = state.account_stats.get(uid, {})

            # Update stats cards
            stats_grid = self.root.get_screen('dashboard').ids.stats_grid
            stats_grid.clear_widgets()

            stats = [
                ("💰", str(st.get('current_cash', 0)), "Balance"),
                ("⏱️", st.get('uptime', '00:00:00'), "Uptime"),
                ("🏹", f"{st.get('session_hunt_count', 0)}", "Hunts (Session)"),
                ("⚔️", f"{st.get('session_battle_count', 0)}", "Battles (Session)"),
                ("⚡", f"{st.get('cpm', 0)}", "CPM"),
                ("💬", f"{st.get('session_owo_count', 0)}", "OwO (Session)"),
                ("💎", f"{st.get('gems_used', 0)}", "Gems Used"),
                ("🛡️", f"{st.get('captchas_solved', 0)}", "Captchas Solved"),
            ]

            for icon, value, label in stats:
                card = StatCard()
                card.icon_text = icon
                card.value = value
                card.label = label
                stats_grid.add_widget(card)

            # Update account list
            self.update_account_list()

        except Exception as e:
            print(f"Dashboard update error: {e}")

    @mainthread
    def update_account_list(self):
        """Update the accounts screen list"""
        accounts_list = self.root.get_screen('accounts').ids.accounts_list
        accounts_list.clear_widgets()

        for i, bot_data in enumerate(self.bots):
            bot = bot_data['bot']
            username = bot.username if bot.user else bot_data['name']
            user_id = str(bot.user.id) if bot.user else "Connecting..."
            status = "Running" if bot.is_ready and not bot.paused else "Paused" if bot.is_ready else "Connecting..."
            status_color = [0, 0.8, 0.3, 1] if status == "Running" else [1, 0.8, 0, 1] if status == "Paused" else [0.5, 0.5, 0.5, 1]

            item = ThreeLineListItem(
                text=username,
                secondary_text=f"ID: {user_id}",
                tertiary_text=f"Status: {status}",
                on_release=lambda x, idx=i: self.select_account(idx)
            )
            accounts_list.add_widget(item)

    def select_account(self, index):
        """Switch to selected account"""
        if 0 <= index < len(self.bots):
            self.current_bot_index = index
            self.go_dashboard()
            self.show_snackbar(f"Switched to {self.bots[index]['name']}")

    def go_dashboard(self):
        """Navigate to dashboard screen"""
        self.root.current = 'dashboard'

    def open_accounts(self):
        """Navigate to accounts screen"""
        self.root.current = 'accounts'

    def open_settings(self):
        """Navigate to settings screen"""
        self.root.current = 'settings'

    def start_bot(self):
        """Start/resume the current bot"""
        if self.current_bot_index >= 0:
            bot = self.bots[self.current_bot_index]['bot']
            bot.paused = False
            bot.throttle_until = 0
            bot.log("SYS", "Bot RESUMED via Mobile App")
            self.show_snackbar("Bot started")

    def stop_bot(self):
        """Pause the current bot"""
        if self.current_bot_index >= 0:
            bot = self.bots[self.current_bot_index]['bot']
            bot.paused = True
            bot.log("SYS", "Bot STOPPED via Mobile App")
            self.show_snackbar("Bot paused")

    def check_cash(self):
        """Send cash check command"""
        if self.current_bot_index >= 0:
            bot = self.bots[self.current_bot_index]['bot']
            asyncio.run_coroutine_threadsafe(
                bot.send_message(f"{bot.prefix}cash", skip_typing=True, priority=True),
                bot.loop
            )
            self.show_snackbar("Cash check sent")

    def refresh_dashboard(self):
        """Force dashboard refresh"""
        self.update_dashboard(0)
        self.show_snackbar("Dashboard refreshed")

    def refresh_logs(self):
        """Refresh terminal logs"""
        terminal_screen = self.root.get_screen('terminal')
        output_label = terminal_screen.ids.terminal_output

        logs = []
        for bot in state.bot_instances:
            if bot.user:
                uid = str(bot.user.id)
                bot_logs = [l for l in state.command_logs if str(l.get('bot_id')) == uid]
                logs.extend(bot_logs[-50:])

        if logs:
            output_text = "\n".join([
                f"[{time.strftime('%H:%M:%S', time.localtime(l.get('timestamp', time.time())))}] "
                f"[{l.get('type', 'LOG')}] {l.get('message', '')}"
                for l in logs[-20:]
            ])
        else:
            output_text = "No logs available yet..."

        output_label.text = output_text

    def clear_terminal(self):
        """Clear terminal output"""
        terminal_screen = self.root.get_screen('terminal')
        terminal_screen.ids.terminal_output.text = "Terminal cleared."

    def add_account_dialog(self):
        """Show add account dialog"""
        if self._account_dialog:
            self._account_dialog.dismiss()

        content = MDBoxLayout(
            orientation='vertical',
            spacing=dp(16),
            padding=dp(16),
            size_hint_y=None,
            height=dp(300)
        )

        name_field = MDTextField(
            hint_text="Account Name",
            mode="rectangle",
        )
        token_field = MDTextField(
            hint_text="Discord Token",
            mode="rectangle",
            password=True,
        )
        channels_field = MDTextField(
            hint_text="Channel IDs (space separated)",
            mode="rectangle",
        )

        content.add_widget(name_field)
        content.add_widget(token_field)
        content.add_widget(channels_field)

        self._account_dialog = MDDialog(
            title="Add Account",
            type="custom",
            content_cls=content,
            buttons=[
                MDFlatButton(text="CANCEL", on_release=lambda x: self._account_dialog.dismiss()),
                MDRaisedButton(text="SAVE", on_release=lambda x: self.save_account(name_field, token_field, channels_field)),
            ],
        )
        self._account_dialog.open()

    def save_account(self, name_field, token_field, channels_field):
        """Save new account to config"""
        name = name_field.text.strip()
        token = token_field.text.strip()
        channels = channels_field.text.strip().split()

        if not name or not token:
            self.show_snackbar("Name and token required")
            return

        config_dir = state.CONFIG_DIR
        accounts_path = os.path.join(config_dir, 'accounts.json')

        try:
            with open(accounts_path, 'r') as f:
                data = json.load(f)
        except:
            data = {'accounts': []}

        new_account = {
            'name': name,
            'token': token,
            'channels': channels,
            'enabled': True,
            'proxy_id': None,
        }

        data['accounts'].append(new_account)

        with open(accounts_path, 'w') as f:
            json.dump(data, f, indent=4)

        self._account_dialog.dismiss()
        self.show_snackbar(f"Account '{name}' saved. Restart app to apply.")
        # Re-initialize bot
        threading.Thread(target=self.init_bot_background, daemon=True).start()

    def show_snackbar(self, text):
        """Show a snackbar message"""
        MDSnackbar(
            MDLabel(text=text),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        ).open()


def main():
    """Entry point for Kivy app"""
    app = RootMeowApp()
    app.run()


if __name__ == "__main__":
    main()