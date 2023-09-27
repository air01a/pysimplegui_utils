from PIL import Image, ImageTk

class ZoomConstraint:

    def __init__(self, image, widget_width, widget_height):
        w, h = image.size
        self.image_ratio = h/w
        self.zoom_max = 3
        if (w>h):
            self.zoom_min = widget_width/w
        else:
            self.zoom_min = widget_height/h

        self.zoom_factor = self.zoom_min

        self.image_size = (w,h)
        self.canvas_width=widget_width
        self.canvas_height=widget_height

    def increase_zoom_factor(self):
        self.zoom_factor *= 1.1
        if self.zoom_factor>self.zoom_max:
            self.zoom_factor = self.zoom_max

    def decrease_zoom_factor(self):
        self.zoom_factor *=0.9
        if self.zoom_factor < self.zoom_min:
            self.zoom_factor = self.zoom_min


class ImageZoomPan:

    def __init__(self,image_path, canvas, size):
        image = Image.open(image_path)
        self.canvas = canvas
        self.image = image
        self.offset_x = 0
        self.offset_y = 0
        self.width  = size[0]
        self.height = size[1]
        self.zoom_manager = ZoomConstraint(image, size[0],size[1])
        self.resize_image()
        self.draw_image()

        # Bond mouse wheel event
        canvas.bind('<MouseWheel>', lambda event: self.event_zoom_image(event))
        #Bind click event
        canvas.bind("<ButtonPress-1>", lambda event: self.start_panning(event))
        canvas.bind("<B1-Motion>", lambda event: self.move_image(event))

    # Call only when canvas size has changed
    def resize(self, width, height):
        current_zoom = self.zoom_manager.zoom_factor
        self.zoom_manager = ZoomConstraint(self.image, width, height)
        self.zoom_manager.zoom_factor = current_zoom

        self.width  = width
        self.height = height
        self.draw_image()

    # Start drag
    def start_panning(self, event):
        self.pan_start_x = event.x
        self.pan_start_y = event.y

    # Manage Pan
    def move_image(self, event=None):
        # Calculate delta with reference point
        delta_x = event.x - self.pan_start_x
        delta_y = event.y - self.pan_start_y

        self.offset_x -= delta_x
        self.offset_y -= delta_y

        # reset reference point
        self.pan_start_x = event.x
        self.pan_start_y = event.y

        self.draw_image()


    # resize image according to zoom
    def resize_image(self):
        width, height = self.image.size
        new_width = int(width * self.zoom_manager.zoom_factor)
        new_height = int(height * self.zoom_manager.zoom_factor)

        self.resized_image = self.image.resize((new_width, new_height))


    # a bit of math
    def _calculate_boundaries(self, w,h):
        left = self.offset_x
        top = self.offset_y
        right = left + self.width
        bottom = top + self.height

        return (left, top, right, bottom)


    # Calculate boundaries according to zoom and pan
    def _get_boundaries(self):
        (w,h)=self.resized_image.size
        (left, top, right, bottom) = self._calculate_boundaries(w,h)
        # check if corners are out of image
        if left<0:
            self.offset_x=0   
        if top<0:
            self.offset_y=0

        if self.width>w:
            self.offset_x = -(self.width -w)/2
        elif right>w:
            self.offset_x = w - self.width

        if self.height>h:
            self.offset_y = -(self.height-h)/2
        elif bottom>h:
            self.offset_y = h-self.height

        if (left<0 or top<0 or right>w or bottom>h):
            return self._calculate_boundaries(w,h)
        
        return (left, top, right, bottom)


    # Dram image on canvas
    def draw_image(self):
        # Get corner of image according to pan and zoom
        (left, top, right, bottom) = self._get_boundaries()
        # Resize image
        displayed_image = self.resized_image.crop((left, top, right, bottom))


        # Display Image
        new_photo = ImageTk.PhotoImage(displayed_image)
        self.canvas.create_image(0, 0, anchor='nw', image=new_photo)
        self.canvas.photo = new_photo



    # Manage Zoom
    def event_zoom_image(self, event):


        old_zoom = self.zoom_manager.zoom_factor
        if event.delta > 0:
            self.zoom_manager.increase_zoom_factor()
        else:
            self.zoom_manager.decrease_zoom_factor() 

        self.resize_image()
        self.offset_x = self.offset_x + (self.zoom_manager.zoom_factor-old_zoom)*self.width/2
        self.offset_y = self.offset_y + (self.zoom_manager.zoom_factor-old_zoom)*self.width/2
        self.draw_image()

