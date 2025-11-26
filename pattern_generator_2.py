def generate_design(n):
    H = n if n % 2 != 0 else n + 1
    
    BASE_STRING = "FORMULAQSOLUTIONS"
    BASE_LEN = len(BASE_STRING)
    
    S = [BASE_STRING[i % BASE_LEN] for i in range(H)]

    UNIFIED_DATA = [3, 9, 15, 4, 10, 12, 5, 16, 6, 4, 6, 11, 2, 0]
    DATA_LEN = len(UNIFIED_DATA)
    
    M = (H - 1) // 2 
    
    gap_line_counter = 0
    bottom_gap_counter = 0
    
    result = []

    for i in range(H):

        k = min(i, H - 1 - i)
        
        if k % 2 == 0:
            start_base_index = i % BASE_LEN
            end_base_index = (start_base_index + 2 * k) % BASE_LEN
            
            C_left = BASE_STRING[start_base_index]
            C_right = BASE_STRING[end_base_index]
            
        else:
            C_left = S[i]
            
            if i <= M:
                seq_index = gap_line_counter
            else:
                L = H // 2
                start_offset = 30 - (5 * L) // 2
                seq_index = start_offset + bottom_gap_counter
                
                bottom_gap_counter += 1

            R_index_base = UNIFIED_DATA[seq_index % DATA_LEN]
            
            gap_line_counter += 1
            
            C_right = BASE_STRING[R_index_base % BASE_LEN]
 
        if k == 0:
            line = C_left
        else:
            fill_char = "-" if i == M else " "
            mid_char = "|"
            gap = fill_char * (k - 1)
            
            line = f"{C_left}{gap}{mid_char}{gap}{C_right}"
            
        result.append(line)
        
    return result