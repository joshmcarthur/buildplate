""" Defines and manages variant data models"""
from marshmallow import Schema, fields, post_load


class Variant:  # pylint: disable=too-few-public-methods
    """ Represents a variant of a project """

    def __init__(self):
        self.description = None
        self.build_file_path = None
        self.preview_image_path = None
        self.slicer_profile_file_path = None

    @staticmethod
    def from_dict(data):
        """ Deserializes a dict into a Variant instance """
        variant = Variant()
        variant.description = data["description"]
        variant.build_file_path = data["build_file_path"]
        variant.preview_image_path = data["preview_image_path"]
        variant.slicer_profile_file_path = data["slicer_profile_file_path"]


class VariantSchema(Schema):
    """ Represents a variant persisted into a portable format (e.g. JSON) """
    description = fields.Str()
    build_file_path = fields.Str(required=True)
    preview_image_path = fields.Str()
    slicer_profile_file_path = fields.Str()

    @post_load
    def make_variant(self, data, **_kwargs):  # pylint: disable=no-self-use
        """ Invoked by the schema to transform a deserialized dict into a Variant instance"""
        return Variant.from_dict(data)
