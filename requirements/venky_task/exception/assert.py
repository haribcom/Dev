def kelvintoforiegn(temparature):
    assert (temparature>=0), """its colder than absolute"""
    return ((temparature-273)*1.8)+32

try:
    print(kelvintoforiegn(273))
    print(kelvintoforiegn(505.23))
    print(kelvintoforiegn(-5))
except:
    print("error occured")
