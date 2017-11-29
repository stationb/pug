from pyley import CayleyClient, GraphObject


if __name__ == '__main__':
    client = CayleyClient()
    g = GraphObject()

    q = g.V('<pug://building/EARHART_RD_bldgL877>').All()

    r = client.Send(q)
    print(r.result)
