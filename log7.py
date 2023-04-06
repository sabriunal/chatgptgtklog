import os
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, Gio, GtkSource

class LogCleaner(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Log Temizleyici")

        # Load the UI file
        builder = Gtk.Builder()
        builder.add_from_file("log.ui")

        # Get widgets
        self.window = builder.get_object("window")
        self.label = builder.get_object("label")
        self.button = builder.get_object("button")
        self.password_label = builder.get_object("password_label")
        self.password_entry = builder.get_object("password_entry")
        self.progressbar = builder.get_object("progressbar")
        self.dialog = builder.get_object("dialog")
        self.dialog_label = builder.get_object("dialog_label")
        self.dialog_button = builder.get_object("dialog_button")

        # Connect signals
        self.window.connect("destroy", self.on_window_destroy)
        self.button.connect("clicked", self.on_button_clicked)
        self.dialog_button.connect("clicked", self.on_dialog_button_clicked)

        # Set progressbar fraction to 0
        self.progressbar.set_fraction(0)

        # Set up sudo environment variable
        os.environ["SUDO_ASKPASS"] = "/usr/lib/openssh/gnome-ssh-askpass"

        # Add window to application
        self.set_child(self.window)

    def on_button_clicked(self, widget):
        # Show password dialog
        response = self.dialog.run()
        password = self.password_entry.get_text()
        self.dialog.hide()

        if response == Gtk.ResponseType.OK:
            # Set up command and run it
            command = "sudo -A journalctl --vacuum-time=3d; sudo -A journalctl --vacuum-size=100M"
            os.system('echo %s | %s' % (password, command))

            # Show success dialog
            self.dialog_label.set_text("Log dosyaları başarıyla temizlendi!")
            self.dialog.show_all()
            self.progressbar.set_fraction(1)

        else:
            print("İşlem iptal edildi.")

    def on_dialog_button_clicked(self, widget):
        self.dialog.hide()

    def on_window_destroy(self, widget):
        self.close()

app = Gtk.Application(application_id="org.example.logcleaner", flags=Gio.ApplicationFlags.FLAGS_NONE)
app.register()
win = LogCleaner(app)
win.show()
app.run()
