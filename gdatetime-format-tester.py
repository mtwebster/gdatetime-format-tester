#!/usr/bin/python3

import setproctitle
import signal
import sys

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio, GLib
class MyApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="org.foo.Bar",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.window = None
        self.entry = None
        self.label = None
        self.datetime = GLib.DateTime.new_now_local()
        self.cal = None

    def do_startup(self):
        Gtk.Application.do_startup(self) # if you're going to be a dbus service, set up and export before this.

    def do_activate(self):
        if self.window is None:
            self.window = Gtk.ApplicationWindow(application=self)
            self.window.set_title("Foo Bar")
            self.window.connect("destroy", self.quit)

            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            box.props.margin_start = 6
            box.props.margin_end = 6
            box.props.margin_top = 6
            box.props.margin_bottom = 6
            self.window.set_child(box)

            self.label = Gtk.Label(halign=Gtk.Align.START)
            box.append(self.label)
            self.entry = Gtk.Entry()
            self.entry.connect("changed", self.update_format)
            box.append(self.entry)
            self.cal = Gtk.Calendar()
            box.append(self.cal)
            self.cal.connect("day-selected", self.on_date_time_changed)

            hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
            self.hour_spinner = Gtk.SpinButton.new_with_range(0, 23, 1)
            self.hour_spinner.set_wrap(True)
            self.hour_spinner.set_hexpand(True)
            self.hour_spinner.connect("value-changed", self.on_date_time_changed)
            hbox.append(self.hour_spinner)
            self.minute_spinner = Gtk.SpinButton.new_with_range(0, 59, 1)
            self.minute_spinner.set_wrap(True)
            self.minute_spinner.set_hexpand(True)
            self.minute_spinner.connect("value-changed", self.on_date_time_changed)
            hbox.append(self.minute_spinner)
            box.append(hbox)

        self.window.present()

    def on_date_time_changed(self, spin, data=None):
        hours = self.hour_spinner.get_value_as_int()
        minutes = self.minute_spinner.get_value_as_int()
        picked = self.cal.get_date()
        self.datetime = GLib.DateTime.new_local(picked.get_year(),
                                                picked.get_month(),
                                                picked.get_day_of_month(),
                                                hours, minutes, 0)
        self.update_format(self.entry)

    def update_format(self, entry, data=None):
        dt = self.datetime.format(entry.get_text())
        if dt is None:
            self.label.set_markup("invalid")
            return

        self.label.set_markup(f"<b>{dt}</b>")

    def do_shutdown(self):
        Gtk.Application.do_shutdown(self)

if __name__ == "__main__":
    setproctitle.setproctitle("foobar")

    app = MyApplication()

    signal.signal(signal.SIGINT, lambda a, b: app.quit())
    sys.exit(app.run(sys.argv))
