# @effiehan 
# https://github.com/StoreyLab/fFDR
# install.packages("devtools")
# library("devtools")
# devtools::install_github("StoreyLab/fFDR")

combo<- read.csv(file='/Users/effiehan/Desktop/term4/swsc/fdr_ratios/cov/combo.csv')
p_value<-combo$p
z<-combo$rsquare
library(fFDR)
fq <- fqvalue(p_value, z)
fqvalues <- fq$table$fq.value
dd<-which(fqvalues < .1)
write.csv(dd, file = '/Users/effiehan/Desktop/term4/swsc/fdr_ratios/ffdr/rsquare.csv', row.names = FALSE)

z<-combo$fund_size
library(fFDR)
fq <- fqvalue(p_value, z)
fqvalues <- fq$table$fq.value
dd<-which(fqvalues < .1)
write.csv(dd, file = '/Users/effiehan/Desktop/term4/swsc/fdr_ratios/ffdr/fund_size.csv', row.names = FALSE)


z<-combo$fund_flow
library(fFDR)
fq <- fqvalue(p_value, z)
fqvalues <- fq$table$fq.value
dd<-which(fqvalues < .1)
write.csv(dd, file = '/Users/effiehan/Desktop/term4/swsc/fdr_ratios/ffdr/fund_flow.csv', row.names = FALSE)


z<-combo$sharp
library(fFDR)
fq <- fqvalue(p_value, z)
fqvalues <- fq$table$fq.value
dd<-which(fqvalues < .1)
write.csv(dd, file = '/Users/effiehan/Desktop/term4/swsc/fdr_ratios/ffdr/sharp.csv', row.names = FALSE)


z<-combo$return_gap
library(fFDR)
fq <- fqvalue(p_value, z)
fqvalues <- fq$table$fq.value
dd<-which(fqvalues < .1)
write.csv(dd, file = '/Users/effiehan/Desktop/term4/swsc/fdr_ratios/ffdr/return_gap.csv', row.names = FALSE)

z<-combo$treynor
library(fFDR)
fq <- fqvalue(p_value, z)
fqvalues <- fq$table$fq.value
dd<-which(fqvalues < .1)
write.csv(dd, file = '/Users/effiehan/Desktop/term4/swsc/fdr_ratios/ffdr/treynor.csv', row.names = FALSE)

z<-combo$beta
library(fFDR)
fq <- fqvalue(p_value, z)
fqvalues <- fq$table$fq.value
dd<-which(fqvalues < .1)
write.csv(dd, file = '/Users/effiehan/Desktop/term4/swsc/fdr_ratios/ffdr/beta.csv', row.names = FALSE)

z<-combo$vol
library(fFDR)
fq <- fqvalue(p_value, z)
fqvalues <- fq$table$fq.value
dd<-which(fqvalues < .1)
write.csv(dd, file = '/Users/effiehan/Desktop/term4/swsc/fdr_ratios/ffdr/vol.csv', row.names = FALSE)

