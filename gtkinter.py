import gi

gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
gi.require_version('Pango', '1.0')
from gi.repository import Gtk, Gdk, GdkPixbuf, Pango, GLib
import os
import sys
from functools import partial


class Tk:
    def __init__(self):
        self.window = Gtk.Window()
        self.window.connect("destroy", Gtk.main_quit)
        self._container = None
        self._title = ""
        self._geometry = ""
        self._overrideredirect = None
        self._widgets = {}
        self._icon = None
        self._resizable = (True, True)
        self._minsize = (0, 0)
        self._maxsize = (0, 0)
        self._transparent = False
        self._alpha = 1.0
        self._menubar = None
        self._background = None
        self._cursor = None
        self._fullscreen = False
        self._position = None
        self._menu = None

        Widget._root = self
        self._mainloop_running = False

    def quit(self):
        Gtk.main_quit()

    def overrideredirect(self, overrideredirect=None):
        if overrideredirect is not None:
            self._overrideredirect = overrideredirect
            self.window.set_decorated(not overrideredirect)
        return self._overrideredirect

    def title(self, title=None):
        if title is not None:
            self._title = title
            self.window.set_title(title)
        return self._title

    def geometry(self, geometry=None):
        if geometry is not None:
            self._geometry = geometry
            if 'x' in geometry:
                parts = geometry.split('+')
                size = parts[0].split('x')
                self.window.set_default_size(int(size[0]), int(size[1]))
                if len(parts) > 1:
                    self.window.move(int(parts[1]), int(parts[2]))
        return self._geometry

    def iconphoto(self, photo=None):
        if photo is not None and isinstance(photo, PhotoImage):
            self._icon = photo
            self.window.set_icon(photo.pixbuf)
        return self._icon

    def resizable(self, width=None, height=None):
        if width is not None and height is not None:
            self._resizable = (width, height)
            self.window.set_resizable(width and height)
        return self._resizable

    def minsize(self, width=None, height=None):
        if width is not None and height is not None:
            self._minsize = (width, height)
            self.window.set_size_request(width, height)
        return self._minsize

    def maxsize(self, width=None, height=None):
        if width is not None and height is not None:
            self._maxsize = (width, height)
            if width > 0 and height > 0:
                self.window.set_max_size(width, height)
        return self._maxsize

    def attributes(self, alpha=None):
        if alpha is not None:
            self._alpha = alpha
            self.window.set_opacity(alpha)
        return self._alpha

    def background(self, color=None):
        if color is not None:
            self._background = color
            rgba = Gdk.RGBA()
            if rgba.parse(color):
                self.window.override_background_color(Gtk.StateFlags.NORMAL, rgba)
        return self._background

    def cursor(self, cursor=None):
        if cursor is not None:
            self._cursor = cursor
            display = self.window.get_display()
            cursor_map = {
                'arrow': Gdk.CursorType.ARROW,
                'hand1': Gdk.CursorType.HAND1,
                'hand2': Gdk.CursorType.HAND2,
                'cross': Gdk.CursorType.CROSS,
                'watch': Gdk.CursorType.WATCH,
                'xterm': Gdk.CursorType.XTERM,
                'plus': Gdk.CursorType.PLUS,
                'sb_h_double_arrow': Gdk.CursorType.SB_H_DOUBLE_ARROW,
                'sb_v_double_arrow': Gdk.CursorType.SB_V_DOUBLE_ARROW,
                'fleur': Gdk.CursorType.FLEUR,
                'pirate': Gdk.CursorType.PIRATE,
                'based_arrow_up': Gdk.CursorType.BASED_ARROW_UP,
                'based_arrow_down': Gdk.CursorType.BASED_ARROW_DOWN,
                'boat': Gdk.CursorType.BOAT,
                'gumby': Gdk.CursorType.GUMBY,
                'clock': Gdk.CursorType.CLOCK,
                'dotbox': Gdk.CursorType.DOTBOX,
                'exchange': Gdk.CursorType.EXCHANGE,
                'spraycan': Gdk.CursorType.SPRAYCAN,
                'star': Gdk.CursorType.STAR,
                'target': Gdk.CursorType.TARGET,
                'tcross': Gdk.CursorType.TCROSS
            }
            cursor_type = cursor_map.get(cursor, Gdk.CursorType.ARROW)
            cursor = Gdk.Cursor.new_for_display(display, cursor_type)
            self.window.get_root_window().set_cursor(cursor)
        return self._cursor

    def fullscreen(self, enable=None):
        if enable is not None:
            self._fullscreen = enable
            if enable:
                self.window.fullscreen()
            else:
                self.window.unfullscreen()
        return self._fullscreen

    def position(self, pos=None):
        if pos is not None:
            self._position = pos
            if pos == 'center':
                self.window.set_position(Gtk.WindowPosition.CENTER)
            elif pos == 'mouse':
                self.window.set_position(Gtk.WindowPosition.MOUSE)
        return self._position

    def config(self, menu=None, **kwargs):
        if menu is not None:
            self._menu = menu
            vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

            if isinstance(menu, MenuBar):
                vbox.pack_start(menu._widget, False, False, 0)

            if self._container:
                vbox.pack_start(self._container, True, True, 0)

            self.window.add(vbox)
            self._container = vbox

        for key, value in kwargs.items():
            if key == 'bg':
                self.background(value)
            elif key == 'cursor':
                self.cursor(value)
            elif key == 'title':
                self.title(value)
            elif key == 'geometry':
                self.geometry(value)
            elif key == 'resizable':
                self.resizable(value[0], value[1])
            elif key == 'fullscreen':
                self.fullscreen(value)
            else:
                print(f"Warning: Unknown configuration option '{key}'")

    configure = config

    def mainloop(self):
        self.window.show_all()
        self._mainloop_running = True
        Gtk.main()

    def pack(self, widget, **kwargs):
        if self._container is None or not isinstance(self._container, Gtk.Box):
            child = self.window.get_child()
            if child:
                self.window.remove(child)
            self._container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            self.window.add(self._container)

        padx = kwargs.get('padx', 0)
        pady = kwargs.get('pady', 0)
        widget._widget.set_margin_start(padx)
        widget._widget.set_margin_end(padx)
        widget._widget.set_margin_top(pady)
        widget._widget.set_margin_bottom(pady)

        if isinstance(widget, Button):
            ipadx = kwargs.get('ipadx', 0)
            ipady = kwargs.get('ipady', 0)
            widget._set_internal_padding(ipadx + widget._default_ipadx,
                                         ipady + widget._default_ipady)

        expand = kwargs.get('expand', False)
        fill = kwargs.get('fill', None)
        side = kwargs.get('side', 'top')
        anchor = kwargs.get('anchor', None)

        widget._widget.set_hexpand(expand and (fill in ['x', 'both']))
        widget._widget.set_vexpand(expand and (fill in ['y', 'both']))

        if not expand and fill:
            if fill == 'x' or fill == 'both':
                widget._widget.set_halign(Gtk.Align.FILL)
            if fill == 'y' or fill == 'both':
                widget._widget.set_valign(Gtk.Align.FILL)
        else:
            widget._widget.set_halign(Gtk.Align.CENTER)
            widget._widget.set_valign(Gtk.Align.CENTER)

        if anchor:
            anchor_map = {
                'n': (Gtk.Align.CENTER, Gtk.Align.START),
                'ne': (Gtk.Align.END, Gtk.Align.START),
                'e': (Gtk.Align.END, Gtk.Align.CENTER),
                'se': (Gtk.Align.END, Gtk.Align.END),
                's': (Gtk.Align.CENTER, Gtk.Align.END),
                'sw': (Gtk.Align.START, Gtk.Align.END),
                'w': (Gtk.Align.START, Gtk.Align.CENTER),
                'nw': (Gtk.Align.START, Gtk.Align.START),
                'center': (Gtk.Align.CENTER, Gtk.Align.CENTER)
            }
            if anchor in anchor_map:
                halign, valign = anchor_map[anchor]
                widget._widget.set_halign(halign)
                widget._widget.set_valign(valign)

        if side in ['left', 'right']:
            if self._container.get_orientation() != Gtk.Orientation.HORIZONTAL:
                self._convert_container_to_horizontal()

            if side == 'left':
                self._container.pack_start(widget._widget, expand, fill != 'none', 0)
            else:
                self._container.pack_end(widget._widget, expand, fill != 'none', 0)
        else:
            if self._container.get_orientation() != Gtk.Orientation.VERTICAL:
                self._convert_container_to_vertical()

            if side == 'top':
                self._container.pack_start(widget._widget, expand, fill != 'none', 0)
            else:
                self._container.pack_end(widget._widget, expand, fill != 'none', 0)

    def grid(self, widget, **kwargs):
        if self._container is None or not isinstance(self._container, Gtk.Grid):
            child = self.window.get_child()
            if child:
                self.window.remove(child)

            self._container = Gtk.Grid()
            self.window.add(self._container)

        widget._widget.set_margin_start(kwargs.get('padx', 0))
        widget._widget.set_margin_end(kwargs.get('padx', 0))
        widget._widget.set_margin_top(kwargs.get('pady', 0))
        widget._widget.set_margin_bottom(kwargs.get('pady', 0))

        self._container.attach(
            widget._widget,
            kwargs.get('column', 0),
            kwargs.get('row', 0),
            kwargs.get('columnspan', 1),
            kwargs.get('rowspan', 1)
        )

    def place(self, widget, *args, **kwargs):
        if self._container is None or not isinstance(self._container, Gtk.Fixed):
            child = self.window.get_child()
            if child:
                self.window.remove(child)

            self._container = Gtk.Fixed()
            self.window.add(self._container)

        if args:
            if len(args) >= 2:
                kwargs['x'] = args[0]
                kwargs['y'] = args[1]
            if len(args) >= 4:
                kwargs['width'] = args[2]
                kwargs['height'] = args[3]

        self._container.put(
            widget._widget,
            kwargs.get('x', 0),
            kwargs.get('y', 0)
        )

        if 'width' in kwargs or 'height' in kwargs:
            widget._widget.set_size_request(
                kwargs.get('width', -1),
                kwargs.get('height', -1)
            )


class Widget:
    _root = None

    def __init__(self, master=None, **kwargs):
        if master is None:
            if Widget._root is None:
                Widget._root = Tk()
            master = Widget._root

        self.master = master
        self._widget = self._create_widget(**kwargs)
        self._images = {}
        self._configure(**kwargs)

    def __getitem__(self, key):
        if hasattr(self, f"_get_{key}"):
            return getattr(self, f"_get_{key}")()
        elif hasattr(self._widget, f"get_{key}"):
            return getattr(self._widget, f"get_{key}")()
        else:
            raise KeyError(f"Unknown option '{key}'")

    def __setitem__(self, key, value):
        if hasattr(self, f"_set_{key}"):
            getattr(self, f"_set_{key}")(value)
        elif hasattr(self._widget, f"set_{key}"):
            getattr(self._widget, f"set_{key}")(value)
        else:
            raise KeyError(f"Unknown option '{key}'")

    def _create_widget(self, **kwargs):
        raise NotImplementedError

    def _parse_font(self, font_spec):
        font_desc = Pango.FontDescription()

        if isinstance(font_spec, (tuple, list)):
            family = None
            size = None
            weight = Pango.Weight.NORMAL
            style = Pango.Style.NORMAL

            for item in font_spec:
                if isinstance(item, int):
                    size = item
                elif isinstance(item, str):
                    item_lower = item.lower()
                    if item_lower == 'bold':
                        weight = Pango.Weight.BOLD
                    elif item_lower == 'italic':
                        style = Pango.Style.ITALIC
                    else:
                        family = item

            if family:
                font_desc.set_family(family)
            if size:
                font_desc.set_size(size * Pango.SCALE)
            font_desc.set_weight(weight)
            font_desc.set_style(style)

        elif isinstance(font_spec, str):
            parts = font_spec.split()
            family_parts = []
            size = None
            weight = Pango.Weight.NORMAL
            style = Pango.Style.NORMAL

            for part in parts:
                if part.isdigit():
                    size = int(part)
                elif part.lower() == 'bold':
                    weight = Pango.Weight.BOLD
                elif part.lower() == 'italic':
                    style = Pango.Style.ITALIC
                else:
                    family_parts.append(part)

            if family_parts:
                font_desc.set_family(' '.join(family_parts))
            if size:
                font_desc.set_size(size * Pango.SCALE)
            font_desc.set_weight(weight)
            font_desc.set_style(style)

        return font_desc

    def _configure(self, **kwargs):
        for key, value in kwargs.items():
            if key == 'textvariable':
                self._set_textvariable(value)
            elif key == 'var':
                self._set_variable(value)
            elif key == 'font':
                font_desc = self._parse_font(value)
                if font_desc:
                    if hasattr(self._widget, 'override_font'):
                        self._widget.override_font(font_desc)
                    elif hasattr(self._widget, 'modify_font'):
                        self._widget.modify_font(font_desc)
            elif key == 'bg':
                self._set_bg(value)
            elif key == 'fg':
                self._set_fg(value)
            elif key == 'relief':
                self._set_relief(value)
            elif key == 'cursor':
                self._set_cursor(value)
            elif key == 'compound':
                self._set_compound(value)
            elif key == 'padx':
                self._widget.set_margin_start(value)
                self._widget.set_margin_end(value)
            elif key == 'pady':
                self._widget.set_margin_top(value)
                self._widget.set_margin_bottom(value)
            elif key == 'borderwidth':
                self._widget.set_border_width(value)
            elif key == 'anchor':
                self._set_anchor(value)
            elif key == 'width':
                if isinstance(self._widget, Gtk.Label):
                    self._widget.set_width_chars(value)
                else:
                    self._widget.set_size_request(value, -1)
            elif key == 'height':
                if isinstance(self._widget, Gtk.Label):
                    self._widget.set_height_chars(value)
                else:
                    self._widget.set_size_request(-1, value)
            elif key == 'tooltip':
                if hasattr(self._widget, 'set_tooltip_text'):
                    self._widget.set_tooltip_text(value)
                else:
                    print(f"Warning: Widget {self.__class__.__name__} does not support tooltips")
            elif hasattr(self, f"_set_{key}"):
                getattr(self, f"_set_{key}")(value)
            elif hasattr(self._widget, f"set_{key}"):
                getattr(self._widget, f"set_{key}")(value)
            else:
                print(f"Warning: Unknown configuration option '{key}'")

    def configure(self, **kwargs):
        self._configure(**kwargs)

    def config(self, **kwargs):
        self.configure(**kwargs)

    def pack(self, **kwargs):
        self.master.pack(self, **kwargs)

    def grid(self, **kwargs):
        self.master.grid(self, **kwargs)

    def place(self, *args, **kwargs):
        self.master.place(self, *args, **kwargs)

    def bind(self, sequence, func, add=None):
        if sequence == "<Button-1>":
            self._widget.connect("button-press-event", lambda w, e: func(e) if e.button == 1 else None)
        elif sequence == "<ButtonRelease-1>":
            self._widget.connect("button-release-event", lambda w, e: func(e) if e.button == 1 else None)
        elif sequence == "<Motion>":
            self._widget.connect("motion-notify-event", func)
        elif sequence == "<Enter>":
            self._widget.connect("enter-notify-event", func)
        elif sequence == "<Leave>":
            self._widget.connect("leave-notify-event", func)
        elif sequence == "<Key>":
            self._widget.connect("key-press-event", func)
        elif sequence == "<FocusIn>":
            self._widget.connect("focus-in-event", func)
        elif sequence == "<FocusOut>":
            self._widget.connect("focus-out-event", func)
        else:
            print(f"Warning: Unsupported event sequence '{sequence}'")

    def unbind(self, sequence, funcid=None):
        pass

    def _set_anchor(self, anchor):
        anchor_map = {
            'n': (Gtk.Align.CENTER, Gtk.Align.START),
            'ne': (Gtk.Align.END, Gtk.Align.START),
            'e': (Gtk.Align.END, Gtk.Align.CENTER),
            'se': (Gtk.Align.END, Gtk.Align.END),
            's': (Gtk.Align.CENTER, Gtk.Align.END),
            'sw': (Gtk.Align.START, Gtk.Align.END),
            'w': (Gtk.Align.START, Gtk.Align.CENTER),
            'nw': (Gtk.Align.START, Gtk.Align.START),
            'center': (Gtk.Align.CENTER, Gtk.Align.CENTER)
        }
        if anchor in anchor_map:
            halign, valign = anchor_map[anchor]
            self._widget.set_halign(halign)
            self._widget.set_valign(valign)


class Button(Widget):
    def __init__(self, master=None, **kwargs):
        self._command = None
        self._click_handler_id = None
        self._default_ipadx = 10
        self._default_ipady = 5
        self._image = None
        self._image_widget = None
        self._label = None
        self._content_box = None
        self._gtk_button = None
        super().__init__(master, **kwargs)

    def _create_widget(self, **kwargs):
        self._gtk_button = Gtk.Button()

        self._content_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        self._label = Gtk.Label(label=kwargs.get('text', ''))
        self._content_box.pack_start(self._label, True, True, 0)
        self._gtk_button.add(self._content_box)

        if 'image' in kwargs:
            self._set_image(kwargs['image'])

        if 'command' in kwargs:
            self._set_command(kwargs['command'])

        if 'compound' in kwargs:
            self._set_compound(kwargs['compound'])

        self._set_internal_padding(self._default_ipadx, self._default_ipady)

        return self._gtk_button

    def _set_image(self, image):
        if isinstance(image, str):
            if not os.path.exists(image):
                raise ValueError(f"File {image} not found")
            image = PhotoImage(file=image)

        self._image = image

        self._image_widget = Gtk.Image.new_from_pixbuf(image.pixbuf)

        for child in self._content_box.get_children():
            if isinstance(child, Gtk.Image):
                self._content_box.remove(child)

        self._content_box.pack_start(self._image_widget, False, False, 0)
        self._content_box.reorder_child(self._image_widget, 0)
        self._content_box.show_all()

    def _set_command(self, command):
        if not callable(command):
            raise ValueError("Command must be callable")

        if self._click_handler_id is not None:
            self._gtk_button.disconnect(self._click_handler_id)

        self._command = command
        self._click_handler_id = self._gtk_button.connect("clicked", self._handle_click)

    def _handle_click(self, widget):
        if self._command:
            self._command()

    def _set_internal_padding(self, ipadx, ipady):
        self._content_box.set_margin_start(ipadx)
        self._content_box.set_margin_end(ipadx)
        self._content_box.set_margin_top(ipady)
        self._content_box.set_margin_bottom(ipady)

        width = self._content_box.get_preferred_width()[0] + ipadx * 2
        height = self._content_box.get_preferred_height()[0] + ipady * 2
        self._gtk_button.set_size_request(width, height)

    def _set_text(self, text):
        self._label.set_label(text)

    def _set_compound(self, compound):
        pos_map = {
            'left': 0,
            'right': 1,
            'top': 0,
            'bottom': 1
        }

        if compound in pos_map:
            for child in self._content_box.get_children():
                self._content_box.remove(child)

            if compound in ['left', 'top']:
                if self._image_widget:
                    self._content_box.pack_start(self._image_widget, False, False, 0)
                self._content_box.pack_start(self._label, True, True, 0)
            else:
                self._content_box.pack_start(self._label, True, True, 0)
                if self._image_widget:
                    self._content_box.pack_start(self._image_widget, False, False, 0)

            self._content_box.show_all()

    def _set_bg(self, color):
        rgba = Gdk.RGBA()
        if rgba.parse(color):
            self._gtk_button.override_background_color(Gtk.StateFlags.NORMAL, rgba)

    def _set_fg(self, color):
        rgba = Gdk.RGBA()
        if rgba.parse(color):
            self._label.override_color(Gtk.StateFlags.NORMAL, rgba)

    def configure(self, **kwargs):
        if 'command' in kwargs:
            self._set_command(kwargs['command'])
        if 'image' in kwargs:
            self._set_image(kwargs['image'])
        if 'compound' in kwargs:
            self._set_compound(kwargs['compound'])
        super().configure(**kwargs)

    def config(self, **kwargs):
        self.configure(**kwargs)

    def pack(self, **kwargs):
        self.master.pack(self, **kwargs)


class Label(Widget):
    def __init__(self, master=None, **kwargs):
        self._image = None
        self._images = {}
        self._label_widget = None
        self._image_widget = None
        super().__init__(master, **kwargs)

    def _create_widget(self, **kwargs):
        label = Gtk.Label(label=kwargs.get('text', ''))
        label.set_xalign(0.0)

        if 'image' in kwargs:
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            self._image_widget = Gtk.Image()
            box.pack_start(self._image_widget, False, False, 0)
            box.pack_start(label, True, True, 0)
            self._label_widget = label
            self._set_image(kwargs['image'])
            if 'compound' in kwargs:
                self._set_compound(kwargs['compound'])
            return box
        else:
            self._label_widget = label
            return label

    def _set_image(self, image):
        if isinstance(image, (str, PhotoImage)):
            if isinstance(image, str):
                if not os.path.exists(image):
                    raise ValueError(f"File {image} not found")
                image = PhotoImage(file=image)

            self._image = image
            self._images['current'] = image
            self._image_widget.set_from_pixbuf(image.pixbuf)

    def _get_text(self):
        return self._label_widget.get_label()

    def _set_text(self, text):
        self._label_widget.set_label(text)

    def _set_textvariable(self, var):
        var.trace('w', lambda *_: self._label_widget.set_label(var.get()))
        self._label_widget.set_label(var.get())

    def _set_compound(self, compound):
        if compound == 'left':
            self._label_widget.set_xalign(0.0)
        elif compound == 'right':
            self._label_widget.set_xalign(1.0)
        elif compound == 'center':
            self._label_widget.set_xalign(0.5)

    def _set_bg(self, color):
        rgba = Gdk.RGBA()
        if rgba.parse(color):
            self._widget.override_background_color(Gtk.StateFlags.NORMAL, rgba)

    def _set_fg(self, color):
        rgba = Gdk.RGBA()
        if rgba.parse(color):
            self._label_widget.override_color(Gtk.StateFlags.NORMAL, rgba)

    def _set_font(self, font):
        font_desc = self._parse_font(font)
        if font_desc:
            self._label_widget.override_font(font_desc)

    def _set_wrap(self, wrap):
        self._label_widget.set_line_wrap(wrap)

    def _set_justify(self, justify):
        justify_map = {
            'left': Gtk.Justification.LEFT,
            'right': Gtk.Justification.RIGHT,
            'center': Gtk.Justification.CENTER,
            'fill': Gtk.Justification.FILL
        }
        if justify in justify_map:
            self._label_widget.set_justify(justify_map[justify])

    def configure(self, **kwargs):
        if 'image' in kwargs:
            self._set_image(kwargs['image'])
        if 'compound' in kwargs:
            self._set_compound(kwargs['compound'])
        super().configure(**kwargs)


class Entry(Widget):
    def _create_widget(self, **kwargs):
        entry = Gtk.Entry()
        if 'show' in kwargs:
            entry.set_visibility(kwargs['show'] != '*')
        if 'textvariable' in kwargs:
            self._textvariable = kwargs['textvariable']
            entry.set_text(self._textvariable.get())
            self._textvariable.trace("w", self._update_text)
            entry.connect("changed", self._update_var)
        return entry

    def _set_text(self, text):
        self._widget.set_text(text)

    def get(self):
        return self._widget.get_text()

    def insert(self, index, text):
        self._widget.set_text(text)

    def delete(self, first, last=None):
        self._widget.set_text('')

    def _update_text(self, *args):
        self._widget.set_text(self._textvariable.get())

    def _update_var(self, widget):
        self._textvariable.set(widget.get_text())


class Text(Widget):
    def _create_widget(self, **kwargs):
        self._textview = Gtk.TextView()
        self._buffer = self._textview.get_buffer()
        self._widget = Gtk.ScrolledWindow()
        self._widget.add(self._textview)

        if 'wrap' in kwargs:
            wrap_mode = {
                'none': Gtk.WrapMode.NONE,
                'char': Gtk.WrapMode.CHAR,
                'word': Gtk.WrapMode.WORD,
                'word_char': Gtk.WrapMode.WORD_CHAR
            }.get(kwargs['wrap'], Gtk.WrapMode.WORD)
            self._textview.set_wrap_mode(wrap_mode)

        return self._widget

    def insert(self, index, text, tags=None):
        if isinstance(index, str) and index == 'end':
            iter = self._buffer.get_end_iter()
        else:
            iter = self._buffer.get_iter_at_line(index)
        self._buffer.insert(iter, text)

    def get(self, first, last=None):
        start = self._buffer.get_iter_at_line(first)
        end = self._buffer.get_iter_at_line(last) if last else self._buffer.get_end_iter()
        return self._buffer.get_text(start, end, True)

    def delete(self, first, last=None):
        start = self._buffer.get_iter_at_line(first)
        end = self._buffer.get_iter_at_line(last) if last else self._buffer.get_end_iter()
        self._buffer.delete(start, end)

    def tag_add(self, tag_name, first, last=None):
        pass

    def tag_config(self, tag_name, **kwargs):
        pass


class Frame(Widget):
    def _create_widget(self, **kwargs):
        frame = Gtk.Frame(label=kwargs.get('text', ''))
        self._inner_container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        frame.add(self._inner_container)
        return frame

    def _set_text(self, text):
        self._widget.set_label(text)

    def pack_configure(self, **kwargs):
        self.master._add_child(self._widget, **kwargs)

    def pack(self, widget, **kwargs):
        expand = kwargs.get('expand', False)
        fill = kwargs.get('fill', 'none')
        side = kwargs.get('side', 'top')
        padx = kwargs.get('padx', 0)
        pady = kwargs.get('pady', 0)

        widget._widget.set_margin_start(padx)
        widget._widget.set_margin_end(padx)
        widget._widget.set_margin_top(pady)
        widget._widget.set_margin_bottom(pady)

        if side in ['left', 'top']:
            self._inner_container.pack_start(widget._widget, expand, fill != 'none', 0)
        else:
            self._inner_container.pack_end(widget._widget, expand, fill != 'none', 0)

    def grid_configure(self, **kwargs):
        if not isinstance(self.master._container, Gtk.Grid):
            self.master._container = Gtk.Grid()
            self.master.window.remove(self.master._container)
            self.master.window.add(self.master._container)
        self.master._add_child(self._widget, **kwargs)

    def grid(self, widget, **kwargs):
        if not isinstance(self._inner_container, Gtk.Grid):
            old_container = self._inner_container
            self._inner_container = Gtk.Grid()

            for child in old_container.get_children():
                old_container.remove(child)
                self._inner_container.attach(child, 0, 0, 1, 1)

            self._widget.remove(old_container)
            self._widget.add(self._inner_container)

        self._inner_container.attach(
            widget._widget,
            kwargs.get('column', 0),
            kwargs.get('row', 0),
            kwargs.get('columnspan', 1),
            kwargs.get('rowspan', 1)
        )


class Checkbutton(Widget):
    def _create_widget(self, **kwargs):
        check = Gtk.CheckButton(label=kwargs.get('text', ''))
        if 'variable' in kwargs:
            self._variable = kwargs['variable']
            check.set_active(self._variable.get())
            check.connect("toggled", self._update_var)
        return check

    def _set_text(self, text):
        self._widget.set_label(text)

    def _update_var(self, widget):
        self._variable.set(widget.get_active())

    def select(self):
        self._widget.set_active(True)

    def deselect(self):
        self._widget.set_active(False)

    def toggle(self):
        self._widget.set_active(not self._widget.get_active())


class Radiobutton(Widget):
    def _create_widget(self, **kwargs):
        group = kwargs.get('group', None)
        if group and hasattr(group, '_widget'):
            radio = Gtk.RadioButton.new_with_label_from_widget(group._widget, kwargs.get('text', ''))
        else:
            radio = Gtk.RadioButton.new_with_label([], kwargs.get('text', ''))

        if 'variable' in kwargs and 'value' in kwargs:
            self._variable = kwargs['variable']
            self._value = kwargs['value']
            if self._variable.get() == self._value:
                radio.set_active(True)
            radio.connect("toggled", self._update_var)

        return radio

    def _set_text(self, text):
        self._widget.set_label(text)

    def _update_var(self, widget):
        if widget.get_active():
            self._variable.set(self._value)

    def select(self):
        self._widget.set_active(True)

    def deselect(self):
        self._widget.set_active(False)


class Listbox(Widget):
    def _create_widget(self, **kwargs):
        self._liststore = Gtk.ListStore(str)
        self._treeview = Gtk.TreeView(model=self._liststore)

        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Items", renderer, text=0)
        self._treeview.append_column(column)

        self._widget = Gtk.ScrolledWindow()
        self._widget.add(self._treeview)
        return self._widget

    def insert(self, index, text):
        if index == 'end':
            self._liststore.append([text])
        else:
            self._liststore.insert(index, [text])

    def delete(self, first, last=None):
        if last is None:
            path = Gtk.TreePath.new_from_string(str(first))
            iter = self._liststore.get_iter(path)
            self._liststore.remove(iter)
        else:
            for i in range(first, last):
                path = Gtk.TreePath.new_from_string(str(i))
                iter = self._liststore.get_iter(path)
                self._liststore.remove(iter)

    def get(self, index):
        path = Gtk.TreePath.new_from_string(str(index))
        iter = self._liststore.get_iter(path)
        return self._liststore.get_value(iter, 0)

    def size(self):
        return len(self._liststore)


class Scrollbar(Widget):
    def _create_widget(self, **kwargs):
        if kwargs.get('orient', 'vertical') == 'vertical':
            return Gtk.VScrollbar()
        return Gtk.HScrollbar()


class Canvas(Widget):
    def _create_widget(self, **kwargs):
        self._drawing_area = Gtk.DrawingArea()
        self._drawing_area.connect("draw", self._on_draw)
        self._items = []
        self._widget = Gtk.ScrolledWindow()
        self._widget.add(self._drawing_area)

        if 'width' in kwargs or 'height' in kwargs:
            width = kwargs.get('width', 200)
            height = kwargs.get('height', 200)
            self._drawing_area.set_size_request(width, height)

        return self._widget

    def _on_draw(self, widget, cr):
        for item in self._items:
            if item['type'] == 'rectangle':
                cr.rectangle(item['x'], item['y'], item['width'], item['height'])
                if 'fill' in item:
                    cr.set_source_rgb(*item['fill'])
                    cr.fill_preserve()
                if 'outline' in item:
                    cr.set_source_rgb(*item['outline'])
                    cr.stroke()
            elif item['type'] == 'oval':
                cr.arc(item['x'] + item['width'] / 2, item['y'] + item['height'] / 2,
                       min(item['width'], item['height']) / 2, 0, 2 * 3.1415926)
                if 'fill' in item:
                    cr.set_source_rgb(*item['fill'])
                    cr.fill_preserve()
                if 'outline' in item:
                    cr.set_source_rgb(*item['outline'])
                    cr.stroke()
            elif item['type'] == 'line':
                cr.move_to(item['x1'], item['y1'])
                cr.line_to(item['x2'], item['y2'])
                if 'fill' in item:
                    cr.set_source_rgb(*item['fill'])
                    cr.stroke()
            elif item['type'] == 'text':
                cr.move_to(item['x'], item['y'])
                if 'font' in item:
                    cr.set_font_size(item['font'][1])
                cr.show_text(item['text'])

    def create_rectangle(self, x1, y1, x2, y2, **kwargs):
        self._items.append({
            'type': 'rectangle',
            'x': x1, 'y': y1,
            'width': x2 - x1, 'height': y2 - y1,
            'fill': kwargs.get('fill'),
            'outline': kwargs.get('outline')
        })
        self._drawing_area.queue_draw()

    def create_oval(self, x1, y1, x2, y2, **kwargs):
        self._items.append({
            'type': 'oval',
            'x': x1, 'y': y1,
            'width': x2 - x1, 'height': y2 - y1,
            'fill': kwargs.get('fill'),
            'outline': kwargs.get('outline')
        })
        self._drawing_area.queue_draw()

    def create_line(self, x1, y1, x2, y2, **kwargs):
        self._items.append({
            'type': 'line',
            'x1': x1, 'y1': y1,
            'x2': x2, 'y2': y2,
            'fill': kwargs.get('fill')
        })
        self._drawing_area.queue_draw()

    def create_text(self, x, y, text, **kwargs):
        self._items.append({
            'type': 'text',
            'x': x, 'y': y,
            'text': text,
            'font': kwargs.get('font', ('Arial', 12))
        })
        self._drawing_area.queue_draw()

    def delete(self, item_id):
        if 0 <= item_id < len(self._items):
            del self._items[item_id]
            self._drawing_area.queue_draw()


class PhotoImage:
    def __init__(self, file=None, **kwargs):
        self.pixbuf = None
        self._subsample_cache = {}
        self._zoom_cache = {}

        if file:
            if not os.path.exists(file):
                raise ValueError(f"File {file} not found")
            self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(file)
        else:
            width = kwargs.get('width', 100)
            height = kwargs.get('height', 100)
            self.pixbuf = GdkPixbuf.Pixbuf.new(GdkPixbuf.Colorspace.RGB, True, 8, width, height)
            self.pixbuf.fill(0xffffffff)

    def subsample(self, x_denominator, y_denominator):
        key = (x_denominator, y_denominator)
        if key not in self._subsample_cache:
            width = self.pixbuf.get_width() // x_denominator
            height = self.pixbuf.get_height() // y_denominator
            self._subsample_cache[key] = self.pixbuf.scale_simple(
                width, height, GdkPixbuf.InterpType.NEAREST)
        return self._subsample_cache[key]

    def zoom(self, x_numerator, y_numerator):
        key = (x_numerator, y_numerator)
        if key not in self._zoom_cache:
            width = self.pixbuf.get_width() * x_numerator
            height = self.pixbuf.get_height() * y_numerator
            self._zoom_cache[key] = self.pixbuf.scale_simple(
                width, height, GdkPixbuf.InterpType.BILINEAR)
        return self._zoom_cache[key]

    def width(self):
        return self.pixbuf.get_width()

    def height(self):
        return self.pixbuf.get_height()


class StringVar:
    def __init__(self, master=None, value=""):
        self._value = value
        self._trace_callbacks = []

    def get(self):
        return self._value

    def set(self, new_value):
        if self._value != new_value:
            self._value = new_value
            for callback in self._trace_callbacks:
                callback()

    def trace(self, mode, callback):
        self._trace_callbacks.append(callback)
        return callback


class IntVar:
    def __init__(self, master=None, value=0):
        self._value = value
        self._trace_callbacks = []

    def get(self):
        return self._value

    def set(self, new_value):
        if self._value != new_value:
            self._value = new_value
            for callback in self._trace_callbacks:
                callback()

    def trace(self, mode, callback):
        self._trace_callbacks.append(callback)
        return callback


class BooleanVar:
    def __init__(self, master=None, value=False):
        self._value = value
        self._trace_callbacks = []

    def get(self):
        return self._value

    def set(self, new_value):
        if self._value != new_value:
            self._value = new_value
            for callback in self._trace_callbacks:
                callback()

    def trace(self, mode, callback):
        self._trace_callbacks.append(callback)
        return callback


class Scale(Widget):
    def _create_widget(self, **kwargs):
        orientation = Gtk.Orientation.HORIZONTAL
        if kwargs.get('orient', 'horizontal') == 'vertical':
            orientation = Gtk.Orientation.VERTICAL

        adjustment = Gtk.Adjustment(
            value=kwargs.get('from_', 0),
            lower=kwargs.get('from_', 0),
            upper=kwargs.get('to', 100),
            step_increment=kwargs.get('resolution', 1),
            page_increment=kwargs.get('bigstep', 10)
        )

        scale = Gtk.Scale(orientation=orientation, adjustment=adjustment)
        scale.set_digits(kwargs.get('digits', 0))
        scale.set_value_pos(kwargs.get('sliderrelief', Gtk.PositionType.BOTTOM))

        if 'command' in kwargs:
            scale.connect("value-changed", lambda s: kwargs['command'](s.get_value()))

        return scale

    def get(self):
        return self._widget.get_value()

    def set(self, value):
        self._widget.set_value(value)


class Message(Widget):
    def _create_widget(self, **kwargs):
        message = Gtk.Label(label=kwargs.get('text', ''))
        message.set_line_wrap(True)
        message.set_xalign(0)
        return message


class MenuBar(Widget):
    def _create_widget(self, **kwargs):
        self._menubar = Gtk.MenuBar()
        return self._menubar

    def add_cascade(self, label, menu):
        menu_item = Gtk.MenuItem(label=label)
        menu_item.set_submenu(menu._widget)
        self._menubar.append(menu_item)
        menu_item.show_all()
        return menu_item


class Menu(Widget):
    def _create_widget(self, **kwargs):
        return Gtk.Menu()

    def add_command(self, **kwargs):
        item = Gtk.MenuItem(label=kwargs.get('label', ''))
        if 'command' in kwargs:
            item.connect("activate", lambda _: kwargs['command']())
        self._widget.append(item)
        item.show()
        return item

    def add_cascade(self, **kwargs):
        item = Gtk.MenuItem(label=kwargs.get('label', ''))
        submenu = kwargs.get('menu', None)
        if submenu:
            item.set_submenu(submenu._widget)
        self._widget.append(item)
        item.show()
        return item

    def add_separator(self):
        separator = Gtk.SeparatorMenuItem()
        self._widget.append(separator)
        separator.show()
        return separator

    def add_checkbutton(self, **kwargs):
        item = Gtk.CheckMenuItem(label=kwargs.get('label', ''))
        if 'variable' in kwargs:
            var = kwargs['variable']
            item.set_active(var.get())
            item.connect("toggled", lambda w: var.set(w.get_active()))
        if 'command' in kwargs:
            item.connect("toggled", lambda w: kwargs['command']())
        self._widget.append(item)
        item.show()
        return item

    def add_radiobutton(self, **kwargs):
        group = kwargs.get('group', None)
        if group and hasattr(group, '_widget'):
            item = Gtk.RadioMenuItem.new_with_label_from_widget(group._widget, kwargs.get('label', ''))
        else:
            item = Gtk.RadioMenuItem.new_with_label([], kwargs.get('label', ''))

        if 'variable' in kwargs and 'value' in kwargs:
            var = kwargs['variable']
            value = kwargs['value']
            if var.get() == value:
                item.set_active(True)
            item.connect("toggled", lambda w: var.set(value) if w.get_active() else None)

        if 'command' in kwargs:
            item.connect("toggled", lambda w: kwargs['command']())

        self._widget.append(item)
        item.show()
        return item


class Notebook(Widget):
    def _create_widget(self, **kwargs):
        notebook = Gtk.Notebook()
        notebook.set_scrollable(True)
        return notebook

    def add(self, child, **kwargs):
        tab_label = kwargs.get('text', '')
        if 'image' in kwargs:
            tab_label = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
            img = Gtk.Image.new_from_pixbuf(kwargs['image'].pixbuf)
            tab_label.pack_start(img, False, False, 0)
            label = Gtk.Label(label=kwargs.get('text', ''))
            tab_label.pack_start(label, False, False, 0)
            tab_label.show_all()

        self._widget.append_page(child._widget, tab_label)

    def insert(self, pos, child, **kwargs):
        tab_label = kwargs.get('text', '')
        self._widget.insert_page(child._widget, Gtk.Label(label=tab_label), pos)


class Separator(Widget):
    def _create_widget(self, **kwargs):
        if kwargs.get('orient', 'horizontal') == 'horizontal':
            return Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        return Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)


class ProgressBar(Widget):
    def _create_widget(self, **kwargs):
        pb = Gtk.ProgressBar()
        pb.set_fraction(kwargs.get('value', 0) / 100.0)
        pb.set_show_text(kwargs.get('showtext', False))
        return pb

    def start(self, interval=50):
        self._widget.pulse()
        GLib.timeout_add(interval, self._widget.pulse)

    def stop(self):
        self._widget.set_fraction(0)

    def step(self, amount=1):
        self._widget.set_fraction(min(1.0, self._widget.get_fraction() + amount / 100.0))


class TreeView(Widget):
    def _create_widget(self, **kwargs):
        self._liststore = Gtk.ListStore(*([str] * kwargs.get('columns', 1)))
        treeview = Gtk.TreeView(model=self._liststore)

        for i in range(kwargs.get('columns', 1)):
            renderer = Gtk.CellRendererText()
            column = Gtk.TreeViewColumn(f"Column {i + 1}", renderer, text=i)
            treeview.append_column(column)

        self._widget = Gtk.ScrolledWindow()
        self._widget.add(treeview)
        return self._widget

    def insert(self, parent, index, *values):
        return self._liststore.insert(parent, index, list(values))

    def delete(self, iter):
        self._liststore.remove(iter)

    def get_children(self, iter=None):
        return self._liststore.iter_children(iter)


class MessageDialog:
    def __init__(self, parent=None, **kwargs):
        buttons = {
            'ok': Gtk.ButtonsType.OK,
            'okcancel': Gtk.ButtonsType.OK_CANCEL,
            'yesno': Gtk.ButtonsType.YES_NO,
            'yesnocancel': Gtk.ButtonsType.YES_NO_CANCEL
        }.get(kwargs.get('buttons', 'ok'), Gtk.ButtonsType.OK)

        self.dialog = Gtk.MessageDialog(
            transient_for=parent.window if parent else None,
            flags=0,
            message_type=getattr(Gtk.MessageType, kwargs.get('type', 'info').upper()),
            buttons=buttons,
            text=kwargs.get('title', '')
        )
        self.dialog.format_secondary_text(kwargs.get('message', ''))

    def show(self):
        response = self.dialog.run()
        self.dialog.destroy()

        return {
            Gtk.ResponseType.OK: 'ok',
            Gtk.ResponseType.YES: 'yes',
            Gtk.ResponseType.NO: 'no',
            Gtk.ResponseType.CANCEL: 'cancel'
        }.get(response, 'cancel')


def messagebox(**kwargs):
    dialog = MessageDialog(**kwargs)
    return dialog.show()


class AboutDialog(Widget):
    def _create_widget(self, **kwargs):
        dialog = Gtk.AboutDialog()
        dialog.set_program_name(kwargs.get('title', ''))
        dialog.set_version(kwargs.get('version', ''))
        dialog.set_comments(kwargs.get('message', ''))

        if 'icon' in kwargs:
            dialog.set_logo(kwargs['icon'].pixbuf)

        return dialog

    def show(self):
        response = self._widget.run()
        self._widget.destroy()
        return response == Gtk.ResponseType.OK


class FileDialog:
    def __init__(self, parent=None, **kwargs):
        action = {
            'open': Gtk.FileChooserAction.OPEN,
            'save': Gtk.FileChooserAction.SAVE,
            'dir': Gtk.FileChooserAction.SELECT_FOLDER
        }.get(kwargs.get('action', 'open'), Gtk.FileChooserAction.OPEN)

        self.dialog = Gtk.FileChooserDialog(
            title=kwargs.get('title', ''),
            transient_for=parent.window if parent else None,
            action=action
        )

        self.dialog.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.dialog.add_button("OK", Gtk.ResponseType.OK)

    def show(self):
        response = self.dialog.run()
        filename = self.dialog.get_filename()
        self.dialog.destroy()

        if response == Gtk.ResponseType.OK:
            return filename
        return None


class ColorButton(Widget):
    def _create_widget(self, **kwargs):
        btn = Gtk.ColorButton()
        if 'color' in kwargs:
            rgba = Gdk.RGBA()
            rgba.parse(kwargs['color'])
            btn.set_rgba(rgba)
        return btn

    def get_color(self):
        return self._widget.get_rgba().to_string()


class FontButton(Widget):
    def _create_widget(self, **kwargs):
        btn = Gtk.FontButton()
        if 'font' in kwargs:
            btn.set_font_name(kwargs['font'])
        return btn

    def get_font(self):
        return self._widget.get_font_name()


class SpinButton(Widget):
    def _create_widget(self, **kwargs):
        adjustment = Gtk.Adjustment(
            value=kwargs.get('value', 0),
            lower=kwargs.get('from_', 0),
            upper=kwargs.get('to', 100),
            step_increment=kwargs.get('step', 1)
        )
        spin = Gtk.SpinButton(adjustment=adjustment, climb_rate=1, digits=0)
        return spin

    def get(self):
        return self._widget.get_value()

    def set(self, value):
        self._widget.set_value(value)


class Switch(Widget):
    def _create_widget(self, **kwargs):
        switch = Gtk.Switch()
        switch.set_active(kwargs.get('value', False))
        return switch

    def get(self):
        return self._widget.get_active()

    def set(self, value):
        self._widget.set_active(value)


class Statusbar(Widget):
    def _create_widget(self, **kwargs):
        self._context_id = 1
        return Gtk.Statusbar()

    def add_message(self, text):
        return self._widget.push(self._context_id, text)

    def remove_message(self, message_id):
        self._widget.remove(self._context_id, message_id)


class Toplevel(Tk):
    def __init__(self, master=None):
        super().__init__()
        self._master = master


def bind(widget, sequence, func, add=None):
    return widget.bind(sequence, func, add)


def unbind(widget, sequence, funcid=None):
    widget.unbind(sequence, funcid)


def config(widget, **kwargs):
    widget.configure(**kwargs)


class Combobox(Widget):
    def _create_widget(self, **kwargs):
        self._liststore = Gtk.ListStore(str)
        self._combobox = Gtk.ComboBox.new_with_model(self._liststore)
        renderer = Gtk.CellRendererText()
        self._combobox.pack_start(renderer, True)
        self._combobox.add_attribute(renderer, "text", 0)

        if 'values' in kwargs:
            for value in kwargs['values']:
                self._liststore.append([str(value)])

        if 'textvariable' in kwargs:
            self._textvariable = kwargs['textvariable']
            self._combobox.set_active_id(self._textvariable.get())
            self._combobox.connect("changed", self._update_var)

        return self._combobox

    def _update_var(self, widget):
        active = widget.get_active()
        if active >= 0:
            self._textvariable.set(self._liststore[active][0])

    def get(self):
        active = self._combobox.get_active()
        if active >= 0:
            return self._liststore[active][0]
        return None

    def set(self, value):
        for i, row in enumerate(self._liststore):
            if row[0] == str(value):
                self._combobox.set_active(i)
                return
        self._combobox.set_active(-1)


class Paned(Widget):
    def _create_widget(self, **kwargs):
        orientation = Gtk.Orientation.HORIZONTAL
        if kwargs.get('orient', 'horizontal') == 'vertical':
            orientation = Gtk.Orientation.VERTICAL

        self._paned = Gtk.Paned(orientation=orientation)
        return self._paned

    def add1(self, widget):
        self._paned.pack1(widget._widget, resize=True, shrink=False)

    def add2(self, widget):
        self._paned.pack2(widget._widget, resize=True, shrink=False)


class Toolbar(Widget):
    def _create_widget(self, **kwargs):
        self._toolbar = Gtk.Toolbar()
        return self._toolbar

    def add_button(self, text=None, image=None, command=None):
        if image and isinstance(image, (str, PhotoImage)):
            if isinstance(image, str):
                if not os.path.exists(image):
                    raise ValueError(f"File {image} not found")
                image = PhotoImage(file=image)
            tool_button = Gtk.ToolButton.new(Gtk.Image.new_from_pixbuf(image.pixbuf), text)
        else:
            tool_button = Gtk.ToolButton.new(None, text)

        if command:
            tool_button.connect("clicked", lambda _: command())

        self._toolbar.insert(tool_button, -1)
        return tool_button

    def add_separator(self):
        separator = Gtk.SeparatorToolItem()
        self._toolbar.insert(separator, -1)
        return separator


class Expander(Widget):
    def _create_widget(self, **kwargs):
        self._expander = Gtk.Expander(label=kwargs.get('text', ''))
        self._inner_widget = None
        return self._expander

    def add(self, widget):
        if self._inner_widget:
            self._expander.remove(self._inner_widget)
        self._inner_widget = widget._widget
        self._expander.add(widget._widget)

    def _set_text(self, text):
        self._expander.set_label(text)


class Spinner(Widget):
    def _create_widget(self, **kwargs):
        self._spinner = Gtk.Spinner()
        return self._spinner

    def start(self):
        self._spinner.start()

    def stop(self):
        self._spinner.stop()


class LinkButton(Widget):
    def _create_widget(self, **kwargs):
        btn = Gtk.LinkButton(uri=kwargs.get('uri', ''), label=kwargs.get('text', ''))
        return btn

    def _set_text(self, text):
        self._widget.set_label(text)

    def _set_uri(self, uri):
        self._widget.set_uri(uri)


class Calendar(Widget):
    def _create_widget(self, **kwargs):
        self._calendar = Gtk.Calendar()
        return self._calendar

    def get_date(self):
        year, month, day = self._calendar.get_date()
        return (year, month + 1, day)

    def set_date(self, year, month, day):
        self._calendar.select_month(month - 1, year)
        self._calendar.select_day(day)

def askopenfilename(**kwargs):
    dialog = FileDialog(**kwargs)
    return dialog.show()

def asksaveasfilename(**kwargs):
    kwargs['action'] = 'save'
    dialog = FileDialog(**kwargs)
    return dialog.show()

def askdirectory(**kwargs):
    kwargs['action'] = 'dir'
    dialog = FileDialog(**kwargs)
    return dialog.show()

def askcolor(**kwargs):
    dialog = ColorChooserDialog(**kwargs)
    return dialog.show()


class ColorChooserDialog:
    def __init__(self, parent=None, **kwargs):
        self.dialog = Gtk.ColorChooserDialog(
            title=kwargs.get('title', 'Select Color'),
            transient_for=parent.window if parent else None
        )

    def show(self):
        response = self.dialog.run()
        color = None
        if response == Gtk.ResponseType.OK:
            rgba = self.dialog.get_rgba()
            color = "#{:02x}{:02x}{:02x}".format(
                int(rgba.red * 255),
                int(rgba.green * 255),
                int(rgba.blue * 255)
            )
        self.dialog.destroy()
        return color

Toplevel = Tk
root = Tk