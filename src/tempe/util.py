def contains(rect_1, rect_2):
    return (
        rect_1[0] >= rect_2[0]
        and rect_1[0] + rect_1[2] <= rect_2[0] + rect_2[2]
        and rect_1[1] >= rect_2[1]
        and rect_1[1] + rect_1[3] <= rect_2[1] + rect_2[3]
    )
