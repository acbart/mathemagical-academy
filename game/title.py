import spyral

SIZE = WIDTH, HEIGHT = 1200, 900

# class Ball(spyral.Sprite):
    # def __init__(self, scene):
        # super(Ball, self).__init__()        

class Title(spyral.Scene):
    def __init__(self, *args, **kwargs):
        super(Title, self).__init__(*args, **kwargs)
        
        self.camera = self.parent_camera.make_child(virtual_size = (WIDTH, HEIGHT))
        
        # We have to give our camera to the group so it knows where to draw
        self.group = spyral.Group(self.camera)
        # We can add the sprites to the group
        #self.group.add(self.left_paddle, self.right_paddle, self.ball)
        
        
    def on_enter(self):
        background = spyral.Image(filename="images/title.png")
        self.camera.set_background(background)
        
        # name_entry = spyral.TextInputWidget(500, 'is so awesome', default_value=False)
        # name_entry.pos = (30,30)
        # email_entry = spyral.TextInputWidget(200, 'acbart', default_value=True, max_length = 10)
        # email_entry.pos = (30, 100)
        
        minigames_btn = spyral.ButtonWidget("Minigames")
        minigames_btn.pos = (100, 100)
        
        self.manager = spyral.event.EventManager()
        form = spyral.form.Form('Forms', 
                                self.manager)
        #form.add_widget("name_entry",
        #                name_entry)
        #form.add_widget("email_entry",
        #                email_entry)
        
        form.add_widget("minigames_btn", minigames_btn)
        
        form.focus()
        self.group.add(form)
        self.manager.register_listener(form, ['KEYDOWN', 'KEYUP', 'MOUSEMOTION','MOUSEBUTTONUP', 'MOUSEBUTTONDOWN'])
        
    def render(self):
        # Simply tell the group to draw
        self.group.draw()
        
    def update(self, dt):
        """
        The update loop receives dt as a parameter, which is the amount
        of time which has passed since the last time update was called.
        """
        self.group.update(dt)
        events= self.event_handler.get()
        self.manager.send_events(events)
        
        # Gets all the events from the event handler
        for event in events:
            # You should always be sure you're handling the quit events
            if event['type'] == 'QUIT':
                spyral.director.pop()  # Happens when someone asks the OS to close the program
                return
            if event['type'] == 'KEYDOWN':
                # On keydown, we store the direction the paddle should be moving
                # We reset this on keyup, so that holding down the buttons works
                if event['key'] == spyral.keys.escape:
                    spyral.director.pop()
                if event['ascii'] == 'w':
                    pass
                    #self.left_paddle.moving = 'up'
                if event['key'] == spyral.keys.down:
                    pass
            elif event['type'] == 'KEYUP':
                if event['ascii'] in ('w', 's'):
                    pass
        