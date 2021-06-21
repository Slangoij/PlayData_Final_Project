import cv2

def draw_canvas(img, cnt, draw_arr):
    # 검지
    prev_index = tuple(draw_arr[0][:2])
    # 약지
    if len(draw_arr[0]) > 2:
        prev_pinky = tuple(draw_arr[0][2:])
    else:
        prev_pinky = []

    for i in range(1, cnt):
        # 검지
        curr_index = tuple(draw_arr[i][:2])
        cv2.line(img, prev_index, curr_index, (255, 255, 255), 7)
        prev_index = curr_index
        # 약지
        if len(draw_arr[i]) > 2:
            curr_pinky = tuple(draw_arr[i][2:])
            if prev_pinky:
                cv2.line(img, prev_pinky, curr_pinky, (255, 255, 255), 7)
        else:
            curr_pinky = prev_pinky
        prev_pinky = curr_pinky

    return img
    
# if len(draw_arr[0]) == 2:
#     prev_locations = tuple(draw_arr[0][:2])
#     for i in range(1, cnt):
#         curr_locations = tuple(draw_arr[i][:2])
#         try:
#             cv2.line(img, prev_locations, curr_locations, (255, 255, 255), 7)
#             prev_locations = curr_locations
#         except:
#             pass
# else:
#     prev_index = tuple(draw_arr[0][:2])
#     prev_pinky = tuple(draw_arr[0][2:])
#     for i in range(1, cnt):
#         curr_index = tuple(draw_arr[i][:2])
#         curr_pinky = tuple(draw_arr[i][2:])
#         try:
#             cv2.line(img, prev_index, curr_index, (255, 255, 255), 7)
#             cv2.line(img, prev_pinky, curr_pinky, (255, 255, 255), 7)
#             prev_index = curr_index
#             prev_pinky = curr_pinky
#         except:
#             pass