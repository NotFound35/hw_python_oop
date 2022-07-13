from dataclasses import dataclass, asdict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE = ('Тип тренировки: {}; '
               'Длительность: {:.3f} ч.; '
               'Дистанция: {:.3f} км; '
               'Ср. скорость: {:.3f} км/ч; '
               'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        t = asdict(self)
        return self.MESSAGE.format(*t.values())


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    M_IN_HR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        len_speed = self.get_distance() / self.duration
        return len_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определить get_spent_calories в %s.' %
                                  (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    Coeff_run_1 = 18
    Coeff_run_2 = 20

    def get_spent_calories(self) -> float:
        spent_cal = ((self.Coeff_run_1 * self.get_mean_speed()
                     - self.Coeff_run_2)
                     * self.weight / self.M_IN_KM * self.duration
                     * self.M_IN_HR)
        return spent_cal


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    Coeff_sw_1: float = 0.035
    Coeff_sw_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        spent_cal_1 = ((self.Coeff_sw_1 * self.weight
                       + (self.get_mean_speed()
                        ** 2 // self.height)
                       * self.Coeff_sw_2 * self.weight) * self.duration
                       * self.M_IN_HR)
        return spent_cal_1


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    Coeff_swim_1: float = 1.1
    Coeff_swim_2: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        sw_mean_speed = (self.length_pool
                         * self.count_pool
                         / self.M_IN_KM
                         / self.duration
                         )
        return sw_mean_speed

    def get_spent_calories(self) -> float:
        sw_spent_cal = ((self.get_mean_speed()
                        + self.Coeff_swim_1)
                        * self.Coeff_swim_2
                        * self.weight)
        return sw_spent_cal


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_params = {'SWM': Swimming,
                       'RUN': Running,
                       'WLK': SportsWalking
                       }
    if workout_type in training_params:
        return training_params[workout_type](*data)
    else:
        raise ValueError("Тренировка не найдена")


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
