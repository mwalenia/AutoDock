
import ADTparser as fp
#filename=input("Enter path or filename of .dlg file:",)
# Database creation
def df2sqlite(dataframe, db_name="ATD_database.db", tbl_name="data"):
    import sqlite3
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()

    wildcards = ','.join(['?'] * len(dataframe.columns))
    data = [tuple(x) for x in dataframe.values]

    #cur.execute("drop table if exists %s" % tbl_name)

    col_str = '"' + '","'.join(dataframe.columns) + '"'
    cur.execute("create table IF NOT EXISTS %s (%s)" % (tbl_name, col_str))
    cur.executemany("insert into %s values(%s)" % (tbl_name, wildcards), data)

    cur.execute("DELETE FROM data WHERE rowid NOT IN (SELECT min(rowid) FROM data GROUP BY Date, Protein, Run, Energy)")

    conn.commit()
    conn.close()
    #print("Data from",filename,"successfuly uploaded to the",db_name)

#df2sqlite(fp.parse(filename),'ATD_database.db','data')
