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
        line_length = 2 * k + 1
        
        if k % 2 == 0:
            line_parts = []
            start_base_index = i % BASE_LEN

            for j in range(line_length):
                base_index = (start_base_index + j) % BASE_LEN
                line_parts.append(BASE_STRING[base_index])
            
            line = "".join(line_parts)
            
        else:
            C_left = S[i]
            gap_count = line_length - 2
            
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
            line = C_left + ("-" * gap_count) + C_right
            
        result.append(line)
        
    return result