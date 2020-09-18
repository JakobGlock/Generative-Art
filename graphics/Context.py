import cairo
from uuid import uuid4
from .Helpers import does_path_exist, open_file
from os import path
from datetime import datetime


class DrawContext:
    def __init__(self, width, height, file_format, filepath, project_folder, open_bool):
        self.open_bool = open_bool
        self.width = width
        self.height = height
        self.file_format = file_format
        self.filename = self.generate_filename()
        self.filepath = filepath
        self.project_folder = "/" + project_folder[:-3]
        self.cwd = self.set_cwd()
        self.fullpath = self.cwd + "/" + self.filename + "." + self.file_format.lower()
        self.init()

    def init(self):
        does_path_exist(self.cwd)

        if self.file_format == 'PNG':
            self.cairo_context = self.setup_png()
        elif self.file_format == 'SVG':
            self.cairo_context = self.setup_svg()

    def setup_png(self):
        self.surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.width, self.height)
        return cairo.Context(self.surface)

    def export_png(self):
        self.surface.write_to_png(self.fullpath)
        print("INFO: Saving file to {}".format(self.fullpath))
        if self.open_bool:
            print("INFO: Opening file {}".format(self.fullpath))
            open_file(self.fullpath)

    def setup_svg(self):
        self.surface = cairo.SVGSurface(self.fullpath, self.width, self.height)
        return cairo.Context(self.surface)

    def export_svg(self):
        self.surface.finish()
        print("INFO: Saving file to {}".format(self.fullpath))
        if self.open_bool:
            print("INFO: Opening file {}".format(self.fullpath))
            open_file(self.fullpath)

    def export(self):
        if self.file_format == "PNG":
            self.export_png()
        elif self.file_format == "SVG":
            self.export_svg()

    @property
    def context(self):
        return self.cairo_context

    @context.setter
    def context(self, context):
        self.context = context

    def get_file_name(self):
        return self.filename

    def get_fullpath(self):
        return self.fullpath

    def generate_filename(self):
        now = datetime.now()
        timestamp = now.strftime("%Y%d%m-%H%M%S")
        unique_id = uuid4().hex[:8]
        return str(timestamp + "-" + unique_id)

    def set_cwd(self):
        if self.file_format == "PNG":
            return path.dirname(path.realpath(__file__))[:-9] + self.filepath + self.project_folder
        elif self.file_format == "SVG":
            return path.dirname(path.realpath(__file__))[:-9] + self.filepath + self.project_folder + "/0-svg"
        else:
            print("ERROR: Choose a valid file format: PNG|SVG")
            exit(0)
