#install.packages("dplyr")
#install.packages("ggplot2")
#install.packages("gganimate")
#install.packages("gifski")
library(dplyr)
library(ggplot2)
library(gganimate)
library(gifski)

preprocessing <- function(df){
  # Función preprocessing(), la cual sirve para darle el formato de acuerdo a los años desde que los juegos se encuentran disponibles 
  df1 <- as.data.frame(seq(min(games$Year), max(games$Year)))
  # Se diseña un df que abarca la cantidad de años desde el primer juego disponible 
  colnames(df1) <- "Years"
  
  for(i in seq(df1$Years)){
    df1[i, "Rank"] <- df$Rank
    df1[i, "Name"] <- df$Name
    # Se adiciona el rango y el nombre al nuevo dataframe 
    
    # Vamos a hacer una resta de la cantidad de tiempo desde que el juego se lanzo a la venta 
    # hasta el último año disponible en el dataframe. Este nos ayudara a poder hacer la diferencia 
    # para poder agregar una cantidad especifica de ventas por año
    if (max(df1$Years) != df$Year){
      difference <- max(df1$Years) - df$Year
    } else {
      difference <- max(df1$Years) # En el caso que el año que se lanzo el juego es el mismo 
      # que el último disponible en el dataframe se asigna este 
    }
    
    # Comparativa que permite asignar la cantidad de copias vendidas por año 
    if(as.numeric(df1[i, "Years"]) < as.numeric(df$Year)){
      df1[i, "TotalShipped"] <- 0 # Años en que el juego aun no se lanza se asigna 0
    } else if(as.numeric(df1[i, "Years"]) == as.numeric(df$Year)) {
      # Años en que lanza el juego y adelante se asigna una proporción de ventas del juego 
      a <- df$Total_Shipped / difference # Se divide la cantidad completa de juegos entre la diferencia 
      df1[i, "TotalShipped"] <- a # Al primer año se asigna el resultado de la división
    } else if(as.numeric(df1[i, "Years"]) > as.numeric(df$Year)) {
      df1[i, "TotalShipped"] <- a + df1[i - 1, "TotalShipped"] # A los resultados en adelante se asigna la suma de los anteriores 
    }
  }
  return(df1)
}
assign_rank <- function(df){
  # Loops diseñados con el fin de asignar el rango de acuerdo a la cantidad máxima de juegos 
  # disponibles en cada uno de los años 
  
  # For disponible para asignar el Rank == 1 en cada uno de los años 
  for(i in levels(df$Years)) {
    b <- df %>% filter(Years == i)
    df$Rank[which(df$Name == b$Name[which(b$TotalShipped == max(b$TotalShipped))]
                  & df$Years == i)] <- 1
  }
  
  # For disponible para asignar el Rank == 2 en cada uno de los años 
  for(i in levels(df$Years)) {
    b <- df %>% filter(Years == i & Rank != 1)
    df$Rank[which(df$Name == b$Name[which(b$TotalShipped == max(b$TotalShipped))]
                  & df$Years == i)] <- 2
  }
  
  # For disponible para asignar el Rank == 3 en cada uno de los años 
  for(i in levels(df$Years)) {
    b <- df %>% filter(Years == i & Rank != 1 & Rank != 2)
    df$Rank[which(df$Name == b$Name[which(b$TotalShipped == max(b$TotalShipped))]
                  & df$Years == i)] <- 3
  }
  
  # For disponible para asignar el Rank == 4 en cada uno de los años 
  for(i in levels(df$Years)) {
    b <- df %>% filter(Years == i & Rank != 1 & Rank != 2 & Rank != 3)
    df$Rank[which(df$Name == b$Name[which(b$TotalShipped == max(b$TotalShipped))]
                  & df$Years == i)] <- 4
  }
  
  # For disponible para asignar el Rank == 5 en cada uno de los años 
  for(i in levels(df$Years)) {
    b <- df %>% filter(Years == i & Rank != 1 & Rank != 2 & Rank != 3 & Rank != 4)
    df$Rank[which(df$Name == b$Name[which(b$TotalShipped == max(b$TotalShipped))]
                  & df$Years == i)] <- 5
  }
  
  # For disponible para asignar el Rank == 6 en cada uno de los años 
  for(i in levels(df$Years)) {
    b <- df %>% filter(Years == i & Rank != 1 & Rank != 2 & Rank != 3 & Rank != 4
                       & Rank != 5)
    df$Rank[which(df$Name == b$Name[which(b$TotalShipped == max(b$TotalShipped))]
                  & df$Years == i)] <- 6
  }
  
  # For disponible para asignar el Rank == 7 en cada uno de los años 
  for(i in levels(df$Years)) {
    b <- df %>% filter(Years == i & Rank != 1 & Rank != 2 & Rank != 3 & Rank != 4
                       & Rank != 5 & Rank != 6)
    df$Rank[which(df$Name == b$Name[which(b$TotalShipped == max(b$TotalShipped))]
                  & df$Years == i)] <- 7
  }
  
  # For disponible para asignar el Rank == 8 en cada uno de los años 
  for(i in levels(df$Years)) {
    b <- df %>% filter(Years == i & Rank != 1 & Rank != 2 & Rank != 3 & Rank != 4
                       & Rank != 5 & Rank != 6 & Rank != 7)
    df$Rank[which(df$Name == b$Name[which(b$TotalShipped == max(b$TotalShipped))]
                  & df$Years == i)] <- 8
  }
  
  # For disponible para asignar el Rank == 9 en cada uno de los años 
  for(i in levels(df$Years)) {
    b <- df %>% filter(Years == i & Rank != 1 & Rank != 2 & Rank != 3 & Rank != 4
                       & Rank != 5 & Rank != 6 & Rank != 7 & Rank != 8)
    df$Rank[which(df$Name == b$Name[which(b$TotalShipped == max(b$TotalShipped))]
                  & df$Years == i)] <- 9
  }
  
  # For disponible para asignar el Rank == 10 en cada uno de los años 
  for(i in levels(df$Years)) {
    b <- df %>% filter(Years == i & Rank != 1 & Rank != 2 & Rank != 3 & Rank != 4
                       & Rank != 5 & Rank != 6 & Rank != 7 & Rank != 8 & Rank != 9)
    df$Rank[which(df$Name == b$Name[which(b$TotalShipped == max(b$TotalShipped))]
                  & df$Years == i)] <- 10
  }
  
  return(df)
}
sv_anim <- function(data, name){
  final_animation <- animate(data, 100,fps = 20,duration = 30, width = 950,
                             height = 750, renderer = gifski_renderer())
  assign("final_animation", final_animation, envir = globalenv())
  filename <- getwd()
  filename <- paste(filename, "/", name, ".gif", sep = "")
  anim_save(filename, animation=final_animation)
}

### Fase 1: Asignar la lectura del documento .csv  
games <- read.csv("complete_vgchartz.csv")

# Se selecciona ciertas columnas con las que se desean trabajar 
games <- games %>% select(Rank, Name, Total_Shipped, Year)

# Esta es una pequeña trampa por que de acuerdo VGChartz "Call of Duty" y "Gran Theft Auto" 
# tienen la misma cantidad de ventas. Asignamos que "Call of Duty" tenga más copias vendidas
games$Total_Shipped[which(games$Name == "Call of Duty")] <- as.numeric(300.10)
games$Rank <- rep(0, length(games$Rank)) # Se asigna un formato de Rango que todos sean 0, se les asignara por ventas proximamente

### Fase 2: Formato de un df con el fin de trabajar correctamente con gganimate 

# Realizar un dataframe que incluya todos los años desde la venta inicial del juego 
gamesdb <- as.data.frame(NULL) # Se crea el dataframe vacio  

# Este loop toma el indexado individual de cada uno de los juegos 
for(i in seq(games$Name)){
  game <- games[i,] # Esta fila del juego indiviual es el que se usa como base para la siguiente función
  a <- preprocessing(game) # Se asigna el resultado de la función a a 
  gamesdb <- rbind(gamesdb, a) # Se une los resultados en el dataframe "gamesdb"
}

# Se cambia la clase de "Years" de numerico a factor, con el fin de poder conseguir los niveles
gamesdb$Years <- as.factor(gamesdb$Years)
gamesdb <- assign_rank(gamesdb) # Se reassigna el resultado de la función 

# Se realiza un filtrado final con el fin de solo obtener los juegos que en algún momento 
# se encontraban en el Top 10, eliminando los años en que no se encontraban a la venta 
finalgame <- gamesdb %>% filter(Rank >= 1 & TotalShipped != 0)

### Fase 3: Construcción del Plot Estático 
p <- ggplot(data = finalgame, aes(x = Rank, group = as.character(Name), 
                             color = Name, fill = Name)) +
    # geom_tile() para generar el histograma 
    geom_tile(aes(y = TotalShipped/2, height = TotalShipped,
                width = 0.9), alpha=0.8, color = NA) + 
    geom_text(aes(y = 0, label = paste(Name, "")), vjust = 0.2, hjust = 1) + 
    # coor_flip() para voltear el eje del gráfico 
    coord_flip(clip = "off", expand = TRUE) + 
    # scale_y_continous permite asignar que los titulos sigan el valor de la escala 
    scale_y_continuous(labels = scales::comma) +
    # scale_x_reverse para voltear 180° el inicio del eje X
    scale_x_reverse() + 
    guides(color = FALSE, fill = FALSE) +
    # elimina el formato del eje X y eje Y que se establece en el plot estático 
    theme_minimal() + 
    # formato de los titulos del gráfico 
    theme(
      plot.title=element_text(size=20, hjust=0.5, face="bold", colour="grey", vjust=-1),
      plot.subtitle=element_text(size=18, hjust=0.5, face="italic", color="grey"),
      plot.caption =element_text(size=8, hjust=0.5, face="italic", color="grey"),
      axis.ticks.y = element_blank(), 
      axis.text.y = element_blank(),
      axis.title.y = element_blank(), 
      plot.margin = margin(1, 1, 1, 4, "cm")
    )
p

### Fase 4: Construcción del Plot Dinámico 
# Se usa de base el plot estático 
plt <- p + 
  # La función transition_states() permite que se realice la animación
  transition_states(states = Years, transition_length = 4, state_length = 1) +
  # Permite establece el formato cuadrático de los aes del plot estático 
  ease_aes("cubic-in-out") + 
  # Estable los titulos de cada uno de los objetos del gráfico 
  labs(title = "Top 10 Most Sucessful Videogames : {closest_state}", 
       subtitle = "Millions Units Sold",
       caption = "Sorce: VGChartz",
       y = "Total Copies Sold")

plt

### Fase 5: Guardar la animación
# Los argumentos son el plot dinámico y el nombre que se quiere asignar a la animación 
sv_anim(plt, "vgchartzcomplete")
