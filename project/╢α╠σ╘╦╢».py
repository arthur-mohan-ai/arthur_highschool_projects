import tkinter as tk
from tkinter import simpledialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def compute_gravitational_force(p1, p2):
    r_vec = p2['pos'] - p1['pos']
    r_mag = np.linalg.norm(r_vec)
    return G * p1['mass'] * p2['mass'] / r_mag**2 * r_vec / r_mag

def update_positions(planets, dt):
    for i, planet in enumerate(planets):
        total_force = np.array([0.0, 0.0])
        for j, other_planet in enumerate(planets):
            if i != j:
                
                total_force += compute_gravitational_force(planet, other_planet)
        planet['vel'] += total_force / planet['mass'] * dt
        planet['pos'] += planet['vel'] * dt

root = tk.Tk()
root.withdraw()
num_planets = simpledialog.askinteger("Input", "Enter the number of planets", parent=root, minvalue=1)
planet_infos = [{'pos': [0, 0], 'mass': 0} for _ in range(num_planets)]

for i in range(num_planets):
    planet_infos[i]['pos'][0] = simpledialog.askfloat("Input", f"Enter x coordinate of planet {i+1} (in AU)", parent=root)
    planet_infos[i]['pos'][1] = simpledialog.askfloat("Input", f"Enter y coordinate of planet {i+1} (in AU)", parent=root)
    planet_infos[i]['mass'] = simpledialog.askfloat("Input", f"Enter mass of planet {i+1} (in Solar Masses)", parent=root)

planets = [{'pos': np.array(info['pos']), 'vel': np.array([0.0, 0.0]), 'mass': info['mass']} for info in planet_infos]
G = 4 * np.pi ** 2
fig, ax = plt.subplots()
plt.xlim(-10, 10)
plt.ylim(-10, 10)
points = [ax.plot([], [], 'o', markersize=np.sqrt(info['mass']) * 5)[0] for info in planet_infos]
texts = [ax.text(0, 0, f'Planet {i+1}') for i in range(num_planets)]

def update(frame):
    update_positions(planets, 1.0 / 365.25)
    for point, text, planet in zip(points, texts, planets):
        point.set_data(planet['pos'][0], planet['pos'][1])
        text.set_position((planet['pos'][0], planet['pos'][1]))
    return points + texts

ani = FuncAnimation(fig, update, frames=200, interval=50)
plt.show()
