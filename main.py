import math
import random
import sys
from typing import List, Tuple, Optional
import pygame

# --- Настройки окна и отображения ---
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 750
PANEL_WIDTH = 300
CANVAS_WIDTH = WINDOW_WIDTH - PANEL_WIDTH
FPS = 60

# --- Цветовая палитра (RGB / RGBA) ---
COLOR_BG = (22, 24, 30)
COLOR_PANEL_BG = (32, 36, 45)
COLOR_CITY = (255, 105, 97)
COLOR_CITY_OUTLINE = (255, 255, 255)
COLOR_BEST_PATH = (80, 220, 100)
COLOR_PHEROMONE = (100, 180, 255)
COLOR_TEXT = (230, 235, 245)
COLOR_TEXT_MUTED = (150, 160, 175)
COLOR_ACCENT = (255, 190, 80)

# --- Гиперпараметры алгоритма муравьиной колонии (ACO) ---
DEFAULT_NUM_CITIES = 25
NUM_ANTS = 35
ALPHA = 1.0          # Вес феромона (влияние стадного чувства)
BETA = 3.5           # Вес эвристики (жадность к близким городам)
EVAPORATION = 0.4    # Коэффициент испарения феромона (rho)
Q = 100.0            # Константа количества откладываемого феромона
ELITIST_WEIGHT = 2.0 # Коэффициент усиления лучшего глобального маршрута
INITIAL_PHEROMONE = 0.1
MIN_PHEROMONE = 0.001

def generate_cities(num_cities: int, margin: int = 45) -> List[Tuple[int, int]]:
    """
    Генерирует список случайных координат городов (x, y) в пределах рабочей области.
    """
    cities = []
    for _ in range(num_cities):
        x = random.randint(margin, CANVAS_WIDTH - margin)
        y = random.randint(margin, WINDOW_HEIGHT - margin)
        cities.append((x, y))
    return cities

