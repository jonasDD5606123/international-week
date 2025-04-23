from database_context import DatabaseContext

sql = ''' '''
dc = DatabaseContext()
conn = dc.getDbConn()
cursor = conn.cursor()
cursor.execute(sql)
conn.commit()