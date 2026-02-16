from querys import get_fact

# simple call to the example query
if __name__ == '__main__':
    df_ventas = get_fact()
    print(df_ventas)
