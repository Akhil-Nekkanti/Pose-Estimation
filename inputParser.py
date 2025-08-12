def parse_focal_length(filename):
    with open(filename, 'r') as file:
        focal_length = float(file.readline().strip())  # Read and convert to float
    return focal_length

def parse_joint_names(filename):
    joint_names = {}
    with open(filename, 'r') as file:
        for line in file:
            ident, name = line.strip().split()  # Split into two parts
            joint_names[int(ident)] = name      # Convert ID to int and store in dictionary
    return joint_names

def parse_poses(filename):
    poses = []
    with open(filename, 'r') as file:
        for line in file:
            values = list(map(float, line.strip().split()))  # Convert each value to float
            camera_position = values[:3]  # First 3 values are camera position
            joint_coordinates = values[3:]  # Remaining values are joint coordinates
            poses.append({
                'camera_position': camera_position,
                'joint_coordinates': joint_coordinates
            })
    return poses

if '__main__' == __name__:
    focal_length = parse_focal_length('focal.txt')
    joint_names = parse_joint_names('joint-names.txt')
    poses = parse_poses('poses.txt')
    
    #print to verify
    print(focal_length)
    print(joint_names)
    print(poses)