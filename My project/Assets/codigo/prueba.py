import math

def create_wheel(radius, circle_radius, wheel_width):
    vertices = []
    normals = []
    faces = []

    circle_vertices = create_circle(circle_radius, radius)
    circle_normals = create_circle_normals(circle_radius, radius)

    # Top
    top_face = []
    for i in range(0, len(circle_vertices), 2):
        top_face.append(circle_vertices[i] + (wheel_width / 2))
    top_face = list(reversed(top_face))
    top_face.append(circle_vertices[0] + (wheel_width / 2))

    faces.append(top_face)

    # Bottom
    bottom_face = []
    for i in range(0, len(circle_vertices), 2):
        bottom_face.append(circle_vertices[i] - (wheel_width / 2))
    bottom_face.append(circle_vertices[0] - (wheel_width / 2))

    faces.append(bottom_face)

    # Sides
    for i in range(0, len(circle_vertices), 2):
        faces.append([circle_vertices[i] + (wheel_width / 2),
                      circle_vertices[i + 1] + (wheel_width / 2),
                      circle_vertices[i + 1] - (wheel_width / 2),
                      circle_vertices[i] - (wheel_width / 2)])

    # Vertices and Normals
    vertices.extend(circle_vertices)
    vertices.extend([circle_vertices[i] + (wheel_width / 2) for i in range(0, len(circle_vertices), 2)])
    vertices.extend([circle_vertices[i] - (wheel_width / 2) for i in range(0, len(circle_vertices), 2)])

    normals.extend(circle_normals)
    normals.extend([(0, 1, 0) for _ in range(0, len(circle_vertices), 2)])
    normals.extend([(0, -1, 0) for _ in range(0, len(circle_vertices), 2)])

    return vertices, normals, faces

def create_circle(radius, steps):
    vertices = []
    angle = 2 * math.pi / steps
    for i in range(steps):
        x = radius * math.cos(i * angle)
        y = radius * math.sin(i * angle)
        vertices.append((x, y, 0))
    return vertices

def create_circle_normals(radius, steps):
    normals = []
    angle = 2 * math.pi / steps
    for i in range(steps):
        x = math.cos(i * angle)
        y = math.sin(i * angle)
        normals.append((x, y, 0))
    return normals

def export_obj(vertices, faces, normals, output_file):
    with open(output_file, 'w') as file:
        # Escribir vértices
        for vertex in vertices:
            file.write(f"v {vertex[0]} {vertex[1]} {vertex[2]}\n")

        # Escribir normales
        for normal in normals:
            file.write(f"vn {normal[0]} {normal[1]} {normal[2]}\n")

        # Escribir caras
        for face in faces:
            file.write(f"f {face[0]}//{face[0]} {face[1]}//{face[1]} {face[2]}//{face[2]}\n")

if __name__ == "__main__":
    import sys
    radius = float(sys.argv[1])
    circle_radius = float(sys.argv[2])
    wheel_width = float(sys.argv[3])
    vertices, normals, faces = create_wheel(radius, circle_radius, wheel_width)
    export_obj(vertices, faces, normals, 'wheel2.obj')

