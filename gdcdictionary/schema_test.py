"""This is an example of json schema for the GDC using schemas defined
in local yaml files.

Included are a few functions to augment jsonschema and the python
validator.

Examples are at the end.

"""

from __future__ import print_function

import argparse
import copy
import glob
import json
import os
import unittest
import yaml

from jsonschema import validate, ValidationError

from gdcdictionary import gdcdictionary


def load_yaml_schema(path):
    """Load yaml schema"""
    with open(path, "r", encoding="utf8") as f:
        return yaml.safe_load(f)


CUR_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(CUR_DIR, "examples")
project1 = load_yaml_schema(os.path.join(CUR_DIR, "schemas/projects/project1.yaml"))
projects = {"project1": project1}


def merge_schemas(schema_a, schema_b, path=None):
    """Recursively zip schemas together"""
    path = path if path is not None else []
    for key in schema_b:
        path_to_key = ".".join(path + [str(key)])
        if key in schema_a:
            if isinstance(schema_a[key], dict) and isinstance(schema_b[key], dict):
                merge_schemas(schema_a[key], schema_b[key], path + [str(key)])
            elif schema_a[key] == schema_b[key]:
                pass
            else:
                print(
                    f"Overriding '{path_to_key}':\n\t- {schema_a[key]}\n\t+ {schema_b[key]}"
                )
                schema_a[key] = schema_b[key]
        else:
            print(f"Adding '{path_to_key}':\n\t+ {schema_b[key]}")
            schema_a[key] = schema_b[key]
    return schema_a


def get_project_specific_schema(projects, project, schema, entity_type):
    """Look up the core schema for its type and override it with any
    project level overrides

    """
    root = copy.deepcopy(schema)
    project_overrides = projects.get(project)
    if project_overrides:
        overrides = project_overrides.get(entity_type)
        if overrides:
            merge_schemas(root, overrides, [entity_type])
    return root


def validate_entity(entity, schemata, project=None, name=""):
    """Validate an entity by looking up the core schema for its type and
    overriding it with any project level overrides

    """
    local_schema = get_project_specific_schema(
        projects, project, schemata[entity["type"]], entity["type"]
    )
    result = validate(entity, local_schema)
    return result


def validate_schemata(schemata, metaschema):
    """Validate schemata"""
    print("Validating schemas against metaschema... ", end=" ")
    for s in schemata.values():
        validate(s, metaschema)
        s_id = s["id"]
        def assert_link_is_also_prop(link):
            assert (
                link in s["properties"]
            ), f"Entity '{s_id}' has '{link}' as a link but not property"

        for link in [l["name"] for l in s["links"] if "name" in l]:
            assert_link_is_also_prop(link)
        for subgroup in [l["subgroup"] for l in s["links"] if "name" not in l]:
            for link in [l["name"] for l in subgroup if "name" in l]:
                assert_link_is_also_prop(link)


class SchemaTest(unittest.TestCase):
    def setUp(self):
        self.dictionary = gdcdictionary
        self.definitions = yaml.safe_load(
            open(os.path.join(CUR_DIR, "schemas", "_definitions.yaml"), "r", encoding="utf8")
        )

    def test_schemas(self):
        """Validate schema against metaschema"""
        validate_schemata(self.dictionary.schema, self.dictionary.metaschema)

    def test_valid_files(self):
        """Test files that are expected to be valid"""
        for path in glob.glob(os.path.join(DATA_DIR, "valid", "*.json")):
            print(f"Validating {path}")
            doc = json.load(open(path, "r", encoding="utf8"))
            print(doc)
            if isinstance(doc, dict):
                self.add_system_props(doc)
                validate_entity(doc, self.dictionary.schema)
            elif isinstance(doc, list):
                for entity in doc:
                    self.add_system_props(entity)
                    validate_entity(entity, self.dictionary.schema)
            else:
                raise Exception("Invalid json")

    def test_invalid_files(self):
        """Test files that are expected to be invalid"""
        for path in glob.glob(os.path.join(DATA_DIR, "invalid", "*.json")):
            print(f"Validating {path}")
            doc = json.load(open(path, "r", encoding="utf8"))
            if isinstance(doc, dict):
                self.add_system_props(doc)
                with self.assertRaises(ValidationError):
                    validate_entity(doc, self.dictionary.schema)
            elif isinstance(doc, list):
                for entity in doc:
                    self.add_system_props(entity)
                    with self.assertRaises(ValidationError):
                        validate_entity(entity, self.dictionary.schema)
            else:
                raise Exception("Invalid json")

    def add_system_props(self, doc):
        """Add system props"""
        schema = self.dictionary.schema[doc["type"]]
        for key in schema["systemProperties"]:
            use_def_default = (
                "$ref" in schema["properties"][key]
                and key in self.definitions
                and "default" in self.definitions[key]
            )
            if use_def_default:
                doc[key] = self.definitions[key]["default"]


if __name__ == "__main__":
    ####################
    # Setup
    ####################

    parser = argparse.ArgumentParser(description="Validate JSON")
    parser.add_argument(
        "jsonfiles",
        metavar="file",
        type=argparse.FileType("r"),
        nargs="*",
        help="json files to test if (in)valid",
    )

    parser.add_argument(
        "--invalid",
        action="store_true",
        default=False,
        help="expect the files to be invalid instead of valid",
    )

    args = parser.parse_args()

    ####################
    # Example validation
    ####################

    # Load schemata
    dictionary = gdcdictionary

    for f in args.jsonfiles:
        doc = json.load(f)
        if args.invalid:
            try:
                print(f"CHECK if {f.name} is valid:", end=" ")
                if isinstance(doc, dict):
                    validate_entity(doc, dictionary.schema)
                elif isinstance(doc, list):
                    for entity in doc:
                        validate_entity(entity, dictionary.schema)
                else:
                    raise ValidationError("Invalid json")
            except ValidationError as e:
                print("Invalid as expected.")
            else:
                raise Exception("Expected invalid, but validated.")
        else:
            print(f"CHECK if {f.name} is valid:", end=" ")
            if isinstance(doc, dict):
                validate_entity(doc, dictionary.schema)
            elif isinstance(doc, list):
                for entity in doc:
                    validate_entity(entity, dictionary.schema)
            else:
                print("Invalid json")

            print("Valid as expected")
    print("ok.")
