data = read.csv('all-days.csv', header=FALSE, col.names=c('Date','Count'))

barplot(data$Count)
hist(data$Count, breaks=25, xlim=(c(20, 180)))
boxplot(data$Count, outline=FALSE)
