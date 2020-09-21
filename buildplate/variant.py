""" Defines and manages variant data models"""
import os.path
from marshmallow import Schema, fields, post_load
import buildplate.thumbnail

VariantImageSchema = Schema.from_dict({
    'type': fields.Str(), 
    'dimensions': fields.List(fields.Int()),
    'path': fields.Str()
})

class Variant:  # pylint: disable=too-few-public-methods
    """ Represents a variant of a project """

    def __init__(self):
        self.project = None
        self.description = None
        self.build_file_path = None
        self.preview_image_paths = []
        self.slicer_profile_file_path = None

    @staticmethod
    def from_dict(data):
        """ Deserializes a dict into a Variant instance """
        variant = Variant()
        variant.project = data.get("project")
        variant.description = data["description"]
        variant.build_file_path = data["build_file_path"]
        variant.preview_image_paths = data["preview_image_paths"]
        variant.slicer_profile_file_path = data["slicer_profile_file_path"]

        return variant


    def attach_image(self, path, type=type, dimensions=[None]):
        return self.preview_image_paths.append({
            'type': type,
            'dimensions': dimensions,
            'path': path
        })

    def generate_preview_image(self):
        """ Generates a preview image in PNG format from the build file """
        build_file_name, _ext = os.path.splitext(
            os.path.basename(self.build_file_path))
        preview_file_name = f"{build_file_name}_preview.png"
        size = [1280, int(1280 * 0.67)]
        output_path = self.project.images_dir(absolute=True).joinpath(preview_file_name)
        buildplate.thumbnail.generate_thumbnail(
            self.project.root.joinpath(self.build_file_path), output_path, size=size)
        assert os.path.exists(output_path)

        self.attach_image(
            self.project.images_dir().joinpath(preview_file_name),
            type='card_preview_image',
            dimensions=size
        )


class VariantSchema(Schema):
    """ Represents a variant persisted into a portable format (e.g. JSON) """
    project = fields.Nested("ProjectSchema", exclude=[
                            "variants"], load_only=True)
    description = fields.Str(allow_none=True)
    build_file_path = fields.Str(required=True)
    preview_image_paths = fields.List(fields.Nested(VariantImageSchema))
    slicer_profile_file_path = fields.Str(allow_none=True)

    @post_load
    def make_variant(self, data, **_kwargs):  # pylint: disable=no-self-use
        """ Invoked by the schema to transform a deserialized dict into a Variant instance"""
        return Variant.from_dict(data)
