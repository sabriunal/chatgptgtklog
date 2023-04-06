import os
import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib

class LogCleaner(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app, title="Log Temizleyici")
        self.set_border_width(10)
        self.set_default_size(400, 200)

        # Label
        label = Gtk.Label()
        label.set_markup("<big>Bu uygulama ile gereksiz log dosyalarını temizleyebilirsiniz.</big>")

        # Button
        button = Gtk.Button.new_with_label("Logları Temizle")
        button.connect("clicked", self.on_button_clicked)

        # Box
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(vbox)

        # Pack widgets
        vbox.append(label)
        vbox.append(button)

    def on_button_clicked(self, widget):
        # Sudo ayrıcalıkları için parola iste
        password_dialog = Gtk.Dialog(
            title="Sudo Parolası Gerekli",
            transient_for=self,
            flags=0,
            buttons=(
                ("Cancel", Gtk.ResponseType.CANCEL),
                ("OK", Gtk.ResponseType.OK),
            ),
        )
        password_label = Gtk.Label("Lütfen sudo parolanızı girin.")
        password_entry = Gtk.Entry()
        password_entry.set_visibility(False)
        password_entry.set_invisible_char("*")
        password_dialog.set_child(password_label)
        password_dialog.get_content_area().append(password_entry)
        password_dialog.show_all()
        response = password_dialog.run()
        password = password_entry.get_text()
        password_dialog.destroy()

        if response == Gtk.ResponseType.OK:
            os.environ["SUDO_ASKPASS"] = "/usr/lib/openssh/gnome-ssh-askpass" # ssh-askpass aracı yoksa yüklü olabilir, değiştirmeniz gerekebilir
            command = "sudo -A journalctl --vacuum-time=3d; sudo -A journalctl --vacuum-size=100M"
            os.system('echo %s | %s' % (password, command))
            dialog = Gtk.MessageDialog(
                parent=self,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Log dosyaları başarıyla temizlendi!"
            )
            dialog.connect("response", self.on_dialog_response)
            dialog.show()

        else:
            print("İşlem iptal edildi.")

    def on_dialog_response(self, dialog, response_id):
        if response_id == Gtk.ResponseType.OK:
            dialog.destroy()
            self.close()

app = Gtk.Application(application_id="org.example.logcleaner", flags=Gio.ApplicationFlags.FLAGS_NONE)
app.register()
win = LogCleaner(app)
win.show()
app.run()
