#!/usr/bin/env python3
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio, GLib

class LogCleaner(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self, title="Log Temizleyici")
        self.set_default_size(350, 150)

        # Layout
        layout = Gtk.Grid()
        self.add(layout)

        # Label for log folder
        log_label = Gtk.Label("Log klasörü:")
        layout.attach(log_label, 0, 0, 1, 1)

        # Entry for log folder
        self.log_entry = Gtk.Entry()
        self.log_entry.set_text("/var/log")
        layout.attach(self.log_entry, 1, 0, 1, 1)

        # Label for password
        password_label = Gtk.Label("Sudo parolası:")
        layout.attach(password_label, 0, 1, 1, 1)

        # Entry for password
        self.password_entry = Gtk.Entry()
        self.password_entry.set_visibility(False)
        layout.attach(self.password_entry, 1, 1, 1, 1)

        # Buttons
        ok_button = Gtk.Button.new_with_label("Tamam")
        ok_button.connect("clicked", self.on_ok_button_clicked)
        layout.attach(ok_button, 0, 2, 1, 1)

        cancel_button = Gtk.Button.new_with_label("İptal")
        cancel_button.connect("clicked", Gtk.main_quit)
        layout.attach(cancel_button, 1, 2, 1, 1)

    def on_ok_button_clicked(self, button):
        log_folder = self.log_entry.get_text()
        password = self.password_entry.get_text()

        # Build command and run it with sudo
        command = "rm -rf {}/*".format(log_folder).split()
        try:
            subprocess.check_call(["sudo", "-S"] + command, stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   universal_newlines=True, input=password)
            dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.INFO,
                                       buttons=Gtk.ButtonsType.OK, text="Log temizleme işlemi başarıyla tamamlandı!")
            dialog.run()
            dialog.destroy()
        except subprocess.CalledProcessError as e:
            error_dialog = Gtk.MessageDialog(parent=self, flags=0, message_type=Gtk.MessageType.ERROR,
                                             buttons=Gtk.ButtonsType.CANCEL, text="Log temizleme işlemi başarısız oldu!")
            error_dialog.format_secondary_text(e.output)
            error_dialog.run()
            error_dialog.destroy()

win = LogCleaner()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
