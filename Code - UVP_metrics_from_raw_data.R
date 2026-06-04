## From Underwater Vision Profiler 6 (UVP6) raw data to ecological metrics for Marine Conservation Areas monitoring
## (C) Laure Vilgrain, Andéol Bourgouin 
## January 2026


# Aim of the script ----
# The aim of this script is to compute metrics that could be routinely measured during marine conservation programs 
# from UVP deployment. They request minimal post-processing of raw data while providing meaningful ecological information 
# on pelagic ecosystems (productivity, structure, biodiversity)


# Statement ---- 
# The metrics computed here will undoubtedly provide valuable insights into pelagic ecosystems. 
# However, they have not been produced by a scientific consortium and should therefore be used with caution. 
# Further studies would be beneficial to validate their relevance and use. 


# Libraries ----
library(readr)      # To read the initial dataset
library(tidyverse)  # To manipulate datasets
library(ggrepel)    # To label stations in maps
library(patchwork)  # To create patchworks of several graphs
library(FactoMineR) # To compute PCA
library(factoextra) # To analyse PCA
library(vegan)      # To compute diversity index

# Download Exotaxa and Ecopart raw data ----
# -> see the guide "Use Ecotaxa and Ecoport to export data"
# The Ecotaxa dataset will be named taxa_db_raw and then modified into taxa_db in this code
# The Ecopart dataset will be named part_db_raw and then modified into part_db in this code

# Read raw data ----
taxa_db_raw <- read_delim("data/ecotaxa_hawkechannel_30jan.tsv", 
                          delim = "\t", escape_double = FALSE, 
                          locale = locale(), trim_ws = TRUE)

part_db_raw <- read_delim("data/ecopart_hawkechannel_30jan.tsv", 
                          delim = "\t", escape_double = FALSE, 
                          locale = locale(encoding = "WINDOWS-1252"), 
                          trim_ws = TRUE)

coast <- read_csv("data/ref/world_coast.csv.zip")          |> # coasts lines for maps
  rename(lon=long)                                     |>
  filter(lon < -50 & lon > -67 & lat > 50 & lat < 61)     # adapt the lat and lon for the MCA of interest

cols <- c("#263B50", "#577590", "#4d908e", "#43aa8b", "#90be6d", "#f9c74f", "#f8961e", "#f3722c", "#f94144")


# Clean Ecotaxa raw data ----

## Extract important information
image_pixelsize <- unique(taxa_db_raw$acq_pixel) # in microns, example: 73 microns for this UVP
image_volume <- unique(taxa_db_raw$acq_volimage) # in liters, example: 0.53L for this UVP

## Select and rename the most useful columns
taxa_db <- taxa_db_raw %>% select(cruise = sample_cruise, ship = sample_ship, station = sample_stationid, sample_id, lat = object_lat, lon = object_lon, date = object_date, 
                                  time = object_time, object_id, depth = object_depth_min, status = object_annotation_status, category = object_annotation_category, 
                                  hierarchy = object_annotation_hierarchy, ctd_filename = sample_ctdrosettefilename)

## Create a datable with morphological information about each particule image
taxa_morpho_db <- taxa_db_raw %>% 
  select(station = sample_stationid, sample_id, lat = object_lat, 
  lon = object_lon, object_id, category = object_annotation_category, 
  depth = object_depth_min, object_area:object_skeleton_area)

## Check the number of casts (= samples)
length(unique(taxa_db$sample_id)) # -> example: 30 casts for the project Hawke Channel 2024



# Clean Ecopart raw data ----

## Select and rename the most useful columns
part_db <- part_db_raw %>% 
  select(sample_id = Profile, ecopart_project_name = Project, depth_bin = `Depth [m]`, 
  sampled_volume = `Sampled volume [L]`, `LPM (1-2 µm) [# l-1]`: `LPM biovolume (>16.4 mm) [mm3 l-1]` ) %>% 
  left_join(distinct(taxa_db, sample_id, station, lat, lon)) %>% 
  ungroup() %>% 
  select(sample_id, ecopart_project_name, station, lat, lon, depth_bin, everything())

## Check if sample number is the same than Ecotaxa database
length(unique(part_db$sample_id)) # -> 30, same than Ecotaxa data 

## Clean R space
remove(taxa_db_raw, part_db_raw)


# Add sampled volume to Ecotaxa data from Ecopart data ----

## Create round function
round_any <- function (x, accuracy, f=round){
  f(x/accuracy) * accuracy
}

## Compute depth-bins on taxa_db  
taxa_db <- taxa_db %>% 
  # compute depth bin
  mutate(depth_bin=round_any(depth, 5, floor)+2.5)

## Left join to get sample volume
taxa_db <- taxa_db %>% 
  left_join(select(part_db, sample_id, depth_bin, sampled_volume)) %>% 
  # reorder columns
  select(cruise:object_id, depth, depth_bin, sampled_volume, everything())

## Plot water volume seen by the UVP according to depth bins
#taxa_db %>% ggplot()+
#  geom_boxplot(aes(x=sampled_volume, y=-depth_bin, group=depth_bin), size = 0.2, alpha = 0.1)+
#  labs(y= "Depth bin (5m)", x = "Sampled atervolume (L)")
# -> UVP6 sample 100L in each 5 meters depth-bins on average, when the rosette is going to 60m/min
# -> more organisms in the first 200m so sometimes it takes time for the camera to process images and little less images are taken, 
#    diminuishing the volume aquired. 
# -> as the rosette slow down next to the sea bottom, the sampled volume increases

# Keep only the 200 first meters for particules data ----
part_db <- part_db %>% filter(depth_bin < 200) 
# -> we keep only information on the water column above 200m to allow better
# intercomparison of shallow and deep stations






# Metric 1 - Average densities of particles per cast (#/L) ----
## Explanation: 
# Density of particles averaged in the first 200m of the depth profile.

## Calculation: 
# Sum the particles densities of different size ranges and convert it into a number of particles :
part_db <- part_db |>
  mutate( nb_tot = rowSums(across(`LPM (64-128 µm) [# l-1]`: `LPM (4.1-8.19 mm) [# l-1]`)) * sampled_volume)

# Dataframe of the averaged particles density :
part_1_dens <- part_db                                     |>
  group_by(sample_id)                   |> # regroup data per sample id
  summarise(station = first(station), 
            lat = first(lat), lon = first(lon), 
            m1_part_dens  = sum(nb_tot) / sum(sampled_volume)) |> # mean density = sum nb of particles / sum volume sampled
  mutate(sample_id = reorder(sample_id, -m1_part_dens))        # order by density for the plot


# Plot the result :
ggplot(part_1_dens, aes(x = sample_id, y = m1_part_dens))                     +
  geom_col()                                                          +
  labs(
    x    = "station ID",
    y    = "Particle average density (#.L-1)")                    +
  theme_bw()                                                          +
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5)) # present the station IDs vertically

# Export the plot :
ggsave(
  "graphs/supp_m1_dens.png", # the name
  dpi    = 400,               # the resolution
  width  = 8,
  height = 5)  


# Plot in a map :
ggplot() +
  geom_polygon(mapping=aes(x=lon, y=lat, group=group), data=coast) + # coastline
  geom_label_repel(data=part_1_dens,aes(lon, lat, label = station), 
                   segment.alpha = 0.3, size = 2.5)                 + # station labels
  geom_point(data=part_1_dens, aes(lon, lat, color = m1_part_dens), size=4)         + # stations
  scale_color_gradientn(colors = cols, name = "Density (#.L-1)") + # stations' color palette
  labs(x= "Longitude (°E)", y= "Latitude (°N)")                     +
  theme_bw() + 
  theme(legend.title = element_text(size = 10))                     + # size of legend title
  coord_quickmap(xlim=c(-57, -53), ylim = c(51.6, 54))                # map limits

# Export the plot :
ggsave(
  "./graphs/m1_map_dens.png", # the name
  dpi    = 400,                   # the resolution
  width  = 8,
  height = 7)  


# Metric 2 - Average biovolume of particles per cast (mm3/L) ----
## Explanation: Biovolume of particles averaged in the first 200m of the depth profile.

## Calculation: 
# Sum the particles biovolume per L of different size ranges and convert it into absolute biovolume :
part_db <- part_db |>
  mutate( biovol_tot = rowSums(across(`LPM biovolume (64-128 µm) [mm3 l-1]`: `LPM biovolume (4.1-8.19 mm) [mm3 l-1]`)) * sampled_volume)

# Dataframe of the averaged particles biovolume :
part_2_biovol <- part_db                                       |>
  group_by(sample_id)                                          |> # regroup data per sample id
  summarise(station = first(station), 
            lat = first(lat), lon = first(lon),
            m2_part_biovol    = sum(biovol_tot) / sum(sampled_volume)) |> # mean biovolume = sum biovolume / sum volume sampled
  mutate(sample_id = reorder(sample_id, -m2_part_biovol))              # order by density for the plot


# Plot the result :
ggplot(part_2_biovol, aes(x = sample_id, y = m2_part_biovol))                 +
  geom_col()                                                          +
  labs(
    x    = "station ID",
    y    = "Particles average biovolume (mm3.L-1)")                  +
  theme_bw()                                                          +
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5)) # present the station IDs vertically

# Export the plot :
ggsave(
  "graphs/supp_m2_biovol.png", # the name
  dpi    = 400,                 # the resolution
  width  = 8,
  height = 5)  


# Plot in a map :
ggplot() +
  geom_polygon(mapping=aes(x=lon, y=lat, group=group), data=coast) + # coastline
  geom_label_repel(data=part_2_biovol,aes(lon, lat, label = station), 
                   segment.alpha = 0.3, size = 2.5)                   + # station labels
  geom_point(data=part_2_biovol, aes(lon, lat, color = m2_part_biovol), size=4)         + # stations
  scale_color_gradientn(colors = cols, name = "Biovolume (mm3.L-1)") + # stations' color palette
  labs(x= "Longitude (°E)", y= "Latitude (°N)")                       +
  theme_bw() + 
  theme(legend.title = element_text(size = 8))                        + # size of legend title
  coord_quickmap(xlim=c(-57, -53), ylim = c(51.6, 54))                  # map limits

# Export the plot :
ggsave(
  "graphs/m2_map_biovol.png", # the name
  dpi    = 400,                   # the resolution
  width  = 8,
  height = 7)  



# Metric 3 - Slope of the relationship between particles abundances and size ----
## Explanation: The slope of the relationship between particles abundance and size is an indicator of
# ecosystem productivity. It supposes a linear relationship between the log of abundance and the log
# of size.

## Calculation: 

# Create a size spectrum dataset with the name of the size ranges, the middle value of each size ranges, and the width of the size ranges:
size_spectrum <- tibble(
  size_range = c("LPM (64-128 µm) [# l-1]", "LPM (128-256 µm) [# l-1]", "LPM (256-512 µm) [# l-1]", "LPM (0.512-1.02 mm) [# l-1]",
                 "LPM (1.02-2.05 mm) [# l-1]", "LPM (2.05-4.1 mm) [# l-1]", "LPM (4.1-8.19 mm) [# l-1]", "LPM (8.19-16.4 mm) [# l-1]"),
  middle     = c(96, 192, 384, 766, 1535, 3075, 6145, 12295), 
  size_width = c(64, 128, 256, 512, 1020, 2050, 4100, 8190))


all_id <- unique(part_db$sample_id) # vector of all the sample IDs

# Create a dataframe for the results : 
part_3_slope <- tibble(
  sample_id = all_id, 
  m3_part_slope     = NA)

megaplots <- list()

for (i in 1:length(all_id)) {
  
  temp_sample_id <- all_id[i] # select the sample id
  
  # Shape the data:
  temp_data_station <- part_db                                                              |> 
    filter(sample_id == temp_sample_id)                                                     |> # take only data of the desired sample id
    #select(sample_id, depth_bin,  `LPM (128-256 µm) [# l-1]`: `LPM (1.02-2.05 mm) [# l-1]`) |>
    select(sample_id, depth_bin,  `LPM (128-256 µm) [# l-1]`: `LPM (2.05-4.1 mm) [# l-1]`) |> # just take the densities of a certain range
    pivot_longer(cols      =  !sample_id & !depth_bin,                                         # transform data shape : the size range becomes a column
                 names_to  = "size_range",
                 values_to = "dens")                                                        |>
    inner_join(size_spectrum, by="size_range")                                              |> # merge data with the size_spectrum dataset
    mutate(dens_correct = dens / size_width)                                                |> # determine a density ponderated by the width of the size range
    filter(dens_correct > 0)                                                                   # remove data with density = 0, because it can't be used in a log function
  
  # linear regression in log:
  mod       <- lm(log(dens_correct) ~ log(middle), data = temp_data_station)
  temp_pval <- summary(mod)$coefficients[2,4] #extract p-value associated to the slope coefficient
  
  k         <- coef(mod)[2]                  # extract slope coefficient
  b         <- exp(coef(mod)[1])             # extract intercept coefficient
  
  # Verify homoscedasticity, normality and no extreme value :
  # plot(mod, which = 1)                       # residuals VS adjusted values for homoscedasticity
  # plot(mod, which = 2)                       # QQ-plot to verify normal distribution
  # plot(mod, which = 4)                       # distance de Cook
  
  # Plot the relation :
  p <- ggplot() +
    stat_function(fun = function(x) b * x^(k), linewidth = 1, color = "blue", alpha = 0.6) + # the predicted relation
    geom_point   (data = temp_data_station, aes(x = middle, y = dens_correct), alpha = 0.5) + # the observed relation
    scale_x_log10()                                                                         + # x scale in log
    scale_y_log10()                                                                         + # y scale in log
    labs(x    = "Particle size (microns)",
         y    = "Density (#.L-1)")                                                        +
    ggtitle(paste("Sample", temp_sample_id))                                                +
    theme_bw()
  
  megaplots[[i]] <- p
  
  # Add results to the results dataframe : 
  if (temp_pval < 0.05){
    part_3_slope$m3_part_slope[i] = k
  }
} 

# Create a megaplot of all the relationships :
final_plot <- wrap_plots(megaplots, ncol = 6)
ggsave("graphs/supp_m3_all_relationships.png", final_plot, width = 16, height = 20, dpi = 500, limitsize = F)

# remove variables that are now useless :
remove(size_spectrum, all_id, temp_sample_id, temp_data_station, mod, temp_pval, k, b, p, i, megaplots)

# order by density for the plot:
part_3_slope <- part_3_slope |>
  mutate(sample_id = reorder(sample_id, -m3_part_slope))             

# Lollipop plot of the result :
ggplot(part_3_slope, aes(x = sample_id, y = m3_part_slope))    +
  geom_segment( aes(xend=sample_id, y=-5, yend=m3_part_slope)) + # segment of the lollipop
  geom_point(size = 2.5)                               + # point of the lollipop
  labs(
    x    = "station ID",
    y    = "slope")                                   +
  theme_bw()                                          +
  scale_y_continuous(limits = c(-5, -2))              + # set Y limits between -5 and -2
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5)) # present the station IDs vertically

# Export the plot :
ggsave(
  "graphs/supp_m3_slope.png", # the name
  dpi    = 400,                # the resolution
  width  = 8,
  height = 5)  

# Add lat and lon
part_3_slope <- part_3_slope %>% 
  left_join(distinct(taxa_db, sample_id, station, lat, lon))

# Plot in a map :
ggplot() +
  geom_polygon(mapping=aes(x=lon, y=lat, group=group), data=coast) + # coastline
  geom_label_repel(data=part_3_slope,aes(lon, lat, label = station), 
                   segment.alpha = 0.3, size = 2.5)                + # station labels
  geom_point(data=part_3_slope, aes(lon, lat, color = m3_part_slope), size=4)      + # stations
  scale_color_gradientn(colors = cols)                            + # stations' color palette
  labs(x= "Longitude (°E)", y= "Latitude (°N)", color = "Slope")   +
  theme_bw() + 
  coord_quickmap(xlim=c(-57, -53), ylim = c(51.6, 54))               # map limits

# Export the plot :
ggsave(
  "graphs/m3_map_slope.png", # the name
  dpi    = 400,                   # the resolution
  width  = 8,
  height = 7)  


# Metric 4 - Morphological indices ----
# Explanation:a Shannon diversity index performed on variations particle morphological catergories: 
# it quantifies the equitability of particle abundances within 5 morphological clusters 
# (dark, elongated, fluffy, flakes and agglomerated particles). It is constructed by following the steps 
# outlined in Trudnowska et al. (2021), adapted so that morphological variations of new 
# images are described in relation to a fixed reference

# Calculation: 

## a. Morphological descriptors ----
## Select morphological descriptors (as in Trudnowska et al. 2021)
morpho_vars_selection <- read_delim("data/ref/morpho_vars_selection.csv", delim = ";",  #table created from information of Supp. Material from Trudnowska et al. 2021
                                    escape_double = FALSE, trim_ws = TRUE) %>% 
                                    filter(kept_Trudnowska_2021 ==TRUE)

taxa_morpho_m4 <- taxa_morpho_db %>% # create a new database because we need to keep initial descriptors before transformation
  select(station:depth, morpho_vars_selection$var) %>% # select the 24 morphological descriptors of interest (e.g. area, mean grey levels, fractal, etc)
  rename_with(
    ~ gsub("^object[_\\.]", "", .x),
    starts_with("object")) #rename them to be coherent (no "object_" in column names)

##' Clean morphological descriptors (trim extreme values,  replace extreme values by NA)
#'
#' @param x a vector
#' @param p proportion of values to remove
#' @param side on which extreme to remove values (left=low, right=high, both=...both). Can be abbreviated
trim <- function(x, p=0.001, side="right") {
  # check argument (and allow to abbreviate it)
  side <- match.arg(side, choices=c("both", "left", "right"))
  # compute quantiles
  q <- quantile(x, probs=c(p, 1-p), na.rm=T)
  # mask extreme values
  if (side == "left" | side == "both") {
    x[x < q[1]] <- NA
  }
  if (side == "right" | side == "both") {
    x[x > q[2]] <- NA
  }
  return(x)
}

## Plot  histograms of the 24 morphological descriptors
p <- gather(sample_frac(taxa_morpho_m4, 0.1), key="var", val="val", area:sr) |>
  ggplot() + geom_histogram(aes(x=val), bins=50) + facet_wrap(~var, scales="free")
ggsave(p, filename = "graphs/supp_m4_histograms_of_features.pdf", width=20, height=10)

## Transform features to have normal distributions (same transformation than in Trudnowska et al. 2021)
taxa_morpho_m4_test <- taxa_morpho_m4 |> mutate(
  area = log10(trim(area)),
  mean = trim(mean, side="left"),
  stddev = trim(stddev),
  mode = trim(mode, side="both"),
  perim. = log10(trim(perim.)),
  major = log10(trim(major)),
  circ. = trim(circ.),
  feret = log10(trim(feret)),
  intden = log10(trim(intden)),
  median = trim(median, side="left"),
  skew = trim(skew, side="both"),
  kurt = trim(kurt),
  `%area` = log1p(trim(`%area`)), 
  fractal = trim(fractal, side="both"),
  skelarea = log10(skelarea),
  slope = log10(trim(slope)), #log10 added
  symetrieh = log10(trim(symetrieh)),
  symetriev = log10(trim(symetriev)),
  thickr = log1p(trim(thickr, side="both")),
  elongation = log10(trim(elongation)),
  range = trim(range, side="both"),
  meanpos = trim(meanpos, side="left"),
  cv = trim(cv),
  sr = trim(sr, side="both")
)

## Plot all normalized histograms
p <- gather(sample_frac(taxa_morpho_m4_test, 0.1), key="var", val="val", area:sr) |>
  ggplot() + geom_histogram(aes(x=val), bins=50) + facet_wrap(~var, scales="free")
ggsave(p, filename="graphs/supp_m4_histograms_of_features_normalised.pdf", width=20, height=10)

## Eliminate extreme indviduals
## = more than 5 features are NA
n_na <- select(taxa_morpho_m4_test, area:sr) |> apply(1, function(x) {sum(is.na(x))})
taxa_morpho_m4_test <- taxa_morpho_m4_test[n_na<=5,]

## Eliminate - INF
taxa_morpho_m4_test <- taxa_morpho_m4_test %>%
  mutate(across(
    where(is.numeric),
    ~ replace(.x, is.infinite(.x), NA)
  ))

## replace NAs by the mean of the column
for (col in names(select(taxa_morpho_m4_test, area:sr))) {
  taxa_morpho_m4_test[[col]][is.na(taxa_morpho_m4_test[[col]])] <- mean(taxa_morpho_m4_test[[col]], na.rm=TRUE)
}

## Accept the final database in a new database
taxa_morpho_m4 <- taxa_morpho_m4_test


## b. Morphological space of objects = Principal Component Analysis ----

## Compute individual concentration of objects (=images) to ponderate the PCA
taxa_morpho_m4 <- taxa_morpho_m4 %>% 
  left_join(select(taxa_db, id = object_id, depth, depth_bin, sampled_volume)) %>% 
  mutate(conc= 1/sampled_volume) #this will allow that all objects have the same weight in the construction of the morphological space

## Read reference dataset to plot the reference PCA space
# -> we need a space of reference in which 5 clusters of "typical" particles groups have been defined, as in Trudnowska et al. 2021
# -> we will then project the new objects of MCA projects and assign them to clusters
morpho_diversity_ref <- read_csv("data/ref/morpho_diversity_ref.csv")

## Compute the PCA ref to check 
pcaw_ref <- PCA(
  select(morpho_diversity_ref, area:sr),
  row.w=morpho_diversity_ref$conc/sum(morpho_diversity_ref$conc), # NB: weights must be scaled to sum to 1
  graph=FALSE, ncp=4, scale.unit = TRUE)
##plot.PCA(pcaw_ref, axes = c(1, 2), choix = "var") # -> Dim. 1 - 44.86%; Dim. 2 - 19.90%; Dim.3 
##plot.PCA(pcaw_ref, axes = c(3, 4), choix = "var") # -> Dim. 3 - 12.61%; Dim. 4 - 6.10%; Dim.3 
##plot.PCA(pcaw_ref, axes = c(1, 2), choix = "ind")



## Concatenate the two dataset (ref and new) to project the new objects in the morphospace 
d_PCA <- select(morpho_diversity_ref, area:sr, conc) %>% 
  bind_rows(select(taxa_morpho_m4, area:sr, conc))

## Store the rows indices of the ref and new objects to use theses indices in PCA()
## -> new objects will be used in "ind.sup" so they do not influence the shape of the space but coordinates are created
idx_sup <- (nrow(morpho_diversity_ref) + 1):nrow(d_PCA)
idx_ref <- seq_len(nrow(morpho_diversity_ref))

## Create a weight vector of the PCA of total length, with 0 for the ind.sup
## -> this is to respect the need for the PCA() function to have weights with the same length than the
## initial dataset, but with new observation having no influence on the construction of the space
row_weights <- numeric(nrow(d_PCA))
row_weights[idx_ref] <- d_PCA$conc[idx_ref] / sum(d_PCA$conc[idx_ref])


## Perform the PCA with new objects as supplementary individuals
pcaw <- PCA(
  select(d_PCA, area:sr), #select the 24 morphological descriptors
  row.w = d_PCA$conc[idx_ref] / sum(d_PCA$conc[idx_ref]), #apply weights on references objects
  ind.sup = idx_sup, #supp objects = MCA objects
  graph = FALSE,
  ncp = 4, #4 axes kept
  scale.unit = TRUE
)


## Verification of results
## Plot the morphospace 
plot.PCA(pcaw, axes = c(1, 2), choix = "var")
plot.PCA(pcaw, axes = c(3, 4), choix = "var")
# -> all good, the same space is produced.  
nrow(pcaw$ind$coord)      == nrow(morpho_diversity_ref) # -> ok, same number than reference objects
nrow(pcaw$ind.sup$coord)  == nrow(taxa_morpho_m4) # -> ok, same number than supplementary objects

## Plot position of new objects in the morphospace
taxa_morpho_m4 <- tibble(taxa_morpho_m4, as_tibble(pcaw$ind.sup$coord)) # -> gather coordinates of supplementary objects (the ones of the MCA)

## Plot them (ref obs in black, new obs in lightblue)
ggplot()+
  geom_point(aes(x = Dim.1, y = Dim.2), data = slice_sample(morpho_diversity_ref, prop = 0.3), shape = ".", alpha = 0.8)+
  geom_point(aes(x = Dim.1, y = Dim.2), data = slice_sample(taxa_morpho_m4, prop = 0.3), color = "lightblue", shape = ".", alpha = 0.7)+
  theme_minimal() # -> well projected in the morphospace

ggplot()+
  geom_point(aes(x = Dim.3, y = Dim.4), data = slice_sample(morpho_diversity_ref, prop = 0.3), shape = ".", alpha = 0.8)+
  geom_point(aes(x = Dim.3, y = Dim.4), data = slice_sample(taxa_morpho_m4, prop = 0.3), color = "lightblue", shape = ".", alpha = 0.7)+
  theme_minimal() # -> well projected in the morphospace

## Clean R memory
remove(final_plot, d_PCA, morpho_vars_selection,pcaw,
       p, pcaw_ref,taxa_morpho_m4_test,row_weights, n_na)

## c. Assigning clusters to objects ----
## Read a dataset containing a reference for position of clusters barycenters
centers_init_ref <- read_csv("data/ref/centers_init_ref.csv") 

## Select datasets to compare (position of new objects with cluster barycenters)
centres_ref_coord <- select(centers_init_ref, Dim.1 = barycenter_dim1, Dim.2 = barycenter_dim2, Dim.3 = barycenter_dim3, Dim.4 = barycenter_dim4)  # 5 × 4: because 5 clusters and 4 dimensions
new_obs_coord <- select(taxa_morpho_m4, Dim.1, Dim.2, Dim.3, Dim.4) # coordinates of the new observations we want to assign to a cluster

# Transform them as matrices
ref_mat <- as.matrix(centres_ref_coord)   # 5 × 4
new_mat <- as.matrix(new_obs_coord)       # n_new × 4

# Compute the euclidean distance between points and barycenters (squared distances)
dist_sq <- outer(rowSums(new_mat^2), rowSums(ref_mat^2), FUN = "+") - 2 * new_mat %*% t(ref_mat)
##-> d(x,c)^2= ∑k=1to4 (xk−ck)^2; 
## with x = new_mat and c = ref_mat

## For each line, get the index of the closest barycenter
taxa_morpho_m4$cluster <- max.col(-dist_sq)  #-> cluster 1 to 5 

## Order the cluster in all our dataset according to categories given in Trudnowska et al. 2021
taxa_morpho_m4 <- taxa_morpho_m4 %>% 
  mutate(cluster_name = factor(cluster, levels = 1:5, labels = c("flakes", "dark", "agglomerated", "fluffy", "elongated"))) %>%
  mutate(cluster_name = factor(cluster_name, levels = c("dark", "elongated", "flakes", "fluffy", "agglomerated"))) #

centers_init_ref <- centers_init_ref %>%   mutate(cluster_name = factor(cluster_name, 
                                            levels = c("dark","elongated","flakes","fluffy", "agglomerated")))

morpho_diversity_ref <- morpho_diversity_ref %>%  mutate(cluster_name = factor(cluster_name,
                                            levels = c("dark","elongated","flakes","fluffy", "agglomerated")))

# PCA ref - Dim. 1 and 2
PCA_ref_1_2 <- ggplot()+
  geom_point(aes(x = Dim.1, y = Dim.2, color = as.factor(cluster_name)), data = slice_sample(morpho_diversity_ref, prop = 0.3), size = 0.2, alpha = 0.3)+
  geom_point(aes(x = barycenter_dim1, y = barycenter_dim2, shape = cluster_name), size = 3, alpha = 1, data = centers_init_ref)+
  scale_color_viridis_d(guide = "none")+
  labs(shape = "cluster", title = "Reference - Dim 1 and 2")+
  theme_minimal() +
  theme(legend.position = "none")

# PCA ref - Dim. 3 and 4
PCA_ref_3_4 <- ggplot()+
  geom_point(aes(x = Dim.3, y = Dim.4, color = as.factor(cluster_name)), data = slice_sample(morpho_diversity_ref, prop = 0.3), size = 0.2, alpha = 0.3)+
  geom_point(aes(x = barycenter_dim3, y = barycenter_dim4, shape = cluster_name), size = 3, alpha = 1, data = centers_init_ref)+
  scale_color_viridis_d(guide = "none")+
  labs(shape = "cluster", title = "Reference - Dim 3 and 4")+
  theme_minimal() +
  theme(legend.position = "none")


# PCA with new observations from the MCA - Dim. 1 and 2
PCA_new_1_2 <- ggplot()+
  geom_point(aes(x = Dim.1, y = Dim.2), data = slice_sample(morpho_diversity_ref, prop = 0.3), shape = ".", alpha = 0.5)+
  geom_point(aes(x = Dim.1, y = Dim.2, color = cluster_name), data = slice_sample(taxa_morpho_m4, prop = 0.5), size = 0.2, alpha = 0.7)+
  geom_point(aes(x = barycenter_dim1, y = barycenter_dim2, shape = cluster_name), size = 3, alpha = 1, data = centers_init_ref)+
  scale_color_viridis_d(guide = "none")+
  labs(shape = "cluster", title = "New obs - Dim 1 and 2")+
  theme_minimal() +
  theme(legend.position = "bottom")

# PCA with new observations from the MCA - Dim. 3 and 4
PCA_new_3_4 <- ggplot()+
  geom_point(aes(x = Dim.3, y = Dim.4), data = slice_sample(morpho_diversity_ref, prop = 0.3), shape = ".", alpha = 0.5)+
  geom_point(aes(x = Dim.3, y = Dim.4, color = as.factor(cluster_name)), data = slice_sample(taxa_morpho_m4, prop = 0.5), size = 0.2, alpha = 0.7)+
  geom_point(aes(x = barycenter_dim3, y = barycenter_dim4, shape = cluster_name), size = 3, alpha = 1, data = centers_init_ref)+
  scale_color_viridis_d(guide = "none")+
  labs(shape = "cluster (see Trudnowska et al. 2021)", title = "New obs - Dim 3 and 4")+
  theme_minimal() +
  theme(legend.position = "none")

# Plot position of new objects with their clusters
PCA_ref_1_2 + PCA_ref_3_4 + PCA_new_1_2 + PCA_new_3_4

ggsave(
  "graphs/supp_m4_morpho_PCA_clusters.png", 
  dpi    = 400,                  
  width  = 12,
  height = 10)  


## d. Morpho-shannon index ----
## Count number of objects per clusters (used like species)
clust_summary <- taxa_morpho_m4 %>% 
  filter(depth_bin < 200) %>% # filter the 200m first meters because large changes deeper (see Trudnowska et al. 2021)
  group_by(station, sample_id, lat, lon, cluster_name) %>% 
  summarise(tot_conc= sum(conc)) %>% #instead of counts? 
  ungroup()

## Transform the datatable and convert as a count matrix
clust_wide <- clust_summary %>%
  select(sample_id, cluster_name, tot_conc) %>%
  pivot_wider(names_from = cluster_name, values_from = tot_conc, values_fill = 0)
count_matrix <- as.matrix(clust_wide[, -1])

## Compute Shannon index (0-200m)
shannon_index <- diversity(count_matrix, index = "shannon")

## Results
taxa_4_shannon <- distinct(taxa_morpho_m4, station, sample_id, lat, lon) %>% 
  left_join(tibble(sample_id = clust_wide$sample_id,shannon = shannon_index)) %>% 
  rename(m4_shannon_morpho = shannon) 

ggplot() +
  geom_polygon(mapping=aes(x=lon, y=lat, group=group), data=coast) + # coastline
  geom_label_repel(data=taxa_4_shannon,aes(lon, lat, label = station), 
                   segment.alpha = 0.3, size = 2.5)                + # station labels
  geom_point(data=taxa_4_shannon, aes(lon, lat, color = m4_shannon_morpho), size=4)      + # stations
  scale_color_gradientn(colors = cols)                            + # stations' color palette
  labs(x= "Longitude (°E)", y= "Latitude (°N)", color = "Morpho-Shannon index")                    +
  theme_bw() + 
  coord_quickmap(xlim=c(-57, -53), ylim = c(51.6, 54))               # map limits

ggsave(
  "graphs/m4_map_morpho_shannon.png", # the name
  dpi    = 400,                   # the resolution
  width  = 8,
  height = 7)  

# See the influence of the different clusters to diversity
clust_summary %>% 
  ggplot() +
  facet_wrap(~ cluster_name) +
  geom_polygon(mapping=aes(x=lon, y=lat, group=group), data=coast) + # coastline
  geom_label_repel(aes(lon, lat, label = station), 
                   segment.alpha = 0.3, size = 2.5)                + # station labels
  geom_point( aes(lon, lat, color = tot_conc), size=4)      + # stations
  scale_color_gradientn(colors = cols)                            + # stations' color palette
  labs(x= "Longitude (°E)", y= "Latitude (°N)", color = "#/L")                    +
  theme_bw() + 
  coord_quickmap(xlim=c(-57, -53), ylim = c(51.6, 54))               # map limits

ggsave(
  "graphs/supp_m4_clusters_distrib.png", # the name
  dpi    = 400,                   # the resolution
  width  = 12,
  height = 9)  

# Remove now useless objects
remove(centers_init_ref, centres_ref_coord, count_matrix, dist_sq,
       new_mat, new_obs_coord, ref_mat, idx_ref, idx_sup, 
       PCA_new_1_2, PCA_new_3_4, PCA_ref_1_2, PCA_ref_3_4, 
       shannon_index)

## Plot distribution of particles abundances within clusters along stations with
# increasing Shannon indices 
clust_summary %>% 
  left_join(taxa_4_shannon) %>% 
  ggplot(aes(x = m4_shannon_morpho, y = tot_conc, color = cluster_name))    +
  geom_segment(aes(xend=m4_shannon_morpho, y=0, yend=tot_conc, color = cluster_name)) + # segment of the lollipop
  geom_point(size = 2.5)                              + # point of the lollipop
  geom_smooth(se = FALSE, linewidth = 0.5)+
   labs(
    x    = "morpho-Shannon",
    y    = "conc. (#/L)", 
    color = "cluster")                                   +
  theme_bw()                                          +
  theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0.5)) # present the station IDs vertically

ggsave(
  "graphs/supp_m4_concentrations_in_clusters.png", # the name
  dpi    = 400,                   # the resolution
  width  = 8,
  height = 4)  


# Metric 5 - Average copepods densities (ind/L)  ----
## Explanation: average densities of all copepods (>600 microns), the dominant zooplankton taxa, in the first and last 50 meters of the water column
## Calculation: 
## Compute copepod densities per depth-bin
copepod_densities_db <- taxa_db %>% 
  # keep only categories belonging to the Copepoda class and children categories of interest
  filter(category %in% c("Copepoda<Multicrustacea", "Calanoida", "Heterorhabdidae", 
         "Calanus", "Paraeuchaeta", "Metridia", "female+eggs<Paraeuchaeta", "copepoda eggs")) %>% 
  #compute copepod densities %>% 
  mutate(ind_nb = 1) %>% 
  group_by(cruise, ship, lat, lon, date, station, sample_id, depth_bin, sampled_volume) %>% 
  summarise(tot_cop = sum(ind_nb)) %>% 
  ungroup() %>% 
  mutate(cop_dens = tot_cop/sampled_volume)

# Plot vertical distribution
copepod_densities_db %>% 
  group_by(sample_id) %>% 
  mutate(
    max_depth = max(depth_bin, na.rm = TRUE)) %>% 
  ungroup() %>% 
  ggplot()+
  geom_point(aes(x=cop_dens, y= -depth_bin, color = sample_id), alpha = 0.5, size = 0.1)+
  geom_hline(aes(yintercept = -max_depth, color = sample_id), alpha = 0.2)+
  geom_smooth(
    aes(x = cop_dens, y = -depth_bin, color = sample_id, group = sample_id),
    orientation = "y", se = FALSE, alpha = 0.2, linewidth = 0.3)+
  labs(x= "Copepods density (ind.L-1)", y= "Depth bin (m)", color = "Sample")   +
  theme_bw() 
# -> copepods have a bi-modal distribution: close to the surface and close to the sea bottom

ggsave(
  "graphs/supp_m5_copepods_verticaldistrib.png", # the name
  dpi    = 400,                   # the resolution
  width  = 8,
  height = 7)  

# Compute copepods densities close to the surface (0-50m) and close to the sea floor (50m-bottom)
cop_dens_summary <- copepod_densities_db %>%
  group_by(cruise, ship, station, lat, lon, date, sample_id) %>%
  mutate(
    max_depth = max(depth_bin, na.rm = TRUE)
  ) %>%
  summarise(
    mean_cop_surface_0_50 = mean(
      cop_dens[depth_bin <= 50],
      na.rm = TRUE
    ),
    mean_cop_bottom_50 = mean(
      cop_dens[depth_bin >= (max_depth - 50)],
      na.rm = TRUE
    ),
    max_depth = first(max_depth),
    .groups = "drop"
  )

taxa_5_copepods <- cop_dens_summary %>%
  mutate(avrg_cop_dens = (mean_cop_surface_0_50 + mean_cop_bottom_50)/2) %>% 
  select(cruise:sample_id, max_depth, m5_cop_dens = avrg_cop_dens)
# -> m5 a cop_density is in #/L
# -> it represents the average density of copepods at the surface or at the bottom, 
#    no matter the depth of the profile
# -> you can read at station HC-02 there is on average 0.22 copepod/L (220 copepod/L)

ggplot() +
  geom_polygon(mapping=aes(x=lon, y=lat, group=group), data=coast) + # coastline
  geom_label_repel(data=taxa_5_copepods,aes(lon, lat, label = station), 
                   segment.alpha = 0.3, size = 2.5)                + # station labels
  geom_point(data=taxa_5_copepods, aes(lon, lat, color = m5_cop_dens), size=4)      + # stations
  scale_color_gradientn(colors = cols)                            + # stations' color palette
  labs(x= "Longitude (°E)", y= "Latitude (°N)", color = "Copepod densities 
(ind.L-1)")                    +
  theme_bw() + 
  coord_quickmap(xlim=c(-57, -53), ylim = c(51.6, 54))               # map limits

ggsave(
  "graphs/m5_map_cop_dens.png", # the name
  dpi    = 400,                   # the resolution
  width  = 8,
  height = 7)  

# Metric 6 - Average large copepod densities (ind/L) ----
## Explanation: average density of copepods sizing more than 2mm (presumably adult Calanus copepods) in the first and
## last 50 metres of the water column.
## Calculation: 
large_cop_db <- taxa_morpho_db %>% 
  left_join(select(taxa_db, sample_id, object_id, depth_bin, sampled_volume)) %>% 
  # select metrics of interest
  select(station:depth, depth_bin, sampled_volume, object_major) %>% 
  # filter copepods in the dataset that contains morphological information on images
  filter(category %in% c("Copepoda<Multicrustacea", "Calanoida", "Heterorhabdidae", 
                         "Calanus", "Paraeuchaeta", "Metridia", "female+eggs<Paraeuchaeta", "copepoda eggs")) %>% 
  # compute a size based on the number of pixels and the pixel pitch
  mutate(copepod_size_um = object_major*image_pixelsize) %>%
  filter(copepod_size_um > 2000) %>% 
  group_by(station, lat, lon, sample_id, depth_bin, sampled_volume) %>%
  summarise(large_cop_nb = n()) %>% 
  mutate(large_cop_dens = large_cop_nb/sampled_volume)

# Surface (0-50m) and sea floor (50m-bottom)
large_cop_dens_summary <- large_cop_db %>%
  group_by(station, lat, lon, sample_id) %>%
  mutate(
    max_depth = max(depth_bin, na.rm = TRUE)
  ) %>%
  summarise(
    mean_largecop_surface_0_50 = mean(
      large_cop_dens[depth_bin <= 50],
      na.rm = TRUE
    ),
    mean_largecop_bottom_50 = mean(
      large_cop_dens[depth_bin >= (max_depth - 50)],
      na.rm = TRUE
    ),
    max_depth = first(max_depth),
    .groups = "drop"
  )

taxa_6_large_cop <- large_cop_dens_summary %>%
  mutate(avrg_largecop_dens = (mean_largecop_surface_0_50 + mean_largecop_bottom_50)/2) %>% 
  select(station:sample_id, max_depth, m6_largecop_dens = avrg_largecop_dens)


# Map :
ggplot() +
  geom_polygon(mapping=aes(x=lon, y=lat, group=group), data=coast) + # coastline
  geom_label_repel(data=taxa_6_large_cop, aes(lon, lat, label = station), 
                   segment.alpha = 0.3, size = 2.5)                + # station labels
  geom_point(data=taxa_6_large_cop, aes(lon, lat, color = m6_largecop_dens), size=4)      + # stations
  scale_color_gradientn(colors = cols)                            + # stations' color palette
  labs(x= "Longitude (°E)", y= "Latitude (°N)", color = "Copepods >2mm
(ind.L-1)")                    +
  theme_bw() + 
  coord_quickmap(xlim=c(-57, -53), ylim = c(51.6, 54))               # map limits

ggsave(
  "graphs/m6_map_largecop_dens.png", # the name
  dpi    = 400,                   # the resolution
  width  = 8,
  height = 7)  


# Scores ----

## Score 1: Particles and plankton abundance (m2, m3, m5) ----
## Explanation: This score from 0 to 3 is relative to the quantity of plankton and 
# other drifting particles. It is an average of the biovolume, slope and copepod density metrics. 
# All the metrics are interpolated from 0 to 3 before being averaged.
# The pmin function is used so that if a value of a variable is greater than the upper boudary, 
# it takes the upper boundary as value.


score_1 <- part_2_biovol                         |>
  mutate(
    rel_biovol  = pmin(m2_part_biovol, 10) * 3/10) |>              # Biovolume interpolation
  select(-m2_part_biovol)                          |>              # remove the initial biovolume variable
  mutate(
    rel_slope   =  part_3_slope$m3_part_slope                  ,   # Slope interpolation
    rel_slope   =  case_when(
      rel_slope <= -5.5 ~ 0,
      rel_slope >= -2   ~ 3,
      TRUE              ~ 3 * (rel_slope + 5.5) / 3.5)         , 
    rel_cop     =  pmin(taxa_5_copepods$m5_cop_dens, 5) * 3/5,   # copepod density interpolation
    score1       =  (rel_biovol + rel_slope + rel_cop) / 3)         # score = average of the 3 variables

# look at the distribution of each variable, in the 0-3 range :
hist(score_1$rel_biovol)
hist(score_1$rel_slope )
hist(score_1$rel_cop)
hist(score_1$score1)


## Score 2: Particles and plankton abundance (m4 only) ----
## -> m4 is assigned to Score 2 in the final dataset

# Final dataset and map ----
uvp_metrics <- distinct(taxa_db, cruise, ship, station, date, lat, lon, sample_id) %>% 
  left_join(distinct(part_db, ecopart_project_name, sample_id)) %>% 
  left_join(part_1_dens)     %>% 
  left_join(part_2_biovol)   %>% 
  left_join(part_3_slope)    %>% 
  left_join(taxa_4_shannon)    %>% 
  left_join(taxa_5_copepods) %>%
  left_join(select(taxa_6_large_cop, sample_id, m6_largecop_dens)) %>% 
  left_join(score_1 %>% select(-c(rel_biovol, rel_slope, rel_cop))) %>% 
  mutate(score2 = m4_shannon_morpho) %>% # m4 corresponds to Score 2
  select(ecopart_project_name, cruise:sample_id, max_cast_depth = max_depth, everything())
head(uvp_metrics)

# Plot in a map :
score1 <- ggplot() +
  geom_polygon(mapping=aes(x=lon, y=lat, group=group), data=coast) + # coastline
  geom_label_repel(data=uvp_metrics,aes(lon, lat, label = station), 
                   segment.alpha = 0.3, size = 2.5)                + # station labels
  geom_point(data=uvp_metrics, aes(lon, lat, color = score1), size=4) + # stations
  scale_color_gradientn(colors = cols)                             + # stations' color palette
  labs(x= "Longitude (°E)", y= "Latitude (°N)", color = "Score 1",
       title = "Proxy of particules and plankton quantity")   +
  theme_bw() + 
  coord_quickmap(xlim=c(-57, -53), ylim = c(51.6, 54))               # map limits

score2 <- ggplot() +
  geom_polygon(mapping=aes(x=lon, y=lat, group=group), data=coast) + # coastline
  geom_label_repel(data=uvp_metrics,aes(lon, lat, label = station), 
                   segment.alpha = 0.3, size = 2.5)                + # station labels
  geom_point(data=uvp_metrics, aes(lon, lat, color = score2), size=4) + # stations
  scale_color_gradientn(colors = cols)                             + # stations' color palette
  labs(x= "Longitude (°E)", y= "Latitude (°N)", color = "Score 2",
       title = "Proxy of particules and plankton diversity (equitable distribution)")   +
  theme_bw() + 
  coord_quickmap(xlim=c(-57, -53), ylim = c(51.6, 54))               # map limits

score1 / score2

# Export the plot :
ggsave(
  "graphs/scores_final_map.png", # the name
  dpi    = 400,           # the resolution
  width  = 7,
  height = 10)  


# Write final dataset ----
project_name <- uvp_metrics$ecopart_project_name[1]
project_name <- str_replace_all(project_name, "[^[:alnum:]_]+", "_")
filename <- paste0("final_datasets/uvp_metrics_", project_name, ".csv")

write_csv(uvp_metrics, filename)


