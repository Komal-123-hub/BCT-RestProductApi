import sqlite3
import os

class ProductModel:
    def __init__(self):
        
        try:
            self.conn=sqlite3.connect('ProductsDB.db',check_same_thread=False)
            self.create_product_table()
            self.conn.row_factory=sqlite3.Row
        except sqlite3.error as e:
            print(e)

    def __del__(self):                                  
        self.conn.commit()                                    
        self.conn.close()                                      
                                                            
    def get_all_products(self):  

        query='SELECT product_id, product_name, product_brand, product_description, product_price FROM Products'      
        result_set=self.conn.execute(query).fetchall()        
        result=[
            {column:row[i] for i,column in enumerate(result_set[0].keys())}
            for row in result_set
        ]
        return result

    def create_product(self,product_name, product_brand, product_description, product_price, product_img):
        
        def convertToBinaryData(filename):
            try:
                with open(filename, 'rb') as file:
                    blobData = file.read()
                print(blobData)
                return blobData
            except IOError as ex:
                print("Error: can\'t find file or read data")
        
        try:
            
            photo = product_img
            #print(photo)
            product_img = convertToBinaryData(photo)        
            #print(product_img)
            
            sqlite_insert_blob_query = f""" INSERT INTO Products (product_name, product_brand, product_description, product_price, product_img)  VALUES (?, ?, ?, ?, ?)"""
            data_tuple = (
                                product_name,
                                product_brand,
                                product_description,
                                product_price,
                                product_img
                            )
            
            result = self.conn.execute(sqlite_insert_blob_query,data_tuple)
            return self.get_product_by_id(result.lastrowid)
 
        except sqlite3.Error as error:
                print("Failed to insert blob data into sqlite table", error)
        except sqlite3.IntegrityError:
                print("UNIQUE constraint failed: Products.product_id")
        finally:
                print("the sqlite connection is closed")


        
    def get_product_by_id(self, product_id):
        query = 'SELECT product_id, product_name, product_brand, product_description, product_price FROM Products WHERE product_id={0}'.format(product_id)
        result_set=self.conn.execute(query).fetchall()
        result=[
            {column: row[i] for i,column in enumerate(result_set[0].keys())}
            for row in result_set
        ]
        return result



    def update_product(self, product_id, product_name, product_brand, product_description, product_price, product_img):

        def convertToBinaryData(filename):
            try:
                # Convert digital data to binary format
                with open(filename, 'rb') as file:
                    blobData = file.read()
                print(blobData)
                return blobData
            except IOError as ex:
                print("Error: can\'t find file or read data")

        try:

            photo = product_img
            #print(photo)
            product_img = convertToBinaryData(photo)        
            #print(product_img)

            query="UPDATE Products SET product_name= ?, product_brand= ?, product_description= ?, product_price= ?, product_img= ?  WHERE product_id= ? "
            data=(
                product_name,
                product_brand,
                product_description,
                product_price,
                product_img,
                product_id
            )
            self.conn.execute(query,data)
            return self.get_product_by_id(product_id)
        except sqlite3.IntegrityError:
            print("UNIQUE constraint failed: Products.product_id")


    def delete_product(self, product_id):

        query='DELETE from Products WHERE product_id={0}'.format(product_id)
        result=self.conn.execute(query)
        status= 200 if result.rowcount == 1 else 404
        return {"status":status,"affected_rows":result.rowcount}



    def create_product_table(self):

        query="""
        CREATE TABLE IF NOT EXISTS "Products" (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT NOT NULL,
            product_brand TEXT NOT NULL,
            product_description TEXT,
            product_price INTEGER NOT NULL,
            product_img BLOB
            );
            """
        self.conn.execute(query)
    
    