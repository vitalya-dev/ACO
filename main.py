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

def compute_distance_matrix(cities: List[Tuple[int, int]]) -> List[List[float]]:
    """
    Вычисляет симметричную матрицу евклидовых расстояний между всеми парами городов.
    """
    n = len(cities)
    matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            dx = cities[i][0] - cities[j][0]
            dy = cities[i][1] - cities[j][1]
            dist = math.hypot(dx, dy)
            # Защита от деления на ноль при совпадении координат
            dist = max(dist, 1e-4)
            matrix[i][j] = dist
            matrix[j][i] = dist
    return matrix

def create_pheromone_matrix(num_cities: int, initial_value: float = INITIAL_PHEROMONE) -> List[List[float]]:
    """
    Создаёт начальную матрицу феромонов, заполненную базовым значением.
    """
    return [[initial_value for _ in range(num_cities)] for _ in range(num_cities)]


def select_next_city(
    current_city: int,
    unvisited: List[int],
    pheromones: List[List[float]],
    distances: List[List[float]],
    alpha: float = ALPHA,
    beta: float = BETA
) -> int:
    """
    Выбирает следующий город для муравья методом рулетки на основе
    концентрации феромона (tau^alpha) и близости города (eta^beta).
    """
    weights = []
    for city in unvisited:
        tau = pheromones[current_city][city] ** alpha
        eta = (1.0 / distances[current_city][city]) ** beta
        weights.append(tau * eta)

    total_weight = sum(weights)
    if total_weight <= 0.0:
        return random.choice(unvisited)

    # Выбор методом рулетки (пропорционально весам)
    return random.choices(unvisited, weights=weights, k=1)[0]


def calculate_tour_length(tour: List[int], distances: List[List[float]]) -> float:
    """
    Вычисляет полную длину замкнутого маршрута коммивояжёра (включая возврат в старт).
    """
    total_dist = 0.0
    n = len(tour)
    for i in range(n):
        u = tour[i]
        v = tour[(i + 1) % n]
        total_dist += distances[u][v]
    return total_dist


def construct_ant_tour(
    num_cities: int,
    pheromones: List[List[float]],
    distances: List[List[float]],
    alpha: float = ALPHA,
    beta: float = BETA
) -> Tuple[List[int], float]:
    """
    Моделирует проход одного муравья по всем городам графа.
    Возвращает список индексов посещённых городов и итоговую длину тура.
    """
    start_city = random.randrange(num_cities)
    tour = [start_city]
    unvisited = [c for c in range(num_cities) if c != start_city]

    current_city = start_city
    while unvisited:
        next_city = select_next_city(
            current_city, unvisited, pheromones, distances, alpha, beta
        )
        tour.append(next_city)
        unvisited.remove(next_city)
        current_city = next_city

    tour_length = calculate_tour_length(tour, distances)
    return tour, tour_length