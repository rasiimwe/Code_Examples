#!/usr/bin/python
import psycopg2
import sys
import csv
import os
import string
import subprocess
#from psycopg2 import sql

con = None

try:
    con = psycopg2.connect(
        "host='localhost' dbname='genomic_variants' user='rasiimwe' password='password'")
    print "Opened database successfully"

    cur = con.cursor()

    #cur.execute("CREATE TABLE destruct_breakpoints(id serial primary key , tumour_id varchar references samples(tumour_id),prediction_id varchar,  chromosome_1 varchar,   strand_1 varchar,       position_1 varchar,     chromosome_2 varchar,   strand_2 varchar,	position_2 varchar,     homology varchar,	num_split varchar,	inserted varchar,        mate_score	varchar, template_length_1 varchar,     log_cdf varchar,        template_length_2 varchar,        log_likelihood varchar, template_length_min varchar,    num_reads varchar,	num_unique_reads varchar,        type varchar,   num_inserted varchar,   sequence varchar,	gene_id_1	varchar, gene_name_1 varchar,           gene_location_1 varchar,        gene_id_2 varchar,	gene_name_2     varchar, gene_location_2 varchar, dgv_ids varchar)")

    flout2 = open(
        "/home/rasiimwe/Projects/TNBC/destruct_breakpoint_read.txt", "a")
    flout3 = open(
        "/home/rasiimwe/Projects/TNBC/destruct_breakpoint_table.txt", "a")

    # flout3.write("tumour_id"+ '\t' + "prediction_id" + '\t'+ " chromosome_1" +'\t'+ "strand_1" +'\t'+ "position_1" +'\t'+ "chromosome_2" +'\t'+ "strand_2" +'\t'+ "position_2" +'\t'+ "homology" +'\t'+ "num_split" +'\t'+ "inserted" +'\t'+ "mate_score" +'\t'+ "template_length_1" +'\t'+ "log_cdf" +'\t'+ "template_length_2" +'\t'+ "log_likelihood" +'\t'+ "template_length_min" +'\t'+ "num_reads" +'\t'+ "num_unique_reads" + '\t'+ "type" +'\t'+ "num_inserted" +'\t'+ "sequence" +'\t'+ "gene_id_1" +'\t'+ "gene_name_1" +'\t'+ "gene_location_1" +'\t'+ "gene_id_2" +'\t'+ "gene_name_2" +'\t'+ "gene_location_2" + '\t'  + "dgv_ids"+"\n")
    # #cur.execute("select tumour_id, tumour_archive_id,  destruct from pipeline_result_paths")
#    cur.execute("select destruct from pipeline_result_paths")
#    path = cur.fetchall()

#    for x in path:
#            x = '%s' %(x)
#            #print x
#            id ='_destruct '.join(x.split('_destruct')[:1])
#            id ='destruct/'.join(id.split('destruct/')[1:])
#            #print id
#            os.chdir(x)

#           	for file in os.listdir(x):
    # 		#print file
# 			if "breakpoint_read_table" in file:
#                   	       	f2=open(file,"r")
    #                      	for i2 in f2:
#                        		x2= id + '\t ' + i2
    # 				flout2.write(x2)
#                                            #flout3.write( tumour_id + ',' +  ''.join(i3) + "\n")

    # 		elif "breakpoint_table" in file:
    # 			f3=open(file,"r")
    # 			for i3 in f3:
    # 				x3=id + '\t'+i3
    # 				flout3.write(x3)
#                                            #flout3.write( tumour_id + ',' +  ''.join(i3) + "\n")
    # #
    # 		else:
    # 			print "file not captured in loop - outlier", file

# ----------------------------------------------------------------------------------------
    flout3.close()
    os.chdir("/home/rasiimwe/Projects/TNBC/")
#	flout3 = open("/home/rasiimwe/Projects/TNBC/destruct_breakpoint_table.txt","a")
    flout3 = open(
        "/home/rasiimwe/Projects/TNBC/destruct_breakpoint_table.txt", "r")

    # if destruct_breakpoint_table.txt","a")
    # with open("/Users/rasiimwe/destruct_bp.csv","rU") as in_file3:
    #reader3 = csv.reader(flout3)
    for line in flout3:  # reader3:
        row = line.split('\t')
        tumour_archive_id = row[0]
        # print tumour_archive_id

        prediction_id = row[1]
        chromosome_1 = row[2]
        strand_1 = row[3]
        position_1 = row[4]
        chromosome_2 = row[5]
        strand_2 = row[6]
        position_2 = row[7]
        homology = row[8]
        num_split = row[9]
        inserted = row[10]
        mate_score = row[11]
        template_length_1 = row[12]
        log_cdf = row[13]
        template_length_2 = row[14]
        log_likelihood = row[15]
        template_length_min = row[16]
        num_reads = row[17]
        num_unique_reads = row[18]
        type = row[19]
        num_inserted = row[20]
        sequence = row[21]
        gene_id_1 = row[22]
        gene_name_1 = row[23]
        gene_location_1 = row[24]
        gene_id_2 = row[25]
        gene_name_2 = row[26]
        gene_location_2 = row[27]
        dgv_ids = row[28]

        # print tumour_archive_id,prediction_id,chromosome_1,strand_1,position_1,chromosome_2,strand_2,position_2,homology,num_split,inserted, mate_score
        cur.execute("INSERT INTO destruct_breakpoints (tumour_archive_id,prediction_id,chromosome_1,strand_1,position_1,chromosome_2,strand_2,position_2,homology,num_split,inserted, mate_score, template_length_1,log_cdf,template_length_2,log_likelihood,template_length_min,num_reads,num_unique_reads,type,num_inserted,sequence,gene_id_1,gene_name_1,gene_location_1,gene_id_2,gene_name_2,gene_location_2,dgv_ids) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                    (tumour_archive_id, prediction_id, chromosome_1, strand_1, position_1, chromosome_2, strand_2, position_2, homology, num_split, inserted, mate_score, template_length_1, log_cdf, template_length_2, log_likelihood, template_length_min, num_reads, num_unique_reads, type, num_inserted, sequence, gene_id_1, gene_name_1, gene_location_1, gene_id_2, gene_name_2, gene_location_2, dgv_ids))


# -------------------------------------------------------------------------------------------

    con.commit()

except psycopg2.DatabaseError, e:
    if con:
        con.rollback()
    print 'Eror %s' % e
    sys.exit(1)
