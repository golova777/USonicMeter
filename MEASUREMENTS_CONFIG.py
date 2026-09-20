from logging import fatal

import flet as ft

from misc import m_8_3_function, IntervalType

NORMAL_INTERVAL_COLOR = "#54ff8d"
NOT_NORMAL_INTERVAL_COLOR = "#ededed"
BELOW_NORMAL_INTERVAL_COLOR = "#4da9ff"
ABOVE_NORMAL_INTERVAL_COLOR = "#ffb700"

ERROR_COLOR = "#ff303e"

MALE_GENDER = "Мужской"
FEMALE_GENDER = "Женский"
REALLY_BIG_NUMBER = 10 ** 10
REALLY_SMALL_NUMBER = 1 / REALLY_BIG_NUMBER

GRADE_INTERVAL_COLOR_1 = "#a8ff1c"
GRADE_INTERVAL_COLOR_2 = "#2bffce"
GRADE_INTERVAL_COLOR_3 = "#57c1ff"
GRADE_INTERVAL_COLOR_4 = "#b66eff"
GRADE_INTERVAL_COLOR_5 = "#ff5c7a"

general_fields = {
    "fields": {
        "PatientFirstLastName": {
            "field_id": "PatientFirstLastName",
            "title": "ФИО пациента",
            "non_numeric_field": True,
            "printable_title": "ФИО пациента",
            "type": ft.TextField,
            "control": {
                "label": "ФИО пациента",
                "hint_text": None,
                "width": 300,
                "text_size": 18,
                "update_on_change": False,

            }

        },

        "gender": {
            "field_id": "gender",
            "title": "Пол",
            "non_numeric_field": True,
            "printable_title": "Укажите пол",
            "type": ft.Dropdown,
            "control": {
                "options": [MALE_GENDER, FEMALE_GENDER],
                "label": "Укажите пол",
                "hint_text": "Укажите пол",
                "width": 150,
                "text_size": 18,
                "update_on_change": True,
            }

        },

        "birth_year": {
            "field_id": "birth_year",
            "title": "birth_year",
            "printable_title": "Год рождения",
            "type": ft.Dropdown,
            "control": {
                "options": [*range(2025, 1900, -1)],
                "label": "Год рождения",
                "hint_text": "Год рождения",
                "width": 150,
                "text_size": 16,
                "update_on_change": False,
            }

        },

    }
}

measurement_blocks = {
    "init_block_1": {
        "title": "init_block_1",
        "print_title": "Пациент",
        "group_num": 101,
        "group_id": "g_101",
        "visible_title": True,
        "disabled_title": True,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "h_cm",
                "measure_title": "Рост, см.",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],

            },
            {
                "measure_num": 2,
                "field_id": "w_kg",
                "measure_title": "Вес, кг",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
            },

            {
                "measure_num": 1,
                "field_id": "Mostl",
                "measure_title": "ППТ(Mosteller)м2",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: ((p1 * p2) / 3600) ** 0.5,
                "needed_params": ["h_cm", "w_kg"],

            },
            {
                "measure_num": 2,
                # "field_id": "patient_BMI",
                "field_id": "BMI",
                "measure_title": "ИМТ кг/м2",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda weight_kg, height_m: weight_kg / ((height_m / 100) ** 2),
                "needed_params": ["w_kg", "h_cm"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [0, 18.499],
                            "description": "Сниженный индекс массы тела (менее 18,5 кг/м2)",
                            "gender": None,
                            "color": "#78f6ff",
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [18.5, 24.899],
                            "description": "Нормальный вес (ИМТ: от 18,5 до 24,9 кг/м2)",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [24.9, 29.899],
                            "description": "Избыточный вес (ИМТ: от 24,9 до 29,9 кг/м2) ",
                            "gender": None,
                            "color": "#9f63ff",
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [29.9, REALLY_BIG_NUMBER],
                            "description": "Ожирение (ИМТ: более 30 кг/м2) ",
                            "gender": None,
                            "color": "#ff7236",
                            "type": IntervalType.GRADE2,
                        },
                    ]
                },
            },
        ]
    },

    "init_block_2": {
        "title": "init_block_2",
        "print_title": "init_block_2",
        "group_num": 102,
        "group_id": "g_102",
        "visible_title": False,
        "disabled_title": True,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "SAD",
                "measure_title": "САД,мм.рт.ст",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
            },
            {
                "measure_num": 2,
                "field_id": "DAD",
                "measure_title": "ДАД,мм.рт.ст",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
            },
            {
                "measure_num": 1,
                "field_id": "CHss",
                "measure_title": "ЧСС, в мин",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
            },
        ]
    },

    "init_block_3": {
        "title": "init_block_3",
        "print_title": "init_block_3",
        "group_num": 103,
        "group_id": "g_103",
        "visible_title": False,
        "disabled_title": True,
        "measurements": [

        ]
    },

    "init_block_4": {
        "title": "init_block_4",
        "print_title": "init_block_4",
        "group_num": 104,
        "group_id": "g_104",
        "visible_title": False,
        "disabled_title": True,
        "measurements": [

        ]
    },

    "aorta": {
        "title": "aorta",
        "print_title": "Аорта",
        "group_num": 1,
        "group_id": "g_1",
        "visible_title": True,
        "disabled_title": False,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "m_1_1",
                "measure_title": "Синусы , мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 27.999],
                            "description": "ошибка",
                            "gender": MALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [28.0, 40.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [40.001, REALLY_BIG_NUMBER],
                            "description": "Расширение корня аорты",
                            "gender": MALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 23.999],
                            "description": "ошибка",
                            "gender": FEMALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [24.0, 36.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [36.001, REALLY_BIG_NUMBER],
                            "description": "Расширение корня аорты",
                            "gender": FEMALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                    ]
                }
            },
            {
                "measure_num": 2,
                "field_id": "m_1_2",
                "measure_title": "иСин.,мм/м2",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: p1 / p2,
                "needed_params": ["m_1_1", "Mostl"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 12.999],
                            "description": "Сужение корня аорты",
                            "gender": MALE_GENDER,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },
                        {
                            "values_belongs": [13.0, 21.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [21.001, REALLY_BIG_NUMBER],
                            "description": "Расширение корня аорты",
                            "gender": MALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 13.999],
                            "description": "Сужение корня аорты",
                            "gender": FEMALE_GENDER,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },
                        {
                            "values_belongs": [14.0, 22.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [22.001, REALLY_BIG_NUMBER],
                            "description": "Расширение корня аорты",
                            "gender": FEMALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },
                    ]
                }
            },
            {
                "measure_num": 3,
                "field_id": "m_1_3",
                "measure_title": "Восх.прокс.,мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [

                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 21.999],
                            "description": "ошибка",
                            "gender": MALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [22.0, 38.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [38.001, REALLY_BIG_NUMBER],
                            "description": "Расширение восходящего отдела аорты",
                            "gender": MALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 18.999],
                            "description": "ошибка",
                            "gender": FEMALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [19.0, 35.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [35.001, REALLY_BIG_NUMBER],
                            "description": "Расширение восходящего отдела аорты",
                            "gender": FEMALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                    ]
                }
            },
            {
                "measure_num": 4,
                "field_id": "m_1_4",
                "measure_title": "иВосх,мм/м2",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: p1 / p2,
                "needed_params": ["m_1_3", "Mostl"],
                "value_intervals": {
                    "intervals": [

                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 10.999],
                            "description": "ошибка",
                            "gender": MALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [11.0, 19.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [19.001, REALLY_BIG_NUMBER],
                            "description": "Расширение восходящего отдела аорты",
                            "gender": MALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 9.999],
                            "description": "ошибка",
                            "gender": FEMALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [10.0, 22.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [22.001, REALLY_BIG_NUMBER],
                            "description": "Расширение восходящего отдела аорты",
                            "gender": FEMALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                    ]
                }
            },
            {
                "measure_num": 5,
                "field_id": "m_1_5",
                "measure_title": "Дуга, мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, REALLY_SMALL_NUMBER],
                            "description": "Ошибка",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [REALLY_SMALL_NUMBER, 21.999],
                            "description": "Сужение дуги аорты",
                            "gender": None,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [22.0, 36.0],
                            "description": "норма для всех",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [36.001, REALLY_BIG_NUMBER],
                            "description": "Расширение дуги аорты",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },
                    ]
                }
            },
        ]
    },

    "left_ventricle": {
        "title": "left_ventricle",
        "print_title": "Левый желудочек ",
        "group_num": 2,
        "group_id": "g_2",
        "visible_title": True,
        "disabled_title": False,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "m_2_1",
                "measure_title": "КДР,мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 19.999],
                            "description": "ошибка",
                            "gender": MALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [20.0, 41.999],
                            "description": "Уменьшение размера левого желудочка.",
                            "gender": MALE_GENDER,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [42.0, 58.4],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [58.401, REALLY_BIG_NUMBER],
                            "description": "Расширение левого желудочка.",
                            "gender": MALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 17.999],
                            "description": "ошибка",
                            "gender": FEMALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [18.0, 37.799],
                            "description": "Уменьшение размера левого желудочка.",
                            "gender": FEMALE_GENDER,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [37.8, 52.2],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [52.201, REALLY_BIG_NUMBER],
                            "description": "Расширение левого желудочка.",
                            "gender": FEMALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                    ]
                }
            },
            {
                "measure_num": 2,
                "field_id": "m_2_2",
                "measure_title": "КСР,мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [25.0, 39.8],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [21.6, 34.8],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                    ]
                }
            },
            {
                "measure_num": 3,
                "field_id": "m_2_3",
                "measure_title": "МЖП,мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [6.0, 10.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [6.0, 9.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                    ]
                }
            },
            {
                "measure_num": 4,
                "field_id": "m_2_4",
                "measure_title": "ЗС,мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [6.0, 10.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [6.0, 9.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                    ]
                }
            },
            {
                "measure_num": 5,
                "field_id": "m_2_5",
                "measure_title": "иКДР, мм/м2",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: p1 / p2,
                "needed_params": ["m_2_1", "Mostl"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [22.0, 31.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [24.0, 32.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                    ]
                }
            },
        ]
    },

    "UnknownBlock1": {
        "title": "UnknownBlock1",
        "print_title": "(B режим)",
        "group_num": 3,
        "group_id": "g_3",
        "visible_title": True,
        "disabled_title": False,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "m_3_1",
                "measure_title": "ММ, гр.",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p3, p4: (0.8 * (1.04 * ((p1 + p3 + p4) ** 3 - p1 ** 3) + 0.6)) / 1000,
                "needed_params": ["m_2_1", "m_2_3", "m_2_4", ],

            },
            {
                "measure_num": 2,
                "field_id": "m_3_2",
                "measure_title": "иММ, гр/м2",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: p1 / p2,
                "needed_params": ["m_3_1", "Mostl"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 49.999],
                            "description": "ошибка",
                            "gender": MALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [50.0, 103.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [103.001, REALLY_BIG_NUMBER],
                            "description": "Превышение",
                            "gender": MALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 43.999],
                            "description": "ошибка",
                            "gender": FEMALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [44.0, 88.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [88.001, REALLY_BIG_NUMBER],
                            "description": "Превышение",
                            "gender": FEMALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },
                    ]
                }

            },
            {
                "measure_num": 3,
                "field_id": "m_3_3",
                "measure_title": "ОТС,см",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: (p1 + p1) / p2,
                "needed_params": ["m_2_4", "m_2_1"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 0.2199],
                            "description": "ошибка",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [0.22, 0.42],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [0.42001, REALLY_BIG_NUMBER],
                            "description": "Утолщение",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },
                    ]
                }
            },
            {
                "measure_num": 4,
                "field_id": "m_3_4",
                "measure_title": "МЖП/ЗС",
                "editable": False,
                "calculable": True,
                "enabled": False,
                "visible": True,
                "formula": lambda p1, p2: p1 / p2,
                "needed_params": ["m_2_3", "m_2_4"],

            },
            {
                "measure_num": 5,
                "field_id": "m_3_5",
                "measure_title": "ФУ,%",
                "editable": False,
                "calculable": True,
                "enabled": False,
                "visible": True,
                "formula": lambda p1, p2: ((p1 - p2) / p1) * 100,
                "needed_params": ["m_2_1", "m_2_2"],

            },
        ]
    },

    "UnknownBlock2": {
        "title": "UnknownBlock2",
        "print_title": "",
        "group_num": 4,
        "group_id": "g_4",
        "visible_title": False,
        "disabled_title": False,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "m_4_1",
                "measure_title": "КДО,мл",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 19.999],
                            "description": "ошибка",
                            "gender": MALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [20.0, 61.999],
                            "description": "Уменьшение размера левого желудочка.",
                            "gender": MALE_GENDER,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [62.0, 150.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [150.001, REALLY_BIG_NUMBER],
                            "description": "Расширение левого желудочка.",
                            "gender": MALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 17.999],
                            "description": "ошибка",
                            "gender": FEMALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [18.0, 45.999],
                            "description": "Уменьшение размера левого желудочка.",
                            "gender": FEMALE_GENDER,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [46.0, 106.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [106.001, REALLY_BIG_NUMBER],
                            "description": "Расширение левого желудочка.",
                            "gender": FEMALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                    ]
                }

            },
            {
                "measure_num": 2,
                "field_id": "m_4_2",
                "measure_title": "КСО,мл",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [21.0, 61.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [14.0, 42.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                    ]
                }

            },
            {
                "measure_num": 3,
                "field_id": "m_4_3",
                "measure_title": "ФВ(Simpson),%",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: (p1 - p2) / p1 * 100,
                "needed_params": ["m_4_1", "m_4_2"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 9.999],
                            "description": "ошибка",
                            "gender": MALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [10.0, 51.999],
                            "description": "снижение фракции выброса ЛЖ",
                            "gender": MALE_GENDER,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [52.0, 72.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [72.001, REALLY_BIG_NUMBER],
                            "description": "ошибка",
                            "gender": MALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },

                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 9.999],
                            "description": "ошибка",
                            "gender": FEMALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [10.0, 53.999],
                            "description": "снижение фракции выброса ЛЖ",
                            "gender": FEMALE_GENDER,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [54.0, 74.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [74.001, REALLY_BIG_NUMBER],
                            "description": "ошибка",
                            "gender": FEMALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },

                    ]
                }
            },
            {
                "measure_num": 4,
                "field_id": "m_4_4",
                "measure_title": "иКДО,мл/м2",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: p1 / p2,
                "needed_params": ["m_4_1", "Mostl"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [34.0, 74.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [29.0, 61.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                    ]
                }

            },
            {
                "measure_num": 5,
                "field_id": "m_4_5",
                "measure_title": "иКСО,мл/м2",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: p1 / p2,
                "needed_params": ["m_4_2", "Mostl"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [11.0, 31.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [8.0, 24.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                    ]
                }

            },
        ]
    },

    "left_atrium": {
        "title": "left_atrium",
        "print_title": "Левое предсердие",
        "group_num": 5,
        "group_id": "g_5",
        "visible_title": True,
        "disabled_title": False,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "m_5_1",
                "measure_title": "Попер.разм., мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [30.0, 40.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [27.0, 38.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                    ]
                }

            },
            {
                "measure_num": 2,
                "field_id": "m_5_2",
                "measure_title": "иРЛП, мм/м2",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: p1 / p2,
                "needed_params": ["m_5_1", "Mostl"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 14.999],
                            "description": "Ошибка!",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR
                        },
                        {
                            "values_belongs": [15.0, 23.0],
                            "description": "норма для всех",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [23.001, REALLY_BIG_NUMBER],
                            "description": "Расширение левого предсердия.",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                    ]
                }

            },
            {
                "measure_num": 3,
                "field_id": "m_5_3",
                "measure_title": "Кор.ось,мм",
                "editable": True,
                "calculable": False,
                "enabled": False,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [0.0, 40.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [0.0, 38.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                    ]
                }
            },

            {
                "measure_num": 4,
                "field_id": "m_5_4",
                "measure_title": "Длин.ось,мм",
                "editable": True,
                "calculable": False,
                "enabled": False,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [0.0, 50.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [0.0, 50.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                    ]
                }
            },

            {
                "measure_num": 5,
                "field_id": "m_5_5",
                "measure_title": "Объем, мл",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [18.0, 58.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [22.0, 52.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                    ]
                }

            },
            {
                "measure_num": 6,
                "field_id": "m_5_6",
                "measure_title": "иОЛП, мл/м2",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: p1 / p2,
                "needed_params": ["m_5_5", "Mostl"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 15.999],
                            "description": "ошибка",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [16.0, 33.999],
                            "description": "Нормальный размер",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [35.0, 40.999],
                            "description": "Легкое увеличение",
                            "gender": None,
                            "color": "#00edc2",
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [42.0, 47.999],
                            "description": "Умеренное увеличение",
                            "gender": None,
                            "color": "#00c4de",
                            "type": IntervalType.GRADE2,
                        },
                        {
                            "values_belongs": [48.0, REALLY_BIG_NUMBER],
                            "description": "Значительное увеличение",
                            "gender": None,
                            "color": "#1281ff",
                            "type": IntervalType.GRADE3,
                        },
                    ]
                }

            },
        ]
    },

    "right_ventricle": {
        "title": "right_ventricle",
        "print_title": "Правый желудочек",
        "group_num": 6,
        "group_id": "g_6",
        "visible_title": True,
        "disabled_title": False,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "m_6_1",
                "measure_title": "Базал.диам, мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 24.999],
                            "description": "ошибка",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [25.0, 41.0],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [41.001, REALLY_BIG_NUMBER],
                            "description": "Расширение правого желудочка.",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },
                    ]
                }

            },
            {
                "measure_num": 2,
                "field_id": "m_6_2",
                "measure_title": "Сред.диам, мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 18.999],
                            "description": "ошибка",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [19.0, 35.0],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [35.001, REALLY_BIG_NUMBER],
                            "description": "Расширение правого желудочка.",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },
                    ]
                }

            },
            {
                "measure_num": 3,
                "field_id": "m_6_3",
                "measure_title": "КДПлощадь, см2",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 9.999],
                            "description": "ошибка",
                            "gender": MALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [10.0, 24.0],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [24.001, REALLY_BIG_NUMBER],
                            "description": "Расширение правого желудочка.",
                            "gender": MALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 7.999],
                            "description": "ошибка",
                            "gender": FEMALE_GENDER,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [8.0, 20.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [20.001, REALLY_BIG_NUMBER],
                            "description": "Расширение правого желудочка.",
                            "gender": FEMALE_GENDER,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                    ]
                }
            },
            {
                "measure_num": 7,
                "field_id": "m_6_7",
                "measure_title": "КСПлощадь, см2",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],

            },

            {
                "measure_num": 4,
                "field_id": "m_6_4",
                "measure_title": "иКДП ПЖ, см/м2",
                "editable": False,
                "calculable": True,
                "enabled": False,
                "visible": True,
                "formula": lambda p1, p2: p1 / p2,
                "needed_params": ["m_6_3", "Mostl"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [5.0, 12.6],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [4.5, 11.5],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                    ]
                }
            },

            {
                "measure_num": 6,
                "field_id": "m_6_6",
                "measure_title": "FAC, %",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: (p1 - p2) / p1 * 100,
                "needed_params": ["m_6_3", "m_6_7"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-1 * REALLY_BIG_NUMBER, 34.999],
                            "description": "снижено",
                            "gender": None,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [35.0, REALLY_BIG_NUMBER],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                    ]
                }

            },
        ]
    },

    "right_atrium": {
        "title": "right_atrium",
        "print_title": "Правое предсердие",
        "group_num": 7,
        "group_id": "g_7",
        "visible_title": True,
        "disabled_title": False,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "m_7_1",
                "measure_title": "Площ.ПП,см2",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 4.999],
                            "description": "ошибка",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [5.0, 17.999],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [18.0, 25.999],
                            "description": "Расширение правого предсердия.",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [26.0, REALLY_BIG_NUMBER],
                            "description": "Дилатация правого предсердия.",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.GRADE2,
                        },
                    ]
                }

            },
            {
                "measure_num": 2,
                "field_id": "m_6_5",
                "measure_title": "TAPSE, мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [REALLY_SMALL_NUMBER, 17.999],
                            "description": "снижен",
                            "gender": None,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [18.0, REALLY_BIG_NUMBER],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        }

                    ]
                }

            },
            {
                "measure_num": 3,
                "field_id": "m_7_3",
                "measure_title": "ОбъемПП,мл",
                "editable": True,
                "calculable": False,
                "enabled": False,
                "visible": True,
                "formula": None,
                "needed_params": [],

            },

            {
                "measure_num": 4,
                "field_id": "m_7_4",
                "measure_title": "иОПП, мл/м2",
                "editable": False,
                "calculable": True,
                "enabled": False,
                "visible": True,
                "formula": lambda p1, p2: p1 / p2,
                "needed_params": ["m_7_3", "Mostl"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [11.0, 39.6],
                            "description": "норма для мужчин",
                            "gender": MALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [9.0, 33.0],
                            "description": "норма для женщин",
                            "gender": FEMALE_GENDER,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                    ]
                }
            },
            {
                "measure_num": 5,
                "field_id": "m_7_2",
                "measure_title": "ВТПЖ над АК,мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [REALLY_SMALL_NUMBER, 24.999],
                            "description": "ниже нормы",
                            "gender": None,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [25.0, 29.999],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [30.0, 32.999],
                            "description": "незначительное расширение",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [33.0, 35.999],
                            "description": "умеренное расширение",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.GRADE2,
                        },
                        {
                            "values_belongs": [36.0, REALLY_BIG_NUMBER],
                            "description": "выраженное расширение",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.GRADE3,
                        },
                    ]
                }
            },
            {
                "measure_num": 6,
                "field_id": "m_7_6",
                "measure_title": "ВТПЖ над ЛА,мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [REALLY_SMALL_NUMBER, 16.999],
                            "description": "ниже нормы",
                            "gender": None,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [17.0, 23.999],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [24.0, 27.999],
                            "description": "незначительное расширение",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [28.0, 31.999],
                            "description": "умеренное расширение",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.GRADE2,
                        },
                        {
                            "values_belongs": [32.0, REALLY_BIG_NUMBER],
                            "description": "выраженное расширение",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.GRADE3,
                        },
                    ]
                }
            },

            {
                "measure_num": 7,
                "field_id": "m_7_5",
                "measure_title": "ЛА ,мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [REALLY_SMALL_NUMBER, 14.999],
                            "description": "ниже нормы",
                            "gender": None,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [15.0, 21.999],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [22.0, 25.999],
                            "description": "незначительное расширение",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [26.0, 29.999],
                            "description": "умеренное расширение",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.GRADE2,
                        },
                        {
                            "values_belongs": [30.0, REALLY_BIG_NUMBER],
                            "description": "выраженное расширение",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.GRADE3,
                        },
                    ]
                }

            },
        ]
    },

    "UnknownBlock3": {
        "title": "UnknownBlock3",
        "print_title": "ЛА, НПВ",
        "group_num": 8,
        "group_id": "g_8",
        "visible_title": True,
        "disabled_title": False,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "m_8_1",
                "measure_title": "НПВ, мм",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [0.0, 20.999],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [21.0, REALLY_BIG_NUMBER],
                            "description": "расширение",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },
                    ]
                }

            },
            {
                "measure_num": 2,
                "field_id": "m_8_2",
                "measure_title": "Колабирует, %",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
            },
            {
                "measure_num": 3,
                "field_id": "m_8_3",
                "measure_title": "давл.ПП,мм.рт.ст",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: m_8_3_function(p1, p2),
                "needed_params": ["m_8_1", "m_8_2"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [0.0, 5.0],
                            "description": "(НПВ мм.) < 21  и (Колабирует %) > 50",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [15.0, REALLY_BIG_NUMBER],
                            "description": "(НПВ мм.) > 21  и (Колабирует %) < 50",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [5.001, 14.999],
                            "description": "другое",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.GRADE2,
                        },
                    ]
                }

            },

            {
                "measure_num": 4,
                "field_id": "m_8_4",
                "measure_title": "Сист.ДЛА,мм.рт.ст.",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: 4 * (p1 ** 2) + 5 if p2 == 0 else 4 * (p1 ** 2) + p2,
                "needed_params": ["m_10_3", "m_8_3"],
                "value_intervals": {
                    "intervals": [

                        {
                            "values_belongs": [-1 * REALLY_BIG_NUMBER, 0.0],
                            "description": "ОШИБКА",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [0.001, 34.999],
                            "description": "норма легочной артерии",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [35.0, REALLY_BIG_NUMBER],
                            "description": "повышенная",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },
                    ]
                }

            },

            {
                "measure_num": 5,
                "field_id": "m_8_5",
                "measure_title": "СрДЛА(Chembla),мм.рт.ст",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1: 0.61 * p1 + 2,
                "needed_params": ["m_8_4", ],
                "value_intervals": {
                    "intervals": [

                        {
                            "values_belongs": [-1 * REALLY_BIG_NUMBER, 0.0],
                            "description": "ОШИБКА",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [0.001, 24.999],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [25.0, REALLY_BIG_NUMBER],
                            "description": "повышенная",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },
                    ]
                }

            },

            {
                "measure_num": 6,
                "field_id": "m_8_6",
                "measure_title": "TAPSE/СДЛА",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: p1 / p2,
                "needed_params": ["m_6_5", "m_8_4"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [0.0, 0.5499],
                            "description": "пониженное",
                            "gender": None,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [0.55, REALLY_BIG_NUMBER],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },

                    ]
                }

            },
        ]
    },

    "aortic_valve": {
        "title": "aortic_valve",
        "print_title": "Артериальный клапан",
        "group_num": 9,
        "group_id": "g_9",
        "visible_title": True,
        "disabled_title": False,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "m_9_1",
                "measure_title": "Скор.макс.,м/с",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 0.899],
                            "description": "ошибка",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [0.9, 1.7],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [1.7001, 2.999],
                            "description": "1 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_1,
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [3.0, 4.0],
                            "description": "2 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_2,
                            "type": IntervalType.GRADE2,
                        },
                        {
                            "values_belongs": [4.001, REALLY_BIG_NUMBER],
                            "description": "3 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_3,
                            "type": IntervalType.GRADE3,
                        },
                    ]
                },

            },

            {
                "measure_num": 2,
                "field_id": "m_9_2",
                "measure_title": "Макс.Град.,мм.рт.ст.",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1: 4 * (p1 ** 2),
                "needed_params": ['m_9_1', ],

            },
            {
                "measure_num": 3,
                "field_id": "m_9_3",
                "measure_title": "Ср.Град.,мм.рт.ст",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 0.999],
                            "description": "ошибка",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [1.0, 12.0],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [12.001, 19.999],
                            "description": "превышение 1 степени",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_1,
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [20.0, 40.0],
                            "description": "превышение 2 степени",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_2,
                            "type": IntervalType.GRADE2,
                        },
                        {
                            "values_belongs": [40.001, REALLY_BIG_NUMBER],
                            "description": "превышение 3 степени",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_3,
                            "type": IntervalType.GRADE3,
                        },
                    ]
                },

            },

            {
                "measure_num": 4,
                "field_id": "m_9_4",
                "measure_title": "Площадь АК,см2",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [2.801, REALLY_BIG_NUMBER],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [1.5, 2.8],
                            "description": "1 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_1,
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [1.0001, 1.499],
                            "description": "2 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_2,
                            "type": IntervalType.GRADE2,
                        },
                        {
                            "values_belongs": [REALLY_SMALL_NUMBER, 1.0],
                            "description": "3 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_3,
                            "type": IntervalType.GRADE3,
                        },
                    ]
                }
            },
        ]
    },

    "pk_tk": {
        "title": "pk_tk",
        "print_title": "ПК и ТК",
        "group_num": 10,
        "group_id": "g_10",
        "visible_title": True,
        "disabled_title": False,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "m_10_1",
                "measure_title": "Скор.макс., м/с",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [0.5, 1.0],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [1.001, 2.999],
                            "description": "1 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_1,
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [3.0, 3.999],
                            "description": "2 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_2,
                            "type": IntervalType.GRADE2,
                        },
                        {
                            "values_belongs": [4.0, REALLY_BIG_NUMBER],
                            "description": "3 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_3,
                            "type": IntervalType.GRADE3,
                        },
                    ]
                },

            },
            {
                "measure_num": 2,
                "field_id": "m_10_2",
                "measure_title": "Макс.Град.,мм.рт.ст.",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1: 4 * (p1 ** 2),
                "needed_params": ['m_10_1', ],

            },
            {
                "measure_num": 3,
                "field_id": "m_10_3",
                "measure_title": "ТР макс.скор.,м/с",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 0.0999],
                            "description": "ошибка",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [0.1, 2.7999],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [2.8, REALLY_BIG_NUMBER],
                            "description": "превышение",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                    ]
                }

            },
            {
                "measure_num": 4,
                "field_id": "m_10_4",
                "measure_title": "Ср.Град.,мм.рт.ст.",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [5.0, REALLY_BIG_NUMBER],
                            "description": "стеноз",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.GRADE1,
                        },

                    ]
                }
            },
        ]
    },

    "diastolic_pk": {
        "title": "diastolic_pk",
        "print_title": "МК и Диастолическая ф-я",
        "group_num": 11,
        "group_id": "g_11",
        "visible_title": True,
        "disabled_title": False,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "m_11_1",
                "measure_title": "E, см/с",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 4.999],
                            "description": "ошибка",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [5.0, 50.0],
                            "description": "пониженное",
                            "gender": None,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [50.001, 130.0],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [130.001, REALLY_BIG_NUMBER],
                            "description": "превышение",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },

                    ]
                },

            },
            {
                "measure_num": 2,
                "field_id": "m_11_2",
                "measure_title": "A см/с",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],

            },

            {
                "measure_num": 5,
                "field_id": "m_11_5",
                "measure_title": "E/A",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: p1 / p2,
                "needed_params": ["m_11_1", "m_11_2"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [REALLY_SMALL_NUMBER, 0.8],
                            "description": "менее нормы",
                            "gender": None,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [0.801, 2.0],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [2.001, REALLY_BIG_NUMBER],
                            "description": "превышение",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        }
                    ]
                }
            },

            {
                "measure_num": 6,
                "field_id": "m_11_6",
                "measure_title": "TD, мсек",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [140.0, 200.0],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },

                    ]
                }
            },

            {
                "measure_num": 7,
                "field_id": "m_11_7",
                "measure_title": "e' бок, см/с",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 0.999],
                            "description": "ошибка",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [1.0, 9.999],
                            "description": "пониженное",
                            "gender": None,
                            "color": BELOW_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.LOWER,
                        },
                        {
                            "values_belongs": [10.0, REALLY_BIG_NUMBER],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },

                    ]
                }
            },

            {
                "measure_num": 8,
                "field_id": "m_11_8",
                "measure_title": "E/e'",
                "editable": False,
                "calculable": True,
                "enabled": True,
                "visible": True,
                "formula": lambda p1, p2: p1 / p2,
                "needed_params": ["m_11_1", "m_11_7"],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [-REALLY_BIG_NUMBER, 0.999],
                            "description": "ошибка",
                            "gender": None,
                            "color": ERROR_COLOR,
                            "type": IntervalType.ERROR,
                        },
                        {
                            "values_belongs": [1.0, 14.0],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [14.001, REALLY_BIG_NUMBER],
                            "description": "превышение давления в левом предсердии",
                            "gender": None,
                            "color": ABOVE_NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.UPPER,
                        },
                    ]
                }
            },

            {
                "measure_num": 3,
                "field_id": "m_11_3",
                "measure_title": "Ср.Град.,мм.рт.ст.",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [REALLY_SMALL_NUMBER, 5.0],
                            "description": "1 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_1,
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [5.001, 9.999],
                            "description": "2 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_2,
                            "type": IntervalType.GRADE2,
                        },
                        {
                            "values_belongs": [10.0, REALLY_BIG_NUMBER],
                            "description": "3 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_3,
                            "type": IntervalType.GRADE3,
                        },

                    ]
                },

            },

            {
                "measure_num": 4,
                "field_id": "m_11_4",
                "measure_title": "Площадь МК,см2",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [1.5, REALLY_BIG_NUMBER],
                            "description": "1 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_1,
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [1.001, 1.499],
                            "description": "2 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_2,
                            "type": IntervalType.GRADE2,
                        },
                        {
                            "values_belongs": [1 / REALLY_BIG_NUMBER, 1.0],
                            "description": "3 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_3,
                            "type": IntervalType.GRADE3,
                        },
                    ]
                }
            },

        ]
    },

    "UnknownBlock4": {
        "title": "UnknownBlock4",
        "print_title": "UnknownBlock4",
        "group_num": 12,
        "group_id": "g_12",
        "visible_title": False,
        "disabled_title": False,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "m_12_1",
                "measure_title": "МН,степень",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],

            },
            {
                "measure_num": 2,
                "field_id": "m_12_2",
                "measure_title": "МР v.c.(мм)",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [0.0, 0.0],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [REALLY_SMALL_NUMBER, 2.999],
                            "description": "1 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_1,
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [3.0, 6.0],
                            "description": "2 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_2,
                            "type": IntervalType.GRADE2,
                        },
                        {
                            "values_belongs": [6.001, REALLY_BIG_NUMBER],
                            "description": "3 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_3,
                            "type": IntervalType.GRADE3,
                        },

                    ]
                }

            },

            {
                "measure_num": 3,
                "field_id": "m_12_3",
                "measure_title": "МР EROA, см2",
                "editable": True,
                "calculable": False,
                "enabled": False,
                "visible": False,
                "formula": None,
                "needed_params": [],

            },

            {
                "measure_num": 4,
                "field_id": "m_12_4",
                "measure_title": "Фракция МР,%",
                "editable": True,
                "calculable": False,
                "enabled": False,
                "visible": False,
                "formula": None,
                "needed_params": [],
            },

            {
                "measure_num": 5,
                "field_id": "m_12_5",
                "measure_title": "АН, степень",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],

            },

            {
                "measure_num": 6,
                "field_id": "m_12_6",
                "measure_title": "АР v.c.(мм)",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [0.0, 0.0],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [REALLY_SMALL_NUMBER, 2.999],
                            "description": "1 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_1,
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [3.0, 6.0],
                            "description": "2 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_2,
                            "type": IntervalType.GRADE2,
                        },
                        {
                            "values_belongs": [6.001, REALLY_BIG_NUMBER],
                            "description": "3 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_3,
                            "type": IntervalType.GRADE3,
                        },

                    ]
                }
            },

            {
                "measure_num": 7,
                "field_id": "m_12_7",
                "measure_title": "ТН, степень",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
            },

            {
                "measure_num": 8,
                "field_id": "m_12_8",
                "measure_title": "ТР v.c.(мм)",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
                "value_intervals": {
                    "intervals": [
                        {
                            "values_belongs": [0.0, 0.0],
                            "description": "норма",
                            "gender": None,
                            "color": NORMAL_INTERVAL_COLOR,
                            "type": IntervalType.NORMAL,
                        },
                        {
                            "values_belongs": [REALLY_SMALL_NUMBER, 2.999],
                            "description": "1 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_1,
                            "type": IntervalType.GRADE1,
                        },
                        {
                            "values_belongs": [3.0, 6.0],
                            "description": "2 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_2,
                            "type": IntervalType.GRADE2,
                        },
                        {
                            "values_belongs": [6.001, REALLY_BIG_NUMBER],
                            "description": "3 ст",
                            "gender": None,
                            "color": GRADE_INTERVAL_COLOR_3,
                            "type": IntervalType.GRADE3,
                        },

                    ]
                }

            },

            {
                "measure_num": 9,
                "field_id": "m_12_9",
                "measure_title": "ПН, степень",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,
                "needed_params": [],
            },
        ]
    },

    "extra_block1": {
        "title": "extra_block1",
        "print_title": "Аортальный клапан",
        "group_num": 13,
        "group_id": "g_13",
        "visible_title": True,
        "disabled_title": False,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "m_13_1",
                # "measure_title": "створки не измен.",
                "measure_title": "створки не измен.",
                "editable": True,
                "calculable": False,
                "enabled": False,
                "visible": True,
                "formula": None,

                "non_numeric_field": True,
                "custom_element_type": "checkbox",
                "default_value": True,

                "needed_params": [],

            },
            {
                "measure_num": 2,
                "field_id": "m_13_2",
                # "measure_title": "створки уплотнены",
                "measure_title": "створки упло",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,

                "non_numeric_field": True,
                "custom_element_type": "checkbox",
                "default_value": False,

                "needed_params": [],

            },
            {
                "measure_num": 3,
                "field_id": "m_13_3",
                # "measure_title": "створки утолщены",
                "measure_title": "створки уто",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,

                "non_numeric_field": True,
                "custom_element_type": "checkbox",
                "default_value": False,

                "needed_params": [],

            },
            {
                "measure_num": 4,
                "field_id": "m_13_4",
                "measure_title": "АК - Кальцинир.",

                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,

                "non_numeric_field": True,
                "custom_element_type": "dropdown",
                "no_label_field": True,
                "options": [
                    {"---": "нет кальциноза."},
                    {"степень 1": "Незначительный кальциноз аортального клапана."},
                    {"степень 2": "Умеренный кальциноз аортального клапана."},
                    {"степень 3": "Выраженный кальциноз аортального клапана."},
                ],
                # "default_value": False,

                "needed_params": [],

            },

        ]
    },

    "extra_block2": {
        "title": "extra_block2",
        "print_title": "Митральный клапан",
        "group_num": 14,
        "group_id": "g_14",
        "visible_title": True,
        "disabled_title": False,
        "measurements": [
            {
                "measure_num": 1,
                "field_id": "m_14_1",
                # "measure_title": "створки не измен.",
                "measure_title": "створки не из.",
                "editable": True,
                "calculable": False,
                "enabled": False,
                "visible": True,
                "formula": None,

                "non_numeric_field": True,
                "custom_element_type": "checkbox",
                "default_value": True,

                "needed_params": [],

            },
            {
                "measure_num": 2,
                "field_id": "m_14_2",
                # "measure_title": "створки уплотнены",
                "measure_title": "створки уплот.",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,

                "non_numeric_field": True,
                "custom_element_type": "checkbox",
                "default_value": False,

                "needed_params": [],

            },
            {
                "measure_num": 3,
                "field_id": "m_14_3",
                # "measure_title": "створки утолщены",
                "measure_title": "створки уто",
                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,

                "non_numeric_field": True,
                "custom_element_type": "checkbox",
                "default_value": False,

                "needed_params": [],

            },
            {
                "measure_num": 4,
                "field_id": "m_14_4",
                "measure_title": "МК - Кальцинир.",

                "editable": True,
                "calculable": False,
                "enabled": True,
                "visible": True,
                "formula": None,

                "non_numeric_field": True,
                "custom_element_type": "dropdown",
                "no_label_field": True,
                "options": [
                    {"степень 1": "Незначительный кальциноз аортального клапана."},
                    {"степень 2": "Умеренный кальциноз аортального клапана."},
                    {"степень 3": "Выраженный кальциноз аортального клапана."},
                ],
                # "default_value": False,

                "needed_params": [],

            },

        ]
    },

}
