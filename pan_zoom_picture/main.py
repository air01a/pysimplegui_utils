
import PySimpleGUI as sg
from gui_image_pan_zoom import ImageZoomPan



def main():
    # Crée une fenêtre avec une toile (Canvas) pour afficher l'image
    layout = [
        [sg.Canvas(background_color='black', key='-CANVAS-')],
    ]
    window = sg.Window('Image Viewer', layout, size=(400, 300),resizable=True, finalize=True)
    window.bind('<Configure>', "Configure")
    canvas_elem = window['-CANVAS-']
    canvas = canvas_elem.Widget
    canvas.config(width=window.Size[0], height=window.Size[1])
    image_manager = ImageZoomPan('m57_2023-09-19.png', canvas,(window.Size[0], window.Size[1]))

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
        elif event == 'Configure':
            canvas.config(width=window.Size[0], height=window.Size[1])
            image_manager.resize(window.Size[0],window.Size[1])
    window.close()


   

if __name__ == "__main__":
    main()
