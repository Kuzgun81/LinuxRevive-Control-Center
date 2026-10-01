from __future__ import annotations

import os
import subprocess

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

from .maintenance import clear_user_cache, scan_temporary_files
from .system_info import SystemInfo, collect_system_info


class MainWindow(Gtk.Window):
    def __init__(self) -> None:
        super().__init__(title="LinuxRevive Control Center")
        self.set_default_size(920, 620)
        self.set_border_width(20)
        self.info = collect_system_info()
        self.status = Gtk.Label(xalign=0)
        self.status.set_text("Hazır")
        self._build()

    def _build(self) -> None:
        root = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=16)
        self.add(root)
        title = Gtk.Label(label="LinuxRevive")
        title.set_xalign(0)
        title.get_style_context().add_class("title")
        root.pack_start(title, False, False, 0)
        subtitle = Gtk.Label(
            label="Linux sisteminizi terminale ihtiyaç duymadan yönetin"
        )
        subtitle.set_xalign(0)
        root.pack_start(subtitle, False, False, 0)

        notebook = Gtk.Notebook()
        root.pack_start(notebook, True, True, 0)
        notebook.append_page(self._dashboard(), Gtk.Label(label="Genel Bakış"))
        notebook.append_page(self._maintenance(), Gtk.Label(label="Bakım"))
        notebook.append_page(self._help(), Gtk.Label(label="Güvenlik ve Yardım"))
        root.pack_end(self.status, False, False, 0)

    def _dashboard(self) -> Gtk.Widget:
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_border_width(16)
        for label, value in (
            ("İşletim sistemi", self.info.operating_system),
            ("Çekirdek", self.info.kernel),
            ("İşlemci", self.info.processor),
            ("Bellek", self.info.memory),
            ("Ana disk", self.info.disk),
            ("Çalışma süresi", self.info.uptime),
        ):
            row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            key = Gtk.Label(label=label, xalign=0)
            key.set_width_chars(18)
            value_label = Gtk.Label(label=value, xalign=0)
            row.pack_start(key, False, False, 0)
            row.pack_start(value_label, True, True, 0)
            box.pack_start(row, False, False, 0)
        refresh = Gtk.Button(label="Bilgileri yenile")
        refresh.connect("clicked", self._refresh)
        box.pack_start(refresh, False, False, 8)
        return box

    def _maintenance(self) -> Gtk.Widget:
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_border_width(16)
        description = Gtk.Label(
            label="Yalnızca geçici kullanıcı verilerini tarar. Silme işleminden önce onay istenir."
        )
        description.set_xalign(0)
        description.set_line_wrap(True)
        box.pack_start(description, False, False, 0)
        scan = Gtk.Button(label="Geçici dosyaları tara")
        scan.connect("clicked", self._scan)
        box.pack_start(scan, False, False, 0)
        clear = Gtk.Button(label="Kullanıcı önbelleğini temizle")
        clear.connect("clicked", self._clear_cache)
        box.pack_start(clear, False, False, 0)
        return box

    def _help(self) -> Gtk.Widget:
        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        box.set_border_width(16)
        label = Gtk.Label(
            label="LinuxRevive sistem güvenliğini kapatmaz ve rastgele terminal komutu çalıştırmaz. "
            "Yönetici yetkisi isteyen işlemler açıkça belirtilir."
        )
        label.set_xalign(0)
        label.set_line_wrap(True)
        box.pack_start(label, False, False, 0)
        return box

    def _refresh(self, _button: Gtk.Button) -> None:
        self.info = collect_system_info()
        self.status.set_text("Sistem bilgileri yenilendi.")

    def _scan(self, _button: Gtk.Button) -> None:
        files, total = scan_temporary_files()
        self.status.set_text(f"{files} dosya bulundu ({total / 1024 / 1024:.1f} MB).")

    def _clear_cache(self, _button: Gtk.Button) -> None:
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Kullanıcı önbelleği temizlensin mi?",
        )
        response = dialog.run()
        dialog.destroy()
        if response == Gtk.ResponseType.YES:
            removed = clear_user_cache()
            self.status.set_text(f"{removed} önbellek öğesi temizlendi.")


def main() -> None:
    window = MainWindow()
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()
