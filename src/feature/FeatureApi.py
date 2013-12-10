#!/usr/bin/env python
import sqlite3 as lite
import csv
class FeatureApi:
        DB = '/home/imicrobe/feature.db'
        QUERY_ONE = 'select * from feature where feature_id=:fid'
        QUERY_TWO = 'select * from feature where feature_id=? and seq_id=?'
        QUERY_THR = 'select * from feature where feature_id=? and seq_id=? and feature_name=?'
        def query_simap(self, fid, sid, fname):
                
                con = lite.connect(self.DB)
                with con:
                        cur = con.cursor() 
                        if sid != '' and fname != '':
                                cur.execute(self.QUERY_THR, (fid, sid, fname));
                        elif sid != '':
                                cur.execute(self.QUERY_TWO, (fid, sid));
                        else:
                                cur.execute(self.QUERY_ONE, {"fid":fid});
                        rows = cur.fetchall()
                
                return rows;
        
        def import_file(self, filename):        
                arr = list(csv.reader(open(filename, 'rb'), delimiter='\t'))
                con = lite.connect(self.DB)
                with con:
                        cur = con.cursor()
                        cur.executemany("INSERT INTO feature VALUES(?, ?, ?, ?,?,?,?,?,?,?,?,?,?)", arr)
                
        def create_table(self, filename):
                f = open(filename, 'r')
                with f:
                        data = f.read()        

                con = lite.connect(self.DB)
                with con:   
                        cur = con.cursor()
                        cur.executescript(data)

        def feature_annotate(self, filename):
                fo = open(filename+'.feature.out', 'wb')
                wr = csv.writer(fo, delimiter='\t')
                with open(filename, 'rb') as f:
                        reader = csv.reader(f, delimiter='\t')
                        for row in reader:
                                arr = list(row)
                                if len(arr) < 2 :
                                        continue;
                                entries = self.query_simap(str(arr[2]), "", "");
                                for entry in entries:
                                        arr.extend(entry)
                                        wr.writerow(arr)




