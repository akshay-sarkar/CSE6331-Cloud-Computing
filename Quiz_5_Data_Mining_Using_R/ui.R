#
# This is the user-interface definition of a Shiny web application. You can
# run the application by clicking 'Run App' above.
#
# Find out more about building applications with Shiny here:
# 
#    http://shiny.rstudio.com/
#

library(shiny)

# Define UI for application that draws a histogram
shinyUI(fluidPage(
  
  # Application title
  titlePanel("Akshay Sarkar - 1001506793 "),
  
  textInput("caption_House", "House", "House"),
  
  textInput("caption_District", "District", "District"),
  
  # Sidebar with a slider input for number of bins 
  sidebarLayout(
    sidebarPanel(
      sliderInput("bins",
                  "Number of bins:",
                  min = 1,
                  max = 20,
                  value = 6)
    ),
    
    # Show a plot of the generated distribution
    mainPanel(
      # textOutput("txt1"),
      #plotOutput("distPlot"),
      plotOutput("distPlot1"),
      h3("Cluster Data"),
      htmlOutput("timeTORun"),
      h3("Centroid Part"),
      dataTableOutput("tableCentriod"),
      h3("Cluster Points"),
      dataTableOutput("tablePoint")
    )
  )
))
