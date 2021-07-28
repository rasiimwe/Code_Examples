#!/home/rasiimwe/miniconda3/bin/python
import psycopg2
import sys
import csv
import os

con = None

try:
	con = psycopg2.connect("host='localhost' dbname='genomic_variants' user='rasiimwe' password='password'")
	print ("Opened database successfully")

	cur = con.cursor()#Python likes to be able to keep track of where it last left off in reading and writing to the database = cursor in psycopg

	glob = "/genesis/shahlab/danlai/TNBC-77/PAIR_STRE/strelka_pipeline/OUTPUT/RUN"
	glob2="/genesis/shahlab/danlai/TNBC-77/PAIR_TITA/titan_pipeline/OUTPUT/RUN"

	#destruct  hmmcopy  lumpy_pypeline  mutationseq  strelka  titan > /shahlab/archive/wgs_results/SA1070/mutationseq >museq.vcf
	
	## Creating pipeline_result_paths
	##---------------------------------------------------------------------------------------------------------
	#cur.execute("DROP TABLE IF EXISTS kronos_pipeline_result_paths")
	#cur.execute("CREATE TABLE kronos_pipeline_result_paths(tumour_id VARCHAR, strelka VARCHAR,  titan VARCHAR,  PRIMARY KEY(tumour_id))")

	#os.chdir(glob)
	
	#for root, dirs, files in os.walk(glob):
	#	for file in files:
	#		if file.endswith("snvs.annotSnpEff.annotMA.flagDBsnp.flag1000gen.flagCosmic.vcf"):
	#			full_path = os.path.join(root,file)
	#			base="/".join(full_path.split("/")[:-1])
	#			#print(base)
	#			#print(full_path)
	#			x = "_strelka.passed".join(full_path.split("_strelka.passed")[:1])
	#			tumour_id="_".join(x.split("_")[-1:])
	#			cur.execute("INSERT INTO kronos_pipeline_result_paths (tumour_id, strelka) VALUES (%s,%s)", (tumour_id, base))
	
	os.chdir(glob2)
	for root, dirs, files in os.walk(glob2):
		for file in files:
			if file.endswith("pygenes_segs.txt"):
				full_path = os.path.join(root,file)
				base="/".join(full_path.split("/")[:-1])
				x = "_titan".join(full_path.split("_titan")[:1])
				id="_".join(x.split("_")[-1:])
				tumour_id = "/".join(id.split("/")[-1:])
				print (tumour_id)
				cur.execute("update kronos_pipeline_result_paths set titan=%s where tumour_id=%s", (base, tumour_id))	
 	##--------------------------------------------------------------------------------------------------------

	


	con.commit()
except psycopg2.DatabaseError as e:
	if con:
		con.rollback()

	print ('Error %s') % e
	sys.exit(1)

finally:
	if con:
		con.close()



