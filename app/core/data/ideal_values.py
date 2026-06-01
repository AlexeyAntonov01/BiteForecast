IMPORTANCE = {
    'pressure_weight':    2.0,  # Давление — абсолютный лидер влияния
    'temperature_weight': 2.0,  # Температура воды/воздуха крайне важна
    'time_weight':        1.5,  # Время суток (ночь/рассвет) — сильный фактор
    'windSpeed_weight':   1.5,  # Сила ветра
    'windAngle_weight':   1.2,  # Направление ветра
    'prec_weight':        1.0,  # Интенсивность осадков (фоновое)
    'prec_type_weight':   0.8,  # Тип осадков (фоновое)
    'cloudiness_weight':  0.7,  # Облачность (фоновое)
    'humidity_weight':    0.5,  # Влажность (почти не влияет на рыбу напрямую)
}

IDEAL = {
	"ЛЕЩ": {

        "treands": {
          "pressure_max_delta": 2.0,
          "pressure_penalty": 0.10,
          "bitekiller_pressure": 0.30,
          "wind_max_delta": 2.5,
          "wind_penalty": 0.20,
          "bitekiller_wind": 0.40,
          "temp_max_delta": 1.5,
          "temp_penalty": 0.25,
          "bitekiller_temp": 0.50
        },

		"temperature" : {
			"min": 20,
		    "max": 22,
		    "tolerance_min": 3,
		    "tolerance_max": 3
		    },
	    "pressure" : {
	    	"min": 760,
		    "max": 762,
		    "tolerance_min": 5, 
		    "tolerance_max": 5
	    	},
	    "windSpeed" : {
	    	"min" : 0.5,
		    "max": 2.5,
		    "tolerance_min": 1.0,
		    "tolerance_max": 1.5
	    	},    
	    "windAngle": {
	    	"min": 180,        
	    	"max": 270,        
	    	"tolerance_min": 45,
	    	"tolerance_max": 45
	    },
	    "humidity": {
		    "min": 60,      
		    "max": 80,
		    "tolerance_min": 10, 
		    "tolerance_max": 10  
		},
		"prec": {
		    "min": 0.0,
		    "max": 0.5,     
		    "tolerance_min": 0,
		    "tolerance_max": 1.0 
		},
		"timeOfDay":{
			"hour": {
				"best_hours": [5, 6, 20, 21],
				"good_hours": [4, 7, 8, 19, 22],
				"bad_hours": [3, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
				"terrible_hours": [0, 1, 2, 23, 24]
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
	    "cloudiness_penalty": 0.3,    
	    "prec_type_optimal": ["NO_TYPE", "RAIN"],
	    "bad_values": ["SLEET", "SNOW", "HAIL"],
	    "prec_type_penalty": 0.5,      
	    "moon_phase_optimal": ["NEW_MOON", "WAXING_CRESCENT", "FIRST_QUARTER", "WAXING_GIBBOUS", "WANING_GIBBOUS", "THIRD_QUARTER", "WANING_CRESCENT"],
	    "moon_phase_penalty": 0.2   
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