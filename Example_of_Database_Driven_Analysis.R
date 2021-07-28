## Example of Database (DB)-Driven Analysis: Oncoplot DB call
## Author: Rebecca Asiimwe
## Version: 1.0.0
## Last modified: Dec 1, 2018
## Function: multi-mutation impact, case-gene plot
## Input: 3-column data frame with header: case, gene, type or a directory that contains these files
## Output: case-gene-aberration plot (oncoplot)
## Usage: Rscript onco.R

# Load required packages
library(RPostgreSQL)
library(ggplot2)
library(splitstackshape)
library(RColorBrewer)
library(gsubfn)
library(tidyverse)
library(stringi)
library(reshape2)
library(dplyr)
library(plyr)
library(Cairo) 
library(magicfor)  
# ---------------------------------------------------------------------------------------

# DB connection - remote call  
# connecting to db on server node using ssh tunnelling on port x: 
# run (depends on local config): 
#     ssh -L x:localhost:x1 rasiimwe@lab17                 

pw <- " " 
port_number <- x #provide port number for DB connection
database_name <- y #provide database name
usr <- "rasiimwe" #DB user name

#Connecting to back-end database

drv <- dbDriver("PostgreSQL") #DBMS
con <- dbConnect(drv, dbname = database_name,
                 host = "localhost", port = port_number,
                 user = usr, password = pw)
on.exit(dbDisconnect(con))

# ---------------------------------------------------------------------------------------

gene.list <- c("TP53","PIK3CA","PTEN","RB1","BRCA1","BRCA2","GATA3","ERBB2","USH2A","EGFR", "MUC21", "EMCN", "MUC4", "MB", "CTU2", "RAB3IL1", "CLEC9A", "NOL10", "LAMB4", "OTOR","TMEM80", "NUBPL", "TRPM3", "PLP1", "SPATA4", "GUCY2C","PRB3", "MIDN")
annotation.list <- c("inframe", "missense", "gene_fusion", "frameshift", "splice_acceptor", "splice_donor", "stop_lost", "stop_gained", "start_lost")


# DB call for cnas
copy_number.homd <- function(gene.list){
  
  if (!is.character(gene.list)) {
    stop(paste("Expecting gene.list to be of type character. You supplied", typeof(gene.list)))
  }
  else 
    if(is_empty(gene.list)){
      stop(paste("Expecting a list of gene elements. The vector supplied is empty"))
    }
  
  else 
  {
    gene.list <- paste(gene.list, "%;", sep="")
    gene.list <- paste( "%,", gene.list,sep="")
    genes.list <- as.vector(gene.list)
    
    magic_for(print, silent=TRUE) 
    
    for(i in genes.list){
      gene <- i
      query <- fn$identity("select distinct tumour_id, titan_call from titan_segs_cnas where pygenes_gene_id_gene_name like '$gene' and titan_call='HOMD'")
      x <- dbGetQuery(con, query)
      
      if (nrow(x)!=0)
      {
        i2 <- i
        i2 <- gsub(".{2}$", "", i2)
        i2 <- sub('..', '', i2)
        x <- x %>% 
          mutate(gene_name=i2)
        x <- as.data.frame(x)
        x <- na.omit(x)
        print(x)
      }
      else{
        next
      }
      
    }
    
  }
}

output <- copy_number.homd(gene.list)
onco <- do.call(rbind, output$x)
onco <- as.data.frame(onco)
onco <- onco[,c(1,3,2)]

#----------------------------------------------------------------------------

gene.effect <- function(gene.list, annotation.list ){
  
  if (!is.character(gene.list) | !is.character(annotation.list)) {
    stop(paste("Expecting gene list or annotation list to be of type character. You supplied", typeof(gene.list), "for gene list and ",typeof(annotation.list),"for annotation list" ))
  }
  else 
    if(is_empty(gene.list) | is_empty(annotation.list) ){
      stop(paste("Expecting a list of gene or annotation elements. The vector supplied is empty"))
    }
  
  else 
  {
    genes.list <- as.vector(gene.list)
    
    for(i in genes.list){
      annotation.list <- paste(annotation.list, "%", sep="")
      annotation.list <- paste( "%", annotation.list,sep="")
      annotations.list <- as.vector(annotation.list)
      
      for(j in annotations.list){
        gene <- i
        effect <- j
        
        query <- fn$identity("select distinct tumour_id, gene_name, annotation from strelka_indels where gene_name like '$gene' and annotation like '$effect' union select distinct tumour_id,gene_name, annotation from snvs_intersect where gene_name like '$gene' and annotation like '$effect' and pr>0.9 order by gene_name asc")
        x <- dbGetQuery(con, query)
        x <- as.data.frame(x)
        
        if (nrow(x)!=0)
        {
          x <- as.data.frame(x)
          x <- na.omit(x)
          print(x)
        }
        else{
          next
        }
      }
    }
  }
}

output.gene.effect <- as.data.frame(capture.output(gene.effect(gene.list, annotation.list)))

effects0 <- cSplit(output.gene.effect, 1, sep = " ", direction = "wide", fixed = FALSE, drop = TRUE, stripWhite = TRUE, makeEqual =TRUE,  type.convert = TRUE)
effects0 <- na.omit(effects0)
effects0[,1] <- NULL
names(effects0) <- c("tumour_id", "gene_name", "annotation")
effects0 <- cSplit(effects0, 3, sep = "&", direction = "long", fixed = FALSE, drop = TRUE, stripWhite = TRUE, makeEqual =TRUE,  type.convert = TRUE)
effects <- na.omit(effects0)

names(onco)[names(onco)=='titan_call'] <- 'annotation'
effects <- rbind(onco,effects)

case.gene.type <- effects
names(case.gene.type) <- c("case", "gene", "type")

case.gene.type <- case.gene.type %>% add_count(type)

b = acast(case.gene.type, gene~case)
case.gene.type$gene <- factor(case.gene.type$gene, levels = names(sort(rowSums(b),decreasing = FALSE)))

gene_order = unique(case.gene.type[ ,"gene"])
sample_order = unique(case.gene.type[ ,"case"])
gene.order <- as.data.frame(gene_order)
sample.order <- as.data.frame(sample_order)

# Assign a color to each mutation type 
colourCount = length(unique(case.gene.type[ ,"type"]))
getPalette = colorRampPalette(brewer.pal(10, "RdYlBu"))

# Reformat tiles for multiple hits/mutations
dt <- data.table(unique(case.gene.type))
dt$case <- as.character(dt$case)
dt$gene <- as.character(dt$gene)
dt[, var1 := (match(gene, gene.order$gene))]
dt[, var2 := match(case, sample.order$case)]
dt[, shift := (1:(.N))/.N - 1/(2 * .N) - 1/2, by=list(var1, var2)]
dt[, height := 1/.N, by = list(var1, var2)]
dt$type = factor(dt$type, levels = unique(dt$type))


colourCount = length(unique(dt$type))
getPalette = colorRampPalette(brewer.pal(10, "RdYlBu"))


ggplot.obj <- dt %>% 
  mutate(case = fct_reorder(case, n, .desc = TRUE )) %>%
  ggplot(aes(var2, y = var1 + shift, fill = type, height = height)) + 
  geom_tile(color = "white", size = 0.5) + 
  scale_x_continuous(breaks = seq(1:length(sample.order$case)), labels = sample.order$case, expand = c(0, 0)) + 
  scale_y_reverse(breaks=seq(1:length(gene.order$gene)), labels = gene.order$gene)  + 
  theme_bw() + 
  theme(axis.text.x = element_text(angle = 90,hjust = 1, color = "black"))+
  coord_fixed() +  
  theme(axis.text.y =element_text(colour ="black"), axis.ticks=element_line(size=0.1), plot.background=element_blank(), panel.border=element_blank())+
  scale_fill_manual(values = getPalette(colourCount))+
  labs(x = "", y = "")+ theme(legend.position = "bottom") +
  theme(legend.direction = "horizontal",legend.justification="center") +
  theme( axis.line = element_line(colour = "black", size = 0.2, linetype = "solid"))

ggsave("~/plots/oncoplot_funccall.pdf", plot=ggplot.obj,width=15, height=5, device="pdf")
