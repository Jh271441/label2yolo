import os
import json

# train_json_path = "json\\train"
#
# train_json_files = os.listdir(train_json_path)
#
# for train_json_file in train_json_files:
#     if train_json_file.endswith(".json") and int(train_json_file[:-5]) > 1176:
#         print(train_json_file)
#         with open(os.path.join(train_json_path, train_json_file)) as f:
#             file = json.load(f)
#             # shapes = file["shapes"]
#             image_name = file["imagePath"]
#             modified_name = "..\\" + image_name.replace("/", "\\")
#             file["imagePath"] = modified_name
#             with open(os.path.join(train_json_path, train_json_file), "w") as f:
#                 json.dump(file, f, indent=4)
# print()


train_json_path = "json\\val"

train_json_files = os.listdir(train_json_path)

for train_json_file in train_json_files:
    if train_json_file.endswith(".json"): #and int(train_json_file[:-5]) > 1176:
        print(train_json_file)
        with open(os.path.join(train_json_path, train_json_file)) as f:
            file = json.load(f)
            # shapes = file["shapes"]
            image_name = file["imagePath"]
            modified_name = "..\\" + image_name
            file["imagePath"] = modified_name
            with open(os.path.join(train_json_path, train_json_file), "w") as f:
                json.dump(file, f, indent=4)
print()