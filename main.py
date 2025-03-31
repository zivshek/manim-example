from manim import *

class CubeProjectionScene(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes()
        self.add(axes)

        self.move_camera(phi=75 * DEGREES, theta=-30 * DEGREES, run_time=1)

        cube = Cube(side_length=2, fill_opacity=0.5, stroke_width=1, color=BLUE)
        cube_label = Text("Game Object", font_size=20).next_to(cube, UP).rotate(PI/2, RIGHT)
        
        width, height = 7, 4
        plane = Rectangle(
            width=width, 
            height=height, 
            fill_opacity=0.5, 
            stroke_width=1, 
            color=WHITE
        ).move_to(axes.c2p(0, -3, 0))
        
        plane.rotate(PI/2, RIGHT)
        plane_label = Text("Screen", font_size=20).next_to(plane, LEFT).rotate(PI/2, RIGHT).move_to(plane.get_center() + OUT * 1.5 + LEFT * 2.5)
        
        self.play(Create(cube), Create(plane), Write(cube_label), Write(plane_label), subcaption_duration=0.2)
        
        cube_target_position = axes.c2p(0, 3, 0)
        self.play(
            cube.animate.move_to(cube_target_position),
            cube_label.animate.next_to(cube_target_position, UP),
            subcaption_duration=0.2
        )

        # Get the face of the cube facing toward the plane

        # facing_plane_vertices = [cube.get_corner(pos) for pos in [
        #     DOWN + LEFT + IN, DOWN + RIGHT + IN, UP + LEFT + IN, UP + RIGHT + IN
        # ]]
        # facing_plane_vertices = [cube.get_corner(pos) for pos in [
        #     DOWN + IN + LEFT, DOWN + OUT + LEFT, UP + LEFT + IN, UP + LEFT + OUT
        # ]]

        # to be honest, I am not sure which axis is which, but this one works, I tried...
        facing_plane_vertices = [cube.get_corner(pos) for pos in [
            DOWN + IN + LEFT, DOWN + OUT + LEFT, DOWN + RIGHT + IN, DOWN + RIGHT + OUT
        ]]
        
        # Create dots at each vertex for visualization
        vertex_dots = [Dot(point=v, color=RED, radius=0.05) for v in facing_plane_vertices]
        self.play(Create(VGroup(*vertex_dots)), subcaption_duration=0.1)
        
        # Create projection lines and projected points - orthogonal projection along z-axis
        projection_lines = []
        projected_points = []
        
        # For each vertex, create vertical projection line to the plane
        for vertex in facing_plane_vertices:
            # For orthogonal projection along y-axis, we keep x and z coordinates 
            # and replace the y coordinate with the plane's y position
            x, y, z = vertex[0], vertex[1], vertex[2]
            plane_y = plane.get_center()[1]
            
            # Calculate intersection point (preserving x and z, replacing y)
            intersection = np.array([x, plane_y, z])
            
            # Create vertical line from vertex to intersection (parallel to y-axis)
            line = DashedLine(vertex, intersection, color=YELLOW)
            projection_lines.append(line)
            
            # Create dot at intersection point
            projected_dot = Dot(point=intersection, color=GREEN, radius=0.08)
            projected_points.append(projected_dot)
        
        # Show projection lines
        self.play(Create(VGroup(*projection_lines)), subcaption_duration=0.1)
        
        # Show projected points
        self.play(Create(VGroup(*projected_points)), subcaption_duration=0.1)
        
        # Connect projected points to form the projected square
        # The order is important to form a square
        square_edges = [(0, 1), (1, 3), (3, 2), (2, 0)]
        projected_edges = []
        
        for i, j in square_edges:
            projected_edge = Line(projected_points[i].get_center(), 
                                 projected_points[j].get_center(), 
                                 color=BLUE_E, 
                                 stroke_width=3)
            projected_edges.append(projected_edge)
        
        self.play(Create(VGroup(*projected_edges)), subcaption_duration=0.2)

        # Move the camera to directly face the plane
        self.move_camera(phi=90 * DEGREES, theta=-90 * DEGREES, run_time=1)
        self.wait(1)
        
        # Add a view from an angle to better see the projection effect
        self.move_camera(phi=60 * DEGREES, theta=-60 * DEGREES, run_time=1)
        self.wait(1)

if __name__ == "__main__":
    with tempconfig({
        "quality": "medium_quality", 
        "preview": True,
        "pixel_width": 1920,
        "pixel_height": 1080,
        "frame_rate": 30,
    }):
        scene = CubeProjectionScene()
        scene.render()
