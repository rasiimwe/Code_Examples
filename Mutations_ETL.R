library(VariantAnnotation)
library(dplyr)
library(tidyr)
library(splitstackshape)
library(RPostgreSQL)
library(ggplot2)

pw <- { " "}
database_name <- "x" #provide database name

drv <- dbDriver("PostgreSQL")
con <- dbConnect(drv, dbname = database_name, host = "localhost", user = "rasiimwe", password = pw)
rm(pw)

dbExistsTable(con, "pipeline_result_paths")
museqsnvs <- dbGetQuery(con, "select tumour_id, mutationseq from pipeline_result_paths")
museqsnvs <- as.data.frame(museqsnvs)
tumour_id1 = museqsnvs[1]
museqsnvs_path = museqsnvs[2]

#print(tumour_id1)
#print(museqsnvs_path)

#for every path in museqsnvs_path, read the file that ends wth flagcosmic.vcf
 
for(i in museqsnvs_path){
        files <- Sys.glob(file.path(i, "*.vcf"))
        for (f in files){
               # print (f)
                x <- matrix(unlist(strsplit(as.character(f), '/')), ncol=1, byrow=TRUE)
                tumour_id <- as.character(x[5])
                ##tumour_archive_id <- matrix(unlist(strsplit(as.character(x[9]), '_museq')), ncol=1, byrow=TRUE) #for montreal
               	#print (tumour_id)
		
	
		vcf <- readVcf(f, "hg19")# museq
              	if (dim(vcf)[1]!=0){
	            	initial <- data.frame(info(vcf)) #everything under info
        	  	##all <- data.frame(info(vcf)) #everything under
         		initial <- tibble::rownames_to_column(initial, "chrom_pos_ref_alt")
			#print(initial)

			split1 <- matrix(unlist(strsplit(as.character(initial$chrom_pos_ref_alt), ':')), ncol=2, byrow=TRUE)
	      		after <- cbind(initial$chrom_pos_ref_alt, as.data.frame(split1))
      			names(after) <- c("chrom_pos_ref_alt", "chrom", "pos")
      			split2 <- matrix(unlist(strsplit(as.character(after$pos), '_')), ncol=2, byrow=TRUE)
      			after2 <-cbind(after, split2)
      			names(after2) <- c("chrom_pos_ref_alt", "chrom", "pos1", "pos", "ref_alt")
      			split3 <- matrix(unlist(strsplit(as.character(after2$ref_alt), '/')), ncol=2, byrow=TRUE)
	      		after3 <-cbind(after2, split3)
      			names(after3) <- c("chrom_pos_ref_alt", "chrom", "pos1", "pos", "ref_alt", "ref", "alt")
      
     			initial <- cbind (after3$chrom, after3$pos,after3$ref,after3$alt,initial)
	      		#initial <- cbind (initial, after3$chrom, after3$pos,after3$ref,after3$alt)
      			names(initial)[names(initial) == 'after3$chrom'] <- 'chrom'
      			names(initial)[names(initial) == 'after3$pos'] <- 'pos'
	      		names(initial)[names(initial) == 'after3$ref'] <- 'ref'
      			names(initial)[names(initial) == 'after3$alt'] <- 'alt'
      			initial$chrom_pos_ref_alt <- NULL
     
   
      
	      		newann<-cSplit(initial, 13, sep = ",", direction = "long", fixed = FALSE, drop = TRUE, stripWhite = TRUE, makeEqual =FALSE,  type.convert = TRUE)
      			newann <- as.data.frame(newann)
      			newann[] <- lapply(newann, gsub, pattern='"', replacement='')
	      		newann <- cSplit(newann, "ANN", "|")
      			names(newann)[names(newann) %in% c("chrom","pos","ref","alt","PR","TC","TR","TA","NR","NA.","ND", "NI","LOF","NMD","MA","DBSNP","X1000Gen","Cosmic","ANN_01","ANN_02","ANN_03","ANN_04","ANN_05","ANN_06","ANN_07","ANN_08","ANN_09","ANN_10","ANN_11","ANN_12","ANN_13","ANN_14","ANN_15","ANN_16")]<-c("chrom","pos","ref","alt","PR","TC","TR","TA","NR","NA","ND", "NI","LOF","NMD","MA","DBSNP","X1000Gen","Cosmic","allele","annotation", "annotation_impact", "gene_name", "gene_id", "feature_type", "feature_id", "transcript_biotype", "rank", "hgvs_c", "hgvs_p","cdna_pos_cdna_length", "cds_pos_cds_length", "aa_pos_aa_length", "distance", "errors_warnings_info")
      			newann[] <- lapply(newann, gsub, pattern='\\(', replacement='')
	      		newann[] <- lapply(newann, gsub, pattern=')', replacement='')
      			newann$allele[] <- lapply(newann$allele, gsub, pattern='c', replacement='')
     

      			newann$tumour_id <- " "
	      		newann$tumour_id <- tumour_id
      			newann <- setNames(newann, tolower(colnames(newann)))
      			museq_unfiltered <- newann[,c(35,1:12,19:34,13:18)]
			#museq_unfiltered <- newann[,c(1:12,19:34,13:18)]
	      		museq_unfiltered <- cbind("id"=1:nrow(museq_unfiltered), museq_unfiltered)

			dbWriteTable(con, "museq_unfiltered", museq_unfiltered, append=TRUE, row.names=0)

 		}
	}

}

dbDisconnect(con)
#dbUnloadDriver(drv)

