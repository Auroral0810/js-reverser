import cv2
import numpy as np


def calculate_distance(cx_slider, cy_slider, cx_slot, cy_slot):
    # 计算滑块到滑块槽的欧氏距离
    distance = np.sqrt((cx_slider - cx_slot) ** 2 + (cy_slider - cy_slot) ** 2)
    return distance


# 读取图片
image = cv2.imread('b6a696b60df734a80ecf2b1251ee57eb_bg.jpg')
# 将图片转换为灰度图像
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# 通过阈值处理获取二值图像
_, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
# 轮廓检测
contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# 创建一个用于可视化的图像副本
visualization = image.copy()

if len(contours) >= 2:
    # 找到最大的轮廓（滑块）
    max_contour = max(contours, key=cv2.contourArea)
    # 创建一个新的轮廓列表，不包含最大轮廓
    contours = [contour for contour in contours if contour is not max_contour]

    min_distance = float('inf')  # 初始化最小距离为无穷大
    best_slot = None
    best_cx_slider, best_cy_slider = 0, 0
    best_cx_slot, best_cy_slot = 0, 0

    # 计算滑块的质心
    M1 = cv2.moments(max_contour)
    cx_slider = int(M1['m10'] / M1['m00'])
    cy_slider = int(M1['m01'] / M1['m00'])
    
    # 在图像上绘制滑块轮廓和质心
    cv2.drawContours(visualization, [max_contour], -1, (0, 255, 0), 2)
    cv2.circle(visualization, (cx_slider, cy_slider), 5, (0, 255, 0), -1)
    cv2.putText(visualization, "Slider", (cx_slider - 30, cy_slider - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 遍历所有可能的槽
    for slot_contour in contours:
        # 计算滑块槽的质心
        M2 = cv2.moments(slot_contour)
        if M2['m00'] != 0:
            cx_slot = int(M2['m10'] / M2['m00'])
            cy_slot = int(M2['m01'] / M2['m00'])

            # 计算滑块到滑块槽的欧氏距离
            distance = calculate_distance(cx_slider, cy_slider, cx_slot, cy_slot)

            # 更新最小距离和最匹配的槽
            if distance < min_distance:
                min_distance = distance
                best_slot = slot_contour
                best_cx_slider, best_cy_slider = cx_slider, cy_slider
                best_cx_slot, best_cy_slot = cx_slot, cy_slot
        else:
            print("找不到滑块槽")

    if best_slot is not None:
        # 在图像上绘制最佳匹配的滑块槽轮廓和质心
        cv2.drawContours(visualization, [best_slot], -1, (0, 0, 255), 2)
        cv2.circle(visualization, (best_cx_slot, best_cy_slot), 5, (0, 0, 255), -1)
        cv2.putText(visualization, "Slot", (best_cx_slot - 30, best_cy_slot - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        
        # 绘制从滑块到滑块槽的连线
        cv2.line(visualization, (best_cx_slider, best_cy_slider), 
                 (best_cx_slot, best_cy_slot), (255, 0, 0), 2)
        
        # 在连线中间显示距离
        mid_x = (best_cx_slider + best_cx_slot) // 2
        mid_y = (best_cy_slider + best_cy_slot) // 2
        cv2.putText(visualization, f"Distance: {min_distance:.2f}", (mid_x, mid_y), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
        
        print("最匹配的滑块槽距离:", min_distance)
        print(f"滑块位置: ({best_cx_slider}, {best_cy_slider})")
        print(f"滑块槽位置: ({best_cx_slot}, {best_cy_slot})")
        print(f"水平距离: {abs(best_cx_slot - best_cx_slider)}")
    else:
        print("找不到最匹配的滑块槽")
else:
    print("找不到足够的轮廓")

# 显示可视化结果
cv2.imshow("Visualization", visualization)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 保存可视化结果
cv2.imwrite("visualization_result.png", visualization)