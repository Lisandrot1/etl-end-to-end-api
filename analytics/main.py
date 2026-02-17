from querys import (get_temp_actual,
                    get_top5_countrys_calientes,
                    get_city_mas_frio
                    )

# simple call to the example query
if __name__ == '__main__':
    df = get_city_mas_frio()
    df_ventas = get_temp_actual()
    print(df)
