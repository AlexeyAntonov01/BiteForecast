IMPORTANCE = {
    'pressure_weight':    3.5,  # Давление — абсолютный лидер влияния
    'temperature_weight': 3.0,  # Температура воды/воздуха крайне важна
    'time_weight':        2.5,  # Время суток (ночь/рассвет) — сильный фактор
    'windSpeed_weight':   1.5,  # Сила ветра
    'windAngle_weight':   1.2,  # Направление ветра
    'prec_weight':        0.8,  # Интенсивность осадков (фоновое)
    'prec_type_weight':   0.6,  # Тип осадков (фоновое)
    'cloudiness_weight':  0.5,  # Облачность (фоновое)
    'humidity_weight':    0.3,  # Влажность (почти не влияет на рыбу напрямую)
}

IDEAL = {
	"ЛЕЩ": {

        "treands":
        {
            "pressure_max_delta": 2.5,
            "pressure_penalty": 0.15,
            "bitekiller_pressure": 0.25,
            "wind_max_delta": 4.0,
            "wind_penalty": 0.30,
            "bitekiller_wind": 0.25,
            "temp_max_delta": 4.0,
            "temp_penalty": 0.30,
            "bitekiller_temp": 0.25

        },

		"temperature" : {
			"min": 18,
		    "max": 22,
		    "tolerance_min": 6,
		    "tolerance_max": 6
		    },
	    "pressure" : {
	    	"min": 745,
		    "max": 755,
		    "tolerance_min": 10, 
		    "tolerance_max": 10
	    	},
	    "windSpeed" : {
	    	"min" : 0.0,
		    "max": 3.5,
		    "tolerance_min": 4.0,
		    "tolerance_max": 4.0
	    	},    
	    "windAngle": {
	    	"min": 135,        
	    	"max": 315,        
	    	"tolerance_min": 90,
	    	"tolerance_max": 90
	    },
	    "humidity": {
		    "min": 60,      
		    "max": 85,
		    "tolerance_min": 20, 
		    "tolerance_max": 10  
		},
		"prec": {
		    "min": 0.0,
		    "max": 1.0,     
		    "tolerance_min": 0,
		    "tolerance_max": 4.0 
		},
		"timeOfDay":{
			"hour": {
				"best_hours": [4, 5, 6, 20, 21, 22],
				"good_hours": [3, 7, 8, 9, 19, 23],
				"bad_hours": [10, 11, 12, 13, 14, 15, 16],
				"terrible_hours": [0, 1, 2]
			},
			"weights": {
                "best": 1.0,
                "good": 0.8,
                "bad": 0.4,
                "terrible": 0.1
            }
		},
	    "cloudiness_optimal": ["CLOUDY", "OVERCAST", "SIGNIFICANT"],
	    "bad_values": ["CLEAR", "PARTLY"],
	    "cloudiness_penalty": 0.7,    
	    "prec_type_optimal": ["NO_TYPE", "RAIN"],
	    "bad_values": ["SLEET", "SNOW", "HAIL"],
	    "prec_type_penalty": 0.7,      
	    "moon_phase_optimal": ["NEW_MOON", "WAXING_CRESCENT", "FIRST_QUARTER", "WAXING_GIBBOUS", "WANING_GIBBOUS", "THIRD_QUARTER", "WANING_CRESCENT"],
	    "moon_phase_penalty": 0.5   
    },


    "ЯЗЬ": {
      
        "treands":
        {
            "pressure_max_delta": 2.5,
            "pressure_penalty": 0.15,
            "bitekiller_pressure": 0.25,
            "wind_max_delta": 4.0,
            "wind_penalty": 0.30,
            "bitekiller_wind": 0.25,
            "temp_max_delta": 4.0,
            "temp_penalty": 0.30,
            "bitekiller_temp": 0.25

        },

        "temperature": {
            "min": 16, "max": 24,
            "tolerance_min": 6, "tolerance_max": 6
        },
        "pressure": {
            "min": 740, "max": 755,
            "tolerance_min": 10, "tolerance_max": 10
        },
        "windSpeed": {
            "min": 0.5, "max": 4.0,
            "tolerance_min": 3.0, "tolerance_max": 4.0
        },
        "windAngle": {
            "min": 135, "max": 315,
            "tolerance_min": 90, "tolerance_max": 90
        },
        "humidity": {
            "min": 55, "max": 80,
            "tolerance_min": 20, "tolerance_max": 15
        },
        "prec": {
            "min": 0.0, "max": 1.5,
            "tolerance_min": 0, "tolerance_max": 4.0
        },
        "timeOfDay": {
            "hour": {
                "best_hours": [5, 6, 7, 19, 20, 21],
                "good_hours": [4, 8, 9, 18, 22],
                "bad_hours": [10, 11, 12, 13, 14, 15, 16],
                "terrible_hours": [0, 1, 2, 3]
            },
            "weights": {
                "best": 1.0, "good": 0.8,
                "bad": 0.4, "terrible": 0.1
            }
        },
        "cloudiness_optimal": ["CLOUDY", "OVERCAST", "SIGNIFICANT", "PARTLY"],
        "bad_values": ["CLEAR"],
        "cloudiness_penalty": 0.8,
        "prec_type_optimal": ["NO_TYPE", "RAIN"],
        "bad_values": ["SLEET", "SNOW", "HAIL"],
        "prec_type_penalty": 0.7,
        "moon_phase_optimal": ["NEW_MOON", "WAXING_CRESCENT", "FIRST_QUARTER",
                               "WAXING_GIBBOUS", "WANING_GIBBOUS", "THIRD_QUARTER",
                               "WANING_CRESCENT"],
        "moon_phase_penalty": 0.5
    }

}