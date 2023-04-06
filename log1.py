import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class LogCleaner(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Log Temizleyici")
        self.set_border_width(10)
        self.set_size_request(400, 200)

        # Label
        label = Gtk.Label()
        label.set_markup("<big>Bu uygulama ile gereksiz log dosyalarını temizleyebilirsiniz.</big>")

        # Button
        button = Gtk.Button.new_with_label("Logları Temizle")
        button.connect("clicked", self.on_button_clicked)

        # Box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.add(vbox)

        # Pack widgets
        vbox.pack_start(label, True, True, 0)
        vbox.pack_start(button, True, True, 0)

    def on_button_clicked(self, widget):
        os.system("sudo journalctl --vacuum-time=3d")
        os.system("sudo journalctl --vacuum-size=100M")

        dialog = Gtk.MessageDialog(
            parent=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Log dosyaları başarıyla temizlendi!"
        )
        dialog.run()
        dialog.destroy()

win = LogCleaner()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
