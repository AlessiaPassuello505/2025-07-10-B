from database.DB_connect import DBConnect
from model.Arco import Arco
from model.Prodotto import Prodotto


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getDateRange():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT distinct (order_date) from orders o order by order_date"

        cursor.execute(query)

        for row in cursor:
            results.append(row["order_date"])

        first = results[0]
        last = results[-1]

        cursor.close()
        conn.close()
        return first, last

    @staticmethod
    def getCategorie():

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select distinct c.category_name 
                    from categories c """

        cursor.execute(query)

        for row in cursor:
            results.append(row["category_name"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodi(categoria):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """  select p.*
                    from products p, categories c 
                    where p.category_id =c.category_id and c.category_name = %s """

        cursor.execute(query,(categoria,))

        for row in cursor:
            results.append(Prodotto(**row))

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getArchi(categoria,d1,d2,idMapP):

        conn = DBConnect.get_connection()

        results = []

        cursor = conn.cursor(dictionary=True)
        query = """ select t1.prodotto p1, t2.prodotto p2, t1.q +t2.q  as peso
from (select p.product_id prodotto , sum(oi.quantity) q
from products p, categories c, order_items oi ,orders o 
where  p.category_id =c.category_id and c.category_name = %s and p.product_id =oi.product_id and oi.order_id =o.order_id 
and o.order_date between %s and %s
group by p.product_id )t1,
(select p.product_id prodotto , sum(oi.quantity) q
from products p, categories c, order_items oi ,orders o 
where  p.category_id =c.category_id and c.category_name =%s and p.product_id =oi.product_id and oi.order_id =o.order_id 
and o.order_date between %s and %s
group by p.product_id )t2
where t1.prodotto <>t2.prodotto and t1.q<=t2.q 
group by t1.prodotto ,t2.prodotto 
order by peso desc """

        cursor.execute(query, (categoria,d1,d2,categoria,d1,d2 ))

        for row in cursor:
            results.append(Arco(idMapP[row["p1"]], idMapP[row["p2"]], row["peso"]))

        cursor.close()
        conn.close()
        return results


