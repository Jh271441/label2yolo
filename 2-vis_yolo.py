import os
import cv2
import numpy as np


def visualize_yolo_segmentation(image_dir, label_dir, output_dir, class_names):
    """
    可视化 YOLOv8 实例分割数据集。
    :param image_dir: 图片文件夹路径
    :param label_dir: YOLO 格式标签文件夹路径
    :param output_dir: 可视化结果输出文件夹路径
    :param class_names: 类别名称列表（按 class_id 索引）
    """
    os.makedirs(output_dir, exist_ok=True)

    # 遍历图片文件夹中的所有图片
    for image_file in os.listdir(image_dir):
        if not (image_file.endswith(".jpg") or image_file.endswith(".png")):
            continue

        # 加载图片
        image_path = os.path.join(image_dir, image_file)
        image = cv2.imread(image_path)
        if image is None:
            print(f"Failed to read image: {image_path}")
            continue
        height, width, _ = image.shape

        # 查找对应的标签文件
        label_file = os.path.splitext(image_file)[0] + ".txt"
        label_path = os.path.join(label_dir, label_file)
        if not os.path.exists(label_path):
            print(f"No label file found for image: {image_file}")
            continue

        # 解析标签文件
        with open(label_path, "r") as f:
            lines = f.readlines()

        for line in lines:
            parts = line.strip().split()
            class_id = int(parts[0])  # 类别 ID
            center_x, center_y, bbox_width, bbox_height = map(float, parts[1:5])
            polygon = list(map(float, parts[5:]))

            # 解归一化到像素坐标
            center_x *= width
            center_y *= height
            bbox_width *= width
            bbox_height *= height
            x_min = int(center_x - bbox_width / 2)
            y_min = int(center_y - bbox_height / 2)
            x_max = int(center_x + bbox_width / 2)
            y_max = int(center_y + bbox_height / 2)

            # 绘制包围框
            color = (0, 255, 0)  # 绿色
            cv2.rectangle(image, (x_min, y_min), (x_max, y_max), color, 2)

            # 转换多边形坐标为像素坐标
            polygon_points = np.array(polygon).reshape(-1, 2)
            polygon_points[:, 0] *= width
            polygon_points[:, 1] *= height
            polygon_points = polygon_points.astype(np.int32)

            # 绘制分割区域
            color = (0, 0, 255)  # 红色
            cv2.polylines(image, [polygon_points], isClosed=True, color=color, thickness=2)
            cv2.fillPoly(image, [polygon_points], color=(0, 0, 255, 50))  # 填充透明红色

            # 显示类别名称
            label = class_names[class_id] if class_id < len(class_names) else f"Class {class_id}"
            cv2.putText(image, label, (x_min, y_min - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        # 保存结果到输出文件夹
        output_path = os.path.join(output_dir, image_file)
        cv2.imwrite(output_path, image)
        print(f"Saved visualization: {output_path}")


if __name__ == "__main__":
    split = 'val'
    # 配置路径
    image_dir = f"json/yolo_dataset/{split}/images"  # 修改为图片文件夹路径
    label_dir = f"json/yolo_dataset/{split}/labels"  # 修改为标签文件夹路径
    output_dir = f"json/yolo_dataset/{split}/vis"  # 修改为输出文件夹路径

    # 类别名称列表（按 class_id 顺序）
    class_names = ["stairs"]  # 根据你的数据集修改

    # 可视化
    visualize_yolo_segmentation(image_dir, label_dir, output_dir, class_names)