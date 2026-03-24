import cv2
import numpy as np

img = cv2.imread("assets/test4.jpg")

# 최대 높이 설정
max_height = 720
h, w = img.shape[:2]
if h > max_height:
    scale = max_height / h
    new_w = int(w * scale)
    img = cv2.resize(img, (new_w, max_height), interpolation=cv2.INTER_AREA)

# 1. 색상 부드럽게
color = cv2.bilateralFilter(img, 9, 200, 200)

# 2. 색상 양자화
Z = color.reshape((-1, 3))
Z = np.float32(Z)

K = 8
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 20, 1.0)
_, label, center = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
center = np.uint8(center)
color = center[label.flatten()].reshape(color.shape)

# 3. grayscale
edge_src = cv2.cvtColor(color, cv2.COLOR_BGR2GRAY)
edge_src = cv2.GaussianBlur(edge_src, (3, 3), 0)

# 4. internal gradient 사용 (double edge 완화)
grad_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
eroded = cv2.erode(edge_src, grad_kernel)
grad = cv2.subtract(edge_src, eroded)   # internal gradient

# 5. baseline 이하 제거
# baseline보다 작은 gradient는 0으로 깎임
baseline = 15
baseline_img = np.full_like(grad, baseline)
grad_cut = cv2.subtract(grad, baseline_img)

# 6. 대비 강화
# baseline 제거 후 남은 강한 gradient만 키움
grad_norm = cv2.normalize(grad_cut, None, 0, 255, cv2.NORM_MINMAX)
grad_emph = cv2.convertScaleAbs(grad_norm, alpha=2.5, beta=0)

# 너무 거친 부분 완화
grad_emph = cv2.GaussianBlur(grad_emph, (3, 3), 0)

# 7. 선 마스크로 직접 사용
# 강한 gradient일수록 검은 선이 되도록 반전
line_img = 255 - grad_emph

# 필요시 약한 회색을 흰색으로 더 밀어버리기
# 너무 연한 선을 없애고 진한 선만 남기려면 threshold 사용
line_threshold = 220
line_img = np.where(line_img > line_threshold, 255, line_img).astype(np.uint8)

# 8. 선 두께/연결성 조절용 마스크 처리
# 선 영역만 따로 뽑아서 close
line_mask = 255 - line_img
kernel_close = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
line_mask = cv2.morphologyEx(line_mask, cv2.MORPH_CLOSE, kernel_close)

# 약간 두껍게
line_mask = cv2.dilate(line_mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3)), iterations=1)

# 다시 반전해서 최종 line image
line_img = 255 - line_mask

# 9. 컬러와 직접 합성
line_f = line_img.astype(np.float32) / 255.0
line_f = cv2.merge([line_f, line_f, line_f])

cartoon = (color.astype(np.float32) * line_f).clip(0, 255).astype(np.uint8)

cv2.imshow("Edge Source", edge_src)
cv2.imwrite("assets/edge_source.jpg", edge_src)
cv2.imshow("Internal Gradient", grad)
cv2.imwrite("assets/internal_gradient.jpg", grad)
cv2.imshow("Gradient Cut", grad_cut)
cv2.imwrite("assets/gradient_cut.jpg", grad_cut)
cv2.imshow("Gradient Emphasized", grad_emph)
cv2.imwrite("assets/gradient_emphasized.jpg", grad_emph)
cv2.imshow("Line Image", line_img)
cv2.imwrite("assets/line_image.jpg", line_img)
cv2.imshow("Cartoon", cartoon)
cv2.imwrite("assets/cartoon.jpg", cartoon)

cv2.waitKey(0)
cv2.destroyAllWindows()