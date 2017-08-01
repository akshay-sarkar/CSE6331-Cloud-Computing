#
# This is the server logic of a Shiny web application. You can run the 
# application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#
library("ggplot2")
#library("cluster")
library(shiny)

# Define server logic required to draw a histogram
shinyServer(function(input, output) {
  
  output$distPlot <- renderPlot({
    no_cluster <- input$bins
    
    file_csv <- read.csv("C:/Assignemnt-5/data2.csv")
    #plot(age ~ height, file_csv)
    #Eliminating Unnecssary columns from CSV 
    tableFromCSV <- file_csv[,-c(1,3,4,5,6,7,8,9)]
    print(tableFromCSV)
    #For normalizing
    tableFromCSV_Scaled <- scale(tableFromCSV)
    set.seed(42)
    # K- Means Algorithm
    clusterData <- kmeans(tableFromCSV, no_cluster, nstart = 30)
    # Creating Table 
    # ggplot(file_csv=tableFromCSV) + geom_bar(mapping = aes(x= age))
    
    
    #plotting Cluster
    plot(tableFromCSV[c("House","District")], col=clusterData$Size, pch = 5, main="Clustering")
    points(clusterData$centers, pch = 4, cex = 3, lwd =2,  col="blue")
    lines(clusterData$centers, col="black", lwd = 2)
    
    
    print(clusterData)
    #NOrmalizarion for distance betweeen
    
    # m <- apply(tableFromCSV, 2, mean)
    # s <- apply(tableFromCSV, 2, sd)
    # z <- scale(tableFromCSV, m, s)
    # 
    # distance <- dist(z)
    
    #centroids <- aggregate(age~height,tableFromCSV,mean)
    
    #ggplot(tableFromCSV, aes(age, height,color=clusterData$cluster))+ 
    #  geom_point(file_csv=centroids, size = 5)+ geom_point(size=3)
    
    #clusplot(tableFromCSV, clusterData$cluster, color=TRUE, shade=TRUE, main="Cusplot",
    #         labels = 0, xlab = "Height", ylab = "Age", xlim=c(-60,70), ylim = c(-40,50))
  })
  
  output$distPlot1 <- renderPlot({

    no_cluster <- input$bins
    file_csv <- read.csv("C:/Assignemnt-5/data2.csv")
    #plot(age ~ height, file_csv)
    tableFromCSV <- file_csv[,-c(1,3,4,5,6,7,8,9)]

    library(factoextra)

    #For normalizing
    tableFromCSV_Scaled <- scale(tableFromCSV)
    set.seed(42)
    clusterData <- kmeans(tableFromCSV, no_cluster, nstart = 30)

    #Finding Optimal Cluster Value
    #fviz_nbclust(tableFromCSV, method = "wss", FUNcluster = kmeans) +
    # geom_vline(xintercept = 5, linetype = 3)


    # barplot(clusterData$size, horiz=TRUE,
    #         names.arg = clusterData$cat,
    #         beside = TRUE,legend.text = TRUE,
    #         main = "Bar Graph",
    #         xlab = "Size", ylab = "Clusters",
    #         args.legend = list(x = "topleft", bty="n"))
    
    pie(clusterData$size, main="Pie Chart of Countries")
  })

 
  output$timeTORun <- renderUI({
    no_cluster <- input$bins
    str2 <- ""
    str1 <- paste("There are ", no_cluster, " Cluster")
    #Start Time
    start.time <- Sys.time()

    file_csv <- read.csv("C:/Assignemnt-5/data2.csv")
    tableFromCSV <- file_csv[,-c(1,3,4,5,6,7,8,9)]

    #For normalizing
    tableFromCSV_Scaled <- scale(tableFromCSV)
    set.seed(42)
    clusterData <- kmeans(tableFromCSV, no_cluster, nstart = 30)

    #Time Calculate
    end.time <- Sys.time()
    time_taken <- end.time - start.time
    print(time_taken)
    str1 <- paste(str1, ", <br> Time Taken",  time_taken, " ,<br> Each Cluster Size : ", clusterData$size)

    #j<-0

    #Calculate Distance Between Centriods
    ##barplot(clusterData$centers, main="Car Distribution", xlab="Number of Gears")
    # for (i in 1:no_cluster){
    #   k <- i+1
    #   if(!( k>no_cluster))
    #     for( j in k:no_cluster){
    #       #paste("Cluster Size = ",i, j)
    #       #myDist( clusterData$centers )
    #       m <- i+no_cluster
    #       p <- j+no_cluster
    #       t <- sqrt( (clusterData$centers[i]-  clusterData$centers[j])^2 +(clusterData$centers[m]-  clusterData$centers[p])^2)
    #
    #       str2 <- paste(str2, "Cluster ",i,":", j," has distance ", t,"<br>", sep=" ")
    #     }
    # }

    HTML(paste(str1,  sep = '<br/>'))
  })

  output$tableCentriod <- renderDataTable({
    no_cluster <- input$bins
    file_csv <- read.csv("C:/Assignemnt-5/data2.csv")
    tableFromCSV <- file_csv[,-c(1,3,4,5,6,7,8,9)]
    clusterData <- kmeans(tableFromCSV, no_cluster, nstart = 30)

    clusterData$centers
  })

  output$tablePoint <- renderDataTable({
    no_cluster <- input$bins
    h1 <- input$caption_House
    d1 <- input$caption_District
    print(h1[1])
    
    library(data.table)
    file_csv <- fread("C:/Assignemnt-5/data2.csv", select = c(h1,d1))

    #file_csv <- read.csv("C:/Assignemnt-5/data2.csv")
    
    # file_csv <- read.csv(file = "C:/Assignemnt-5/data2.csv", sep = " ")[ ,c(h1, d1)]
    #print(file_csv)
    
    #tableFromCSV <- file_csv[,-c(1,3,4,5,6,7,8,9)]

    clusterData <- kmeans(file_csv, no_cluster, nstart = 30)
    # 
     # Showing Cluster
     out <- cbind(file_csv, clusterNum = clusterData$cluster)
     out
  })
})