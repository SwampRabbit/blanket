# window.py
#
# Copyright 2020 Rafael Mardojai CM
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os

from gi.repository import Gtk, Handy

from .sound import SoundObject
from .widgets import SoundsGroup


@Gtk.Template(resource_path='/com/rafaelmardojai/Blanket/window.ui')
class BlanketWindow(Handy.ApplicationWindow):
    __gtype_name__ = 'BlanketWindow'

    box = Gtk.Template.Child()

    sounds = {
        'Nature': [
            'Rain',
            'Storm',
            'Wind',
            'Summer Night'
        ],
        'Interiors': [
            'Coffee Shop',
            'Fireplace'
        ],
        'Noise': [
            'Pink Noise',
            'White Noise'
        ]
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.setup_sounds()
        self.setup_custom_sounds()

        self.show_all()

    def setup_sounds(self):
        # Setup default sounds
        for g, sl in self.sounds.items():
            # Create a new SoundsGroup
            group = SoundsGroup(g)
            # Iterate sounds
            for s in sl:
                # Create a new SoundObject
                sound = SoundObject(s)
                # Add SoundObject to SoundsGroup
                group.add(sound)

            # Add SoundsGroup to the window's main box
            self.box.pack_start(group, False, True, 0)

    def setup_custom_sounds(self):
        # Setup user custom sounds
        self.custom_sounds = SoundsGroup('Custom')
        self.box.pack_start(self.custom_sounds, False, True, 0)

        # Add sound button row
        add_row = Gtk.ListBoxRow()
        add_row.set_selectable(False)
        add_row_box = Gtk.Box(
            height_request = 34
        )
        add_row.add(add_row_box)
        add_row_icon = Gtk.Image.new_from_icon_name(
            'list-add-symbolic',
            Gtk.IconSize.MENU
        )
        add_row_box.pack_start(add_row_icon, True, True, 0)
        self.custom_sounds.listbox.add(add_row)
        self.custom_sounds.listbox.connect('row-activated', self.open_audio)

    def open_audio(self, _widget=None, _row=None):
        otf_filter = Gtk.FileFilter()
        otf_filter.set_name(_('OTF Fonts'))
        otf_filter.add_mime_type('font/otf')
        otf_filter.add_pattern('.otf')
        ttf_filter = Gtk.FileFilter()
        ttf_filter.set_name(_('TTF Fonts'))
        ttf_filter.add_mime_type('font/ttf')
        ttf_filter.add_pattern('.ttf')

        filechooser = Gtk.FileChooserNative.new(
            _('Open audio'),
            self,
            Gtk.FileChooserAction.OPEN,
            None,
            None)
        response = filechooser.run()

        if response == Gtk.ResponseType.ACCEPT:
            filename = filechooser.get_filename()
            if filename:
                name = os.path.basename(filename).split('.')[0]
                uri = filechooser.get_uri()
                print(filename)
                print(uri)

                # Create a new SoundObject
                sound = SoundObject(name, uri)
                # Add SoundObject to SoundsGroup
                self.custom_sounds.add(sound)
                self.custom_sounds.show_all()

