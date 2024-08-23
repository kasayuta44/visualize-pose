import os
import json
import cv2

def load_skeleton_data(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    return data

def draw_skeleton(image, keypoints, color=(0, 255, 0), thickness=2):
    points = [(int(keypoints[i]), int(keypoints[i + 1])) for i in range(0, len(keypoints), 3)]
    
    for point in points:
        cv2.circle(image, point, 5, color, -1)

    # Drawing lines between points (example: head to shoulders, shoulders to elbows, etc.)
    # Adjust the pairs according to your skeleton structure
    pairs = [
        (0, 1), (1, 2), (2, 3), (2, 4),       # Head connections
        (3, 5), (4, 6),                       # Ear to eye connections
        (7, 8), (7, 9), (9, 11), (8, 10), (10, 12), # Upper body connections
        (13, 14), (13, 15), (15, 17), (14, 16), (16, 18)  # Lower body connections
    ]
    for pair in pairs:
        pt1 = points[pair[0]]
        pt2 = points[pair[1]]
        cv2.line(image, pt1, pt2, color, thickness)

    return image

def process_images(image_folder, skeleton_data, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for image_info in skeleton_data['images']:
        image_path = os.path.join(image_folder, image_info['file_name'])
        if os.path.exists(image_path):
            image = cv2.imread(image_path)
            
            annotation = next((ann for ann in skeleton_data['annotations'] if ann['image_id'] == image_info['id']), None)
            if annotation:
                keypoints = annotation['keypoints']
                image_with_skeleton = draw_skeleton(image, keypoints)
                
                output_path = os.path.join(output_folder, os.path.basename(image_info['file_name']))
                cv2.imwrite(output_path, image_with_skeleton)
                print(f'Processed and saved: {output_path}')
            else:
                print(f'No skeleton data for image: {image_info["file_name"]}')
        else:
            print(f'Image not found: {image_info["file_name"]}')

# Example usage
json_file = './annotations/out.json'
image_folder = './images/'
output_folder = './output/'

skeleton_data = load_skeleton_data(json_file)
process_images(image_folder, skeleton_data, output_folder)
