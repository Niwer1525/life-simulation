import tkinter as tk
import random
from PIL import Image, ImageTk

# Creating the window
app = tk.Tk()
app.title("Life simulator")
app.geometry("1200x600")
app.resizable(False, False)
app.configure(bg="#313338")

simulation_running = False
canvas = None
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 500

#
def create_rectangle(x1, y1, x2, y2, **kwargs):
    global canvas
    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = app.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (x2-x1, y2-y1), fill)
        images.append(ImageTk.PhotoImage(image))
        canvas.create_image(x1, y1, image=images[-1], anchor='nw')
    canvas.create_rectangle(x1, y1, x2, y2, **kwargs)

# The food class
class BLueObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(1, 3)
        self.type = "food"

    def draw(self):
        global canvas
        x1, y1 = self.x - 10 * self.size, self.y - 10 * self.size
        x2, y2 = self.x + 10 * self.size, self.y + 10 * self.size
        canvas.create_oval(x1, y1, x2, y2, fill="#0b6387", outline="#0b6387")

# The bad food class
class RedObject:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(1, 2)
        self.type = "damage"

    def draw(self):
        global canvas
        x1, y1 = self.x - 10 * self.size, self.y - 10 * self.size
        x2, y2 = self.x + 10 * self.size, self.y + 10 * self.size
        canvas.create_oval(x1, y1, x2, y2, fill="#7e2520", outline="#7e2520")

# This allow to randomize the color for children
def blend_colors(color1, color2):
    r1, g1, b1 = tk.Color(color1).rgb
    r2, g2, b2 = tk.Color(color2).rgb
    blended_r = (r1 + r2) // 2
    blended_g = (g1 + g2) // 2
    blended_b = (b1 + b2) // 2
    return f'#{blended_r:02x}{blended_g:02x}{blended_b:02x}'


# A class that represnets an animal
class Animal:
    def __init__(self, x, y, color):
        self.prevx = x
        self.prevy = y
        self.x = x
        self.y = y
        self.vx = random.randint(-1, 1)
        self.vy = random.randint(-1, 1)
        self.health = 100
        self.hunger = 0
        self.age = 0
        # hereditary caracteristics
        self.color = color;
        self.size = 1;

    def move(self):
        # Prevent borders touching
        if self.x < 20: self.vx = random.randint(0, 1) # Move to the right
        elif self.x > CANVAS_WIDTH - 20: self.vx = random.randint(-1, 0) # Move to the left
        if self.y < 20: self.vy = random.randint(0, 1) # Move down
        elif self.y > CANVAS_HEIGHT - 20: self.vy = random.randint(-1, 0) # Move up

        # Move the entity
        self.x += self.vx * 5
        self.y += self.vy * 5

    def eat(self, food):
        self.hunger -= food
        if self.hunger < 0: self.hunger = 0

    def damage(self, damage):
        self.health -= damage
        if self.health < 0: self.health = 0

    def draw(self):
        global canvas
        x1, y1 = self.x - 10, self.y - 10
        x2, y2 = self.x + 10, self.y + 10
        canvas.create_rectangle(x1, y1, x2, y2, fill=self.color, outline=self.color)

    def drawSelected(self):
        global canvas
        x1, y1 = self.x - 10 * self.size, self.y - 10 * self.size
        x2, y2 = self.x + 10 * self.size, self.y + 10 * self.size
        create_rectangle(x1, y1, x2, y2, fill="#f0b132", alpha=.5)

result_label = tk.Label(app, bg="#313338", fg="white", text="Press the button to start the simulation")
result_label.pack()
info_label = tk.Label(app, bg="#313338", fg="white", text="Entity info :")
info_label.pack(side=tk.RIGHT, padx=40, anchor="e")
start_button = tk.Button(app, text="Start simulating")
start_button.pack()

# Saving entities
entities = []
blue_objects = []
red_objects = []
selectedEntity = None

# Canvas click event
def on_canvas_click(event):
    global selectedEntity
    x, y = event.x, event.y
    for entity in entities:
        if abs(entity.x - x) < 10 and abs(entity.y - y) < 10:
            selectedEntity = entity;
            break
        else: selectedEntity = None

# Checking if two objects are colliding
def collision(obj1, obj2):
    obj1_x1, obj1_y1, obj1_x2, obj1_y2 = obj1.x - 10 * obj1.size, obj1.y - 10 * obj1.size, obj1.x + 10 * obj1.size, obj1.y + 10 * obj1.size
    obj2_x1, obj2_y1, obj2_x2, obj2_y2 = obj2.x - 10 * obj2.size, obj2.y - 10 * obj2.size, obj2.x + 10 * obj2.size, obj2.y + 10 * obj2.size
    if obj1_x1 < obj2_x2 and obj1_x2 > obj2_x1 and obj1_y1 < obj2_y2 and obj1_y2 > obj2_y1: return True
    else: return False

def update_simulation():
    if simulation_running:
        global selectedEntity

        # Reset canvas
        canvas.delete("all")

        # Drawing the pills
        for b_obj in blue_objects: b_obj.draw()
        for r_obj in red_objects: r_obj.draw()

        # Simulating the entities
        for entity in entities:
            entity.move() # Move the entity
            entity.draw() # Draw the entity
            entity.hunger += 1 # Increase the hunger
            entity.age += 1 # Increase the age

            # If the entity is dead, remove it
            if entity.health <= 0 or entity.age >= 200 or entity.hunger > 100: 
                entities.remove(entity)
                if selectedEntity == entity: selectedEntity = None # If the entity is selected, unselect it

            # Reproduction
            for entity_reporduction in entities:
                if entity != entity_reporduction and collision(entity, entity_reporduction) and entity.hunger < 10 and entity_reporduction.hunger < 10 and random.randint(0, 100) < 5:
                    entities.append(Animal(entity.x + 5, entity.y + 5, blend_colors(entity.color, entity_reporduction.color))) # Reproduce

            # Eating
            for b_obj in blue_objects:
                if collision(entity, b_obj):
                    entity.eat(b_obj.size) # Eat the food
                    blue_objects.remove(b_obj)

            # Damage
            for r_obj in red_objects:
                if collision(entity, r_obj):
                    entity.damage(r_obj.size) # Damage the entity
                    red_objects.remove(r_obj)

        # User interface
        result_label.config(text="Simulation started (Bad food:"+str(len(red_objects))+", Food:"+str(len(blue_objects))+", Entities :" + str(len(entities)) + ", GEN :"+ str(0) +")")
        app.after(100, update_simulation) # Repeat after 100 ms
    
        if selectedEntity is not None:
            info_text = f"Entity Info:\nAge: {selectedEntity.age}\nHealth: {selectedEntity.health}\nHunger: {selectedEntity.hunger}"
            info_label.config(text=info_text)
            selectedEntity.drawSelected()

def start_simulation():
    # Checking if the simulation is already running
    global simulation_running
    global canvas
    
    if simulation_running: return
    simulation_running = True
    
    # Creating the canvas
    canvas = tk.Canvas(app, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg="#1e1f22", bd=0)
    canvas.pack()
    canvas.bind("<Button-1>", on_canvas_click)

    #Add randomly food objects
    for _ in range(30): blue_objects.append(BLueObject(random.randint(0, CANVAS_WIDTH), random.randint(0, CANVAS_HEIGHT)))

    # Add randomly bad food objects
    for _ in range(30): red_objects.append(RedObject(random.randint(0, CANVAS_WIDTH), random.randint(0, CANVAS_HEIGHT)))

    # Adding entities to the list
    available_colors = ["white", "magenta", "green"]
    for _ in range(5):
        entities.append(Animal(x=(CANVAS_WIDTH/2) * random.random(), y=(CANVAS_HEIGHT/2) * random.random(), color=random.choice(available_colors)))

    # Updating the simulation
    update_simulation()

start_button.config(command=start_simulation)
app.mainloop()
