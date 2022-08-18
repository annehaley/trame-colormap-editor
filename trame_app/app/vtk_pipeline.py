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
        reader = vtkXMLImageDataReader()
        reader.SetFileName(input_image)
        reader.Update()
        mapper = vtkFixedPointVolumeRayCastMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        # Send as n buckets
        # scalar_data_source = reader.GetOutput().GetPointData().GetScalars()
        # scalar_data = [
        #     scalar_data_source.GetValue(i) for i in range(scalar_data_source.GetSize())
        # ]
        # print(len(scalar_data), "scalar data computed")
        # state.scalars = [6, 7, 8, 9, 0]

        color_function = vtkColorTransferFunction()
        opacity_function = vtkPiecewiseFunction()

        volume_property = vtkVolumeProperty()
        volume_property.SetColor(color_function)
        volume_property.SetScalarOpacity(opacity_function)

        actor = vtkVolume()
        actor.SetProperty(volume_property)
        actor.SetMapper(mapper)
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
