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
        # Sudo ayrıcalıkları için parola iste
        password_dialog = Gtk.MessageDialog(
            self,
            0,
            Gtk.MessageType.WARNING,
            Gtk.ButtonsType.OK_CANCEL,
            "Sudo parolası gerekiyor"
        )
        password_dialog.format_secondary_text("Lütfen sudo parolanızı girin.")
        password_entry = Gtk.Entry()
        password_entry.set_visibility(False)
        password_entry.set_invisible_char("*")
        password_dialog.get_content_area().pack_end(password_entry, True, True, 0)
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
            dialog.run()
            dialog.destroy()
        else:
            print("İşlem iptal edildi.")

win = LogCleaner()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
