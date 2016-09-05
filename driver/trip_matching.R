library(dplyr)
setwd('/Users/Kay/Github/Z-T_Statistics/driver')
drivers = list.files("drivers")
driver = drivers[1]
driver_files <- list.files(path = paste("./drivers/",driver,sep=""))

for (file in driver_files){
	coord <- as.matrix(read.csv(paste("./drivers/",driver[1],"/", file, sep="")))
}




setwd("/Users/Kay/Github/Z-T_Statistics/driver")

library(dplyr)
library(doParallel)
cl <- makeCluster(1)
registerDoParallel(cores=3)

dataDir <- "drivers/"
drivers <- list.files(dataDir)
# For selecting a range of drivers
lowBound = 1
highBound = 1

runTime<-system.time({


similarTrips<-foreach(driver=drivers[lowBound:highBound],.combine=rbind) %dopar%{
  load(paste0(dataDir,driver))
  driverID<-gsub(driver,pattern="DriverData",replacement="")
  test<-drives %>%
    group_by(tripID) %>%
    mutate(x = x, y = y,
           r=sqrt(x^2+y^2),
           alpha=atan2(last(y),last(x))-atan2(y,x),
           rot.x=r*cos(alpha),
           rot.y=r*sin(alpha),
           rows=n(),
           rot.x.flip=ifelse(sum(rot.x<0)>floor(rows/2), -rot.x, rot.x),
           rot.y.flip=ifelse(sum(rot.y<0)>floor(rows/2), -rot.y, rot.y)
    )%>%
    select(tripID,rot.x=rot.x.flip,rot.y=rot.y.flip)
  mini2<-NULL
  # begin a nested loop to check all UNIQUE combinations of trips
  for(i in 1:199){
    focus<-select(test[test$tripID==i,],foc.x=rot.x,foc.y=rot.y)
    mini1<-NULL
    for(k in (i+1):200) {
      compare<-select(test[test$tripID==k,], cmp.x=rot.x, cmp.y=rot.y)
      # Necessary to only check trips that are even close to the same footprint (thanks to Jiayi Liu aka. JSon for the idea)
      if(!(diff(range(focus$foc.x))<0.8*diff(range(compare$cmp.x))) &
           !(diff(range(compare$cmp.x))<0.8*diff(range(focus$foc.x))) &
           !(diff(range(focus$foc.y))<0.8*diff(range(compare$cmp.y))) &
           !(diff(range(compare$cmp.y))<0.8*diff(range(focus$foc.y)))
      ){

        trimLength<- min(nrow(compare),nrow(focus)) # Trimming instead of imputing values (Tim's suggestion) improves speed by 10%, catches more true positives
        
        focusTrim<-focus[1:trimLength,]#%>%
#           transmute(r.foc=sqrt(foc.x^2+foc.y^2)) # Option to use distance of point to origin
        
        compareTrim<-compare[1:trimLength,]#%>%
#           transmute(r.cmp=sqrt(cmp.x^2+cmp.y^2)) # Option to use distance of point to origin
        
        eqDistMat<-rbind(focusTrim$foc.y,compareTrim$cmp.y)
        mini1<-rbind(mini1,
                     data.frame(driver=driverID, tripA=i,tripB=k,
                  # this is the euclidian distance between y values of both curves
                  # it was necessary to normalize the result: trips with larger x and y values had higher euclidian distances
                  # I chose to normalize by the average "footprint" of the two trips
                   eucDist=unlist(as.numeric(dist(eqDistMat)))/mean(c(max(focusTrim$foc.y),max(compareTrim$cmp.y)))
                  ))
      } # end if loop
    } # end comparison loop
    mini2<-rbind(mini2,mini1)
  } # end focus loop
  mini2
}
})


outputFileName = paste0('similarTrips-y_',lowBound,'_',highBound)
save(similarTrips,file=outputFileName)


require(data.table)

setwd("/Users/Kay/Github/Z-T_Statistics/driver")
# Use fread from the data.table package to read in x and y coords
# Apply trip ID to new third column in data frame
fread_modify <- function(file.number, driver) {
  tmp <- fread(paste0("drivers/",driver,"/",file.number,".csv"), header=T, sep=",")
  tmp[, tripID:=file.number]
  return(tmp)
}

  
# Pull down list of driver directories and create a home for binaries
driverlist <- list.files("./drivers/")
dir.create("./data/", showWarnings = TRUE, recursive = FALSE, mode = "0777")

# Loop through the driver list and use rbindlist to bind data from
# x, and y columns to the specific driver data frame
for (i in 1:length(driverlist)) {
  onedriver <- driverlist[i]
  drives <- rbindlist(lapply(1:200, fread_modify, onedriver))
  save(drives, file = paste('./data/DriverData',onedriver, sep=''))
}


read_trips = function(x){
  setwd(x)
  dir_list = list.files(x)
  dir_list = dir_list[grep('[[:alpha:]]{0,3}.csv', dir_list)]
  num_files = length(dir_list)
  files = lapply(dir_list, read.csv)
  idx = unlist(lapply(files, nrow))
  trip = rep(1:num_files, idx)
  files = do.call(rbind, files)
  time = unlist(sapply(idx, function(x) seq(from=1, to=x, by=1)))
  files = cbind(files, trip, time)
  }

driverOne = read_trips("drivers/1")

require(ggplot2)
require(plyr)
require(dplyr)

driverOne$dist = sqrt(driverOne$x^2+driverOne$y^2)

png('/Users/Kay/Github/Z-T_Statistics/driver/driver1.png')
ggplot(data = driverOne, aes(x=x,y=y, group=trip, color='red', label=trip))+geom_path()+theme_bw()+xlab('')+ylab('')+theme(legend.position='none')+ 
      ggtitle('Trips by Driver 1')
dev.off()

selected_trip = c(7,34,36,57,77,79,80,81,91,111,139,142,155,186,190,196)
selected_trip = c(17,31,33,43,46,60,68,76,86,91,129,139,154,160,170,182)
png('/Users/Kay/Github/Z-T_Statistics/driver/driver1_sem.png')
ggplot(data = driverOne_rot[driverOne_rot$trip %in% selected_trip,], aes(x=x,y=y, group=trip, color='red', label=trip))+geom_path()+theme_bw()+xlab('')+ylab('')+theme(legend.position='none')+ 
      ggtitle('Trips by Driver 1')

ggplot(data = driverOne_rot[driverOne_rot$trip ==i,], aes(x=x,y=y, group=trip, color='red', label=trip))+geom_path()+theme_bw()+xlab('')+ylab('')+theme(legend.position='none')+ 
      ggtitle('Trips by Driver 1')
print(i)
i = i+1


par(mfrow = c(5, 5))
for (i in 176:200){
	temp = driverOne_rot[driverOne_rot$trip == i,]
	plot(temp[,1],temp[,2],type = "l",col = "red",xlab = i)
}


temp = driverOne_rot[driverOne_rot$trip == 1,]
last = driverOne[nrow(driverOne),]


  test<-drivesOne %>%
    group_by(trip) %>%
    mutate(x = x, y = y,
           r=sqrt(x^2+y^2),
           alpha=atan2(last(y),last(x))-atan2(y,x),
           rot.x=r*cos(alpha),
           rot.y=r*sin(alpha),
           rows=n(),
           rot.x.flip=ifelse(sum(rot.x<0)>floor(rows/2), -rot.x, rot.x),
           rot.y.flip=ifelse(sum(rot.y<0)>floor(rows/2), -rot.y, rot.y)
    )%>%
    select(trip,rot.x=rot.x.flip,rot.y=rot.y.flip)




temp2 = test[test$trip == 1,]
plot(temp[,2],temp[,2],type = "l",col = "red")


ggplot(data=filter(driverOne_rot,(trip %in% selected_trip)))+geom_point(aes(x=x,y=y,color=trip),size=1)+
facet_wrap(~ trip,scales="free")+theme_bw()+theme(legend.position="none")
