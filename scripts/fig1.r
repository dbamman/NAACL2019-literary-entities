library(ggplot2)
library(reshape2)

data=read.table("../results/fig1.dists.txt", header=TRUE)
melted=melt(data, id.vars="type", variable.name="Data")
melted$type<- factor(melted$type, levels=c("PER", "GPE", "ORG", "FAC", "LOC", "VEH"))
melted$Model<- factor(melted$Data, levels=c("ACE", "Literature"),  labels=c("ACE", "Literature") )

dodge=position_dodge(width=0.5)

ggplot(melted, aes(x=type, y=value, fill=Data)) + geom_bar(width=0.5, position=dodge, colour='black', stat="identity") + ylab("frequency") + xlab("") + scale_fill_manual(values=alpha(c("#59BAF2", "#0000FF"),0.5), labels=c("ACE    ", "Literature")) + theme(text=element_text(size=15), axis.title.y=element_text(margin = margin(t = 0, r = 20, b = 0, l = 0)),  legend.position="top",legend.title=element_blank())