import cv2
import numpy as np
import ultralytics

model = ultralytics.YOLO('data/lesson_seg/brain-tumor-seg.pt')

img = cv2.imread('data/lesson_seg/tumor1.jpg')

results = model.predict(img, conf=0.5)
result = results[0]

res_img = result.plot(boxes=False, masks=True)

mask = result.masks.data[0]
mask = mask.cpu().numpy().astype(np.uint8)
mask_bool = mask.astype(bool)

area_pixels = np.sum(mask_bool)
print(f"Площа пухлини в пікселях: {area_pixels}")

area_cm2 = area_pixels * 0.0025
print(f"Площа пухлини в см²: {area_cm2:.2f}")

if area_cm2 < 10:
    tumor_type = 'small'
elif 10 <= area_cm2 <= 25:
    tumor_type = 'middle'
else:
    tumor_type = 'large'

print(f"Тип пухлини: {tumor_type}")

tumor_only = np.zeros_like(img)
tumor_only[mask_bool] = img[mask_bool]

cv2.imshow(f'T - {tumor_type}', tumor_only)
cv2.imshow('Segmentation', res_img)
cv2.waitKey(0)

