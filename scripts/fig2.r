library(ggplot2)

orig=read.table("~/fig2.labeldist.txt", header=TRUE)
data=data.frame(orig)
data$type<- factor(data$type, levels=c("PER", "GPE", "ORG", "FAC", "LOC", "VEH"))

dodge=position_dodge(width=0.5)

ggplot(data, aes(x=data$type, y=data$value, fill=data$Data)) + geom_bar(width=0.5, position=dodge, colour='black', stat="identity") + ylab("F-score") + xlab("") + ylim(0,80) + scale_fill_manual(values=alpha(c("#59BAF2", "#0000FF", "#FFFFFF"),0.5), labels=c("ACE    ", "Literature")) + theme(text=element_text(size=15), axis.title.y=element_text(margin = margin(t = 0, r = 20, b = 0, l = 0)), legend.position="top", legend.title=element_blank()) + geom_errorbar(aes(ymin=data$ymin, ymax=data$ymax), position=dodge, width=0.25)