import cv2

def draw_canvas(img, cnt, input_arr):
    if len(input_arr[0])  == 2:
        prev_locations, _ = tuple(input_arr[0][:2])
        for i in range(1, cnt):
            curr_locations, _ = tuple(input_arr[i][:2])
            try:
                cv2.line(img, prev_locations, curr_locations, (255, 255, 255), 3)
                prev_locations = curr_locations
            except:
                break
    else:
        prev_index = tuple(input_arr[0][:2])
        prev_pinky = tuple(input_arr[0][2:])
        for i in range(1, cnt):
            curr_index = tuple(input_arr[i][:2])
            curr_pinky = tuple(input_arr[i][2:])
            try:
                cv2.line(img, prev_index, curr_index, (255, 255, 255), 3)
                cv2.line(img, prev_pinky, curr_pinky, (255, 255, 255), 3)
                prev_index = curr_index
                prev_pinky = curr_pinky
            except:
                break
    return img