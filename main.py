#!/usr/bin/python
# coding: UTF-8

import os
import sys
import pygtk
import gtk


brightness_configfile = "/sys/devices/platform/pwm-backlight/backlight/pwm-backlight/brightness"

brightness_max = 255
brightness_min = 10
brightness_deep_min = 0

if len( sys.argv) &gt; 1 and sys.argv[1] == "--deep":
    brightness_min = brightness_deep_min


class Brightness:
    def __init__( self):
        self.check_brightness_configfile()
        self.make_window_main()

    def __del__( self):
        pass

    def make_window_main( self):
        self.window_main = gtk.Window()
        self.window_main.set_title( "AC100 Brightness Control")
        self.window_main.set_default_size( 300, 120)
        self.window_main.connect( "destroy_event", self.application_end)
        self.window_main.connect( "delete_event", self.application_end)

        self.menubar = gtk.MenuBar()
        self.menu_file = gtk.Menu()
        self.menu_file_save = gtk.MenuItem( "Save")
        self.menu_file_quit = gtk.MenuItem( "Quit")
        self.menu_file.append( self.menu_file_save)
        self.menu_file.append( self.menu_file_quit)
        self.menu_item_file = gtk.MenuItem( "File")
        self.menu_item_file.set_submenu( self.menu_file)
        self.menubar.append( self.menu_item_file)
        self.menu_file_save.connect( "activate", self.brightness_save)
        self.menu_file_quit.connect( "activate", self.application_end)

        self.label_message = gtk.Label()
        self.label_message.set_markup( "&lt;b&gt;Brightness&lt;/b&gt;")

        self.scale_brightness = gtk.HScale()
        self.scale_brightness.set_digits( 0)
        self.scale_brightness.set_adjustment( gtk.Adjustment( value=self.brightness_now, lower=brightness_min, upper=brightness_max, step_incr=1))
        self.scale_brightness.connect( "value_changed", self.scale_value_changed)

        self.window_main_vbox = gtk.VBox()
        self.window_main_vbox.pack_start( self.menubar, False, True, 0)
        self.window_main_vbox.pack_start( self.label_message, True, True, 0)
        self.window_main_vbox.pack_start( self.scale_brightness, True, True, 0)
        self.window_main.add( self.window_main_vbox)

        self.window_main.show_all()

    def scale_value_changed( self, widget, data=None):
        f = open( brightness_configfile, "w")
        f.write( str( int( widget.get_value())))
        f.close()
        self.brightness_now = int( widget.get_value())

    def brightness_save( self, widget, data=None):
        pass

    def application_end( self, widget=None, data=None):
        gtk.main_quit()
        return False

    def check_brightness_configfile( self):
        if os.access( brightness_configfile, os.F_OK) and os.access( brightness_configfile, os.W_OK):
            self.brightness_now = int( open( brightness_configfile, "r").read().rstrip())
        else:
            self.no_write_brightness_configfile()

    def no_write_brightness_configfile( self):
        dlg = gtk.MessageDialog( None, gtk.DIALOG_MODAL, gtk.MESSAGE_WARNING, gtk.BUTTONS_OK, "設定ファイルに書きこみ権限がありません。")
        dlg.run()
        dlg.destroy()
        sys.exit( 1)


def main():
    brightness = Brightness()
    gtk.main()


if __name__ == "__main__":
    main()
