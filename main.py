# v(t+Δt) ≈ v(t) + a(t) ⋅ Δt
import os
import tkinter as tk
from tkinter import simpledialog, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib import font_manager
from matplotlib.animation import PillowWriter

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def simulate_spring_mass(m, k, x0, v0, t_max, dt):
    steps = int(t_max / dt)
    if steps < 1:
        raise ValueError("Insufficient simulation steps. Please ensure t_max and dt are reasonable.")
    x = x0
    v = v0
    t = 0.0

    t_list = [t]     # Add initial point
    x_list = [x0]
    v_list = [v0]

    steps = int(t_max / dt)
    for _ in range(steps):
        a = -k/m * x
        v = v + a * dt
        x = x + v * dt
        t = t + dt

        t_list.append(t)
        x_list.append(x)
        v_list.append(v)

    return np.array(t_list), np.array(x_list), np.array(v_list)

def plot_position_time(t, x):
    plt.figure(figsize=(8,4))
    plt.plot(t, x, label='Position x(t)')
    plt.xlabel('Time t (s)')
    plt.ylabel('Position x (m)')
    plt.title('Spring-Mass System: Position vs. Time')
    plt.legend()
    plt.grid(True)
    plt.show()


def animate_motion(t, x, save_as_gif=True, filename="spring_mass.gif"):
    x = np.asarray(x).flatten()
    t = np.asarray(t).flatten()

    if len(t) == 0 or len(x) == 0:
        print("❌ Animation data is empty: please check simulation parameters")
        return

    fig, ax = plt.subplots(figsize=(6, 2))

    x_min = min(x)
    x_max = max(x)
    if x_min == x_max:
        x_min -= 0.1
        x_max += 0.1

    ax.set_xlim(x_min * 1.2, x_max * 1.2)
    ax.set_ylim(-1, 1)
    ax.set_yticks([])
    ax.set_title("Spring-Mass Motion Animation")

    mass, = ax.plot([], [], 'ro', markersize=20)

    def init():
        mass.set_data([], [])
        return mass,

    def update(frame):
        if frame >= len(x):
            print(f"⚠️ Skipping out-of-range frame: {frame} >= {len(x)}")
            return mass,
        mass.set_data([x[frame]], [0])
        return mass,

    frames = list(range(len(x)))
    ani = FuncAnimation(
        fig, update,
        frames=frames,
        init_func=init,
        blit=True,
        interval=20,
        repeat=False
    )

    if save_as_gif:
        filename = "spring_mass.gif"
        abs_path = os.path.join(os.getcwd(), filename)
        print(f"💾 Saving GIF to: {abs_path}")
        ani.save(abs_path, writer=PillowWriter(fps=30))
        print("✅ Save completed")
    else:
        plt.show()

def get_float_input(prompt, default):
    root = tk.Tk()
    root.withdraw()  # Hide main window
    while True:
        try:
            result = simpledialog.askstring("Input Parameter", prompt + f" (default {default})")
            if result is None or result.strip() == "":
                return default
            value = float(result)
            return value
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number!")


if __name__ == "__main__":
    m = get_float_input("Enter mass m (kg)", 1.0)
    k = get_float_input("Enter spring constant k (N/m)", 10.0)
    x0 = get_float_input("Enter initial position x0 (m)", 1.0)
    v0 = get_float_input("Enter initial velocity v0 (m/s)", 0.0)
    t_max = get_float_input("Enter total simulation time t_max (s)", 10.0)
    dt = get_float_input("Enter time step dt (s)", 0.01)

    t, x, v = simulate_spring_mass(m, k, x0, v0, t_max, dt)
    plot_position_time(t, x)
    print("Count:", len(t), "x count:", len(x), "x[0:5]:", x[:5])
    animate_motion(t, x, save_as_gif=True)
