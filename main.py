import os
from pathlib import Path

from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.client.Extension import Extension
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.event import KeywordQueryEvent

HOME_PATH = Path.home()
ICONS_PATH = HOME_PATH / '.local/share/ulauncher/extensions/System_Plugin/images'
SHUTDOWN_ICON = ICONS_PATH / 'shutdown.png'
REBOOT_ICON = ICONS_PATH / 'reboot.png'

options = [
    ('shutdown', 'shutdown -P now'),
    ('reboot', 'shutdown -r now'),
    ('sleep', 'systemctl suspend')
]


class SystemExtension(Extension):
    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())


class KeywordQueryEventListener(EventListener):
    def __init__(self):
        super().__init__()
        self.controller: SystemController = SystemController()

    def on_event(self, event: KeywordQueryEvent, extension: SystemExtension):
        return self.controller.handle_query(event.get_keyword(), extension.preferences.items())


class SystemController:
    @staticmethod
    def handle_query(query, preferences):
        print(preferences)
        for itemId, trigger in preferences:
            if itemId == query:
                command = next((option[1] for option in options if option[0] == query), "")
                os.system(command)
                return HideWindowAction()


if __name__ == '__main__':
    SystemExtension().run()
