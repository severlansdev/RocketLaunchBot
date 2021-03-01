def bisect(left_index, right_index):
    """
    Runs a bisection and returns the new frame

    """
    #Calculate the number of frames
    n = right_index - left_index
    new_frame = 0

    # Sanity check: n frames cannot be a negative number, error in indexes
    if n < 0:
        raise ValueError("Indexes are not correct. Left index higher than right index")
    elif n == 0:
        return new_frame
    else:    
        # while left_index + 1 < right_index:
        new_frame = int((left_index + right_index) / 2)

    return left_index, right_index, new_frame