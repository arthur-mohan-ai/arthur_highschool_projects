#image_recognition
import torch
from torchvision import models, transforms
from PIL import Image
import requests
from io import BytesIO

# ResNet
model = models.resnet101(pretrained=True)
model.eval()

# resize  to tensor  normalize
preprocess = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def process_image(image_url):
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))
    image = preprocess(image)
    image = image.unsqueeze(0)
    return image

def predict(image_url):
    image = process_image(image_url)
    with torch.no_grad():
        outputs = model(image)
    _, predicted = outputs.max(1)
    return predicted.item()

with open("imagenet_classes.txt") as f:
    labels = [line.strip() for line in f.readlines()]

image_url = "https://bkimg.cdn.bcebos.com/pic/0df3d7ca7bcb0a464ccc3b5e6b63f6246a60afef"
predicted_class = predict(image_url)
print(f"Predicted class: {labels[predicted_class]}")
# import torch
# from torchvision import models, transforms
# from PIL import Image
# import requests
# from io import BytesIO

# # ResNet
# model = models.resnet101(pretrained=True)
# model.eval()

# # 
# preprocess = transforms.Compose([
#     transforms.Resize(256),
#     transforms.CenterCrop(224),
#     transforms.ToTensor(),
#     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
# ])

# # 
# def process_image(image_url):
#     response = requests.get(image_url)
#     image = Image.open(BytesIO(response.content))
#     image = preprocess(image)
#     image = image.unsqueeze(0)
#     return image

# # 
# def check_prediction(predicted_class):
#     # 
#     target_classes = ['traffic light', 'fire hydrant', 'sidewalk']
#     if predicted_class in target_classes:
#         return predicted_class
#     return 'none'

# # 
# def predict(image_url):
#     image = process_image(image_url)
#     with torch.no_grad():
#         outputs = model(image)
#     _, predicted = outputs.max(1)
#     return labels[predicted.item()]

# with open("imagenet_classes.txt") as f:
#     labels = [line.strip() for line in f.readlines()]

# image_urls = [
#     "https://img1.baidu.com/it/u=3932803710,3502666738&fm=253&fmt=auto&app=138&f=JPEG?w=671&h=500",
#     "https://img1.baidu.com/it/u=3300998240,1620386723&fm=253&fmt=auto&app=138&f=JPEG?w=741&h=500",
#     "https://bkimg.cdn.bcebos.com/pic/0df3d7ca7bcb0a464ccc3b5e6b63f6246a60afef",
#     "https://img0.baidu.com/it/u=3414788238,2918669433&fm=253&fmt=auto&app=138&f=JPEG?w=667&h=500",
#     # 更多 URL...
# ]

# for url in image_urls:
#     predicted_class = predict(url)
#     print(f"Image URL: {url}")
#     print(f"Predicted class: {check_prediction(predicted_class)}\n")

# # #这是一个识别给定图像是否是消防栓，人行道，或者红绿灯的代码