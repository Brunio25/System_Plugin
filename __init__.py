import os
import re
from pathlib import Path

from albert import *

md_iid = '2.2'
md_version = "1.0"
md_id = 'Shutdown'
md_name = "Shutdown"
md_description = "Shutdown, Reboot, etc"
md_license = "MIT"
md_url = "https://github.com/albertlauncher/python/tree/master/emoji"
md_authors = "@brunio25"

HOME_PATH = Path.home()
ICONS_PATH = '.local/share/albert/python/plugins/Shutdown/icons/'
SHUTDOWN_ICON = HOME_PATH / ICONS_PATH / 'shutdown.png'
REBOOT_ICON = HOME_PATH / ICONS_PATH / 'reboot.png'

options = [
    ('Shutdown', 'shutdown -P now', 'Shutdown the computer immediately', SHUTDOWN_ICON.__str__()),
    ('Reboot', 'shutdown -r now', 'Restart the computer immediately', REBOOT_ICON.__str__()),
    ('Sleep', 'systemctl suspend', 'Suspend the computer immediately', REBOOT_ICON.__str__())
]


class Plugin(PluginInstance, GlobalQueryHandler):

    def __init__(self):
        GlobalQueryHandler.__init__(self,
                                    id=md_id,
                                    name=md_name,
                                    description=md_description,
                                    defaultTrigger='!',
                                    synopsis='')
        PluginInstance.__init__(self, extensions=[self])

    def handleGlobalQuery(self, query):
        stripped_query = query.string.strip()
        rank_items = []
        for title, command, description, icon in options:
            if re.search(stripped_query, title, re.IGNORECASE):
                item = StandardItem(
                    id=title,
                    text=title,
                    subtext=description,
                    iconUrls=[icon],
                    inputActionText=title,
                    actions=[
                        Action(
                            title.capitalize(), f"Execute {command}",
                            lambda execute=command: os.system(execute)
                        ),
                    ]
                )

                rank_items.append(RankItem(item, 1))

        return rank_items

    def configWidget(self):
        return [
            {
                'type': 'label',
                'text': __doc__.strip()
            }
        ]
