from typing import List

from app.utils.s3 import get_s3_object


def generate_file_objects(file_paths: List[str]):
    new_file_paths = []
    for path in file_paths:
        new_file_paths.extend(path.split(","))

    file_objects = []
    for path in new_file_paths:
        parts = path.split("/", 1)
        if len(parts) == 2:
            type_ = parts[0][:-1]
            file_path = path
        else:
            type_, file_path = "unknown", path
        file_objects.append({"type": type_, "file_path": file_path})

    return file_objects


async def generate_file_data(file_objects):
    file_data = []

    for object in file_objects:
        data = await get_s3_object(object["file_path"])
        file_data.append({"type": object["type"], "data": data})

    return file_data
