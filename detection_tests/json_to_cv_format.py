import json

if __name__ == '__main__':
    json_file = json.load(open('json_data.json'))
    print(json_file)
    output_file = open('train_data.txt', 'w+')
    for line in json_file:
        pos = line['face_position']
        # face_position x_start - 2, y_start - 0, x_end - 3, y_end - 1
        # 2 0 3 1
        if not pos[2] == pos[3] and not pos[0] == pos[1]:
            line = f'{line["file_name"]} 1 {pos[2]} {pos[0]} {pos[3]-pos[2]} {pos[1]-pos[0]}\n'
            output_file.write(line)
