import math
from decimal import Decimal
from .models import Point


class Location:

    def __init__(self, center_lat, center_lon, radius):
        self.center_lat = center_lat
        self.center_lon = center_lon
        self.radius = radius

    def get_points(self):
        '''Возвращает точки в пределах радиуса.
        Сначала считается ограничивающий прямоугольник.
        Затем отбираются все точки в его пределах и впоследствии идет подробной расчет растояния и сравнения с радиусом
        '''
        min_lat, max_lat, min_lon, max_lon = self.get_bounding_box(self.center_lat, self.center_lon, self.radius)
        points_bounding_box = Location.get_points_bounding_box(min_lat, max_lat, min_lon, max_lon)
        points_in_radius = Location.points_in_radius(points_bounding_box, self.center_lat, self.center_lon, self.radius)
        points = filter(lambda x: x[0][0], zip(points_in_radius, points_bounding_box))
        return points

    @staticmethod
    def calculate_distance(lat1, lon1, lat2, lon2):
        '''Нахождение расстояния между двумя точками'''
        R = 6371

        lat1_rad = math.radians(float(lat1))
        lon1_rad = math.radians(float(lon1))
        lat2_rad = math.radians(float(lat2))
        lon2_rad = math.radians(float(lon2))

        delta_lat_rad = lat2_rad - lat1_rad
        delta_lon_rad = lon2_rad - lon1_rad

        cos_lat = math.cos(lat1_rad) * math.cos(lat2_rad)
        sin_lat = math.sin(delta_lat_rad / 2)
        sin_lon = math.sin(delta_lon_rad / 2)

        a = sin_lat ** 2 + cos_lat * sin_lon ** 2
        distance = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return distance * R

    @staticmethod
    def is_point_in_radius(lat1, lon1, lat2, lon2, radius):
        '''Возвращает находится ли точка в радиусе и дистанцию'''
        distance = Location.calculate_distance(lat1, lon1, lat2, lon2)
        return distance <= radius, distance

    @staticmethod
    def get_bounding_box(latitude, longitude, radius) -> tuple:
        '''Возвращение ограничивающего прямоугольника для предварительной фильотрации'''
        KM_PER_DEGREE_LAT = 111.0

        delta_lat = float(radius) / KM_PER_DEGREE_LAT

        rad_lat = math.radians(latitude)
        delta_lon = float(radius) / (KM_PER_DEGREE_LAT * math.cos(rad_lat))

        max_lat = float(latitude) + delta_lat
        min_lat = float(latitude) - delta_lat
        max_lon = float(longitude) + delta_lon
        min_lon = float(longitude) - delta_lon
        return min_lat, max_lat, min_lon, max_lon

    @staticmethod
    def points_in_radius(points, center_lat, center_lon, radius):
        '''Вовращает генератор являются ли точки в пределах радиуса'''
        for point in points:
            lat2, lon2 = point.coordinates
            flag, distance = Location.is_point_in_radius(center_lat, center_lon, lat2, lon2, radius)
            yield flag, distance

    @staticmethod
    def get_points_bounding_box(min_lat, max_lat, min_lon, max_lon):
        '''Филтрация точек по ограничивающему прямоугольнику'''
        points = Point.objects.filter(
            latitude__gte=Decimal(str(min_lat)),
            latitude__lte=Decimal(str(max_lat)),
            longitude__gte=Decimal(str(min_lon)),
            longitude__lte=Decimal(str(max_lon))
        ).select_related('user')
        return points
