""" Defines and manages variant data models"""
import os.path
from marshmallow import Schema, fields, post_load
import buildplate.thumbnail


class Variant:  # pylint: disable=too-few-public-methods
    """ Represents a variant of a project """

    def __init__(self):
        self.project = None
        self.description = None
        self.build_file_path = None
        self.preview_image_path = None
        self.slicer_profile_file_path = None

    @staticmethod
    def from_dict(data):
        """ Deserializes a dict into a Variant instance """
        variant = Variant()
        variant.project = data.get("project")
        variant.description = data["description"]
        variant.build_file_path = data["build_file_path"]
        variant.preview_image_path = data["preview_image_path"]
        variant.slicer_profile_file_path = data["slicer_profile_file_path"]

        return variant

    def generate_preview_image(self):
        """ Generates a preview image in PNG format from the build file """
        build_file_name, _ext = os.path.splitext(
            os.path.basename(self.build_file_path))
        preview_file_name = f"{build_file_name}_preview.png"
        expected_preview_path = self.project.images_dir().joinpath(preview_file_name)
        buildplate.thumbnail.generate_thumbnail(
            self.project.root.joinpath(self.build_file_path), expected_preview_path)
        assert os.path.exists(expected_preview_path)

        self.preview_image_path = expected_preview_path


class VariantSchema(Schema):
    """ Represents a variant persisted into a portable format (e.g. JSON) """
    project = fields.Nested("ProjectSchema", exclude=[
                            "variants"], load_only=True)
    description = fields.Str(allow_none=True)
    build_file_path = fields.Str(required=True)
    preview_image_path = fields.Str(allow_none=True)
    slicer_profile_file_path = fields.Str(allow_none=True)

    @post_load
    def make_variant(self, data, **_kwargs):  # pylint: disable=no-self-use
        """ Invoked by the schema to transform a deserialized dict into a Variant instance"""
        return Variant.from_dict(data)
