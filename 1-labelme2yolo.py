import os
import json
import shutil
from tqdm import tqdm


def convert_labelme_to_yolo(json_path, output_dir, image_dir):
    """
    将 LabelMe 的 JSON 文件转换为 YOLOv8 实例分割格式。
    :param json_path: JSON 文件路径
    :param output_dir: 输出的标签文件夹路径
    :param image_dir: 图片输出文件夹路径
    """
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 获取图片信息
    image_name = data['imagePath']
    image_height = data['imageHeight']
    image_width = data['imageWidth']

    # 复制图片到目标文件夹
    src_image_path = os.path.join(os.path.dirname(json_path), image_name)
    dst_image_path = os.path.join(image_dir, os.path.splitext(image_name)[0].split("\\")[-1] + os.path.splitext(image_name)[1])
    shutil.copy(src_image_path, dst_image_path)

    # 创建 YOLO 格式标注内容
    yolo_annotations = []
    for shape in data['shapes']:
        label = shape['label']
        points = shape['points']
        class_id = class_name_to_id[label]  # 映射类别名称到类别 ID

        # 计算目标的包围框 (x_min, y_min, x_max, y_max)
        x_min = min(p[0] for p in points)
        y_min = min(p[1] for p in points)
        x_max = max(p[0] for p in points)
        y_max = max(p[1] for p in points)

        # 转换为归一化的 YOLO 格式
        x_center = (x_min + x_max) / 2 / image_width
        y_center = (y_min + y_max) / 2 / image_height
        width = (x_max - x_min) / image_width
        height = (y_max - y_min) / image_height

        # 转换多边形坐标为归一化格式
        normalized_points = []
        for x, y in points:
            normalized_x = x / image_width
            normalized_y = y / image_height
            normalized_points.extend([normalized_x, normalized_y])

        # 组合成 YOLOv8 实例分割格式
        annotation = f"{class_id} {x_center} {y_center} {width} {height} " + " ".join(map(str, normalized_points))
        yolo_annotations.append(annotation)

    # 保存为 YOLO 格式的标签文件
    label_file = os.path.join(output_dir, os.path.splitext(image_name)[0].split("\\")[-1] + '.txt')
    with open(label_file, 'w') as f:
        f.write("\n".join(yolo_annotations))


def process_dataset(labelme_dir, output_base_dir, train=True):
    """
    将训练集或验证集转换为 YOLOv8 实例分割格式。
    :param labelme_dir: LabelMe 数据集路径
    :param output_base_dir: YOLO 数据集输出路径
    :param train: 是否为训练集
    """
    split = 'train' if train else 'val'
    images_dir = os.path.join(output_base_dir, split, 'images')
    labels_dir = os.path.join(output_base_dir, split, 'labels')

    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)

    json_files = [f for f in os.listdir(labelme_dir) if f.endswith('.json')]
    for json_file in tqdm(json_files, desc=f"Processing {split} dataset"):
        json_path = os.path.join(labelme_dir, json_file)
        convert_labelme_to_yolo(json_path, labels_dir, images_dir)


if __name__ == "__main__":
    # 映射类别名称到类别 ID
    class_name_to_id = {
        "stairs": 0,
    }

    # 输入路径（LabelMe 数据集）
    train_labelme_dir = "json\\train"  # 训练集 JSON 文件夹
    test_labelme_dir = "json\\val"    # 测试集 JSON 文件夹

    # 输出路径（YOLO 数据集）
    output_dir = "json\\yolo_dataset"

    # 处理训练集和测试集
    process_dataset(train_labelme_dir, output_dir, train=True)
    process_dataset(test_labelme_dir, output_dir, train=False)