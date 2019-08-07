# Purpose
Normalizes pkg_resources and the newer, better importlib.resources.

importlib.resources.path and pkg_resources.resource_filename are normalized to
`get_pkg_resource_path`. Both APIs safely return a Path object.

legacy pkg_resources are mapped to their importlib equivalents.

    resource_filename = resource_path
    resource_stream = open_binary
    resource_string = read_text
