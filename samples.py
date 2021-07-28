#!/home/rasiimwe/miniconda3/bin/python
import psycopg2
import sys
import csv
import os

con = None

try:
	con = psycopg2.connect("host='localhost' dbname='dbname' user='rasiimwe' password='password'")
	print ("Opened database successfully")

	cur = con.cursor()#Python likes to be able to keep track of where it last left off in reading and writing to the database = cursor in psycopg

	glob = "/shahlab/archive/wgs_results/"
	
	#destruct  hmmcopy  lumpy_pypeline  mutationseq  strelka  titan > /lab/archive/wgs_results/sample_49/mutationseq > museq.vcf
	
	## Creating table samples and bulk loading data in database
	cur.execute("DROP TABLE IF EXISTS samples_new")
	cur.execute("CREATE TABLE samples_new(tumour_id VARCHAR, normal_id VARCHAR NOT NULL, consent_id VARCHAR, tumour_bamfile_loc VARCHAR, normal_bamfile_loc VARCHAR, facility_of_origin VARCHAR, sample_type VARCHAR, project VARCHAR REFERENCES projects (project_code) NOT NULL, PRIMARY KEY (tumour_id))")
	

	os.chdir(glob)
	x=1
	for root, dirs, files in os.walk(glob):
		for file in files:
			if file.endswith("museq.vcf"):
				full_path = os.path.join(root,file)
				base = "/".join(full_path.split("/")[:5])
				tumour_id = "/".join(base.split("/")[4:])
				normal_id = tumour_id + "N"
				print(normal_id, tumour_id, base)
				print(full_path)
 				#hmmcopy_path = base + "/hmmcopy/"             
				if tumour_id.startswith("SA"):
								
					#-------------------- insert available for samples----------------------
					cur.execute("INSERT INTO samples_new(tumour_id, normal_id, project) VALUES (%s,%s,'TNBC')", (tumour_id, normal_id))    
 	


	con.commit()
except psycopg2.DatabaseError as e:
	if con:
		con.rollback()

	print ('Error %s') % e
	sys.exit(1)

finally:
	if con:
		con.close()



