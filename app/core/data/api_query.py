# moonPhase - фаза Луны
# sunrise - время восхода солнца
# sunset - время заката
# time - время
# temperature - температура воздуха
# pressure -  атмосферное давление (мм рт.ст.)
# precType - тип осадков
    # NO_TYPE — без осадков; 
    # RAIN — дождь; 
    # SLEET — дождь со снегом; 
    # SNOW — снег; 
    # HAIL — град. 
# cloudiness - облачность
# windSpeed - скорость ветра (м/с)
# windGust - порывы ветра (м/с)
# windAngle - направление ветра в градусах
# humidity - влажность воздуха (%)
# season - сезон
# daytime - время суток (утро, день, вечер, ночь)
# precProbability - вероятность осадков

def get_query(*,lat: float,lon:float) -> str:

  
  query = f"""
  {{
    weatherByPoint(request: {{ lat: {lat}, lon: {lon} }}) {{
      forecast {{
        days(limit: 1,offset: 1) {{
          moonPhase
          sunrise
          sunset
          hours {{
            time
            temperature
            pressure
            prec
            precType 
            precStrength
            cloudiness
            windSpeed
            windGust
            windAngle
            humidity
          }}
        }}
      }}
      now {{
        season
        daytime
        precProbability
      }}
    }}
  }}
  """

  return query
