from vtk import (
    vtkXMLImageDataReader,
    vtkFixedPointVolumeRayCastMapper,
    vtkColorTransferFunction,
    vtkPiecewiseFunction,
    vtkVolumeProperty,
    vtkVolume,
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)


class VtkPipeline:
    def __init__(self, input_image):
        self.load_file(input_image)
        self.get_histogram_data()

        color_function = vtkColorTransferFunction()
        opacity_function = vtkPiecewiseFunction()

        volume_property = vtkVolumeProperty()
        volume_property.SetColor(color_function)
        volume_property.SetScalarOpacity(opacity_function)

        actor = vtkVolume()
        actor.SetProperty(volume_property)
        actor.SetMapper(self.mapper)
        renderer = vtkRenderer()
        render_window = vtkRenderWindow()
        render_window.AddRenderer(renderer)
        render_interactor = vtkRenderWindowInteractor()
        render_interactor.SetRenderWindow(render_window)
        render_interactor.GetInteractorStyle().SetCurrentStyleToTrackballCamera()
        renderer.AddVolume(actor)
        renderer.ResetCamera()

        self.color_function = color_function
        self.opacity_function = opacity_function
        self.render_window = render_window

    def load_file(self, input_image):
        reader = vtkXMLImageDataReader()
        reader.SetFileName(input_image)
        reader.Update()
        mapper = vtkFixedPointVolumeRayCastMapper()
        mapper.SetInputConnection(reader.GetOutputPort())
        self.mapper = mapper

    def get_histogram_data(self):
        # Send as n buckets
        # scalar_data_source = reader.GetOutput().GetPointData().GetScalars()
        # scalar_data = [
        #     scalar_data_source.GetValue(i) for i in range(scalar_data_source.GetSize())
        # ]
        # print(len(scalar_data), "scalar data computed")
        # state.scalars = [6, 7, 8, 9, 0]
        pass

    def update_colors(self, colormap_points):
        self.color_function.RemoveAllPoints()
        for point in colormap_points:
            self.color_function.AddRGBPoint(*point)

    def update_opacity(self, opacity_points):
        self.opacity_function.RemoveAllPoints()
        for point in opacity_points:
            self.opacity_function.AddPoint(*point)
