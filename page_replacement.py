import pandas as pd


MAX_FRAMES = 3  # Số khung trang tối đa
MAX_PAGES = 10  # Số trang tối đa
INF = float('inf')  # Vô cùng

def record(frames, current_page, fault = None, ):
    rec = {f'frame {index}' : frame for index, frame in enumerate(frames)}
    rec['fault'] = fault
    rec['page'] = current_page
    return rec


def fifo(pages):
    frames = [0] * MAX_FRAMES  # Khung trang
    frame_index = 0  # Chỉ số khung trang hiện tại
    data = []


    for page in pages:
        found = page in frames

        # Nếu trang không tồn tại trong khung trang
        if not found:
            frames[frame_index] = page  # Thay thế trang trong khung trang
            frame_index = (frame_index + 1) % MAX_FRAMES  # Chuyển đến khung trang tiếp theo
            data.append(record(frames, page, '*'))
        else:
            data.append(record(frames, page))

    df = pd.DataFrame(data)
    total_page_faults = df[['fault']].count().values[0]
    df.loc[len(pages)] = [None] * (MAX_FRAMES - 3) +['total', 'page', 'faults', total_page_faults, 'page']
    return df.T.to_markdown()

def opt(pages:list):
    frames = [0] * MAX_FRAMES  # Khung trang
    data = []
    for index, page in enumerate(pages):
        found = page in frames

        if not found:
            future_pages = pages[index+1:]
            page_removed = max(frames, key= lambda frame: future_pages.index(frame) if frame in future_pages else INF)
            frames.remove(page_removed)
            frames.append(page)
            data.append(record(frames, page, '*'))
        else:
            data.append(record(frames, page))
    
    df = pd.DataFrame(data)
    total_page_faults = df[['fault']].count().values[0]
    df.loc[len(pages)] = [None] * (MAX_FRAMES - 3) +['total', 'page', 'faults', total_page_faults, 'page']
    return df.T.to_markdown()
            


def lru(pages):
    frames = [0] * MAX_FRAMES
    counter = [0] * MAX_FRAMES 
    data = []
    for page in pages:
        found = page in frames

        if not found:
            min_counter = min(range(MAX_FRAMES), key= lambda index: counter[index])

            frames[min_counter] = page
            counter[min_counter] = 0
            data.append(record(frames, page, '*'))
        else:
            data.append(record(frames, page))

        counter += [1] * MAX_FRAMES

    df = pd.DataFrame(data)
    total_page_faults = df[['fault']].count().values[0]
    df.loc[len(pages)] = [None] * (MAX_FRAMES - 3) +['total', 'page', 'faults', total_page_faults, 'page']
    return df.T.to_markdown()


def main():
    pages = [1, 9, 5, 2, 1, 2, 0, 4, 0, 0, 7]  # default
    # pages = [1, 2, 3, 1, 2, 3, 4, 2, 3, 4, 2, 3]

    print('============================ FIFO ============================\n',fifo(pages),'\n\n')
    print('============================ OPT ============================\n',opt(pages),'\n\n')
    print('============================ LRU ============================\n',lru(pages))

if __name__ == "__main__":
    main()