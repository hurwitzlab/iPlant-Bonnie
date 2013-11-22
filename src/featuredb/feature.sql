CREATE TABLE FEATURE(
   feature_id varchar(128) NOT NULL,
   seq_id varchar(128) NOT NULL,
   protein_len INT8,
   dbname varchar(128),
   feature_name varchar(128),
   feature_desc varchar(128),
   hit_start INT8,
   hit_stop INT8,
   evalue varchar(128),
   true_pos_flag varchar(128),
   date TEXT,
   interpro_name varchar(128),
   interpro_desc varchar(128),
   UNIQUE (feature_id, seq_id,feature_name) ON CONFLICT REPLACE,
   PRIMARY KEY(feature_id , seq_id, feature_name)
);
